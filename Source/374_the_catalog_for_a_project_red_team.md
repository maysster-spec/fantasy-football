# 374. THE GUARD IS BUILT AND RUNNING, AND HERE IS THE CATALOG FOR THE PROJECT RED TEAM MATT ASKED FOR

*19 September 2026. Written against six questions Matt asked, three of which were "did you ship it
or just describe it". Two of the three answers were "described it", and this doc is written after
fixing that rather than before. Population note (0.6): guard output is measured on the
`WEEK_SHEET.html` built Friday 18 Sept 08:57 against `form_2026.csv` as of 19 Sept. Doc 373 previous.*

---

## 0. WHAT TO DO

1. **Matt: run `Scripts\setup_tasks.bat` once from an administrator prompt.** It adds a fifth
   Windows task, a daily 07:30 `ff.bat`. That is the whole fix for the Saturday claims. Section 3.
2. **Matt: `py waivers.py --live`.** Still yours, still not scheduled, and it has not run since
   11 Sept. Section 3.
3. **`check_vintage.py` is built, tested, committed, and wired into `ff.bat` as step 6.** It fails
   the run when a page prints a rate this season already refutes. On the shipped page it flags
   **ten**, Vele and Jeanty among them. Section 1.
4. **The online page does NOT update with `ff.bat`** and cannot. Two different clocks. Section 2.
5. **The catalog for the project red team is section 5**, eight batches, sized to finish, with the
   two that must run first named.

---

## 1. THE GUARD, BUILT RATHER THAN PROPOSED

Matt: *"'my grid was built on a dead number.' how are we preventing that?"*

**The honest answer at the time he asked was: we were not.** Doc 373 described a vintage column and
a guard and marked both NOT YET RUN. That is the project's oldest failure mode wearing a new coat:
the diagnosis shipped as though it were the fix. So the guard exists now.

`Scripts\check_vintage.py` reads the rates `WEEK_SHEET.html` actually prints, reads what each man
has averaged in `form_2026.csv`, and fails when they disagree by more than a starter's week (4.0, or
6.0 where only one game supports the actual). **`ff.bat` runs it as step 6 and writes a loud line to
the log when it fires.**

**ON THE SHIPPED PAGE IT FLAGS TEN:**

| | page says | actual | gap |
|---|---|---|---|
| Ashton Jeanty | 14.5 | 29.7 | +15.2 |
| **Devaughn Vele** | **5.8** | **16.4** | **+10.6** |
| Davante Adams | 11.7 | 4.1 | −7.6 |
| George Pickens | 11.7 | 4.3 | −7.4 |
| Puka Nacua | 17.2 | 9.9 | −7.3 |
| Rico Dowdle | 10.2 | 3.1 | −7.1 |
| Pat Freiermuth | 6.3 | 13.1 | +6.8 |
| Quinshon Judkins | 12.4 | 6.0 | −6.4 |
| Rashid Shaheed | 7.2 | 0.9 | −6.3 |
| J.K. Dobbins | 9.7 | 3.6 | −6.1 |

**AND THE GUARD WAS RED-TEAMED BEFORE IT SHIPPED, WHICH FOUND TWO DEFECTS IN IT.** The first draft
flagged **28**. Three of its own bugs, each an instance of the thing it exists to catch:
1. **`form_2026.csv` scores half-PPR from rushing and receiving only.** Jalen Hurts reads 4.6 with
   0 targets and 7 carries, which is his rushing line, not his week. Every quarterback and kicker
   looked "refuted" by a file that never scored them. Fixed: RB, WR and TE only.
2. **Every man appears twice, week 0 and week 1, identical.** The game count doubled and the
   tolerance band flipped. Fixed: week 0 dropped, and a part-played week ignored.
3. **The name-to-rate match walked out of its table.** The seat list writes a percentage in its rate
   column; the percentage did not match; the search ran on into the quarterback table and paired
   **Tank Bigsby with 18.0.** Fixed: one `<tr>` at a time.

**FIVE NEGATIVE CONTROLS RUN FIRST AND ALL PASS** (§0.2): numbers agree and it stays quiet; the real
18 Sept Vele defect and it fires; the week-0 duplicate counts as one game; Hurts at 21.6 against a
rushing-only 4.6 is NOT flagged; and the Bigsby trap does not reattach. `py check_vintage.py
--selftest` runs them.

**WHAT IT DOES NOT DO, stated so nobody assumes otherwise: it does not correct the page.** The sheet
still prints 5.8 and a 0.0 drop cost for Vele. The guard makes that impossible to ship *silently*,
which is a smaller claim than fixing it. Fixing it is batch A in section 5.

---

## 2. THE ONLINE PAGE AND `ff.bat` ARE TWO CLOCKS

Matt: *"clarify, 'New online page', it will fire/update with ff.bat or no?"*

**No, and it cannot.** `ff.bat` runs five Python scripts on his Windows machine and writes local
files. **Nothing in it touches claude.ai**, and nothing could: publishing needs a session with the
artifact tool.

The page refreshes on a separate cloud task, *Refresh the Juggers Pocket Sheet*, Sundays and
Tuesdays 12:30pm ET, **timed to fire after the morning `ff.bat` and read whatever it wrote.**

**THE WEAKNESS IN THAT, NAMED BECAUSE IT IS REAL: if `ff.bat` did not run, the task republishes
older data.** It is instructed to stamp the true build time of the pull it used and to republish
nothing at all if the machine is unreachable, so the page can be old but never lies about its age.
**Checking that stamp is the whole discipline of using the page.**

