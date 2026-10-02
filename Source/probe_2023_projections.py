#!/usr/bin/env python3
"""
probe_2023_projections.py — four cheap experiments to find 2023 preseason projections.

WHY: ESPN's league endpoint returns 2023 projection rows that are HOLLOW. Confirmed three ways:
  * every player has exactly ONE 2023 projection row (699/700) -- no ambiguity, nothing missed
  * 435 of those rows contain only {"210": games_played}; 140 are empty; just 124 are real
  * it reproduces on an independent fetch (2023 as prior-year inside the 2024 run: 91 real)
  * 2022 -- an OLDER season -- fetches clean twice, so this is not age-related decay
  * --drop-filter (removing filterStatsForTopScoringPeriodIds) changed NOTHING: still 96 real

STRUCTURAL CLUE worth knowing: in the 2021 payload each player carries TWO src=1 rows --
split=0 (season total, e.g. Ekeler 226.9) and split=2 (per-game, 16.84). The 2023 payload has
NO split=2 rows at all and its split=0 rows are hollow. So 2023's projection data is shaped
differently, not merely filtered.

DECISIVE TEST for every probe below, all on one player:
    Christian McCaffrey, espn_id 3117251 -> does his 2023 src=1 row have MORE THAN ONE stat key?
    1 key  = still broken.   25+ keys = FIXED.

Run:  python probe_2023_projections.py
Paste the whole output back. Each probe is one request; the script never writes a data file.
"""
import json, sys
import requests

# ---- paste the same COOKIES dict the main puller uses -------------------------------------
COOKIES = {}          # <-- REQUIRED for the league-scoped probes (A, B, D). Probe C may work without.
LEAGUE_ID = 21985
TARGET_ID = 3117251   # Christian McCaffrey
HDR = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}


def verdict(payload, label, season=2023):
    """Find the target player anywhere in the payload and report his projection row."""
    players = payload.get("players") or payload if isinstance(payload, list) else payload.get("players", [])
    if isinstance(payload, list):
        players = payload
    found = None
    for entry in (players or []):
        p = entry.get("player") if isinstance(entry, dict) and "player" in entry else entry
        if isinstance(p, dict) and p.get("id") == TARGET_ID:
            found = p
            break
    if not found:
        print(f"  [{label}] target player not in payload (rows returned: {len(players or [])})")
        return
    proj = [s for s in found.get("stats", [])
            if s.get("seasonId") == season and s.get("statSourceId") == 1]
    if not proj:
        print(f"  [{label}] NO {season} projection row at all")
        return
    for s in proj:
        n = len(s.get("stats") or {})
        flag = "*** FIXED ***" if n > 1 else "still hollow"
        print(f"  [{label}] split={s.get('statSplitTypeId')} keys={n:3d} "
              f"applied={s.get('appliedTotal')}  -> {flag}")


def probe(label, url, headers=None, cookies=None):
    try:
        r = requests.get(url, headers={**HDR, **(headers or {})}, cookies=cookies, timeout=30)
        r.raise_for_status()
        verdict(r.json(), label)
    except Exception as e:
        print(f"  [{label}] request failed: {type(e).__name__}: {str(e)[:120]}")


BASE = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl"

print("PROBE A — generic season players endpoint, NO league scope (may not need cookies)")
probe("A players_wl", f"{BASE}/seasons/2023/players?scoringPeriodId=0&view=players_wl",
      headers={"x-fantasy-filter": json.dumps({"players": {"limit": 50,
               "filterIds": {"value": [TARGET_ID]}}})})

print("\nPROBE B — league endpoint, view=mDraftDetail instead of kona_player_info")
probe("B mDraftDetail", f"{BASE}/seasons/2023/segments/0/leagues/{LEAGUE_ID}?view=mDraftDetail",
      cookies=COOKIES)

print("\nPROBE C — single-player card, the most targeted view ESPN offers")
probe("C playercard", f"{BASE}/seasons/2023/segments/0/leagues/{LEAGUE_ID}?view=kona_playercard",
      headers={"x-fantasy-filter": json.dumps({"players": {"filterIds": {"value": [TARGET_ID]},
               "filterStatsForTopScoringPeriodIds": {"value": 0,
               "additionalValue": ["002023", "102023", "122023"]}}})},
      cookies=COOKIES)

print("\nPROBE D — ask for the split=2 (per-game) projection explicitly; 2021 has it, 2023 did not")
probe("D split2", f"{BASE}/seasons/2023/segments/0/leagues/{LEAGUE_ID}?view=kona_player_info",
      headers={"x-fantasy-filter": json.dumps({"players": {"limit": 50,
               "filterIds": {"value": [TARGET_ID]},
               "filterStatsForSplitTypeIds": {"value": [0, 2]}}})},
      cookies=COOKIES)

print("\nIf all four say 'still hollow', ESPN does not serve 2023 preseason projections and the")
print("matter is closed -- doc 41 and doc 43 already record that outcome. Do not spend more on it.")
