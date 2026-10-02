# START HERE

*Version 24, 2 Oct ET, 02:20: **directive v9.39 is pasted** (confirmed in the project's instructions header), **the project store is at 68%** (doc 471: docs 200 to 299 moved to `_archive\store_20261001\claude\`, hash-verified three ways and deleted; doc 473: the five docs outside `claude/` moved to `_archive\store_20261002\`; doc 290 stays because a content classifier stops every model copy of it, and the next trigger is about 10 Oct). **What the night changed that a fresh chat must know:** the week sheet's roster table and drop ladder print a matchup number beside every back's and tight end's rate (doc 472, finding 4.49; nothing prints until a defense has four finished weeks, and `check_page_logic.py` P11 holds it to the files); P12 and P13 hold doc 457's two rules (a second tight end never on THE CALL this week; the total counts this-week rows only), 72 controls; **nflverse had not posted week 4 as of 01:40 on 2 Oct**, so every "this season (3 g)" cell, the blend weight and the matchup column stand on three weeks until `build_form.py` picks it up on a scheduled run, and the first four-week build is the one to read (doc 472 section 4: on a synthetic fourth week THE CALL chained a displaced starter as a later drop and P5 fired; decide then, not before). Two lines wait for v9.40 in one paste: the 4.49 index row no longer says NOT YET RUN, and 9 rule 5 gains "a banner applied in Source is pushed to the store the same turn" (doc 255's store copy sat three days without its banner). Newest doc 473. Version 23 (1 Oct 20:30) recorded v9.39, the card, the live playoff number and `audit_directive.py` clean in season (docs 464 to 469); versions 14 to 19 the cold audit and its sequels (docs 435 to 446), whose four retractions (16.2% not 6.1%; 66% not 96%; the pairing chart's +0.50; one drop per claim) stand in the directive's DO-NOT-QUOTE table. **Bump this stamp in the same commit as any edit.** The newest numbered doc whose title says what is open beats every tracker in section 9; as this version ships that is doc 473.*

---

## 0. WHICH READER ARE YOU. SORT BY YOUR TOOL LIST, NOT BY WHAT YOU ARE CALLED.

- **Are `mcp__remote-devices__*` tools in your list?** Then section 4 applies to you, whatever you
  are called. Stage what you need in one call.
- **Not there?** Section 4 does not apply. **The project doc store (`claude/...`) holds the DOCS from
  200 on and not the DATA** (no roster CSV, no wire, no snap counts). **Docs 1 to 199 and the pre-draft
  data left the store on 22 Sept (doc 384)**; they are on the drive at `_archive\store_predraft_20260922\`
  and their findings are in `Source\DIRECTIVE_FINDINGS.md`, so a pre-draft doc number in a finding is a
  citation you can read only with the bridge. Say so rather than guessing at what it said. **Name the exact file from section 6 and
  ask Matt to attach it. Do not invent a path and do not say you looked.** Do NOT reach for the
  Google Drive connector: the directive's SECTION 9 forbids it for file work because it pulls whole
  files into context.  **And before you ask for anything: `.\ff.bat` rebuilds the pages that answer most questions
  without you. Point him at that first.**
- **Is `00_PROJECT_DIRECTIVE.md` already your system prompt?** Inside this Claude project, yes.
  Anywhere else, read it first; nothing below makes sense without it.

**PRECEDENCE, BECAUSE TWO RULES IN THIS FILE CAN BOTH APPLY TO ONE NUMBER: a generated page wins on
STATE, and an `[OPEN]` row in `AUDIT_LEDGER.md` wins on the page.** A page is rebuilt from the live
pull so it knows today; a ledger row marks a defect the page still carries. **Example: ledger row
108, a name join that prints one back on the wrong team; check whether it is still open before
quoting it.**

**THIS FILE GOES STALE AND HAS TWICE BEFORE.** So **nothing here
states the state of the season, the roster or the numbers.** It states where state LIVES. On a
disagreement: a generated page beats this file, and a higher doc number beats a lower one.

---

## 1. ESTABLISH THE DATE BEFORE ANYTHING ELSE. IT IS NOT IN THIS FILE.

```
device_list_dir  G:\My Drive\_Fantasy\2026\Source      read the MTIMES, not the names
```
**Those filenames carry the day `ff.bat` LAST RAN, not today.** Five scheduled runs call it (section 5);
the daily 07:30 one was added 19 Sept (doc 374) and **whether it is registered is visible only in Task
Scheduler, never in any file** (doc 377). `WEEK_SHEET.html` carries its build date in the masthead. **Compare the newest date against today before using anything, and if they
differ say so out loud.**

**AND ONLY EIGHT OF THE FILES IN SECTION 6 ARE ON THAT CADENCE AT ALL.** `ff.bat` writes
`MY_ROSTER`, `LEAGUE_ROSTERS`, `WIRE`, `FREE_UNRANKED`, `LINEUP_CHECK`, `WEEK_SHEET`, `MY_TODO` and
`THE_WEEKLY_WIRE`. **Nothing rebuilds `injuries_2026.csv`, `depth_map.csv`, `inherit_2026.csv` or `sched_2026.csv`,
so their mtimes are the last time a human touched them. `waiver_report_2026.csv` is rebuilt only by
`py waivers.py --live`, which needs his ESPN cookies and is his to run.** The transaction file's last
event date is the only clock it has, and the roster can be a day or more ahead of it: a move that is on
the roster and not in that file happened after its last pull, and no file says how. **A claim appears
twice in it, once PENDING at filing and once EXECUTED at the run; count the EXECUTED row.** His Coleman
claim: filed 18 Sept 23:07, executed 19 Sept 03:11 ET, both rows present in the 11:50 pull.
**`injuries_2026.csv` is the live trap: it holds ONE WEEK's report and no more.** The file mtime
tells you it is old; it does not tell you the current week is simply absent. **Never answer "who is
hurt" from it without checking which week it covers.**
**AND ON A TUESDAY `LINEUP_CHECK.html` CAN SAY "ALL CLEAR" ABOUT A STARTER WHO JUST SAT OUT.** It reads
ESPN's designation, and at 06:00 on 22 Sept it said everybody was expected to play while Puka Nacua had been
inactive on Monday night (groin). Until the Wednesday practice report, look for a starter with NO row in the
last completed week of `form_2026.csv` and check the news on him (doc 385).

**NO DRIVE TOOLS? THEN YOU HAVE NO DATE ROUTE AT ALL. ASK HIM: what week is it, and has `ff.bat`
run today.** Two facts, one question, and everything below depends on both. Do not infer the week
from your own clock and present it as known.

**THE FRESHNESS RULE, AND IT APPLIES TO EVERY FILE BELOW, NOT JUST THE PAGES.** A file written
before the last game that has been played describes a world that no longer exists. **The specific
trap: `injuries_2026.csv` written Sunday night shows a man healthy who got hurt on Monday.** Check
the mtime against the schedule before you answer any question about who is hurt, who is free, or
who is playing. Say the file's date out loud when it matters.

---

## 2. THE DURABLE SPINE. The only facts here with no expiry.

**Matt Mays, team JUG, "The Poetry of Junkyard Juggers", slot 8 of 12.** ESPN, 0.5 PPR, 6-point
passing TDs, 14-week regular season, 6-team playoff weeks 15 to 17.

**Roster 15: 9 starters (QB, RB, RB, WR, WR, TE, FLEX, D/ST, K), 6 bench, 3 IR.** Position caps
**QB 3, RB 6, WR 6, TE 3, D/ST 3, K 3.** A full roster means **any add needs a drop**, and the drop
is the irreversible half.

**Keeper: George Pickens.** One per team, costs a round-15 pick, must have been drafted round 5+
and rostered all season. Waiver pickups are never keeper-eligible.

**THE IR SLOT IS A HELD SEAT AND HE USES IT THAT WAY (docs 390, 391, 394; his words, 22 Sept):** a man ruled out
before the game can sit there and **he does not occupy one of the fifteen**. Puka Nacua has been in it since 22 Sept.
**Count the active roster from `MY_ROSTER.csv`'s `slot_id` column**; before that column existed, doc 388 counted him as
active and got the number of drops wrong. **A claim carrying its own drop KEEPS the free seat; a claim without one
spends it.**

**THE RULES ARE SOURCED NOW AND THREE OF THEM REVERSED ON 22 SEPT (doc 394, v9.19). Everything in this table is
verbatim from ESPN > Fantasy FOOTBALL > Managing Your Team, *Players on Injured Reserve (IR)*, read as page text.**

| the state | what happens |
|---|---|
| **Out (O) or Injured/Reserve (IR)** | the **only two statuses the slot accepts** |
| **Suspended (SSPD)** | ***"NOT eligible for IR on FFL."*** cannot be parked at all |
| **OUT/IR → QUESTIONABLE or DOUBTFUL** | **SAFE.** The roster is ***"NOT invalid"***, he keeps the seat, and he ***"can make claims/add players, adjust their lineups as they wish"*** |
| **OUT → no designation at all** | **THE ONLY BREAK.** The roster goes ***"INVALID"*** and the lineup is FROZEN until he cuts someone. **This is his lock** |
| **a healthy man already in the slot when a claim is entered** | ***"If you have a healthy player in IR, the claim will not process."*** Clear the slot BEFORE entering claims |

**WHAT THIS FILE TOLD YOU UNTIL 23 SEPT AND WHICH IS WRONG — all four retracted at v9.19, and this file carried them
for sixteen hours after:** ~~ruled Out then upgraded in-week flips any day and nothing protects you~~ (an upgrade to
Questionable or Doubtful is explicitly safe, and it is the most common upgrade there is); ~~the 19.5% downgraded-to-
Questionable cell is a quiet failure, seat gone~~ (he keeps the seat); ~~suspension/PUP/NFI is safe at any placement
day~~ (**SSPD is never eligible**; PUP and NFI are not addressed by that page either way, so NOT ESTABLISHED); ~~still
BLOCKED: which designations this league accepts~~ (**closed, doc 394**). **Never quote an ESPN support page through
`WebFetch`, and check the breadcrumb for the SPORT — the page that looked like a contradiction was Fantasy Women's
Basketball.**

~~**THE CLOCK IS THE WHOLE MECHANIC, AND IT IS NOT A WEEKDAY. `Waiver Period: 2 Days`** (settings line 125): a claim
placed on day D runs on the morning of **D+2**, confirmed live, three claims placed Tuesday 22 Sept process Thursday
24th. So the placement day chooses which injury paperwork the claim has to survive.
→ PLACE CLAIMS SUNDAY NIGHT. They run Tuesday morning and cross nothing, because the new week's reports do not
exist yet. Tuesday placement runs Thursday and crosses Wednesday's practice report; Wednesday placement runs Friday
and crosses three.~~
**RETRACTED IN FULL AT v9.26 (doc 405), and this file carried it for two days after.** `Waiver Period: 2 Days` is how
long a PLAYER sits on waivers after being dropped, not how long a CLAIM waits (all 283 unowned men in the 24 Sept pull
share one clear time, 03:00). **MEASURED, this league, every executed claim 2022 to 2026, n=626: 86.3% execute
THURSDAY 03:00 to 06:00 ET, 13.7% Friday to Sunday, and ZERO have ever executed Monday, Tuesday or Wednesday.** The
placement day does not choose the run; a Sunday claim and a Wednesday claim process in the same Thursday batch.
→ **PLACE CLAIMS WEDNESDAY NIGHT.** Sunday placement bought nothing and gave up both night games and two practice
reports. Matt already did this; the rule now matches his behaviour.
~~92% of Out designations are filed Thursday or later.~~ **RETRACTED, doc 392: that figure is the share whose LAST
edit came Thursday or later, and the feed keeps only the final row per player-week, so it cannot say what a row said
on Wednesday. Floor only: at least 8% settled by Wednesday. The rest is BLOCKED.**

**PUT A DROP ON EVERY CLAIM. MEASURED, this league, n=2,256 waiver events** (doc 393): among claims that reached
processing and were not outbid, **a claim naming a drop is 884 executed with ZERO roster-limit failures; naming none is
~~371 with 24 failures (6.1%)~~** **[v9.32, doc 435: that 371 includes 247 free-agent adds that cannot fail; on WAIVER claims alone the no-drop failure rate is 16.2%, 19.5% with position-limit failures, against 0 of 502 with a drop, and one drop covers one claim]**, and all 24 carried no drop. **Matt owns 8 of the 24**, all 2025.
**AND RANK THE CONTESTED MAN FIRST** (doc 396). ESPN: *"Reorder claims by dragging them into your preferred
priority"*, and a winner *"will move to the end of the waiver order"* MID-RUN. Measured here over five seasons: only
**28.6%** of player-runs are contested and an uncontested claim wins **78%** regardless. ~~On the 586 contested
claims the win rate runs 61.1% with no other win that run, 29.1% with one, 11.2% with two or more.~~ **RETRACTED at
v9.24 (doc 401): the bucket is the team's other wins that run, which is its total minus this claim's own result, so a
winner sits a bucket below a loser BY CONSTRUCTION; a permutation null reproduces all three cells with zero variance.
"Rank the contested man first" survives as a DOMINANCE argument with no number, and the within-run order cannot be
measured from `waiver_report_*.csv` at all (one timestamp per run); the missing input is his own claim order at
placement, which `py claim_order_log.py` now records.** **Check
`avail` before ordering: a free agent *"does not affect your waiver position"*, so he is not a claim and takes no slot
in the order.** Never quote his priority from memory — `wire.py` reads `waiverRank` off `mTeam` every run.

**THE SEAT IS A LOAN, RE-MEASURED AT v9.22 (doc 399, n=1,431, 2021 to 2025).** In w+1 an Out player is still **Out
38.9%**, **Questionable 19.5%**, Doubtful 3.4%, **no designation 38.2%**, and **plays a snap 29.6%**.
**THE SEAT DIES WHEN HE LOSES THE DESIGNATION, NOT WHEN HE PLAYS**, so those are different curves:

| | w+1 | w+2 | w+3 | w+4 | w+5 |
|---|---|---|---|---|---|
| **seat still valid** | **75.5%** | **51.2%** | **35.2%** | **26.4%** | **22.2%** |
| ~~still not playing (what this file used to say)~~ | 70.4% | 52.7% | 41.9% | 35.6% | 31.5% |

**Safer in week one, shorter from week three. The median seat still dies between two and three weeks, so the play is
unchanged.** ~~w+1 73.8% ... w+5 23.8%~~ **RETRACTED, UNREPRODUCIBLE on six population definitions — do not quote it.**
**PARKING AN OUT MAN FREEZES THE LINEUP THE FOLLOWING SUNDAY 24.5% OF THE TIME**, about one in four, which is what the
Sunday-morning roster check buys. Seat invalid at w+1 by position: **RB 20.3%, QB 22.4%, TE 24.9%, WR 26.1%** — a
parked RB is the safest seat and **a parked QB is second riskiest, the opposite of what this file said before v9.22.**

**THE 3 IR SLOTS ARE SEPARATE FROM THE BENCH. Still [OPEN], mine:** what `Auto Reactivate: No` does in football (it is
in the settings file and ESPN's football help does not document it), whether an IR man counts against a position cap,
and whether time on IR breaks *"rostered all season"* for keeper eligibility.

**Waivers are standing order, not FAAB**, reset weekly to inverse standings *(settings: `Waiver Order: Reset Each Week
to Inverse Order of Standings`)*. ~~The run count, two a week, is Matt's own and has NOT been checked against ESPN.~~
**RUN DOWN AND RETRACTED, v9.21: there is no two-run week.** The settings file has **no run-count line at all**
(`Season Acquisition Limit: No Limit`, `Waiver Period: 2 Days`), and ESPN processes waivers *"typically daily around
3:00 AM ET"*. ~~A claim matures at D+2 and processes at the next daily run.~~ **Measured at v9.26: the run is Thursday 03:00 to
06:00, never Monday to Wednesday (section 2).** **What a winning claim spends is his waiver
PRIORITY for the rest of that week** — he drops to the end of the order mid-run and it resets only on the week
boundary. That is scarcer than a run, so the protection in section 3 is unchanged.

The draft was 7 September and is over.

---

## 3. THE FOUR THINGS ONLY MATT DOES. Everything else is yours.

1. **Anything needing his ESPN session**, and separately, **anything that runs on HIS machine**:
   every command in section 5 is his to run, though only the pull and the live tools touch ESPN.
2. **Anything that WRITES to ESPN.** Lineup, claim, drop, trade, prerank.
3. **Money, or anything irreversible.** **A winning claim spends his waiver PRIORITY for the rest of that week, and a drop
   is permanent.** Both stop and ask, every time. **The keeper half applies only to a DRAFTED
   player: by section 2's own rule a waiver pickup was never keeper-eligible, so dropping one costs
   nothing in 2027.** Do not defend a body that has no keeper value on keeper grounds.
4. **A file that only exists behind a login.**

**Outside those four, do not wait for a go.** Name the one thing, start it, report it done, and
state the claim in its testable form in the same breath so he can redirect after.

**IF YOU CANNOT TELL WHICH SIDE AN ACTION IS ON, IT IS ON HIS SIDE. ASK.** The paragraph above is
an accelerant and a fresh reader has no calibration yet.

**NAMING A DROP IS ALLOWED. NAMING ONE FROM MEMORY IS NOT. THE TWO CONDITIONS ARE THE WHOLE RULE:**
**his roster file open and read THIS session, not recalled, and every candidate's keeper cost stated
next to him** (drafted round 5+ and rostered all season is eligible; a waiver pickup never is; the
rounds are in `Source\DRAFT_RECAP_2026.html`, section 6, and in no other file the table lists).
With both, name the ONE, say what it costs, and say what the seat buys instead. With either missing,
say which one is missing and stop. **Do not substitute a ranked bench: that is the same work handed
back.**
What the four protected categories cover is EXECUTING: he clicks the button, and the claim and the
drop are his. Analysis is not spending anything.
**SETTLED 18 SEPT, DO NOT REOPEN IT AS A CHOICE.** A hard ban on naming the drop was considered and
is DEAD, for one reason: the case it was written for is a model working from memory with no roster
file, and **condition 1 already refuses that, in the same words.** The ban adds nothing there and
costs a whole answer everywhere the file IS open. It also binds the wrong object: it constrains this
file and not `WEEK_SHEET.html`, and the sheet is what actually mispriced Mike Washington.
**The live risk in this rule is condition 2, not condition 1: a confidently stated WRONG keeper cost
reads as checked. State the cost next to each candidate so he can catch it; never assert the
conclusion alone.**

---

## 4. HIS FILES

`device_list_dir` to look, `device_stage_files` to read, `device_commit_files` to write.

```
G:\My Drive\_Fantasy\2026                 everything
C:\Users\wmatt\OneDrive\Fantasy           superseded copies, check before trusting
```

**Before you WRITE anything, read the directive's SECTION 9.** It carries the four rules that cost
this project real time: archive first, verify every commit by content rather than by its result, a
fresh container path per commit, and re-stage any shared file immediately before editing it because
another session may be writing it too.

---

## 5. WHAT HE RUNS. One command, and he runs it.

**`.\ff.bat` is the one command and it rebuilds nearly everything.** Five scheduled tasks call it:
Tue 06:00, Thu 17:30, Sun 11:45, Sun 15:30 ET, and daily 07:30 since 19 Sept (`Scripts\setup_tasks.bat`
registers all five; doc 374). **It ends with a vintage check: when the log says VINTAGE CHECK FAILED, the
sheet is printing preseason rates that this season already refutes, and the table it prints names them.
Read that table before trusting any pts/wk on the sheet** (doc 373). On 19 Sept it named ten men.

**For any other command open `2026\COMMANDS.html`, never a list in prose including this one.** It is
generated from `sheet_engine.TODO_CMDS` plus the batch files, and is never hand-edited.

---

## 6. THE DATA, AND THE PAGES THAT RENDER IT. Read the mtime on every one.

| file | what it is |
|---|---|
| `Source\MY_ROSTER.csv` | **his fifteen, one row per man. COUNT THEM**; never assume the roster is full or a spot is free. **Read this before answering anything about his team** |
| `Source\LEAGUE_ROSTERS.csv` | the other eleven, so you can see who is already owned |
| `Source\DRAFT_RECAP_2026.html` | his 2026 draft, every pick with its round: the input to condition 2 of the drop rule in section 3 |
| `Source\WIRE_<date>.csv` · `FREE_UNRANKED_<date>.csv` | the free pool, dated |
| `Source\injuries_2026.csv` | availability. **Week 1's report only, and nothing rebuilds it (section 1)** |
| `Source\form_2026.csv` | week-by-week usage; the workload screen and the seat lane read it |
| `Source\inherit_2026.csv` · `Scripts\depth_map.csv` | who is behind whom, what the job is worth |
| `Source\sheet_constants.json` | every number the sheet prints that is not computed live |
| `Source\waiver_report_2022..2026.csv` | five seasons of waiver ACTIVITY, not adds. **Check the shape before counting: the 2026 file written 19 Sept 11:50 is one row per event (55 rows, `Status` in EXECUTED / PENDING / CANCELED / FAILED_*); every earlier copy repeated each event once per `Week` from 2 to 18 (624 rows for 48 events), and the older seasons may still. If a `Date + Team + Transaction` repeats, dedupe on it first, then filter `Status == EXECUTED`.** Its last event date is its clock |
| `Source\WEEK_SHEET.html` | **the page he reads.** What to do, THE SEAT LIST, the bar, his roster |
| `Source\ONLINE_WEEK_SHEET.html` | **the copy of the week sheet that goes to the web**, built by `Scripts\make_online.py` as a step inside `ff.bat` (doc 430; it refuses rather than writing a bad file). Nothing on his PC can publish it: a scheduled task, "Publish the week sheet", `trig_01F1k2gt3LKkRowMWB7mScpy`, daily 08:54 ET, bound to his computer, stages it and republishes the artifact at `claude.ai/artifact/1eaMAtyCzdqMcSdh96w4SK`. **Compare its build stamp against `WEEK_SHEET.html` before trusting it**; it sat six days stale once |
| the roster clock, `claude.ai/artifact/NpLWo1xBiWRG4bztW7L5xw` | the QB2 and TE2 pairing table, the late-season card and the supply curves (docs 427, 428, 431). An artifact, not a file; the audit prompt (section 9) lists what on it is a bound rather than a measurement |
| `Source\STATUS_LOG.csv` | **append-only** `injuryStatus` for every man every `wire.py` run since v9.18 (doc 393), so a status flip has a time. Nothing else on the drive keeps the history |
| `Source\claude_todo.txt` · `Source\matt_todo.txt` | the two reply-item lists, mine and his (section 9) |
| `MY_TODO.html` · `THE_WEEKLY_WIRE.html` · `LINEUP_CHECK.html` | the rest, all rebuilt by `ff.bat` |
| **`2026\COMMANDS.html`, at the FOLDER ROOT** | **not the one in `Source\`**, which is a dead copy from before the draft. The root file is the live one |
| `Source\adp_registry\` | **the only sanctioned historical draft market**, one file a year 2021 to 2025, `MANIFEST.csv` says what each is made of. **All five are the FantasyPros half-PPR archive page since 22 Sept (docs 384, 385).** To replace a year, from `Scripts\`: `py research\adp_registry_from_fp.py --year <Y> --file "<the export in the 2026 folder>"`; it archives, writes, checks, **refuses a rank and refuses the full-PPR page** (ESPN, CBS and Fantrax columns: same site, different scoring), and prints the line for `Source\code_adp_guard.py`. Then re-run JOB 4 (`research\j4\j4_riser_keeper.py --with-2021`, then `j4_band_loo.py` on its rows file). Never `espn_adp` from a historical pull |

**THE BAR** is the points a week a new player must beat to change his starting nine that week;
below it he is worth zero. **THE SEAT LIST** is backups who could inherit a job he does not own
yet, priced as the chance the job opens times what it pays if it does.

---

## 7. TELLING A LIVE NUMBER FROM A DEAD ONE. This project's signature failure.

- **Superseded text is struck through** and followed by a bracketed version tag saying what replaced
  it. Read the tag, not the struck text.
- **`Source\AUDIT_LEDGER.md`** is one row per claim the red team has killed or qualified, with the
  old sentence, the replacement and grep tokens. **Rows marked `[OPEN]` still carry the bad sentence
  somewhere.** Grep it before quoting anything.
- **The findings are in `Source\DIRECTIVE_FINDINGS.md`, not in the directive, since v9.8 (18 Sept, doc
  367).** The directive's SECTION 4 is a one-line index of all 42, with no numbers; the finding
  itself, with its baseline, population and sample size, is in the findings file under the same id.
  The draft-side sections (§5, §7, §8, the depletion table) are in `Source\DIRECTIVE_DRAFT_BOOK.md`,
  and the stop signs quoted in section 8 below live in those two files now. A numbered doc is the
  EVIDENCE; the finding is the CLAIM.
- **`py Scripts\research\audit_directive.py`** re-checks the directive's load-bearing numbers against
  the shipping files and fails loudly if a wording moved. Since v9.8 it reads §4.14 from the findings
  file and says so.
- **BEFORE ANY PLAYER TAKE LEAVES YOUR REPLY, the directive's 0.1(h) applies: five lines beside the
  name (vintage, population, the man ahead, the standing rule and the roster after, the counterfactual)
  or the take does not go out.** It is there because it was measured first: on 174 of this project's own
  takes, missing three or more of the five meant a 44% chance the take's own author later corrected it,
  against 21% for two or fewer (doc 378, `Source\take_contract_scores.csv`). **The three error classes
  that retired the last two chats are the same shape**: a claim about a file stated without opening it, a
  number quoted from prose rather than run, and a comparison offered with a dead option in it (doc 365).
  The fourth, found 19 Sept, is a number read off a generated page without asking what population
  produced it (docs 370, 371, 373).

---

## 8. YOU MAY RE-OPEN A CLOSED QUESTION. THERE IS A GATE, AND IT IS NOT "IS IT INTERESTING".

The directive carries at least eight stop signs: *"PICK 8 IS CLOSED"*, *"Do not rebuild it"*,
*"Do not re-derive this"*. Doc 288 argues, without measuring it, that a stranger arrives
pre-committed against questioning exactly what most needs questioning.

**Read the numbered docs as EVIDENCE and the directive's findings as CLAIMS. The gate before you
spend an afternoon on one: does a decision Matt faces THIS WEEK still depend on it?** If not, say it
is re-openable and leave it. Re-derive nothing from memory, and quote no number you have not run
past section 7.

**His record on his own hunches: 12 confirmed or partly confirmed, 1 underpowered his way, 7 null.**
Better than a coin flip. **Never open with the assumption his idea will die.**

**When you cannot test something you owe exactly one of three answers:** TESTED with population,
baseline, n and number · **NOT YET RUN** with the testable form written down · **BLOCKED** naming
the exact missing input and whether you tried. *"That is not measurable"* is not one of them and
has been wrong seven times.

---

## 9. WHAT IS OPEN, AND WHERE

`Source\matt_todo.txt` is his list, and anything you ask him to run goes in it the moment you say
it. **No write access? Then say so in the reply, in one line, and put the item where he will see
it: "this is not on your list because I cannot write to it."** `AUDIT_LEDGER.md` rows marked `[OPEN]`. `OPEN_THREADS.md` is generated by
`py research\open_threads.py` and its closer needs an exact phrase, so treat it as candidates.
**`Source\claude_todo.txt` is MY list (v9.31, doc 430): a thing I say in a reply that I will do goes there before the
reply is sent, and `open_threads.py` renders both lists at the top of `OPEN_THREADS.md`.** **Since 28 Sept (doc 435) `ff.bat` runs
`open_threads.py` every run and the script no longer scans its own output, so `OPEN_THREADS.md` is as fresh as the last
`ff.bat`.** The two to-do files render at its top. **The red team of v9.13 through v9.31 ran in full on 28 Sept: doc 435
is its findings, one table per batch; `AUDIT_PROMPT_20260925.md` is now a record, not a task.**
**To find a finding by subject, grep `Source\*.md`**: the filenames are written to be greppable,
each named after what it found. Newest number wins.

**THE TRACKERS RECORD ASKS, NOT COMPLETIONS.** A to-do item can be done on ESPN and still read
`[ ]`; it carries a date in its text and no status. Check the roster before acting on a roster item,
and the project's instructions before telling him to paste a directive. `OPEN_THREADS.md` is only as
fresh as its last run, so the newest numbered doc whose title says what is open beats all three.

**A SECOND MODEL WRITES HERE TOO.** Fable runs jobs from `Source\REDTEAM_TASKING_PROMPT.md` and commits
to `Source\` while you work. SECTION B's jobs are numbered (JOB 1 done, JOB 3 run, JOB 2 partly
pre-empted, **JOB 4, the riser as keeper, RUN: docs 382, 383, 384, 385 (four seasons), findings 4.34**); SECTION C's are
NAMED, never numbered: THE TAKE CONTRACT ran 19 Sept (doc 378), the outside read on freshness ran (doc
380) and the next kickoff ran (doc 381). One is queued, the directive read by someone with no stake in
it, and it may not run on Fable, which wrote v9.8 through v9.12. **Queued and mine, one batch: findings
4.12, 4.18b, 4.20, 4.22, 4.25 and 4.26 re-run on the five-year half-PPR registry (doc 385 section 5). Its old
blocker, no 2021 nflverse weekly file, is gone: it is in `Scripts\research\_nflverse_cache\` since 22 Sept.**
**The project store has a capacity trigger (directive §0.5(d)): above 1,600,000 of 2,000,000, the oldest
numbered docs move to the drive, hash-verified, the way doc 384 did it.** The handover tests were also numbered JOB 4 to 6 (docs 357, 361, 365); those are done
and are not the tasking prompt's jobs. **Re-stage any shared file immediately before editing it.**

---

## 10. HOW HE WANTS TO BE TALKED TO

- **Numbered do-this list first**, then a few short paragraphs. Over about 25 lines has failed.
- **One recommendation, not a menu.** Ranking them is the job.
- **CHECK THE LOGIC OF AN OPTION BEFORE YOU OFFER IT, AND SAY WHEN ONE IS DEAD.** Matt, 18 Sept:
  *"What give me an option that doesn't logically work without saying so, that seems to introduce
  unnecessary risk doesn't it? I join here tired and I can easily see me doing something dumb."*
  **A menu that contains a broken choice is worse than a menu**, because it spends his attention
  on a thing that cannot work and it looks like a real decision. Before presenting any comparison,
  test each option against the case it exists for. **If one fails, say so IN THE FIRST LINE and
  present it as closed, not as a choice.** The case: a ban on naming a drop was offered against a
  conditioned rule, when the ban did not stop the failure it was written for and the condition
  already did. That was decidable before he read a word of it.
- **HE WANTS TO BE HUMBLED AND FACT CHECKED, AND HE MEANS IT ABOUT HIS OWN IDEAS.** Same message:
  *"I have good hunches, but I like to be humbled and fact checked. I don't want to go forward with
  something broke because I was being dumb in the moment. I'm a human first."* **His hunches are
  better than a coin flip (section 8) and half-baked ones still arrive, especially late.** So:
  test the idea, say plainly when it does not hold, and never carry a broken thing forward on the
  grounds that he said it. **Challenge the substance, never the expression** (below) is the same
  rule from the other side: take what he MEANT seriously enough to check it.
- **Never use em dashes in anything you write or send him.** The existing files are full of them;
  that is history, not a licence.
- **A rendered page carries the instruction and the plain number and nothing else.** No section
  numbers, no p-values, no sample sizes. Provenance lives in the docs.
- **Challenge the substance, never the expression.** Read through to what he means.
- **Standing boundaries, quoted:** *"Mike Washington Jr. - 0% chance i drop him."* *"Don't take my
  suggestions without using critical thinking, ever."* *"Don't take what I say as truth!!!"*
  ESPN cookies in scripts are settled; do not raise it again.
