with source as (

    select distinct
        trim(status) as status
    from {{ ref('stg_flights') }}
    where status is not null

),

final as (

    select
        row_number() over (order by status) as status_key,
        status as status_name
    from source

)

select *
from final