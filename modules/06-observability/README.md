# Module 06: Observability

## The concept

Modules 01-05 build a working pipeline. This module makes it debuggable at 3am when it breaks. metrics.py adds two things: structured (JSON) logging instead of plain print statements, and a tiny metrics emitter that records run duration and row counts you can later graph or alert on.

## Why structured logging, not print()

log.info(f'loaded {n} rows') is fine until you have 50 pipelines' logs mixed together in one place, at which point you need to filter and query them like data - which means they need to actually be structured data (JSON), not free-form sentences. emit_log() below writes one JSON object per line specifically so any log aggregator (CloudWatch Logs Insights, Datadog, even just jq on a file) can filter by field without regex.

## Why metrics are emitted as events, not just left in Airflow's UI

Airflow's UI shows you the current and recent state of tasks, which is great for 'what's happening now' but bad for 'has our average load duration crept up over the last 3 months'. Emitting a metric event per run (to a file here; to CloudWatch/Prometheus/Datadog in a real system) means you can build a trend chart independent of whatever orchestrator you're using this year - this is exactly the pattern the pipeline-cost-observatory project builds a whole dashboard around.

## Run it

```bash
cd modules/06-observability
python -c "from metrics import emit_log, emit_metric; emit_log('info', 'test message', pipeline='course_dag'); emit_metric('rows_loaded', 42, pipeline='course_dag')"
cat metrics.jsonl
```

## Exercise

1. Wire emit_metric into module 03's load.py to record rows_loaded after every load.
2. Write a small script that reads metrics.jsonl and prints an ASCII bar chart of rows_loaded over the last 7 runs (no plotting library needed - this is the same idea pipeline-cost-observatory's Streamlit dashboard does, just without the UI).

Next: [Module 07 - Deployment](../07-deployment)
