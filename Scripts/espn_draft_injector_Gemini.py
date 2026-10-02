import pandas as pd
import requests
import sys

# 1. Configuration
# doc 60: this used to be a BARE FILENAME resolved against the working directory. Matt runs this
# from OneDrive\Fantasy\Scripts, so it read the copy sitting THERE -- which on Aug 28 was still
# the original broken file (kickers at rank 481, D/ST at 507; 473 of 544 rows differed from the
# corrected one). Every prerank fix made on Aug 27 would never have reached ESPN.
# ONE canonical file now, addressed absolutely. Run this script from anywhere.
CSV_FILENAME = r"G:\My Drive\_Fantasy\2026\Scripts\live_draft\ESPN_prerank_with_ids.csv"
LEAGUE_ID = 21985
TEAM_ID = 9
SEASON = 2026

# The exact endpoint extracted from your cURL
URL = f"https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}/teams/{TEAM_ID}?platformVersion=5e254affd13eaa961c7dffbd9de59d867a2e0acf"

COOKIES = {
    'swid': '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': ''
}

HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'x-fantasy-platform': 'espn-fantasy-web',
    'x-fantasy-source': 'kona',
    'origin': 'https://fantasy.espn.com',
    'referer': 'https://fantasy.espn.com/'
}

# 2. Load and Validate the Data
print(f"Reading player IDs from {CSV_FILENAME}...")
try:
    df = pd.read_csv(CSV_FILENAME)
    
    # Safeguard 1: Validate column structure
    if "ESPN_ID" not in df.columns:
        sys.exit("Error: Could not find a column named 'ESPN_ID' in your CSV. Please check the header.")
        
    initial_count = len(df)
    
    # Drop blanks and force into clean integers
    ids = df["ESPN_ID"].dropna().astype(int).tolist()
    
    # Safeguard 2: Check for dropped rows
    if len(ids) != initial_count:
        print(f"Warning: {initial_count - len(ids)} rows were blank and dropped.")
        
    # Safeguard 3: Check for duplicate IDs (Crucial: ESPN will silently reject or scramble duplicates)
    if len(ids) != len(set(ids)):
        sys.exit("Error: Duplicate ESPN_IDs found in your CSV. You must remove duplicate players before injecting.")

    # Convert to the specific dictionary format ESPN expects
    draft_list = [{"playerId": pid} for pid in ids]

    payload = {
        "draftStrategy": {
            "draftList": draft_list,
            "excludedPlayerIds": [] 
        }
    }

    # 3. Push to ESPN Servers
    print(f"Injecting {len(draft_list)} players into the draft room...")
    response = requests.post(URL, headers=HEADERS, cookies=COOKIES, json=payload,
                             timeout=20)          # doc 59: no timeout -> a hung socket at 7:05pm
                                                  # is indistinguishable from success-in-progress

    if response.status_code in [200, 201, 204]:
        # doc 59: a 200 is NOT verification. Read the list back and count what ESPN actually kept.
        print(f"POST accepted ({response.status_code}). Verifying...")
        # doc 89: the old read-back looked for back["draftStrategy"]["draftList"] at the TOP
        # LEVEL of a /teams/{id} response. ESPN's v3 API returns the LEAGUE object with a
        # `teams` array even when a team id is in the path, so that lookup found nothing and
        # printed "0 players stored" whether or not the write worked. A verifier that reports
        # failure on a success is as bad as one reporting success on a failure.
        # Now: try several views, and search each response RECURSIVELY for the key.
        def find_draft_list(obj, depth=0):
            """Return (list, path) for the first non-trivial draftStrategy.draftList found."""
            if depth > 6: return None, None
            if isinstance(obj, dict):
                ds = obj.get("draftStrategy")
                if isinstance(ds, dict) and isinstance(ds.get("draftList"), list):
                    return ds["draftList"], "draftStrategy.draftList"
                for k, v in obj.items():
                    got, path = find_draft_list(v, depth + 1)
                    if got is not None: return got, str(k) + "." + str(path)
            elif isinstance(obj, list):
                for i, v in enumerate(obj[:40]):
                    got, path = find_draft_list(v, depth + 1)
                    if got is not None: return got, "[" + str(i) + "]." + str(path)
            return None, None

        BASE_R = ("https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/"
                  f"{SEASON}/segments/0/leagues/{LEAGUE_ID}")
        CANDIDATES = [
            (f"{BASE_R}/teams/{TEAM_ID}?view=mDraftDetail", "teams/ID mDraftDetail"),
            (f"{BASE_R}/teams/{TEAM_ID}?view=mTeam",        "teams/ID mTeam"),
            (f"{BASE_R}?view=mDraftDetail",                 "league mDraftDetail"),
            (f"{BASE_R}?view=mTeam",                        "league mTeam"),
        ]
        stored, where, shapes = None, None, []
        for url, label in CANDIDATES:
            try:
                back = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=20).json()
            except Exception as e:
                shapes.append("    " + label + ": request failed - " + str(e)); continue
            if isinstance(back, list): back = back[0] if back else {}
            got, path = find_draft_list(back)
            keys = ",".join(sorted(back.keys())[:8]) if isinstance(back, dict) else type(back).__name__
            if got:
                stored, where = got, label + " -> " + str(path); break
            shapes.append("    " + label + ": no non-empty draftList. top-level keys: " + keys)

        if stored is None:
            print("  !! COULD NOT VERIFY - no view returned a stored draft list.")
            for line in shapes: print(line)
            print("  This does NOT mean the write failed. The POST returned "
                  + str(response.status_code) + ".")
            print("  SETTLE IT BY EYE, it takes 20 seconds:")
            print("     ESPN -> your league -> Draft -> Pre-Draft Rankings")
            print("     #1 should be the first row of the CSV (id " + str(ids[0]) + "), defenses")
            print("     should appear in the list, and the list should end with a kicker.")
        else:
            n = len(stored)
            print("  ESPN reports " + str(n) + " players stored (sent "
                  + str(len(draft_list)) + ")   [" + where + "]")
            if n != len(draft_list):
                print("  !! MISMATCH - ESPN did not keep the whole list. Most likely causes:")
                print("     truncation (the tail goes first), or rejected D/ST ids (negative).")
                print("     " + str(len(draft_list) - n) + " missing. 32 missing = the defenses.")
            else:
                first = stored[0] if isinstance(stored[0], int) else stored[0].get("playerId")
                print("  count matches. first stored id = " + str(first)
                      + " (expect " + str(ids[0]) + ").")
        print("Pre-draft rankings updated.")
    else:
        print(f"Update Failed. Status Code: {response.status_code}")
        print(response.text)

except FileNotFoundError:
    print(f"Error: Could not find '{CSV_FILENAME}'. This is an ABSOLUTE path set at the top of this file - it does NOT depend on the working directory.")