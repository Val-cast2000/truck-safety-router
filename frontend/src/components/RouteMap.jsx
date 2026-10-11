// frontend/src/components/RouteMap.jsx
import { MapContainer, TileLayer, Polyline, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const RISK_COLORS = {
  "Low": "#22c55e",
  "Moderate": "#eab308",
  "High": "#f97316",
  "Severe": "#ef4444",
  "No Travel": "#7f1d1d",
};

export default function RouteMap({ routes, bestIndex }) {
  if (!routes?.length) return <div className="h-full bg-gray-100 flex items-center justify-center">No routes yet</div>;

  const best = routes[bestIndex];
  const allCoords = routes.flatMap(r => r.geometry.coordinates);

  return (
    <MapContainer
      bounds={allCoords.map(([lng, lat]) => [lat, lng])}
      className="h-full w-full"
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap"
      />

      {/* All routes in gray */}
      {routes.map((route, i) => (
        <Polyline
          key={i}
          positions={route.geometry.coordinates.map(([lng, lat]) => [lat, lng])}
          color={i === bestIndex ? "#2563eb" : "#9ca3af"}
          weight={i === bestIndex ? 5 : 3}
        />
      ))}

      {/* Checkpoints for best route */}
      {best.checkpoints.map((cp, i) => (
        <CircleMarker
          key={i}
          center={[cp.lat, cp.lng]}
          radius={6}
          fillColor={RISK_COLORS[cp.risk_level]}
          color="#fff"
          weight={2}
          fillOpacity={0.9}
        >
          <Popup>
            <div className="text-sm">
              <strong>Mile {cp.distance_miles}</strong><br />
              Risk: {cp.risk_level}<br />
              Wind: {cp.weather.wind_mph} mph<br />
              Rain: {cp.weather.rain_in_hr} in/hr<br />
              ETA: {new Date(cp.eta).toLocaleString()}
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
