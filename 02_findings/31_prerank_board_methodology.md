# 31 — PRE-RANK FULL BOARD: METHODOLOGY
**Built 2026-08-23** from `board_edges_v6.csv` (captured 2026-08-20T08:14, built 2026-08-22).
Output: `prerank_board_full_v1.csv` (317 rows) and `prerank_names_only_v1.txt` (plain list, one
player per line, in rank order — paste order for ESPN's drag-and-drop custom-rankings tool,
which has no bulk import). This is a **complete ordered list**, not a divergence-from-ESPN diff
— supersedes the old `prerank_divergence.csv` in purpose but that file was left untouched.

## SORT LOGIC (mechanical, not judgment, except one override below)

1. **Skill positions (QB/RB/WR/TE, n=253):** sorted by `vbd` descending. VBD already uses the
   position-adjusted replacement levels in `constants_2026.csv` [SOURCED: constants_2026.csv,
   2026-08-20 — RB30=168.6, WR30=163.5, QB12=341.6, TE12=140.3], which is the closest on-hand
   proxy to the project's stated objective (expected starting-lineup points).
2. **D/ST (n=32) and K (n=32): hard-floored below every skill player**, sorted internally by
   `proj_leaguepts`, not VBD. [TESTED: 4.8 — 11-12 of 12 teams stream a D/ST every season;
   4.9 — ESPN ADP field-minus-ESPN median K +55.0, D/ST +33.2 vs QB +10.7]. VBD is not trustworthy
   for these two positions, so it is not used to rank them even internally.
3. **One manual override: Josh Allen.** Natural VBD rank was 14th overall. Moved to rank 9
   (immediately after the natural top-8 cluster) per **4.2 [TESTED]**: +24.2 ± 2.0 marginal
   points vs. Henry-tier at pick 8 specifically, best on both mean and p10, survival-to-pick-17
   ≈ 0.14, survival-to-32 = 0.00. Caveat carried forward unchanged from the finding: the edge
   lives inside a 7% band on one projection set (−10% → −0.6 vs Henry). Treated per Section 7's
   output contract as max-EV positioning, not a certainty. **This is the only hand-moved player
   on the board.** If the projection set is refreshed Sept 5 and the band moves against Allen,
   this override should be re-tested, not assumed to still hold.

## WHAT WAS DELIBERATELY LEFT OUT OF THE SORT

- **Consensus ranker columns already in `board_edges_v6.csv`** (Boone, Smyth, Harmon,
  Pianowski, Winks, Norris, FIELD, SHARP_RK) were carried through as reference columns only.
  Section 4.4 scopes consensus-divergence to RANKINGS MODE (editing ESPN's own default board),
  not to a from-scratch VBD ranking. Blending two differently-purposed metrics without testing
  the blend would itself violate Section 0's validation rule, so it wasn't done.
- **2026 analyst target/downgrade convergence** (from `rawanalystcalls.csv` /
  `analystbreakoutcalls.xlsx`) is in the `analyst_flag_UNSCORED_2026` column as an annotation
  only — **[HYPOTHESIS]**, not a rank driver. These are unscored 2026 podcast calls; per
  `27_model_offload_plan.md` only 2024/2025 calls are scoreable against actuals on file, 2026
  outcomes don't exist yet. 19 TARGET / 2 DOWNGRADE / 2 CONTESTED matches landed on the board.
  Some evident transcription noise in the source data (e.g. "Davian Wicks" → Dontayvion Wicks) —
  treat flags as a last-look nudge between otherwise-equal players, never as a reason to jump
  a tier.

## KNOWN STALENESS

Board does not yet reflect Aug 25 roster cuts or the Sept 5 (T-48h) projection/ADP refresh —
both are already on the standing Section 8 schedule. Rebuild after each.
