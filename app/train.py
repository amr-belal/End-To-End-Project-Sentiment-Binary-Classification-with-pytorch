import torch
import torch.nn as nn
import torch.optim as optim
from app.model import SentimentLSTM
from app.dataloader import get_dataloader


def train_model(vocab , pad_token , device):
    BATCH_SIZE = 32
    EMBEDDING_DIM = 100
    HIDDEN_DIM = 128
    OUTPUT_DIM = 2
    EPOCHS = 5
    
    pad_idx = vocab[pad_token]
    
    vocab_size =  len(vocab)
    
    model = SentimentLSTM(vocab_size  , EMBEDDING_DIM , HIDDEN_DIM , OUTPUT_DIM , pad_idx)
    
    model = model.to(device)
    
    optimizer = optim.Adam(model.parameters() , lr = 0.001)
    
    criterion = nn.CrossEntropyLoss()
    
    train_loader = get_dataloader("artifacts/train_dataset.pt" ,batch_size=32 , shuffle=True)
    test_loader  = get_dataloader("artifacts/test_dataset.pt" , BATCH_SIZE , shuffle=False)
    
    
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        
        for batch in train_loader:
            inputs , labels = batch
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs,labels)
            loss.backward()
            optimizer.step()
            
            total_loss +=loss.item()
            
        avg_loss = total_loss / len(train_loader)
        print(f"🔁 Epoch {epoch+1}/{EPOCHS} - Loss: {avg_loss:.4f}")
    
    #save
    torch.save(model.state_dict(), "artifacts/sentiment_model.pt")
    print("✅ Model saved to: artifacts/sentiment_model.pt")