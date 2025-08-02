import { useState, useEffect } from "react";
import "./App.css";

interface HealthResponse {
  status: number;
  timestamp: string;
}

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then((data: HealthResponse) => {
        setHealth(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch health:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Camply Web</h1>
        <p>Find campsites at sold-out campgrounds</p>

        <div className="health-status">
          <h3>Backend Status</h3>
          {loading ? (
            <p>Loading...</p>
          ) : health ? (
            <div>
              <p>Status: {health.status}</p>
              <p>Timestamp: {health.timestamp}</p>
            </div>
          ) : (
            <p>Failed to connect to backend</p>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
