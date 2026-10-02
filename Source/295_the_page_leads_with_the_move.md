# 295 -- the page leads with the move, and his own file can veto it

**11 September 2026, late.** Matt's six-part message. Everything here is shipped and verified on the
drive; the one thing that is not is the test named in §6, which is NOT YET RUN with its missing
input named.

---

## 1. Check kit's four problems were four bad PINS, not four stale files

He ran `py check_kit.py` and it reported four. All four were the checker being wrong about the
drive, not the drive being wrong.

| file | pinned | actually on the drive since | why the pin was wrong |
|---|---|---|---|
| `board_v8_fixed.csv` | doc 267's re-pin | 7 Sept, untouched | doc 267 pinned from a copy that was not the drive's |
| `board_v7_kdst_separate.csv` | same | 7 Sept, untouched | same |
| `ESPN_prerank_with_ids.csv` | same | 7 Sept, untouched | same |
| `player_context.csv` | same | 7 Sept, untouched | same |
| `set_cookies.py` | never updated | changed 8 Sept | a legitimate change nobody re-pinned |

Re-pinned at the drive's own bytes and re-run against every file in the manifest: **63 files,
0 mismatches.** `check_kit.py` is 26,890 bytes on the drive as of tonight.

**THE LESSON, and it is the third time: a pin taken from anything but the canonical file is a
false alarm generator, and a checker that cries wolf is a checker nobody reads.** Doc 260 is
literally called "the pin nobody read". Pin from the drive, never from a staged or working copy.

---

## 2. The week sheet now opens with the move (his item 3)

> *"I need the key players, trends and points of interest right off the bat at the top of the page
> ... What adds the most value to making a waiver or free agent claim when compared to my current
> roster, that is exactly what we intend to do here ... Provide the optimal move, and the context
> ... How long to hold the player and the relevant information to help me decide ... You are the
> fantasy expert and I want to hear your arguments and leanings."*

**Section 0 is new and it is the first thing on the page.** It ranks every candidate the sheet
already prices -- certain fills, screened bets and backfield seats -- in ONE unit: points above his
own bar. Nothing in it is typed by hand or by me; it is sections 1 to 5, sorted. Each move carries:

* **what it is** -- fills an empty slot, beats your own man, a bet, a seat
* **why, in his numbers** -- the week his slot is empty, the odds the screen fires, the job's worth
* **how long to hold him** -- the weeks he is actually above the bar, which is usually one
* **when to claim him** -- a fill five weeks out says *no rush, take him the week before*, and a
  speculative bet in week 1 says *not this week* and gives the reason
* **the news** -- the dated card line for the top move, on the page instead of in another file
* **what it costs** -- the cheapest body he owns, by name, with the insurance caveat
* **a verdict** -- clears / does not clear / not yet, in one line

Then a **watch list** (his own men with a status, men with no projection at all, the next bye, the
empty slots ahead, rivals short at a position) and **his open to-do items**, scraped straight from
`matt_todo.txt`, because he said it plainly: *"i don't want to be all over the place when the
enrichment could be done on the main strategy page."*

**Columns:** a long name now clips with the full name on hover, which gave the fourteen week
columns their width back. 68 names carry a tooltip.

**The page opens itself.** `ff.bat` records the sheet's timestamp before and after the run and
opens it **only if it moved**. Opening a stale page on a schedule is the exit-code defect wearing a
different hat (doc 146). `FF_NO_OPEN=1` suppresses it. The log says SHEET OPENED or SHEET NOT
OPENED and why.

**Tested before it left here.** An offline harness renders the page from recorded inputs: the
7 Sept projection pull, today's wire, his fifteen. Negative controls run: planted injury statuses
appear in the watch list; removing the DO NOT line brings the ruled-out man straight back to the
top; the rows that must be on the page are on it by name. Both files compile under 3.11 and 3.12
with `SyntaxWarning` as an error.

---

## 3. THE CONFLICT THE FIRST BUILD SHIPPED, AND THE MECHANISM THAT CLOSES IT

The first render's headline move was **"Take Brenton Strange, +6.6"**. Line 54 of his own to-do
file says **DO NOT CLAIM BRENTON STRANGE**.

