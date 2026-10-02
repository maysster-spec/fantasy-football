# 41 — RED TEAM OF DOC 40. THE HEADLINE WAS HALF ARTIFACT, AND DOC 21 CONFLATED TWO VARIANCES.
**Aug 25, 2026.** Adversarial re-examination of `claude/40_multiyear_backtest_2022_2024.md`,
run at Matt's request on Opus. Reproduce with `code_backtest_redteam_v2.py`.
**Population: all 12 managers × 2022, 2024, 2025 = n=36 manager-seasons. Keepers held constant.**

---

## THE ANSWER, IN ONE LINE

**Doc 40's headline ("the rule beat only 2 of 24 manager-seasons") does not survive.** Roughly
half of that deficit was a policy defect — the rule spent premium picks on kickers and defenses,
which this project's own §4.8 says is worthless. Corrected, and with 2025 added on identical
code: **the rule beats 18 of 36 manager-seasons, mean delta −12.8, bootstrap 95% CI
[−89.5, +62.3] — which includes zero.** The honest verdict is **no measurable difference between
the value rule and real managers**, not "the rule loses."

---

## RT-1 — THE FATAL DEFECT: THE RULE DRAFTED KICKERS AND DEFENSES FIVE ROUNDS TOO EARLY

**[TESTED]** Across the 24 manager-seasons in doc 40, the greedy policy made 48 K/D-ST
selections:

| metric | observed | directive says |
|---|---|---|
| median overall pick used on K/D-ST | **75** | §4.7: median first D/ST is **round 12** (pick ~133); first K round 11+ in **95.8%** of team-seasons |
| taken inside pick 108 (round 10) | **36 of 48** | — |
| taken inside pick 72 (round 6) | **20 of 48** | — |

In 2022 **all twelve managers** take Packers D/ST, between picks 49 and 75, because it survived
to those picks in the real draft and its VBD (proj − D/ST12) outranked every skill player on the
board. (Each manager's roster is simulated independently against real go-forward availability —
see Limit 3 — so the same player can be taken by more than one of them.)

> **Correction, Aug 25 verification pass:** this paragraph originally read "eight different
> managers … between picks 49 and 59." Recomputed from source it is **twelve managers, picks
> 49–75.** The error understated the defect; every other figure in this document reproduced
> exactly on re-run. Logged as a caught error per directive §0.

**Why this happens:** D/ST replacement is the 12th-best of a **32-team** pool, so the top
defenses carry large positive VBD that competes with round-5 skill players. Kicker replacement
behaves the same way. **Directive §4.8 already establishes that this value is not realizable** —
11–12 of 12 teams stream a D/ST every season. A policy that spends pick 55 on a defense is not
"the project's value rule"; it is a naive VBD greedy that the project's own findings forbid.

**Doc 40 therefore tested a strawman.** So did doc 21 — the same policy is in
`code_backtest_redteam.py`.

### Cost of the defect

Re-running with one added constraint — **no K or D/ST before pick 121 (round 11)**, a faithful
encoding of §4.7 — and changing nothing else:

| | doc 40 as published (V0) | corrected (V1) |
|---|---|---|
| rule beat, 2022+2024 | **2 of 24** | **8 of 24** |
| mean delta | −221.1 | **−115.5** |
| vs Lobsinger 2022 | −242.0 | **+11.9 (rule now WINS)** |
| vs R Taylor 2022 | −253.9 | −42.4 |

**Mean gain from simply not drafting K/D-ST early: +105.6 points per manager-season. 20 of 24
manager-seasons improved.** Doc 40's specific claim that *"the rule lost to Lobsinger AND Taylor
in both years"* is **false in one of four cells** once the policy respects the league's own
observed behaviour.

## RT-2 — IS THAT JUST A DIFFERENT ARBITRARY CHOICE? NO — SENSITIVITY IS FLAT

Replacing one hand-set constant with another is the D6/A11 trap, so the deadline was swept
rather than assumed. Pooled n=36:

