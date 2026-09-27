with flights as (

    select *
    from {{ ref('stg_flights') }}

),

final as (

    select
        row_number() over (
            order by f.flight_id
        ) as seat_utilization_key,

        f.flight_id,

        cast(
            replace(
                substr(cast(f.scheduled_departure as varchar), 1, 10),
                '-',
                ''
            )
            as integer
        ) as date_key,

        dep.airport_key as departure_airport_key,
        arr.airport_key as arrival_airport_key,

        ac.aircraft_key,

        f.seat_capacity,
        f.ticket_flight_count,
        f.boarded_count,

        greatest(
            f.seat_capacity - f.boarded_count,
            0
        ) as available_seats,

        greatest(
            f.ticket_flight_count - f.boarded_count,
            0
        ) as booked_not_boarded_count,

        f.ticketed_load_pct,
        f.boarded_load_pct,

        f.departure_daypart,
        f.departure_is_weekend

    from flights f

    left join {{ ref('dim_airport') }} dep
        on f.departure_airport = dep.airport_code

    left join {{ ref('dim_airport') }} arr
        on f.arrival_airport = arr.airport_code

    left join {{ ref('dim_aircraft') }} ac
        on f.aircraft_code = ac.aircraft_code

)

select *
from final