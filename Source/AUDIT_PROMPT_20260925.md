# AUDIT PROMPT: the Opus span, v9.13 through v9.31 (22 to 25 September 2026)

*Version 2, 25 Sept 2026, Fable. Paste this whole file into a FRESH chat in the E-Discovery Keeper League 2026
project. It is written for a session that has NOT seen the work and must not be told what the work concluded before
it checks. Version 1 was written by the Opus session that did the work and covered only its last sitting (24 to 25
Sept, claims C1 to C13); it is at `_archive\AUDIT_PROMPT_20260925_v1_opus.md` and is carried here as SECTIONS 1 to 6
with its edits marked. SECTION 0 is new: the whole span, what was measured before this was written, and how the audit
is batched against Matt's usage budget.*

---

## SECTION 0. SCOPE, BUDGET, BATCHES

**What Matt asked for, verbatim:** *"I'm looking for all changes for the better or worse."* The span is directive
v9.13 through v9.31, docs 385 through 431, written by one Claude Opus chat between 22 Sept 06:00 and 25 Sept 18:30
ET. Version 1 of this prompt covered one sitting of it. **The deliverable is not a list of things that are
consistent. It is one table per batch: the change · better / worse / neutral · on what evidence · what to do (keep,
strike, re-measure, or cut to the changelog).**

**BUDGET RULES. Matt's usage is capped and resets Monday; every turn in this project carries a 93 KB directive as its
system prompt, so turns are the cost, not files.**
1. One batch per sitting. End every batch with a §0.1 overview and a ledger row, then STOP. Do not start the next.
2. Read only the lines a check needs. Stage files and hash or grep them; never `project_read` anything over 20 KB
   (it lands in context whole; the directive did today, 25,000 tokens for one hash).
