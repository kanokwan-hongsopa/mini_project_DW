select
    dep.airport_code as departure_airport,
    dep.airport_name as departure_airport_name,
    arr.airport_code as arrival_airport,
    arr.airport_name as arrival_airport_name,

    sum(fts.amount) as total_revenue,
    sum(fts.ticket_flight_count) as ticket_flight_count

from {{ ref('fact_ticket_sales') }} fts

left join {{ ref('dim_airport') }} dep
    on fts.departure_airport_key = dep.airport_key

left join {{ ref('dim_airport') }} arr
    on fts.arrival_airport_key = arr.airport_key

group by
    dep.airport_code,
    dep.airport_name,
    arr.airport_code,
    arr.airport_name

order by total_revenue desc