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
        trim(cast(timezone as varchar)) as timezone,
        trim(cast(country as varchar)) as country,
        trim(cast(analysis_region as varchar)) as analysis_region
    from source

)

select *
from cleaned