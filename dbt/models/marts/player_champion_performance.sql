with calculations as (

    select
        m.puuid,
        m.champion_key,
        m.queue_id,

        round(
            avg((m.kills + m.assists) / nullif(m.deaths, 0)),
            2
        ) as kda,

        round(
            avg(
                m.minion_kills /
                (m.game_duration_seconds / 60.0)
            ),
            2
        ) as lane_cs_per_min,

        round(
            avg(
                (m.ally_jungle_kills + m.enemy_jungle_kills) /
                (m.game_duration_seconds / 60.0)
            ),
            2
        ) as jungle_cs_per_min,

        round(avg(m.dpm), 2) as avg_dpm,

        round(
            avg(m.team_damage_percent) * 100,
            2
        ) as avg_team_damage_percent,

        round(
            avg(case when m.win then 1 else 0 end) * 100,
            2
        ) as win_rate,

        count(*) as games_played

    from {{ ref('fct_player_matches') }} m

    group by
        m.puuid,
        m.champion_key,
        m.queue_id
)

select
    c.puuid,

    p.game_name,
    p.tag_line,

    ch.champion_name,

    c.queue_id,
    q.queue_name,

    c.kda,
    c.lane_cs_per_min,
    c.jungle_cs_per_min,
    c.avg_dpm,
    c.avg_team_damage_percent,
    c.win_rate,
    c.games_played

from calculations c

left join {{ ref('dim_players') }} p
    on c.puuid = p.puuid

left join {{ ref('dim_champions') }} ch
    on c.champion_key = ch.champion_key

left join {{ ref('dim_queue_type') }} q
    on c.queue_id = q.queue_id