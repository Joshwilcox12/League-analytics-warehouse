import requests
import json
import os
from dotenv import load_dotenv
import snowflake.connector
import time


load_dotenv()
#first connect to snowflake database raw table
try:
    cnx = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        authenticator="username_password_mfa",
        client_request_mfa_token=True
        )

except snowflake.connector.errors.DatabaseError as e:
    if e.errno == 394508:
        totp = input("Enter Snowflake MFA code: ")
        cnx = snowflake.connector.connect(
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA"),
                authenticator="username_password_mfa",
                passcode=totp,
                client_request_mfa_token=True
            )
        print("Connected")
    else:
        raise
print("Connected to Snowflake")












#get api key and set global variable

riot_api_key = os.getenv("RIOT_API_KEY")
headers = {"X-Riot-Token": riot_api_key}

#client game name/tag
player = [("stonedfly","1998"),
           ("masterspacewater","NA1"),
           ("blackythunder", "NA1"),
               ("mood swings", "9236"),
               ("ohwillybilly", "NA1"),
               ("21 Drew", "TTV"),
               ("kuronin", "NA1"),
               ("meeku", "zed"),
               ("PickleRichard","CLOWN"),
               ("Vintram", "Vinny")]








#first get unique id using player name/tag api

def get_puuid(player):
    
    all_puuid = []
    for game_name, tag_line in player:
        url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"

        response = requests.get(url,headers=headers,timeout=30)
        response.raise_for_status()
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
             "count":"100"  }

    for puuid in all_puuid:
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"

        response = requests.get(url,headers=headers,params=params,timeout=30)
        response.raise_for_status()

        match_id = response.json()
    
        all_match_id.update(match_id)
    
    print(f"found {len(all_match_id)} unique match id")
    return all_match_id

#now we need to send this list of match id to snowflake table and query which ids we already have and don't so we get new match data to download

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
    print(f"New matches to download: {len(rows)}")

    return rows







def download_unique_matches(match_ids):
    match_data = []
    for match in match_ids:
        match_id = match[0]
        url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}'
        response = requests.get(url,headers=headers,timeout=30)

        response.raise_for_status()
        values = (response.json(),match_id)
        match_data.append(values)
        time.sleep(1.3)
    return match_data










def upload_matches_to_snowflake(match_data):
     cursor = cnx.cursor()
    
     total_list = []       
     for i, (match, match_id) in enumerate(match_data,start =1):
                    print(f"uploading {match_id}, {i} out of  {len(match_data)}")
                    payload = json.dumps(match)
                    values = (match_id, payload)
                    total_list.append(values)
     
     cursor.execute("""
            CREATE TEMPORARY TABLE TEMP_RIOT_MATCHES (
                match_id VARCHAR,
                payload VARCHAR
            )
        """)

     cursor.executemany("""
            INSERT INTO TEMP_RIOT_MATCHES
                (match_id, payload)
            VALUES (%s, %s)
        """, total_list)

     cursor.execute("""
            INSERT INTO LEAGUE_ANALYTICS.RAW.RIOT_MATCHES
                (match_id, loaded_at, payload)
            SELECT
                match_id,
                CURRENT_TIMESTAMP(),
                PARSE_JSON(payload)
            FROM TEMP_RIOT_MATCHES
        """)

     cnx.commit()
     print(f"Uploaded {len(total_list)} matches.")              
   
upload_matches_to_snowflake(download_unique_matches(query_snowflake_unique_match_id(get_match_id(get_puuid(player)))))

