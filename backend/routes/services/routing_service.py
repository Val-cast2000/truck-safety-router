# backend/routes/services/routing_service.py
import requests

OSRM_BASE = "http://router.project-osrm.org"

def get_routes(origin, destination, alternatives=3):
    """Get up to 3 alternative routes."""
    coords = f"{origin['lng']},{origin['lat']};{destination['lng']},{destination['lat']}"
    url = f"{OSRM_BASE}/route/v1/driving/{coords}"
    params = {
        "alternatives": alternatives,
        "geometries": "geojson",
        "overview": "full",
        "steps": "false",
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    
    if data.get("code") != "Ok":
        raise ValueError("Routing failed")
    
    routes = []
    for route in data["routes"]:
        routes.append({
            "geometry": route["geometry"],
            "distance_miles": route["distance"] * 0.000621371,
            "duration_hours": route["duration"] / 3600,
        })
    return routes