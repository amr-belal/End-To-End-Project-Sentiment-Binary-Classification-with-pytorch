import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from app import utils
import pandas as pd   
from data.DataLoad import load_data_from_datasets

df = load_data_from_datasets("imdb","train")


vocab_data = utils.build_vocab(list(df["text"]))
utils.save_vocab(vocab_data["vocab"], "artifacts/train_vocab.json")

# Later in another script
vocab = utils.load_vocab("artifacts/train_vocab.json")
sequence = utils.text_to_sequence("This is a test", vocab)
