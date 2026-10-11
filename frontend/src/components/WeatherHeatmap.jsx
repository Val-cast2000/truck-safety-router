// frontend/src/components/WeatherHeatmap.jsx
import { useState } from "react";
import { Circle, Marker } from "react-leaflet";

const RISK_OPACITY = {
  "Low": 0.15,
  "Moderate": 0.3,
  "High": 0.5,
  "Severe": 0.7,
  "No Travel": 0.9,
};

const RISK_COLORS = {
  "Low": "#22c55e",
  "Moderate": "#eab308",
  "High": "#f97316",
  "Severe": "#ef4444",
  "No Travel": "#7f1d1d",
};

export default function WeatherHeatmap({ route, timeOffset }) {
  const [selectedHour, setSelectedHour] = useState(0); // 0-48

  if (!route) return null;

  // Filter checkpoints within the selected hour window
  // For simplicity: show heatmap for all checkpoints
  // In production: you'd fetch weather for each hour offset

  return (
    <>
      {route.checkpoints.map((cp, i) => (
        <Circle
          key={i}
          center={[cp.lat, cp.lng]}
          radius={8000} // ~5 miles in meters
          pathOptions={{
            color: RISK_COLORS[cp.risk_level],
            fillColor: RISK_COLORS[cp.risk_level],
            fillOpacity: RISK_OPACITY[cp.risk_level],
            weight: 0,
          }}
        />
      ))}
      
      {/* Time slider would be outside the map */}
    </>
  );
}