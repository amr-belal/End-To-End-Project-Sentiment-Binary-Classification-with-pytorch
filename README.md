# Sentiment Analysis with LSTM (PyTorch + FastAPI)

This is an end-to-end Sentiment Analysis application using LSTM (no Transformers!) built in PyTorch and served via FastAPI.

## 📁 Project Structure

```text
project/
├── app/
│ ├── main.py ← FastAPI app (inference API)
│ ├── model.py ← LSTM model definition
│ ├── predict.py ← Prediction logic
│ ├── preprocessing.py ← Tokenization, cleaning, padding
│ └── utils.py ← Dataset loaders, tokenizer helpers
│ └── train.py ← training loop
│ └── predict.py ←predictions 
| 
├── model/
│ └── sentiment_model.pt ← Trained LSTM model => ipynb data
|
├── data/
│ └── DataLoad.py ← loader
|
|
├── scripts/
│ └── build_vocab.py ←
│ └── encode_text.py ← 
| └── evaluate.py ←model base 
|
├── artifacts/
│ └── sentiment_model.pt ←model base 
│ └── test_data.pt ← test base data
│ └── train_data.pt ← train base data 
│ └── train_vocab.pt ← vocab of train data 
|
├── requirements.txt ← All Python dependencies
└── README.md ← Project documentation
```


## 📦 Setup Instructions

```bash
git clone https://github.com/your_username/sentiment-lstm-api.git
cd sentiment-lstm-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the API Server

```bash
uvicorn app.main:app --reload
```

## 🧠 Training the Model
The model was trained using a Jupyter Notebook (model.ipynb) using a labeled dataset.
You can customize and retrain using your own dataset.

## 🧪 Example Inference Request
```
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I really loved this movie!"}'
```

## 🐳 Docker (Optional)

```
docker build -t sentiment-api .
docker run -p 8000:8000 sentiment-api
```

##  📤 Deployment Tips
You can deploy this API on:

- Render.com (free tier)

- Railway.app

- Heroku (via Docker)

- AWS EC2 (manual or containerized)




## 🧠 Model Info
> Model: LSTM (1-layer)

> Embeddings: 100-dim

> Hidden size: 128

> Output classes: Positive / Negative


---

## Run uvicorn
```bash
uvicorn app.main:app --reload
```


## ✅`requirements.txt`

```txt
fastapi
uvicorn
torch
numpy
scikit-learn
nltk
```

## upload on github 

```
git init
git add .
git commit -m "Initial Sentiment LSTM API"
gh repo create sentiment-lstm-api --public --source=. --remote=origin
git push -u origin main
```


## Example Dataset

Use IMDB dataset or your own CSV with columns:

- text
- label (0 or 1)


## License

> MIT License