3. Do not read a doc you are not auditing, and do not read docs 422 and 425 (the author's own verdicts on its guards)
   before your own verdict on the same thing is written.
4. Write the findings doc at the next free number above 431. List `Source\` first: six numbers between 385 and 431
   have no file (413, 414, 424, 426, 429, 430) and they are NOT free, they are cited.

**WHY A DIFFERENT MODEL.** §0.5(c)6 says one batch of every red team goes outside; the cheapest outside check on four
days of one model's work is another model reading it cold. Do not inherit its framing: form the number, then open
the doc.

**THE BATCHES, in this order. A is the cheapest and the one every future chat pays for; C is where the rules rest.**

| batch | what | why this order |
|---|---|---|
| **A. the handover and the resident set** | (1) `00_START_HERE.md` v13 against directive v9.31: for every left-column string in the directive's DO-NOT-QUOTE table, grep ALL of `Source\` and report every live occurrence outside a strike-through or a banner (§9 rule 5's reach check, done as a script, not by hand); (2) the store copy `claude/00_PROJECT_DIRECTIVE.md` byte-identical to the drive copy; (3) `py check_citations.py --selftest` then a run; (4) the six missing doc numbers: which files cite each, and write or strike; (5) the directive header is 41 lines against §9 rule 7's ~20 cap, and the DO-NOT-QUOTE table the rule mandates is 19 of them, so the rule cannot be obeyed as written: say which is wrong, the cap or the table; (6) `OPEN_THREADS.md` is dated 20 Sept and `ff.bat` has no `open_threads.py` step, so v9.31's "renders both lists at the top" has never happened on the drive | every fresh chat reads these first; v12 of the handover carried two retracted rules for two days and nobody's guard fired |
| **B. the week sheet** | version 1's SECTION 3 items 1 to 3 and claims C1 to C3, exactly as written there | it is what Matt acts on Sunday |
| **C. the numbers the rules rest on** | in this order, each reproduced from the raw data by your own code before the doc is opened: doc 405 (Thursday run, n=626, from `waiver_report_*.csv`; mind the negative D/ST ids and the older files' repeated rows); doc 393 (884 for 884 with a drop, 24 of 371 without); doc 399 (seat valid 75.5 / 51.2 / 35.2 / 26.4 / 22.2, and the 24.5% freeze); doc 423 (K12 8.26, sd 0.16); doc 385 (riser +36, 9 to 56, n=138, and the 2021 reversal); doc 389 (spike 4.3% base, 10.1% top fifth); then version 1's C4 to C13 | these are the standing instructions in §2 and §6; a wrong one changes what he does on Wednesday night |
| **D. the directive diet, the outside read** | SECTION 0 is 41,243 of 93,560 bytes. For every paragraph tagged v9.13 or later, classify RULE (a sentence a session must obey) or STORY (how it was found), and propose the cut as a diff for Matt, not an applied edit; price the paste: tokens per turn before and after. Published practice is already cited in §9 rule 7 (Keep a Changelog; context rot); the question is whether the file obeys its own rule below the header, and it does not: §0.5(a6), (a7), §2's kicker and IR blocks and §9 rule 7 each carry their case in full | the cost is paid on every turn of every chat, including the daily publish task |
| **E. the guard kit** | version 1's SECTION 3 items 4 to 6, then `Scripts\check_guards.py` re-run and its eight mutations listed with which guard, if any, caught each | doc 425's own number is seven of eight survive; confirm or move it |

---

## SECTION 0.1. THE SPAN CATALOG. Every change, the one sentence that kills it, the check.

The "prior" column is Fable's read from the changelog alone, before any check, and **the auditor must not accept
it.** It is there so a disagreement is visible.

| version | doc | what changed | the load-bearing sentence | the check | prior |
|---|---|---|---|---|---|
| 9.13 | 385 | all five registry years on the FantasyPros half-PPR page; §4.34 restated: +36 VBD14 (9 to 56, n=138), uneven, 2021 runs the other way | the 2021 and 2025 files are the half-PPR page, not full-PPR and not a rank | `Source\adp_registry\MANIFEST.csv` and the raw files: columns Yahoo / Sleeper / RTSports (2025 adds Real-Time), never ESPN / CBS / Fantrax; 2021 values not exactly 1..n; re-run `research\j4\j4_riser_keeper.py --with-2021` | better; the reversal is stated honestly |
| 9.14 | 389 | §4.35, the spike week: 4.3% base, top fifth by WOPR 10.1%, targets alone 6.7% | population: WR/TE not startable last week and claimable, n=8,651 | reproduce from the nflverse cache | unknown, low stakes |
| 9.14 amended | 390 | the IR slot does not occupy one of the fifteen; a claim with its own drop keeps the seat | settings line 29 lists IR 3 separately from the roster | read the line | better, sourced |
| 9.15 | 391 | waiver period 2 days → PLACE SUNDAY NIGHT; 91.9% of Out designations Thursday or later; seat curve 73.8 ... 23.8; eight states | all three numbers were retracted within the span (v9.16, v9.22, v9.26) | confirm doc 391 carries its banner and that no live file quotes any of the three | the version was net worse for 36 hours; the retractions are the improvement |
| 9.16 | 392 | 91.9% retracted; §0.5(a5): measure the claim, not its surroundings | `date_modified` is the last edit to a row, so timing is BLOCKED | the feed's structure | the rule is better; whether it was then obeyed is batch C's question (it was not, twice: v9.20 and doc 417 shipped after it) |
| 9.17 | none | §9 rules 5 and 6; the em-dash rule removed | a retraction must reach the doc that minted it | grep `Source\` for "92%" and "91.9" outside banners | better |
| 9.18 | 393 | PUT A DROP ON EVERY CLAIM: 884 executed with 0 failures, 371 with 24; `STATUS_LOG.csv`; the frozen-lineup rule | all 24 failures carried no drop | reproduce from `waiver_report_*.csv`; confirm `STATUS_LOG.csv` grows on every `wire.py` run | better, on his own record |
| 9.19 | 394 | the IR rules sourced from ESPN's FOOTBALL page; three rules reversed; SSPD never IR-eligible | an upgrade to Questionable or Doubtful leaves the roster NOT invalid | read the page in a browser and check the breadcrumb's sport | better; the method failure is the lesson |
| 9.20 | 396 | rank the contested man first; 61.1 / 29.1 / 11.2 | retracted at v9.24 | no live file carries the three numbers (START_HERE v12 did until today) | worse, then corrected; the rule survives as dominance only |
| 9.21 | 397, 398 | the resident set contradicted itself in five places; the handover rewritten | the sweep's class does not recur | it did: START_HERE v12 carried v9.24's and v9.26's retractions for two days | better, but the class recurs, so batch A(1) is a script |
| 9.22 | 399 | seat valid 75.5 / 51.2 / 35.2 / 26.4 / 22.2; 24.5% freeze the next Sunday; position order inverts | the seat dies when the DESIGNATION goes, not when he plays | `research\ir\ir_seat_validity.py` against the cache, then your own code; the retracted curve is unreproducible, try once and stop | better |
| 9.23 | 400 | §9 rule 7; the DO-NOT-QUOTE table | the header stays under ~20 lines | it is 41 today | the rule is better; its threshold contradicts its content |
| 9.24 | 401 | 61 / 29 / 11 degenerate by construction; the negative D/ST id trap in `METHOD_TRAPS.md` | a permutation null reproduces the cells with zero variance | reproduce the null | better |
| 9.25 | 402 | `check_citations.py` | the SECTION 4 index is the authority | `--selftest`; then extend it to `doc N` | better; it cannot see the six dangling doc numbers |
| 9.26 | 405 | claims execute THURSDAY 03:00 to 06:00, 86.3% of 626, never Monday to Wednesday; PLACE WEDNESDAY NIGHT | the execution timestamp in `waiver_report_*.csv` is the run time | reproduce; the 2026 file is one row per event, the older ones repeat each event per week, dedupe first | better, and it changes his weekly play |
| 9.27 | 409 | §0.5(a6), answer the question he asked | a rule, not a number | does it duplicate §4.20 and §0.5(a3)? | unknown; 2 KB of resident text |
| 9.28 | 417 | §9 rule 2 per write; the first `BLEND_W` table retracted, re-fit by `blend_weight.py` | the shipped `BLEND_W` is the measured one | `py research\blend_weight.py --check` | better |
| 9.29 | 423 | K12 replacement 8.26 a week, sd 0.16 | scored under our rules, 8+ games, weeks 1 to 14 | `k12_replacement.py`, then your own code | better |
| 9.30 | 427 | §0.5(a7); softest matchup +1.93 (se 0.90); the `norm_name` join and the seat gate fixed | version 1's C4, C5 and SECTION 3 items 1 to 3 | as written there | better on the fixes; (a7) is another 2 KB |
| 9.31 | 430, no file | `claude_todo.txt`; `make_online.py` in `ff.bat`; the daily publish task | `open_threads.py` renders both lists at the top | `OPEN_THREADS.md` is dated 20 Sept | the mechanism is unproven on its artifact |

**Docs in the span not tied to a version**, each a take or a page fix, audited only where batch B or C reaches
them: 386, 387, 388 (week 3 takes), 404 (Schultz), 406, 407 (the sheet had never seen a 2026 snap), 408, 410, 411,
412 (the injury feed), 415 (THE CALL), 416, 418, 419 (C1), 420, 421, 422, 425, 428, 431.

---

## SECTION 0.2. MEASURED BEFORE THIS WAS WRITTEN, so it is not redone. Check it, do not trust it.

- `Source\00_PROJECT_DIRECTIVE.md`: 93,560 bytes, sha256 `aaef2377ad44b17a`, which matches version 1's pin. v9.12
  was 62,367 bytes on 22 Sept: **+31,193 bytes, +50%, in three days.** SECTION 0 is 41,243 bytes (44%). The header
  is 41 lines and 820 words before "You are a quantitative".
- The store copy `claude/00_PROJECT_DIRECTIVE.md` carries the v9.31 header and was written 18:08 UTC 25 Sept; the
  pasted project instructions are v9.31. **Byte-identity with the drive is NOT confirmed. Batch A(2).**
- `00_START_HERE.md` v12 (27,857 bytes, 23 Sept) told a fresh chat to place claims Sunday night and quoted 61.1 /
  29.1 / 11.2 as live. **v13 (25 Sept) strikes both in place**; its hash is in SECTION 1.
- `claude_todo.txt` is 1,825 bytes; version 1 pinned 1,448. It was edited one minute after version 1 was written.
  Not a tamper; re-pin it.
- `OPEN_THREADS.md`: mtime 20 Sept 14:47 UTC. `ff.bat` (150 CRLF, 0 bare LF) runs `lineup`, `build_news`, `wire`,
  `todo_page`, `make_online`, `make_commands`, `check_kit`, `check_sources`, `check_vintage`, `check_pages`, and
  not `open_threads`.
- Missing doc numbers in 385 to 431: **413, 414, 424, 426, 429, 430.** Version 1 listed four. "doc 430" is cited in
  `ff.bat`, `open_threads.py`, the directive (twice), the changelog and `claude_todo.txt`. The other five: not checked.
- **Retractions inside the span, of the span's own claims: six** (91.9%; the Sunday-night rule; the seat curve; "a
  parked QB holds longest"; 61 / 29 / 11; the first `BLEND_W`). Three self-found, three found by Matt. **Two shipped
  AFTER §0.5(a5) was written against exactly that pattern** (v9.20 on 23 Sept, doc 417 on 24 Sept). That is the
  question to put to every number still standing in batch C: was its load-bearing sentence measured before the rule
  shipped, or after?
- `matt_todo.txt` names `py claim_order_log.py` for Wednesday, and `claude_todo.txt` still holds "build claim ORDER
  at placement into `wire.py`" as open. One of the two is stale; reconcile in batch A.

---

## SECTION 0.3. WHAT THE OPUS SESSION WROTE FOR ITS OWN LAST SITTING. Version 1 follows, edits marked [v2].

## WHY YOU ARE HERE, AND THE ONE THING THAT MAKES THIS AUDIT DIFFERENT

A long session on 24-25 September changed the engine, the directive, two published pages and the
tracking mechanism. **Every defect it found was found by Matt, not by a guard.** That is measured,
not a feeling: doc 425 ran a mutation harness that reintroduced eight real shipped defects one at a
time, and **seven of the eight survived every check in the kit.** The reason is structural. The
checks recompute from the same engine they are checking, so they can only find a file disagreeing
with another file.

**So the rule for this audit, and it governs everything below: do not read the session's own
documents until after you have independently verified the thing they describe.** Read a doc first
and you will confirm its framing; that is the failure mode this audit exists to break. Verify from
the raw source, form your own number, then open the doc and compare. Say plainly when they disagree.

Two more rules that come from the same place:

- **A test must exercise the object PRODUCTION builds, not an equivalent one.** On 25 September a
  guard was shipped, "verified" against a CSV that spelled a field `team`, and was dead on arrival
  because production spells it `tm`. It never fired once and the commit reported success. If you
  verify a fix, call the real function with real production-shaped inputs.
- **Verify by content, never by a result line.** `device_commit_files` returning a path means the
  call was accepted, not that the bytes landed. Stage the file back and hash it.

---

## SECTION 1. THE SPINE: What changed, where it lives, what hash it should carry.

All paths are on Matt's PC, reachable through the remote-devices tools. Base: `G:\My Drive\_Fantasy\2026\`

**Stage each of these and confirm the size and sha256 prefix before auditing anything.** A mismatch
means something changed after the session ended and everything below is suspect.

| file | bytes | sha256 (first 16) |
|---|---|---|
| `Scripts\sheet_engine.py` | 209,607 | `48ca1ea40d169633` |
| `Scripts\ff.bat` | 8,414 | `3a4684272a1fb1c7` |
| `Scripts\make_online.py` | 6,239 | `73ca8d8a9de09531` |
| `Scripts\research\open_threads.py` | 14,392 | `2e7c5d3f0777a3a1` |
| `Source\00_PROJECT_DIRECTIVE.md` | 93,560 | `aaef2377ad44b17a` |
| `Source\claude_todo.txt` | [v2] see `_archive\` stamps; re-pin | [v2] moved after version 1 |
| [v2] `Source\00_START_HERE.md` (v13) | [v2] 30,985 | [v2] `44eafa13763dc8ac` |

**Also written, hashes not pinned here so you check them yourself against the session's claims:**
`Source\DIRECTIVE_CHANGELOG.md` · `Source\matt_todo.txt` · `Source\ONLINE_WEEK_SHEET.html` ·
`Source\427_the_slope_was_not_his_claim.md` · `Source\428_the_two_defence_trick_does_not_transfer_to_quarterback.md` ·
`Source\431_the_two_i_owed.md` · `_archive\00_PROJECT_DIRECTIVE_20260925.md` (the archived v9.29) ·
`Scripts\research\qb_matchup.py` · `qb_pair_playoffs.py` · `te_pair.py` · `qb2_window.py` · `dst_k_supply.py`

**Off the drive, and each needs its own check:**
- Project doc store: `claude/00_PROJECT_DIRECTIVE.md` and `claude/DIRECTIVE_CHANGELOG.md` were pushed
  at the end. **Confirm the store copy and the drive copy are byte-identical.** The store is what
  gets pasted into the Project's custom instructions, and on 25 September the directive reached the
  drive and NOT the store, which Matt caught. [v2: hash the store copy from a local file; do not read it.]
- Two artifacts: the week sheet at `claude.ai/artifact/1eaMAtyCzdqMcSdh96w4SK` and the roster clock at
  `claude.ai/artifact/NpLWo1xBiWRG4bztW7L5xw`.
- One scheduled task, `trig_01F1k2gt3LKkRowMWB7mScpy`, "Publish the week sheet", daily 08:54 ET,
  bound to Matt's computer.

---

## SECTION 2. THE CLAIMS, AND HOW TO KILL EACH ONE

Each row is a claim the session shipped. For each: **derive the number yourself from the raw data,
by your own code, before reading the doc.** Running the session's own script proves only that the
script is deterministic. The raw data is the nflverse cache at
`Scripts\research\_nflverse_cache\stats_player_week_{2021..2025}.csv` and
`Source\dst_weekly_2021_2025.csv`. League scoring is in SECTION 2 of the directive.

| # | the claim | the number to reproduce | where it is used |
|---|---|---|---|
| C1 | ESPN's `proj_2026` is a REST-OF-SEASON total, so a weekly rate divides by games LEFT, not 17 | the identity `(old proj − new proj) == (new actual − old actual)` | every rate on the page |
| C2 | The form join missed nine men because it used a raw name lookup instead of `norm_name` | Kyle Pitts Sr. printed **7.89**, correct **5.41** | THE CALL, the week-5 calendar row |
| C3 | A seat is void when the backup left the job's team | Emari Demercado is on DAL, was priced behind Kenneth Walker III on KC | the seat list, THE CALL |
| C4 | Matchup moves an ELITE quarterback at least as much as a streamable one | elite slope **0.448** (se 0.159), streamable **0.216** (se 0.097), difference **−0.232** (se 0.186) | doc 427, directive §0.5(a7) |
| C5 | Picking the softest matchup among streamable QBs pays | **20.36** a week against **18.43**, +1.93, se 0.90, n=70 season-weeks | doc 427, the roster clock |
| C6 | An elite QB1 plus a streamer QB2, platooned on matchup, LOSES in weeks 15-17 | **24.80** against **22.49**, −2.31, se 0.35 | doc 428, the roster clock |
| C7 | Two streamable QBs platooned is a weak positive | +0.31, se 0.23 | doc 428 |
| C8 | Tight end splits the same way on the quality gap | elite −0.86, mid (ranks 7-12) **−0.37**, two streamers **+0.50** (se 0.06) | the roster clock, the pairing table |
| C9 | The pairing payoff is monotone in the quality gap and crosses zero near 1 point | six rows: +0.79 / +0.50 / +0.31 / −0.37 / −0.86 / −2.31 against gaps of <1 / 0 / 0 / 2.7 / 5.5 / 6.4 | the roster clock's bar chart |
| C10 | A starting QB's missed weeks rise all season | **6.2%** in week 1 to **29.9%** in week 14 to **44.6%** in week 17, n=160 team-seasons | doc 431, the roster clock |
| C11 | A QB2 held from week 10 captures 96% of a full season's exposure | **2.57** of **2.67** missed weeks | doc 431, the late-season card |
| C12 | The defense pool does not thin | **13.5** clear 5.99 in weeks 1-5, **13.6** in weeks 10-14 | doc 431, the roster clock |
| C13 | The kicker pool thins mildly | 15.4 to 14.2 | doc 431, the roster clock |

**For C9 specifically:** the six payoffs come from three different scripts and one earlier doc (267).
**Check they are on the same footing before you accept the pattern.** A monotone line assembled from
measurements with different populations, windows or baselines is a coincidence wearing a law's
clothes. If they are not comparable, say so; that finding is on the roster clock as a chart and Matt
will act on it.

**For C12 and C13:** the session used `usable minus 12` as "free and usable", a worst-case bound, not
doc 252's roster reconstruction. **Confirm the bound is stated as a bound everywhere it appears**,
including on the published page, and that nothing quotes it as a measurement.

---

## SECTION 3. THE FIXES, AND WHETHER THEY FIRE

For each, **call the real function with production-shaped inputs and confirm the behaviour changes.**
Build free rows the way `wire.py` builds them (`f = dict(rate[pid])` plus the wire columns), not the
way the wire CSV is shaped.

1. **`norm_name` on the form join.** After the fix, zero RB/WR/TE should carry vintage `proj` while a
   measured rate exists under a normalised name. Verify the count is zero and that it was nine before.
2. **The seat gate.** It should cut exactly one of the ten live seat rows and print the reason. Verify
   it reads `tm`, not `team`, and that the negative control fires: hand `render()` rows shaped with
   `team` and confirm the key contract raises.
3. **The key contract in `render()`.** Confirm it raises on missing `name/pos/tm/wk/bye` and that you
   have seen it raise, not merely that the code exists.
4. **`make_online.py`.** Run it. Confirm each of its four refusals fires when you break the input:
   no page bar, no stamp, no roster-clock link, surviving outer document. **A guard you have not seen
   fail is not a guard.**
5. **`ff.bat`.** Confirm the new step is present, that the file is still pure CRLF (150 line endings,
   zero bare LF), and that `RC8` reaches the RESULT line.
6. **`open_threads.py`.** Confirm it reads both `matt_todo.txt` and `claude_todo.txt` and renders both
   at the top of `OPEN_THREADS.md`. [v2: and that the file on the drive has been rebuilt at all; it had
   not been, as of 25 Sept 18:30 ET.]

---

## SECTION 4. KNOWN OPEN, so you do not spend the batch rediscovering it

These are already identified. **Confirm them, price them, and fix what is cheap. Do not treat finding
them as the audit's result.**

1. **Doc numbers cited in shipped files with no document: 424, 426, 429, 430** [v2: and 413 and 414 have no
   file either; whether they are cited is unchecked]. `sheet_engine.py`, `make_online.py`, `open_threads.py`,
   `ff.bat`, `claude_todo.txt`, the directive and the changelog all cite at least one of them.
   **`check_citations.py` covers `§4.x` references and does not cover `doc N`.** The cheapest real fix is to
   extend it, run it, and then either write the missing docs or strike the citations. Doc 402 is the precedent
   and its `--selftest` shows the shape.
2. ~~**`00_START_HERE.md` is eight directive versions stale.**~~ [v2: **fixed at v13 on 25 Sept**, and it was worse
   than stale: it carried two retracted rules as live. Batch A(1) checks whether v13 is now clean and whether any
   OTHER canonical file still carries a DO-NOT-QUOTE string.]
3. **`claude_todo.txt` still holds two open items**, the claim-order logging in `wire.py` and the
   five-week QB look-ahead port onto the week sheet. Neither was started. [v2: `matt_todo.txt` says
   `py claim_order_log.py` exists and runs Wednesday; reconcile.]
4. [v2] **`OPEN_THREADS.md` has not been rebuilt since 20 Sept**, through nineteen directive versions and 46 docs.
   Cheap fix: a one-line step in `ff.bat` after `todo_page.py`, CRLF preserved, RC checked like the others; then one
   run. Do not do it on a Sunday morning before he runs the bat.
5. [v2] **The directive header is 41 lines against §9 rule 7's ~20**, and the rule's own table is 19 of them.
6. [v2] **The directive grew 50% in three days and 44% of it is SECTION 0.** Batch D.

---

## SECTION 5. HOW TO RUN IT

Follow §0.5(c) of the directive, which is Matt's own method:

1. **CATALOG FIRST.** SECTION 0.1 is the catalog. Ship your re-ordering of it, if any, before batch A, in one
   reply, so Matt can see the shape.
2. **BATCH.** SECTION 0's five, in order, one per sitting. A half-finished sweep is worse than a small complete one
   because it reads as coverage.
3. **OVERVIEW AT THE END OF EACH BATCH** in §0.1 form: what changed, what held, what is still open. Then stop.
4. **COLLISION CHECK** before writing any file: list the folder. Two names for one job is the same
   defect as two files claiming one number.
5. **MISSING-ROW CHECK** on any rebuilt page: the rows that serve a decision must be ON it, by name.
6. **ONE BATCH GOES OUTSIDE.** Batch D is it.

**Write your findings to a numbered doc in `Source\`. Check the folder for the next free number
first**, and note that the free numbers are not contiguous, which is item 4.1 above.

**Report in §0.1 form: a numbered do-this list, then at most five short paragraphs. No em dashes.**

---

## SECTION 6. WHAT WOULD MAKE THIS AUDIT WORTHLESS

Say so plainly if you find yourself doing any of these, and stop:

- Reading a session doc and reporting that its numbers are internally consistent. They will be.
- Running a session script and reporting that it produces the number the session reported. It will.
- Confirming a fix exists in the source without seeing it change behaviour.
- Accepting a hash from this prompt without staging the file and computing it.
- Reporting a defect's severity without measuring it. Twice in this project a real defect had its
  cost overstated by 100x. Report the defect, then measure, then report the cost.
- [v2] Accepting the "prior" column in SECTION 0.1. It was written from the changelog, which is the author's account.
- [v2] Starting batch B before batch A's overview is written, or any batch after the sitting's budget is spent.
