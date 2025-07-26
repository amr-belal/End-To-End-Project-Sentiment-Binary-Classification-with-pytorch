import torch
import torch.nn as nn
import torch.optim as optim
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd



        

class SentimentLSTM(nn.Module):
    
    def __init__(self  , vocab_len , emdedding_dim , hidden_dim , output_dim , pad_idx):
        super().__init__()
        
        self. embedding = nn.Embedding(vocab_len,emdedding_dim)
        self.lstm  = nn.LSTM(emdedding_dim , hidden_dim,batch_first=True)
        self.fc =  nn.Linear(hidden_dim , output_dim)
        
        self.dropout = nn.Dropout(0.3)
        
        
    def forward(self, x):
    # x shape: [batch_size, seq_len]
        embedded = self.embedding(x)                      # [batch_size, seq_len, embed_dim]
        output, (hidden, cell) = self.lstm(embedded)      # hidden: [1, batch_size, hidden_dim]
        hidden = hidden.squeeze(0)                        # [batch_size, hidden_dim]
        out = self.fc(hidden)                             # [batch_size, output_dim]
        return out

    
