with source as (

    select *
    from {{ source('raw', 'bookings') }}

),

cleaned as (

    select
        cast(book_ref as varchar) as book_ref,
        cast(book_date as timestamp) as book_date,
        cast(total_amount as decimal(18,2)) as total_amount
    from source

)

select *
from cleaned