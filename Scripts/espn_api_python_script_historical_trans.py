from espn_api.football import League
import pandas as pd

# Set the season year once right here
SEASON_YEAR = 2023

# 1. Connect to the league
league = League(
    league_id=21985, 
    year=SEASON_YEAR, 
    espn_s2='', 
    swid='{A7217088-1F36-4F1F-AE73-67262BF763EF}'
)

# Create a lookup dictionary for team names
team_map = {team.team_id: team.team_name for team in league.teams}

# Helper to look up player names safely
def get_player_name(player_id):
    if hasattr(league, 'player_map') and player_id in league.player_map:
        player_data = league.player_map[player_id]
        if isinstance(player_data, str):
            return player_data
        elif hasattr(player_data, 'name'):
            return player_data.name
    return f"Player ID {player_id}"

transaction_list = []
print(f"Pulling {SEASON_YEAR} transactions week by week...")

# 2. Bypass the broken 'recent_activity' feed and hit the raw database for all 18 weeks
for week in range(1, 19):
    try:
        raw_data = league.espn_request.league_get(params={'view': 'mTransactions2', 'scoringPeriodId': week})
        
        # Skip if ESPN returns empty data for that week
        if not isinstance(raw_data, dict) or 'transactions' not in raw_data:
            continue
            
        for t in raw_data['transactions']:
            # Filter specifically for Waivers and Free Agent additions
            if t.get('type') in ['WAIVER', 'FREEAGENT']:
                team_id = t.get('teamId')
                
                # Format the Unix timestamp into a readable date
                date_ms = t.get('proposedDate', 0)
                date_str = pd.to_datetime(date_ms, unit='ms').strftime('%Y-%m-%d %H:%M')
                
                # Build a readable string of who was added/dropped
                actions = []
                for item in t.get('items', []):
                    p_name = get_player_name(item.get('playerId'))
                    actions.append(f"{item.get('type')} {p_name}")
                    
                transaction_list.append({
                    "Week": week,
                    "Date": date_str,
                    "Team": team_map.get(team_id, "Unknown Team"),
                    "Type": t.get('type'),
                    "Status": t.get('status'),
                    "Transaction": " | ".join(actions)
                })
    except Exception as e:
        print(f"Skipped week {week} due to error: {e}")

# 3. Export to CSV using an f-string to insert the year dynamically
df = pd.DataFrame(transaction_list)
df.to_csv(f"waiver_report_{SEASON_YEAR}.csv", index=False)
print(f"Export complete! Found {len(transaction_list)} transactions.")