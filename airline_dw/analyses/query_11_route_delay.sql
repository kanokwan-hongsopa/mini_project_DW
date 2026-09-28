select
    dep.airport_code as departure_airport,
    arr.airport_code as arrival_airport,

    round(avg(ffo.departure_delay_minutes), 2) as avg_departure_delay_minutes,
    round(avg(ffo.arrival_delay_minutes), 2) as avg_arrival_delay_minutes,

    sum(ffo.flight_count) as total_flights

from {{ ref('fact_flight_operations') }} ffo

left join {{ ref('dim_airport') }} dep
    on ffo.departure_airport_key = dep.airport_key

left join {{ ref('dim_airport') }} arr
    on ffo.arrival_airport_key = arr.airport_key

where
    ffo.departure_delay_minutes is not null
    or ffo.arrival_delay_minutes is not null

group by
    dep.airport_code,
    arr.airport_code

order by
    avg_departure_delay_minutes desc