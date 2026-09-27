select
    d.year,
    d.month,
    d.month_name,
    sum(fts.amount) as total_revenue,
    sum(fts.ticket_flight_count) as ticket_flight_count

from {{ ref('fact_ticket_sales') }} fts

left join {{ ref('dim_date') }} d
    on fts.date_key = d.date_key

group by
    d.year,
    d.month,
    d.month_name

order by
    d.year,
    d.month