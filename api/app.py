from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import os
from src.pipeline import run_pipeline

model_path = "artifacts/model.pkl"

if not os.path.exists(model_path):
    print("Model not found. Training inside container...")
    run_pipeline()
    
app = FastAPI()

# Load model
model = joblib.load("artifacts/model.pkl")


# ✅ Input Schema (VERY IMPORTANT)
class PredictionInput(BaseModel):
    date: str
    last_values: list


# ✅ Feature Engineering inside API
def create_features(date, last_values):
    date = pd.to_datetime(date)

    features = {}

    # Time features
    features['year'] = date.year
    features['month'] = date.month
    features['week_of_year'] = date.isocalendar().week
    features['day_of_year'] = date.dayofyear
    features['day_of_week'] = date.dayofweek
    features['is_weekend'] = int(date.dayofweek >= 5)

    # Lag features
    features['lag_1'] = last_values[-1]
    features['lag_7'] = last_values[-7] if len(last_values) >= 7 else last_values[0]
    features['lag_14'] = last_values[0]  # fallback

    # Rolling features
    features['rolling_mean_7'] = np.mean(last_values[-7:])
    features['rolling_std_7'] = np.std(last_values[-7:])

    return list(features.values())


# ✅ Prediction endpoint
@app.post("/predict")
def predict(data: PredictionInput):
    features = create_features(data.date, data.last_values)

    prediction = model.predict([features])

    return {
        "prediction": float(prediction[0])
    }


@app.get("/")
def home():
    return {"message": "ForecastFlow API running 🚀"}