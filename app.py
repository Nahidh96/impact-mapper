import math
import os
from typing import Optional, Tuple

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

# --- NASA CONFIG ---
NASA_NEO_ENDPOINT = "https://api.nasa.gov/neo/rest/v1/neo/{neo_id}"
DEFAULT_DENSITY = 3000  # kg/m^3 fallback when NASA data omits density


# --- MOCK DATA FOR NASA NEO ENDPOINT ---
MOCK_ASTEROID = {
    "id": "2025-AB",
    "name": "Mock Asteroid",
    "estimated_diameter_m": 150,
    "velocity_kms": 22.5,
    "density_kgm3": 3200,
    "close_approach_date": "2025-10-01",
    "orbit": {
        "semi_major_axis_au": 1.2,
        "eccentricity": 0.15,
        "inclination_deg": 5.2
    },
    "source": "mock",
    "message": "Set NASA_API_KEY to fetch live data."
}


def _resolve_api_key() -> Optional[str]:
    """Resolve NASA API key from request query/header or environment."""
    return (
        request.args.get("api_key")
        or request.headers.get("X-NASA-API-Key")
        or os.getenv("NASA_API_KEY")
        or os.getenv("NASA_API_TOKEN")
    )


def _fetch_nasa_neo(asteroid_id: str, api_key: str) -> Tuple[dict, Optional[str], Optional[int]]:
    """Call NASA NeoWs API and transform output, returning (data, error, status)."""
    candidate_ids = [asteroid_id]
    try:
        numeric_id = int(asteroid_id)
    except (TypeError, ValueError):
        numeric_id = None

    if numeric_id is not None and numeric_id < 2_000_000:
        candidate_ids.append(str(2_000_000 + numeric_id))

    last_error: Optional[str] = None
    last_status: Optional[int] = None

    for candidate in candidate_ids:
        url = NASA_NEO_ENDPOINT.format(neo_id=candidate)
        try:
            response = requests.get(url, params={"api_key": api_key}, timeout=10)
            response.raise_for_status()
            payload = response.json()
        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status == 404:
                last_error = (
                    f"NASA NeoWs could not find an object with ID {candidate}. "
                    "Try using the SPK-ID (for example, 433 → 2000433)."
                )
                last_status = 404
                continue
            status = status or 502
            return {}, f"NASA NeoWs request failed with status {status}.", status
        except requests.exceptions.RequestException as exc:
            return {}, f"NASA NeoWs request error: {exc}", 502

        close_approach = payload.get("close_approach_data") or []
        approach = close_approach[0] if close_approach else {}
        rel_velocity = approach.get("relative_velocity", {})
        orbit = payload.get("orbital_data", {})
        diameter_info = (payload.get("estimated_diameter") or {}).get("meters", {})

        def to_float(value: Optional[str]) -> Optional[float]:
            try:
                return float(value) if value not in (None, "") else None
            except (TypeError, ValueError):
                return None

        transformed = {
            "id": payload.get("id", candidate),
            "name": payload.get("name", candidate),
            "estimated_diameter_m": diameter_info.get("estimated_diameter_max") or diameter_info.get("estimated_diameter_min"),
            "estimated_diameter_min_m": diameter_info.get("estimated_diameter_min"),
            "estimated_diameter_max_m": diameter_info.get("estimated_diameter_max"),
            "velocity_kms": to_float(rel_velocity.get("kilometers_per_second")),
            "relative_velocity_kph": to_float(rel_velocity.get("kilometers_per_hour")),
            "close_approach_date": approach.get("close_approach_date_full") or approach.get("close_approach_date"),
            "miss_distance_km": to_float((approach.get("miss_distance") or {}).get("kilometers")),
            "orbiting_body": approach.get("orbiting_body"),
            "potentially_hazardous": payload.get("is_potentially_hazardous_asteroid", False),
            "absolute_magnitude_h": payload.get("absolute_magnitude_h"),
            "density_kgm3": DEFAULT_DENSITY,
            "orbit": {
                "semi_major_axis_au": to_float(orbit.get("semi_major_axis")),
                "eccentricity": to_float(orbit.get("eccentricity")),
                "inclination_deg": to_float(orbit.get("inclination")),
                "mean_anomaly_deg": to_float(orbit.get("mean_anomaly")),
                "ascending_node_longitude_deg": to_float(orbit.get("ascending_node_longitude")),
                "orbital_period_days": to_float(orbit.get("orbital_period")),
                "mean_motion_deg_day": to_float(orbit.get("mean_motion")),
                "perihelion_distance_au": to_float(orbit.get("perihelion_distance")),
                "aphelion_distance_au": to_float(orbit.get("aphelion_distance")),
                "epoch_osculation": orbit.get("epoch_osculation"),
            },
            "source": "nasa",
            "requested_id": asteroid_id,
            "resolved_id": candidate,
        }

        return transformed, None, None

    return {}, last_error or "NASA NeoWs lookup failed.", last_status or 502


@app.route('/neo/<string:asteroid_id>', methods=['GET'])
def get_neo(asteroid_id):
    api_key = _resolve_api_key()
    if not api_key:
        mock_payload = {**MOCK_ASTEROID, "message": "NASA_API_KEY missing; returning mock data."}
        return jsonify(mock_payload)

    neo_data, error, status = _fetch_nasa_neo(asteroid_id, api_key)
    if error:
        fallback = {
            **MOCK_ASTEROID,
            "requested_id": asteroid_id,
            "source": "mock",
            "message": error
        }
        return jsonify(fallback), status or 502

    return jsonify(neo_data)

@app.route('/simulate-impact', methods=['POST'])
def simulate_impact():
    data = request.get_json()
    diameter = float(data.get('diameter', 100))  # meters
    velocity = float(data.get('velocity', 20))   # km/s
    density = float(data.get('density', 3000))   # kg/m^3
    delta_v = float(data.get('delta_v', 0))      # km/s (optional deflection)

    # Adjust velocity if delta-v is applied (mock logic)
    impact_velocity = max(velocity - delta_v, 0.1)

    # Calculate mass (sphere): m = (4/3) * pi * r^3 * density
    radius = diameter / 2
    mass = (4/3) * math.pi * (radius ** 3) * density

    # Kinetic energy: KE = 0.5 * m * v^2 (v in m/s)
    v_ms = impact_velocity * 1000
    kinetic_energy = 0.5 * mass * v_ms ** 2

    # TNT equivalent: 1 ton TNT = 4.184e9 J
    tnt_equiv = kinetic_energy / 4.184e9

    # Crater diameter (simplified power-law):
    # D = k * (E/1e9)^(1/4), k ~ 1.8 for Earth, E in Joules
    crater_diameter = 1.8 * (kinetic_energy / 1e9) ** 0.25

    # Seismic magnitude (Mw):
    # Mw = (2/3) * log10(E) - 3.2, E in Joules
    seismic_mw = (2/3) * math.log10(kinetic_energy) - 3.2

    return jsonify({
        "kinetic_energy_j": kinetic_energy,
        "tnt_equivalent_tons": tnt_equiv,
        "crater_diameter_m": crater_diameter,
        "seismic_magnitude_mw": seismic_mw
    })

if __name__ == '__main__':
    app.run(debug=True)
