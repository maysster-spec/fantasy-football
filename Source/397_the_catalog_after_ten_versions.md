# 397. Red-team catalog: ten directive versions in one night, and what they broke.

**23 Sept 2026. Matt: *"worth a review and a red team. We have updated 10x since the last fable run."***
**Catalog only, per §0.5(c)1: every candidate defect enumerated before any is investigated, shipped on
its own so he can see the shape and re-order it. Nothing below is fixed yet.**

**Scope: v9.10 through v9.20, docs 382 to 396.** Ten versions, six of them in the last twelve hours.

---

## BATCH A. THE RESIDENT SET CONTRADICTS ITSELF. All four CONFIRMED, highest severity.

| # | defect | status |
|---|---|---|
| **A1** | **§2 states a claim it has already retracted, seventeen lines apart.** Line 669 strikes *"the 19.5% downgraded-to-Questionable cell is the quiet failure, seat gone and nothing gained"* as WRONG. Line 686 asserts it: *"19.5% are downgraded to Questionable, the quiet failure, seat gone and nothing gained"*. A session reading §2 top to bottom meets the correction and then the error. **This is §9 rule 5 failing one day after I wrote §9 rule 5** | CONFIRMED |
| **A2** | **`00_START_HERE.md` is stale on every IR rule settled in v9.19 and v9.20.** Zero occurrences of SSPD, "NOT invalid", or "Questionable or Doubtful". Last written 22 Sept 20:00, before doc 394. **This is the handover file: a fresh chat begins from the retracted story** | CONFIRMED |
| **A3** | **The findings count is stated three ways.** The WHERE THINGS LIVE block says *"all 42 findings"*, §4's intro says *"The 43 findings"*, the index actually holds **45** rows | CONFIRMED |
| **A4** | **The changelog pointer is stale**: *"every entry v5.4 through v9.14"*. It now runs to v9.19 | CONFIRMED |

---

## BATCH B. THE HEADER, WHICH IS WHAT MATT NOTICED UNPROMPTED

*"i don't recall seeing system directive structured this way... just looks different."* **He is
right and the cause is mine, made tonight.**

| # | defect | status |
|---|---|---|
| **B1** | **The header accreted instead of being replaced, five times in one night.** It is now **42 lines, 847 words, 6.1% of the file**, naming **six versions** (v9.14, v9.15, v9.16, v9.17, v9.18, v9.20) across **four nested bracket blocks**, before the reader reaches a single rule. **The file's own NAMING RULE says "The version lives in the header LINE above" — singular — and "Full history: `DIRECTIVE_CHANGELOG.md`".** I duplicated the changelog into the header and then kept prepending | CONFIRMED by count |
| **B2** | **The same accretion in `check_kit.py`.** The `wire.py` pin comment is now one run-on with five *"Before that"* clauses | CONFIRMED |
| **B3** | **THE OUTSIDE CHECK (§0.5(c)6), not yet run.** What is published practice for where a changelog sits relative to an operating document, and for how long a preamble that is read on every single turn should be? Every red team this project has run was internal-consistency only; this is the batch that can find what nobody here has thought of | NOT YET RUN |

---

## BATCH C. CODE SHIPPED TONIGHT, NOT YET RUN IN PRODUCTION

| # | defect | status |
|---|---|---|
| **C1** | `own_chg`, `own_start`, `own_asof`, `clears` and `STATUS_LOG.csv` have **never executed on his machine**. Built and unit-tested in the container with negative controls; the next `ff.bat` is the first real proof | OPEN, one run away |
| **C2** | **Downstream readers of `WIRE_*.csv` and `FREE_UNRANKED_*.csv` after adding four columns.** §3's merge-collision corollary says grep every reader when you change a file's shape, and I had not | **CHECKED AND CLOSED: `sheet_engine.py` uses `csv.DictReader` at every read site (lines 500, 520, 527), which maps by header name and tolerates extra columns. No positional indexing anywhere. Safe** |
| **C3** | Whether his league's payload carries his own `waiverProcessDate`, or only the default league's | OPEN, one run away |

---

## BATCH D. NUMBERS PUT INTO FILES TONIGHT THAT MAY NOT MEASURE WHAT THEY CLAIM

| # | defect | status |
|---|---|---|
| **D1** | **The seat-life numbers may be measuring the wrong event.** §2 says *"the median seat dies between two and three weeks"*, computed as **"does he take an offensive snap in w+1"**. But ESPN's rules, sourced a day later, say **the seat survives Questionable, Doubtful, and even him PLAYING, and ends only when the designation vanishes entirely.** Return-to-play and seat-death are different events. **If so the seat lasts LONGER than §2 says and the number understates his option** | **SUSPECTED, mine, not yet measured** |
| **D2** | The 61.1 / 29.1 / 11.2 ordering split is measured, but the confound argument (that banked-win teams are high-priority teams and so the effect is conservative) is **verbal, not modelled**. It should be conditioned on waiver rank, which `wire.py` has been reading all along | NOT YET RUN |
| **D3** | `own_chg` predicts contention **in this league**: stated as NOT ESTABLISHED in doc 395 and 396, correctly. Flagged here so it is not quietly promoted later | OPEN by design |

---

## BATCH E. THREADS CARRIED SINCE BEFORE THIS RUN, STILL OPEN

Ledger **162** (`sheet_engine` names the wrong man ahead: Coleman is Denver, Jeanty is Las Vegas),
**163** (the in-doubt table pairs a backup by the preseason chart's team), **165** (air-yards share
and WOPR onto the wire row, and the list ordered on the cross rather than on targets alone).
The **doc 383 batch**: §4.12, §4.18b, §4.20, §4.22, §4.25 and §4.26 were measured on the rank-proxy
registry and have never been re-run on the five-year half-PPR one. **§4.33's TE playoff draw is
[OPEN] between two docs that disagree.** And three IR unknowns: `Auto Reactivate: No`, the
position-cap interaction, and whether time on IR breaks *"rostered all season"*.

---

## WHAT I WOULD DO FIRST, AND WHY

**A1 and A2 are not tidiness, they are live wrongness in the two files that get read the most.** A2
is the worse of the two: it is the handover, so a fresh chat starts from rules that were retracted
yesterday. **B1 is what Matt actually noticed and it is the reason A1 and A4 happened**, because a
header that accretes is a header nobody re-reads as a whole. **D1 is the most interesting** and the
only one that could change a decision rather than a document.

**Suggested order: A2, A1, A4, A3, then D1, then B1 with B3's outside read, then B2. C2 is closed.**
Batches C and E are waiting on a run or on a measurement, not on a decision.
