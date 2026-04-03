# ForecastFlow

This is a full-stack machine learning project where I tried to go beyond just training a model and actually build something closer to a real-world system.

The idea was simple:
👉 Take past time-series values and predict the next one.

But instead of stopping at a notebook, I turned it into a complete application with backend, frontend, and deployment.

---

## 🌐 Live Demo

* Frontend: https://forecastflow-ui.vercel.app
* Backend API: https://forecastflow-7xq6.onrender.com/docs

---

## 📌 What this project does

You give it recent values (like last 7 data points), and it predicts the next value using a trained ML model.

I built the whole flow:

**Data → Features → Model → API → UI → Deployment**

---

## 🧠 How it works

### 📊 Feature Engineering

* Created lag features (previous values)
* Added rolling averages
* Used time-based features like month/year

---

### 🤖 Model

* Tried Prophet as a baseline
* Final model: **XGBoost**
* Achieved RMSE ≈ **46.45**

---

### ⚙️ Backend (FastAPI)

* Built an API to serve predictions
* Handles input + preprocessing
* Returns prediction in real-time

---

### ⚛️ Frontend (React)

* Simple and clean UI
* User enters values → clicks predict
* Displays prediction instantly
* Added basic chart for visualization

---

### 🚀 Deployment

* Backend deployed on **Render**
* Frontend deployed on **Vercel**
* CI/CD using GitHub Actions
* Dockerized for portability

---

## 📁 Project Structure

```
forecastflow-core/
│
├── api/              # FastAPI backend
├── src/              # ML pipeline
├── artifacts/        # trained model
├── forecastflow-ui/  # React frontend
```

---

## 🚀 Run Locally

### Backend

```
pip install -r requirements.txt
python -m src.pipeline
uvicorn api.app:app --reload
```

### Frontend

```
cd forecastflow-ui
npm install
npm start
```

---

## 🧪 Example Input

```
380,390,400,410,420,430,440
```

---

## 📈 Output

```
Prediction: 491.93
```

---

## 💡 What I learned

* How to move from notebook → real system
* Importance of feature engineering in time-series
* How to structure ML code properly
* How to deploy models using APIs
* How frontend + backend integrate in ML apps
* Handling real deployment issues (Render, ports, dependencies, etc.)

---

## 🔥 Why I built this

Most ML projects stop at training a model.
I wanted to understand how things work in production — how users actually interact with ML systems.

---

## 👨‍💻 About me

Hi, I’m Ankur 👋
I’m learning ML/AI and focusing on building real-world, production-style projects.

---

⭐ If you liked this project, feel free to star it!
