"""
code_adp_guard.py -- ADP PROVENANCE GUARD.  Written 2026-08-26.

RULE (Matt, 2026-08-26): "ADP before the draft is the correct measure for projecting
2026, and for prior years draft prep. The prep doesn't include knowing the actual ADP
when the draft is over."

WHY THIS IS A HARD REFUSAL AND NOT A THRESHOLD
ESPN's player endpoint serves ONE `averageDraftPosition` field. Re-pulled after a season
ends, it has drifted toward what happened. The drift is NOT a broad shift -- it is
concentrated in exactly the players whose outcome diverged from their preseason price,
which is the worst possible place for it, because those players are what a backtest turns on:

  2024 pull   McCaffrey  espn_adp 16.0   preseason consensus rank 1   (missed the season)
  2024 pull   Barkley    espn_adp  3.4   preseason consensus rank 17  (MVP-caliber year)
  2024 pull   Kamara     espn_adp  8.3   preseason consensus rank ~50
  2023 pull   Nacua      espn_adp 44.0   Underdog preseason ADP 216   (undrafted -> WR5)

I tried to build a DETECTOR so a contaminated column could still be used where it was
"clean enough". It failed its negative control and is withdrawn -- see WITHDRAWN below.
There is no salvage path. Use a preseason capture or drop the season.
"""
import os
import pandas as pd

# Registry lives in ./adp_registry next to this file. Override with $ADP_REGISTRY.
REGISTRY_DIR = os.environ.get(
    "ADP_REGISTRY", os.path.join(os.path.dirname(os.path.abspath(__file__)), "adp_registry"))

# Contemporaneous preseason boards actually held, one per season. Provenance in MANIFEST.csv.
PRESEASON_SOURCES = {
    2021: "FantasyPros_2021_Overall_ADP_Rankings.csv :: AVG of Yahoo, Sleeper, RTSports  (FantasyPros half-PPR archive, exported by Matt 22 Sept 2026, doc 385; the consensus-RANK proxy it replaced is _archive\\preseason_adp_2021_replaced_20260922_0628.csv)",
    2022: "FantasyPros_2022_Overall_ADP_Rankings.csv :: AVG of Yahoo, Sleeper  (FantasyPros half-PPR archive, read 22 Sept 2026, doc 384; the rounded xlsx column it replaced is in _archive)",
    2023: "FantasyPros_2023_Overall_ADP_Rankings.csv :: AVG of Yahoo, Sleeper, RTSports  (FantasyPros half-PPR archive, read 22 Sept 2026, doc 384; the Underdog best-ball file it replaced is in _archive)",
    2024: "FantasyPros_2024_Overall_ADP_Rankings.csv :: AVG of Yahoo, Sleeper, RTSports  (true preseason ADP; the consensus-RANK proxy used 26 Aug to 22 Sept 2026 is in _archive, doc 383)",
    2025: "FantasyPros_2025_Overall_ADP_Rankings.csv :: AVG of Yahoo, Sleeper, RTSports, Real-Time  (FantasyPros half-PPR archive, exported by Matt 22 Sept 2026, doc 385; the rounded nine-site file it replaced is NOT in _archive, see doc 385)",
}


def load_preseason_adp(season):
    """The only sanctioned way to get a historical season's draft market."""
    if season not in PRESEASON_SOURCES:
        raise AssertionError(
            f"season {season}: no contemporaneous preseason board is held.\n"
            f"  ESPN's historical `espn_adp` has measured drift toward outcomes and MUST NOT\n"
            f"  be substituted (doc 53). Supply a preseason capture or drop the season.\n"
            f"  Held: {sorted(PRESEASON_SOURCES)}")
    path = os.path.join(REGISTRY_DIR, f"preseason_adp_{season}.csv")
    if not os.path.exists(path):
        raise AssertionError(f"registry file missing: {path}")
    return pd.read_csv(path)


def refuse_historical_espn_adp(df, season, adp_col="espn_adp"):
    """Call this at the top of ANY backtest, opponent model, keeper-prediction or
    survival estimate that touches a completed season. It refuses unconditionally."""
    if adp_col in df.columns and season < 2026:
        raise AssertionError(
            f"REFUSED: `{adp_col}` from a {season} historical pull is a POST-season field, "
            f"not a preseason market (doc 53). Call load_preseason_adp({season}) instead.")
    return True


# ---------------------------------------------------------------------------
# WITHDRAWN -- kept as a record so this is not re-attempted.
#
# Hypothesis: a contaminated ADP column can be detected by |spearman(adp, actual)|,
#             because a real preseason market predicts the finish only weakly (~0.35).
# TESTED, 2026-08-26, and it FAILED both directions on population adp<=180:
#     clean 2022 contemporaneous board  rho = 0.551   -> would be REJECTED (false positive)
#     contaminated 2023 ESPN pull       rho = 0.339   -> would be ACCEPTED (false negative)
# The clean and contaminated distributions overlap completely (clean 0.26-0.62,
# contaminated 0.18-0.80 depending on the population cut). NO THRESHOLD SEPARATES THEM.
# Cause: the drift is concentrated in a few divergent players, so it barely moves an
# aggregate rank correlation. Aggregate checks cannot find it. Do not rebuild this.
# ---------------------------------------------------------------------------
