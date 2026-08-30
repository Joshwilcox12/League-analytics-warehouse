from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import json
import time


sample_dir = Path("data") / "samples" / "match_samples"
sample_dir.mkdir(parents=True, exist_ok=True)


# Players we want match history for
players = [
    ("stonedfly", "1998"),
    ("masterspacewater", "NA1"),
    ("blackythunder", "NA1"),
    ("mood swings", "9236"),
    ("ohwillybilly", "NA1"),
    ("21 Drew", "TTV"),
]


load_dotenv(override=True)

api_key = os.getenv("RIOT_API_KEY")



if api_key is None:
    raise ValueError("RIOT_API_KEY was not found")
else:
    print("API key loaded successfully")


headers = {
    "X-Riot-Token": api_key
}


# Loop through each player
for game_name, game_tag in players:

    print(f"\nGetting matches for {game_name}#{game_tag}")

    # Get account information
    url = (
        f"https://americas.api.riotgames.com"
        f"/riot/account/v1/accounts/by-riot-id/{game_name}/{game_tag}"
    )

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    account_data = response.json()

    puuid = account_data["puuid"]

    print(
        f"Found account: "
        f"{account_data['gameName']}#{account_data['tagLine']}"
    )


    # Get ranked match IDs
    match_ids_url = (
        f"https://americas.api.riotgames.com"
        f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
    )

    params = {
        "queue": 420,
        "start": 0,
        "count": 100
    }

    match_ids_response = requests.get(
        match_ids_url,
        headers=headers,
        params=params,
        timeout=30
    )

    match_ids_response.raise_for_status()

    match_ids = match_ids_response.json()

    print(f"Found {len(match_ids)} recent ranked matches.")


    # Download each match
    for match_id in match_ids:

        output_file = sample_dir / f"{match_id}.json"


        # Don't download a match we already have
        if output_file.exists():
            print(f"Already have {match_id}, skipping...")
            continue


        match_details_url = (
            f"https://americas.api.riotgames.com"
            f"/lol/match/v5/matches/{match_id}"
        )

        match_response = requests.get(
            match_details_url,
            headers=headers,
            timeout=30
        )

        time.sleep(1.3)

        match_response.raise_for_status()

        player_match = match_response.json()

        print(f"Downloaded match: {match_id}")


        with output_file.open("w") as f:
            json.dump(player_match, f, indent=4)

        print(f"Saved to {output_file}")