select
    dep.airport_code as departure_airport,
    dep.airport_name as departure_airport_name,
    arr.airport_code as arrival_airport,
    arr.airport_name as arrival_airport_name,
    sum(f.amount) as total_ticket_sales
from {{ ref('fact_ticket_sales') }} f

join {{ ref('dim_airport') }} dep
    on f.departure_airport_key = dep.airport_key

join {{ ref('dim_airport') }} arr
    on f.arrival_airport_key = arr.airport_key

group by
    dep.airport_code,
    dep.airport_name,
    arr.airport_code,
    arr.airport_name

order by total_ticket_sales desc