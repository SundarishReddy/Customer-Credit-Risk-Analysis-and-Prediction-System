from typing import Dict, Any
from pydantic import BaseModel
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os

MODEL_PATH = os.environ.get('MODEL_PATH', 'backend/model.joblib')

app = FastAPI(title="Credit Risk Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        app.logger = getattr(app, 'logger', None)
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Run training script first.")
    model = joblib.load(MODEL_PATH)

class PredictRequest(BaseModel):
    data: Dict[str, Any]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    global model
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    data = req.data
    # ensure input is a dict
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="data must be an object mapping feature names to values")
    try:
        df = pd.DataFrame([data])
        proba = model.predict_proba(df)[0,1]
        pred = int(model.predict(df)[0])
        return {
            "prediction": pred,
            "probability": float(proba)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
