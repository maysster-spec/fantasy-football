# 52 — TWO-SEASON RANKER BACKTEST ON CLEAN PRESEASON ADP
**Aug 25, 2026.** Supersedes doc 50's secondary tests. Artifact: **Ranker Edge Ledger**.
Reproduce: `/tmp/viz/backtest_2022.csv`, `backtest_2025.csv`, `pooled.csv`.

## WHY THIS ONE IS TRUSTWORTHY WHERE DOC 50 WAS NOT

Doc 51 established that `espn_adp` from a past-season pull drifts toward that season's outcome and
cannot be used as a preseason market. **This test uses only ADP Matt captured before the drafts:**
- **2022** — FantasyPros preseason ADP (`FP_ADP`) from the 4for4 workbook. Sanity: Jonathan Taylor 1,
  Ekeler 2, McCaffrey 3, Henry 4, Kupp 5 — the real 2022 board.
- **2025** — nine-site average from the combined workbook.

**Alignment was verified, not assumed.** The 2022 workbook carries three separately-sorted side
blocks that disagree with the main block (1–4% agreement). The main block was confirmed by the
file's own arithmetic: `Boone Value == FP_ADP − JB Rank` to **max error 0.00 across n=182**, and
the same for `4for4 Value`. This is the check that would have caught doc 50's 2025 column error.

## THE RESULT — POOLED n=377

Question: **does disagreeing with the market predict beating the market?** Spearman of
(ADP rank − source rank) against realized surplus over ADP expectation.

| source | weighted hit | ρ pooled | 95% CI | 2022 | 2025 | verdict |
|---|---|---|---|---|---|---|
| **Claude VOR** | **63.6%** | **+0.213** | **[+0.116, +0.302]** | +0.207 | +0.221 | **EDGE** |
| 4for4 / Paulsen | 50.2% | +0.055 | [−0.045, +0.153] | +0.017 | +0.111 | none |
| ESPN raw points | 43.7% | +0.094 | [−0.006, +0.196] | +0.162 | +0.060 | none |
| Justin Boone | 35.8% | −0.063 | [−0.165, +0.036] | −0.079 | −0.047 | none (negative both years) |

**Pat Fitzmaurice, 2022 only: ρ +0.101, CI [−0.051, +0.239], weighted 52.1% — the best human
score recorded, and still short of significance.** FantasyPros ECR 2022: ρ −0.012, weighted 50.6%
— the consensus is exactly a coin flip, which is what "vanilla" looks like when measured.

**The VOR model is the only source whose interval clears zero, and it lands in nearly the same
place in both seasons (+0.207, +0.221).** That stability is what separates an edge from a good year.

## THE STRUCTURAL FINDING — QUARTERBACK, AND ITS INSTABILITY

Share of all positive surplus by position:

| season | RB | WR | QB | TE | QBs in top 10 by surplus |
|---|---|---|---|---|---|
| 2022 | 30% | 33% | **23%** | 14% | **5 of 10** (Mahomes, Hurts, Burrow, Allen, Cousins) |
| 2025 | **46%** | 22% | 15% | 17% | 3 of 10 |

Mean QB surplus: **2022 +27.0 · 2025 −25.5.**

The mechanism is real and permanent: ADP is built on standard scoring, this league pays six per
passing TD, so quarterbacks are structurally underpriced by the market. **But the size of the
payoff swings hard.** In 2022 the VOR model had Mahomes 10th against ADP 34 and Allen 4th against
23 — enormous. In 2025 the same edge was negative. `[HYPOTHESIS]` — the QB discount is directional
but its magnitude is not forecastable from one season. **Do not encode a fixed QB bump.**

## WHAT THIS MEANS FOR MATT'S ORIGINAL CLAIM

He argued professional rankers with custom models should beat a platform's default projections.
Measured across two seasons and four humans (Boone, Fitzmaurice, 4for4/Paulsen, plus ECR):
**no human ranker beat the market at a level distinguishable from chance**, and the best of them
(Fitzmaurice +0.101) still had an interval crossing zero.

**But the finding that actually matters is not about the humans.** ESPN's *raw projected points*
also fails (+0.094, crosses zero). What works is the **position adjustment applied to those same
projections** — VOR moves the weighted hit rate from 43.7% to 63.6%. The edge in this project has
never been the projection source. It is the scarcity math on top of it.

## LIMITS
1. n=377 player-seasons, 2 seasons, 1 league's scoring. Fitzmaurice appears in one season only.
2. The VOR model is derived from ESPN projections, so "VOR beats ESPN raw" measures the adjustment,
   not an independent forecast. Against the human rankers the comparison is clean.
3. A published top-200 is not how an analyst actually drafts. This measures list order only.
4. 2022 used FantasyPros ADP, 2025 a nine-site average — not the identical market definition.
5. Surplus is measured against a fitted log curve of realized VOR on ADP rank; a different
   expectation curve would shift individual surplus values, though not the rank correlations.
