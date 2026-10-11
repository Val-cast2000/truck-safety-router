// frontend/src/App.jsx
import { useState } from "react";
import axios from "axios";
import TripForm from "./components/TripForm";
import RouteMap from "./components/RouteMap";
import TimeSlider from "./components/TimeSlider";

const API = "http://localhost:8000/api";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [timeOffset, setTimeOffset] = useState(0);

  const handlePlan = async (form) => {
    setLoading(true);
    try {
      const { data } = await axios.post(`${API}/plan/`, form);
      setResult(data);
    } catch (err) {
      alert("Error: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex">
      <div className="w-80 p-4 overflow-y-auto">
        <h1 className="text-xl font-bold mb-4">Truck Safety Router</h1>
        <TripForm onSubmit={handlePlan} loading={loading} />
        
        {result && (
          <div className="mt-4 space-y-2">
            <h2 className="font-semibold">Routes ({result.routes.length})</h2>
            {result.routes.map((route, i) => (
              <div key={i} className={`p-2 rounded border ${i === result.best_route_index ? "border-blue-500 bg-blue-50" : ""}`}>
                <div className="flex justify-between">
                  <span className="font-medium">Route {i + 1}</span>
                  {i === result.best_route_index && <span className="text-xs bg-blue-600 text-white px-1 rounded">BEST</span>}
                </div>
                <div className="text-sm text-gray-600">
                  {route.distance_miles.toFixed(1)} mi · {route.duration_hours.toFixed(1)} hrs
                </div>
                <div className="text-xs mt-1">
                  {Object.entries(route.risk_counts).map(([level, count]) => (
                    count > 0 && <span key={level} className="mr-2">{level}: {count}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      <div className="flex-1 relative">
        {result ? (
          <>
            <RouteMap routes={result.routes} bestIndex={result.best_route_index} />
            <TimeSlider value={timeOffset} onChange={setTimeOffset} />
          </>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-400">
            Enter trip details to see routes
          </div>
        )}
      </div>
    </div>
  );
}