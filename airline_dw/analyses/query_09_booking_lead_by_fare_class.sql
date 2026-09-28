select
    dfc.fare_class,

    round(avg(fts.booking_lead_days), 2) as avg_booking_lead_days,
    median(fts.booking_lead_days) as median_booking_lead_days,
    min(fts.booking_lead_days) as min_booking_lead_days,
    max(fts.booking_lead_days) as max_booking_lead_days,

    sum(fts.ticket_flight_count) as ticket_flight_count

from {{ ref('fact_ticket_sales') }} fts

left join {{ ref('dim_fare_class') }} dfc
    on fts.fare_class_key = dfc.fare_class_key

where fts.booking_lead_days is not null

group by dfc.fare_class

order by avg_booking_lead_days desc