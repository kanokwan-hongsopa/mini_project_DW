select
    dep.analysis_region as departure_region,
    arr.analysis_region as arrival_region,

    sum(fts.ticket_flight_count) as ticket_flight_count,
    sum(fts.amount) as total_revenue

from {{ ref('fact_ticket_sales') }} fts

left join {{ ref('dim_airport') }} dep
    on fts.departure_airport_key = dep.airport_key

left join {{ ref('dim_airport') }} arr
    on fts.arrival_airport_key = arr.airport_key

group by
    dep.analysis_region,
    arr.analysis_region

order by
    ticket_flight_count desc