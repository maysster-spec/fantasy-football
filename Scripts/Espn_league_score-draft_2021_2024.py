from espn_api.football import League
import pandas as pd

# 1. Configuration
LEAGUE_ID = 21985
SEASONS = [2022]
## SEASONS = [2022, 2023, 2024, 2025]
ESPN_S2 = ''
SWID = '{A7217088-1F36-4F1F-AE73-67262BF763EF}'

draft_data = []

# 2. Pull Draft Results
for year in SEASONS:
    print(f"Fetching {year} draft...")
    try:
        # Initialize league for the specific year
        league = League(league_id=LEAGUE_ID, year=year, espn_s2=ESPN_S2, swid=SWID)
        
        # Extract each pick and use enumerate to generate the overall pick number
        for overall_pick, pick in enumerate(league.draft, start=1):
            
            # Safely extract team name and keeper status in case the API structure shifts
            team_name = pick.team.team_name if hasattr(pick.team, 'team_name') else "Unknown Team"
            is_keeper = getattr(pick, 'keeper_status', False)
            
            draft_data.append({
                "Season": year,
                "Round": pick.round_num,
                "Round Pick": pick.round_pick,
                "Overall Pick": overall_pick,
                "Team": team_name,
                "Player": pick.playerName,
                "Keeper Status": is_keeper
            })
    except Exception as e:
        print(f"  -> Could not load draft data for {year}. Error: {e}")

# 3. Export
df = pd.DataFrame(draft_data)
output_filename = "historical_draft_results_2021.csv"
df.to_csv(output_filename, index=False)
print(f"Success! Exported {len(draft_data)} draft picks to {output_filename}.")