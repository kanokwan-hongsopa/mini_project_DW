with fare_revenue as (

    select
        dfc.fare_class,
        sum(fts.amount) as total_revenue

    from {{ ref('fact_ticket_sales') }} fts

    left join {{ ref('dim_fare_class') }} dfc
        on fts.fare_class_key = dfc.fare_class_key

    group by
        dfc.fare_class
),

final as (

    select
        fare_class,
        total_revenue,

        round(
            100.0 * total_revenue
            / sum(total_revenue) over (),
            2
        ) as revenue_share_pct

    from fare_revenue
)

select *
from final

order by total_revenue desc