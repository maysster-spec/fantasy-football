# 67 — RED TEAM OF DOC 65

**Aug 28, 2026, 13:30 UTC.** Written by the originating chat, answering doc 65 §8.
**Headline: §6.2 is FALSIFIED. FREEZE survives anyway — the explanation was wrong, not the decision.**

---

## 1. §6.2 — C21 IS FALSE. MEASURED, NOT ARGUED.

**C21 claimed:** the sub-0.5-point deltas between the Aug-20 and Aug-28 pulls are the Aug-28
`SCORING` patch (2-pt ids 19/26/44). Doc 65 flagged it `[ASSUMED — NOT MEASURED]` and called it
the single highest-value check. It is false, and it could not have been true.

**Why, from the code.** `Espn_pull_projections.py` line 219:

```python
f"proj_{season}": cur.get("appliedTotal") if (cur and not is_empty_stat(cur)) else None,
```

`proj_2026` is **ESPN's server-side `appliedTotal`**, computed under the league's scoring settings
on ESPN's side. The `SCORING` dict is referenced in exactly one place — `verify_scoring()`, whose
output feeds `scoring_err` / `actual_err`, the reconciliation **diagnostic**. It never touches an
exported column. **No edit to `SCORING` can move any number in the CSV.**

**Verified empirically, not just read.** Re-parsed `espn_raw_2026_20260820.json` (700 players):

| test | result |
|---|---|
| rows with a real 2026 projection | **525** |
| `abs(CSV proj_2026 − appliedTotal)` | **max 0.0000000000** |
| exact matches | **525 of 525** |

**Corollary, and it corrects doc 56's framing:** 2-pt ids are NOT actual-side-only. On the
**projection** side of the Aug-20 raw: id 19 on **65** rows, id 26 on **242**, id 44 on **360**,
id 62 on **432**. The patch was still correct to make — the reconciliation check was blind to
three real stat ids — but it is a **diagnostic** fix, not a scoring fix.

### What this does to FREEZE

**FREEZE stands.** Its evidence is C17 — boards rebuilt independently from each pull, 100 of 161
ranks identical, 150 of 161 within 2 slots, zero dropouts — plus C18's replacement levels. Neither
depends on C21. C21 was only the *explanation* for why the deltas were small.

**What changes is the forward read.** Those deltas are ESPN genuinely re-forecasting, in small
amounts. Combined with C10 (zero movement 08-20 → 08-23), ESPN appears to re-forecast in
**discrete batches**, not continuously. Sep 5 sits after the Aug-26 roster cuts and deep into
preseason. **The doc-64 board-order test on Sep 5 is therefore mandatory, not a formality.**

**And C22 gets bigger, not smaller.** Tank Dell −46.5 pts / board 134 → 192 is a real ESPN
re-forecast, not a scoring artifact. It is still unsourced. Someone should find out why.

---

## 2. §6.4–§6.9 — WHICH ARE OVERSTATED

Doc 65 §8.3 asked to be told where it overstated. Three of six.

| item | verdict |
|---|---|
| **6.4** universe shrank 556 → 520 | **OVERSTATED.** The stated worry is that replacement levels get computed on a different pool. **C18 already measured them: RB30 −0.003, WR30 −0.007, TE12 −0.006, QB12 −0.504.** The outcome is measured even though the cause is not. Demote to a provenance mystery worth one cheap `--sort owned` comparison, not a live risk |
| **6.5** `--sort draft` chosen from help text | **OVERSTATED**, and it collapses into 6.4. Correctly labelled a hypothesis; the thing it would endanger is already measured |
| **6.9** `check_kit.py` manifest is self-referentially fragile | **OVERSTATED as written, right in principle.** Yes, a manifest certifies consistency not correctness — but I independently verified all five kit files byte-for-byte against copies made before that session existed, and every sha256 in §3 reproduces. The manifest is pinned to *verified* bytes |
| **6.6** three scripts never executed end to end | **UNDERSTATED. This is the biggest open risk.** The injector's `CSV_FILENAME` was repointed to `Scripts\live_draft\` and never run. It is the only changed path that fails at draft time rather than in advance, and the weekend mock is its first execution |
| **6.7** the 34 unmatched FP names | Fairly stated. Cheap to close: list them, check the 80–140 band |
| **6.8** C22 unsourced | Fairly stated, and now **more** important — see §1 |

---

## 3. §6.1 AND §6.3 — ADJUDICATED

**6.1 — real, fix it by deletion not annotation.** Doc 63 §2 still teaches the superseded test.
A Sep-5 session that reads 63 before 64 runs the wrong one. Editing 63 to add "superseded" leaves
the wrong test on the page. **Delete doc 63 §2 outright and leave a one-line pointer to doc 64 §0.**

**6.3 — low stakes, verifiable.** The overwritten hand-edit is functionally superseded by
`DEFAULT_SEASONS = [2026]`. The Aug-28 pull at 12:56 UTC ran *before* the current script's last
write (~13:06 UTC), so `espn_projections_2026_20260828_0856.csv` was produced by the pre-patch
script — the guard has still never run for real. Note it; do not spend the week on it.

---

## 4. §7 — WHAT IS MISSING FROM THE PATH

1. **The injector mock test is the critical-path item**, not one of three weekend chores. It is
   the only changed code whose failure lands on draft night. Do it first.
2. **`Source\live_draft\` has been trashed** (Aug 28, this session) after byte-for-byte
   verification against `Scripts\live_draft\`. Five stragglers cleared; the three in
   `OneDrive\Fantasy\Scripts\` remain and need Matt.
3. **Directive §9's file map is wrong again** — it points at `Source\live_draft\`. Corrected in
   v5.3.

---

## 5. THE REAL INSTABILITY IS NOT IN THE MODEL

Three sessions have now moved or rewritten the canonical file tree in a single day, each
correctly and each invalidating the last one's map. Every handoff document written today was
stale within hours — not because anyone was careless, but because the map lives in prose that
each session re-derives and rewrites.

**`check_kit.py` is the answer and should be promoted over every prose file map.** A session
should not read where files are; it should run the checker and be told. The directive's §9 table
should say "run `py check_kit.py`" and stop enumerating paths.
