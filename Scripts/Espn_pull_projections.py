r"""
ESPN league projection puller — E-Discovery Keeper League (21985).

Consolidated Multi-Season Batch Runner:
- Outputs directly to: C:\Users\wmatt\OneDrive\Fantasy\Scripts
- Automatically fetches prior season in background to populate historical columns.
- Uses `is_empty_stat` to preserve K/DST rows while filtering stat 210 metadata stubs.
- Non-blocking anomaly reporting to ensure CSV export always executes.
"""

import argparse, json, sys, time, datetime as dt
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

LEAGUE_ID = 21985
DRAFT_SEASON    = 2026
DEFAULT_SEASONS = [DRAFT_SEASON]   # was [2022, 2023, 2024] -- the historical backtest set.
# Changed 2026-08-28: running this bare produced espn_projections_2024_*.csv with no
# proj_2026 column and a post-season espn_adp (the 1.1 contaminated field). Historical
# seasons are still available, but now only on purpose -- see confirm_seasons() below.
LIMIT = 700

# ------------------------------------------------------------------ Authentication --
COOKIES = {
    'swid': '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': ''
}

# ------------------------------------------------------------------ Output Paths --
# 2026-08-28: was hardcoded to C:\Users\wmatt\OneDrive\Fantasy\Scripts, which is now retired.
# Data lands in Source\ beside every prior pull; Scripts\ holds code only.
DATA_DIR = Path(r"G:\My Drive\_Fantasy\2026\Source")
OUT_CANDIDATES = [DATA_DIR, HERE.parent / "Source", HERE, Path.cwd()]

KNOWN_NAME = "ESPN_projections_in_my_League.csv"
KNOWN_CANDIDATES = [
    DATA_DIR / KNOWN_NAME,
    (HERE.parent / "Source") / KNOWN_NAME,
    HERE / KNOWN_NAME,
    Path.cwd() / KNOWN_NAME,
]

def _writable(c, create=False):
    try:
        if create:
            c.mkdir(parents=True, exist_ok=True)
        elif not c.is_dir():
            return False
        probe = c / ".write_probe.tmp"
        probe.write_text("x", encoding="utf-8")
        probe.unlink()
        return True
    except Exception:
        return False

def resolve_outdir(explicit=None):
    if explicit and _writable(Path(explicit), create=True):
        return Path(explicit)
    for c in OUT_CANDIDATES:
        if _writable(c):
            return c
    return HERE

POS_MAP = {1: "QB", 2: "RB", 3: "WR", 4: "TE", 5: "K", 16: "D/ST"}
TEAM_MAP = {
    0: "FA", 1: "ATL", 2: "BUF", 3: "CHI", 4: "CIN", 5: "CLE", 6: "DAL", 7: "DEN",
    8: "DET", 9: "GB", 10: "TEN", 11: "IND", 12: "KC", 13: "LV", 14: "LAR", 15: "MIA",
    16: "MIN", 17: "NE", 18: "NO", 19: "NYG", 20: "NYJ", 21: "PHI", 22: "ARI",
    23: "PIT", 24: "LAC", 25: "SF", 26: "SEA", 27: "TB", 28: "WSH", 29: "CAR",
    30: "JAX", 33: "BAL", 34: "HOU",
}

SCORING = {
    3:  0.04,   # Passing Yards
    4:  6.0,    # Passing TD
    20: -2.0,   # Interception Thrown
    24: 0.1,    # Rushing Yards
    25: 6.0,    # Rushing TD
    42: 0.1,    # Receiving Yards
    43: 6.0,    # Receiving TD
    53: 0.5,    # Receptions (0.5 PPR)
    72: -2.0,   # Fumble Lost
    62: 2.0,    # 2-Point Conversion (PROJECTION side)
    19: 2.0,    # 2-pt Passing Conversion  (ACTUAL side)  -- doc 56
    26: 2.0,    # 2-pt Rushing Conversion  (ACTUAL side)  -- doc 56
    44: 2.0,    # 2-pt Receiving Conversion(ACTUAL side)  -- doc 56
    101: 6.0,   # Kickoff Return TD
    102: 6.0,   # Punt Return TD
}
SCORING_CHECK_POS = {"QB", "RB", "WR", "TE"}

