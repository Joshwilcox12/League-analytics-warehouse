from dotenv import load_dotenv
import os
import requests
import json
game_name = "stonedfly"
game_tag = "1998"

url=f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{game_tag}"


load_dotenv()

api_key = os.getenv("RIOT_API_KEY")

if api_key is None:
   raise ValueError("RIOT_API_KEY was not found")

else:
    print("API key loaded successfully")



headers = {
    "X-Riot-Token": api_key
}

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

account_data = response.json()

puuid = account_data["puuid"]

match_ids_url = (
    f"https://americas.api.riotgames.com"
    f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
)

match_ids_response = requests.get(match_ids_url, headers=headers)
match_ids_response.raise_for_status()

match_ids = match_ids_response.json()

match_id =match_ids[0]

match_details_url =(
    f"https://americas.api.riotgames.com"
       f"/lol/match/v5/matches/{match_id}"
)
match_response = requests.get(match_details_url,headers=headers)
match_response.raise_for_status()
player_match = match_response.json()

print(f"Found account: {account_data['gameName']}#{account_data['tagLine']}")
print(f"Found {len(match_ids)} recent matches.")
print(f"Downloaded match: {match_id}")
with open("match.json", "w") as f:
    json.dump(player_match, f, indent=4)