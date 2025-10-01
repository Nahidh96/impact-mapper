# Meteor Madness - NASA Space Apps Hackathon

## Overview
Meteor Madness is a full-stack hackathon-ready web app for simulating asteroid impacts and visualizing NEO threats. It is designed for rapid integration with NASA NeoWs data when available.

## Features
- Flask backend with REST API for asteroid data and impact simulation
- HTML/JS frontend with:
  - Sliders for asteroid parameters
  - 3D orbit visualization (Three.js)
  - 2D impact map (Leaflet)
  - Gamified "Defend Earth" mode
  - Tooltips for physics concepts
- Mock data and endpoints for NASA API
- Sample DEM info for crater visualization

## Getting Started

### Backend (Flask)
1. Install Python 3.8+ and Flask:
   ```sh
   pip install flask flask-cors
   ```
2. Run the backend:
   ```sh
   python app.py
   ```
   The API will be available at `http://localhost:5000`.

### Frontend
1. Open `frontend/index.html` in your browser.
   - For local API calls, ensure CORS is enabled (already set in Flask).
   - For production, serve `index.html` via Flask or a static server.

### NASA API Integration
- When NASA NeoWs API is available, update the `/neo/<id>` endpoint in `app.py` to fetch real data.
- Add your NASA API key as needed (see code comments).

### DEM Data
- Place USGS DEM GeoTIFFs in `static/` for crater visualization (see `sample_dem_info.txt`).
- DEM processing functions are to be added in the frontend for crater overlay.

## File Structure
- `app.py` - Flask backend
- `frontend/index.html` - Main frontend app
- `static/sample_asteroid.json` - Mock asteroid data
- `static/sample_dem_info.txt` - DEM info

## Educational Value
- All calculations and visualizations include comments and tooltips for learning.

## Hackathon Notes
- Modular, hackathon-friendly code
- Ready for live NASA data integration
- All endpoints and UI work with mock data

---

**Good luck, Space Apps hackers!**
