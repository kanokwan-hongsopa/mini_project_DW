with source as (

    select *
    from {{ source('raw', 'aircrafts_data') }}

),

cleaned as (

    select
        upper(trim(cast(aircraft_code as varchar))) as aircraft_code,
        trim(cast(model as varchar)) as model,
        cast(range as integer) as range,
        trim(cast(manufacturer as varchar)) as manufacturer
    from source

)

select *
from cleaned