# 57 — RED TEAM CHUNK 3 OF 7: REPLACEMENT AND VBD (V1–V7)

> **BANNER, 28 Sept 2026 (doc 435).** Two numbers born here are dead: the D/ST defect sized at **"78 points" measured at +0.26** (doc 59, directive §0.2), and the rollout's **"+8.6" is a superseded spec; quote the range** (§4.10, docs 68 to 70). Kept as a dated record.
**Aug 27, 2026.** Five confirmed defects, **one of them shipping in the file already injected into
the ESPN draft room.** The adversarial agent's biggest claim — a 78-point loss — was measured
directly here and is **0.26 points, CI [−0.99, +1.52]**. Both halves of that matter.

---

## THE ANSWER, IN THREE LINES

1. **`ESPN_prerank_with_ids.csv` had all 26 kickers ranked ahead of the best defense.** If Matt
   times out at pick 152 — the D/ST slot — ESPN autodrafts a kicker. **Fixed and rebuilt.**
2. **Both engines used a WR replacement level 5.0 points too high**, inherited from a 200-row
   export the ledger itself records as 39% fabricated. **Fixed.**
3. **The rollout shortlisted future picks by raw projected points across positions** — the exact
   pattern this project banned. Real defect, correctly identified, **but its measured cost is zero.**

---

## RECONCILIATION — ALL SEVEN ROWS CARRY EXACTLY ONE VERDICT

| id | constraint | verdict | evidence |
|---|---|---|---|
| V1 | starter counts match the league | **CONFIRMED DEFECT (documentation)** | No code in the pipeline computes the cutoffs. `code_integrity.py:30` carries bare literals `{'RB':(30,168.6),'WR':(30,163.5),'QB':(12,341.6),'TE':(12,140.3)}` with no derivation. The generating script `code_rebuild_spine_v5.py` is not in the shipped set. **The numbers are defensible; the absence of the arithmetic is the defect** |
| V2 | pools exclude nulls/zeros/synthetic | **CLEAN** | 0 null, 0 zero, 0 synthetic rows within ±5 ranks of any cutoff. Nearest synthetic is RB #117 against a #30 cutoff. All 31 zero-projection rows sit at ADP ≥ 169.93 |
| V3 | K/D-ST carry no cross-position VBD | **CONFIRMED DEFECT (spine only)** | `code_universe_v5.csv` ships all 64 K/D-ST rows with live `vbd` — Broncos D/ST +32.5 ranks **41st overall**, Aubrey **51st**. `apply_kdst_guard` operates on `df.copy()` and is never persisted. **Does not reach `board_v7_2026.csv`** (0 K/D-ST rows there) |
| V4 | the FLEX slot is priced, and the split is stated | **CONFIRMED DEFECT (documentation)** | The string "flex" appears nowhere in the ledger or in any VBD code — only as `FLEX_OK` in the two lineup scorers. RB30/WR30/TE12 implies a 6/6/0 split of the 12 FLEX slots. **Arithmetically closed, never written down** |
| V5 | replacement never borrowed across sources | **CONFIRMED DEFECT** | `board_v7_2026.csv` was built on **341.603 / 168.589 / 163.540 / 140.295** (recovered as `proj − vbd`, constant to 6.6e-07). Both engines and directive §4.1 use **341.7 / 168.0 / 168.5 / 137.7** from a 200-row v2 export. **WR is 5.0 points too high** |
| V6 | no cross-position ranking on raw points | **CONFIRMED DEFECT ×2** | (a) `code_live_engine.py` `_finish`: `idx[np.argsort(-self.proj[idx])]` — cross-position, and 14 QBs project above the best RB. (b) `code_build_board_v7.py`: K and D/ST sorted **together** on raw points |
| V7 | byes do not enter VBD | **CLEAN** | `vbd == proj_leaguepts − repl[pos]` exactly, max residual 6.6e-07 over 592 rows. `bye` appears only in lineup construction and a display column |

**Coverage: 7 of 7. No holes.**

---

## THE ONE THAT WAS ABOUT TO COST A ROSTER SPOT — V6(b)

```python
kdst = pool[pool['pos'].isin(STREAMED)].sort_values('proj_leaguepts', ascending=False)
```

Kickers project 121.7–171.7. Defenses project 55.4–128.4. Sorted together, **the first D/ST lands
at row 27 of 64**, and that ordering became the tail of the file injected into ESPN:

| | before | after |
|---|---|---|
| first D/ST prerank | **507** | **481** |
| first K prerank | **481** | **513** |

ESPN's autodraft walks the prerank list in order. Matt drafts **D/ST at 152 and K at 161**
(directive 2.1b). With the old file, a timeout at 152 takes **Brandon Aubrey**, and he ends the
draft with two kickers and no defense.

