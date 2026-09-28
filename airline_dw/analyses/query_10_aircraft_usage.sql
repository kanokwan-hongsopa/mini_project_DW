select
    da.manufacturer,
    da.model as aircraft_model,
    sum(ffo.flight_count) as total_flights

from {{ ref('fact_flight_operations') }} ffo

left join {{ ref('dim_aircraft') }} da
    on ffo.aircraft_key = da.aircraft_key

group by
    da.manufacturer,
    da.model

order by
    total_flights desc