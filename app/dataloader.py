import torch
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset

# السماح لـ TensorDataset
torch.serialization.add_safe_globals([TensorDataset])

def get_dataloader(dataset_path , batch_size , shuffle =True):
    
    dataset = torch.load(dataset_path, weights_only=False)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    
    return dataloader


