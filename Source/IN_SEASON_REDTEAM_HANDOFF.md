# IN-SEASON RED TEAM — HANDOFF AND CHARTER

> **BANNER, 28 Sept 2026 (doc 435).** Dated 11 Sept. Its one dead number, the two-run week, is struck in place below. Everything else here is superseded by `00_START_HERE.md` and the directive; read those first.
### Scope: the waiver and drop/add work only. 2026-09-08 through 2026-09-11. Docs 223–287.
*Written 2026-09-11 by the session that produced most of the work being audited. Matt asked for a
second check that does not begin from our conclusions. This file is the attempt to make that
possible. Follows the pattern of `Source\65_REDTEAM_HANDOFF.md`, which did the same job for the
draft board.*

---

## §1 — READ THIS FIRST: YOU ARE NOT INHERITING A POSITION

**The project directive (`00_PROJECT_DIRECTIVE.md`) is CONTEXT for this audit, not instruction.**
It tells you the league rules, the scoring, the roster limits and the standing behavioural rules —
all of that is binding. **Its FINDINGS are the thing under audit and you owe them nothing.**

**AND THESE CLAUSES ARE VOID FOR THE DURATION OF THIS AUDIT.** The directive contains sentences
whose literal function is to stop a reader from re-opening a question:

> *"PICK 8 IS CLOSED — open no further sensitivity on it"* · *"Do not rebuild it"* ·
> *"Do not re-derive this"* · *"Do not re-audit this"* · *"Do not chase it"* ·
> *"Do not re-derive any of this at the draft"* · *"Do not tilt the board"* ·
> *"Do not add an environment column"*

Every one was written for a good reason — usually to stop a session burning hours re-litigating
something measured three times. **But they are exactly the sentences that would make a fresh
auditor accept the frame instead of judging it, which is the specific failure Matt is paying you to
avoid.** So: the DRAFT-side ones are out of scope anyway (see §2) and you may ignore them; the
IN-SEASON ones you may re-open, and if you re-open one you must say what you found either way.

