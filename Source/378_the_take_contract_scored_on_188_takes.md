# 378. THE TAKE CONTRACT, SCORED ON 188 TAKES: NO ONE PART PREDICTS A CORRECTION, THE COUNT OF MISSING PARTS DOES, AND ONLY FIVE TAKES EVER CARRIED ALL FIVE

*19 Sept 2026, 18:30 ET. Fable, running SECTION C's "THE TAKE CONTRACT" from `Source\REDTEAM_TASKING_PROMPT.md`
at Matt's instruction ("I do want the red team referenced to be run by you"). The takes scored are the project
session's, not mine; where one of mine is in the population (the three handover test replies, docs 357, 361,
365) it is marked. Doc 377 is the previous number; 378 reserved by listing the folder. Deliverables (a) to (d)
are sections 2, 3, 5 and the last line.*

---

## 0. WHAT TO DO

1. **A rule changed, and it goes in the paste: SECTION 0.1 gains the take contract as a pre-send check,
   shipped as v9.9.** Section 5 has the block. It is the one instruction change this job earns and the
   measurement behind it is in section 3.
2. **The claim half-dies: no single part's absence predicts a later correction.** The largest single gap
   is THE MAN AHEAD, 45% corrected when absent against 29% when present, and it does not reach
   significance (p=0.16). The other four are within seven points of each other.
3. **The claim half-lives, and it is the useful half: the COUNT of missing parts predicts correction.**
   A take missing three or more of the five was later corrected 44% of the time; a take missing two or
   fewer, 21% (n=101 against 73, Fisher p=0.002). It holds inside claim/add/drop takes alone (58% against
   34%, p=0.045) and it disappears inside hold and do-not takes, which are rarely corrected at all.
4. **The falsifier did not fire, with one caveat that changes part 4.** Three of the four labelled takes
   were recoverable from files and none scores five of five. Two of them fail on exactly the part the
   correcting doc named (Vele: VINTAGE; Schultz: POPULATION). The third, Demercado, PASSED part 4 because it
   quoted a rule (keeper eligibility) while the rule that actually killed it (a second kicker is a wasted
   seat) was never touched. So part 4 now requires the roster after the move, not just a rule.
5. **The population hole, named: the Coleman cancel was never in a file.** One of the four labelled rows
   exists only as its correction (doc 370, and the to-do note). Every count below is a count of what was
   written down; 3 of 4 is the honest ceiling on recoverability for this project's chat-born takes.
6. **A number that must not be quoted: "takes carrying all five were corrected at rate X".** Only 5 of 188
   takes carried all five parts (or had a part not apply), so that cell cannot be measured. The contract has
   almost never been applied in full; the test is dose-response, not full-versus-not.
7. **Nothing to run.** The thing that must refuse to build is named in the last line and is not mine.

---

## 1. POPULATION, STATED IN FULL (section 0.6)

**What counts as a take:** the doc's own recommendation to Matt about one named player or D/ST unit, with
one of: claim, add, drop, start, sit, flex, hold, trade, cancel, stash, do-not-claim, do-not-drop. Not a
description of a move already made, not an arithmetic example, not a draft pick.

