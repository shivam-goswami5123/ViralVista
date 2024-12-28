import React, { useState } from "react";
import axios from "axios";
import "./styles.css";


  function getCurrentDateTime(data) {
    const timestamp = new Date(data.timestamp); // Assuming `data.timestamp` is a valid ISO string or UNIX timestamp
    const istDate = new Date(timestamp.getTime() - (5 * 60 + 30) * 60 * 1000); // Convert to IST by subtracting 5 hours 30 minutes
  
    // Formatting into dd-mm-yy hh-mm-ss
    const day = String(istDate.getDate()).padStart(2, "0");
    const month = String(istDate.getMonth() + 1).padStart(2, "0"); // Months are zero-based
    const year = String(istDate.getFullYear()).slice(-2);
    const hours = String(istDate.getHours()).padStart(2, "0");
    const minutes = String(istDate.getMinutes()).padStart(2, "0");
    const seconds = String(istDate.getSeconds()).padStart(2, "0");
  
    return `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
  }
  

function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  const runScript = async () => {
    setLoading(true);
    setError("");
    setData(null);

    try {
      // Trigger the backend to run the Selenium script
      await axios.get("http://localhost:3000/run-script");

      // Fetch the latest trending topics
      const response = await axios.get("http://localhost:3000/get-latest");
      setData(response.data);
    } catch (err) {
      setError("Failed to fetch data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>Twitter Trending Topics</h1>

      {data && (
        <div className="results">
          <h3>Trending Topics as of {getCurrentDateTime(data)}</h3>
          <ul>
            <li>{data.trend1}</li>
            <li>{data.trend2}</li>
            <li>{data.trend3}</li>
            <li>{data.trend4}</li>
            <li>{data.trend5}</li>
          </ul>
          <p>
            <strong>The IP address used for this query was </strong> {data.ipAddress}
          </p>
        </div>
      )}

      <button onClick={runScript} disabled={loading}>
        {loading ? "Running Script..." : "Click here to run the script"}
      </button>

      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
