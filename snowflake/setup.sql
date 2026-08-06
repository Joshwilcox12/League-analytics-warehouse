USE WAREHOUSE LEAGUE_WH;

CREATE DATABASE IF NOT EXISTS LEAGUE_ANALYTICS;
CREATE SCHEMA IF NOT EXISTS LEAGUE_ANALYTICS.RAW;
CREATE SCHEMA IF NOT EXISTS LEAGUE_ANALYTICS.ANALYTICS;

CREATE FILE FORMAT IF NOT EXISTS LEAGUE_ANALYTICS.RAW.RIOT_JSON_FORMAT
    TYPE = JSON;

CREATE STAGE IF NOT EXISTS LEAGUE_ANALYTICS.RAW.RIOT_STAGE
    FILE_FORMAT = LEAGUE_ANALYTICS.RAW.RIOT_JSON_FORMAT;

CREATE TABLE IF NOT EXISTS LEAGUE_ANALYTICS.RAW.RIOT_MATCHES (
    match_id VARCHAR,
    loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    payload VARIANT
);

-- copy data from stage to table --

COPY INTO LEAGUE_ANALYTICS.RAW.RIOT_MATCHES
    (match_id, payload)

FROM (
SELECT $1:metadata:matchId::VARCHAR,
$1
FROM @LEAGUE_ANALYTICS.RAW.RIOT_STAGE
);

-- load values to see if all is correct --
SELECT
    match_id,
    loaded_at,
    payload:metadata:matchId::VARCHAR AS match_id_from_payload,
    payload:info:gameDuration::INTEGER as game_duration_seconds
    from LEAGUE_ANALYTICS.RAW.RIOT_MATCHES;


    SELECT
    p.value:riotIdGameName::VARCHAR AS player_name,
    p.value:championName::VARCHAR AS champion_name,
    p.value:kills::INTEGER AS kills,
    p.value:deaths::INTEGER AS deaths,
    p.value:assists::INTEGER AS assists
FROM LEAGUE_ANALYTICS.RAW.RIOT_MATCHES r,
LATERAL FLATTEN(INPUT => r.payload:info:participants) p;