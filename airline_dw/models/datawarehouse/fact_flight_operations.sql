with flights as (

    select *
    from {{ ref('stg_flights') }}

),

final as (

    select
        row_number() over (order by f.flight_id) as flight_operations_key,

        f.flight_id,
        f.flight_no,

        cast(
            strftime(cast(f.scheduled_departure as date), '%Y%m%d')
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

        case
            when f.actual_departure is not null then
                date_diff(
                    'minute',
                    f.scheduled_departure,
                    f.actual_departure
                )
            else null
        end as departure_delay_minutes,

        case
            when f.actual_arrival is not null then
                date_diff(
                    'minute',
                    f.scheduled_arrival,
                    f.actual_arrival
                )
            else null
        end as arrival_delay_minutes,

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