select 
    s.match_id,

    c.champion_key,
    p.puuid,
    q.queue_id ,
    d.date_key,

    s.match_participant_key,

    s.game_start_timestamp,
    s.game_end_timestamp,
    s.game_duration_seconds,

    s.lane,

    s.kills,
    s.deaths,
    s.assists,
    s.dpm,
    s.team_damage_percent,

    s.minion_kills,
    s.enemy_jungle_kills,
    s.ally_jungle_kills,
    s.gold_earned,

    s.win

from {{ ref('stg_match_participants') }} s

left join {{ ref('dim_champions') }} c
    on s.champion_name = c.champion_name

left join {{ ref('dim_players') }} p
    on s.puuid = p.puuid

left join {{ ref('dim_queue_type') }} q
    on s.queue_id = q.queue_id

left join {{ ref('dim_date') }} d
    on to_number(to_char(s.game_start_timestamp, 'YYYYMMDD')) = d.date_key