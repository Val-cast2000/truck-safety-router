# backend/routes/services/recommendation_service.py

RISK_ORDER = ["Low", "Moderate", "High", "Severe", "No Travel"]

def recommend_route(routes_analyzed):
    """
    Sort routes by priority:
    1. Fewest Severe miles (No Travel = immediate disqualify)
    2. Fewest High miles
    3. Lowest average risk
    4. Shortest travel time
    """
    def route_score(route):
        counts = route["risk_counts"]
        total = sum(counts.values()) or 1
        
        # Immediate disqualify if any No Travel
        no_travel_penalty = 10000 if counts.get("No Travel", 0) > 0 else 0
        
        # Priority weights
        severe_score = counts.get("Severe", 0) * 100
        high_score = counts.get("High", 0) * 10
        
        # Average risk (0=Low, 4=No Travel)
        avg_risk = sum(
            RISK_ORDER.index(level) * count 
            for level, count in counts.items()
        ) / total
        
        return (
            no_travel_penalty +  # Priority 0: No Travel = bad
            severe_score +        # Priority 1
            high_score +          # Priority 2
            avg_risk * 5 +        # Priority 3
            route["duration_hours"] * 0.1  # Priority 4
        )
    
    sorted_routes = sorted(routes_analyzed, key=route_score)
    return sorted_routes[0], sorted_routes