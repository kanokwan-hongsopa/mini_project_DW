with source as (

    select *
    from {{ source('raw', 'boarding_passes') }}

),

cleaned as (

    select
        trim(cast(ticket_no as varchar))
            as ticket_no,

        cast(flight_id as integer)
            as flight_id,

        cast(boarding_no as integer)
            as boarding_no,

        upper(trim(cast(seat_no as varchar)))
            as seat_no

    from source

)

select *
from cleaned