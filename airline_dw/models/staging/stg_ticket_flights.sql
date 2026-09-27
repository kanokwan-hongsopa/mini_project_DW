with source as (

    select *
    from {{ source('raw', 'ticket_flights') }}

),

cleaned as (

    select
        cast(ticket_no as varchar) as ticket_no,
        cast(flight_id as integer) as flight_id,
        trim(cast(fare_conditions as varchar)) as fare_conditions,
        cast(amount as decimal(18,2)) as amount,
        cast(book_ref as varchar) as book_ref,
        cast(book_date as timestamp) as book_date,
        cast(flight_date as date) as flight_date,
        cast(booking_lead_days as decimal(10,2)) as booking_lead_days,
        trim(cast(departure_airport as varchar)) as departure_airport,
        trim(cast(arrival_airport as varchar)) as arrival_airport,
        trim(cast(departure_region as varchar)) as departure_region,
        trim(cast(arrival_region as varchar)) as arrival_region,
        trim(cast(aircraft_code as varchar)) as aircraft_code,
        trim(cast(aircraft_model as varchar)) as aircraft_model,
        trim(cast(manufacturer as varchar)) as manufacturer,
        cast(scheduled_duration_minutes as decimal(10,2)) as scheduled_duration_minutes
    from source

)

select *
from cleaned