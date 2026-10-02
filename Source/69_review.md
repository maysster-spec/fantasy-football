# 69 — REVIEW: THE +8.6 PROVENANCE, THE SIMULATOR, AND PICK 8
**2026-08-28, written under the switched model, same session lineage.** Honesty note up front:
this run happened in the long chat, not a fresh one, so the anti-anchoring premise of the tasking
prompt is compromised. Mitigation: every verdict below is a computation on files, and the review's
main result is that **doc 68 — written by this same lineage hours earlier — was wrong** in its
central suspicion. That is some evidence the measurements, not the lineage, are driving.

---

## (a) TARGET 1 — WHERE +8.6 CAME FROM. RESOLVED: it is legitimate, and doc 68 was wrong.

**Doc 68's transcription-error suspicion is RETRACTED.** The three numbers are three documented
experimental conditions, not one number miscopied:

| number | source | condition |
|---|---|---|
| **+4.23** [+2.89, +5.58] | doc 54 original, `ruletest_summary_n300.csv` | N=300, noise `sd=0.30×eff_pick` |
| +8.1 [+6.1, +10.2] | doc 55 §B1 re-run | N=200, corrected noise `sd=0.30×min(ADP,70)` |
| **+8.6** [+6.5, +10.8] | **doc 57 line 87**, post-fix head-to-head | N=200, corrected noise + fixed rollout shortlist bug |
| +12.97 (unpaired mean diff) | `risk_summary_w22.csv` | different sim (`OPP_WINDOW=22`, doc 55 config) |

`02b_LEDGER_CORRECTIONS_v5.md` line 48 confirms the chain: "+8.6 (doc 54, re-verified doc 57)."
The adjacency to |−8.648| was a coincidence.

**Recomputed from the raw 300 per-sim rows, not the summary:** paired R6−R2 mean **+4.234**,
95% CI **[+2.86, +5.61]**, win-rate 0.643. The shipped summary reproduces exactly. Paired SE is
0.70, so N=300 resolves effects ≥ ~1.4 points — the design is adequate.

**The dollar reading verified:** $160.15 − $144.9625 = **+$15.19**, and `PAYOUT` at
`code_league_sim.py` line 12 is the §2 table exactly. Two caveats doc 68 missed: (1) by device
mtimes, `risk_summary_w22.csv` (Aug 27 ~04:37, same minute as doc 55) **predates the doc-57
shortlist fix** (Aug 27 ~12:15); the fix moved the points head-to-head by +0.5, so the dollar
figure is approximately right, not exact. (2) No CI is attached; doc 55's paired CIs on same-sized
contrasts run ±$13–19, so **+$15.19 is a point estimate whose interval plausibly touches zero.**

**(c-of-Target-1) "The board is worth six times the rule" survives** within-config: 24.45 / 4.23
≈ 5.8× in the N=300 run. Do not mix configs when quoting it.

## (b) TARGET 2 — SIMULATOR AUDIT. The effect stands in direction; the magnitude is config-bound.

1. **Lookahead advantage is real but bounded and admitted.** The rollout's inner expectation uses
   *fresh draws* of the same opponent generator (no oracle leakage — doc 57 already killed the
   one concrete circularity claim raised against `run.py`, its §175). The structural issue is that
   in-sim opponents are exactly as predictable as the rollout assumes; real managers are less so
   (doc 54, Limit 3). **The measured anchor for magnitude sensitivity: the same comparison moved
   +4.2 → +8.6 (≈2×) purely from changing the noise spec.** Per §0.2 I assert no further number.
2. **Circularity: the rollout optimises the scoring function by construction.** All seven rules
   are scored identically, so the race is fair *as a race*; what it proves is "best at this
   objective in this sim." §0.3 moved the objective to dollars — and in dollars the direction
   holds (+$15.19 point estimate, unresolved CI). So: keep the engine; do not quote the points
   edge as if it were a resolved dollar edge.
