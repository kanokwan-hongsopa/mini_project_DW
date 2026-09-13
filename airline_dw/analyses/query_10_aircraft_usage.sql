select
    a.aircraft_code,
    a.model,
    sum(f.flight_count) as total_flights
from {{ ref('fact_flight_operations') }} f

join {{ ref('dim_aircraft') }} a
    on f.aircraft_key = a.aircraft_key

group by
    a.aircraft_code,
    a.model

order by total_flights desc