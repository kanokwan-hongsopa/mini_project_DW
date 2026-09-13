with source as (

    select *
    from {{ source('raw', 'flights') }}

),

cleaned as (

    select
        cast(flight_id as integer) as flight_id,

        trim(cast(flight_no as varchar)) as flight_no,

        cast(scheduled_departure as timestamptz)
            as scheduled_departure,

        cast(scheduled_arrival as timestamptz)
            as scheduled_arrival,

        upper(trim(cast(departure_airport as varchar)))
            as departure_airport,

        upper(trim(cast(arrival_airport as varchar)))
            as arrival_airport,

        trim(cast(status as varchar))
            as status,

        upper(trim(cast(aircraft_code as varchar)))
            as aircraft_code,

        case
            when actual_departure is null
              or trim(actual_departure) = ''
              or trim(actual_departure) = '\N'
            then null
            else cast(actual_departure as timestamptz)
        end as actual_departure,

        case
            when actual_arrival is null
              or trim(actual_arrival) = ''
              or trim(actual_arrival) = '\N'
            then null
            else cast(actual_arrival as timestamptz)
        end as actual_arrival

    from source

)

select *
from cleaned