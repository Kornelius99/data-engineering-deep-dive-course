"""Module 01: ingest raw weather data for a given date into a landing zone.

Usage:
    python modules/01-ingestion/ingest.py --date 2024-01-15
    python modules/01-ingestion/ingest.py --date 2024-01-15 --force

Idempotent by design: re-running the same --date is a no-op unless --force
is passed, because the output filename is derived purely from the logical
date, not wall-clock time.
"""
import argparse
import json
import os
from pathlib import Path

import requests

LANDING_ZONE = Path(__file__).resolve().parents[2] / "landing_zone"

# London, for simplicity. See the exercise for adding a --city flag.
LATITUDE = 51.5072
LONGITUDE = -0.1276


def fetch_weather(date: str) -> dict:
    resp = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "start_date": date,
            "end_date": date,
            "hourly": "temperature_2m,precipitation",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def write_landing_file(date: str, payload: dict) -> Path:
    LANDING_ZONE.mkdir(parents=True, exist_ok=True)
    out_path = LANDING_ZONE / f"weather_{date}.jsonl"
    with open(out_path, "w") as f:
        f.write(json.dumps(payload))
        f.write("\n")
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--force", action="store_true", help="Re-fetch even if the file already exists")
    args = parser.parse_args()

    out_path = LANDING_ZONE / f"weather_{args.date}.jsonl"
    if out_path.exists() and not args.force:
        print(f"{out_path} already exists, skipping (use --force to re-fetch)")
        return

    payload = fetch_weather(args.date)
    written = write_landing_file(args.date, payload)
    print(f"Wrote {written}")


if __name__ == "__main__":
    main()
