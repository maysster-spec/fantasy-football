# 373. VELE SCORED 16.4 IN WEEK ONE AND THE PAGE STILL PRICES HIM AT 5.8, WHICH IS THE SAME DEFECT FOR THE FOURTH TIME

*19 September 2026. Population note (0.6): every usage figure below is from `Source\form_2026.csv`,
week 1, Matt's own file, rebuilt by `ff.bat`; the projections and drop costs are from the
`WEEK_SHEET.html` built Friday 18 Sept 08:57. Doc 372 is the previous number.*

---

## 0. WHAT TO DO

1. **A number that must not be quoted again: Devaughn Vele at 5.8 a week, and his drop cost of 0.0.**
   His own file has him at **16.4 half-PPR in week one on 91% of the snaps.** Section 1.
2. **Matt's read was right and mine was wrong. He does not come off the roster.** The grid in doc 371
   rested on 5.8, which is a preseason projection that week one refutes.
3. **The online page is live and it is built around this exact failure**: every man shows the
   projection and the actual side by side. Section 2.
4. **The artifact he asked about was a dead snapshot**, not a maintained page, and two of its links
   could never have worked. Section 2.
5. **One new scheduled task refreshes the online page** Sundays and Tuesdays at 12:30pm ET, after his
   machine rebuilds. His two existing tasks are correct and need no change. Section 3.
6. **The tracker's garbled rows are a self-scrape loop, all of them already closed**, and two of the
   real blocked items ARE his to unblock. Section 4.
7. **The deterministic fix for all four of tonight's errors is one column, not another rule.**
   Section 5.

---

## 1. THE MEASUREMENT, AND IT IS HIS OWN FILE

`Source\form_2026.csv`, week 1, verbatim:

| | snap % | targets | target share | half-PPR |
|---|---|---|---|---|
| **Devaughn Vele** | **91.0** | **9** | 17.3 | **16.4** |
| Chris Olave | 86.0 | 13 | 25.0 | 23.2 |
| Puka Nacua | 70.0 | 9 | 33.3 | 9.9 |
| Xavier Worthy | 77.0 | 6 | 24.0 | 3.3 |

**Vele out-snapped Olave**, who is New Orleans' WR1, and **out-scored Worthy by 13.1**. The week
sheet prices him at **5.8 a week** and his drop at **0.0**, and doc 371's grid concluded from that
figure that he never clears the 11.7 receiver bar in any of fourteen weeks. **16.4 clears it by 4.7.**

**THE GRID WAS NOT WRONG ARITHMETIC. IT WAS THE RIGHT ARITHMETIC ON A DEAD NUMBER.** Every row of it
inherited 5.8, so every row inherited the error: the lineup row, the week-11 row, the Spears
precedent row. One game is one game and 16.4 is not a forecast, but **91% of the snaps is a role,
and role is the part that persists** ("wait for a pop when the workload popped" is in Matt's
confirmed column).

**THE SUPPORTING FACTS FROM HIS REFERENCE DOC CHECK OUT AND TWO OF THEM MATTER MORE THAN THE POINTS.**
Jordyn Tyson, New Orleans' first-round rookie receiver, is on injured reserve. **Chris Olave is
officially questionable with a hamstring** for Sunday at Baltimore, limited Thursday and Friday
(NBC Sports player news, URL-dated 2026-09-18; the Saints' own final report lists three
questionable). With Tyson out and Olave limited, the target share Vele is second in line for is the
whole room.

**THE CAVEAT ON THE REFERENCE DOC ITSELF, because it is not a project source.** It states plainly
that *"the specific proprietary league settings from the user catalog were not directly accessible"*
and assumes PPR or half-PPR. **So its lineup advice was written without Matt's bar, his roster caps
or his scoring**, and its conclusion "start Vele over Worthy" is reasoning, not arithmetic against
this league. What survives independent checking is the usage table, and that is what this section
rests on.

---

## 2. THE ARTIFACT HE ASKED ABOUT WAS NOT BEING MAINTAINED

`claude.ai/artifact/1eaMAtyCzdqMcSdh96w4SK` is **a one-off copy of `WEEK_SHEET.html` as it stood on
18 September**, version stamp 1789734267. Nothing publishes to it. `ff.bat` writes local files and
has no route to claude.ai, so **it has been frozen since the moment it was made and will stay
frozen.**

**AND IT COULD NOT HAVE WORKED EVEN WHEN FRESH.** Its masthead links to `MY_TODO.html` and its
footer to the same, both relative paths that resolve against `claude.ai` and 404. It also carries
"to-do list, 42 open" against a file that now holds 46. **A page that is stale AND broken-linked is
worse than no page, because it looks like the real one.**

**WHAT SHIPPED INSTEAD: `claude.ai/artifact/1iFS2iFyDACxRknmbJiFNT`, the Juggers Pocket Sheet.**
Phone-first, no local links, and built around section 1's defect rather than around the week sheet's
layout: **every man carries the projection, the week-one actual and the bar he must beat, side by
side, with the gap called out in words.** Jeanty reads 14.5 projected against 29.7 actual; Adams
11.7 against 4.1; Vele 5.8 against 16.4. **Three of the fifteen are wrong by more than a full
starter's week, and until tonight none of that was visible anywhere.**

It carries a freshness stamp naming the pull it was built from and states in plain words that it
does not update itself, because the previous artifact's whole failure was looking current.

---

## 3. THE SCHEDULED TASKS

