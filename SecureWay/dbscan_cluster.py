import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import json

# ===== 1) Load data =====
# Use your file name here 
df = pd.read_csv("crime_data_clean.csv")   # columns: Location, Latitude, Longitude, Crime Type, Time

# We only need coordinates for clustering
coords = df[['Latitude', 'Longitude']].values

# ===== 2) Configure DBSCAN for geospatial data =====
# DBSCAN with haversine distance expects radians
kms_per_radian = 6371.0088
eps_km = 0.2                 # ~200 meters neighborhood
epsilon = eps_km / kms_per_radian

db = DBSCAN(
    eps=epsilon,
    min_samples=3,           # require at least 3 incidents to form a hotspot
    algorithm='ball_tree',
    metric='haversine'
).fit(np.radians(coords))

# ===== 3) Summarize clusters into hotspot centers + severity =====
clusters = []
for cid in sorted(df['Cluster'].unique()):
    if cid == -1:
        continue  # skip noise
    cpts = df[df['Cluster'] == cid]
    center_lat = cpts['Latitude'].mean()
    center_lon = cpts['Longitude'].mean()
    total_incidents = len(cpts)      # or cpts['Count'].sum() if you have a Count column
    zone = "red" if total_incidents >= 10 else "yellow"

    clusters.append({
        "Cluster": int(cid),
        "Center_Latitude": float(center_lat),
        "Center_Longitude": float(center_lon),
        "Total_Incidents": int(total_incidents),
        "Zone": zone
    })

summary_df = pd.DataFrame(clusters)

# ===== 4) Create JSON for frontend/Google Maps overlay =====
zones = [
    {
        "lat": float(row.Center_Latitude),
        "lon": float(row.Center_Longitude),
        "zone": row.Zone,
        "total_incidents": int(row.Total_Incidents),
        "radius": 200  # meters, for drawing circles on the map
    }
    for _, row in summary_df.iterrows()
]

with open("zones.json", "w") as f:
    json.dump(zones, f, indent=4)
print("Saved zones.json (ready to plot on a map)")
