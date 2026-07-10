-- Daily aggregation mart: one row per (city, day). This is the grain a
-- dashboard actually wants, computed once here instead of recomputed
-- ad hoc in every BI tool that queries the warehouse.

select
    city_id,
    city_name,
    observed_date,
    avg(temperature_c)  as avg_temperature_c,
    min(temperature_c)  as min_temperature_c,
    max(temperature_c)  as max_temperature_c,
    sum(precipitation_mm) as total_precipitation_mm
from {{ ref('stg_weather') }}
group by 1, 2, 3