**His two existing tasks are correct and neither needs changing.**
- *Tuesday wire read, the judgement layer*, fires 08:00 ET Tuesdays. Last ran 15 Sept, succeeded.
- *Sunday 11:40am, inactives are out*, fires 11:40 ET Sundays. Last ran 13 Sept, succeeded.

**The draft-era tasks in his screenshot are already gone.** *Sep 6 weekend practice sweep* and
*Draft day: final ADP pull* were one-shots; they fired and disabled themselves, which is the
date-shaped-trigger problem solving itself correctly for once.

**ONE THING THE TUESDAY TASK ALREADY KNOWS THAT THE PAGE DOES NOT.** Its prompt carries, from the
12 Sept red team: *"THE DROP IS NOT FREE AND THE OLD SHEET SAID IT WAS... use that, and never a
0.0."* **The shipped week sheet still prints 0.0 for Vele.** So the instruction to distrust that
number exists, in a place that is read once a week, while the number itself sits on the page he
reads every day. That is §0.5(f)'s failure shape exactly: the fix went into one instruction and not
into the thing it was about.

**NEW: *Refresh the Juggers Pocket Sheet*, Sundays and Tuesdays 12:30pm ET**, after the morning
`ff.bat`. One task, two firings, single purpose: stage, check the official injury report, rebuild,
republish to the same URL. It is bound to his computer and it republishes nothing if the machine is
unreachable, because a stale page that looks fresh is the failure it exists to avoid.

---

## 4. THE TRACKER'S GARBLED ROWS, AND THE TWO HE CAN ACTUALLY UNBLOCK

**Diagnosis: `open_threads.py` scrapes `OPEN_THREADS.md`, which is its own output.** Each run wraps
the previous run's lines in another `OPEN_THREADS - -` prefix. Measured on the current file: **21
lines carry two or more nested prefixes and 5 are nested four deep.** All 21 are struck through,
meaning already closed, so **they are noise and not a backlog**. The file's own header says these are
not his to action.

**BUT TWO OF THE UNDERLYING ITEMS ARE GENUINELY HIS, and answering his question honestly means
saying so rather than waving him off:**
1. **The trade record, NOT YET RUN.** Its named input is `py waivers.py --live`, which needs his
   ESPN cookies on his machine. That is §0.4 category one and only he can run it.
2. **Slot rate and targets per route run, BLOCKED on PFF fields.** Those need a PFF subscription.
   **That is a money decision, §0.4 category three, and it is his alone.** Not worth it on what they
   would buy, in my view, but the call is not mine to make silently.

**[OPEN] `open_threads.py` should exclude its own output from its scan.** Mine, one line, queued.

---

## 5. THE DETERMINISTIC FIX: A VINTAGE COLUMN, NOT ANOTHER RULE

Matt: *"let's think of ways to refine the rules to be more deterministic so that considerations are
not missed at every turn."*

**FOUR ERRORS IN TWENTY-FOUR HOURS AND THEY ARE ONE ERROR.** Pineiro's 8.4, Schultz's 11.1,
Schultz's 38%, Vele's 5.8. **In each case I read a number off a generated page and used it without
asking what produced it.** The directive already has three rules aimed at this (§0.2, §0.6, §3's
baseline-population-sample requirement) and **all three are addressed to the writer of a finding,
not to the reader of a page.** The pages carry no provenance at all, so there is nothing to check
even when I remember to.

**SO THE FIX IS NOT A FIFTH RULE. IT IS A COLUMN ON THE PAGE, AND A GUARD THAT REFUSES TO BUILD
WITHOUT IT.** Every rate a page prints gets a one-word vintage:

| tag | means | example |
|---|---|---|
| `proj` | preseason projection, never updated | Vele 5.8 |
| `2026` | this season's actual, and how many games | Vele 16.4, 1 game |
| `rate` | a population base rate, not this player's forecast | the screen's 38% |

**THREE MECHANICAL CONSEQUENCES, each of which would have caught one of tonight's four:**
1. **Where `proj` and `2026` disagree by more than a starter's week, the page says so on the row.**
   Catches Vele, Jeanty and Adams tonight.
2. **A `rate` figure may never be printed beside a player's name without its population.** Catches
   Schultz's 11.1 and his 38%, which are the same number for every man who clears the screen.
3. **The drop-cost column takes the HIGHER of `proj` and `2026`.** A man is not cheap to drop because
   a preseason number says so when his own season says otherwise. Catches Vele's 0.0, and Pineiro's
   8.4 was the mirror of it.

**AND THE GUARD IS THE PART THAT MAKES IT DETERMINISTIC RATHER THAN ASPIRATIONAL** (§0.2: a guard
that has never fired is not a guard). A build step that greps every generated page for a printed
rate with no vintage tag and **fails the build**, run against tonight's shipped pages as its negative
control, where it must flag Vele's 5.8 and Schultz's 11.1 or it does not work.

**WHY THIS AND NOT A LONGER CHECKLIST.** Every rule added to SECTION 0 so far is a thing I must
remember at the moment of writing. This is a thing the FILE must carry, checked by a script, and it
fails loudly when absent. **The directive is already 57 KB and tonight proves that adding to it does
not stop the reader from trusting a bare number.** Doc 372 asked for a linter on generated pages for
unsubstituted braces; this is the same linter with a second rule, and they should ship together.

**NOT YET RUN: the vintage tagging and its guard.** Testable form: *build the current pages with the
guard enabled and confirm it flags at least Vele's 5.8 and Schultz's 11.1, then confirm a tagged
build passes.* Mine, and it is the next thing in this lane.
