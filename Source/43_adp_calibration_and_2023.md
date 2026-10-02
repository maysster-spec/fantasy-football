# 43 — IS ESPN ADP THE RIGHT MARKET TO PULL? AND THE 2023 POST-MORTEM
**Aug 25, 2026.** Two questions Matt raised. Both are answered against data, and the first one
corrects a claim made in an earlier chat in this project.

---

## PART 1 — "ESPN ADP DOESN'T REFLECT MY LEAGUE SETTINGS." TRUE, AND ALMOST IRRELEVANT.

**The claim is factually right.** `ownership.averageDraftPosition` is ESPN's **global, cross-league**
ADP, computed across all ESPN leagues on default scoring. It has no knowledge of this league's
6-point passing TD or 0.5 PPR. Nothing in the pull can make it league-specific.

**But the conclusion drawn from it — don't pull it — is wrong, for two reasons.**

### It is a behaviour, not an evaluation

`ERROR_PATTERNS` B6 draws exactly this line: *"Distinguish evaluations (rankers) from behaviours
(ADP, mock drafts) — they answer different questions."* ESPN ADP is not being used to say who is
good. It is used in §4.12 to model **what the other eleven managers will do**, and those eleven
managers draft on ESPN's platform looking at ESPN's board. Its miscalibration to league scoring is
not a defect for that purpose — **it is the thing being measured.** Dropping it would leave the
model with no opponent behaviour signal at all.

Note also that no available ADP is league-calibrated. The FantasyPros export
(`FantasyPros_2026_Overall_ADP_Rankings 1.csv`, Yahoo/Sleeper/RTSports, no ESPN column) is
*equally* uncalibrated to 6-pt passing TDs, and further from the board Matt's opponents actually
see. It remains useful as a cross-market check, not as a replacement.

### Measured, the miscalibration is small

**[TESTED]** Board ordered by **VBD under this league's scoring** vs ordered by ESPN ADP.
**BASELINE:** ESPN market slot minus league-value slot; positive = the market takes them later than
league value warrants. **POPULATION:** non-K/DST, uncensored ADP < 169. **SAMPLE:** n=167.

| pos | n | mean gap | median | directive §4.4 (ESPN column) |
|---|---|---|---|---|
| QB | 27 | **+1.7** | +2.0 | +5.5 |
| TE | 23 | **+8.5** | +7.0 | +5.0 mean / −1.5 median |
| RB | 51 | **+3.5** | +3.0 | +8.1 |
| WR | 66 | **−6.3** | −4.0 | **−6.4** |

WR reproduces §4.4 almost exactly (−6.3 vs −6.4). QB, RB and TE have drifted from the recorded
values and §4.4's ESPN column should be refreshed to these numbers at the Sept 5 pull.

**The QB gap is +1.7 picks, not a round.** Josh Allen is the top QB by VBD (+80.3, board rank 14)
and the market takes him at 22.1 — a five-pick gap, which §4.2 already prices. The 6-point passing
TD does *not* leave quarterbacks broadly mispriced on ESPN's board.

### A caught error worth recording

The first version of this test ranked players by **raw projected points** instead of VBD, and
reported a QB gap of **+82 picks** — because a quarterback's 421 points was being compared to a
running back's 330 as though they were the same unit. That is precisely the error VBD exists to
prevent, and it inflated the effect roughly **50×**. Caught before it reached a recommendation.
Logged here because directive §0 requires reporting tests that kill their own first answer.

**Verdict: keep pulling ESPN ADP. It is the correct and only behavioural anchor for this league.**

---

## PART 2 — 2023 POST-MORTEM: `--drop-filter` DID NOT WORK

`python Espn_pull_projections.py --seasons 2023 --drop-filter` was run at 08:14 on Aug 25.
Removing `filterStatsForTopScoringPeriodIds` was the highest-value experiment in
`GEMINI_FIX_BRIEF_espn_pull.md`. **Result: no change.** 96 real `proj_2023` values, 19 inside
ADP 169, and McCaffrey, Hill, Chase, Kelce, Ekeler, Hurts and Lamb all still null — identical to
the run before it. **The stat filter was not the cause; that hypothesis is dead.**

### A structural clue found by comparing 2021 (works) against 2023 (broken)

Stat rows returned per player, by `(statSourceId, statSplitTypeId)`:

| payload | src=0 split=0 | src=0 split=1 | src=1 split=0 | src=1 split=2 |
|---|---|---|---|---|
| **2021 (works)** | 700 | — | **691 rich** | **700** |
| **2023 (broken)** | 700 | 1285 | **699 hollow** | **absent** |

In 2021 each player carries two projection rows: `split=0` the season total (Ekeler 226.9) and
`split=2` the per-game figure (16.84). **2023 has no `split=2` rows at all**, and its `split=0`
rows contain only `{"210": games_played}`. So 2023's projection data is shaped differently, not
merely filtered — which is why removing a filter did nothing.

### Why imputing 2023 from ESPN's preseason ranks was tried and rejected

`rank_ppr` / `rank_std` are fully populated for 2023 (700/700) and are genuinely season-specific
(only 2% of values match the 2024 pull, so they are not a stale 2026 snapshot). That made
rank → points imputation worth testing.

**[TESTED] It fails on two counts.** `rank_ppr` is **entirely absent from the 2021 and 2022 pulls
(0/700 each)**, so the mapping could be calibrated on 2024 alone — a single year. And even there
the relationship is loose: log-rank against projected points gives **r ≈ −0.80 to −0.85 by
position (R² ≈ 0.70)**, so roughly 30% of the variance in the exact quantity the backtest measures
would be manufactured. That is `ERROR_PATTERNS` **B5** — generated values filling a gap — and it
would be injected into the outcome variable itself. **Rejected.**

### What is left, in order

1. **`probe_2023_projections.py`** — four single-request experiments (generic season endpoint with
   no league scope; `view=mDraftDetail`; `kona_playercard`; an explicit `filterStatsForSplitTypeIds`
   request for the missing `split=2`). Each reports one number: how many stat keys McCaffrey's 2023
   projection row carries. **1 key = still broken, 25+ = fixed.** This is the last cheap thing.
2. If all four come back hollow, **2023 cannot join the VBD backtest** and the matter should be
   closed. 2021, 2022, 2024 and 2025 all work, which is a four-season sample — the original
   falsifier only ever asked for three.
3. A **rank-based or ADP-based** rule could still include 2023 using its intact `espn_adp`
   (224 uncensored) and `actual_2023`. That answers a different question — what the market
   *looked* like versus what was *valuable* — and must never be pooled with the VBD numbers
   without saying so.

**Matt's stated reason for wanting 2023 is sound and worth recording:** league composition changed
between 2023 and 2024 (Pierce departed, Arthur Ray joined), so 2021–2023 and 2024–2025 are two
different manager populations. Without 2023 the older era rests on 2021 and 2022 alone.