**Fixed in two places:** `ESPN_prerank_with_ids.csv` rebuilt with D/ST 481–512 and K 513–544, and
`code_build_board_v7.py` patched so a rebuild cannot reintroduce it. Contract re-asserted: 544
rows, `ESPN_ID` unique and non-null.

> **Matt must re-inject the prerank file.** The version currently in ESPN is the broken one.

---

## THE ONE THAT LOOKED HUGE AND ISN'T — V6(a)

The audit reported the inner rollout shortlisting future picks on raw projected points, traced a
draft where it "burns picks 17 and 32 on QBs in every realisation," and priced it at
**≈78 points, 5.6 per week — 12× the spread directive 4.10 uses to separate strategies.**

**The defect is real.** `code_live_engine.py` and `rules.py` both did
`idx[np.argsort(-sim.proj[idx])][:cand_k]` inside `_finish`, spanning all four positions. It is
`ERROR_PATTERNS` V6 — the +82-pick error — recurring in code **I wrote this week**.

**The severity claim is wrong.** It measured the change in the rollout's own `roll` *estimate*,
not the change in *draft outcomes*. Fixing the shortlist naturally raises the simulated
continuation value; that number is only ever used to rank candidates against each other, and the
bias was common to all of them, so it cancelled.

**Measured properly — paired, same seeds, buggy rollout versus fixed rollout, N=200:**

```
fixed 1470.1   buggy 1469.8
TRUE COST OF THE V6 DEFECT: +0.26 pts   CI [-0.99, +1.52]   fixed wins 43%
```

**Zero.** `[TESTED]`

The fix ships anyway — it is free, it is correct, and a banned pattern left in place will bite in
a configuration where the bias does not cancel. But **doc 54's numbers do not change**: re-running
the head-to-head post-fix gives the rollout **+8.6 [+6.5, +10.8]** over static VBD, against +8.1
before. One thing did change: **deeper search is no longer worth anything** (+0.45,
CI [−0.77, +1.65], was +1.5) — so the live engine can run the cheaper settings.

> This is the second time in two chunks that an adversarial agent's *severity* was wrong while its
> *finding* was right. Both times the correction came from running the experiment rather than
> reading the code. **Treat agent-reported magnitudes as unverified until measured.**

---

## V5 — THE REPLACEMENT LEVELS THE ENGINES USED WERE NOT THE BOARD'S

| source | QB | RB | **WR** | TE |
|---|---|---|---|---|
| `board_v7_2026.csv`, recovered from its own `vbd` | 341.603 | 168.589 | **163.540** | 140.295 |
| `code_live_engine.py`, `engine.py`, directive §4.1 | 341.7 | 168.0 | **168.5** | 137.7 |

The v2 numbers come from a 200-row undated export that `02_findings_ledger.md` F42 records as
**39% fabricated** (195 of 494 rows filled with a linear ramp), and the ledger already logs a prior
incident of this exact shape: *"skewed WR replacement 10 pts low vs RB 2.8, biasing every RB-vs-WR
comparison."* The ledger's own claim that *"all four F1 replacement levels reproduce exactly"* is
**false against the shipped board.**

Directive §4.1's headline VBD figures are stale by the same amount: Nacua +126.5 → **+131.3**,
McBride +50.4 → **+47.6**, Bowers +53.3 → **+51.2**, Andrews +2.9 → **0.0**.

**Impact is smaller than it looks and I want to be precise about why.** The `delta` column is
unaffected — the replacement term cancels inside `MV(p) − E[MV(best at same position)]`. It bites
only where a lineup slot goes unfilled and the waiver level is used, and wherever §4.1's numbers
are quoted. **Fixed in both engines.**

---

## V1/V4 — THE CENTRAL QUESTION, AND WHY THE OBVIOUS FIX IS WRONG

RB30/WR30/QB12/TE12 implies a **6/6/0** split of the 12 FLEX slots: 24 base RB + 6, 24 base WR + 6,
12 base TE + 0. It closes exactly. Nothing is orphaned or double-counted. But it is written down
nowhere, which is the V1/V4 defect.

The agent's recommendation was to replace the literals with a flex allocation computed at build
time. **Do not do this.** Computed the same way on every basis available:

| basis | RB / WR / TE | implied cutoffs |
|---|---|---|
| 2026 projected | **6 / 6 / 0** | RB30 WR30 TE12 |
| 2022 projected | 6 / 6 / 0 | RB30 WR30 TE12 |
| 2022 **actual** | 5 / 7 / 0 | RB29 WR31 TE12 |
| **2024 projected** | **1 / 11 / 0** | **RB25 WR35** TE12 |
| 2024 **actual** | 4 / 8 / 0 | RB28 WR32 TE12 |

A rule that refits annually off projections would have set **RB25/WR35 in 2024** — a ten-rank
swing driven by noise in one season's projection, not by anything real. **RB30/WR30 is a stable
central estimate and should be kept as a documented constant, with the uncertainty stated: the
honest range is RB28–31 and WR29–32, worth roughly ±1.5 VBD per player on RB-versus-WR.**

