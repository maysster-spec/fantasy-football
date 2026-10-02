# 402 — A citation is not a finding. Four dead ones were live, and the hand-check found two.

*23 Sept 2026. Closes the `§4.23a` thread opened in doc 397 batch A. Directive v9.24 → v9.25.
`check_citations.py` is new and is now a §0.5(d) milestone check. Ledger row 177.*

---

## 1. THE ITEM THAT OPENED IT WAS NOT WHAT IT LOOKED LIKE

Batch A's reconcile flagged `§4.23a` as cited with **no index row and no body**, and it went into three docs and two
ledger rows as `[OPEN], mine`.

**It is not a missing finding.** It is a citation to **§4.23(a)**, *"Positional calibration"*, written without its
parentheses. The finding has existed since v6.3. The citation reads *"the positional tilt (§4.23a)"*, which is
exactly what §4.23(a) is about.

So the residue of batch A's false alarm was real, but it was a **formatting** defect that my own reconcile had
**upgraded into a missing-body defect** and sent a session looking for something that was never absent.

---

## 2. CHASING IT PROPERLY FOUND THREE MORE

| citation | where | the truth |
|---|---|---|
| `§4.23a` | findings, changelog, method traps | **§4.23(a)**, positional calibration |
| `§4.22e` | draft book | **4.22 has (a), (b), (c) and no (e).** The availability haircut and the surfaced-not-scored decision are **§4.22(c)** |
| `§4.24b` | method traps | **§4.24(b)**, the QB payoff null |
| `§4.24c` | method traps | **4.24 has (a) and (b) only.** The clustering-trap passage it points at carries no letter, so it now cites **§4.24** |

**`§4.22e` had been sitting in the draft book through ten directive versions**, on the pick-32 tie-break paragraph.
It could not have moved a pick this season, the draft is over, but §0.5(a) is substance versus expression, not
impact: a citation that resolves to nothing is a claim with no source, which is §3's territory.

---

## 3. THE FINDING IS THE METHOD, NOT THE TYPOS

**A hand-audit found two of the four.** It missed `§4.24b` and `§4.24c` for a dull reason: the file list I typed did
not include `METHOD_TRAPS.md`. The audit was correct on every file it looked at and silently blind to the one it
did not.

**`check_citations.py` found all four on its first run**, and it is about thirty lines.

That asymmetry is the point. This project already has §0.5(c)5, the missing-row check, written after MarShawn Lloyd
was rank 184 against a 180-row printed cut and simply was not on the paper. **Until now that rule had no
instrument.** §0.2 catches a thing that should not exist. Nothing caught a thing that should exist and does not.

**How the guard works.** It reads the SECTION 4 index out of `00_PROJECT_DIRECTIVE.md` as the single authority for
which finding ids exist, then scans every canonical file for `§4.x` and reports any with no index row. It **refuses
to run if it parses fewer than 20 ids**, so a broken or moved index cannot make it pass silently, which is the
exit-code trap from doc 146 in a new place.

**It was run against the four real defects before they were fixed and shown to flag all four** (§0.2: a guard that
has never been executed is not a guard). `--selftest` is independent of the live state: it injects one dead id and
one live id and asserts the checker fires on exactly the first.

**Now a row in §0.5(d)**, triggered by any finding being added, renumbered or retracted, and before any canonical
file ships.

---

## 4. THE GUARD'S FIRST RUN AFTER THE FIX FLAGGED ITS OWN DOCUMENTATION

Committed, re-run against the drive, and it reported **four dangling citations again** — this time in the v9.25
header and the changelog entry that *document the four dead ids*. Writing `section 4.23a` in a retraction notice is
**naming a string, not citing a finding**, and the checker could not tell the difference.

**That is doc 376's failure exactly** (*"the catalog rule would have cried wolf twenty-one times"*): a guard that
fires on correct text gets switched off, and then it is not a guard. Every false positive was inside backticks and
every real citation was bare, so the rule is principled rather than a patch: **blank out backticked spans before
scanning.** The selftest now has three arms rather than two, and asserts the checker is silent on a backticked dead
id.

**It took shipping the guard to find this.** Nothing in the design review would have; the defect only exists once
something documents a retraction, which is the same turn the guard was written.

---

## 4. WHAT THIS DOES NOT CLAIM

The guard checks that a cited id **exists**. It does not check that the citation is **apt** — that §4.22(c) really
is the sub-section supporting the sentence that cites it. That is a reading job and it stays one. Three of the four
fixes above were resolved by reading the cited sub-section against the citing sentence, not by the tool.

**And it only knows about section 4.** Citations to §0.x, §2, §6 and §9 are not checked, because those have no index
to check against. Extending it would mean giving the directive's own sections an index, which is a bigger change
than the defect justifies today. **[OPEN], mine, low priority.**

---

## 5. STILL OPEN

- **D3** — whether `own_chg` predicts contention in this league. **Unblocked as of this morning**: the first values
  landed in `WIRE_20260923.csv`. Needs several weeks before it is a measurement rather than an anecdote.
- **[OPEN], mine:** log the claim ORDER at placement in `wire.py`, so doc 401's blocked mechanic becomes measurable.
- **Batch E** — ledger rows 162, 163, 165; the doc 383 registry batch; §4.33's TE playoff draw; `Auto Reactivate:
  No`; the position-cap and keeper-eligibility interactions with IR.

---

## 6. PROVENANCE

Archived before overwriting, committed from a fresh container path with `expectedMtimeMs`, staged back and compared
by CRLF-normalised sha256 (§9 rules 1 and 2). Every edit asserted its occurrence count before applying (§9 rule 6).
The guard was re-run against the drive after the fixes landed and reports clean.
