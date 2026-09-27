select
    fsu.flight_id,

    dep.airport_code as departure_airport,
    arr.airport_code as arrival_airport,

    fsu.ticket_flight_count,
    fsu.boarded_count,
    fsu.booked_not_boarded_count,

    fsu.seat_capacity,
    fsu.ticketed_load_pct,
    fsu.boarded_load_pct

from {{ ref('fact_seat_utilization') }} fsu

left join {{ ref('dim_airport') }} dep
    on fsu.departure_airport_key = dep.airport_key

left join {{ ref('dim_airport') }} arr
    on fsu.arrival_airport_key = arr.airport_key

order by
    fsu.booked_not_boarded_count desc