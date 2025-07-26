

from fastapi  import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from predict import predict_statement

# التحقق من وجود الموديل قبل التحميل
model_path = "artifacts/sentiment_model.pt"
if not os.path.exists(model_path):
    print("❌ Model file not found!")
    print("Please run: python train_model.py first")
    print("Or check if the artifacts folder exists")



app = FastAPI(title="Sentiment Analysis API" , )

app.mount("/static", StaticFiles(directory="frontend"), name="static")


class InputText(BaseModel):
    text :str 


@app.get("/health")
def home():
    return {"message": "Welcome to the Sentiment Analysis API"}



@app.post("/predict")
def get_prediction(input_text: InputText):
    sentiment= predict_statement(input_text.text)
    
    sentiment_label = "positive" if sentiment == 1 else "negative"
    return {
        "input": input_text.text,
        "prediction": {
            "sentiment": sentiment,
          
        }
    }
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/home.html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)