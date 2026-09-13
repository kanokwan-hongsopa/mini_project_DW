select
    d.full_date,
    sum(f.amount) as total_sales
from {{ ref('fact_ticket_sales') }} f

join {{ ref('dim_date') }} d
    on f.date_key = d.date_key

group by
    d.full_date

order by
    d.full_date