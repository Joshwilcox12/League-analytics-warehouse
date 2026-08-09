WITH calculations AS(
select 
puuid,
champion_name,
queue_id,
round(avg((kills + assists) / nullif(deaths, 0)),2) as kda,
round(avg((minion_kills)
    / (game_duration_seconds / 60.0)),2) as lane_cs_per_min,
round(avg((ally_jungle_kills + enemy_jungle_kills)
    / (game_duration_seconds / 60.0)),2)as jungle_cs_per_min,
round(avg(dpm), 2) as avg_dpm,
round(avg(team_damage_percent) * 100, 2)
    as avg_team_damage_percent,
round(
    avg(case when win then 1 else 0 end) * 100,
    2
)  as win_rate,
count(*) as games_played

from {{ ref('fct_player_matches')}}

group by puuid, champion_name,queue_id
)

SELECT 
c.puuid,
c.champion_name,
c.queue_id,
case
    when c.queue_id = 420 then 'Ranked Solo/Duo'
    when c.queue_id = 440 then 'Ranked Flex'
    when c.queue_id = 400 then 'Normal Draft'
    when c.queue_id = 450 then 'ARAM'
    else 'Other'
end as queue_name,
c.kda,
c.lane_cs_per_min,
c.jungle_cs_per_min,
c.avg_dpm,
c.avg_team_damage_percent,
c.win_rate,
c.games_played,
p.game_name,
p.tag_line
FROM calculations c LEFT JOIN {{ref('dim_players')}} p ON c.puuid = p.puuid