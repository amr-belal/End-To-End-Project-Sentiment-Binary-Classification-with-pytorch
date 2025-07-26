
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import torch
import torch.nn as nn
from app.model import SentimentLSTM
from app.dataloader import get_dataloader
from app.utils import load_vocab

def evaluate_model():
    # 
    BATCH_SIZE = 32
    EMBEDDING_DIM = 100
    HIDDEN_DIM = 128
    OUTPUT_DIM = 2
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pad_token = "<PAD>"
    #vocab
    vocab = load_vocab("artifacts/train_vocab.json")
    vocab_size = len(vocab)
    pad_idx = vocab[pad_token]

    # تحميل الموديل
    model = SentimentLSTM(vocab_size, EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM, pad_idx)
    model.load_state_dict(torch.load("artifacts/sentiment_model.pt"))
    model.to(DEVICE)
    model.eval()

    # test dataloader
    test_loader = get_dataloader("artifacts/test_dataset.pt", BATCH_SIZE, shuffle=False)

    
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            preds = torch.argmax(outputs, dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    acc = correct / total
    print(f"\n✅ Test Accuracy: {acc * 100:.2f}%\n")

if __name__ == "__main__":
    evaluate_model()
    print("Model evaluation completed.")