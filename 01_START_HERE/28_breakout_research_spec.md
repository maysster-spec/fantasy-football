# 28 — BREAKOUT RESEARCH SPEC: THE WIDE STUDY, WRITTEN FOR ANOTHER MODEL
**Aug 23, 2026.** Hand this whole file to the model doing the work. It is self-contained.

---

## WHY THE CURRENT SAMPLE IS TOO NARROW — stated precisely

The 2025 result (`claude/26_breakout_economics.md`) rests on **one season, twelve teams,
146 drafted skill players, 15 breakouts**. It found aggregate roster surplus correlates
−0.783 with final seed (p=0.003). That is suggestive and it is not enough.

**Here is exactly what blocks widening it, verified against the files on hand:**

| year | league draft | league standings | player preseason price | **player actual finish** |
|---|---|---|---|---|
| 2021 | ✅ | ❌ | ❌ | ❌ |
| 2022 | ✅ | ✅ | ❌ | ❌ |
| 2023 | ✅ | ✅ | ❌ | ❌ |
| 2024 | ✅ | ✅ | ❌ | ❌ |
| 2025 | ✅ | ✅ | ✅ | ✅ |

**Only 2025 has both a preseason price and a season outcome at player level.** Everything else
is blocked on two missing inputs, both free:

1. **Player-level season fantasy points, 2021–2024, in THIS league's scoring.**
   Derivable from nflverse play-by-play plus the twelve-component scoring map in §2 below.
2. **Dated preseason ADP or projections, 2021–2024.**

Get those two and four more league-seasons unlock immediately, plus the whole NFL population.

---

## THE STUDY TO RUN

### Unit of analysis
**Player-season.** Not player. Not team. A player appears once per year he was draftable.

### Outcome — do not use raw points
```
surplus = (actual_points − actual_replacement_at_his_position)
        − (preseason_projection − preseason_replacement_at_his_position)
```
Replacement = the Nth-best at that position, N = 12 QB · 30 RB · 30 WR · 12 TE for a 12-team
league starting 1/2/2/1 plus a flex.

**Why position-adjusted is not optional.** This project ranked all positions together on raw
points once. In a six-point-passing-touchdown league every starting quarterback outscores every
running back, so "breakout" collapsed into "drafted a QB late" — nine of the top fourteen were
quarterbacks. Position-adjusted, QBs were two of fifteen. **If your model's top breakout
predictions are mostly quarterbacks, you have reproduced this bug.**

Define `BREAKOUT = top decile of surplus within the draftable population, within that season.`
Report the base rate every time.

### The scoring system — use exactly this, it is not standard
```
passing yards 0.04 · PASSING TD 6 · interception −2
rushing yards 0.1 · rushing TD 6
receiving yards 0.1 · receiving TD 6 · RECEPTION 0.5
fumble lost −2 · 2-point conversion 2 · kick-return TD 6 · punt-return TD 6
```
Verified to reconstruct ESPN's own totals to a maximum error of 0.197 points.
**Nearly every public ranking assumes full PPR and 4-point passing TDs. Convert or say so.**

### Predictors — pre-draft observable only
Anything you use must have been knowable before Labor Day of that season. No in-season data,
no post-hoc team context, no "he got the starting job in week 3."

### These eighteen factors are already dead. Do not resell them.
Offensive scheme · targets per route run · yards per route run · pass rate over expected ·
NFL draft capital · year-2 experience leap · vacated targets · strength of schedule ·
ranker disagreement · manager positional timing · athleticism · contract year · breakout age ·
BMI · offensive-line quality for running backs · handcuffs · ambiguous backfield ·
elite TPRR with few routes.

Each failed at least one of: year-over-year stickiness · out-of-sample R² gain over prior-year
points per game with a bootstrap CI excluding zero · survival after controlling for volume.

### What survived, and is therefore your starting point
- **Red-zone opportunity is sticky:** inside-10 targets **r=+0.59**, red-zone target volume
  **r=+0.51**, red-zone target share **r=+0.48** (n=37, 2024→2025).
