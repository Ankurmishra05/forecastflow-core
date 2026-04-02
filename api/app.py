from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>ForecastFlow</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>🚀 ForecastFlow</h1>
            <p>Time Series Forecasting API</p>

            <h3>Try API</h3>
            <a href="/docs">Go to Swagger Docs</a>

            <br><br>

            <p>Enter sample input:</p>
            <pre>
{
  "date": "1960-01-01",
  "last_values": [380, 390, 400, 410, 420, 430, 440]
}
            </pre>
        </body>
    </html>
    """