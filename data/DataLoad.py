from datasets import load_dataset
import pandas as pd
# load data 
def load_data_from_datasets(data_name  , splits_type):
    dataset = load_dataset(data_name)
    
    dataset = dataset[splits_type].to_pandas()
    return dataset


def load_data_pandas_csv(csv_path):
    return pd.read_csv(csv_path)


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
