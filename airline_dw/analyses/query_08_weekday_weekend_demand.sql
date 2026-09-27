select
    case
        when departure_is_weekend then 'Weekend'
        else 'Weekday'
    end as day_type,

    sum(flight_count) as total_flights,
    sum(boarded_count) as total_boarded_passengers,

    round(
        avg(boarded_count),
        2
    ) as avg_boarded_per_flight

from {{ ref('fact_flight_operations') }}

group by
    departure_is_weekend

order by
    total_boarded_passengers desc