# Module 05: Data quality

## The concept

dbt's built-in not_null/unique tests (used in module 04) catch structural problems. This module adds checks.py: a small standalone framework for the checks dbt tests can't express - checks that need custom logic, like 'is this row count wildly different from yesterday's'.

## Why these five checks specifically

completeness (are required fields null more than X% of the time), uniqueness (are there duplicate keys), referential integrity (does every city_id in the fact table exist in dim_city), freshness (has data landed in the last N hours), and row-count anomaly (is today's row count wildly different from a rolling average) - together these five catch the large majority of real pipeline breakages people actually see in production: a schema change upstream, a duplicate load, a broken foreign key from an out-of-order load, a silently-stopped-running DAG, and a partial/duplicated load, respectively.

## Why row-count anomaly detection uses a rolling average, not a fixed threshold

A fixed threshold ('alert if fewer than 24 rows') breaks the moment your data volume legitimately changes (you add a city, traffic grows). Comparing against a trailing rolling average adapts automatically and is the same idea used in the pipeline-cost-observatory project's anomaly detection - if a metric is unusually far from its own recent history, that's more informative than any fixed number you'd pick today and forget to update later.

## Run it

```bash
pip install -r requirements.txt
pytest modules/05-data-quality/tests/ -v
```

## Exercise

1. Add a sixth check: schema drift detection (compare a table's current column set against a saved baseline, flag any additions/removals).
2. Wire check_all() into module 02's DAG as a task that runs after load_to_warehouse and fails the DAG run if any check fails.

Next: [Module 06 - Observability](../06-observability)
