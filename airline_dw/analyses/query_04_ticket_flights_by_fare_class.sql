select
    fc.fare_class,
    sum(f.ticket_flight_count) as total_ticket_flights
from {{ ref('fact_ticket_sales') }} f

join {{ ref('dim_fare_class') }} fc
    on f.fare_class_key = fc.fare_class_key

group by
    fc.fare_class

order by
    total_ticket_flights desc