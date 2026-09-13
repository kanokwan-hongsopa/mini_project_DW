with ticket_flights as (

    select *
    from {{ ref('stg_ticket_flights') }}

),

flights as (

    select *
    from {{ ref('stg_flights') }}

),

joined as (

    select
        tf.ticket_no,
        tf.flight_id,

        cast(strftime(cast(f.scheduled_departure as date), '%Y%m%d') as integer)
            as date_key,

        da_departure.airport_key as departure_airport_key,
        da_arrival.airport_key as arrival_airport_key,

        dac.aircraft_key,
        dfc.fare_class_key,

        tf.amount,

        1 as ticket_flight_count

    from ticket_flights tf

    inner join flights f
        on tf.flight_id = f.flight_id

    left join {{ ref('dim_airport') }} da_departure
        on f.departure_airport = da_departure.airport_code

    left join {{ ref('dim_airport') }} da_arrival
        on f.arrival_airport = da_arrival.airport_code

    left join {{ ref('dim_aircraft') }} dac
        on f.aircraft_code = dac.aircraft_code

    left join {{ ref('dim_fare_class') }} dfc
        on tf.fare_conditions = dfc.fare_class

),

final as (

    select
        row_number() over (
            order by ticket_no, flight_id
        ) as ticket_sales_key,

        ticket_no,
        flight_id,
        date_key,
        departure_airport_key,
        arrival_airport_key,
        aircraft_key,
        fare_class_key,

        amount,
        ticket_flight_count

    from joined

)

select *
from final