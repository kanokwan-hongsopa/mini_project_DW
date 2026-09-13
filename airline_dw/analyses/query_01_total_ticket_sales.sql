select
    sum(amount) as total_ticket_sales
from {{ ref('fact_ticket_sales') }}