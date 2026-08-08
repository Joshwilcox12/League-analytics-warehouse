select
    puuid,
    game_name,
    tag_line
from {{ ref('stg_match_participants') }}

qualify row_number() over (
    partition by puuid
    order by game_start_timestamp desc
) = 1