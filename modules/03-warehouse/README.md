# Module 03: Warehouse

## The concept

Raw JSON in a landing zone isn't queryable by analysts. This module defines a small star schema in Postgres (schema.sql) and a loader (load.py) that reads a landing-zone file and writes it into a fact table.

## Why a star schema, and why this one specifically

fact_weather_hourly holds one row per (city, hour) with the measurements (temperature, precipitation) - the grain is explicit and narrow, which is the single most important property of a fact table (get the grain wrong and every downstream aggregation is subtly wrong). dim_city is a tiny dimension table holding city metadata, so the fact table stays narrow and city details (name, latitude, longitude) aren't repeated on every row.

## Why the loader is idempotent via upsert, not append

load.py uses INSERT ... ON CONFLICT (city_id, observed_at) DO UPDATE, not a plain INSERT. Combined with module 01's idempotent ingestion, this means re-running the whole pipeline for a past date - because you fixed a bug, or Airflow retried a task - produces the same end state instead of duplicate rows. This 'idempotent all the way through' property is what separates pipelines that are safe to replay from ones where every rerun requires manual cleanup.

## Run it

```bash
psql postgresql://postgres:postgres@localhost:5432/course -f modules/03-warehouse/schema.sql
python modules/01-ingestion/ingest.py --date 2024-01-15
python modules/03-warehouse/load.py --date 2024-01-15
```

Check it landed:

```bash
psql postgresql://postgres:postgres@localhost:5432/course -c 'select * from fact_weather_hourly limit 5;'
```

## Exercise

1. Add a dim_date table (date, day_of_week, is_weekend, month, year) and join it into a view that shows average temperature by day-of-week.
2. Run the loader twice for the same date and confirm row counts don't double (that's the upsert behavior working).

Next: [Module 04 - Transformation](../04-transformation)
