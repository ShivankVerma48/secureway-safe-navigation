import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# CONFIGURATION
TOMTOM_KEY = os.getenv("API_KEY")
if not TOMTOM_KEY:
    raise ValueError("No TOMTOM_API_KEY found in .env file")

# Load zones once at startup for performance
try:
    with open("zones.json") as f:
        ZONES = json.load(f)
except FileNotFoundError:
    print("WARNING: zones.json not found. Safe routing will not work.")
    ZONES = []

# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def root():
    # We render a template to securely pass the API key to the frontend
    return render_template("test5.html", tomtom_key=TOMTOM_KEY)

@app.route("/suggest")
def suggest():
    q = request.args.get("q", "").strip()
    if len(q) < 3:
        return jsonify([])

    try:
        url = f"https://api.tomtom.com/search/2/search/{q}.json"
        params = {
            "key": TOMTOM_KEY,
            "limit": 5,
            "countrySet": "IN",
            "typeahead": "true"
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        results = [
            {
                "name": item["address"].get("freeformAddress", ""),
                "lat": item["position"]["lat"],
                "lon": item["position"]["lon"]
            }
            for item in data.get("results", []) if "position" in item
        ]
        return jsonify(results)
    except Exception as e:
        print(f"Suggestion Error: {e}")
        return jsonify([]), 500

@app.route("/route")
def get_route():
    start = request.args.get("start")
    end = request.args.get("end")
    mode = request.args.get("mode", "fast")

    if not start or not end:
        return jsonify({"error": "Missing start or end coordinates"}), 400

    try:
        slat, slon = map(float, start.split(","))
        elat, elon = map(float, end.split(","))
    except ValueError:
        return jsonify({"error": "Invalid coordinate format"}), 400

    # 1. Fetch Standard Route (Fastest)
    base_url = f"https://api.tomtom.com/routing/1/calculateRoute/{slat},{slon}:{elat},{elon}/json"
    base_params = {
        "key": TOMTOM_KEY,
        "routeType": "fastest",
        "traffic": "true",
        "instructionsType": "text"
    }

    try:
        # Step A: Get the initial fast route to analyze
        fast_resp = requests.get(base_url, params=base_params)
        fast_resp.raise_for_status()
        fast_data = fast_resp.json()
        
        # If not safe mode, return immediately
        if mode != "safe":
            return jsonify(_format_geojson(fast_data, "fast"))

        # Step B: SAFE MODE - Analyze intersections with Danger Zones
        fast_points = fast_data["routes"][0]["legs"][0]["points"]
        avoid_rects = _get_conflicting_zones(fast_points)

        if not avoid_rects:
            # No danger zones on the fast path, return it
            return jsonify(_format_geojson(fast_data, "fast (safe verified)"))

        # Step C: Re-calculate route avoiding the zones
        safe_payload = {"avoidAreas": {"rectangles": avoid_rects}}
        safe_resp = requests.post(base_url, params=base_params, json=safe_payload)
        
        if safe_resp.status_code == 200:
            return jsonify(_format_geojson(safe_resp.json(), "safe"))
        else:
            # Fallback if calculation fails (e.g., impossible to avoid)
            return jsonify(_format_geojson(fast_data, "fast (avoidance failed)"))

    except Exception as e:
        print(f"Routing Error: {e}")
        return jsonify({"error": "Routing calculation failed"}), 500

@app.route("/zones")
def get_zones():
    return jsonify(ZONES)

@app.route("/report", methods=["POST"])
def report_crime():
    payload = request.json
    # In a real app, save this to a database
    print(f"📝 CRIME REPORT RECEIVED: {payload}")
    return jsonify({"status": "success", "message": "Report logged successfully"})

# -----------------------------
# HELPERS
# -----------------------------

def _format_geojson(tomtom_data, mode_label):
    """Converts TomTom JSON response to GeoJSON LineString."""
    try:
        points = tomtom_data["routes"][0]["legs"][0]["points"]
        coords = [[p["longitude"], p["latitude"]] for p in points]
        summary = tomtom_data["routes"][0]["summary"]
        
        return {
            "type": "Feature",
            "properties": {
                "mode": mode_label,
                "distance_meters": summary.get("lengthInMeters"),
                "time_seconds": summary.get("travelTimeInSeconds")
            },
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            }
        }
    except (KeyError, IndexError):
        return {"error": "Invalid route data structure"}

def _get_conflicting_zones(route_points):
    """Finds which ZONES overlap with the route points."""
    relevant_zones = []
    
    # Optimization: Check every 10th point to speed up processing
    sampled_points = route_points[::10] 

    for z in ZONES:
        rect = {
            "s": float(z["south"]), "w": float(z["west"]),
            "n": float(z["north"]), "e": float(z["east"])
        }
        
        # Check intersection
        for p in sampled_points:
            lat, lon = p["latitude"], p["longitude"]
            if rect["s"] <= lat <= rect["n"] and rect["w"] <= lon <= rect["e"]:
                relevant_zones.append({
                    "southWestCorner": {"latitude": rect["s"], "longitude": rect["w"]},
                    "northEastCorner": {"latitude": rect["n"], "longitude": rect["e"]}
                })
                break # Zone added, move to next zone
        
        if len(relevant_zones) >= 10: # TomTom limit
            break
            
    return relevant_zones

if __name__ == "__main__":
    app.run(debug=True, port=5000)