import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




import pickle
from app import utils

# with open('train_vocab.json', 'rb') as f:
    # vocab = pickle.dump(f)

vocab = utils.load_vocab("train_vocab.json")
print(len(vocab))
print(vocab)

