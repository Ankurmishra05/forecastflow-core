import { useState } from "react";

function App() {
  const [values, setValues] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("https://forecastflow-7xq6.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          date: "1960-01-01",
          last_values: values.split(",").map(Number)
        })
      });

      const data = await response.json();
      setResult(data.prediction);
    } catch (error) {
      alert("Error connecting to API");
    }

    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>🚀 ForecastFlow</h1>

        <p style={styles.subtitle}>
          Predict future values using AI
        </p>

        <input
          type="text"
          placeholder="380,390,400,410,420,430,440"
          value={values}
          onChange={(e) => setValues(e.target.value)}
          style={styles.input}
        />

        <button onClick={handlePredict} style={styles.button}>
          {loading ? "Predicting..." : "Predict"}
        </button>

        {result && (
          <div style={styles.resultBox}>
            📊 Prediction: <b>{result.toFixed(2)}</b>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    height: "100vh",
    background: "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    color: "white",
  },
  card: {
    background: "rgba(255,255,255,0.1)",
    padding: "40px",
    borderRadius: "15px",
    backdropFilter: "blur(10px)",
    textAlign: "center",
    width: "400px",
    boxShadow: "0px 10px 30px rgba(0,0,0,0.3)"
  },
  title: {
    marginBottom: "10px"
  },
  subtitle: {
    marginBottom: "20px",
    fontSize: "14px",
    color: "#ccc"
  },
  input: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    marginBottom: "20px",
    outline: "none",
    fontSize: "14px"
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
  }
};

export default App;