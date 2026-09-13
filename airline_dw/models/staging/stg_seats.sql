with source as (

    select *
    from {{ source('raw', 'seats') }}

),

cleaned as (

    select
        upper(trim(cast(aircraft_code as varchar)))
            as aircraft_code,

        upper(trim(cast(seat_no as varchar)))
            as seat_no,

        trim(cast(fare_conditions as varchar))
            as fare_conditions

    from source

)

select *
from cleaned