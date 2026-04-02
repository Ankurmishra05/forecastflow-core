FROM python:3.11-slim

WORKDIR /app

# ✅ Copy only requirements first (for caching)
COPY requirements.txt .

# ✅ Install dependencies (cached layer)
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Now copy full project
COPY . .

# ✅ Fix import issue
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]