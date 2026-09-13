with source as (

    select *
    from {{ ref('stg_airports') }}

),

final as (

    select
        row_number() over (order by airport_code) as airport_key,
        airport_code,
        airport_name,
        city,
        coordinates,
        timezone
    from source

)

select *
from final