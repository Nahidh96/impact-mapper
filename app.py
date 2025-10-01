import math
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    }
}

@app.route('/neo/<string:asteroid_id>', methods=['GET'])
def get_neo(asteroid_id):
    # Placeholder for NASA NeoWs API integration
    # TODO: Replace with real NASA API call when available
    return jsonify(MOCK_ASTEROID)

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
