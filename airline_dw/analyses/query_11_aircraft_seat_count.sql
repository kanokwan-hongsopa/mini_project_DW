select
    a.aircraft_code,
    a.model,
    sum(f.seat_count) as total_seats
from {{ ref('fact_seat_inventory') }} f

join {{ ref('dim_aircraft') }} a
    on f.aircraft_key = a.aircraft_key

group by
    a.aircraft_code,
    a.model

order by total_seats desc