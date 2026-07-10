# data-engineering-deep-dive-course

A hands-on, end-to-end data engineering course, in one repository. Most tutorials teach one tool in isolation - this connects the whole path a real record travels: from a raw source, through orchestration, into a warehouse, through transformation, past data quality checks, with observability, all the way to a real deployment.

## Who this is for

Anyone who can already write basic Python and SQL and wants to understand how the pieces of a real data platform fit together - whether you're learning data engineering from scratch, coming from data analysis/software engineering and want the platform side, or prepping for interviews and want to be able to explain why, not just how.

## How this course is different

Every module below is runnable, not just readable. Each one has: a README explaining the concept and the specific design decisions made, working code you run yourself, and an exercise with a solution you can check your work against. By the end, module 7 deploys the whole thing for real.

## The learning path

| # | Module | What you'll learn |
|---|--------|--------------------|
| 00 | [setup](modules/00-setup) | Environment setup, repo tour |
| 01 | [ingestion](modules/01-ingestion) | Pulling raw data from an API into a landing zone, idempotently |
| 02 | [orchestration](modules/02-orchestration) | Wiring steps into an Airflow DAG with retries and dependencies |
| 03 | [warehouse](modules/03-warehouse) | Star-schema design, loading a Postgres warehouse |
| 04 | [transformation](modules/04-transformation) | Bronze/silver/gold-style modeling with dbt |
| 05 | [data-quality](modules/05-data-quality) | Writing tests that actually catch real failure modes |
| 06 | [observability](modules/06-observability) | Structured logging and pipeline metrics you can alert on |
| 07 | [deployment](modules/07-deployment) | Running the whole stack for real, not just on localhost |

## Getting started

```bash
git clone https://github.com/Kornelius99/data-engineering-deep-dive-course.git
cd data-engineering-deep-dive-course
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then start at modules/00-setup/README.md and work through the modules in order - each one builds on artifacts produced by the previous one (module 2's DAG orchestrates module 1's ingestion script, module 4's dbt models read module 3's warehouse tables, and so on).

## Running the shared infrastructure

```bash
docker compose up -d
```

This starts Postgres (the warehouse) and Airflow, matching what modules 00-03 assume is running. Modules 04-06 (dbt, data quality checks, logging/metrics) run as plain Python/CLI commands against that infrastructure rather than as their own containers - see each module's own README for its exact run command. See [modules/07-deployment](modules/07-deployment) for taking this further, to a real deployment reachable over the internet.

## Honesty / limitations

I wrote and reviewed every module's code and explanations carefully, but have not run the full docker-compose stack against a live multi-day workload myself (I don't have a persistent runtime available to me). Please treat your first run-through as a learning exercise, and open an issue if a module's instructions don't match what you see.

## License

MIT — see [LICENSE](LICENSE).