3. **§4.13 reconciled — they measure different things. Verified in code**, not argued:
   `code_decompose_luck.py` drafts with `RULES['R6 rollout']` on every one of its 45 draft
   realisations. Its "spread ≈ 0" is variance *across drafts under one fixed rule*. §4.10 is a
   *mean shift between rules*. A rule can shift the mean while realised-draft-vs-realised-draft
   differences stay noise. No contradiction; both stand.

**Draft-night impact of Targets 1–2: none.** The rollout ships either way. The correction is to
how §4.10's edge is *described*: "+4 to +9 points depending on noise spec, direction stable,
worth ~$15 (unresolved) of expected payout."

## (b) TARGET 3 — PICK 8. THE 0.14-vs-0.70 DISPUTE IS RESOLVED BY THE DRAFT HISTORY.

The dispute was a fact question about Snyder, and `draft_history_2021_2025.csv` answers it:

| year | Allen went | to | Snyder's behaviour |
|---|---|---|---|
| 2021 | overall 21 (2.21) | **Snyder** | took him |
| 2022 | overall 23 (2.23) | **Snyder** | took him |
| 2023 | overall 21 (2.21) | **Snyder** | took him |
| 2024 | overall 13 | Ray | **sniped 2 picks before Snyder's 2.15**; Snyder pivoted to Nacua |
| 2025 | **overall 1 (1.01)** | **Snyder** | **paid the #1 overall pick** |

**Four-for-four when Allen was available at his turn; the one miss was a snipe; the next year he
paid the maximum possible price.** Doc 08's 0.70 is "pure ADP" — it deliberately excludes exactly
this record. Whatever doc 21 argued against q≈0.85, the revealed-preference evidence says 0.85 is
if anything **conservative**, and in 2026 Snyder picks at **9 and 16 — two cracks before Matt's
17.** Second, league-local market: in five drafts Allen has **never passed overall 23** (median
price 21, trend earlier: 13, then 1). The national-ADP survival in `survival_v9.csv` (p17 = 0.78)
is a no-Snyder number and overstates this league even before Snyder.

**Planning number: survival to 17 ≈ 0.14. Allen is a pick-8 decision or he is nobody's.**

What remains genuinely open is **value, not survival**, and the directive is right to forbid a
computed answer: §4.2's **+24.2 ± 2.0 over Henry** (which already embeds q=0.85) is the max-EV
case; the ±30-point QB-replacement band is the max-floor case — if QB12 realises at the +30 end,
Allen's ~80-point VBD compresses toward ~50 and an elite RB/WR at 8 with QB at 65+ (the
Snyder-proof tier) is defensible. **Max-EV: Allen at 8. Max-floor: Taylor / St. Brown at 8.**
The windows are unchanged: if Allen is taken at 8, pick 17 becomes pure best-RB/WR and the long
17→32 gap holds no QB temptation until 65.

## (c) FOUND, UNASKED

1. **§4.10's magnitude has never been measured under the FINAL noise model.** +8.6 was run under
   `sd=0.30×min(ADP,70)`; doc 60 then replaced that with the affine `0.111×ADP+5.40` (RMSE 0.89
   vs 3.06). Direction is robust across three specs; the shipped number is from a superseded one.
2. **Directive §5 is wrong about its most predictable manager:** "Josh Allen in 3 of 3" is
   actually **4 of 5, with the miss a two-pick snipe, followed by 1.01.** The correction
   *strengthens* the §4.2 read.
3. **`survival_v9.csv` is a trap of the doc-63 class:** its p17 = 0.78 for Allen is the no-Snyder
   market number and flatly contradicts §4.2's 0.14 to anyone who opens the file cold. It needs a
   header note naming the overlay it excludes.
4. `risk_summary_w22.csv` predates the doc-57 fix (item (a) caveat 1).

## (d) COULD NOT CHECK

Re-running the rule race under the affine noise model (hours of compute; not needed to ship, and
outside the no-re-derivation boundary I chose to respect). Doc 21's actual argument against
q≈0.85 — unread; the draft-history facts supersede it for the decision, but I did not verify its
content. Real-manager transferability of the opponent model — measurable only on draft night.
The exact N behind `risk_summary_w22.csv` — the file does not state it (doc 55 implies ~400).