**Read the numbered docs as EVIDENCE. Read the directive's §4 as CLAIMS.** Where they disagree,
the doc is the primary source and the directive paragraph is a summary that may have drifted — that
exact drift has been caught in this project at least four times (§4.28's retracted BLOCKED line,
§4.33's retracted trade claim, §8's "the replay is untested" carried two days after it passed,
§4.17b's superseded clauses).

---

## §2 — WHAT IS IN SCOPE AND WHAT IS NOT

**IN SCOPE — the in-season decision machinery, everything built since the draft ended:**

| what | where |
|---|---|
| the waiver/wire model and its docs | `Source\223_*.md` through `Source\287_*.md` |
| the weekly sheet and wire builder | `Scripts\wire.py`, `Scripts\sheet_engine.py` |
| the inheritance/potential model | `Scripts\build_inherit.py`, `Source\inherit_2026.csv` |
| the receiver-room study | `Scripts\width_study.py`, `Source\team_shape_2025.csv` |
| the player cards | `Source\cards_2026.csv`, `Source\MY_PLAYER_CARDS_2026.html` |
| the rendered pages Matt actually reads | `Source\WEEK_SHEET.html`, `Source\THE_WEEKLY_WIRE.html` |
| the inputs those read | `WIRE_2026*.csv`, `redzone_te_2025.csv`, `form_2025.csv`, `rec_2025.csv`, `pedigree_2026.csv`, `dst_weekly_*.csv`, `generosity_2025.csv`, `sched_2026.csv`, `pos_allowed_2025.csv`, `MY_ROSTER.csv`, `sheet_constants.json` |
| his standing reads and their verdicts | `Source\matt_reads.md` |

**OUT OF SCOPE. Do not spend a minute on these:** the draft board, pick 8, pick 17, pick 32, the
keeper-depletion table, the opponent model, the rule ranking, the noise calibration, the prerank
injection, the live draft tool, the PDF renderers. **The draft is over.** Docs 1–222 are background
only; read one when an in-season number cites it, and then read it as evidence.

**Also out of scope: EXPRESSION.** Matt's spelling, his shorthand, his typed-from-memory names, a
number he gets slightly wrong where the intent is plain. §0.5(a) forbids correcting those and calls
it a waste of his time. **Challenge substance; never surface.**

---

## §3 — THE SELF-ASSESSMENT THAT PROMPTED THIS. IT IS THE REASON YOU EXIST.

Matt's words, 2026-09-11: *"you do a good job of catching stuff, but it's only after revisiting."*

**He is right, and here is the count that shows it. Every one of the last seven docs was triggered
by a question HE asked, not by my own review:**

| doc | what it found | who started it |
|---|---|---|
| 281 | the wire invented a free roster seat that did not exist | **Matt** — *"you said nothing on waivers but... add Tank Dell and move to IR. Which is it?"* |
| 282 | I recommended Brenton Strange 24 hours after retracting him | **Matt** — *"didn't we discuss him?"* |
| 283 | LaPorta's decline happened in 2024 and has been flat since | **Matt** |
| 284 | the receiver-room premise is right and the conclusion was inverted | **Matt** |
| 285 | three other receivers existed beyond Pearsall | **Matt** — *"Wasn't there the other WRs"* |
| 286 | the market already prices the Sutton doubt | **Matt** |
| 287 | Bryant competes with Franklin, not with Sutton | **Matt** |

**7 of 7.** My own red team in this session re-checked arithmetic and populations *inside* the frame
I had already chosen. It did not once question the frame unprompted. **That is the gap. Your job is
the frame.**

**The three error shapes that actually occurred here, so you know what to hunt:**
1. **A guard that runs and reports success while doing nothing** (doc 281: `rates()` silently drops
   a player with no projection, so a full roster read as having an open seat; the checker passed).
2. **A retraction that did not reach the code** (doc 282: doc 236 retracted Strange in prose; the
   wire still sorted tight ends by projected points, so he came back to the top of the sheet).
3. **The right arithmetic on the wrong object** (Hockenson priced as a bye-week fix when Matt bought
   him as a one-week blanket; the answer was correct and answered nothing he asked).

---

## §4 — HOW TO RUN IT (this is §0.5(c), and it is not optional)

1. **CATALOG FIRST.** Enumerate every candidate defect before investigating any. Ship the catalog on
   its own, so Matt can see the shape and re-order it. **Do not start fixing.**
2. **BATCH**, sized to finish. A half-finished sweep reads as coverage and is worse than a small
   complete one.
3. **Each batch ends in §0.1 form:** numbered do-this list, then what changed, what held, what is
   still open.
4. **COLLISION CHECK before writing any file:** `device_list_dir` the folder. The next free doc
   number is **289** (288 is this decision's own doc). `Source\` already holds two live collisions
   (`150_pick17_in_dollars.md` / `150_the_board_does_have_a_builder.md`, and
   `94_picks_17_and_32.md` / `94_picks_17_and_32_2322.md`) — do not add a third.
5. **MISSING-ROW CHECK.** After any rebuild of a page, verify by NAME that the rows which must be on
   it are on it. Row counts do not catch this; MarShawn Lloyd was rank 184 against a 180-row cut and
   Matt found him, not a guard.
6. **RE-DERIVE OR DECLARE.** For every number you rely on: either recompute it from the raw file, or
   write **`[INHERITED, doc N]`** beside it. An inherited number is not evidence. **Most of the
   thin ice in §6 is inherited numbers that were re-quoted until they felt measured.**

---

## §5 — THE STANDING RULES THAT DO BIND YOU

These are process, not conclusions, and they stay in force:

- **§0.1** — reply opens with a numbered do-this list, then 2–5 short paragraphs. Over ~25 lines of
  prose has failed. **SCOPE RULE: provenance goes in `Source\*.md`; a page Matt reads carries the
  instruction and the plain number and nothing else** — no section numbers, no doc numbers, no
  p-values, no sample sizes, no internal column names.
- **§0.1(f)/(g)** — one recommendation, not a menu; **proceed, do not wait for the go.** Report it
  done. The four things that still stop and ask: a waiver claim (~~one of two runs that week~~ a winning claim spends his priority for the rest of the week; there is one run, Thursday 03:00, docs 405 and 435) · a drop
  (can cost keeper eligibility) · anything that writes to ESPN · anything with money.
- **§0.2** — no untested claim in a recommendation. An exit code is not a result. A guard that has
  never fired is not a guard. Test the object PRODUCTION builds, not an equivalent one.
- **§0.4** — **do it yourself.** Matt does four things only: runs things needing his ESPN session on
  his machine, writes to ESPN, decides money/irreversible, supplies login-gated files. Everything
  else — reading, listing, grepping, staging, patching, committing, searching, arithmetic — is
  yours. Anything you ask him to run goes in `Source\matt_todo.txt` **the moment you say it**.
- **§0.5(a2)** — **state the testable form BEFORE you run the test**, in one line, and proceed in the
  same breath. This is the single rule that would have prevented the most damage in the work you are
  auditing.
- **§0.5(a4)** — every mechanism gets **TESTED** (population, baseline, n, direction, number) or
  **NOT YET RUN** (with the testable form written down) or **BLOCKED** (naming the exact missing
  input and whether you looked). **"That isn't measurable" is not an answer.** Seven times in this
  project the unmeasurable thing was two downloads away. **Before calling anything BLOCKED, list the
  folders for it.**
- **§0.6** — state the population every time, in every doc, including inherited ones. Name what is
  EXCLUDED and how big it is.
- **A5 clustering** — the unit for any team-level variable is the team-season, not the player.
  This has bitten the project four times.
- **§3 identity** — join on `espn_id`, or on name + position + team, never less. A name join that
  matches 100% today is still a defect.
- **Matt's standing instructions, verbatim:** *"Don't take my suggestions without using critical
  thinking, ever"* · *"Don't take what I say as truth!!! Important that you are suspicious of what i
  have provided before and next and act on intent instead of literal advice and direction"* ·
  *"Punting file movement issues back to me doesn't work and that's well establish."* ·
  *"instead of using google drive/cloud connector, i'd rather you use local drive connector access
  since that is lower cost"* · the ESPN cookies in the scripts are **approved and settled** — do not
  raise it again · *"Mike Washington Jr. - 0% chance i drop him."*
- **His record on mechanisms: 12 confirmed or partly confirmed, 1 underpowered his way, 7 null.**
  Better than a coin flip. **Never open by assuming his idea will die.**

---

## §6 — WHERE I THINK THE ICE IS THINNEST. START HERE.

*This is the one thing a stranger could not have written. These are mine, ranked, with what I would
attack first. If you only get through three, get through the first three.*

### (1) THE BAR FOR "STARTABLE" IS A PRESEASON PROJECTION, AND THIS PROJECT'S OWN MEASUREMENT SAYS PRESEASON PROJECTIONS RUN 8–14% HIGH. Everything in scope is scaled by it.

*I got this one wrong twice before writing it down, and both wrong versions are below, because the
shape of the error is itself evidence for why you exist.*

**WHAT IS ACTUALLY TRUE, verified against the spine this session.** `code_universe_v5.csv` reproduces
§4.1 exactly — QB12 Dart 341.603 · RB30 Jaylen Warren 168.589 · WR30 DK Metcalf 163.540 · TE12
Andrews 140.295, and Allen at 421.9 confirms §2's 6-point passing touchdown. Those are **full-season
(17-game) ESPN projections.** And doc 12's per-game replacement rates are **those same totals divided
by 17**, to three figures at all four positions:

| position | §4.1 season total | ÷ 17 | doc 12's "measured" ppg | implied divisor |
|---|---|---|---|---|
| QB | 341.603 | 20.094 | **20.09** | **17.00** |
| RB | 168.589 | 9.917 | **9.92** | **16.99** |
| WR | 163.540 | 9.620 | **9.62** | **17.00** |
| TE | 140.295 | 8.253 | **8.25** | **17.01** |

**Four independent measurements do not land on the same divisor to four significant figures. So doc
12's replacement ppg is a DERIVATION of §4.1, not a measurement of anything** — and that is why
§4.17 could not reproduce doc 12's sample sizes. **The directive calls these numbers "the position's
MEASURED replacement ppg" in §4.19, §4.31 and on the sheet. That label is false**, in the same way
§6's QB/TE doctrine was labelled "in his own words" when it was a paraphrase. §3 forbids it.

**AND THE SUBSTANTIVE PROBLEM, which is bigger than the label: the bar is what ESPN projected in
August, and §4.23 measured what ESPN's projections are worth.** Actual ÷ projected, on drafted
players with a preseason ADP: **QB 0.905 · RB 0.917 · WR 0.858 · TE 0.928.** Deflate the bar by this
project's own ratios and it moves a long way:

| position | bar in use | × §4.23 ratio | realized bar |
|---|---|---|---|
| QB | 20.09 | 0.905 | **18.18** |
| RB | 9.92 | 0.917 | **9.10** |
| WR | 9.62 | 0.858 | **8.25** |
| TE | 8.25 | 0.928 | **7.66** |

**The wire tells Matt a free agent is "not startable" against a bar that may be 8–14% too high, and
every "no" inside that band is a no he should have been given as a yes.** That direction is the one I
was least likely to find on my own, because the whole in-season frame I built is about protecting him
from bad adds.

**CLAIM IN TESTABLE FORM (§0.5(a2)), so you can redirect me in one word before spending the test:**
*Population — every QB/RB/WR/TE weekly line 2021–2025 scored under §2. Compute the 12th-best QB and
tight end and the 30th-best running back and receiver by REALIZED per-game rate among players who
actually occupied a starting slot, weeks 1–14. Baseline — doc 12's 20.09 / 9.92 / 9.62 / 8.25.
Direction — the realized bar comes in LOWER, and some share of the wire's current "not startable"
rows cross it.* If it comes in higher, the screen is too permissive and that matters just as much.

**THE TWO WRONG VERSIONS, kept on purpose.** My first was *"§4.1 ÷ 14 gives 12.04 / 11.68 / 24.40 /
10.02 and doc 12 says 9.92 / 9.62 / 20.09 / 8.25, so the project runs two disagreeing systems."*
Wrong — I had invented the ÷14 system myself by assuming §4.1's totals were a weeks-1–14 figure,
which they are not. My second was *"the bar may be too high or too low, unknown."* Also wrong, because
§4.23 already measured the sign and I had not gone to look. **Both errors were mine, both were inside
one hour, and neither would have been caught by the red team I ran on my own work — which is exactly
Matt's point.**

### (2) `inherit_2026.csv`'s gate is a MEDIAN being used as a PASS/FAIL BAR, on n=40.

§4.27 measured the median relief scoring across 40 RB takeover events at **11.2 half-PPR a game**
and doc 251 then turned that median into gate 2 of the inheritance list: *"the backup's best
consecutive two-week stretch last season averaged 11.2 or better."* **A median is the middle of a
distribution, not a threshold with a measured false-negative rate.** Half the events that DID flip a
job scored below it by construction. **THE TEST:** on the same 88 events, sweep the bar from 6 to 16
and report the hit rate and the count surviving at each. If the curve is flat, the gate is arbitrary
and should be a sort key, not a filter — which is exactly the `job_ceil`-alone error doc 251 was
written to fix, one level up.

> **[11 Sept, catalog D3: this item aimed at a gate that was already gone.]** Docs 275 and 276 had
> removed gate 2 from `build_inherit.py` before this charter shipped; 11.2 survives only as the
> `floor` label (`build_inherit.py:53`), and doc 275 had already tested the backup's prior form
> against relief scoring (rho +0.006, n=39) and swept the bar (8, 15, 20). The live defect was prose:
> directive §4.27's "applied form" (fixed in v9.4) and doc 281's description of 11.2 (corrected in
> place). Catalog B4 re-tests the fragility half on a population that includes starters hurt early.

### (3) `team_shape_2025.csv` is ONE SEASON used as a team trait, and I measured its persistence at r=+0.294.

Doc 284's receiver-room column on the wire comes from a single season of personnel shape. I ran the
persistence check and got **r=+0.294** — real but weak, and weaker than several traits this project
has refused to act on for exactly that reason (defensive quality at +0.204 was called "nowhere near
enough to carry the mechanism"). **THE TEST:** either add the 2022–2024 seasons and use a multi-year
mean, or strike the column. I shipped it on one season and the directive's own standard says I
should not have.

### (4) Doc 284 reports a significant player-level figure beside a clustered p=0.064 and leads with the significant one.

The receiver-room finding survives at player level and does not clear 0.05 once clustered by team —
and the room size IS a team constant, which is precisely the A5 case the project has been burned by
four times (vacated share, OL disruption, the positional tilt, PROE). **THE TEST:** re-read doc 284's
headline and decide whether it should be `[SUGGESTIVE]` rather than `[TESTED]`. I think it should.

### (5) n=15 carrying a 60% rate that is now quoted as a rule.

Doc 251's *"a first-round rookie receiver displaces the incumbent 60% of the time"* rests on
**fifteen players, nine of whom displaced.** The p-value is tiny because the contrast is enormous,
but the interval on 9/15 runs roughly 32%–84%. **It is now in the directive as §4.28 and it is being
used to price live players.** THE TEST: state the interval every time it is quoted, and check whether
any live recommendation would change at the bottom of it.

### (6) Doc 287's bar rests on 14 startable players out of 141.

The "a free agent gains value without passing the man ahead" finding — which I believe is correct in
direction and is Matt's own point — converts on **14 of 141**. Every subgroup cut inside it is
single digits. **THE TEST:** report the cells, not the rate, and say plainly which cuts are shapes
rather than findings.

### (7) The in-season screen's 33.3% vs 8.3% is quoted repeatedly without its n.

It appears in at least four docs and on the sheet. **THE TEST:** find the original, restate the
population and the sample size at every use, and check that the population has not silently widened
between uses — that is doc 228's exact failure mode and it is the one Matt caught from the outside.

### (8) Sutton's "median efficiency" is one season.

Doc 286's verdict that Sutton is median-efficiency and that the market prices the doubt correctly
rests on 2025 alone. Three seasons are on the drive in `pff_receiving_2022-2025.csv`. **Cheap to fix,
and I did not.**

### (9) THE PROCESS DEFECT, and it may matter more than any single number: the retraction path is broken.

Doc 282 happened because a prose retraction never reached a sort key. **THE TEST — and I think this
is the highest-value single thing you can do:** take every retraction in docs 223–287, grep the
scripts and the CSVs for the thing retracted, and report which retractions live only in prose.
`ERROR_PATTERNS.md` and `OPEN_THREADS.md` are the starting points. **A retraction that did not reach
the code is a live recommendation.**

---

## §7 — WHAT I DO NOT BELIEVE IS WRONG (so you can disagree with me on purpose)

Stated so you have something to aim at rather than an open field:
- **The seat arithmetic is now right.** Doc 281's fix ran four controls and CTRL2 reproduced the live
  defect before the patch. I would not re-derive it; I would look for the same class elsewhere.
- **The week-1 vs week-2 claim result** (9.4% vs 34.6%, Fisher p=0.010, n=718) is the cleanest
  in-season measurement here and it survived its own falsifier.
- **"The wire cannot upgrade a working slot, only fill a broken one"** reproduces from two
  independent directions (doc 259's roster comparison and §4.19's four-of-five RB record).
- **Matt's personnel-shape premise, his Bowers whole-room tax, and his "a player doesn't need to pass
  the man ahead" point are all confirmed.** Do not spend the audit re-killing his ideas; his hit rate
  on mechanisms is better than mine on frames.

---

## §8 — THE ONE THING TO SAY BACK FIRST

**Before any test: post the catalog.** Matt re-orders it, and that is the cheapest correction
available in this whole process. Then batch it.

*Inputs you may need and where they are: `G:\My Drive\_Fantasy\2026\Source\` (all data and docs),
`G:\My Drive\_Fantasy\2026\Scripts\` (all code). `py check_kit.py` pins the tree — never read a file
map out of prose. The local drive bridge is the channel Matt prefers; the Google Drive connector is
the most expensive one available and pulls whole files into context.*

---

## §9 — FOUND AFTER THIS CHARTER SHIPPED (added 2026-09-11, same evening)

*Two items that exist nowhere else. Added here rather than as a new file or a third tracker — the
project already pays for "two names for one job" (§4 of this charter, rule 4).*

**(1) WASHINGTON IS MISSING FROM THE SHEET AND MATT VERIFIED IT HIMSELF.** He was asked to Ctrl-F
`WEEK_SHEET.html` for a Commanders player and for "Washington". **Nothing came back.** So this is
confirmed by the artifact, not reported — 17 players and the Commanders D/ST are absent.
**THE COST IS NOT COSMETIC:** §4.33 measures D/ST as the ONE position where chasing the matchup is
the whole decision (108% of the player spread), and a week-9 second-defence add is on Matt's own
dated list. An invisible defence on the sheet that drives that call is a live defect.
**MY DIAGNOSIS, AND IT IS A DIAGNOSIS NOT A FACT — reproduce before fixing (§0.2):** the
`ESPN_TEAMS` / `TEAM_ALIAS` assertion added to `wire.py` on 2026-09-10 validates the 32 codes
resolved by `load_shape()` from `team_shape_2025.csv`. **It does not validate the team code on each
PLAYER row**, so a `WAS`/`WSH` mismatch on the player side never reaches the assert.
**AND THIS IS §0.2's OWN RULE BROKEN BY THE PERSON WHO WROTE IT:** the guard was proved by watching
it fire on `ARZ` and then called done. It fired against the wrong defect. **Check every other
`assert` added in the last four days for the same shape — proved on one path, trusted on all of
them.**

**(2) THE SHEET'S "DO NOT" ITEMS ARE OVER-FIRING. KILL THE PEARSALL SECTION.** Matt, 2026-09-11:
*"why does this get it's own section, lol. I'll obviously see he's on IR if i accidently do think to
add him — which i wont. you've mentioned like 4 times now."*
**He is right and it is a symptom, not a nit.** The negative-item machinery was built to stop the
doc-282 class of error (a retracted player returning to the top of a list) and it now spends the
scarcest space on the page warning him off things he was never going to do.
**THE RULE TO APPLY, and it belongs on the page generator, not in one deletion: a "DO NOT" line
earns space ONLY when the sheet is the only place that information exists.** Anything ESPN's own
player card already shows him — injury status, IR, ownership — is not a finding and must not take a
section. Audit every `DO NOT` / `screen` row on `WEEK_SHEET.html` and `THE_WEEKLY_WIRE.html` against
that test.

---

## §10 — THE INTANGIBLES: HOW TO FOLD COACH SPEAK, TEAMMATE QUOTES AND BEAT WRITERS IN (added 2026-09-11, at Matt's request)

*He cannot watch games and has said so repeatedly. News is his only channel to anything that is not
in a box score, so "the quotes aren't measurable" is §0.5(a4)'s forbidden answer. Below is the
measurable form, the intake filter, and two defects in the card that raised it.*

### (1) THE CARD THAT PROMPTED THIS, AND IT LEADS WITH THE WEAKER OF ITS TWO QUOTES

`cards_2026.csv`, Pat Bryant (DEN), carries two pieces of outside testimony:
- **Sean Payton:** *"rarely does he have to leave his feet to make a clean catch."*
- **Chad Jensen, Sports Illustrated:** predicts a break-out as the number three who *"will see the
  field often."*

**§4.28 already holds the table that ranks these, and it ranks them opposite to the order I printed
them in.** 4for4, 8 July 2024, year-over-year stability of receiver traits: **role / slot rate 0.75 ·
targets per game 0.70 · points per game 0.68 · aDOT 0.65 · targets per route run 0.64** at the top;
**TD rate 0.19 · drop rate 0.14 · contested catch 0.02 · route rate 0.01** at the bottom.
**Payton's quote is about HANDS — the 0.02–0.14 end of that table. Jensen's is about ROLE — the 0.75
end.** The coach's sentence is the one that sounds authoritative and the writer's is the one that
carries information, and the card leads with the coach. **That is the defect: I sorted by who spoke,
not by what the sentence was about.**

### (2) THE INTAKE FILTER. ONE RULE, APPLIED BEFORE ANYTHING IS LOGGED.

**LOG a quote only if it names one of: an alignment or role · a personnel package · a rep, snap or
route count · a depth-chart position · a named competitor.**
**BIN everything else** — hands, effort, "great camp", "best shape of his life", leadership,
maturity, and every adjective. Those are the bottom of the stability table and they are what a coach
says about everyone in August.
**The test is falsifiability in USAGE terms.** *"He's had a great camp"* predicts nothing and can
never be wrong. *"He'll be in our three-receiver sets"* predicts a snap count that exists seven days
later. Only the second kind is evidence.
**Matt's own tea-leaf list, sorted by that same table:** *not knowing the playbook · running the
wrong route · not being on the same page* are ROLE observations — top of the table, log them.
*Dropped balls · not making clean breaks · giving up on a play* are the 0.02–0.14 end — do not log
them, and do not let them move a decision. **His list was right in kind and mixed in quality, and
the table sorts it for him.**

### (3) THE OUTCOME SIDE COSTS NOTHING, WHICH IS WHY THIS IS BUILDABLE

**A logged quote is a PREDICTION WITH A DEADLINE.** Record: the date · the source and their role ·
the exact words · what it predicts in usage terms · the player's usage at the time. Then check the
route share or snap share **1 to 3 weeks later** and mark it hit or miss.
**The outcome half is already queued** — the weekly snap/route puller on the open list (nflverse
`offense_snaps`) for the LaPorta routes trigger. Same input, second consumer. **No new data source.**
Over a season that produces the thing this project has never had: **a measured hit rate per SOURCE
TYPE and per QUOTE TYPE**, on our own rows.
**`[NOT YET RUN — testable form stated]`** *Population: every logged quote 2026 weeks 1–14.
Baseline: the player's route share in the two weeks before the quote. Outcome: route share 1–3 weeks
after. Direction: quotes that pass the §10(2) filter beat quotes that do not, and head-coach quotes
beat beat-writer quotes — or they do not, which is the more interesting result.*
**Do not wait for a season of data to use it.** A ledger with ten rows and no verdict is still better
than a card that quotes a coach with no date and no consequence.

### (4) WHERE A QUOTE CAN BE WORTH ANYTHING, AND IT IS NARROW

**§4.22(b) measured that when the market and the projection disagree, the MARKET is right**
(rho −0.173, p<0.001, n=409). So for any rostered, widely-owned player the quote is already in the
price and reading it buys nothing.
**The exception is the only place Matt is shopping: a player at 1.9% ownership with no snaps to
read.** There is no market to fade and no usage to measure, so testimony is the only channel that
exists. **Value of a quote is inversely proportional to the player's current usage and ownership** —
which is the principled version of Matt's *"long shot, but if there is a shake-up I want to be
paying attention."*

### (5) THE MEASURED WARNING THAT MUST TRAVEL WITH ALL OF IT

**§4.22(a): coaching INTENT lost to game script in this project's own data** — corr(QB EPA per
attempt, pass rate) = **−0.184, p=0.038**, the opposite sign to intent, with defence at r=+0.104,
p=0.24 and the pair carrying R²=0.041. **A coach saying what he plans to do is a weaker claim than a
snap count showing what he did.** So the standing instruction: **coach speak is a TRIPWIRE that says
where to look. It is never evidence of a number, and it must never appear on a page beside a point
total as though it were.**

### (6) TWO OPEN ITEMS ON THE BRYANT CARD ITSELF

- **The depth chart and the alignment claim are not reconciled.** The news field says he is listed
  **third, with Mims starting ahead of him**; the signal field says he is **the only slot receiver in
  the room (57.8% slot, 10.0 aDOT)**. Both may be true — Mims can start wide — but the card never
  says so, and a reader cannot tell whether "third" contradicts "the only slot man." **Resolve it or
  drop one.**
- **The card's own bull line is a coach-tendency claim with no source:** *"the coach who decides his
  snaps has spent a career feeding big possession receivers."* That is exactly the kind of sentence
  §3 requires a source for and it has none. **Either cite Payton's actual target distribution by
  receiver size, or strike it.**

---

## §11 — MATT'S CORRECTION ON THE BRYANT ITEM, AND TWO TESTS THAT ARE NOT YET IN THE CATALOG (added 2026-09-11)

### (1) THE OBJECT WAS WRONG. BRYANT WAS AN EXAMPLE, NOT A PLAN.

Doc 290's reply opened by telling Matt not to swap Hockenson out for Pat Bryant and by holding that
move for batch 1. **He had not asked for that and was not going to make it.** In his own words,
2026-09-11:

> *"i was still on the fence with Bryant and was using it as an example to get ideas for additional
> indicators. With Waddle there, he'll eat up targets. If he was that good with a brain damaged Tua,
> image what he can do now, lol. Pat is likely a long shot but if there is a shake up there I want to
> be paying attention."*

**So: do not price Bryant, and do not re-check the Hockenson swap on his account.** What he is asking
for is **watch triggers and new indicators** — §10 is the method for the testimony half, and (2)
below is the measurement half. **This is §0.5(a2) in the audit itself: correct arithmetic aimed at a
decision he was not making.**

### (2) TWO TESTS, BOTH HIS, NEITHER IN THE CATALOG

**(a) A VETERAN ARRIVAL SQUEEZING THE ROOM BELOW HIM — the mirror of §4.28 and never run.**
§4.28/doc 245 tested an incoming **first-round rookie** displacing the incumbent. **Nobody has tested
an incoming VETERAN compressing the men beneath him.**
**Testable form:** *Population — every team-season 2021–2025 where a receiver with 60+ targets
elsewhere joined a team that already had a 60+-target incumbent. Baseline — the incumbent's and the
3rd/4th man's target share the prior season. Outcome — their share the following season. Direction
(Matt's) — the arrival compresses EVERYONE below him, not only the man at the top.*
**Why it decides his actual question:** if it holds, **Waddle hurts Bryant more than Sutton does**,
and the watch trigger is Waddle's snaps, not Sutton's health. Inputs are nflverse targets plus team
changes — nothing new to fetch. Cluster on the NFL team (A5).

**(b) RUN §4.30's THREE-SIGNAL COMPOSITE ON THE LIVE FREE-AGENT RECEIVERS.** It is a **39% screen**
(0% → 5.0% → 7.1% → **39.4%** as signals accumulate, p=0.0000, n=152) and it has been quoted at
Bryant rather than computed across the pool. **Say plainly whether it has ever been run on the 2026
free pool or only cited.** Inputs all on the drive: `pff_receiving_2025.csv`, `nfl_draft_picks.csv`,
`rec_2025.csv`. Report who clears 3 of 3 right now, Bryant included, and carry §4.30's own caveat —
Bateman cleared it twice and fell to 3.82.

**(c) AND THE ONE HE KEEPS ASKING FOR: which man's ABSENCE opens HIS job.** Alignment, not rank. If
Waddle takes the boundary and Bryant is the slot, then **Sutton going down is Matt's event and Waddle
going down is not.** The alignment column (slot / wide / aDOT on the wire's receiver rows) is already
on the open list; this is the decision it serves.

### (3) HOW THIS FILE IS MEANT TO REACH YOU — AND THE MISTAKE THAT MADE THIS SECTION NECESSARY

**This document is a FILE to be read, never a paste.** Matt's instruction to the audit chat is one
line: *read `Source\IN_SEASON_REDTEAM_HANDOFF.md` and follow it.* He should not be re-typing 28 KB
into a prompt, and nothing here is addressed to him.
**BUT THE FILE GREW AFTER IT WAS FIRST READ, AND A FILE ALREADY IN CONTEXT DOES NOT RE-READ ITSELF.**
The audit chat read the **19,865-byte** version. §9, §10 and this §11 were appended afterwards.
**So: RE-READ THIS FILE BEFORE THE NEXT BATCH, and check its size — if it is not 28 KB or larger you
are working from a stale copy.** That is doc 282's defect (a correction that never reached the
consumer) reappearing in the handoff channel itself, one level above the code.

**AND COMPACTION MAKES THIS MANDATORY, NOT ADVISORY.** The audit chat compacted on 2026-09-11. When a
conversation compacts, the earlier turns are replaced by a SUMMARY of themselves — so after
compaction that session holds **its own paraphrase of this charter, not this charter**, and **its own
paraphrase of the code it read, not the code.** §0.5(a2) names the failure exactly: *the paraphrase
IS the error mode.*
**THREE RULES FOLLOW, and they apply after every compaction:**
1. **Re-read this file.** A summary of a charter is not a charter.
2. **Re-read any code before fixing it.** Doc 290 states it *"confirmed each of these by reading the
   code."* After compaction it holds the verdict and not the lines. §0.2 already forbids a fix aimed
   at an unverified cause — and a remembered cause is unverified.
3. **Treat every number you can no longer point at a file for as `[INHERITED]`, not measured** (§4
   rule 6). That is the same test applied to your own recall.
**What survives compaction intact is what was written to a FILE.** `290_the_in_season_catalog.md` is
on disk and in the doc store, so the catalog is safe; a plan that had lived only in a reply would not
have been. That is the whole argument for catalog-first, restated as a property of the machinery.
