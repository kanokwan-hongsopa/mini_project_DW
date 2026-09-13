with source as (

    select *
    from {{ source('raw', 'ticket_flights') }}

),

cleaned as (

    select
        cast(ticket_no as varchar) as ticket_no,
        cast(flight_id as integer) as flight_id,
        trim(cast(fare_conditions as varchar)) as fare_conditions,
        cast(amount as decimal(18,2)) as amount
    from source

)

select *
from cleaned