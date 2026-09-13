with source as (

    select *
    from {{ source('raw', 'airports_data') }}

),

cleaned as (

    select
        upper(trim(cast(airport_code as varchar))) as airport_code,
        trim(cast(airport_name as varchar)) as airport_name,
        trim(cast(city as varchar)) as city,
        trim(cast(coordinates as varchar)) as coordinates,
        trim(cast(timezone as varchar)) as timezone
    from source

)

select *
from cleaned