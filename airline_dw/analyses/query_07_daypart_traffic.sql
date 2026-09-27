select
    departure_daypart,

    sum(flight_count) as total_flights,
    sum(boarded_count) as total_boarded_passengers

from {{ ref('fact_flight_operations') }}

group by
    departure_daypart

order by
    total_boarded_passengers desc