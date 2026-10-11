# backend/routes/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta

from .services.geocoding_service import geocode_location
from .services.routing_service import get_routes
from .services.sampling_service import sample_checkpoints
from .services.risk_service import calculate_route_risk
from .services.recommendation_service import recommend_route

@api_view(["POST"])
def plan_trip(request):
    data = request.data
    origin = geocode_location(data["origin"])
    destination = geocode_location(data["destination"])
    load_lbs = float(data["load_lbs"])
    departure = datetime.fromisoformat(data["departure"])
    
    raw_routes = get_routes(origin, destination, alternatives=3)
    
    analyzed = []
    for route in raw_routes:
        checkpoints = sample_checkpoints(route["geometry"], interval_miles=25)
        
        # Assign ETA to each checkpoint based on speed
        speed_mph = route["distance_miles"] / route["duration_hours"] if route["duration_hours"] > 0 else 55
        for cp in checkpoints:
            cp["eta"] = departure + timedelta(hours=cp["distance_miles"] / speed_mph)
        
        annotated, risk_counts = calculate_route_risk(checkpoints, load_lbs)
        analyzed.append({
            **route,
            "checkpoints": annotated,
            "risk_counts": risk_counts,
        })
    
    best, all_routes = recommend_route(analyzed)
    
    return Response({
        "best_route_index": all_routes.index(best),
        "routes": all_routes,
    })