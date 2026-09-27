with all_dates as (

    select
        cast(book_date as date) as full_date
    from {{ ref('stg_bookings') }}

    union

    select
        cast(
            substr(cast(scheduled_departure as varchar), 1, 10)
            as date
        ) as full_date
    from {{ ref('stg_flights') }}

    union

    select
        cast(
            substr(cast(scheduled_arrival as varchar), 1, 10)
            as date
        ) as full_date
    from {{ ref('stg_flights') }}

    union

    select
        cast(
            substr(cast(actual_departure as varchar), 1, 10)
            as date
        ) as full_date
    from {{ ref('stg_flights') }}
    where actual_departure is not null

    union

    select
        cast(
            substr(cast(actual_arrival as varchar), 1, 10)
            as date
        ) as full_date
    from {{ ref('stg_flights') }}
    where actual_arrival is not null

),

unique_dates as (

    select distinct
        full_date
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
        year(full_date) as year,

        case
            when dayofweek(full_date) in (0, 6) then true
            else false
        end as is_weekend,

        case
            when dayofweek(full_date) in (0, 6) then 'Weekend'
            else 'Weekday'
        end as day_type

    from unique_dates

)

select *
from final
order by full_date