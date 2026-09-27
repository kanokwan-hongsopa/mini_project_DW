with source as (

    select *
    from {{ source('raw', 'flights') }}

),

cleaned as (

    select
        cast(flight_id as integer) as flight_id,
        trim(cast(flight_no as varchar)) as flight_no,

        try_cast(scheduled_departure as timestamptz) as scheduled_departure,
        try_cast(scheduled_arrival as timestamptz) as scheduled_arrival,

        upper(trim(cast(departure_airport as varchar))) as departure_airport,
        upper(trim(cast(arrival_airport as varchar))) as arrival_airport,
        trim(cast(status as varchar)) as status,
        upper(trim(cast(aircraft_code as varchar))) as aircraft_code,

        try_cast(actual_departure as timestamptz) as actual_departure,
        try_cast(actual_arrival as timestamptz) as actual_arrival,

        trim(cast(departure_region as varchar)) as departure_region,
        trim(cast(arrival_region as varchar)) as arrival_region,
        trim(cast(aircraft_model as varchar)) as aircraft_model,
        trim(cast(manufacturer as varchar)) as manufacturer,

        try_cast(scheduled_duration_minutes as decimal(10,2)) as scheduled_duration_minutes,
        try_cast(actual_duration_minutes as decimal(10,2)) as actual_duration_minutes,
        try_cast(departure_delay_minutes as decimal(10,2)) as departure_delay_minutes,
        try_cast(arrival_delay_minutes as decimal(10,2)) as arrival_delay_minutes,

        try_cast(scheduled_duration_over_2h as boolean) as scheduled_duration_over_2h,
        try_cast(departure_delay_over_2h as boolean) as departure_delay_over_2h,
        try_cast(arrival_delay_over_2h as boolean) as arrival_delay_over_2h,

        try_cast(scheduled_departure_local as timestamp) as scheduled_departure_local,
        try_cast(scheduled_arrival_local as timestamp) as scheduled_arrival_local,
        try_cast(departure_local_hour as integer) as departure_local_hour,

        trim(cast(departure_daypart as varchar)) as departure_daypart,
        try_cast(departure_is_weekend as boolean) as departure_is_weekend,

        try_cast(seat_capacity as integer) as seat_capacity,
        try_cast(ticket_flight_count as integer) as ticket_flight_count,
        try_cast(boarded_count as integer) as boarded_count,
        try_cast(ticketed_load_pct as decimal(10,2)) as ticketed_load_pct,
        try_cast(boarded_load_pct as decimal(10,2)) as boarded_load_pct

    from source

)

select *
from cleaned