| K/D-ST deadline | rule beats | mean delta |
|---|---|---|
| none (doc 40) | 11/36 | −108.1 |
| pick 85 (~rd 8) | 13/36 | −67.6 |
| pick 97 (~rd 9) | 14/36 | −45.0 |
| pick 109 (~rd 10) | 16/36 | −29.7 |
| **pick 121 (rd 11, §4.7)** | **18/36** | **−12.8** |
| pick 133 (~rd 12) | 19/36 | +11.5 |
| pick 145 (~rd 13) | 19/36 | −34.4 |

Monotone through round 12 and stable from round 10 onward. **The conclusion is not knife-edge on
the exact deadline** — any realistic value produces the same qualitative answer.

## RT-3 — ALL THREE YEARS ON IDENTICAL CODE, WHICH DOC 40 NEVER DID

Doc 40 compared its own 2022/2024 numbers against doc 21's separately-computed 2025 figure.
Running 2025 through the same function removes that inconsistency. **2025 V0 independently
reproduces doc 21's headline count of 9 of 12 exactly** — a clean replication of the prior work.

| year | V0 beats | V0 mean | V1 beats | V1 mean |
|---|---|---|---|---|
| 2022 | 1/12 | −233.5 | 5/12 | −55.4 |
| 2024 | 1/12 | −208.8 | 3/12 | −175.6 |
| 2025 | 9/12 | +117.9 | 10/12 | **+192.5** |
| **pooled n=36** | **11/36** | **−108.1** | **18/36** | **−12.8** |

**V1 pooled bootstrap 95% CI on mean delta: [−89.5, +62.3]. Includes zero.**
Per A1 discipline the word is **no detectable difference**, not "loses" and not "wins."

**Note the K/D-ST defect is present in all three years**, so it does *not* explain why 2025 looks
good and 2022/2024 do not. That contrast is real and unexplained by this red team.

## RT-4 — THE DEEPEST FINDING: DOC 21 CONFLATED TWO DIFFERENT VARIANCES

Doc 21's central claim is that the rule is a **floor-raiser** — "outcome variance 14% of a real
manager's (sd 76 vs 202)" — and that Matt needs a ceiling-raiser instead. That number is
**within-year variance across the twelve managers**. It is not the only variance in play.

| | 2022 | 2024 | 2025 | spread |
|---|---|---|---|---|
| league actual, mean | 1675.8 | 1702.3 | 1684.7 | **26.5** |
| rule, mean | 1620.4 | 1526.8 | 1877.2 | **350.5** |

**Between-year sd: rule 181.4 · league 13.5. The rule's year-to-year swing is roughly 13× the
league's.**

Within a year, across managers, the rule's spread is lower in 2 of 3 years (2024, 2025) and
**higher** in 2022 (128.6 vs 104.1) — so even the original claim replicates only 2 of 3.

**Interpretation.** The rule does compress differences *between managers within a season* — it
hands everyone a similar roster. But its absolute quality is **hostage to how well that season's
projections happened to work**, and that varies enormously. Calling it a "floor-raiser" describes
the cross-manager variance while ignoring a cross-year variance an order of magnitude larger.
`[HYPOTHESIS]` — **the rule is not low-variance; it is a concentrated bet on projection quality,
and the 2025 result that started this whole thread is the good draw from that distribution.**
Falsifier: add 2021 and any future season. If the rule's yearly mean keeps swinging ±200 while
the league sits inside ±30, this is confirmed.

## RT-5 — WHAT SURVIVES DOC 40 UNCHANGED

- 2023 remains unusable — independently re-confirmed against the Aug 25 re-pull (below).
- 2024 remains the worst year for the rule even corrected (3/12, −175.6), and it is **not**
  because the league drafted unusually well that year — the league's mean is flat across all
  three years (1675.8 / 1702.3 / 1684.7). It is the rule that underperformed in 2024.
- The pick-by-pick concentration story in doc 40 (unforeseeable breakouts in 2024, injuries in
  2025) is unaffected by the K/D-ST correction.

---