I could not reproduce the agent's 5.86-point bias figure; computed on the keeper-depleted board the
same shift is **2.6 points** (RB30→31 is +1.2, WR30→29 is −1.4). Its number was computed on an
unstated pool.

**TE12 is the one robust cutoff** — zero FLEX slots go to TE on every basis, both historical years
and 2026. **QB12 is exact by construction**, but carries the largest *level* uncertainty: the gap
between projected and realised replacement at rank 12 was +30.8 in 2022 and −30.2 in 2024, roughly
double RB's or WR's. **Any QB-versus-RB call at pick 8 (directive §4.2, Josh Allen) inherits a
±30-point unmodelled term.** That is the most important thing in this section.

---

## EXTRAS WORTH ACTING ON

**EXTRA-1 — the replacement-level integrity check has never run.** `code_integrity.py:37` reads
`u['TOT']`; the v5 spine calls that column `proj_leaguepts`. Executed: `KeyError: 'TOT'`. It also
defaults to `REPLACEMENT_V4` while both engines used `REPLACEMENT_V2` — so even repaired it would
have green-lit a spine the engines disagreed with. **This is `ERROR_PATTERNS` H1: a guard that
does not fire on the defect that motivated it.**

**EXTRA-3 — the engines cap Matt at 2 QB and 2 TE; the league allows 3.** Defensible as an
opponent prior, wrong as a constraint on his own legal moves. It was also the only thing stopping
the V6(a) QB cascade. Now that V6(a) is fixed, worth re-testing whether the cap binds at all.

**EXTRA-7 — `WAIVER = 0.80` is an uncommented scalar** applied to levels that differ by 2.4×. It
subtracts 68.3 season points from QB replacement and 27.5 from TE — a **40.8-point differential**
change to cross-position comparisons. Unswept.

**EXTRA-8 — the two engines score rosters differently.** `rules.py` applies a per-week
availability draw; `code_live_engine.py` `_lineup` applies byes only, while its docstring claims
"injury- and bye-adjusted." Roster values from the two are not comparable.

**REFUTED — EXTRA-2.** The agent reported the rule-comparison engine scoring Pickens at 155.0
instead of 198.68, "differentially penalising WR-opening strategies." **False.** `run.py` passes
`Sim(b, 198.68, rng)` on every construction; the 155.0 default in `load()` is returned into a
discarded variable and never reaches a simulation. Directive §4.10 is unaffected.

---

## WHAT THIS CHANGES

1. **Re-inject `ESPN_prerank_with_ids.csv`.** The copy in the ESPN draft room ranks 26 kickers
   above every defense.
2. **Update directive §4.1** to the board's real levels: RB 168.589 · WR **163.540** · QB 341.603 ·
   TE 140.295, and the elite VBD figures with them.
3. **Write the flex split into the directive as a documented constant** — RB30/WR30 = a 6/6/0
   split — with the RB28–31 / WR29–32 uncertainty band. **Do not make it self-refitting.**
4. **Carry a ±30-point uncertainty band on QB replacement** into any QB-versus-RB decision at
   pick 8.
5. **Repair `code_integrity.py`** — column name, and point it at the levels the engines use.
6. **Persist the K/D-ST guard**, or stop shipping `vbd` on those rows in the spine at all.

## LIMITS

1. One adversarial agent this chunk, with adjudication and direct measurement here rather than a
   second agent. The paired V6 cost test is a stronger refutation than a second opinion would have
   been, but it is one reviewer plus me, not two independent ones.
2. `code_rebuild_spine_v5.py` — the script that actually sets the replacement levels — was not in
   the audited set. V1's verdict rests on reverse-engineering the levels from `proj − vbd`.
3. The flex-split analysis uses only two seasons with usable actuals. 2023 is dead and 2021/2025
   lack the joins.
4. The V6 cost test measures one board, one draft slot, one opponent model. "Zero here" is not
   "zero everywhere" — which is why the fix ships.

## §7 CLOSE-OUT

**Top 3 assumptions:**
1. **`proj − vbd` recovers the true replacement levels.** *Verified:* constant within position to
   6.6e-07 across 592 rows. As close to certain as anything here.
2. **The 6/6/0 flex split is right for 2026.** *Invalidated by:* the 2024 pool, where the same
   method gives 1/11. The defence is that 2024's projected split disagrees with its own actual
   split (4/8), so the method is noisy, not the constant.
3. **Fixing V6(a) is free.** *Verified* at +0.26 [−0.99, +1.52] on this board. Would be invalidated
   by a configuration where QB and RB value curves cross differently — a superflex league, or a
   different scoring system.

**What would most improve this:** `code_rebuild_spine_v5.py` in the audited set, so V1 can be
closed on the actual generating code rather than on reverse-engineered constants.
