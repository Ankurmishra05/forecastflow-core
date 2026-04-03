from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import numpy as np
from pydantic import BaseModel
from src.pipeline import run_pipeline

# -----------------------------
# INIT APP
# -----------------------------
app = FastAPI()

# -----------------------------
# ENABLE CORS (for React)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# LOAD / TRAIN MODEL
# -----------------------------
model_path = "artifacts/model.pkl"

if not os.path.exists(model_path):
    print("Model not found. Training...")
    run_pipeline()

model = joblib.load(model_path)

# -----------------------------
# REQUEST SCHEMA (for API)
# -----------------------------
class InputData(BaseModel):
    date: str
    last_values: list

# -----------------------------
# API ROUTE (used by React)
# -----------------------------
@app.post("/predict")
def predict(data: InputData):
    try:
        values = np.array(data.last_values).reshape(1, -1)
        prediction = model.predict(values)[0]

        return {"prediction": float(prediction)}

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# SIMPLE HTML UI (optional)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>ForecastFlow</title>
    </head>
    <body style="text-align:center; margin-top:100px; font-family:Arial;">
        <h1>🚀 ForecastFlow API</h1>
        <p>Frontend is running separately (React)</p>
        <a href="/docs">Go to API Docs</a>
    </body>
    </html>
    """

# -----------------------------
# OPTIONAL FORM UI (backup)
# -----------------------------
@app.post("/predict-ui", response_class=HTMLResponse)
def predict_ui(values: str = Form(...)):
    try:
        vals = list(map(float, values.split(",")))
        prediction = model.predict([vals])[0]

        return f"""
        <html>
        <body style="text-align:center; margin-top:100px;">
            <h2>✅ Prediction: {prediction:.2f}</h2>
            <a href="/">Go Back</a>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <body style="text-align:center; margin-top:100px;">
            <h2>❌ Error</h2>
            <p>{str(e)}</p>
            <a href="/">Go Back</a>
        </body>
        </html>
        """