## THE AUG 25 RE-PULL OF 2023 — STILL NOT USABLE

`espn_projections_2023_20260825.csv` (captured 07:22) **fixes the 0.0-vs-null defect** — empty
projections are now `NaN` rather than `0.0`, which is correct — but does **not** recover the data.

- `proj_2023`: **96** real values in 700 rows, only **19** inside ADP 169.
- McCaffrey, Hill, Chase, Kelce, Ekeler, Hurts, Allen, Lamb: **all still null.**
- **Of the 178 players drafted in 2023, exactly 18 carry a usable `proj_2023`.**

A VBD rule cannot run at 10% coverage. **2023 is confirmed dead for this test** — this is the
second independent confirmation, and the matter should be considered closed.

### REGRESSION INTRODUCED BY MY OWN FIX INSTRUCTION — A11, AGAIN

The new file also **lost 146 valid non-zero `actual_2023` values, 47 of them inside ADP 169**,
including Brandon Aubrey 179.0, Ravens D/ST 167.0, Cowboys D/ST 162.0, Justin Tucker 155.0.

**Cause, and it is mine.** `GEMINI_FIX_BRIEF_espn_pull.md` said to null any row lacking ≥3 keys
from the `SCORING` map, and to *"apply the same treatment to `actual_{season}`"*. The `SCORING`
map contains only offensive skill stat IDs. **0% of kickers and 0% of defenses have any key in
it** — they score through entirely different stat IDs — so the gate nulls every K and D/ST.
This is `ERROR_PATTERNS` **A11**: a rule fitted on one population (QB/RB/WR/TE) applied to the
whole class. The brief even carried `SCORING_CHECK_POS = {QB,RB,WR,TE}` and I did not gate on it.

**Corrected rule, verified against the Aug 24 file:** treat a stat row as empty only when it has
no keys beyond metadata ID `210` (games played):
```python
def is_empty_stat(stat):
    raw = stat.get("stats") or {}
    return len({int(k) for k in raw} - {210}) == 0
```
Measured: nulls **576** of 700 `proj_2023` (correct — the 435 stubs plus 140 empties), nulls only
**91** `actual_2023` instead of 264, and nulls only **16 of 86** K/D-ST rows instead of all 86.
This works for every position because it tests for *presence of data*, not for membership in an
offense-only scoring map.

---

## WHAT THIS CHANGES FOR THE DRAFT

1. **Do not carry "the value rule loses to good managers" into Sept 7 planning.** The measured
   result is no detectable difference, CI includes zero, n=36.
2. **Do not draft a D/ST or K before round 11.** This is now independently confirmed twice —
   §4.8 said the value is unrealizable, and this red team measures the cost of ignoring it at
   **+105.6 points per season**. It is the single largest effect found in this entire exercise,
   and it is a pure execution rule requiring no forecasting skill.
3. **The objective-function question is still open, but reframed.** The choice is not
   "floor-raiser vs ceiling-raiser." The rule's cross-year swing (sd 181) dwarfs its cross-manager
   compression (sd 62–129). Whatever is chosen for weeks 1–14 should be argued on projection
   quality, not on a variance property that only holds one way.

## LIMITS

1. n=36 manager-seasons, 3 seasons, one league. The pooled CI is wide precisely because of this.
2. Season totals, not weekly — the real objective function is weekly starting-lineup points.
   Unchanged from docs 21 and 40.
3. Each manager's rule-roster is built independently against real go-forward availability; twelve
   rule-drafters are not simulated competing for the same players. Unchanged from docs 21 and 40.
4. The K/D-ST deadline is a hard constraint, not an optimisation. A rule that prices streaming
   value properly would be better still; this only removes an error, it does not add skill.
5. 2022/2024 draft histories hold 178 picks, not 180 (H1).
6. The 2025 column comes from `espn_projections_2026_20260820.csv`, a different capture than the
   2022/2024 files. Doc 21's RT1 verified `proj_2025` is genuinely preseason (r=0.672 restricted);
   that check was not repeated here.
