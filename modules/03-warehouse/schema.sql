-- Module 03: a small star schema for the course warehouse.

CREATE TABLE IF NOT EXISTS dim_city (
    city_id   SERIAL PRIMARY KEY,
    city_name TEXT UNIQUE NOT NULL,
    latitude  NUMERIC NOT NULL,
    longitude NUMERIC NOT NULL
);

INSERT INTO dim_city (city_name, latitude, longitude)
VALUES ('london', 51.5072, -0.1276)
ON CONFLICT (city_name) DO NOTHING;

CREATE TABLE IF NOT EXISTS fact_weather_hourly (
    fact_id         SERIAL PRIMARY KEY,
    city_id         INTEGER NOT NULL REFERENCES dim_city(city_id),
    observed_at     TIMESTAMPTZ NOT NULL,
    temperature_c   NUMERIC,
    precipitation_mm NUMERIC,
    loaded_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (city_id, observed_at)
);

CREATE INDEX IF NOT EXISTS idx_fact_weather_hourly_observed_at
    ON fact_weather_hourly(observed_at);
