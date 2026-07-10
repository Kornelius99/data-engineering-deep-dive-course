"""Exercise solution for Module 01: adds a --city flag and retry-with-backoff.

Usage:
    python modules/01-ingestion/ingest_solution.py --date 2024-01-15 --city london
    python modules/01-ingestion/ingest_solution.py --date 2024-01-15 --city berlin
"""
import argparse
import json
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LANDING_ZONE = Path(__file__).resolve().parents[2] / "landing_zone"

CITIES = {
    "london": (51.5072, -0.1276),
    "berlin": (52.5200, 13.4050),
    "new_york": (40.7128, -74.0060),
}


def _session_with_retries() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.5,  # 0.5s, 1s, 2s between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def fetch_weather(date: str, city: str) -> dict:
    if city not in CITIES:
        raise ValueError(f"Unknown city '{city}'. Known cities: {sorted(CITIES)}")
    lat, lon = CITIES[city]

    session = _session_with_retries()
    resp = session.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": lat,
            "longitude": lon,
            "start_date": date,
            "end_date": date,
            "hourly": "temperature_2m,precipitation",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def write_landing_file(date: str, city: str, payload: dict) -> Path:
    LANDING_ZONE.mkdir(parents=True, exist_ok=True)
    out_path = LANDING_ZONE / f"weather_{city}_{date}.jsonl"
    with open(out_path, "w") as f:
        f.write(json.dumps(payload))
        f.write("\n")
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--city", default="london", choices=sorted(CITIES))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    out_path = LANDING_ZONE / f"weather_{args.city}_{args.date}.jsonl"
    if out_path.exists() and not args.force:
        print(f"{out_path} already exists, skipping (use --force to re-fetch)")
        return

    payload = fetch_weather(args.date, args.city)
    written = write_landing_file(args.date, args.city, payload)
    print(f"Wrote {written}")


if __name__ == "__main__":
    main()
