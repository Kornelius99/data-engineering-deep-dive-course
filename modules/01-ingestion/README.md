# Module 01: Ingestion

## The concept

Every pipeline starts with getting raw data somewhere you control. This module pulls data from a public API (Open-Meteo weather API - free, no API key required) and lands it as-is (raw, unmodified) into a local landing_zone/ directory as newline-delimited JSON, one file per run.

## Why land raw data unmodified first

This is the single most-skipped step in tutorials, and the one that saves you the most pain in production. If you transform data on the way in and your transformation logic has a bug, you've lost the original data - you can't reprocess what you never kept. Landing the raw response first means any bug downstream is always recoverable by reprocessing from the landing zone.

## Why idempotency matters here

ingest.py names each output file with the run's logical date (not wall-clock time), and skips re-fetching if that date's file already exists (unless --force is passed). Re-running the same day's ingestion twice must not create duplicate or conflicting data - this is the property that lets Airflow safely retry a failed task in module 02 without you thinking about cleanup.

## Run it

```bash
python modules/01-ingestion/ingest.py --date 2024-01-15
```

Check the output:

```bash
cat landing_zone/weather_2024-01-15.jsonl
```

Run it again with the same date - notice it skips instead of re-downloading:

```bash
python modules/01-ingestion/ingest.py --date 2024-01-15
```

## Exercise

1. Modify ingest.py to also fetch a second city (it currently hardcodes London's coordinates) - add a --city flag.
2. Add a retry with exponential backoff around the requests.get call, so a transient network failure doesn't crash the whole ingestion.
3. Solution: see ingest_solution.py for one way to do both.

Next: [Module 02 - Orchestration](../02-orchestration)
