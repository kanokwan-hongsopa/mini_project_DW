with source as (

    select *
    from {{ source('raw', 'boarding_passes') }}

),

cleaned as (

    select
        cast(ticket_no as varchar) as ticket_no,
        cast(flight_id as integer) as flight_id,
        cast(boarding_no as integer) as boarding_no,
        upper(trim(cast(seat_no as varchar))) as seat_no,
        upper(trim(cast(departure_airport as varchar))) as departure_airport,
        upper(trim(cast(arrival_airport as varchar))) as arrival_airport,
        trim(cast(departure_region as varchar)) as departure_region,
        trim(cast(arrival_region as varchar)) as arrival_region,
        upper(trim(cast(aircraft_code as varchar))) as aircraft_code,
        trim(cast(aircraft_model as varchar)) as aircraft_model,
        trim(cast(manufacturer as varchar)) as manufacturer,
        cast(seat_capacity as integer) as seat_capacity
    from source

)

select *
from cleaned