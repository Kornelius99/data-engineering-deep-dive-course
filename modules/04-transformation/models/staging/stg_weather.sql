-- Staging model: renames/casts columns from the raw fact table so every
-- downstream model has a single, stable interface to the source.
-- (Referencing the source tables directly by name here, rather than via
-- {{ source() }}, to keep this course's dbt setup minimal - a production
-- project should declare these in a sources.yml instead.)

select
    f.fact_id                    as weather_fact_id,
    f.city_id,
    c.city_name,
    f.observed_at,
    f.observed_at::date          as observed_date,
    f.temperature_c::numeric     as temperature_c,
    f.precipitation_mm::numeric  as precipitation_mm
from fact_weather_hourly f
join dim_city c on c.city_id = f.city_id
