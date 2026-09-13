select
    a.airport_code,
    a.airport_name,
    a.city,
    round(avg(f.departure_delay_minutes), 2) as avg_departure_delay_minutes,
    count(*) as delayed_flights

from {{ ref('fact_flight_operations') }} f

join {{ ref('dim_airport') }} a
    on f.departure_airport_key = a.airport_key

where f.departure_delay_minutes > 0

group by
    a.airport_code,
    a.airport_name,
    a.city

order by
    avg_departure_delay_minutes desc