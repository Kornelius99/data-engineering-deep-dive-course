# Module 04: Transformation

## The concept

The fact table from module 03 is at hourly grain - useful for detail, awkward for a dashboard asking 'what was the weather like each day?'. This module uses dbt to build a staging model (light cleanup) and a mart model (daily aggregation) on top of it.

## Why staging models exist at all (they look like a pointless passthrough)

stg_weather.sql looks almost like SELECT * from the source table, which seems pointless - but it's where you rename columns to your team's naming convention, cast types explicitly, and give every downstream model a single, stable interface to the source. If the source table's column names ever change, you fix it in exactly one place (the staging model) instead of in every mart that used the old name.

## Why the aggregation lives in a mart, not in the BI tool

fct_daily_weather.sql computes avg/min/max temperature per city per day. Doing this in dbt (version-controlled, tested, code-reviewed SQL) instead of as a calculated field buried in a BI tool means the logic is: visible in git history, covered by the tests in modules/05-data-quality, and reusable by any tool that queries the warehouse, not just the one dashboard where someone happened to build the calculation.

## Run it

```bash
cd modules/04-transformation
dbt run
dbt test
```

## Exercise

1. Add a fct_weather_anomalies model that flags days where the daily temperature range (max - min) is more than 2 standard deviations above that city's historical average range.
2. Add a not_null and a unique test on fct_daily_weather's (city_id, date) - see modules/05-data-quality for why these two tests specifically catch the most common real-world breakage.

Next: [Module 05 - Data quality](../05-data-quality)
