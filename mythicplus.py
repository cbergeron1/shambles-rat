import requests

# Update the characters 
characters = ["Diodunce-Zul'Jin", "Bradskey-Tichondrius", "Ohmthatsme-Zul'Jin"]
region = "us"
slackers = []

REQUIRED_RUNS = 4
REQUIRED_LEVEL = 10
BASE_URL = "https://raider.io/api/v1/characters/profile"

def fetch_weekly_runs(name, realm):
    params = {
        "region": region,
        "realm": realm,
        "name": name,
        "fields": "mythic_plus_weekly_highest_level_runs"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("mythic_plus_weekly_highest_level_runs", [])
    except requests.RequestException as e:
        print(f"❌ Error fetching data for {name}-{realm}: {e}")
        return []

def check_character(character):
    if '-' not in character:
        print(f"⚠️ Invalid character format: {character}")
        return

    name, realm = character.split('-', 1)
    realm = realm.replace("'", "")  # Remove apostrophes (API prefers ZulJin over Zul'Jin)

    runs = fetch_weekly_runs(name, realm)
    qualifying_runs = [run for run in runs if run.get("mythic_level", 0) >= REQUIRED_LEVEL]

    if len(qualifying_runs) < REQUIRED_RUNS:
        slackers.append(f"{name}-{realm} ({len(qualifying_runs)} runs)")

def main():
    print("🔎 Checking M+ activity for guildies...\n")
    for character in characters:
        check_character(character)

    print("\n📋 Slackers (fewer than 4 M+10 runs this week):")
    if slackers:
        for s in slackers:
            print(f" - {s}")
    else:
        print(" ✅ Everyone pulled their weight. No slackers!")

if __name__ == "__main__":
    main()
