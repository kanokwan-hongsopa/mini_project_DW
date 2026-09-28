select
    dep.analysis_region as departure_region,
    ffo.departure_daypart,

    round(avg(ffo.departure_delay_minutes), 2) as avg_departure_delay_minutes,
    sum(ffo.flight_count) as total_flights

from {{ ref('fact_flight_operations') }} ffo

left join {{ ref('dim_airport') }} dep
    on ffo.departure_airport_key = dep.airport_key

where
    ffo.departure_delay_minutes is not null
    and dep.analysis_region is not null
    and ffo.departure_daypart is not null

group by
    dep.analysis_region,
    ffo.departure_daypart

order by
    avg_departure_delay_minutes desc