**The page was about to argue with his file, in bold, at the top.** Nothing in the code could see
the instruction: `sheet_constants.json` has no such list and the only DO NOT mechanism was a card
verdict.

**So a DO NOT line is now a first-class input.** Any open `[ ]` line in `matt_todo.txt` beginning
DO NOT, plus any card whose verdict begins DO NOT, removes that man **at selection**, not after
ranking. The name is never parsed out of the sentence -- the sentence is matched against the names
the page already knows, so a new verb ("do not stash", "do not start") cannot silently drop a rule.

**And the page says so, and prices it:**

> **ruled out by your own file.** Brenton Strange (TE) prices at 6.6 and would otherwise lead this
> list. Your line: DO NOT CLAIM BRENTON STRANGE -- my second bad recommendation on him. Next at TE
> is Pat Freiermuth at 6.3, so keeping the rule costs 0.3 points, across week 6.

That is the §0.5(b) shape: obeyed, not silently; surfaced, not argued with; and priced so he can
change his mind on a number instead of a feeling.

**AND THE WHOLE TIGHT-END ARGUMENT IS WORTH 1.3 POINTS, ONCE.** The free tight ends for the week-6
hole run **Strange 6.65 · Freiermuth 6.25 · Schultz 6.06 · Helm 5.76 · Waller 5.47 · Barner 5.38**
a game. His to-do ranks the same men by how often they are thrown to inside the ten (Waller 0.56,
Barner 0.35, Schultz 0.35, Strange 0.25). **Both rankings are inside the noise of one tight-end
week.** The decision is a week-5 decision, and by then four weeks of this season's targets will
settle it better than either preseason number. The page now says exactly that instead of naming a
man five weeks early.

---

## 4. The seat behind McCaffrey was pointing at the wrong man (his item 1)

Matt: *"you see the news about Kaelon Black? ... The CMC clear back up, are you kidding me."*

**He is right, and our files were four days behind him.**

* `inherit_2026.csv` named **Jordan James** as the next man behind McCaffrey.
* `cards_2026.csv` carried a **31 Aug** card calling the seat "contested" and "murky".
* Jordan James was **claimed by another team today**.

**The dated evidence settles it.** PFF, 10 Sep 2026: James was a **healthy inactive** in week 1, so
Black had won the backup job in camp; Black **led the team in carries**; McCaffrey's snap share was
far below his usual 83% with the early-down snaps split more evenly than at any point in his time
there; PFF calls Black **the biggest waiver target for week 2**. Yahoo Sports, 11 Sep 2026: in the
first half **Black played 16 snaps to McCaffrey's 15**, and ran seven times for 36 yards against
McCaffrey's three for 17.

Both files are corrected on the drive. The seat row is Black, free at 15.4%, behind a job worth
**302.4**, and McCaffrey carries a **questionable** tag in the pull and turns 30 this season.

**THE PART THE ARITHMETIC UNDERSTATES, AND IT IS A CLAIM, NOT A MEASUREMENT.** The seat model pays
a backup only for the weeks the job is OPEN -- that is where its 46% and its 1.1 expected points
come from. **Black is being paid while the starter is healthy**, which no handcuff in that table
is. `[HYPOTHESIS]`

**NOT YET RUN, testable form stated (§0.5a2/a4):** *among backs who took 40% or more of a healthy
elite starter's early-down snaps in week 1, does the split persist through week 6, and what does
the backup average over that stretch?* Population: every team-season 2021-2025 with a top-12
preseason back whose week-1 snap share fell below 60%. Inputs: nflverse snap counts, which we hold.
**Queued, not blocked.**

**What doc 294 says about the other half, so it is not over-claimed:** a producing replacement keeps
a share of the job (+12.4 points of share, p=0.006), but taking the job outright from a returning
round 1-3 starter happened **4 times in 26** in weeks 1-14. Black inheriting a share is the modal
outcome. Black replacing McCaffrey is not.

---

## 5. Where the ESPN 403 came from (his item 2)

Yes, three times, and it is **this container, not his machine**: docs 260, 264 and 291 all record
*"the container cannot reach ESPN (403)"* through the agent proxy. It is why `waivers.py --live`,
the wire and the pulls are on his list and not mine.

