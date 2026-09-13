with ticket_fares as (

    select distinct
        trim(fare_conditions) as fare_conditions
    from {{ ref('stg_ticket_flights') }}
    where fare_conditions is not null

),

seat_fares as (

    select distinct
        trim(fare_conditions) as fare_conditions
    from {{ ref('stg_seats') }}
    where fare_conditions is not null

),

combined as (

    select fare_conditions
    from ticket_fares

    union

    select fare_conditions
    from seat_fares

),

final as (

    select
        row_number() over (order by fare_conditions) as fare_class_key,
        fare_conditions as fare_class
    from combined

)

select *
from final