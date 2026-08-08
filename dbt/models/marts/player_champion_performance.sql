WITH calculations AS(
select 
puuid,
champion_name,
round(avg((kills + assists) / nullif(deaths, 0)),2) as kda,
round(avg((minion_kills)
    / (game_duration_seconds / 60.0)),2) as lane_cs_per_min,
round(avg((ally_jungle_kills + enemy_jungle_kills)
    / (game_duration_seconds / 60.0)),2)as jungle_cs_per_min,
round(avg(case when win then 1 else 0 end),1) as win_rate,
count(*) as games_played

from {{ ref('fct_player_matches')}}

group by puuid, champion_name
)

SELECT c.*,
p.game_name,
p.tag_line
FROM calculations c LEFT JOIN {{ref('dim_players')}} p ON c.puuid = p.puuid