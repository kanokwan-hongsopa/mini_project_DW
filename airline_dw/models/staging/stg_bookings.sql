with source as (

    select *
    from {{ source('raw', 'bookings') }}

),

cleaned as (

    select
        cast(book_ref as varchar) as book_ref,
        cast(book_date as timestamp) as book_date,
        cast(total_amount as decimal(18,2)) as total_amount,
        cast(book_date_key as integer) as book_date_key,
        trim(cast(book_day_name as varchar)) as book_day_name,
        cast(book_is_weekend as boolean) as book_is_weekend,
        trim(cast(book_day_type as varchar)) as book_day_type
    from source

)

select *
from cleaned