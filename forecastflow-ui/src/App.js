import { useState } from "react";

function App() {
  const [values, setValues] = useState("");
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
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
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>🚀 ForecastFlow</h1>

      <input
        type="text"
        placeholder="380,390,400,410,420,430,440"
        value={values}
        onChange={(e) => setValues(e.target.value)}
        style={{ padding: "10px", width: "300px" }}
      />

      <br /><br />

      <button onClick={handlePredict}>
        Predict
      </button>

      <br /><br />

      {result && <h2>Prediction: {result}</h2>}
    </div>
  );
}

export default App;