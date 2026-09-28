with route_daypart as (

    select
        dep.airport_code as departure_airport,
        arr.airport_code as arrival_airport,
        fsu.departure_daypart,

        sum(fsu.ticket_flight_count) as ticket_flight_count,
        sum(fsu.boarded_count) as boarded_count,
        sum(fsu.seat_capacity) as seat_capacity,
        count(*) as flight_count,

        round(
            100.0 * sum(fsu.boarded_count)
            / nullif(sum(fsu.seat_capacity), 0),
            2
        ) as boarded_load_pct

    from {{ ref('fact_seat_utilization') }} fsu

    left join {{ ref('dim_airport') }} dep
        on fsu.departure_airport_key = dep.airport_key

    left join {{ ref('dim_airport') }} arr
        on fsu.arrival_airport_key = arr.airport_key

    where
        fsu.departure_daypart is not null

    group by
        dep.airport_code,
        arr.airport_code,
        fsu.departure_daypart
)

select *
from route_daypart
order by
    boarded_load_pct desc,
    boarded_count desc