def is_empty_stat(stat):
    raw = stat.get("stats") or {}
    return len({int(k) for k in raw} - {210}) == 0

# ------------------------------------------------------------------ Network Fetch --
def fetch(season, sort_mode, drop_scoring_filter=False, retries=3):
    import requests
    url = (f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}"
           f"/segments/0/leagues/{LEAGUE_ID}?view=kona_player_info")
    
    prior = season - 1
    stat_ids = [f"00{season}", f"10{season}", f"00{prior}", f"10{prior}"]
    
    filter_dict = {
        "limit": LIMIT
    }
    
    if not drop_scoring_filter:
        filter_dict["filterStatsForTopScoringPeriodIds"] = {
            "value": 2,
            "additionalValue": stat_ids
        }
    
    if sort_mode == "owned":
        filter_dict["sortPercOwned"] = {"sortPriority": 100, "sortAsc": False}
    else:
        filter_dict["sortDraftRanks"] = {"sortPriority": 100, "sortAsc": True, "value": "STANDARD"}
        
    hdr = {
        "x-fantasy-filter": json.dumps({"players": filter_dict}),
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    
    last = None
    for a in range(retries):
        try:
            r = requests.get(url, headers=hdr, cookies=COOKIES, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last = e
            print(f"  attempt {a+1}/{retries} failed: {e}", file=sys.stderr)
            time.sleep(2 * (a + 1))
    raise SystemExit(f"ESPN request failed after {retries} attempts: {last}\n"
                     "Check COOKIES in script configuration.")

# ------------------------------------------------------------------ Data Parsing --
def season_rows(player, season, source):
    target_id = f"00{season}" if source == 0 else f"10{season}"
    out = []
    for s in player.get("stats", []):
        if str(s.get("id")) == target_id:
            out.append(s)
    return out

def pick_one(rows, label, name, anomalies):
    if len(rows) == 1:
        return rows[0]
    if len(rows) == 0:
        return None
    anomalies.append(f"{name}: {len(rows)} rows matched {label} — took first")
    return rows[0]

def verify_scoring(stat):
    raw = stat.get("stats") or {}
    got = sum(SCORING[int(k)] * v for k, v in raw.items()
              if int(k) in SCORING and isinstance(v, (int, float)))
    espn = stat.get("appliedTotal")
    return got, espn, (None if espn is None else got - espn)

def parse(data_cur, data_pri, season):
    prior = season - 1
    players_cur = data_cur.get("players", [])
    if not players_cur:
        raise SystemExit("No 'players' key found in payload response.")

    pri_lookup = {}
    for entry in data_pri.get("players", []):
        p = entry.get("player") or {}
        if "id" in p:
            pri_lookup[p["id"]] = p

    stamp = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    rows, anomalies, scoring_err, actual_err, empty_proj = [], [], [], [], []

    for entry in players_cur:
        p = entry.get("player") or {}
        name = p.get("fullName", "Unknown")
        espn_id = p.get("id")

        p_prior = pri_lookup.get(espn_id, {})

        cur = pick_one(season_rows(p, season, 1), f"proj {season}", name, anomalies)
        acs = pick_one(season_rows(p, season, 0), f"actual {season}", name, anomalies)
        
        pri = pick_one(season_rows(p_prior, prior, 1), f"proj {prior}", name, anomalies)
        acp = pick_one(season_rows(p_prior, prior, 0), f"actual {prior}", name, anomalies)

        pos = POS_MAP.get(p.get("defaultPositionId"), p.get("defaultPositionId"))
        
        if pos in SCORING_CHECK_POS:
            if cur is not None:
                if is_empty_stat(cur):
                    empty_proj.append(name)
                else:
                    got, espn, err = verify_scoring(cur)
                    if err is not None and abs(err) > 1.0:
                        scoring_err.append((name, round(got, 2), round(espn, 2), round(err, 2)))
            
            if acs is not None and not is_empty_stat(acs):
                got, espn, err = verify_scoring(acs)
                if err is not None and abs(err) > 1.0:
                    actual_err.append((name, round(got, 2), round(espn, 2), round(err, 2)))

        own = p.get("ownership") or {}
        ranks = (p.get("draftRanksByRankType") or {})
        rows.append({
            "Player": name,
            "espn_id": espn_id,
            "pos": pos,
            "team": TEAM_MAP.get(p.get("proTeamId"), p.get("proTeamId")),
            "injuryStatus": p.get("injuryStatus"),
            f"proj_{season}": cur.get("appliedTotal") if (cur and not is_empty_stat(cur)) else None,
            f"actual_{season}": acs.get("appliedTotal") if (acs and not is_empty_stat(acs)) else None,
            f"proj_{prior}": pri.get("appliedTotal") if (pri and not is_empty_stat(pri)) else None,
            f"actual_{prior}": acp.get("appliedTotal") if (acp and not is_empty_stat(acp)) else None,
            "espn_adp": own.get("averageDraftPosition"),
            "pct_owned": own.get("percentOwned"),
            "rank_std": (ranks.get("STANDARD") or {}).get("rank"),
            "rank_ppr": (ranks.get("PPR") or {}).get("rank"),
            "raw_stats": json.dumps(cur.get("stats") if cur else None),
            "raw_actual_stats": json.dumps(acs.get("stats") if acs else None),
            "captured_at": stamp,
        })

    df = pd.DataFrame(rows)
    print(f"\n[{season}] Parsed {len(df)} players")
    
    for prefix, yr in [("proj", season), ("actual", season), ("proj", prior), ("actual", prior)]:
        col = df[f'{prefix}_{yr}']
        print(f"  {yr} {prefix.upper():<10}: {col.notna().sum():<4} non-null, {(col > 0).sum():<4} non-zero")
    
    print(f"  Empty proj_{season} recorded : {len(empty_proj)}")

    # A6 (doc 56): row count is the wrong invariant -- every corrupt 2023 pull returned exactly
    # LIMIT rows. Gate on how many players actually carry a projection.
    _live = int(df[f'proj_{season}'].notna().sum())
    _MIN_PROJ = 400
    if len(df) < LIMIT:
        print(f"  !! SHORT PULL: {len(df)} rows, expected {LIMIT}")
    if _live < _MIN_PROJ:
        print(f"\n  !!!! PULL REJECTED: only {_live} of {len(df)} players carry a {season} "
              f"projection (expected >= {_MIN_PROJ}).")
        print(f"       This is the 2023 failure mode. The file was still written for inspection,")
        print(f"       but DO NOT build a board on it. Re-run; ESPN is nondeterministic here.")
        anomalies.append(f"REJECTED: {_live} live projections")
    
    if scoring_err or actual_err:
        print(f"\n  !! SCORING RECONCILIATION MISMATCH: {len(scoring_err)} proj, {len(actual_err)} actual")
        for row in (scoring_err + actual_err)[:20]:
            print("     ", row)
    else:
        print("  SCORING RECONCILIATION PASSED (populated rows match league scoring map).")
        
    if anomalies:
        print(f"  Notice: {len(anomalies)} row selection anomalies logged (first 5 shown):")
        for a in anomalies[:5]:
            print("     ", a)
            
    return df

# ------------------------------------------------------------------ Execution Flow --
def process_single_season(season, sort_mode, outdir, raw_file=None, drop_scoring_filter=False):
    print(f"\n{'='*70}\nPROCESSING SEASON: {season} (sort: {sort_mode})\n{'='*70}")
    prior = season - 1
    
    if raw_file:
        print(f"  -> Warning: --raw bypasses prior-year fetch. Prior columns will be null.")
        with open(raw_file, encoding="utf-8") as fh:
            data_cur = json.load(fh)
        data_pri = {"players": []}
        print(f"Re-parsing local file: {raw_file}")
    else:
        print(f"Requesting top {LIMIT} players for {season}...")
        data_cur = fetch(season, sort_mode, drop_scoring_filter=drop_scoring_filter)
        
        print(f"Requesting top {LIMIT} players for {prior} to populate prior-year columns...")
        try:
            data_pri = fetch(prior, sort_mode, drop_scoring_filter=drop_scoring_filter)
        except Exception as e:
            print(f"  -> Warning: Could not fetch prior season ({prior}). Error: {e}")
            data_pri = {"players": []}

        rawpath = outdir / f"espn_raw_{season}_{dt.datetime.now():%Y%m%d_%H%M}.json"
        with open(rawpath, "w", encoding="utf-8") as fh:
            json.dump(data_cur, fh, ensure_ascii=False)
        print(f"Raw JSON backup saved -> {rawpath}")

    df = parse(data_cur, data_pri, season)
    out = outdir / f"espn_projections_{season}_{dt.datetime.now():%Y%m%d_%H%M}.csv"
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"CSV exported successfully -> {out}")

def confirm_seasons(seasons, assume_yes=False):
    """Refuse to pull a completed season by accident.

    ESPN serves ONE averageDraftPosition field. Re-pulled after a season ends it has
    drifted toward what happened (directive 1.1 / doc 53): 2024 Barkley reads 3.4
    against a true preseason 17. A historical pull is therefore only ever valid for
    projections, never as a market -- and on 2026-08-28 a bare run of this script
    silently produced exactly that file. This makes the choice explicit.
    """
    hist = sorted(x for x in seasons if x < DRAFT_SEASON)
    print(f"\n{'='*70}\nSEASONS REQUESTED: {sorted(seasons)}    (draft season is {DRAFT_SEASON})\n{'='*70}")
    if not hist:
        return True
    print(f"  !!!! {len(hist)} COMPLETED SEASON(S) REQUESTED: {hist}")
    print( "       espn_adp from a completed season is a POST-season field, not a market.")
    print( "       Directive 1.1: never use it as a market. Projections only.")
    if assume_yes:
        print("       --yes supplied; proceeding.")
        return True
    if not sys.stdin.isatty():
        print("       Non-interactive and no --yes. REFUSING.", file=sys.stderr)
        return False
    try:
        return input("       Type the word  historical  to proceed: ").strip().lower() == "historical"
    except EOFError:
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seasons", type=int, nargs="+", default=DEFAULT_SEASONS,
                    help=f"List of seasons to pull (default: {DEFAULT_SEASONS})")
    ap.add_argument("--sort", choices=["draft", "owned"], default="owned",
                    help="Sorting method ('owned' recommended for closed seasons)")
    ap.add_argument("--raw", help="Re-parse a saved JSON file instead of network fetch")
    ap.add_argument("--out", help="Directory where files should be written")
    ap.add_argument("--drop-filter", action="store_true", help="Drop the top scoring period filter")
    ap.add_argument("--yes", action="store_true",
                    help="Skip the completed-season confirmation (for scripted runs)")
    a = ap.parse_args()

    if not confirm_seasons(a.seasons, assume_yes=a.yes):
        raise SystemExit("Aborted: seasons not confirmed. Nothing was pulled.")

    if a.raw and len(a.seasons) > 1:
        raise SystemExit("--raw supports exactly one --seasons value")

    outdir = resolve_outdir(a.out)
    print(f"Output Destination: {outdir}")

    for season in a.seasons:
        process_single_season(season, a.sort, outdir, a.raw, a.drop_filter)

if __name__ == "__main__":
    main()