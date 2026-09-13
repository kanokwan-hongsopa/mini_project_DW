with all_dates as (

    select cast(book_date as date) as full_date
    from {{ ref('stg_bookings') }}

    union

    select cast(scheduled_departure as date)
    from {{ ref('stg_flights') }}

    union

    select cast(scheduled_arrival as date)
    from {{ ref('stg_flights') }}

    union

    select cast(actual_departure as date)
    from {{ ref('stg_flights') }}
    where actual_departure is not null

    union

    select cast(actual_arrival as date)
    from {{ ref('stg_flights') }}
    where actual_arrival is not null

),

unique_dates as (

    select distinct full_date
    from all_dates
    where full_date is not null

),

final as (

    select
        cast(strftime(full_date, '%Y%m%d') as integer) as date_key,
        full_date,
        day(full_date) as day,
        dayname(full_date) as day_name,
        week(full_date) as week,
        month(full_date) as month,
        monthname(full_date) as month_name,
        quarter(full_date) as quarter,
        year(full_date) as year
    from unique_dates

)

select *
from final
order by full_date