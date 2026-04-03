# ForecastFlow

This is a full-stack machine learning project built to go beyond model training and into a more realistic application setup.

The idea is simple:
Take past time-series values and predict the next one.

Instead of stopping at a notebook, this project includes backend, frontend, CI, and deployment.

---

## Live Demo

- Frontend: https://forecastflow-ui.vercel.app
- Backend API: https://forecastflow-7xq6.onrender.com/docs

---

## What this project does

You give it recent values and it predicts the next value using a trained ML model.

End-to-end flow:

**Data -> Features -> Model -> API -> UI -> Deployment**

---

## How it works

### Feature Engineering

- Created lag features from previous values
- Added rolling averages
- Used time-based features such as month and year

---

### Model

- Tried Prophet as a baseline
- Final model: **XGBoost**
- Achieved RMSE about **46.45**

---

### Backend (FastAPI)

- Built an API to serve predictions
- Handles input preprocessing
- Returns predictions in real time

---

### Frontend (React)

- Simple UI for entering recent values
- Sends requests to the backend API
- Displays prediction results immediately

---

### Deployment

- Backend deployed on **Render**
- Frontend deployed on **Vercel**
- CI/CD with GitHub Actions
- Dockerized backend

---

## Project Structure

```text
forecastflow-core/
|-- api/              # FastAPI backend
|-- src/              # ML pipeline
|-- artifacts/        # trained model
|-- forecastflow-ui/  # React frontend
```

---

## Run Locally

### Backend

```bash
pip install -r requirements.txt
python -m src.pipeline
uvicorn api.app:app --reload
```

### Frontend

```bash
cd forecastflow-ui
npm install
npm start
```

Set the frontend API target in `forecastflow-ui/.env`:

```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

---

## Deployment Notes

Backend:
The Docker build includes `artifacts/model.pkl`, so the FastAPI service can start on Render without retraining as long as that file remains in the repo.

Frontend:
Set `REACT_APP_API_BASE_URL` in your frontend host to the deployed backend URL. A template is provided in `forecastflow-ui/.env.example`.

---

## Example Input

```text
112,118,132,129,121,135,148,148,136,119,104,118,115,126
```

---

## Example Output

```text
Prediction: 491.93
```

---

## What I learned

- How to move from notebook to a real system
- Why feature engineering matters in time-series forecasting
- How to structure ML code for reuse
- How to deploy models behind APIs
- How frontend and backend integrate in an ML app

---

## Why I built this

Most ML projects stop at training a model.
This project was built to understand how users actually interact with ML systems in production.
