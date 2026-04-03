from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import joblib
import os
from src.pipeline import run_pipeline

# -----------------------------
# INIT APP
# -----------------------------
app = FastAPI()

# -----------------------------
# LOAD / TRAIN MODEL
# -----------------------------
model_path = "artifacts/model.pkl"

if not os.path.exists(model_path):
    print("Model not found. Training...")
    run_pipeline()

model = joblib.load(model_path)

# -----------------------------
# HOME PAGE (UI)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>ForecastFlow</title>
        <style>
            body {
                font-family: Arial;
                background: #f5f5f5;
                text-align: center;
                margin-top: 100px;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                width: 400px;
                margin: auto;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }
            input {
                width: 80%;
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            button {
                padding: 10px 20px;
                background: black;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            a {
                text-decoration: none;
                color: blue;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 ForecastFlow</h1>
            <p>Enter last 7 values (comma separated)</p>

            <form action="/predict-ui" method="post">
                <input type="text" name="values" placeholder="380,390,400,410,420,430,440" required />
                <br>
                <button type="submit">Predict</button>
            </form>

            <br>
            <a href="/docs">Go to API Docs</a>
        </div>
    </body>
    </html>
    """

# -----------------------------
# PREDICTION ROUTE (UI)
# -----------------------------
@app.post("/predict-ui", response_class=HTMLResponse)
def predict_ui(values: str = Form(...)):
    try:
        vals = list(map(float, values.split(",")))

        # IMPORTANT: adjust this if your model expects different features
        prediction = model.predict([vals])[0]

        return f"""
        <html>
        <body style="text-align:center; font-family: Arial; margin-top:100px;">
            <h2>✅ Prediction: {prediction:.2f}</h2>
            <br>
            <a href="/">⬅️ Go Back</a>
        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <html>
        <body style="text-align:center; margin-top:100px;">
            <h2>❌ Error: Invalid Input</h2>
            <p>{str(e)}</p>
            <a href="/">⬅️ Go Back</a>
        </body>
        </html>
        """ 