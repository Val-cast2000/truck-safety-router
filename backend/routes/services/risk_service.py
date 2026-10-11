# backend/routes/services/risk_service.py

def classify_weather(wind_mph, rain_in_hr, snow_in_hr):
    """Return risk level based on weather thresholds."""
    # Check each condition, take the worst
    levels = []
    
    # Wind
    if wind_mph >= 55: levels.append("No Travel")
    elif wind_mph >= 45: levels.append("Severe")
    elif wind_mph >= 35: levels.append("High")
    elif wind_mph >= 25: levels.append("Moderate")
    else: levels.append("Low")
    
    # Rain
    if rain_in_hr > 1.00: levels.append("No Travel")
    elif rain_in_hr >= 0.50: levels.append("Severe")
    elif rain_in_hr >= 0.25: levels.append("High")
    elif rain_in_hr >= 0.10: levels.append("Moderate")
    else: levels.append("Low")
    
    # Snow
    if snow_in_hr > 3.0: levels.append("No Travel")
    elif snow_in_hr >= 2.0: levels.append("Severe")
    elif snow_in_hr >= 1.0: levels.append("High")
    elif snow_in_hr >= 0.5: levels.append("Moderate")
    else: levels.append("Low")
    
    # Return worst level
    order = ["Low", "Moderate", "High", "Severe", "No Travel"]
    return max(levels, key=lambda x: order.index(x))


def apply_load_rules(weather_level, wind_mph, load_lbs):
    """Override weather level based on load weight rules."""
    # >=55 mph → No Travel for any load
    if wind_mph >= 55:
        return "No Travel"
    
    # 45-54 mph + >30,000 lb → No Travel
    if 45 <= wind_mph <= 54 and load_lbs > 30000:
        return "No Travel"
    
    # 35-44 mph + >40,000 lb → Severe
    if 35 <= wind_mph <= 44 and load_lbs > 40000:
        return "Severe"
    
    return weather_level


def calculate_route_risk(checkpoints, load_lbs):
    """
    For each checkpoint, get weather + risk.
    Returns annotated checkpoints and summary.
    """
    results = []
    risk_counts = {"Low": 0, "Moderate": 0, "High": 0, "Severe": 0, "No Travel": 0}
    
    for cp in checkpoints:
        weather = get_weather_at_time(cp["lat"], cp["lng"], cp["eta"])
        if not weather:
            continue
        
        base_level = classify_weather(
            weather["wind_mph"], weather["rain_in_hr"], weather["snow_in_hr"]
        )
        final_level = apply_load_rules(base_level, weather["wind_mph"], load_lbs)
        
        results.append({
            **cp,
            "weather": weather,
            "risk_level": final_level,
        })
        risk_counts[final_level] += 1
    
    return results, risk_counts