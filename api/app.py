import os
from datetime import date
from typing import Sequence

import joblib
import numpy as np
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from src.pipeline import run_pipeline

MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/model.pkl")
AUTO_TRAIN_MODEL = os.getenv("AUTO_TRAIN_MODEL", "").lower() in {"1", "true", "yes"}
REQUIRED_HISTORY_LENGTH = 14

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None


class InputData(BaseModel):
    date: date
    last_values: list[float] = Field(
        ...,
        min_length=REQUIRED_HISTORY_LENGTH,
        description="Ordered history ending immediately before the prediction date.",
    )


def build_feature_vector(prediction_date: date, history: Sequence[float]) -> np.ndarray:
    if len(history) < REQUIRED_HISTORY_LENGTH:
        raise ValueError(
            f"At least {REQUIRED_HISTORY_LENGTH} historical values are required; "
            f"received {len(history)}."
        )

    history_array = np.asarray(history, dtype=float)
    if not np.isfinite(history_array).all():
        raise ValueError("All historical values must be finite numbers.")

    week_of_year = prediction_date.isocalendar()[1]
    trailing_week = history_array[-7:]
    features = np.array(
        [
            prediction_date.year,
            prediction_date.month,
            week_of_year,
            prediction_date.timetuple().tm_yday,
            prediction_date.weekday(),
            int(prediction_date.weekday() >= 5),
            history_array[-1],
            history_array[-7],
            history_array[-14],
            trailing_week.mean(),
            trailing_week.std(ddof=1),
        ],
        dtype=float,
    )
    return features.reshape(1, -1)


def get_model():
    global model

    if model is not None:
        return model

    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        return model

    if AUTO_TRAIN_MODEL:
        run_pipeline()
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            return model

    raise RuntimeError(
        "Model artifact is missing. Train the pipeline first or set AUTO_TRAIN_MODEL=true."
    )


@app.post("/predict")
def predict(data: InputData):
    try:
        features = build_feature_vector(data.date, data.last_values)
        prediction = get_model().predict(features)[0]
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction failed.") from exc

    return {"prediction": float(prediction)}


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>ForecastFlow</title>
    </head>
    <body style="text-align:center; margin-top:100px; font-family:Arial;">
        <h1>ForecastFlow API</h1>
        <p>Frontend runs separately. Use /predict for inference or /docs for schema details.</p>
        <a href="/docs">Go to API Docs</a>
    </body>
    </html>
    """


@app.post("/predict-ui", response_class=HTMLResponse)
def predict_ui(values: str = Form(...), prediction_date: str = Form(...)):
    try:
        parsed_values = [float(value.strip()) for value in values.split(",") if value.strip()]
        payload = InputData(date=prediction_date, last_values=parsed_values)
        prediction = predict(payload)["prediction"]
        body = f"<h2>Prediction: {prediction:.2f}</h2>"
    except HTTPException as exc:
        body = f"<h2>Error</h2><p>{exc.detail}</p>"

    return f"""
    <html>
    <body style="text-align:center; margin-top:100px;">
        {body}
        <a href="/">Go Back</a>
    </body>
    </html>
    """
