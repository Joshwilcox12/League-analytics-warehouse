from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import json


sample_dir = Path("data") / "samples" / "match_samples"
sample_dir.mkdir(parents=True, exist_ok=True)

game_name = "ohwillybilly"
game_tag = "NA1"

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

params = {
    "queue": 420,
    "start": 0,
    "count": 20
}

match_ids_response = requests.get(
    match_ids_url,
    headers=headers,
    params=params,
    timeout=30
)

match_ids_response.raise_for_status()

match_ids = match_ids_response.json()

print(f"Found account: {account_data['gameName']}#{account_data['tagLine']}")
print(f"Found {len(match_ids)} recent matches.")

for match_id in match_ids:
    
    match_details_url =(
        f"https://americas.api.riotgames.com"
        f"/lol/match/v5/matches/{match_id}"
 )
    match_response = requests.get(match_details_url,headers=headers)
    match_response.raise_for_status()
    player_match = match_response.json()

   
    print(f"Downloaded match: {match_id}")


    output_file = sample_dir / f"{match_id}.json"

    with output_file.open("w") as f:
        json.dump(player_match, f, indent=4)

    print(f"Saved to {output_file}")