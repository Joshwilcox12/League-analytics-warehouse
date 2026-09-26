import requests
import json
import os
from dotenv import load_dotenv
import snowflake.connector


#get .env variables and set global variable
load_dotenv()

#first connect to snowflake database raw table

# totp = input("Enter Snowflake MFA code: ")
cnx = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    authenticator="username_password_mfa",
    #  passcode=totp
    client_request_mfa_token=True
)


#get api key and set global variable
load_dotenv()
riot_api_key = os.getenv("RIOT_API_KEY")
headers = {"X-Riot-Token": riot_api_key}

#client game name/tag
player = [("stonedfly","1998"),
          ("masterspacewater","NA1")]

#first get unique id using player name/tag api

def get_puuid(player):
    
    all_puuid = []
    for game_name, tag_line in player:
        print(f"Getting {game_name} puuid")
        url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"

        response = requests.get(url,headers=headers,timeout=30)
        
        puuid = response.json()["puuid"]
        all_puuid.append(puuid)
    print(f"Found {len(all_puuid)}")     
    return all_puuid


#now we need to look up the last 100 match id of each player

def get_match_id(all_puuid):
    print(f"Grabbing unique match id from all players")
    all_match_id = set()
    params ={"queue":"420",
             "start":"0",
             "count":"2"  }

    for puuid in all_puuid:
        print(f"number {puuid} match id")
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"

        response = requests.get(url,headers=headers,params=params,timeout=30)
        

        match_id = response.json()
    
        all_match_id.update(match_id)
    
    print(f"found {len(all_match_id)} unique match id")
    return all_match_id

#now we need to send this list of match id to snowflake table and query which ids we already ahve and don't so we get new match data to download

#first connect to snowflake

def query_snowflake_unique_match_id(all_match_id):
    
    cursor = cnx.cursor()
    total_match_id = len(all_match_id)
    temp_sql_string = ",".join(["(%s)"] * total_match_id)
    query = f"""
            select all_match_id FROM (VALUES{temp_sql_string}) as client_id(all_match_id)
            where all_match_id NOT IN (select match_id from riot_matches)

    """
    cursor.execute(query,tuple(all_match_id))
    rows = cursor.fetchall()
    print(rows)
    print(type(rows))
get_puuid(player)

        
query_snowflake_unique_match_id(get_match_id(get_puuid(player)))