with seats as (

    select *
    from {{ ref('stg_seats') }}

),

aggregated as (

    select
        aircraft_code,
        fare_conditions,
        count(*) as seat_count

    from seats

    group by
        aircraft_code,
        fare_conditions

),

final as (

    select
        row_number() over (
            order by a.aircraft_key, f.fare_class_key
        ) as seat_inventory_key,

        a.aircraft_key,
        f.fare_class_key,

        ag.seat_count

    from aggregated ag

    left join {{ ref('dim_aircraft') }} a
        on ag.aircraft_code = a.aircraft_code

    left join {{ ref('dim_fare_class') }} f
        on ag.fare_conditions = f.fare_class

)

select *
from final