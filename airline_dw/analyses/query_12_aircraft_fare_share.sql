with seat_summary as (

    select
        a.aircraft_key,
        a.aircraft_code,
        a.model,
        fc.fare_class,
        sum(f.seat_count) as seat_count

    from {{ ref('fact_seat_inventory') }} f

    join {{ ref('dim_aircraft') }} a
        on f.aircraft_key = a.aircraft_key

    join {{ ref('dim_fare_class') }} fc
        on f.fare_class_key = fc.fare_class_key

    group by
        a.aircraft_key,
        a.aircraft_code,
        a.model,
        fc.fare_class
),

final as (

    select
        aircraft_code,
        model,
        fare_class,
        seat_count,

        round(
            seat_count * 100.0
            / sum(seat_count) over (
                partition by aircraft_key
            ),
            2
        ) as seat_percentage

    from seat_summary
)

select *
from final
order by
    model,
    seat_percentage desc