# backend/routes/services/geocoding_service.py
import requests

def geocode_location(query):
    """Convert address to lat/lng using Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "truck-safety-router/1.0"}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()
    if not data:
        raise ValueError(f"Location not found: {query}")
    return {"lat": float(data[0]["lat"]), "lng": float(data[0]["lon"])}
