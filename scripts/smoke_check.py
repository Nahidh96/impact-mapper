"""Quick smoke test for Meteor Madness Flask API.

Run after servers are up:
    python scripts/smoke_check.py

Environment variables you can set:
- NASA_API_KEY: used when calling the live NeoWs proxy
- API_BASE: override backend base URL (default http://localhost:5000)
- NASA_NEO_ID: override the asteroid ID to query (default 3542519)
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.environ.get("API_BASE", "http://localhost:5000").rstrip("/")
NASA_NEO_ID = os.environ.get("NASA_NEO_ID", "3542519")


def _pretty_print(label: str, payload: Dict[str, Any]) -> None:
    print(f"\n{label}")
    print(json.dumps(payload, indent=2, sort_keys=True))


def run_simulation_test() -> Dict[str, Any]:
    payload = {"diameter": 180, "velocity": 21, "density": 2800}
    url = f"{API_BASE}/simulate-impact"
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    required_keys = {"kinetic_energy_j", "tnt_equivalent_tons", "crater_diameter_m"}
    missing = required_keys.difference(data)
    if missing:
        raise AssertionError(f"simulate-impact missing keys: {missing}")
    return data


def run_nasa_proxy_test() -> Dict[str, Any]:
    url = f"{API_BASE}/neo/{NASA_NEO_ID}"
    headers = {}
    api_key = os.environ.get("NASA_API_KEY")
    if api_key:
        headers["X-NASA-API-Key"] = api_key
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    required_keys = {"name", "source", "estimated_diameter_max_m"}
    missing = required_keys.difference(data)
    if missing:
        raise AssertionError(f"/neo payload missing keys: {missing}")
    return data


def main() -> int:
    print(f"API base: {API_BASE}")
    try:
        sim = run_simulation_test()
        _pretty_print("/simulate-impact", sim)
        neo = run_nasa_proxy_test()
        _pretty_print(f"/neo/{NASA_NEO_ID}", neo)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"\nSmoke check failed: {exc}", file=sys.stderr)
        return 1
    print("\nSmoke check passed ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
