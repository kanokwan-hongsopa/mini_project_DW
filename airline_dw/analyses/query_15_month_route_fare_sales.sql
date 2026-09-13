with sales_summary as (

    select
        d.year,
        d.month,
        d.month_name,

        dep.airport_code as departure_airport,
        arr.airport_code as arrival_airport,

        fc.fare_class,

        sum(f.amount) as total_ticket_sales

    from {{ ref('fact_ticket_sales') }} f

    join {{ ref('dim_date') }} d
        on f.date_key = d.date_key

    join {{ ref('dim_airport') }} dep
        on f.departure_airport_key = dep.airport_key

    join {{ ref('dim_airport') }} arr
        on f.arrival_airport_key = arr.airport_key

    join {{ ref('dim_fare_class') }} fc
        on f.fare_class_key = fc.fare_class_key

    group by
        d.year,
        d.month,
        d.month_name,
        dep.airport_code,
        arr.airport_code,
        fc.fare_class
),

ranked as (

    select
        *,
        dense_rank() over (
            partition by year, month
            order by total_ticket_sales desc
        ) as sales_rank

    from sales_summary
)

select
    year,
    month,
    month_name,
    departure_airport,
    arrival_airport,
    fare_class,
    total_ticket_sales

from ranked

where sales_rank = 1

order by
    year,
    month