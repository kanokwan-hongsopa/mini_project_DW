select
    a.airport_code,
    a.airport_name,
    a.city,
    sum(f.ticket_flight_count) as total_ticket_flights
from {{ ref('fact_ticket_sales') }} f

join {{ ref('dim_airport') }} a
    on f.arrival_airport_key = a.airport_key

group by
    a.airport_code,
    a.airport_name,
    a.city

order by
    total_ticket_flights desc