select
    dep.airport_code as departure_airport,
    dep.airport_name as departure_airport_name,
    arr.airport_code as arrival_airport,
    arr.airport_name as arrival_airport_name,

    avg(fsu.boarded_load_pct) as avg_boarded_load_pct,
    sum(fsu.boarded_count) as total_boarded_count,
    sum(fsu.seat_capacity) as total_seat_capacity,
    count(*) as flight_count

from {{ ref('fact_seat_utilization') }} fsu

left join {{ ref('dim_airport') }} dep
    on fsu.departure_airport_key = dep.airport_key

left join {{ ref('dim_airport') }} arr
    on fsu.arrival_airport_key = arr.airport_key

group by
    dep.airport_code,
    dep.airport_name,
    arr.airport_code,
    arr.airport_name

having count(*) > 0

order by
    avg_boarded_load_pct desc