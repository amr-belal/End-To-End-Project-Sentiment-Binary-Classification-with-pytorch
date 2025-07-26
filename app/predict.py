import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
from app.model import SentimentLSTM
from app.utils import load_vocab, tokenize_text

import torch.nn.functional as F


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vocab_path = os.path.join(BASE_DIR, "artifacts", "train_vocab.json")

vocab = load_vocab(vocab_path)


# vocab = load_vocab("artifacts/train_vocab.json")
pad_token = "<PAD>"
pad_idx = vocab[pad_token]



model = SentimentLSTM(len(vocab), emdedding_dim=100, hidden_dim=128, output_dim=2, pad_idx=pad_idx)
os.makedirs("artifacts", exist_ok=True)  # تأكد إن المجلد موجود

# torch.save(model.state_dict(), "artifacts/sentiment_model.pt")
# print("✅ Model saved to artifacts/sentiment_model.pt")

model.load_state_dict(torch.load("artifacts/sentiment_model.pt", map_location=device))
model.eval()




def predict_statement(text):
    tokens = tokenize_text(text)
    indices = [vocab.get(token, vocab["<UNK>"]) for token in tokens]

    max_len = 100
    if len(indices) < max_len:
        indices += [pad_idx] * (max_len - len(indices))
    else:
        indices = indices[:max_len]

    input_tensor = torch.tensor([indices], dtype=torch.long).to(device)
    output = model(input_tensor)  # [1, 2]
    
    probs = F.softmax(output, dim=1)
    confidence, pred = torch.max(probs, dim=1)
    
    sentiment = "positive" if pred.item() == 1 else "negative"
    return sentiment, round(confidence.item(), 3)

