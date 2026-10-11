# backend/routes/services/sampling_service.py
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    """Distance in miles between two points."""
    R = 3958.8  # Earth radius in miles
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def sample_checkpoints(geometry, interval_miles=25):
    """
    Walk along route geometry, pick points every `interval_miles`.
    Returns list of {lat, lng, distance_from_start}.
    """
    coords = geometry["coordinates"]  # [[lng, lat], ...]
    checkpoints = []
    accumulated = 0.0
    next_milestone = 0.0
    
    for i in range(len(coords) - 1):
        lng1, lat1 = coords[i]
        lng2, lat2 = coords[i+1]
        segment_dist = haversine(lat1, lng1, lat2, lng2)
        
        while next_milestone <= accumulated + segment_dist:
            # Interpolate point at next_milestone
            ratio = (next_milestone - accumulated) / segment_dist if segment_dist > 0 else 0
            lat = lat1 + (lat2 - lat1) * ratio
            lng = lng1 + (lng2 - lng1) * ratio
            checkpoints.append({
                "lat": lat, "lng": lng,
                "distance_miles": round(next_milestone, 2)
            })
            next_milestone += interval_miles
        
        accumulated += segment_dist
    
    return checkpoints