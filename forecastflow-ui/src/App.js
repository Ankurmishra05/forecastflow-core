import { useState } from "react";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

function App() {
  const [predictionDate, setPredictionDate] = useState("1960-01-01");
  const [values, setValues] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);
    setError("");

    const parsedValues = values
      .split(",")
      .map((value) => Number(value.trim()))
      .filter((value) => !Number.isNaN(value));

    if (parsedValues.length < 14) {
      setError("Enter at least 14 historical values so the API can build all model features.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          date: predictionDate,
          last_values: parsedValues
        })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Prediction request failed.");
      }

      setResult(data.prediction);
    } catch (requestError) {
      setError(requestError.message || "Error connecting to API.");
    }

    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>ForecastFlow</h1>
        <p style={styles.subtitle}>Predict the next value from 14 or more recent observations.</p>

        <input
          type="date"
          value={predictionDate}
          onChange={(e) => setPredictionDate(e.target.value)}
          style={styles.input}
        />

        <textarea
          placeholder="112,118,132,129,121,135,148,148,136,119,104,118,115,126"
          value={values}
          onChange={(e) => setValues(e.target.value)}
          style={styles.textarea}
        />

        <button onClick={handlePredict} style={styles.button} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>

        {error && <div style={styles.errorBox}>{error}</div>}
        {result !== null && (
          <div style={styles.resultBox}>
            Prediction: <b>{result.toFixed(2)}</b>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    color: "white",
    padding: "24px",
  },
  card: {
    background: "rgba(255,255,255,0.1)",
    padding: "40px",
    borderRadius: "15px",
    backdropFilter: "blur(10px)",
    textAlign: "center",
    width: "100%",
    maxWidth: "480px",
    boxShadow: "0px 10px 30px rgba(0,0,0,0.3)"
  },
  title: {
    marginBottom: "10px"
  },
  subtitle: {
    marginBottom: "20px",
    fontSize: "14px",
    color: "#d8e2ea"
  },
  input: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    marginBottom: "16px",
    outline: "none",
    fontSize: "14px",
    boxSizing: "border-box"
  },
  textarea: {
    width: "100%",
    minHeight: "120px",
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    marginBottom: "20px",
    outline: "none",
    fontSize: "14px",
    resize: "vertical",
    boxSizing: "border-box"
  },
  button: {
    padding: "12px",
    width: "100%",
    border: "none",
    borderRadius: "8px",
    background: "#00c6ff",
    color: "black",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "0.3s"
  },
  resultBox: {
    marginTop: "20px",
    padding: "15px",
    background: "rgba(0,0,0,0.4)",
    borderRadius: "10px"
  },
  errorBox: {
    marginTop: "20px",
    padding: "15px",
    background: "rgba(145, 35, 35, 0.75)",
    borderRadius: "10px"
  }
};

export default App;
