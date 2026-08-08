select
    -- match
    r.match_id,
    r.payload:info:gameDuration::number as game_duration_seconds,
    p.value:puuid::varchar as puuid,
    r.match_id || '-' || p.value:puuid::varchar as match_participant_key,
    r.payload:info:queueId::int as queue_id,
    to_timestamp(r.payload:info:gameStartTimestamp::number / 1000)
    as game_start_timestamp,
    to_timestamp(r.payload:info:gameEndTimestamp::number / 1000)
    as game_end_timestamp,
    -- player
    p.value:riotIdGameName::varchar as game_name,
    p.value:riotIdTagline::varchar as tag_line,
    p.value:championName::varchar as champion_name,
    p.value:lane::varchar as lane,
    --combat
    p.value:kills::int as kills,
    p.value:deaths::int as deaths,
    p.value:assists::int as assists,
    --farming
    p.value:totalMinionsKilled::int as minion_kills,
    p.value:totalEnemyJungleMinionsKilled::int as enemy_jungle_kills,
    p.value:totalAllyJungleMinionsKilled::int as ally_jungle_kills,
    p.value:goldEarned::int as gold_earned,
    p.value:win::boolean as win
from {{ source('raw', 'riot_matches') }} r,
lateral flatten(
    input => r.payload:info:participants
) p