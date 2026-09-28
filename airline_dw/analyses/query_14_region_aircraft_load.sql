select
    dep.analysis_region as departure_region,
    da.manufacturer,
    da.model as aircraft_model,

    sum(fsu.boarded_count) as total_boarded_count,
    sum(fsu.seat_capacity) as total_seat_capacity,

    round(
        100.0 * sum(fsu.boarded_count)
        / nullif(sum(fsu.seat_capacity), 0),
        2
    ) as boarded_load_pct,

    count(*) as flight_count

from {{ ref('fact_seat_utilization') }} fsu

left join {{ ref('dim_airport') }} dep
    on fsu.departure_airport_key = dep.airport_key

left join {{ ref('dim_aircraft') }} da
    on fsu.aircraft_key = da.aircraft_key

where
    dep.analysis_region is not null
    and da.model is not null

group by
    dep.analysis_region,
    da.manufacturer,
    da.model

order by
    departure_region,
    boarded_load_pct desc