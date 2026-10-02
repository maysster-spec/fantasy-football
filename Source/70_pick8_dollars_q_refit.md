# 70 — PICK 8 IN DOLLARS, SNYDER'S q RE-FITTED, AND WHAT +8.6 IS WORTH ON THE CLOCK

> **BANNER, 28 Sept 2026 (doc 435).** The **"+8.6"** in this title and body is a superseded spec (§4.10); quote the range, never the point. Kept as a dated record.
**2026-08-28, amended same day: two corrections from Matt — the §4.2 comparator identity and the band-cancellation argument — both verified below. All numbers are new paired measurements run this session under the FINAL
doc-60 affine noise (`sd = 0.111×ADP + 5.40`), v5 replacement levels, empirical outcome pool
(324 player-seasons), full league sim with H2H standings and the §2 payout table.**
Harness: forced-pick-8 arms, identical opponent boards, per-player common random numbers,
paired seeds. N=600 per configuration.

---

## 1. THE HEADLINE, RECONCILED (item 1)

**(a)** Under the final doc-60 noise spec the rollout-vs-static-VBD effect **has never been
measured — in points or in dollars.** Nearest measurements: +4.23 pts (N=300, original noise),
+8.6 pts (N=200, interim noise), +$15.19 (w22 config, pre-doc-57 engine, no CI).
**(b)** +8.6 is doc 57's post-bugfix N=200 re-run under the *interim* noise `0.30×min(ADP,70)`;
+4.23 is doc 54's original N=300 run under `0.30×eff_pick`. Both noise specs are superseded.
**(c)** **Directive §4.10's headline is stale.** It quotes a superseded-noise measurement as
current. Direction (rollout first, VONA/penalty lose) is stable across all three specs; the
magnitude is not current.

## 2. SNYDER'S q, RE-FITTED AND PROPAGATED (item 2)

**The record:** at his own turn with Allen available, Snyder is **4-for-4** (2.21, 2.23, 2.21,
and **1.01 overall in 2025**). 2024 is *censored*, not a failure — Allen never reached his pick.

| estimator | q | 95% interval |
|---|---|---|
| MLE | 1.00 | — |
| Laplace | 0.833 | — |
| **Jeffreys Beta(4.5, 0.5)** | **0.90** | **[0.56, 1.00]** |
| Clopper-Pearson (frequentist) | — | [0.40, 1.00] |

n=4 is small and the intervals say so. But every estimator sits at or above the old 0.85 —
**doc 08/21's push toward 0.70 is refuted by revealed preference, including a #1-overall price.**

**Survival to pick 17, measured in-sim under the final noise (not the old analytic 0.14):**

| opponent window | q=0.55 | q=0.90 | q=1.00 |
|---|---|---|---|
| w8 | 0.110 | **0.032** | 0.000 |
| **w22 (directive §5)** | — | **0.000** | 0.000 |

**§4.2's "survival ≈ 0.14" does not survive: it falls to ≈0.03 (w8) or ≈0.00 (w22).** Under the
directive's own opponent model, VBD-greedy opponents take Allen by pick 16 even *without* Snyder.

