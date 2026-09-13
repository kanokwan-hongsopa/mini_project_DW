select
    s.status_name,
    sum(f.flight_count) as total_flights

from {{ ref('fact_flight_operations') }} f

join {{ ref('dim_flight_status') }} s
    on f.status_key = s.status_key

group by
    s.status_name

order by
    total_flights desc