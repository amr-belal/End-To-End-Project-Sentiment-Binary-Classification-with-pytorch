import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# import torch
# from utils import load_vocab
# from train import train_model

# PAD_TOKEN = "<PAD>"
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# if __name__ == "__main__":
#     vocab = load_vocab("artifacts/train_vocab.json")
#     # train_model(vocab, PAD_TOKEN, device)    # train one time 
#     # print("Model training completed.")
    
    


# fast app 

from fastapi  import FastAPI
from pydantic import BaseModel
from app.predcit import predict_statement


app = FastAPI(title="Sentiment Analysis API" , )



class InputText(BaseModel):
    text :str 


@app.get("/")
def home():
    return {"message": "Welcome to the Sentiment Analysis API"}


@app.post("/predict")
def get_prediction(input_text:InputText ):
    return predict_statement(input_text.text)