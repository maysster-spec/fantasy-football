# 49 — RED TEAM CHUNK 1 OF 7: SCORING CONVERSION
**Aug 25, 2026.** Run by an isolated adversarial reviewer (fresh context, read-only, no knowledge
of why the code looks the way it does) against the ten pre-committed criteria in doc 48.
**Result: 7 CLEAN · 3 CONFIRMED DEFECTS · 0 cannot-verify.**

## THE FINDING THAT MATTERS MOST — AND IT IS NOT A DEFECT

**`proj_leaguepts` is ESPN's own `appliedTotal`, renamed. The `SCORING` map does not produce it.**

```python
# code_rebuild_spine_v5.py
s = s.rename(columns={... 'proj_2026':'proj_leaguepts' ...})
```
Max difference across all 700 rows: **0.0**.

This is correct, and it is better than recomputing — the pull hits the **league** endpoint
(`/leagues/21985`), so ESPN applies *this league's* settings server-side before returning the
number. Verified independently: reconstructing from `raw_stats` with the league map reproduces
`proj_2026` to **6e-9** for RB/WR/TE (n=396); a 4-point-passing-TD map is off by −23.74 for QBs,
which is exactly the error we would see if ESPN were returning default scoring. It is not.

**This corrects something stated to Matt in chat on Aug 25** — that the model "throws away their
points column and recomputes from raw stats." It does not. ESPN's number is already league-scored;
the map exists to *verify* it and to score historical actuals. The recomputation is a check, not
the source. Ja'Marr Chase hand-check: 119.709 receptions × 0.5 = 59.85 → total 277.6247, matching
`proj_leaguepts` to 4 decimals (full PPR would give 337.48, zero PPR 217.77).

## CLEAN (7)
**S1** all twelve weights correct · **S2** 2-pt conversions ARE included (167 of 201 draftable rows
carry stat 62, 157.0 points in total, max 5.38 Josh Allen) · **S3** return TDs disjoint from
rush/rec TDs, 68 players carry both and reconstruction stays exact · **S5** correlation 1.000 all
positions, MAD 0.000 for RB/WR/TE; the QB +0.093 residual is ESPN truncating each weekly score to
one decimal, appearing only in players with passing yards · **S7** kickers clean (0 of 32 rows
contain any offensive id) · **S9** half-PPR confirmed at 0.5 · **S10** INT and fumble signs correct.

## CONFIRMED DEFECTS (3), ranked by points distorted

### D1 — 2-point conversions are dropped from HISTORICAL ACTUALS
In *projection* lines ESPN supplies id **62** (total 2PT), and the map scores it. In
**`raw_actual_stats` id 62 does not exist** — 2022: 1 row of 549; 2024: 0 of 537. Actuals instead
carry the split ids **19 / 26 / 44** (2-pt pass / rush / rec), none of which are in the map.
**Impact: 135 of 1,086 skill player-seasons (12.4%), mean 2.74 pts lost, median 2.0, max 8.0**
(Kyler Murray 2022, Jameis Winston 2024).
**Blast radius: every backtest built on the actuals archive — docs 21, 40, 41, 44.**
**Fix:** add `19:2.0, 26:2.0, 44:2.0` **for actual lines only**. Adding them alongside 62 on
projection lines would double-count — verified: `62 == 19+26+44` exactly on projections (max
diff 1e-9). This closes the project's long-open item *"two-point conversions — 204 points sit on
the board unexamined."*

### D2 — the FantasyPros scoring omitted three components
The second-source comparison (doc 46) was scored in JavaScript in the browser and its formula
**omits ids 62, 101 and 102** while the Python path includes them. So every FantasyPros player is
understated relative to every ESPN player — a **one-signed** bias, not noise.
**Impact: mean 1.03 pts across 169 draftable skill players, max 5.47. By position: QB +2.62,
RB +0.79, WR +0.76, TE +0.49.**
**SMOKE TESTED — the live board is unaffected.** The 24 disagreement flags in `board_v8_2026.csv`
rest on gaps of 12.4–23.5 points; the largest correction is 2.64 (Kyler Murray 20.4 → 23.0).
**Zero flags change sign, zero players enter or leave the list.** `board_v8_2026.csv` and
`ESPN_prerank_with_ids.csv` stand as shipped.
**But doc 46's per-position gap needs adjusting:** the QB comparison was biased by +2.62 and the
TE gap by +0.49, so the reported "TE +5.0" systematic difference is closer to **+4.5** and the
"QB −0.2" is closer to **−2.8**. Direction unchanged; magnitude modestly overstated for QB.

### D3 — `verify_scoring` still passes vacuously, and overstates its own coverage
`raw = stat.get("stats") or {}` → `got = 0`; if `appliedTotal == 0.0` then `err = 0.0`, below the
`abs(err) > 1.0` threshold. **31 skill rows in the 2026 pull pass vacuously; 144 more are skipped
entirely (`cur is None`). Only 461 of 636 skill rows are substantively tested** — yet the script
prints that it reconstructs ESPN's total for *every* QB/RB/WR/TE in the pull.
This is the same mechanism that let the 2023 break ship green. Doc 47's Gemini brief already
specifies the fix (`is_empty_stat`); **it has not yet been applied to the coverage message.**

## LATENT, NOT SHIPPED
**S7 (D/ST):** 32 of 32 defense rows contain ids 101/102, so the offensive map returns a mean of
3.1 against a true mean of 92.0. Nothing is broken today only because `SCORING_CHECK_POS` excludes
D/ST and their points come from `appliedTotal`. **If anyone ever scores a defense with this map it
will be silently wrong by ~89 points.** Guard it in `code_kdst_guard` before that happens.

## NEXT
Chunk 2 of 7 — source acquisition (A1–A8). Catalog and protocol in doc 48.
