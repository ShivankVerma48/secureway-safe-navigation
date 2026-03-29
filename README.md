# SecureWay – AI-Powered Safe Navigation System

# 

# SecureWay is a safety-focused navigation system that recommends routes based on risk analysis rather than just speed or distance. It integrates machine learning with real-time routing to help users avoid high-risk areas.

# 

# 

# \## Problem

# 

# Traditional navigation systems optimize for shortest or fastest routes, often ignoring safety. This can lead users through unsafe or poorly monitored areas.

# 

# 

# \## Solution

# 

# SecureWay analyzes crime data to identify high-risk zones and integrates this information into route selection. It dynamically evaluates routes and avoids unsafe regions when recommending paths.

# 

# 

# \## Key Features

# 

# \- Safety-aware route optimization  

# \- DBSCAN-based hotspot detection  

# \- Dynamic avoidance of high-risk zones  

# \- Integration with real-time routing APIs  

# \- GeoJSON-based route visualization  

# 

# 

# \## Technical Implementation

# 

# \### 1. Risk Zone Detection

# \- Applied \*\*DBSCAN clustering (Haversine distance)\*\* on geospatial crime data  

# \- Converted clusters into risk zones based on incident density  

# \- Classified zones into severity levels (red / yellow)  

# \- Generated `zones.json` for frontend visualization  

# 

# \### 2. Backend System

# \- Built using \*\*Flask\*\*

# \- Developed APIs for:

# &#x20; - Location search (`/suggest`)

# &#x20; - Route calculation (`/route`)

# &#x20; - Zone retrieval (`/zones`)

# \- Integrated \*\*TomTom Routing API\*\* for real-time navigation  

# 

# \### 3. Safe Routing Logic

# \- Retrieved fastest route from API  

# \- Detected intersections with high-risk zones  

# \- Dynamically recalculated route avoiding unsafe areas  

# \- Implemented fallback when avoidance is not possible  

# 

# 

# \## Tech Stack

# 

# \- Python  

# \- Flask  

# \- Pandas, NumPy  

# \- Scikit-learn (DBSCAN)  

# \- TomTom Maps API  

# \- HTML/CSS (Frontend)  

# 

# \---

# 

# \## Project Structure

# 

# \- `app.py` – Backend server and routing logic  

# \- `dbscan\_cluster.py` – Risk zone generation using DBSCAN  

# \- `zones.json` – Processed danger zones  

# \- `templates/` – Frontend UI  

# 

# \---

# 

# \## My Contribution

# 

# \- Implemented DBSCAN clustering for identifying high-risk zones  

# \- Designed and tuned geospatial clustering using haversine distance  

# \- Built backend APIs using Flask  

# \- Developed safe routing logic with dynamic zone avoidance  

# \- Integrated ML outputs with real-time routing system  

# 

# 

# \## Note

# 

# This project was developed as part of a team collaboration.

# 

# 

# \## How to Run

# 

# 1\. Install dependencies:

# &#x20;  pip install -r requirements.txt  

# 

# 2\. Run the backend:

# &#x20;  python app.py  

# 

# 3\. Open browser:

# &#x20;  http://127.0.0.1:5000/  

# 

# 

# \## Vision

# 

# To make safety a default factor in navigation, especially for users traveling in unfamiliar or high-risk environments.