**Blast radius (§3: enumerate, don't spot-patch):**
1. §4.2 survival 0.14 → 0.00–0.03. Allen is a pick-8 decision or nobody's — now stronger.
2. Doc 08's "0.70 on pure ADP" — dead under both windows; national ADP never applied here.
3. `survival_v9.csv` p17=0.78 — a no-Snyder market number; needs its header caveat (doc 69).
4. Other QBs before 17: unaffected — §5: Snyder is the *only* early-QB manager in the 8→17
   window and his QB is Allen. After 17: conditional on Snyder holding Allen, his later QB demand
   vanishes → second-tier QB survival past 22 rises. Direction only; not measured.
5. The rule race and §4.13 tilts: paired designs where every arm faces the same Snyder draw —
   rule *rankings* are insensitive to q by construction. No re-run needed.
6. §4.12/§5's "q≈0.85" line → update to "0.90 [0.56, 1.00], 4-for-4 when available."

## 3. PICK 8 IN DOLLARS (item 3) — AND A VALIDATION FAILURE THAT MATTERS MORE

**Validation first — and Matt's correction sharpens the diagnosis.** I re-ran §4.2's own
comparison inside the harness — Allen@8 vs forced-Henry@8. §4.2 claims **+24.2 ± 2.0** for
Allen; this harness gives **−11.0 ± 8.5** (w8, midpoint). Matt identified why §4.2's frame was
mis-posed from the start: **Henry's eff_pick is 19.10 — he is the pick-17 alternative, not the
pick-8 alternative** (board verified: Henry 19.10 / vbd +95.38; St. Brown 8.30 / **+101.33**;
Allen 21.9 / +80.31). Forcing Henry at 8 embeds an ~11-pick reach into the baseline, and Allen's
+24.2 was measured against that handicapped comparator. The main experiment below already uses
the correct alternative — the best-non-QB arm takes St. Brown 120/120 — so §4.2's number is not
merely non-transferring; **its comparison was against the wrong player.**

**The main experiment.** Allen@8 vs best-non-QB@8 (it takes Amon-Ra St. Brown 120/120; its QB
arrives at ~65, Jayden Daniels 72%, else Stafford-tier), R2 drafting both arms thereafter,
q=0.90, paired, N=600, across the ±30 QB-replacement band:

| δ (QB band) | E$[Allen@8] | E$[wait] | **Δ$ (A−B), 95% CI** | P(1st) A/B | P(top6) A/B |
|---|---|---|---|---|---|
| **−30 (QB scarce)** | $154.47 | $141.86 | **+12.61 [−4.0, +29.2]** | .173/.168 | .687/.665 |
| **0 (midpoint)** | $126.27 | $139.57 | **−13.30 [−28.6, +2.0]** | .125/.160 | .632/.667 |
| **+30 (QB plentiful)** | $108.26 | $139.41 | **−31.15 [−46.5, −15.8]** | .107/.155 | .573/.672 |

(w8 shows the same pattern, stronger: −38.5 [−55.5, −21.5] at the midpoint.)

**MATT'S SECOND CORRECTION, TESTED AND CONFIRMED: the ±30 band, read as §4.2 states it — a
band on the QB replacement LEVEL — cancels in the A−B contrast and must not hedge this
decision.** His arithmetic: both paths start exactly one QB; a level shift moves both sides
equally. Simulated (level mode: δ applied to ALL QBs including Allen, plus the fill, N=200
paired): mean Δpts across δ ∈ {−30, 0, +30} = −12.12 / −11.81 / −11.48 — **flat to within 0.6
points across the whole ±60 sweep**, invisible against a ±9 CI. Cancellation is exact in the
pre-form ledger exactly as Matt computed; the empirical form multipliers and the 0.80 waiver
fraction leak only a mean-zero per-seed residual. **The δ table above therefore does NOT measure
§4.2's band — it measures a *relative* QB-tier-vs-Allen realization axis, for which the ±30
width has no evidentiary basis in the project.** It stays as an unanchored sensitivity, nothing
more.

**Verdict, un-hedged accordingly: the midpoint row is the answer. Δ$ = −13.30 [−28.6, +2.0] —
wait leans ahead on every metric (mean dollars, P(1st) .160 vs .125, P(top6) .667 vs .632, p10),
and none of it is resolved at 95%. A coin flip, leaning wait.** Allen-at-8's remaining case
must be argued on an axis this project has not measured (relative QB compression), not on
§4.2's band.

**One bias still named against Allen:** the outcome pool is position-blind by ADP band — the
1–24 band contains exactly **1 QB and 23 RBs**, so Allen's draws inherit RB bust risk (form sd
0.281). It equally infects doc 55's dollar tables. The wait arm being WR-first (vs the sim
family's RB-first preference) is the opposing bias. Neither is resolvable with 324 player-seasons.

## 4. WHAT OVERRIDE COST IS MATERIAL (item 4)

Measured here, 1 point ≈ **$1.2–1.5** near Matt's part of the standings curve. The N=300 race
resolves rule differences of ~±1.4 pts; the entire rollout-vs-static season edge is +4-to-+9 pts.
**So: `cost vs #1` under ~3 pts — inside the model's own noise, override freely. 3–10 pts — the
number is real but modest (≈$4–15); your read may legitimately win. Over ~10 pts — that one
override exceeds the engine's whole season-long edge; take the engine's pick.**

## FOUND, UNASKED

- `code_league_sim.py` still ships **v4 replacement levels** (341.7/168.0/168.5/137.7) in its
  waiver fill — the stale numbers §4.1 corrected. Patched for these runs; the file in `Source\`
  is unfixed. Symmetric across teams, so contrasts move little; absolute dollar tables less so.
- `OPP_WINDOW` defaults to 8 in code while directive §5 says ~22 — config drift; doc 55's runs
  set 22 explicitly, the doc-54 race ran at 8.
- The position-blind outcome pool (above) is the binding data limitation on every dollar number
  this project produces. A position-conditioned pool needs more than 324 player-seasons.

## COULD NOT CHECK

Re-running the full §4.10 race under the final affine noise (compute, and the no-re-derivation
rule); §4.2's original config in its own frame; whether a position-conditioned outcome pool
flips the pick-8 midpoint — the data to build one does not exist in the project.


---

## ADDENDUM (same day) — THE POOL-COMPOSITION RESIDUAL, MEASURED AND CLOSED

**Population: the outcome pool itself, 324 player-seasons.** QB (n=41): form sd **0.223**, form
mean **0.926**, gp 14.15. RB (n=109): form sd **0.387**, mean 0.971, gp 13.87. Variance ratio
RB/QB = **3.03** (Levene p=0.0023); games played does not differ (p=0.50). The residual was real —
**and it carries a lower QB form MEAN alongside the lower spread**, which cuts against Allen.

**Re-run with every QB (both arms, keeper QBs included) drawing from the QB rows** — N=1000
paired, δ=0, w22, q=0.90:

| pool | Δ$ (Allen@8 − wait) | P(1st) A/B | P(top6) A/B | p10 pts A/B |
|---|---|---|---|---|
| position-blind (original) | −13.30 [−28.6, **+2.0**] | .125/.160 | .632/.667 | — |
| **QB-conditioned** | **−23.86 [−36.12, −11.61]** | .142/.162 | .587/.685 | 1232/1254 |

**Sign: unchanged. The CI no longer spans zero — resolved AGAINST Allen in this model. The
recommendation upgrades from "wait, leaning" to "wait, resolved."** Caveat per §3: the QB pool
spans ADP 23–170 with only 8 QBs inside 48; whether *elite* QBs share the 0.926 form mean is
unmeasurable on this data (1 elite QB in band 1–24). Under no measured configuration does
Allen@8 win at the midpoint.

**PICK 8 IS CLOSED: best board player at 8, QB later. No further sensitivities.**
