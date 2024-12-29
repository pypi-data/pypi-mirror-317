"""
Usage:
    python analyze.py --plot top_K_chats_with_sender_counts

Purpose:
    Generate a specific set of plots.
    Must run `imess_load` first.
"""
import datetime
import pickle
import random
from typing import Dict, List, Optional
import pandas as pd
import os
import argparse
from tqdm import tqdm
import Levenshtein
from imess.macosx.chats import MYSELF_SENDER_ID,  map_contacts_to_chat_id
from imess.macosx.contacts import Contact, merge_contacts
from imess.utils.modules import output_chat_history, plot_specific_chat_over_time, plot_top_K_chats_with_sender_counts, plot_top_K_chats_over_time
from imess.utils.plots import word_cloud__from_text
from imess.utils.utils import get_path_to_data, get_rel_path, hash_with_seed, sanitize_filename
from multiprocessing import Pool

MODES = ['top_K_chats_with_sender_counts', 'top_K_chats_over_time', 'specific_chat_over_time', 'specific_chat_word_cloud', 'output_chat_history']

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=MODES, help='Name of the analysis to run')
    parser.add_argument('--is_anon', action='store_true', default=False, help='If TRUE, then anonymize all Chat and Sender names in plots')
    # top_K_chats_with_sender_counts, top_K_chats_over_time
    parser.add_argument('--K', type=int, default=20, help='Number of chats to plot. Defaults to 20. Used for: top_K_chats_with_sender_counts, top_K_chats_over_time')
    # specific_chat_over_time
    parser.add_argument('--senders', type=str, default=None, help='A comma-separated list of senders from the chat you want to plot. Provide the string "me" for yourself. Used for: specific_chat_over_time. Example: `+19380944490,myself@gmail.com,+4990099999,+11111111111`')
    parser.add_argument('--chat', type=str, default=None, help='Name of the chat you want to plot. Used for: specific_chat_over_time. Example: `Family`')
    # Input/output paths
    parser.add_argument('--path_to_merges_txt', type=str, default=None, help='Path to a .txt file containing contact merges')
    parser.add_argument('--path_to_output_dir', type=str, default='./plots/', help='Path to where output plots will be saved')
    return parser.parse_args()

def map_args_to_chat_id(args, df: pd.DataFrame, contacts: List[Contact]) -> str:
    """Maps --senders or --chat to a chat ID."""
    # Find correct chat ID for specific chat
    if args.senders is not None:
        # Find chat based on its senders
        #    This works by retrieving the chat ID that matches the most senders (with the least total senders)
        senders: List[str] = args.senders.split(',')
        # Replace 'me' with MYSELF_SENDER_ID
        senders = [ MYSELF_SENDER_ID if x.lower() == 'me' else x for x in senders ]
        # Always make sure MYSELF is added to the list of senders
        if MYSELF_SENDER_ID not in senders:
            senders.append(MYSELF_SENDER_ID)
        # Determine the chat ID corresponding to this list of senders
        chat_id = map_contacts_to_chat_id(df, senders, contacts)
    elif args.chat is not None:
        # Find chat based on its name
        #   This works by retrieving the chat ID that has the smallest Levenshtein distance to `args.chat`
        chat_name: str = args.chat.lower()
        Levenshtein_distances = df['chat_name'].apply(lambda x: Levenshtein.distance(x, chat_name))
        chat_id = df[Levenshtein_distances == Levenshtein_distances.min()]['chat_id'].values[0]
    else:
        raise ValueError(f"Error: Must specify either `senders` or `chat_name` for this plot")
    print(f"Chat ID: {chat_id} | Chat Name: {df[df['chat_id'] == chat_id]['chat_name'].values[0]} | Sender IDs: {df[df['chat_id'] == chat_id]['sender_id'].unique()}")
    return chat_id

def run_top_K_chats_with_sender_counts(args, df: pd.DataFrame):
    assert args.K is not None, "Error: `K` must be specified for this plot"
    assert args.K > 0, "Error: `K` must be greater than 0"
    # Make horizontal stacked bar plots of top `K` chats by character/message count
    plot_top_K_chats_with_sender_counts(df, args.path_to_output_dir, K=args.K)

def run_top_K_chats_over_time(args, df: pd.DataFrame):
    assert args.K is not None, "Error: `K` must be specified for this plot"
    assert args.K > 0, "Error: `K` must be greater than 0"
    # Make line/bar/heatmap plots over time of top `K` chats by character/message count
    plot_top_K_chats_over_time(df, args.path_to_output_dir, K=args.K)
    
def run_specific_chat_over_time(args, df: pd.DataFrame, contacts: List[Contact]):
    # One of senders or chat must be specified, but not both
    assert None in [args.senders, args.chat], "Error: Only one of `senders` and `chat` can be specified"

    # Find correct chat ID for specific chat
    chat_id = map_args_to_chat_id(args, df, contacts)

    # Make line/bar plots over time of the chat
    plot_specific_chat_over_time(df, args.path_to_output_dir, chat_id=chat_id)

