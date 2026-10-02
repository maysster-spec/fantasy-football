# 401 — The claim-order gradient is arithmetic, not a mechanic. And a regex dropped every defence.

*23 Sept 2026. Doc 397 batch D2. Directive v9.23 → v9.24. `claim_order_null.py` is new and reproduces doc 396's
population exactly before it measures anything. Ledger row 176. Doc 396 corrected at source.*

---

## 1. WHAT WAS UNDER TEST

Doc 396, three days old, measured on this league: *"on the 586 CONTESTED claims the win rate goes 61.1% with no other
win that run, 29.1% with one, 11.2% with two or more"*, and offered it as evidence for ESPN's documented mechanic, a
winner being demoted to the end of the order mid-run. Doc 397 catalogued it as **D2: the confound unmodelled against
waiver rank.**

**It is worse than a confound.**

**Pre-registered form, before the run (§0.5(a2)):** hold each team-run's contested win count fixed and permute
**which** of its contested claims won. That destroys any real ordering effect while preserving how many claims each
team entered and won. If the gradient is a mechanic, the null flattens it. Direction not predicted.

---

## 2. THE STATISTIC IS DEGENERATE

| | 0 other wins | 1 other win | 2+ other wins |
|---|---|---|---|
| **observed** | **61.1%** (n=211) | **29.1%** (n=223) | **11.2%** (n=152) |
| **null, 3,000 draws** | 61.1% | 29.1% | 11.2% |
| **null 95% band** | **[61.1, 61.1]** | **[29.1, 29.1]** | **[11.2, 11.2]** |

**Zero variance.** The permutation cannot move the number at all, so the observed data is indistinguishable from
randomly reshuffled data and the gradient carries **no information about ordering whatsoever.**

**Why, and it is visible once stated.** The bucket is *other wins by that team in that run*, which equals the team's
**total** wins minus **this claim's own result**. So a claim that won lands in bucket `T-1` and a claim that lost
lands in bucket `T`. **A winner sits one bucket below a loser from the same team-run by construction.** The gradient
is the distribution of how many claims teams win, restated, and it would appear in data with no mechanic at all.

**The published cells also carried no sample sizes**, which §3 requires on every stored finding. They are 211 / 223 /
152, and the original third cell under a narrower definition is n=11.

---

## 3. AND THE MECHANIC CANNOT BE MEASURED FROM THIS SOURCE AT ALL

Nobody had checked this. **Every claim in a run carries one identical timestamp** — 03:28, 03:30, matching ESPN's
documented *"typically processed daily around 3:00 AM ET"*. Across 135 runs, **zero** have more than one distinct
timestamp.

So `waiver_report_*.csv` **cannot express within-run order**, and *"prior wins that run"* was never a quantity this
data could say. It was read into the file.

**BLOCKED, with the missing input named (§0.5(a4)):** Matt's **own claim ordering, recorded at placement and paired
with the outcome**, forward-going only. He controls that order and ESPN does not record it. **Mine to build into
`wire.py`.**

---

## 4. WHAT SURVIVES, AND THE RULE DOES

**Measured, on a population that reproduces doc 396 to the digit** (745 player-runs, 543 team-runs, 28.6% contested,
586 contested claims, n=1,131 decided claims):

- **only 28.6% of player-runs are contested**
- **an uncontested claim wins about three in four regardless**

**AND "RANK THE CONTESTED MAN FIRST" STILL STANDS** — on ESPN's sourced text, as a **dominance argument with no
effect size**, exactly the footing of the Sunday-night placement rule. A winner is demoted mid-run; he sets the
order; so priority spent where a claim is contested cannot do worse than priority spent where nothing is at stake,
and it costs nothing.

**His play does not change. The number behind it is gone.** That is the second time in one day (doc 399 was the
first) where the conclusion outlived the measurement that was published for it, which is worth noticing on its own.

---

## 5. THE TRAP THAT COST MORE THAN THE FINDING

**ESPN gives D/ST units NEGATIVE player ids.** A team defence is `ADD Player ID -16012`.

The first pass extracted the player with `r'ADD Player ID (\d+)'`. That does not match a minus sign, so **437 of
1,623 waiver rows — 27%, every one of them a defence — vanished with no error and no warning.**

**How it surfaced matters more than the bug.** Not by inspection: the population simply failed to reproduce doc 396's
published counts (476 player-runs against 745). **Had those numbers happened to look plausible, a D/ST-free
population would have gone out as "all waiver claims."** The reproduction check was the only thing standing between a
silent 27% exclusion and a published finding.

**§0.6 exists because of a D/ST exclusion.** This is the same defect in a new place, which is why it goes in
`METHOD_TRAPS.md` rather than only in a ledger row (§0.5(f)): use `(-?\d+)` on any ESPN id, and **assert the
extraction count against the row count**, because an extraction that silently yields NaN is §3's silent-skip trap
wearing a regex.

---

## 6. §9 RULE 7 FIRED ON ITS OWN FIRST TEST

Written an hour earlier in doc 400: *"if the header exceeds ~20 lines, the oldest narrative moves to the changelog
before the new one is written. Measure it, do not eyeball it."*

Adding v9.24's paragraph took the header to **22 lines**. The v9.22/v9.23 narrative moved to the changelog and the
header came back to 16. **The rule caught its author on the first version after it shipped**, which is the argument
for a measured threshold over an instruction to be careful.

---

## 7. STILL OPEN

- **[OPEN], mine:** log the claim ORDER at placement in `wire.py`, so the mechanic becomes measurable forward-going.
- **D3** — whether `own_chg` predicts contention in this league. Now unblocked: the first `own_chg` values landed
  today. **[NOT ESTABLISHED]** until run.
- **§4.23a**, cited in the findings file with no index row and no body.
- **Batch E** — ledger rows 162, 163, 165; the doc 383 registry batch; §4.33's TE playoff draw; `Auto Reactivate:
  No`; the position-cap and keeper-eligibility interactions with IR.

---

## 8. PROVENANCE

Five files archived to `2026\_archive\` before overwriting, committed from a fresh container path with
`expectedMtimeMs`, staged back and compared by CRLF-normalised sha256 (§9 rules 1 and 2). Every edit asserted its
occurrence count (§9 rule 6). **Doc 396 corrected at source with a banner and its gradient struck in place** (§9 rule
5). `claim_order_null.py` carries its pre-registered form in the docstring, asserts the id extraction against the row
count, and prints the reproduction check and the timestamp finding on every run.
