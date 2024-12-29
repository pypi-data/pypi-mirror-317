"""
Usage:
    python 1_load.py --path_to_chat_db ~/Library/Messages/chat.db --path_to_contacts_vcf ~/Desktop/contacts.vcf

Purpose:
    Loads chat.db and contacts.vcf, and saves them to cache for downstream analyses.
    Must be run before `2_plot.py`
"""
import pickle
from typing import Dict, List
import pandas as pd
import os
import argparse
from imess.macosx.chats import load_chats
from imess.macosx.contacts import Contact, load_contacts, merge_contacts, standardize_phone_number
from imess.utils.utils import get_path_to_data

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_chat_db', type=str, default=get_path_to_data('chat.db'), help='Path to the chat.db file (in a readable location)')
    parser.add_argument('--path_to_contacts_vcf', type=str, default=get_path_to_data('contacts.vcf'), help='Path to a .vcf file containing your contacts')
    parser.add_argument('--path_to_merges_txt', type=str, default=None, help='Path to a .txt file containing contact merges')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Cache paths
    os.makedirs(get_path_to_data('cache'), exist_ok=True)
    path_to_contacts_cache = get_path_to_data('cache/contacts.pkl')
    path_to_chats_cache = get_path_to_data('cache/df_chats.parquet')

    # Validate inputs
    if args.path_to_merges_txt == 'None':
        args.path_to_merges_txt = None
    if args.path_to_merges_txt is not None and not os.path.exists(args.path_to_merges_txt):
        print(f"Error: Merges file `{args.path_to_merges_txt}` does not exist")
        exit(1)

    # Load contacts
    contacts: List[Contact] = load_contacts(args.path_to_contacts_vcf)
    print(f"Loaded {len(contacts)} contacts from {args.path_to_contacts_vcf}")
    pickle.dump(contacts, open(path_to_contacts_cache, 'wb'))
    
    # Load custom merges
    if args.path_to_merges_txt is not None:
        with open(args.path_to_merges_txt, 'r') as f:
            merges: List[List[str]] = [line.strip().split(',') for line in f.readlines()]
        print(f"Loaded {len(merges)} merges from `{args.path_to_merges_txt}`")
        # Merge contacts
        contacts = merge_contacts(contacts, merges)
        print(f"New # of contacts: {len(contacts)}")

    # Load chat messages
    print(f"Loading chat messages from `{args.path_to_chat_db}`")
    df: pd.DataFrame = load_chats(args.path_to_chat_db, contacts)
    print(f"Saved `df` of chats to `{path_to_chats_cache}`")
    df.to_parquet(path_to_chats_cache, index=False)
    print("Columns in `df`:", df.columns)

    # Do analysis
    print(">"*20, "Analysis", "<"*20)
    print("="*20, "Chats", "="*20)
    print("Total # of chats:", len(df['chat_id'].unique()))
    print("="*20, "Messages", "="*20)
    print("Total # of messages:", len(df))
    print("Max # of messages in a chat:", df['chat_id'].value_counts().max(), "(", df['chat_name'].value_counts().idxmax(), ")")
    print("Min # of messages in a chat:", df['chat_id'].value_counts().min(), "(", df['chat_name'].value_counts().idxmin(), ")")
    print("Median # of messages in a chat:", df['chat_id'].value_counts().median())
    print("="*20, "Characters", "="*20)
    print("Total # of characters:", df['char_count'].sum())
    print("Max # of characters in a chat:", df.groupby('chat_id')['char_count'].sum().max(), "(", df.groupby('chat_id')['char_count'].sum().idxmax(), ")")
    print("Min # of characters in a chat:", df.groupby('chat_id')['char_count'].sum().min(), "(", df.groupby('chat_id')['char_count'].sum().idxmin(), ")")
    print("Median # of characters in a chat:", df.groupby('chat_id')['char_count'].sum().median())
    print("="*20, "Contacts", "="*20)
    print("Total # of known contacts:", len(contacts))
    print("Total # of people who sent >= 1 message:", len(df['sender_id'].unique()))
    print("Max # of messages per contact:", df['sender_id'].value_counts().max(), "(", df['sender_name'].value_counts().idxmax(), ")")
    print("Min # of messages per contact:", df['sender_id'].value_counts().min(), "(", df['sender_name'].value_counts().idxmin(), ")")
    print("Median # of messages per contact:", df['sender_id'].value_counts().median())
    print("="*20, "Group Chats (i.e. > 2 people OR named)", "="*20)
    print("Total # of named group chats:", len(df[df['is_named_group_chat'] == True]['chat_name'].unique()))
    print("Total # of unnamed group chats:", len(df[df['is_unnamed_group_chat'] == True]['chat_name'].unique()))
    print("Named groups:", df[df['is_named_group_chat'] == True]['chat_name'].unique())
    print("Done!")

if __name__ == '__main__':
    main()