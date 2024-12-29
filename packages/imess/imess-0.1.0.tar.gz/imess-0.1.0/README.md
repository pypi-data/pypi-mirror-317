# iMessage Analysis

Python scripts to analyze your iMessage data. Completely private and locally hosted. Please see [TODO](__) for more details and examples.

![Example Plot](assets/example.png)

Table of Contents:
1. [💽 Installation](#installation)
2. [⚡️ Quickstart](#quickstart)
3. [🧑‍💻 Advanced](#advanced)


<a name="installation" />

## 💽 Installation
```bash
pip install imess
```

<a name="quickstart" />

## ⚡️ Quickstart

First, load your messages and contacts data.
```bash
# Copy data into /tmp/imess/ so that this script can access it
imess_init

# Preprocess data
imess_load
```

Second, generate plots:
```bash
# General plots (top-K) of all-time
imess_run --mode top_K_chats_with_sender_counts --K 20

# General plots (top-K) of chats over time
imess_run --mode top_K_chats_over_time --K 20

# Plots about a specific named group chat
imess_run --mode specific_chat_over_time --chat <chat-name>

# Plots about a specific set of senders
imess_run --mode specific_chat_over_time --senders <comma-separated-list-of-senders>

# Plots about a specific chat's word cloud
imess_run --mode specific_chat_word_cloud --senders <comma-separated-list-of-senders>

# Outputs all chat histories, one CSV and TXT per chat
imess_run --mode output_chat_history
```

All plots and outputs will be saved to `./plots/`.

<a name="advanced" />

## 🧑‍💻 Advanced

### Install

For local development:
```bash
conda create -n imess python=3.10 -y
conda activate imess
pip install -e .
```

### Merging Contacts

**TODO**

If you have contacts that you want to merge but don't think that's captured in the `contacts.vcf` file, you can provide a `data/merges.txt` file to `imless_load` to specify how you want to merge contacts.

First, create a `data/merges.txt` file. Each row is a separate contact that will be merged into a single contact. The row should contain a comma-separated list of contact info that will be merged into a single contact.

An example is below:

```
test@gmail.com,test@comcast.com,599-559-4499
1121122222,999-999-9999,mom@icloud.com
```

Anytime we see `test@gmail.com`, `test@comcast.com`, or `599-559-4499`, we will merge them into a single contact.

The script `imess_load` will automatically try to load `data/merges.txt`. If you don't want to use this file, you can set the `--path_to_merges_txt` flag to `None` or delete the file.

```bash
imess_load --path_to_merges_txt ./data/merges.txt
```