---

## 3. THE SATURDAY CLAIMS, AND THE THING NO CLOUD TASK CAN FIX

Matt: *"What about the Saturday claims that went through early this AM."*

**This is the sharpest question of the six, because the answer is that there was no mechanism at
all.** ESPN settles claims on its own clock. Matt's four Windows pulls are Tue 06:00, Thu 17:30 and
Sun 11:45 and 15:30. **Saturday is none of them.** So when a claim processed this morning, every
file on the drive still described the roster he had before it: `MY_ROSTER.csv` was Thursday's, the
week sheet was Friday's, the wire was Friday's. **No page was wrong. They were all correctly
answering a question about yesterday**, which is worse, because nothing looked broken.

**AND A CLOUD TASK CANNOT CLOSE THIS.** A scheduled session can only read what his machine last
pulled; the pull itself needs his ESPN session on his hardware. So the fix has to be a Windows task,
and it is: **`FF2026 - 5 daily post-waiver`, `ff.bat` every morning at 07:30**, added to
`setup_tasks.bat`. He runs that file once as administrator and it re-registers all five.

**`py waivers.py --live` is a separate matter and is still not scheduled.** It is in no batch file
and never has been. That is deliberate: it writes `waiver_report_2026.csv`, the file five seasons of
analysis read from, and a half-write on a schedule would poison it. It needs his cookies, so it is
his. **It has not run since 11 Sept, and it is the named input for the trade-record thread.**

---

## 4. WHAT THE PLAYER ARGUMENTS ACTUALLY CHANGED, AND WHAT THEY DID NOT

Matt: *"Are resolutions to those able to be fired now and fully implemented to avoid recurrence?"*

**Partly, and the honest split matters more than a yes.**

| what was settled | where it now lives | does it fire? |
|---|---|---|
| Kicker drop is Pineiro, not Demercado | `matt_todo.txt` | no. a note he reads |
| Coleman claim rides | `matt_todo.txt`, doc 370 | no. a note he reads |
| Vele is not the cheapest man he owns | doc 373 | **yes, via `check_vintage.py`** |
| Schultz's 11.1 is a base rate, not a forecast | doc 371 | **no. nothing checks this** |
| Two-signal vs three-signal is a factor of five | doc 371 | **no. nothing checks this** |

**So one of five fires. The other four are prose in a document**, which is §0.5(f)'s failure in its
purest form: the fix went into the record rather than into the thing that runs. **The two screen
items are the ones that will recur**, because the page still prints an identical 11.1 beside two
different men and nothing refuses to build it. That is batch B.

---

## 5. THE CATALOG FOR THE PROJECT RED TEAM

Matt: *"you are not the only chat/model to encounter this... I feel like i've heard that before, but
i also want to say i keep hearing that. This is cause for a red team of the project."*

**He is right, and the recurrence is the finding.** Four errors in twenty-four hours with one shape.
The directive has three rules aimed at it (§0.2, §0.6, §3) and **all three address the writer of a
finding, not the reader of a page.** The pages carry no provenance, so there has never been anything
to check. Catalogued first, per §0.5(c)1, so the shape is visible before anyone investigates.

| # | batch | what it asks | size |
|---|---|---|---|
| **A** | **The page tells you what a number is** | Every rate a page prints carries `proj`, `2026` or `rate`, and the drop-cost column takes the higher of projection and season. Extends `check_vintage.py` from a report into a contract | one session |
| **B** | **A base rate may not wear a player's name** | The screen's 11.1 and 38% print identically for every man who clears it. Guard: refuse to print a population rate beside a name without its population and its n | one session |
| **C** | **The generated-page linter** | `{{`, `}}` and unsubstituted `{token}` in any built page. Doc 369 found eleven dead CSS rules by hand; nothing stops the twelfth | half a session |
| **D** | **Which instrument governs a two-signal player** | The sheet says 38%, §4.30 says 7.1%. A factor of five, unresolved, and it decided a recommendation | one session |
| **E** | **Every hand-written constant that reaches a page** | `STATIC_TOP`, `STATIC_BOTTOM`, the standing-rules block. Name the fact each asserts and where it is checked. Doc 372 found two false ones in `STATIC_TOP` alone | one session |
| **F** | **The trackers** | `open_threads.py` scrapes its own output: 21 nested rows, 5 four deep. And the to-do list records asks, never completions | half a session |
| **G** | **The outside check** (§0.5(c)6) | What do people who build decision pages for a living do about stale inputs? The `target="_blank"` reversal came off WCAG 3.2.5 and cost nothing | half a session |
| **H** | **The directive itself** | 57 KB of resident set, read every turn, and last night it did not stop four errors of one kind. Is any of it load-bearing, or is it read past? | one session |

**RUN A AND C FIRST.** A closes the defect that caused every error in the last day, and C is the
cheapest thing in the list with a known live miss behind it. **H should run LAST and by a different
model**, because a file cannot audit whether it is being read past, and the session that has been
reading it all night is the worst judge of that.

**WHY FABLE FOR THIS.** Every red team this project has run was internal-consistency work, and every
one was run by the session that wrote the thing. Batch H in particular needs a reader with no stake
in the directive being useful. **The tasking file is `Source\REDTEAM_TASKING_PROMPT.md`**, which
already exists and already carries the convention; these batches append to it as numbered jobs, one
per batch, each with its own negative control named before it runs.

**THE STANDING CONSTRAINT ON ALL EIGHT, and it is the one this project keeps breaking: a batch is
not finished when the defect is described. It is finished when something refuses to build.**
