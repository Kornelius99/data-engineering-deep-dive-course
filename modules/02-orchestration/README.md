# Module 02: Orchestration

## The concept

A pipeline is more than a script - it's a set of steps with dependencies, retry behavior, and a schedule. This module wraps module 01's ingest.py in an Airflow DAG (dags/course_dag.py) that runs daily, then chains a load-to-warehouse step after it.

## Why retries and dependencies are the point of orchestration, not scheduling

Cron can run something every day. What cron can't do well is: retry only the failed step (not the whole pipeline), express 'step B must wait for step A', alert you specifically about which step failed, or give you a UI showing the last 30 days of runs at a glance. That's the actual value Airflow adds over a cron job calling a shell script - the scheduling part is almost incidental.

## Reading dags/course_dag.py

Two tasks: ingest_weather (PythonOperator wrapping module 01's fetch_weather function) then load_to_warehouse (PythonOperator calling module 03's loader). The dependency is declared with ingest_weather >> load_to_warehouse. retries=2 and retry_delay=5 minutes are set at the DAG's default_args level, so both tasks inherit them without repeating the config.

## Run it

```bash
docker compose up -d airflow
# copy the DAG into Airflow's dags folder (docker-compose.yml already mounts modules/02-orchestration/dags as a volume)
```

Open http://localhost:8080, find course_dag, un-pause it, and trigger a manual run. Watch the graph view - you'll see ingest_weather turn green, then load_to_warehouse start.

## Exercise

1. Add a third task, notify_on_failure, that only runs if a previous task fails (hint: trigger_rule=TriggerRule.ONE_FAILED).
2. Change the schedule from daily to hourly and explain in a comment why that would or wouldn't make sense for a weather-archive API specifically (the archive API has its own data-availability lag - check the exercise solution's comment for the reasoning).

Next: [Module 03 - Warehouse](../03-warehouse)
