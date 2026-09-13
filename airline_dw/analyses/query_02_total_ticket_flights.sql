select
    sum(ticket_flight_count) as total_ticket_flights
from {{ ref('fact_ticket_sales') }}