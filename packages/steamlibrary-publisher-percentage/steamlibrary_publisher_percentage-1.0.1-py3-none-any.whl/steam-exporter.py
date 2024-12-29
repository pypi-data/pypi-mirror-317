import requests
import csv
import time
from collections import Counter
import os

# Fetch the API key and Steam ID from environment variables (set by GitHub Secrets)
API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

# Validate if the environment variables are loaded correctly
if not API_KEY or not STEAM_ID:
    raise ValueError("STEAM_API_KEY and STEAM_ID must be set in the environment.")

# Fetch owned games with metadata
def fetch_owned_games(api_key, steam_id):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("response", {}).get("games", [])

# Fetch app details from Steam Store API (to get publisher info)
def fetch_app_details(app_id):
    url = f"https://store.steampowered.com/api/appdetails/"
    params = {"appids": app_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json().get(str(app_id), {}).get("data", {})
    return data.get("publishers", ["Unknown"])[0] if data else "Unknown"

def main(api_key, steam_id):
    print("Fetching Steam library...")
    games = fetch_owned_games(api_key, steam_id)

    if not games:
        print("No games found in your Steam library.")
        return

    print(f"Found {len(games)} games. Fetching publisher data...")
    publishers = []
    for game in games:
        app_id = game["appid"]
        name = game["name"]
        print(f"Fetching data for: {name} (AppID: {app_id})")
        try:
            publisher = fetch_app_details(app_id)
            publishers.append(publisher)
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching data for {name} (AppID: {app_id}): {e}")
            publishers.append("Unknown")
        
        # Add a delay to avoid rate limits
        time.sleep(2)  # Adjust the delay as needed (1 second is usually sufficient)

    # Calculate percentages
    total_games = len(publishers)
    publisher_counts = Counter(publishers)
    print("\nPublisher Percentages:")
    for publisher, count in publisher_counts.most_common():
        percentage = (count / total_games) * 100
        print(f"{publisher}: {percentage:.2f}% ({count} games)")

    # Save results to CSV
    with open("steam_library_publishers.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Publisher", "Game Count", "Percentage"])
        for publisher, count in publisher_counts.items():
            percentage = (count / total_games) * 100
            writer.writerow([publisher, count, f"{percentage:.2f}%"])

    print("\nResults saved to 'steam_library_publishers.csv'")

# Run the script
if __name__ == "__main__":
    main(API_KEY, STEAM_ID)
