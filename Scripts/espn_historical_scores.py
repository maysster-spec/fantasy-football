import requests
import pandas as pd

# 1. Configuration
LEAGUE_ID = 21985
SEASONS = [2021]
## SEASONS = [2022, 2023, 2024, 2025]

cookies = {
    'swid': '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': ''
}

scoreboard_data = []

# 2. Iterate through each historical season
for year in SEASONS:
    print(f"Fetching {year} scores...")
    
    # The historical endpoint requires a specific seasonId query parameter
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/leagueHistory/{LEAGUE_ID}?seasonId={year}&view=mMatchup&view=mTeam"
    
    response = requests.get(url, cookies=cookies)
    
    try:
        # leagueHistory payloads are wrapped in an array, so we grab the first index
        data = response.json()[0] 
    except (IndexError, ValueError):
        print(f"  -> Could not load data for {year}. Skipping.")
        continue
        
    # 3. Build a Team ID to Team Name lookup dictionary for this specific year
    team_map = {}
    for team in data.get('teams', []):
        team_id = team.get('id')
        location = team.get('location', '')
        nickname = team.get('nickname', '')
        # ESPN sometimes splits the name, so we join location and nickname
        name = team.get('name', f"{location} {nickname}").strip()
        team_map[team_id] = name
        
    # 4. Extract all Matchups for the year
    for match in data.get('schedule', []):
        week = match.get('matchupPeriodId')
        
        home = match.get('home', {})
        away = match.get('away', {})
        
        # Skip if there is no home team (usually means an empty placeholder slot)
        if not home:
            continue
            
        home_team_id = home.get('teamId')
        home_score = home.get('totalPoints', 0)
        
        # Away can be empty during playoff byes
        away_team_id = away.get('teamId') if away else None
        away_score = away.get('totalPoints', 0) if away else 0
        
        scoreboard_data.append({
            "Season": year,
            "Week": week,
            "Home Team": team_map.get(home_team_id, "Unknown"),
            "Home Score": home_score,
            "Away Team": team_map.get(away_team_id, "Playoff Bye / None"),
            "Away Score": away_score,
            "Winner": match.get('winner', 'UNDECIDED'),
            "Bracket Type": match.get('playoffTierType', 'NONE') # Flags 'WINNERS_BRACKET' vs 'NONE' (Regular Season)
        })

# 5. Export directly to an Excel-ready CSV
df = pd.DataFrame(scoreboard_data)
output_filename = "historical_draft_results_2021.csv"
## output_filename = "historical_scoreboard_2022_2025.csv"
df.to_csv(output_filename, index=False)
print(f"Success! Exported {len(scoreboard_data)} historical matchups to {output_filename}.")