**Where they came from:** every numbered doc in `Source\` from 225 to 376 (149 files, 8 Sept 07:15 to
19 Sept 12:19 ET; 53 of them hold at least one take) and every `[ ]` / `[x]` item in `Source\matt_todo.txt`
as it stood at 12:19 ET on 19 Sept (22 items hold a take). The job's stated minimum was docs 340 to 375; that
window holds 34 takes, too few to test anything, so the population was widened back to the first in-season
doc. Docs before 225 are the draft, whose takes are picks and outside the contract's verbs.

**n = 188 takes.** 139 from docs, 49 from the to-do file. 10 are the handover test replies (docs 357, 361,
365, written by me as a test, marked in the CSV); excluding them changes no result. 14 takes are from 19 Sept
and nothing has had time to correct them; they are scored but held out of the outcome test, leaving **174**.

**Who scored them:** five reader sessions with no stake in the takes, one doc batch each, against a written
rubric (archived as `_archive\378_take_contract_reader_brief.md`), every PASS carrying a verbatim quote. I spot-read eight
scored takes against their docs: eight agree, one arguable (doc 371's Schultz add scored POPULATION FAIL on
numbers the doc itself says must not be quoted). I read docs 368, 370, 371 and 373 in full and the four
labelled takes score as section 4 says.

**How the outcome was set:** the readers extracted 70 correction statements ("retracted", "I was wrong",
"must not be quoted", "not X, Y") from the same docs and the to-do; I joined each take to any later statement
about the same player and action and assigned one of: CORRECTED (an error admitted), NUMBER RETRACTED (the
action stood, a number it rested on was withdrawn), REVERSED (the opposite recommended later, no error
admitted), OVERTAKEN BY EVENTS, STANDS. The main test counts the first two as "corrected". Every assignment
carries its evidence in the CSV.

**What is excluded and how big it is:** takes made in a chat reply and never written to a doc or the to-do.
The size of that exclusion cannot be measured from files; the four labelled rows put it at one in four.

---

## 2. THE SCORES (deliverable a)

`Source\take_contract_scores.csv`, 188 rows, 23 columns: source, date, player, action, the quote, the five
parts as PASS / FAIL / NA each with its evidence, the count of parts failed, whether the doc itself flagged
the take as a judgement, and the outcome with its evidence.

| part | PASS | FAIL | NA | FAIL as a share of applicable |
|---|---|---|---|---|
| 1 VINTAGE | 60 | 97 | 31 | 62% |
| 2 POPULATION | 27 | 68 | 93 | 72% |
| 3 THE MAN AHEAD | 38 | 103 | 47 | 73% |
| 4 THE STANDING RULE | 49 | 118 | 21 | 71% |
| 5 THE COUNTERFACTUAL | 80 | 108 | 0 | 57% |

Five takes of 188 carry every applicable part. Outcomes across the 174 testable: 50 CORRECTED, 9 NUMBER
RETRACTED, 25 REVERSED, 1 OVERTAKEN, 89 STAND. **One take in three was later corrected by its own author;
one in two if silent reversals count.**

---

## 3. THE TEST (deliverable b)

**Stated before the run** (from the job): takes missing one or more parts were corrected at a higher rate
than takes carrying all five, and one part's absence predicts correction better than the others.

**Per part, corrected rate when the part is absent against when it is present, n=174:**

| part | absent: corrected | present: corrected | gap | Fisher p |
|---|---|---|---|---|
| VINTAGE | 30 of 86 (35%) | 20 of 58 (34%) | +0 | 1.00 |
| POPULATION | 28 of 64 (44%) | 10 of 27 (37%) | +7 | 0.65 |
| THE MAN AHEAD | 45 of 100 (45%) | 10 of 34 (29%) | +16 | 0.16 |
| THE STANDING RULE | 42 of 114 (37%) | 15 of 40 (38%) | -1 | 1.00 |
| THE COUNTERFACTUAL | 37 of 102 (36%) | 22 of 72 (31%) | +6 | 0.52 |

**No single part carries it.** The man ahead is the biggest gap and is not resolved at this n. Under the
broad outcome (silent reversals counted too) POPULATION reaches p=0.037 (66% against 41%) and nothing else
does; one cell at one definition is not a finding.

**The count of missing parts does carry it:**

| parts failed | takes | corrected |
|---|---|---|
| 0 | 4 | 1 (25%) |
| 1 | 26 | 4 (15%) |
| 2 | 43 | 10 (23%) |
| 3 | 59 | 23 (39%) |
| 4 | 33 | 16 (48%) |
| 5 | 9 | 5 (56%) |

Point-biserial r = +0.25 between parts failed and a later correction, permutation p = 0.0015 (20,000
draws). Two or fewer missing against three or more: **21% against 44%, Fisher p = 0.002.** Same direction and
significant on docs alone (22% against 45%, p=0.006) and on claim/add/drop takes alone (34% against 58%,
p=0.045). It vanishes on hold, do-not and start/sit takes (11% against 15%, p=0.74): those are corrected one
time in eight whatever they carry, because a take that says "do nothing" has little to be wrong about.

**The confound, named:** action takes carry more numbers, so they fail more parts (mean 3.0 against 2.3) and
they are corrected more often (51% against 12%). The dose-response surviving inside the action takes alone is
what says the parts matter beyond that.

**What it does not say:** whether writing the five parts down would have PREVENTED the correction. This is
observational. Of the four testable takes that carried everything, one was corrected (doc 234's "do not
take Hockenson", reversed by doc 253), which is one in four against one in three, and n=4 says nothing.

---

## 4. THE FALSIFIER, APPLIED MECHANICALLY TO THE FOUR LABELLED ROWS

| the take | in a file? | score (V P M R C) | the part the correcting doc blamed | did the contract flag it? |
|---|---|---|---|---|
| drop Demercado for a kicker (doc 368) | yes | NA NA FAIL PASS FAIL | roster shape: two kickers | **no.** part 4 PASSED because keeper eligibility was quoted; the kicker rule was never touched |
| cancel the Coleman claim | **no**, chat only; doc 370 and the to-do hold the correction | not scorable | half the Spears rule: the man ahead | would have: part 3 is that rule |
| Schultz at 11.1 (doc 365 test reply; to-do lines 746, 766, 886) | yes | FAIL FAIL FAIL FAIL FAIL / FAIL NA FAIL FAIL FAIL | a base rate quoted as a forecast | yes: POPULATION |
| Vele at 5.8 (doc 371) | yes | FAIL FAIL PASS PASS PASS | vintage | yes: VINTAGE |

**Three of four recoverable from files. None scores five of five, so the contract is the instrument and the
job does not close on the falsifier.** The Demercado row is the correction to the contract: a take can
quote a rule and still break the roster, so part 4 must state the fifteen after the move against the caps
and the streaming rule, not merely name a rule it touches.

---

## 5. THE CONTRACT, AS A BLOCK FOR SECTION 0.1 (deliverable c)

Shipped into `00_PROJECT_DIRECTIVE.md` as v9.9, under 0.1, after (g). Worded so the writer checks before
sending, not after:

> **(h) THE TAKE CONTRACT. [v9.9, doc 378.] Before any player take leaves the reply (claim, add, drop,
> start, sit, hold, trade, cancel, stash), five lines sit beside the name, or the take does not go out:**
> 1. **VINTAGE.** Every number says which it is: `proj` (a preseason projection) or `2026, N games` (this
>    season, measured). A number with neither label is not a number, it is a guess wearing one.
> 2. **POPULATION.** A rate says whose rate it is and its n, and "a screen, not this man's forecast" when it
>    is a screen. If a second player prints the same figure, it is a base rate.
> 3. **THE MAN AHEAD.** For any back, and for any seat at any position: the incumbent's games missed and
>    current status, or the words "not checked". Never silently absent.
> 4. **THE STANDING RULE AND THE ROSTER AFTER.** The rule the take touches, quoted, and the fifteen after
>    the move against the caps and the streaming rule. Quoting one rule while breaking another is how a
>    second kicker got recommended.
> 5. **THE COUNTERFACTUAL.** What is given up, priced in the same unit as what is gained.
>
> **Measured, doc 378, on 174 takes 8 to 18 Sept: a take missing three or more of these was later corrected
> by its own author 44% of the time; two or fewer, 21%. No single line carries it. The count does.**

**Why a rule and not only the guard:** the guard named in the last line cannot see a take that is born in a
reply and never reaches a page or the to-do, and one of the four labelled failures was exactly that. The
rule is the only thing that reaches a reply.

---

## 6. WHAT ELSE THE SCORING FOUND, NOT ASKED FOR

- **Tight end is the position that gets corrected: 24 of 41 TE takes (59%), against RB 13 of 53, WR 18 of 44,
  QB 2 of 12, D/ST 1 of 19.** Hockenson, Schultz and Strange between them account for most of it, and the
  same three names were reversed and re-reversed across 234, 236, 253, 281, 308, 315, 337 and the to-do.
- **A take the doc itself flagged as a judgement was corrected MORE often, 38% against 30%.** Flagging is not
  protection.
- **The to-do carries takes and their corrections in the same file, 49 takes and 13 corrections**, and
  `open_threads.py` cannot tell one from the other. Doc 366 item 4 (tasks against notes) is the fix and is
  still not started.

---

## 7. OPEN, BY NAME

- The regression test on the v9.8 paste (doc 367 item 5): still NOT YET RUN.
- The other three SECTION C jobs: WHICH INSTRUMENT GOVERNS A TWO-SIGNAL PLAYER (queued; this doc's POPULATION
  result is a reason to run it next), THE OUTSIDE READ ON A PAGE THAT IS CORRECT ABOUT YESTERDAY, and THE
  DIRECTIVE READ BY SOMEONE WITH NO STAKE IN IT (last, not on the model that wrote it, which after v9.9 means
  not on me either).
- Whether the contract PREVENTS corrections: measurable only forward, by scoring takes made after v9.9 the
  same way. The CSV is the baseline.

**THE LAST LINE, AS THE JOB REQUIRES: this is finished when `Scripts\check_pages.py` refuses to build a page
that prints a rate beside a player's name without its vintage tag or its population (doc 373 section 5, doc
374 batches A and B), with the 18 Sept `WEEK_SHEET.html` as the negative control that must fail on Vele 5.8
and Schultz 11.1; and when `todo_page.py` refuses a `[ ]` line that names a player and an action without
the five lines under it. Both are the project session's under section 0.4 (doc 374 marks A and B "MINE, NOT
STARTED"), not Fable's, and until they fire this document is the brief for them, not the fix.**
