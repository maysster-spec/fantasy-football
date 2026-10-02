# 435. THE COLD AUDIT OF v9.13 TO v9.31: THREE NUMBERS FELL, TWENTY STOOD, AND TWO GUARDS HAD FAILED ON EVERY RUN SINCE 25 SEPT

*28 Sept 2026, 16:30 to 19:45 ET. Fable, in a fresh chat, on Matt's instruction: "see files in this order, red team all
and action all open items... I'll take your top recommendation without my input needed... You are the chief executive
and what you say goes." The files were `AUDIT_PROMPT_20260925.md` and `claude_todo.txt`. All five batches ran in one
sitting because he asked for all of them; the prompt's one-batch-per-sitting rule was a usage-budget rule and he spent
the budget. Every number below was formed by a session that had not read the doc, from the raw file, by its own code,
before the doc was opened. Directive v9.32. Number reserved by listing `Source\` and the store: the drive's newest
file was 432, the store's 425, and 434 was cited with no file, so 435 is the first free number.*

---

## 1. DO THIS, IN ORDER

1. **Wednesday night: a DIFFERENT drop on every claim.** You have 15 active men and all three IR seats are full, so
   a claim with no drop fails on the roster limit. Measured on waiver claims alone: **16.2% of no-drop claims fail
   (24 of 148), 0 of 502 with a drop.** The 6.1% the directive carried counted 247 free-agent adds that cannot fail.
   And **one drop covers one claim**: all 103 failures of drop-carrying claims were a second claim in the same run
   naming the drop the first claim had already spent. Your to-do line said "no drop on the one you rank first"; it
   is replaced.
2. **A man dropped on Wednesday clears Friday about 03:00, not Thursday.** The two-day period is per player. The
   66 Friday-to-Sunday runs are single-player clearances (1.7 claims each). Check the roster Friday morning too.
3. **Run `.\ff.bat`.** The kit check and the page check had failed on every run since 25 Sept (stale pins on
   `sheet_engine.py` and `ff.bat`; a roster-clock link prefixed `Source/`). Both are fixed. `OPEN_THREADS.md`
   rebuilds inside it now and no longer eats its own output.
4. **Paste directive v9.32 into the project's custom instructions.** The header now carries three new
   DO-NOT-QUOTE rows (below) and five draft-era rows moved to the top of `DIRECTIVE_FINDINGS.md`.
5. **Do not quote:** *"6.1% failure without a drop"* (16.2% on waiver claims); *"a QB2 held from week 10 captures
   96% of a season's missed starts"* (66%: 2.57 of 3.89 missed weeks, weeks 10 to 17 over 1 to 17; the 96% divided
   by the weeks-1-to-14 total); *"two ordinary tight ends platooned pay +0.50"* and *"the pairing payoff crosses
   zero near a 1-point gap"* (+0.50 used the season's matchup averages including the game being scored; on prior
   weeks only it is minus 0.03, and the six-row chart mixed three baselines). The roster clock page is corrected.
6. **The week-10 QB2 is insurance worth about two thirds of a season, not nearly free.** Doc 431's "flips the
   verdict" is withdrawn. Hold one if a bench spot is spare; do not cut a real player for him.
7. **Nothing else changes what you do.** The Thursday run, the seat curve, the kicker replacement, the riser, the
   softest-matchup rule and the elite-plus-streamer penalty all reproduced.

---

## 2. BATCH A. THE HANDOVER AND THE RESIDENT SET

| change | verdict | evidence | done |
|---|---|---|---|
| DO-NOT-QUOTE reach check, scripted over all 456 files in `Source\` and `Scripts\` | **worse than the prompt assumed, in the findings file** | `DIRECTIVE_FINDINGS.md` 4.36(a) and (f) still carried "PLACE CLAIMS SUNDAY NIGHT" and the placement-day model unstruck under a section banner; the changelog's v9.15 entry carried the standing instruction unstruck; `IN_SEASON_REDTEAM_HANDOFF.md` carried "one of two runs that week" live; docs 255, 134, 181, 57 and 70 minted dead numbers with no banner | all struck in place or bannered. START_HERE v13 and the directive were clean |
| store copy of the directive against the drive | neutral | the store copy read whole (25,000 tokens, the prompt's own warning): same text start to end; byte identity not machine-checked because `project_read` returns to context, not to a file | v9.32 is pushed to the store from the same file, so the two are identical by construction |
| `check_citations.py --selftest` and run | held | selftest fires on the injected dead id; the live run was clean on `§4.x` | extended to `doc N`: selftest fires on doc 999, live run found **fourteen** dangling numbers |
| the six fileless doc numbers | **worse: fourteen, not six** | 413, 414, 424, 426, 429, 430 as listed, plus 433 (`check_inputs.py`), 434 (`snaps_2026.py`, `claude_todo.txt`), 311, 316, 317 (cited in `check_kit.py`, `wire.py`, `sheet_engine.py` since mid-Sept), and **242, 243, 244, which exist in the store and not on the drive** | 242 to 244 exported to `Source\`; the other eleven written as stubs that quote only their citing comments and say so at the top |
| the directive header: 41 lines against §9 rule 7's ~20 | **the cap was wrong, not the table** | the rule was written before the table existed; a retraction is actionable and stays resident | rule 7 now excludes the table's rows from the count and sends draft-only rows to the findings file; header is 24 lines outside the table, 14 rows in it |
| `OPEN_THREADS.md` dated 20 Sept, no `ff.bat` step | held, and a second defect | `open_threads.py` scanned its own previous output as a doc: 42 garbage rows nested per run, 368 KB on 20 Sept, 460 KB after one more run | own output skipped; step added to `ff.bat` with an RC; rebuilt: 79 KB, 45 open, both to-do lists at the top |
| `claude_todo.txt` against `matt_todo.txt` on the claim-order item | reconciled | `claim_order_log.py` exists (23 Sept) and records the order at placement; nothing joins it to the outcome | the item now says that |

## 3. BATCH B. THE WEEK SHEET

Built offline from the 20 Aug pull plus a `byes_2026.csv` derived from `sched_2026.csv` (the container had no
in-season pull); everything that depends on the 24 Sept pull is marked.

| claim or fix | verdict | evidence |
|---|---|---|
| `norm_name` on the form join (doc 427) | **fires** | post-fix 0 RB/WR/TE rows carry `proj` with a form row under the normalised name; the pre-fix raw lookup misses the same nine men doc 427 named (Jones Sr., Robinson Jr., All Jr., Cook III, Pitts Sr., Pittman Jr., Gadsden, Etienne Jr., Tre' Harris). The join is still name-only, not name + pos + team; 0 collisions today |
| the seat gate reads `tm` (doc 427) | **fires** | on production-shaped rows with the live team patched in, it cuts Emari Demercado ("he is on DAL now, not KC") and prints four seats; 11 of 14 live seat rows are examined, three never reach the page |
| the doc-426 key contract in `render()` | **dead code, moved** | a `team`-shaped row raised `KeyError: 'tm'` from the free-pool table a thousand lines earlier; the named assertion could never print. Moved to the top of `render()`; the negative control now prints its own message, and the page still writes on good input |
| C1, the rest-of-season divisor | confirmed in code | `proj_games(3)` = 15, `proj_games(4)` = 14; the two-pull identity needs two in-season pulls and the container had none |
| C2, Kyle Pitts Sr. 7.89 to 5.41 | consistent, exact value blocked | 0.36 x 1.0 + 0.64 x 7.89 = 5.41 reproduces the arithmetic; 7.89 x 15 is the 24 Sept pull's projection, which was not on hand |
| the IR box | **status first, occupancy second, and correct today** | "no one can be moved" is decided by the status string; `free_slots` only chooses the wording once someone is eligible. Nacua, Dowdle and Coleman are all in slot 21, so the headline is true. Fixed: the plural ("are already parked"), and the healthy-man-in-the-slot case now says no claim will process |

## 4. BATCH C. THE NUMBERS THE RULES REST ON

| doc | claim | reproduced | verdict |
|---|---|---|---|
| 405 | 626 executed claims; 86.3% Thursday 03:00 to 06:00 (115 / 117 / 158 / 139 / 11); zero Mon to Wed | 626; 540 = 86.3%, same by season; zero, also zero among all 1,131 processed | **AGREE, exact.** New: Wednesday placements 176 not 174 (four unprocessed 2026 rows since the doc); a Wednesday drop clears Friday |
| 393 | 884 / 0 with a drop; 371 / 24 (6.1%) without; Matt 8 of 24 | counts exact; **the rate is diluted**: 247 of the 371 are free-agent adds with no processing step. Waiver only: 124 / 24 = **16.2%**, 19.5% with position-limit failures | **DISAGREE on the rate.** Rule strengthens. Also: uncontested claims with a fresh drop and room land 98%, not 76% |
| 401 | 28.6% of player-runs contested; uncontested wins about 3 in 4 | 213 of 745 = 28.6%; 76.1% | AGREE |
| 399 | w+1 Out 38.9 / Q 19.5 / D 3.4 / none 38.2; seat valid 75.5 / 51.2 / 35.2 / 26.4 / 22.2; freeze 24.5%; RB 20.3 QB 22.4 TE 24.9 WR 26.1 | all to the decimal under the script's rule on a fresh nflverse download; within a point under a stricter reading; the population includes 34 fullbacks | AGREE. The designation files are not on the drive; the script downloads them |
| 423 | K12 8.26, sd 0.16; K1 9.9 to 12.5 | 8.26, sd 0.16 (8.46 / 8.08 / 8.38 / 8.08 / 8.31); 9.85 to 12.56 | AGREE |
| 385 | +36 (9 to 56, n=138); 54% / 30%; 2021 minus 11 per ten | +35.6 (se 11.7), floor 8.6 to 9.3 by seed; 54 / 30; minus 11.0 (se 9.2); shares rebuild exactly from the cache | AGREE on the finding. **The registry claim does not fully hold: 2021's AVG is not derivable from its own columns** (200 of 495 rows have an AVG and no site value); 2025's MANIFEST label wrongly includes Real-Time |
| 389 | base 4.3%; WOPR top fifth 10.1%; targets 6.7% in the cross | 4.3%; 10.2%; **the cross table is targets x WOPR, mislabelled as targets x air-yards**; on the true cross targets-only is 8.0% | DISAGREE on the label; 4.35's "weak half" line weakened, not killed |
| 427, C4 | elite slope 0.448 vs streamable 0.216, difference null | identical under the script's definitions; roughly half the size with prior-weeks generosity, still null | AGREE |
| 427, C5 | softest streamable QB +1.93 (se 0.90) | +1.93 with season averages; **+1.75 to +2.01 (se 0.88) with prior weeks only** | AGREE; quote the ex-ante number on a page |
| 428, C6 | elite QB1 plus streamer platoon minus 2.31 (se 0.35) | identical; minus 2.59 over weeks 2 to 14; minus 5.63 with a top-3 elite | AGREE, stronger |
| 428, C7 | two streamers +0.31 (se 0.23) | identical (rebuilt; no script holds it); +0.12 ex ante | AGREE, a null with a tilt |
| 428, C8 | TE: elite minus 0.86, mid minus 0.37, two streamers +0.50 | arithmetic reproduces; **`te_pair.py` uses the in-sample season mean while its docstring says leave-one-out**; ex ante minus 1.77 / minus 0.95 / **minus 0.03** | **DISAGREE on substance** |
| 428, C9 | monotone in the gap, crosses zero near 1 point | the six rows come from one 2026 forecast, three in-sample TE rows and two ex-ante QB rows: three baselines, three windows, two instruments | **not comparable.** Bigger gap worse stands; nothing positive at zero gap |
| 431, C10 | QB starter missed weeks 6.2% / 29.9% / 44.6%, n=160 | reproduces; "missed" is "not the team's top-scoring QB that week", the highest of three definitions | AGREE on the rise; levels are definition-dependent |
| 431, C11 | week-10 QB2 captures 96% (2.57 of 2.67) | **2.67 is the weeks-1-to-14 total; the full season is 3.89; the share is 66%** (67% under did-not-play) | **DISAGREE.** "Flips the verdict" withdrawn |
| 431, C12, C13 | D/ST 13.5 to 13.6 usable; K 15.4 to 14.2 | reproduce as raw counts; the "minus 12" floor is stated separately; the script deducts missed PATs, which §2 does not score; the D/ST file has no blocked-kick or fumble-lost term | AGREE, two small notes filed |

Twenty-three claims: twenty agree, three disagree on the number or its meaning, and each of the three sat under a
standing rule or on a published page. All three were arithmetic or instrument errors, not data errors: a wrong
denominator, a diluted population, and a lookahead in the generosity term.

## 5. BATCH D. THE DIRECTIVE DIET, SIZED AND CLASSIFIED, DIFF NOT WRITTEN

The file is 96,308 bytes after v9.32, about 24,000 tokens on every turn of every chat. The v9.13 and later material
is about 29.8 KB, 7,400 tokens. Classified by block (RULE = a sentence a session must obey; STORY = how it was found):

| block | bytes | RULE share | what would move to the changelog |
|---|---|---|---|
| §2 IR seat, clock, IR rules, seat curve, claim order, missing drop (v9.15 to v9.26) | 13,561 | about 45% | the v9.15 preamble, "WHERE THE MISREADING WAS", the struck seat curve and its six population definitions, the claim-order permutation story, Matt's quoted mechanic. The rules (IR takes Out or IR only; upgrade to Q/D is safe; place Wednesday; a drop on every claim; the 24.5% Sunday check) fit in 3 KB |
| §9 rule 7 header budget (v9.23) | 2,960 | about 25% | the Keep-a-Changelog and context-rot citations and "the part that is mine" |
| §0.5(a6) answer the question he asked (v9.27) | 2,347 | about 40% | THE CASE paragraph; keep the four steps |
| §0.5(a5) measure the claim (v9.16) | 1,823 | about 35% | the 4.36 narrative and the tone paragraph's example |
| §0.5(a7) the decision not the coefficient (v9.30) | 1,823 | about 30% | the whole first paragraph is the case; keep THE TEST and the tone half |
| §0.5(e) v9.31 claude_todo mirror | 1,826 | about 40% | the six-days-stale story; keep THE RULE and the §0.1(g) line |
| §9 rules 5 and 6 (v9.17) | 1,419 | about 50% | doc 391 and the 134-edit story |
| §0.5(a) v9.17 em-dash bullet | 808 | about 30% | the whole bullet is a case; the rule is one sentence |
| §2 v9.29 kicker replacement, §1.1 v9.13 registry, §9 rule 2 v9.28 | 2,184 | about 60% | the quotes and dates |

Rough price of the cut: about 16 KB, 4,000 tokens a turn, 17% of the file. Not applied: the prompt asked for a diff for
Matt, and writing it well is a sitting of its own. On `claude_todo.txt`.

## 6. BATCH E. THE GUARD KIT

| item | verdict | evidence |
|---|---|---|
| `check_guards.py`, eight mutations | **7 of 8 survive, doc 425 confirmed** | only "blend switched off" is caught (by `check_vintage.py`). The harness silently skips a guard named in GUARDS and absent from disk (line 137); `check_sources.py` cannot catch an engine mutation by construction, it never opens the page |
| `make_online.py`, four refusals | **2 of 4 fired; 2 could not** | page bar stripped and outer document surviving both refuse with a non-zero exit. The build-stamp guard tested a string the script inserts itself and passed with "an unknown time": fixed, it now refuses. The roster-clock guard checks the script's own constant, not the input: left, documented |
| `check_pages.py` C3 on COMMANDS.html | **true positive; `make_commands.py` was wrong** | it prefixed every to-do link with `Source/`, including the https roster-clock URL that doc 429 had already exempted in `sheet_engine.py`. Fixed; check_pages was right |
| `ff.bat` | pure CRLF (150 of 150); RC8 in RESULT; **RC5B (check_sources) was not** | RESULT line now carries sources and threads; 159 CRLF lines, 0 bare LF |
| `check_kit.py` | **had failed every run since 25 Sept** | wanted 205,458 / f951ff91 for `sheet_engine.py` and 7,756 / c2212c86 for `ff.bat`; the shipped files were doc 432's and doc 430's. Re-pinned to the files shipped today. A guard that always fails is a guard nobody reads |

## 7. WHAT SHIPPED, AND HOW IT WAS VERIFIED

Every file below was committed from a fresh container path, staged back and hash-compared (§9 rules 1 and 2);
canonical files were archived to `_archive\` with a `_20260928_pre435` suffix first.

Scripts: `sheet_engine.py` (key contract moved; IR box plural and claims-will-not-process sentence), `ff.bat`
(open_threads step; RESULT carries sources and threads), `make_commands.py` (absolute URLs kept as is),
`research\open_threads.py` (skips its own output), `make_online.py` (refuses a page with no build time),
`check_citations.py` (doc N coverage, selftest), `check_kit.py` (three pins).

Source: directive v9.32, changelog (v9.32 entry; v9.15's standing instruction struck in place), findings (draft-era
retractions block; 4.35 and 4.36 corrected in place), `00_START_HERE.md` v14, `matt_todo.txt`, `claude_todo.txt`,
`OPEN_THREADS.md` rebuilt, `AUDIT_LEDGER.md` rows 189 to 193, this doc, docs 242 to 244 exported from the store,
eleven stub docs, banners on 255, 134, 181, 57, 70, 385, 389, 393, 427, 428, 431 and `IN_SEASON_REDTEAM_HANDOFF.md`.

Store: every canonical file above, this doc, the stubs, and docs 427, 428, 431, 432 which the store did not hold.

Published: the roster clock (`claude.ai/artifact/NpLWo1xBiWRG4bztW7L5xw`): the 96% card, the pairing chart, the
tight-end verdict row and the drop rule row corrected.

## 8. STILL OPEN, BY NAME

The directive diet diff (batch D); the outside-check batch (§0.5(c)6, not run here); `te_pair.py`'s leave-one-out
fix and doc 428's tight-end rows from a real run; the registry AVG guard; `check_guards.py` reporting a missing
guard; the two-pull identity for C1 and Pitts' 5.41, which need the 7 and 24 Sept pulls; the delta-not-level test;
the red-zone term; ADOT and air-yards share into `build_form.py`; the spot-check card; the pocket-sheet builder
question. All on `claude_todo.txt` with their testable forms.

## 9. THE ONE LESSON

Of the three numbers that fell, two were denominators and one was a lookahead. None would have been caught by a
guard that recomputes from the same script, which is doc 425's finding again. What caught them was a stranger
rebuilding the number from the raw file before reading the doc. That is cheap enough to repeat: one sitting, five
subagents, twenty-three claims.
