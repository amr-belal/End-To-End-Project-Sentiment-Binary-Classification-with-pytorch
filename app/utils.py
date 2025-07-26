
import re 
from collections import Counter
# from nltk.tokenize import word_tokenize
import json
import pickle
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text.lower()

def tokenize_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return [word for word in text.split()]

def build_vocab( text ):
    
    all_tokens = [ tokenize_text(text) for text in text]

    tokens_flat = [token for sublist in all_tokens for token in sublist ]

    vocab = Counter(tokens_flat)


    vocab = {word: i+2 for i, (word, freq) in enumerate(vocab.items()) if freq > 5}  # remove rare words
    vocab['<PAD>'] = 0
    vocab['<UNK>'] = 1
    
    return {
        "vocab": vocab,
        "vocab_size": len(vocab),
        "all_tokens": all_tokens
    }


def save_vocab(vocab_dict ,filepath):
    with open(filepath ,'w',encoding='utf-8') as f:
        json.dump(vocab_dict, f,indent=4)
        


def load_vocab(file_path):
    with open(file_path , "r", encoding="utf-8") as f:
        vocab = json.load(f)
    return vocab


def text_to_sequence(text ,vocab):
    tokens = tokenize_text(text)
    return [vocab.get(token, vocab["<UNK>"]) for token in tokens]



# example use in other files 
# from utils import build_vocab, save_vocab, load_vocab, text_to_sequence

# # Example
# vocab_data = build_vocab(list(df["text"]))
# save_vocab(vocab_data["vocab"], "vocab.json")

# # Later in another script
# vocab = load_vocab("vocab.json")
# sequence = text_to_sequence("This is a test", vocab)
