# Module 00: Setup

## What you'll do

Get your environment ready so every later module just works.

1. Install Python 3.11+, Docker, and Docker Compose.
2. Clone this repo and create a virtualenv:

       python -m venv .venv
       source .venv/bin/activate
       pip install -r requirements.txt

3. Start the shared infrastructure this course uses (Postgres as the warehouse, Airflow for orchestration):

       docker compose up -d postgres airflow

4. Confirm Postgres is reachable:

       psql postgresql://postgres:postgres@localhost:5432/course -c 'select 1;'

## Repo tour

- modules/ - one folder per lesson, work through them in numeric order.
- Each module's README explains the concept, then points you at code in that same folder.
- docker-compose.yml at the repo root wires up everything modules 02-06 individually describe.
- requirements.txt at the repo root covers every module's Python dependencies (a real project would split these per-service, but one file keeps the course simpler to run).

## Why Postgres and Airflow specifically

They're the most common 'boring, reliable' choices in real data teams: Postgres because most warehousing/analytics-adjacent workloads at small-to-mid scale don't need Snowflake/BigQuery-level scale, and Airflow because it remains the most widely-deployed orchestrator you're likely to meet in a job. The concepts transfer directly to Snowflake/BigQuery/Redshift and to Dagster/Prefect if that's what you end up using at work.

## Exercise

Before moving to module 01, confirm you can do all three of these:

1. Run python -c "import pandas, requests, sqlalchemy" with no errors.
2. Open http://localhost:8080 and see the Airflow UI (default login admin/admin from docker-compose.yml).
3. Connect to Postgres with any client and list tables (there won't be any yet - that's expected).

If any of these fail, fix them here before continuing - every later module assumes this works.

Next: [Module 01 - Ingestion](../01-ingestion)
