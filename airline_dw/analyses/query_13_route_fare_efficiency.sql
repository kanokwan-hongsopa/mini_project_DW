select
    dep.airport_code as departure_airport,
    arr.airport_code as arrival_airport,
    dfc.fare_class,

    sum(fts.amount) as total_revenue,
    sum(fts.ticket_flight_count) as ticket_count,

    round(
        sum(fts.amount) / nullif(sum(fts.ticket_flight_count), 0),
        2
    ) as revenue_per_ticket

from {{ ref('fact_ticket_sales') }} fts

left join {{ ref('dim_airport') }} dep
    on fts.departure_airport_key = dep.airport_key

left join {{ ref('dim_airport') }} arr
    on fts.arrival_airport_key = arr.airport_key

left join {{ ref('dim_fare_class') }} dfc
    on fts.fare_class_key = dfc.fare_class_key

group by
    dep.airport_code,
    arr.airport_code,
    dfc.fare_class

having sum(fts.ticket_flight_count) > 0

order by
    revenue_per_ticket desc