**His machine is fine.** Tonight's log: three runs, `THU 09/09`, `THU 09/10` and `BY HAND 09/11`,
every one `lineup exit 0, wire exit 0`, all three pages written. `waiver_report_2026.csv` was
written at 22:30 UTC today, 15,466 bytes. Nothing has failed on his side.

---

## 6. RED TEAM: "go after quarterbacks and tight ends, be strict about receivers" (his item 3)

**His objection, in his words:** *"TE and QB are solo positions. If i'm focused on those what
happens to the rest of my roster when it depletes and I'm not prepared with a next man up. I can
only play one TE at a time ... If i can only play one, i need to justify two while the other sits
there. Sure he may sit there and be a more valuable player, but if i can't play him, so what ...
The statement is not wrong, but the application is uncertain."*

**He is right, and the defect is precisely the one he names: a hit RATE is not a VALUE.**

The line comes from doc 12's table of executed adds: QB hits 26.5% of the time in this league
(his own rate 35.7%), TE 26.1%, WR 20.1% (his own 12.5%), RB 17.2% (his own 20.5%). That table
answers *"does the man I add become startable somewhere?"* **It never asks whether he becomes
startable HERE, on a roster that already has a starter at a one-slot position.**

**Three things already measured say his objection is correct:**

1. **§4.33 / doc 259, on his own roster:** the best free body is below his worst startable man at
   every position. *The wire cannot upgrade a working slot; it can only fill a broken one.* The
   same free player is worth zero as an upgrade and the full amount in an empty week-6 slot.
2. **§4.18c:** a second quarterback on a different bye adds **+2.49** to the lineup in the rollout,
   and one sharing the starter's bye adds **+0.00**, because he never starts. That is the measured
   size of "so what".
3. **§4.19:** four of five running backs he adds never give him a startable stretch, and nobody in
   the league beats his rate. **The RB hole is the one the wire cannot patch**, which is the whole
   argument for bench depth at RB.

**SO THE RULE IS REWRITTEN, AND THIS REPLACES THE OLD SENTENCE:**

> **Stream the one-slot positions; roster depth at the many-slot ones.** Claim a quarterback or a
> tight end to fill a hole you can already see on the calendar, start him for those weeks, and let
> him go. Do not carry a second one as an asset. Spend the standing bench seats on running backs,
> because that is the hole the wire will not fill for you.

"Be strict about receivers" survives only as a fact about **his own record** -- 12.5% on 24 adds
against a league 20.1% -- and that is a small sample stated as a caution, not a law.

**THE TEST THAT WOULD SETTLE IT -- NOT YET RUN, INPUT NAMED (§0.5a4).**
*Testable form:* among executed adds in this league 2022-2025 that HIT, does a hit at a one-slot
position (QB, TE) convert into fewer STARTED weeks, and fewer points over the man he displaced,
than a hit at RB or WR? Baseline: started weeks and points over the displaced starter, from the add
week to week 14. **Missing input: a per-week lineup history -- ESPN `mRoster` by `scoringPeriodId`
for 2022-2025.** We hold the adds, the scoring and the rosters; we do not hold who was in the nine.
**Only his machine can fetch it (the container is 403).** It is one pull, and it would also answer
three other open questions about what the wire actually does for him.

---

## 7. What is on the drive tonight

| file | bytes | what changed |
|---|---|---|
| `Scripts\sheet_engine.py` | 72,267 | section 0, the to-do block, DO NOT honoured and priced, names clip on hover |
| `Scripts\wire.py` | 79,675 | passes the week to the sheet; a free row carries its ESPN status |
| `Scripts\ff.bat` | 3,255 | opens the sheet when, and only when, it changed. Line endings normalised |
| `Scripts\check_kit.py` | 26,890 | five pins corrected, three re-pinned tonight |
| `Source\inherit_2026.csv` | -- | the SF seat is Kaelon Black, with the dated reason |
| `Source\cards_2026.csv` | -- | the stale Jordan James card replaced by a Kaelon Black card |

Archives for every one in `2026\_archive\`, stamped tonight.

**HIS ff.bat RUN AT 18:27 TONIGHT WAS BEFORE ALL OF THIS.** The pages on his desk are the old ones.
One more double-click gets him section 0.
