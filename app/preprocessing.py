import re
import nltk
from nltk.tokenize import word_tokenize


# encode tokens

# def encode(text, vocab, max_len=100):
#     tokens = word_tokenize(text)
#     ids = [vocab.get(token, vocab["<UNK>"]) for token in tokens[:max_len]]
#     # Ensure all ids are valid indices for embedding
#     vocab_size = len(vocab)
#     ids = [id if id < vocab_size else vocab["<UNK>"] for id in ids]
#     if len(ids) < max_len:
#         ids += [vocab['<PAD>']] * (max_len - len(ids))
#     return ids


# app/preprocessing.py

import re
import torch

def basic_tokenizer(text):
    # Remove special characters and tokenize
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.lower().split()

def encode_sentence(text, vocab, max_len=100):
    tokens = basic_tokenizer(text)
    ids = [vocab.get(token, vocab["<UNK>"]) for token in tokens]
    # Padding or truncating
    if len(ids) < max_len:
        ids += [vocab["<PAD>"]] * (max_len - len(ids))
    else:
        ids = ids[:max_len]
    return torch.tensor(ids).unsqueeze(0)
