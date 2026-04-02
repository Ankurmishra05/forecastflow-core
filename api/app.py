from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from src.pipeline import run_pipeline

# ✅ FIRST create app
app = FastAPI()

# ✅ THEN use decorators
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h1>🚀 ForecastFlow</h1>
            <a href="/docs">Go to API Docs</a>
        </body>
    </html>
    """

# ✅ Model logic after
model_path = "artifacts/model.pkl"

if not os.path.exists(model_path):
    print("Model not found. Training...")
    run_pipeline()