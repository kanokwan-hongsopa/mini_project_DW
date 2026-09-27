with source as (

    select *
    from {{ source('raw', 'tickets') }}

),

cleaned as (

    select
        cast(ticket_no as varchar) as ticket_no,
        cast(book_ref as varchar) as book_ref,
        cast(passenger_id as varchar) as passenger_id,
        cast(book_date as timestamp) as book_date,
        cast(book_date_key as integer) as book_date_key,
        trim(cast(book_day_type as varchar)) as book_day_type
    from source

)

select *
from cleaned