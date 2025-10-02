# Meteor Madness - NASA Space Apps Hackathon

## Overview
Meteor Madness is a mission-control style experience for the 2025 NASA Space Apps "Meteor Madness" challenge. The stack is tuned for hackathon velocity: a Flask API delivers mock-but-scientifically grounded impact analytics, while a blockbuster front-end showcases orbital dynamics, risk intelligence, and gamified deflection planning. NASA NeoWs data will drop in the `/neo/<id>` endpoint once the live window opens.

## Major Features
- **Flask Impact Engine** – `/simulate-impact` returns kinetic energy, TNT equivalent, crater diameter, and seismic magnitude using simplified but cited formulas. CORS is enabled and the code is pre-commented for swapping in real NASA data.
- **Mission Control UI** – Sleek layout powered by `index.html` + `styles.css` with:
  - Parameter deck sliders (diameter, velocity, density, delta-v) with contextual hints
  - Live severity meter, response timeline, and readiness confidence gauge
  - Radar chart (Chart.js), 3D orbit sandbox (Three.js), and Leaflet impact map with population overlays
  - Scenario vault, mission notes, and auto-updating Team Syntaxx leaderboard
  - Defend Earth mission planner with strategy presets and dynamic brief generator
- **Mock Data + Assets** – Sample asteroid JSON, DEM placeholders, and rich tooltips keep the app educational until the real feed arrives.

## Quickstart

### To run
```
D:\Projects\nasaspaceapp\.venv\Scripts\python.exe -m pip install flask flask-cors
D:\Projects\nasaspaceapp\.venv\Scripts\python.exe app.py
```
Open a another terminal and enter:
```
D:\Projects\nasaspaceapp\.venv\Scripts\python.exe -m http.server 8000
```

### Backend (Flask)
```powershell
pip install flask flask-cors
python app.py
```
The API serves at `http://localhost:5000`. Leave it running while iterating on the UI.

### Frontend
```powershell
cd frontend
python -m http.server 8000
```
Visit `http://localhost:8000` in your browser. The SPA expects the Flask API at `http://localhost:5000`.

## NASA Integration Notes
- Replace the mock `MOCK_ASTEROID` response inside `app.py` with a call to the official [NeoWs](https://api.nasa.gov/) endpoint once the key is issued.
- Store your API key in an environment variable and inject it via `requests` headers to keep credentials out of source control.
- The front-end `loadSampleNeo()` helper will automatically display live data when the backend proxy begins returning it.

## DEM + Crater Visuals
- Drop USGS (or other) GeoTIFF tiles into `static/`. The placeholder `dem_processing.js` shows how to generate crater footprints; plug in `geotiff.js` or your GIS stack of choice for real elevation sampling.
- Leaflet will immediately reflect crater radius changes; extend the map overlay with actual DEM contours for bonus points.

## Repository Map
- `app.py` – Flask API with simulation formulas and future NeoWs hook
- `frontend/index.html` – Main SPA with mission modules, charts, orbit/map integrations
- `frontend/styles.css` – High-fidelity styling, responsive layout, hackathon-ready theming
- `frontend/dem_processing.js` – Placeholder crater footprint utilities
- `static/sample_asteroid.json` – Mock asteroid payload for UI demos
- `static/sample_dem_info.txt` – Notes on expected DEM assets

## Pitch-Ready Talking Points
- Educational tooltips explain each physics metric in approachable language.
- Mission Desk combines strategic planning with immediate feedback for judges and visitors.
- Leaderboard, countdown clock, and toast notifications deliver hackathon theatre.
- Footer proudly credits **Team Syntaxx** so evaluators know who to crown.

---

**Clear skies, Team Syntaxx!** Ship updates fast, then flip the NASA feed switch when the window opens.
