select distinct
    {{ dbt_utils.generate_surrogate_key(['champion_name']) }} as champion_key,
    champion_name

from {{ ref('stg_match_participants') }}