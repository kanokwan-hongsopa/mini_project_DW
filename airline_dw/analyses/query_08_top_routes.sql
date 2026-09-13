select
    dep.airport_code as departure_airport,
    arr.airport_code as arrival_airport,

    dep.city as departure_city,
    arr.city as arrival_city,

    sum(f.ticket_flight_count) as total_ticket_flights

from {{ ref('fact_ticket_sales') }} f

join {{ ref('dim_airport') }} dep
    on f.departure_airport_key = dep.airport_key

join {{ ref('dim_airport') }} arr
    on f.arrival_airport_key = arr.airport_key

group by
    dep.airport_code,
    arr.airport_code,
    dep.city,
    arr.city

order by
    total_ticket_flights desc