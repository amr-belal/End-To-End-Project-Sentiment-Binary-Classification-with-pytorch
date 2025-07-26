
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



import pandas as pd
import torch
import json
from torch.utils.data import TensorDataset
from data.DataLoad import load_data_from_datasets
from app import utils

MAX_LEN = 100
PAD_TOKEN = "<PAD>"
UNK_TOKEN = "<UNK>"
TRAIN_PATH = "data/train.csv"
TEST_PATH = "data/test.csv"
VOCAB_PATH = "artifacts/train_vocab.json"
TRAIN_SAVE_PATH = "artifacts/train_dataset.pt"
TEST_SAVE_PATH = "artifacts/test_dataset.pt"


df_train = load_data_from_datasets("imdb"  , 'train')
df_test  = load_data_from_datasets("imdb"  , 'test')

with open(VOCAB_PATH, "r") as f:
    vocab_data = json.load(f)
vocab = vocab_data




def encode_sentence(sentence, vocab, max_len):
    tokens = sentence.lower().split()
    token_ids = [vocab.get(token, vocab[UNK_TOKEN]) for token in tokens]
    token_ids = token_ids[:max_len]
    token_ids += [vocab[PAD_TOKEN]] * (max_len - len(token_ids))
    return token_ids



def encode(text, vocab, max_len=100):
    tokens = utils.tokenize_text(text)
    ids = [vocab.get(token, vocab["<UNK>"]) for token in tokens[:max_len]]
    # Ensure all ids are valid indices for embedding
    vocab_size = len(vocab)
    ids = [id if id < vocab_size else vocab["<UNK>"] for id in ids]
    if len(ids) < max_len:
        ids += [vocab['<PAD>']] * (max_len - len(ids))
    return ids


def process_data(df, save_path):
    # df = pd.read_csv(csv_path)
    encoded_texts = [encode(text, vocab, MAX_LEN) for text in df["text"]]
    labels = df["label"].tolist()
    
    X_tensor = torch.tensor(encoded_texts, dtype=torch.long)
    y_tensor = torch.tensor(labels, dtype=torch.long)
    
    dataset = TensorDataset(X_tensor, y_tensor)
    torch.save(dataset, save_path)
    print(f"✅ Saved dataset: {save_path}")
    
    
    
if __name__ == "__main__":
    process_data(df_train, TRAIN_SAVE_PATH)
    process_data(df_test, TEST_SAVE_PATH)