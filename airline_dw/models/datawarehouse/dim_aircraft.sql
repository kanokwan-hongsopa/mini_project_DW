with source as (

    select *
    from {{ ref('stg_aircrafts') }}

),

final as (

    select
        row_number() over (order by aircraft_code) as aircraft_key,
        aircraft_code,
        model,
        range
    from source

)

select *
from final