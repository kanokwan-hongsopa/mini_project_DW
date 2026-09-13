with source as (

    select *
    from {{ source('raw', 'tickets') }}

),

cleaned as (

    select
        cast(ticket_no as varchar) as ticket_no,
        cast(book_ref as varchar) as book_ref,
        cast(passenger_id as varchar) as passenger_id
    from source

)

select *
from cleaned