# 50 — THE BOONE TEST FINALLY RAN. THE DATA EXISTED ALL ALONG.
**Aug 25, 2026.** Matt was right on the factual point: he *did* collect historical Boone rankings.
Doc 43 and the prior handoffs recorded "no Boone rankings before 2026" — **that was a search
failure, not a supply failure.** The rankings were never in files named "Boone"; they are columns
and sheets inside combined workbooks (`Boone Rank`, `JB Rank`, `JB R`, a `boone` tab).

> **PARTIALLY WITHDRAWN — see `51_adp_contamination_defect.md` (same day).**
> Matt asked whether the historical ADP was representative. It is not: `espn_adp` from a past-season
> pull has drifted toward that season's outcome (2024 file has McCaffrey at 16.0 and Saquon at 3.4;
> reality was ~1 and ~17). **Three tests below are withdrawn** — the ADP comparison column, the
> incremental-information test, and both breakout/bust definitions, all of which used ADP as a
> control. **The headline survives**: it never used ADP. Re-run with ADP removed entirely,
> pooled n=539: **Boone 0.428 vs ESPN 0.681**, bootstrap 95% CI on the gap [+0.181, +0.326],
> excludes zero. ESPN's projections are separately verified clean (McCaffrey projected 301.8,
> finished 40.3 — no hindsight).

## WHAT WAS FOUND — FOUR SEASONS

| year | source | n |
|---|---|---|
| 2021 | `_Fantasy\2021\Combined_CSVs\Combined_Rankings_9-3-Combined.csv` → `Boone Rank` | 194 |
| 2022 | `_Fantasy\2022\Rankings vs ADP - 2022.xlsx` → `JB Rank` | 183 |
| 2023 | `OneDrive\Fantasy\Combined FF Rankings 2023.xlsx` → `boone` sheet | 250 |
| 2025 | `Downloads\Fantasy Football 2025 - combined rank.csv` → `Justin B Player`/`JB R` | 185 |

Testable head-to-head: **2021, 2022, 2025** (2023 has no usable ESPN projection — doc 43).

## AN ERROR I MADE AND CAUGHT

The first 2025 extraction paired `JB_Player` with `JB R`. Those are **two different rank blocks in
the same sheet** — the correct pairs are `JB_Player`↔`JB Rank Data` and `Justin B Player`↔`JB R`.
Every 2025 row was shifted. Caught because a downstream number (3.9%) was too extreme to be real.
Corrected and cross-checked: the two valid pairings now agree with **max |diff| = 0** across 184
players. All numbers below use the corrected data.

## HEADLINE — ESPN'S PROJECTION BEATS BOONE'S RANKING, CLEARLY

Spearman correlation with **actual end-of-season finish**. Population: matched players inside
uncensored ADP (<169), non-K/DST. This is not circular — both are scored against real outcomes.

| year | n | Boone | ESPN proj | ADP (market) |
|---|---|---|---|---|
| 2021 | 162 | 0.344 | **0.662** | 0.576 |
| 2022 | 154 | 0.422 | 0.603 | **0.640** |
| 2025 | 135 | 0.169 | **0.634** | 0.484 |
| **pooled** | **451** | **0.341** | **0.647** | 0.583 |

**Boone loses to ESPN in all three years, and loses to simply following ADP in all three.**

## THE DECISIVE TEST — DOES EITHER ADD INFORMATION BEYOND THE MARKET?

Overall correlation rewards agreeing with the market. The question that actually matters is
whether a ranker's *disagreement* with ADP predicts *beating* ADP. Market as control, deviation
as signal, market-beating as outcome. Non-circular for both.

| | pooled r | p | verdict |
|---|---|---|---|
| **Boone deviation → beating the market** | **−0.115** | 0.015 | **no evidence of added information** (significantly negative) |
| **ESPN deviation → beating the market** | **+0.412** | <0.0001 | **adds real information** |

Per year, Boone: −0.136 / −0.172 / −0.034. Never positive.

**Boone tracks the market more tightly than ESPN does** (r with ADP: Boone 0.816, ESPN 0.646) and
where he departs from it, those departures went the wrong way slightly more often than not.

## WHAT ABOUT THE BREAKOUT CLAIM SPECIFICALLY

Matt's real claim was not overall accuracy — it was that Boone identified breakouts. Tested two
ways, and **both framings turned out to be traps I had to discard:**

1. **Breakout defined vs ESPN's ranking** ("ESPN had him low, he finished high"): Boone was higher
   on **13 of 17** breakouts (76%) with mean advantage **+12.2 ranks** — but his base rate of
   ranking *anyone* above ESPN is **65%**, and the difference is not significant (binomial
   p=0.238; Mann-Whitney p=0.240). **And the framing is circular** — the label is defined from
   ESPN's ranking, so ESPN scores 0% by construction and can never win.
2. **Breakout defined vs ADP**: same defect in mirror image — ADP scores 0% by construction, and
   because Boone tracks ADP at r=0.816 he inherits that, scoring 3.9%. Measures
   divergence-from-market, not skill.

**Neither framing supports the breakout claim, and neither refutes it cleanly** — they are both
badly posed. The incremental-information test above is the one that is properly specified, and it
does not favour Boone.

## THE YAHOO HYPOTHESIS — NOT SUPPORTED

Matt's read was that Boone got more conservative and less useful after joining Yahoo in 2025.
Measured as mean absolute deviation from ESPN's ranking (higher = more willing to disagree):
**2021: 31.5 · 2022: 27.2 · 2025: 36.1.** He was *more* willing to diverge in 2025, not less.
His accuracy in 2025 (0.169) is his worst of the three, but the mechanism is not conservatism.

## WHAT THIS DOES AND DOES NOT SETTLE

**Settles:** on this evidence, one analyst's published ordering does not beat a projection-derived
ordering, and does not beat ADP. The prior claim rested on a circular comparison (doc 06's own
disclaimer); this one does not, and it reaches the same direction with a cleaner method.

**Does not settle:** n=3 seasons, one analyst, one league's scoring. A published top-200 list is
not the same as an analyst's actual draft-day behaviour, and rank-order correlation ignores *where*
on the board the error falls — being wrong at pick 8 costs more than being wrong at pick 150.
Neither is captured here.

**The honest summary for Matt:** he was right that the data existed and right to insist it be
tested. The test now says his instinct about Boone does not hold up — but it took finding his
data to establish that, and "untested" was never the same as "true."

## LIMITS
1. n=451 player-seasons, 3 seasons, 1 analyst.
2. Boone's lists are snapshots of varying dates; the exact capture date within each preseason is
   unknown and rankings move.
3. ESPN `proj_2021`/`proj_2022` were pulled in 2026. Their correlation with outcome (0.60–0.66)
   sits in the band doc 21 established for genuine preseason projections (0.55–0.75), well below
   the >0.90 that would indicate hindsight leakage — but this was not separately re-verified here.
4. Matched population only; players Boone ranked who ESPN did not project are excluded.