- **Red-zone touchdown RATE is not:** r=+0.02. Noise. Never use it.
- After-contact ability is mildly underweighted — tiebreaker only.
- **Untested and live:** offensive-line quality for **quarterbacks** (the RB version is dead;
  the QB version has never been tested, and line disruption costs passing EPA −0.086, p=0.004,
  worth roughly 15–25 fantasy points to a QB over a season). Current status only — 2024→2025
  line-continuity churn is r=−0.01, so history does not forecast it.

### Method — the five guards that stop false patterns
1. **Cluster by team-season.** A team-level variable assigned to every player on that team gives
   you ~32 independent values, not 210. Resample groups, not rows.
2. **Out-of-sample only.** Fit on years 1..n−1, test on year n. Report cross-validated AUC, not
   in-sample R².
3. **Control for the projection.** Any outcome defined as actual-minus-expected is mechanically
   negatively correlated with prior production. Report the partial correlation controlling for
   the preseason projection. The raw one is uninterpretable.
4. **State the number of comparisons** and the corrected threshold in the same sentence as any
   result. A z of 2.3 in a scan of 400 combinations is nothing.
5. **If a subgroup has fewer than ~30 observations, the word is UNDERPOWERED, not "no effect."**

### Deliverable
A per-player **probability of top-decile surplus**, with:
- cross-validated AUC against a baseline of "sort by preseason projection"
- a calibration plot (predicted vs observed, decile buckets)
- the base rate
- **the specific result that would make you abandon each feature**

If your model cannot beat "sort by the projection" out of sample, say so plainly. That is a
real and useful answer — it has been the answer eighteen times already.

---

## DATA SOURCES — free, authoritative, and verified reachable

| what | where | notes |
|---|---|---|
| play-by-play 1999–2025 | `github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_YYYY.parquet` | build season fantasy points in any scoring |
| weekly player stats | `.../releases/download/player_stats/` | faster than rebuilding from PBP |
| snap counts | `.../releases/download/snap_counts/snap_counts_YYYY.parquet` | the OL-continuity input |
| rosters, players, IDs | `.../releases/download/rosters/` and `/players/` | **join on `gsis_id`** |
| injuries | `.../releases/download/injuries/injuries_YYYY.parquet` | weekly report status |
| historical preseason projections | `github.com/FantasyFootballAnalytics/ffanalytics` | multi-source scraper with archives |
| red-zone and advanced splits | pro-football-reference.com | already exported for 2023–2025 |
| ADP archive | FantasyPros paid tier (owner has it) | dated snapshots |

**Join rule, non-negotiable.** Key on `gsis_id`. Where an ID is unavailable the key is
**name + position + team**, never less — and if the source abbreviates first names, add a
numeric tiebreaker. This project has had **ten** name-collision failures, the most recent being
`B. Robinson, ATL, RB` matching both Bijan Robinson and Brian Robinson Jr. **Assert row counts
before and after every merge and fail on a drop.**

---

## WHO RUNS WHICH PART

**Google Antigravity — build the dataset.** It has code execution. Output four files:
`player_season_points_2021_2025.csv` (league scoring, position-adjusted),
`preseason_price_2021_2025.csv`, `features_preseason_2021_2025.csv`, `join_audit.txt`.

**GPT 5.6 Think Deeper — model and interpret.** Give it this file plus Antigravity's output.
It runs the five guards and returns the AUC, calibration and falsifiers.

**Claude — score and red-team.** Bring the result back here. It gets tested against the 2025
holdout already on disk before it touches a draft-day pick.

---

## THE OWNER'S OWN BREAKOUT LIST — use as the validation set, with one warning
Bijan Robinson · Puka Nacua · Christian McCaffrey · Jaxon Smith-Njigba · Chris Olave ·
Trey McBride · Brock Purdy · Chase Brown · Drake Maye · George Pickens · Derrick Henry ·
Jonathan Taylor · Michael Wilson.

**Warning: this list spans several seasons, not one.** Match each name to **its own** breakout
year before computing anything against it. Treating all thirteen as one season's cohort will
produce a confident wrong answer.
