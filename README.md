# SecureWay – AI-Powered Safe Navigation System

SecureWay is a safety-focused navigation system that recommends routes based on risk analysis rather than just speed or distance. It integrates machine learning with real-time routing to help users avoid high-risk areas.

---

## Problem

Traditional navigation systems optimize for shortest or fastest routes, often ignoring safety. This can lead users through unsafe or poorly monitored areas.

---

## Solution

SecureWay analyzes crime data to identify high-risk zones and integrates this information into route selection. It dynamically evaluates routes and avoids unsafe regions when recommending paths.

---

## Key Features

- Safety-aware route optimization  
- DBSCAN-based hotspot detection  
- Dynamic avoidance of high-risk zones  
- Integration with real-time routing APIs  
- GeoJSON-based route visualization  

---

## Technical Implementation

### 1. Risk Zone Detection
- Applied **DBSCAN clustering (Haversine distance)** on geospatial crime data  
- Converted clusters into risk zones based on incident density  
- Classified zones into severity levels (red / yellow)  
- Generated `zones.json` for frontend visualization  

### 2. Backend System
- Built using **Flask**
- Developed APIs for:
  - Location search (`/suggest`)
  - Route calculation (`/route`)
  - Zone retrieval (`/zones`)
- Integrated **TomTom Routing API** for real-time navigation  

### 3. Safe Routing Logic
- Retrieved fastest route from API  
- Detected intersections with high-risk zones  
- Dynamically recalculated route avoiding unsafe areas  
- Implemented fallback when avoidance is not possible  

---

## Tech Stack

- Python  
- Flask  
- Pandas, NumPy  
- Scikit-learn (DBSCAN)  
- TomTom Maps API  
- HTML/CSS (Frontend)  

---

## Project Structure

- `app.py` – Backend server and routing logic  
- `dbscan_cluster.py` – Risk zone generation using DBSCAN  
- `zones.json` – Processed danger zones  
- `templates/` – Frontend UI  

---

## My Contribution

- Implemented DBSCAN clustering for identifying high-risk zones  
- Designed and tuned geospatial clustering using haversine distance  
- Built backend APIs using Flask  
- Developed safe routing logic with dynamic zone avoidance  
- Integrated ML outputs with real-time routing system  

---

## Note

This project was developed as part of a team collaboration.

---

## How to Run
1. Clone the repository:
  ```
  git clone https://github.com/ShivankVerma48/secureway-safe-navigation.git
  cd secureway-safe-navigation
  ```
2. Install dependencies:
  ```
  pip install -r requirements.txt
  ```
3. Add your API key:
- Create a `.env` file in the root folder  
- Add:
  ```
  API_KEY=your_tomtom_api_key_here
  ```
4. Run the backend: 
  ```
  python app.py
  ```
5. Open your browser and go to:
  ```
  http://127.0.0.1:5000/
  ```
6. Use the application:
- Enter start and destination locations  
- Choose between fast and safe routes  
- View safer route recommendations on the map  
