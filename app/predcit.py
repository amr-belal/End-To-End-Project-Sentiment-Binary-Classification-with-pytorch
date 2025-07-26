import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
from app.model import SentimentClassifier
from app.utils import load_vocab, preprocess_text


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SentimentClassifier(input_dim=10000, hidden_dim=256, output_dim=1)
model.load_state_dict(torch.load("artifacts/sentiment_model.pt", map_location=device))
model.eval()


vocab = load_vocab("artifacts/train_vocab.json")
pad_token = "<PAD>"
pad_idx = vocab[pad_token]



def predict_statement(text):
    tokens = preprocess_text(text)
    indices = [vocab.get(token, vocab["<UNK>"]) for token in tokens]
    
    max_len = 100 
    if len(indices) <max_len :
        indices += [pad_idx ] *(max_len - len(indices))
        
    else : 
        indices = indices[:max_len]
    
    
    input_tensor = torch.tensor([indices], dtype=torch.long).to(device)
    
    output = model(input_tensor)
    
    prediction  = torch.sigmoid(output).item()
    
    sentiment = "positive" if prediction > 0.5 else "negative"
    
    return sentiment


