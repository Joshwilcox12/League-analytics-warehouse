from dotenv import load_dotenv
import requests
import json
import time
import os
import snowflake.connector

# Players we want match history for
players = [
    ("stonedfly", "1998"),
    ("masterspacewater", "NA1"),
    ("blackythunder", "NA1"),
    ("mood swings", "9236"),
    ("ohwillybilly", "NA1"),
    ("21 Drew", "TTV"),
]


# Load the API key from the .env file
load_dotenv(override=True)

api_key = os.getenv("RIOT_API_KEY")

if api_key is None:
    raise ValueError("RIOT_API_KEY was not found")
else:
    print("API key loaded successfully")


#store as a set so we don't get duplicate match ids
total_match_ids = set()
#loop start
for game_name, tag_line in players:
   
    print(f"\nGetting matches for {game_name}#{tag_line}")
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"

    headers = {
        "X-Riot-Token": api_key
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()


    account_data = response.json()
    puuid = account_data["puuid"]

    #now get match ids of each player
    match_ids_url = (
            f"https://americas.api.riotgames.com"
            f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        )

    #only look up ranked games, last 100 
    params = {
        "queue": "420",  # Ranked Solo/Duo queue
        "start": 0,
        "count": 100  # Number of matches to retrieve
    }

    match_id_response = requests.get(match_ids_url, headers=headers, params=params, timeout=30)
    match_id_response.raise_for_status()

    total_match_ids.update(match_id_response.json())

    time.sleep(1.3)

print(f"Total match IDs collected: {len(total_match_ids)}")




#send match id to snowflake to run query to return ids that are not in snowflake
print("Connecting to Snowflake and checking for match IDs not in the database...")
candidate_match_id = total_match_ids

num_match_ids = len(candidate_match_id)

temp_sql_string = ",".join(["(%s)"] * num_match_ids)

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

cursor = cnx.cursor()

query = f"""
    SELECT candidate_match_id
    FROM (values {temp_sql_string}) AS candidate(candidate_match_id)
    WHERE candidate_match_id NOT IN (
    select match_id FROM LEAGUE_ANALYTICS.RAW.RIOT_MATCHES)
   """
cursor.execute(query,tuple(candidate_match_id))
   


rows= cursor.fetchall()
print(f"Number of match IDs in Snowflake: {num_match_ids - len(rows)}")
print(f"Number of match IDs not in Snowflake: {len(rows)}")

if len(rows) == 0:
    print("No new match IDs to download. Exiting.")
    cursor.close()
    cnx.close()
    exit(0)
else:
    print("New match IDs found. Proceeding to download match info and store in Snowflake.")

    ids_to_download = [row[0] for row in rows]

    matches_to_insert =[]
    #down load match info and store in snowflake
    for match_id in ids_to_download:
        print(f"Downloading match info for match ID: {match_id}")
        match_info_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
        match_response = requests.get(match_info_url, headers=headers, timeout=30)
        match_response.raise_for_status()
        payload = match_response.json()
        matches_to_insert.append((match_id, json.dumps(payload)))

    

        time.sleep(1.3)  # To respect rate limits

    # Insert the match data into Snowflake

    insert_query = """
    INSERT INTO LEAGUE_ANALYTICS.RAW.RIOT_MATCHES
        (match_id, loaded_at, payload)
    SELECT %s, CURRENT_TIMESTAMP(), PARSE_JSON(%s)
    """

    cursor.executemany(
        insert_query,
        matches_to_insert
    )



#run dbt models