def run_specific_chat_word_cloud(args, df: pd.DataFrame, contacts: List[Contact]):
    """Make a word cloud of a specific chat."""
    # One of senders or chat must be specified, but not both
    assert None in [args.senders, args.chat], "Error: Only one of `senders` and `chat` can be specified"

    # Find correct chat ID for specific chat
    chat_id = map_args_to_chat_id(args, df, contacts)
    df = df[df['chat_id'] == chat_id]
    
    # Make directory for this chat
    chat_name: str = df[df['chat_id'] == chat_id]['chat_name'].values[0]
    path_to_output_dir = os.path.join(args.path_to_output_dir, f"Chat - {sanitize_filename(chat_name)}")
    os.makedirs(path_to_output_dir, exist_ok=True)

    # Make word cloud of the chat
    title: str = f"{chat_name} - WordCloud - All"
    word_cloud__from_text(df, max_words=100, is_preprocess_text=True, title=title, path_to_output_dir=path_to_output_dir)


def _run_output_chat_history_worker(args):
    # Unpack arguments since Pool.imap can only take one argument
    df, path_to_output_dir, chat_ids = args
    for chat_id in tqdm(chat_ids, desc='Outputting chat history'):
        output_chat_history(df, path_to_output_dir, chat_id)

def run_output_chat_history(args, df: pd.DataFrame):
    """Output all chat historys to a CSV and TXT file."""
    path_to_output_dir = os.path.join(args.path_to_output_dir, 'chat_history')
    os.makedirs(path_to_output_dir, exist_ok=True)
    
    
    unique_chat_ids: List[str] = df['chat_id'].unique().tolist()
    random.shuffle(unique_chat_ids) # randomize order for better multiprocessing
    
    n_workers: int = 5
    if n_workers == 1:
        _run_output_chat_history_worker((df, path_to_output_dir, unique_chat_ids))
    else:
        chunks_size: int = len(unique_chat_ids) // n_workers
        worker_args = [(df, path_to_output_dir, unique_chat_ids[idx * chunks_size : (idx + 1) * chunks_size]) for idx in range(n_workers)]
        with Pool(n_workers) as pool:
            __ = list(pool.imap(_run_output_chat_history_worker, worker_args))

def main():
    args = parse_args()
    is_anon: bool = args.is_anon
    os.makedirs(args.path_to_output_dir, exist_ok=True)

    # Validate inputs
    if args.path_to_merges_txt == 'None':
        args.path_to_merges_txt = None
    if args.path_to_merges_txt is not None and not os.path.exists(args.path_to_merges_txt):
        print(f"Error: Merges file `{args.path_to_merges_txt}` does not exist")
        exit(1)

    # Load contacts
    path_to_contacts_cache = get_path_to_data('cache/contacts.pkl')
    if not os.path.exists(path_to_contacts_cache):
        print(f"Error: Contacts cache `{path_to_contacts_cache}` does not exist. Please run `python main.py` first.")
        exit(1)
    contacts: List[Contact] = pickle.load(open(path_to_contacts_cache, 'rb'))
    
    # Load custom merges
    if args.path_to_merges_txt is not None:
        with open(args.path_to_merges_txt, 'r') as f:
            merges: List[List[str]] = [line.strip().split(',') for line in f.readlines()]
        print(f"Loaded {len(merges)} merges from `{args.path_to_merges_txt}`")
        # Merge contacts
        contacts = merge_contacts(contacts, merges)
        print(f"New # of contacts: {len(contacts)}")

    # Load chat messages
    path_to_chats_cache = get_path_to_data('cache/df_chats.parquet')
    if not os.path.exists(path_to_chats_cache):
        print(f"Error: Chats cache `{path_to_chats_cache}` does not exist. Please run `python main.py` first.")
        exit(1)
    df: pd.DataFrame = pd.read_parquet(path_to_chats_cache)
    print(f"Loaded {len(df)} total chats from `{path_to_chats_cache}`")

    # If anonymizing, then replace all chat and sender names by the hash of their Chat / Sender IDs
    if is_anon:
        seed = int(datetime.datetime.now().timestamp())
        df['chat_name'] = df['chat_id'].apply(lambda x: hash_with_seed(x, seed)[:10])
        df['sender_name'] = df['sender_id'].apply(lambda x: hash_with_seed(x, seed)[:10])
        args.path_to_output_dir = os.path.join(args.path_to_output_dir, f'anon_{seed}')
        os.makedirs(args.path_to_output_dir, exist_ok=True)
        print(f"Anonymizing all Chat and Sender names in plots using seed: {seed} | Saving results to: {args.path_to_output_dir}")
    
    # Do analysis
    if args.mode == 'top_K_chats_with_sender_counts':
        run_top_K_chats_with_sender_counts(args, df)
    elif args.mode == 'top_K_chats_over_time':
        run_top_K_chats_over_time(args, df)
    elif args.mode == 'specific_chat_over_time':
        run_specific_chat_over_time(args, df, contacts)
    elif args.mode == 'specific_chat_word_cloud':
        run_specific_chat_word_cloud(args, df, contacts)
    elif args.mode == 'output_chat_history':
        run_output_chat_history(args, df)
    else:
        raise ValueError(f"Invalid analysis type: {args.mode}. Must be one of: {MODES}")

if __name__ == '__main__':
    main()