with flights as (

    select *
    from {{ ref('stg_flights') }}

),

final as (

    select
        row_number() over (
            order by f.flight_id
        ) as flight_operations_key,

        f.flight_id,
        f.flight_no,

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
        fs.status_key,

        f.scheduled_departure,
        f.scheduled_arrival,
        f.actual_departure,
        f.actual_arrival,

        f.scheduled_departure_local,
        f.scheduled_arrival_local,
        f.departure_local_hour,
        f.departure_daypart,
        f.departure_is_weekend,

        f.scheduled_duration_minutes,
        f.actual_duration_minutes,

        f.departure_delay_minutes,
        f.arrival_delay_minutes,

        f.scheduled_duration_over_2h,
        f.departure_delay_over_2h,
        f.arrival_delay_over_2h,

        f.boarded_count,

        1 as flight_count

    from flights f

    left join {{ ref('dim_airport') }} dep
        on f.departure_airport = dep.airport_code

    left join {{ ref('dim_airport') }} arr
        on f.arrival_airport = arr.airport_code

    left join {{ ref('dim_aircraft') }} ac
        on f.aircraft_code = ac.aircraft_code

    left join {{ ref('dim_flight_status') }} fs
        on f.status = fs.status_name

)

select *
from final