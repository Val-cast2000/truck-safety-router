# backend/routes/services/weather_service.py
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
OWM_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_at_time(lat, lng, target_time):
    """
    Get weather at specific lat/lng for a specific time.
    Uses One Call 3.0 hourly forecast (48h window).
    """
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat, "lon": lng,
        "exclude": "current,minutely,daily,alerts",
        "units": "imperial",  # mph, inches
        "appid": OWM_KEY,
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    
    if "hourly" not in data:
        return None
    
    # Find closest hour to target_time
    target_unix = int(target_time.timestamp())
    closest = min(data["hourly"], key=lambda h: abs(h["dt"] - target_unix))
    
    return {
        "wind_mph": closest.get("wind_speed", 0),
        "rain_in_hr": closest.get("rain", {}).get("1h", 0),
        "snow_in_hr": closest.get("snow", {}).get("1h", 0),
        "timestamp": closest["dt"],
    }