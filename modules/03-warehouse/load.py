"""Module 03: load a landing-zone weather file into the fact_weather_hourly table.

Usage:
    python modules/03-warehouse/load.py --date 2024-01-15
"""
import argparse
import json
import os
from pathlib import Path

import psycopg2

LANDING_ZONE = Path(__file__).resolve().parents[2] / "landing_zone"
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/course")


def load_landing_file_to_warehouse(date: str, city: str = "london") -> int:
    path = LANDING_ZONE / f"weather_{date}.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"No landing file at {path} - run module 01's ingest.py first")

    with open(path) as f:
        payload = json.loads(f.readline())

    hourly = payload["hourly"]
    times = hourly["time"]
    temps = hourly["temperature_2m"]
    precip = hourly["precipitation"]

    conn = psycopg2.connect(DATABASE_URL)
    inserted = 0
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT city_id FROM dim_city WHERE city_name = %s", (city,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"City '{city}' not found in dim_city - run schema.sql first")
            city_id = row[0]

            for observed_at, temp_c, precip_mm in zip(times, temps, precip):
                cur.execute(
                    """
                    INSERT INTO fact_weather_hourly (city_id, observed_at, temperature_c, precipitation_mm)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (city_id, observed_at)
                    DO UPDATE SET temperature_c = EXCLUDED.temperature_c,
                                  precipitation_mm = EXCLUDED.precipitation_mm,
                                  loaded_at = now()
                    """,
                    (city_id, observed_at, temp_c, precip_mm),
                )
                inserted += 1
        conn.commit()
    finally:
        conn.close()

    return inserted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--city", default="london")
    args = parser.parse_args()

    count = load_landing_file_to_warehouse(args.date, args.city)
    print(f"Upserted {count} hourly rows for {args.city} on {args.date}")


if __name__ == "__main__":
    main()
