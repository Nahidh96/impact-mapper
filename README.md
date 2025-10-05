<h3 align="center">
  <img src="https://img.shields.io/badge/NASA%20Space%20Apps-2025-blue?style=for-the-badge&logo=nasa" />
  <img src="https://img.shields.io/badge/Mission-Meteor%20Madness-orange?style=for-the-badge&logo=meteor" />
  <img src="https://img.shields.io/badge/Team-Syntax-green?style=for-the-badge&logo=rocket" />
</h3>

# 🚀 Meteor Madness - NASA Space Apps Hackathon

# Meteor Madness - NASA Space Apps Hackathon

## Overview
Meteor Madness is a mission-control style experience for the 2025 NASA Space Apps "Meteor Madness" challenge. The stack is tuned for hackathon velocity: a Flask API delivers mock-but-scientifically grounded impact analytics, while a blockbuster front-end showcases orbital dynamics, risk intelligence, and gamified deflection planning. NASA NeoWs data will drop in the `/neo/<id>` endpoint once the live window opens.

## Major Features
- **Flask Impact Engine** – `/simulate-impact` returns kinetic energy, TNT equivalent, crater diameter, and seismic magnitude using simplified but cited formulas. CORS stays enabled, and the NASA NeoWs proxy now runs live through `/neo/<id>`.
- **Mission Control UI** – Sleek layout powered by `index.html` + `styles.css` with:
  - Parameter deck sliders (diameter, velocity, density, delta-v) with contextual hints
  - Live severity meter, response timeline, readiness confidence gauge, and radar severity plot (Chart.js)
  - 3D orbit sandbox (Three.js) plus Leaflet impact map with crater overlay + population markers
  - Scenario vault, mission notes, toast notifications, and auto-updating Team Syntaxx leaderboard
  - Defend Earth mission planner with strategy presets, budget guidance, and mission briefs
- **NASA Intelligence Feed** – Enter any NASA NeoWs ID to pull live data, auto-sync sliders, and display close-approach facts. A mock dataset remains available for offline demos.
- **Mock Data + Assets** – Sample asteroid JSON, DEM placeholders, and rich tooltips keep the app educational even without network access.

## Quickstart

### 0. Configure environment
```powershell
Copy-Item .env.example .env
notepad .env   # drop in your NASA key under NASA_API_KEY
```
The Flask app and helper scripts auto-load `.env`, so you only have to set the key once.

### 1. Backend (Flask)
```powershell
# from the repo root (e.g. D:\Projects\nasaspaceapp)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python app.py
```
The API serves at `http://localhost:5000`. Leave it running while iterating on the UI. You can still override the key per-request via `?api_key=` or the `X-NASA-API-Key` header when experimenting.

### 2. Frontend
```powershell
cd frontend
python -m http.server 8000
```
Visit `http://localhost:8000` in your browser. The SPA reads simulation data from `http://localhost:5000`.

### 3. NASA NeoWs sanity check
With both servers running, hit the live endpoint:

```powershell
Invoke-WebRequest "http://localhost:5000/neo/3542519" | Select-Object -ExpandProperty Content
```
You should see JSON sourced from NASA. If the key is missing or the service is offline, the response gracefully falls back to the hackathon mock with a helpful message.

### 4. UI smoke walkthrough
1. Load `http://localhost:8000` and wiggle the **Diameter / Velocity / Density** sliders – the kinetic energy, TNT tons, crater diameter, and seismic magnitude tiles should update instantly.
2. In **NEO Intelligence Feed**, enter `3542519` and click **Fetch NEO**. A toast confirms the data source, the facts panel populates, and the sliders sync to the NASA object.
3. Pick any **Mission Planner** preset and call out the timeline, budget, and confidence changes. Update **Mission Notes** to prove the dashboard captures live commentary.
4. Scrub **Delta‑V** under the orbit sandbox and zoom the Leaflet impact map—the trajectory trail and crater overlay respond in real time.

Want an automated check? Run `python scripts/smoke_check.py` (after the backend launches) to exercise `/simulate-impact` and `/neo/<id>` end-to-end.

## NASA Integration Notes
- `GET /neo/<id>` now calls the official [NeoWs](https://api.nasa.gov/) endpoint via `requests`, reading the API key from `.env` (via `python-dotenv`), the `NASA_API_KEY` environment variable, or per-request overrides (`api_key` query string / `X-NASA-API-Key` header).
- Short-form asteroid numbers (e.g., `433`, `101955`) automatically remap to their SPK-ID equivalents so judges can use familiar names without memorizing NASA identifiers.
- Responses are transformed to the UI-friendly payload (`estimated_diameter_m`, `velocity_kms`, `miss_distance_km`, hazard boolean, etc.). If NASA is unreachable, the service returns the local mock data with a diagnostic message.
- The UI’s “NEO Intelligence Feed” form fetches `/neo/<id>`, updates the facts panel, and synchronizes the simulation sliders so teams can immediately explore the impact profile.

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
