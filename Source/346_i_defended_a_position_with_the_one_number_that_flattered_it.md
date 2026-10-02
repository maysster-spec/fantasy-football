# 346 — I DEFENDED A POSITION WITH THE ONE NUMBER THAT FLATTERED IT

**2026-09-18.** Matt red-teamed my Chris Brooks reply and was right on five points of six; the sixth
is a defect in `inherit_2026.csv`, not only in the reply. Four errors, all leaning the same way.

---

## 1. THE CALENDAR, AND IT INVALIDATES TWO SENTENCES

**WEEK 1 WAS SUNDAY 13 SEPTEMBER. WEEK 2 IS SUNDAY 20 SEPTEMBER, AND GREEN BAY AT THE JETS HAS NOT
BEEN PLAYED.** `[SOURCED: NFL.com Packers 2026 schedule, loaded 18 Sept 2026 — week 1 at MIN shows
FINAL 22-39, week 2 at NYJ shows "CURRENT WEEK", Sunday 20th 1:00 PM FOX]`

I wrote *"Green Bay has played the Jets since"* and *"that blurb previews a game that has already
been played."* Both false. I told Matt his own current source was stale. **The week sheet's own
masthead says "Week 2 — what to do" and is stamped 17 September; I had that in front of me.**

**AND IT KILLS MY OWN TO-DO ITEM FROM AN HOUR EARLIER.** I put `build_form.py` on his list saying
the form file was "a week behind" and that every contested band was "reading week one." **Week one
IS the season so far.** `form_2026.csv` is complete and nflverse is not behind. The note is
corrected in `matt_todo.txt`; the run belongs after Monday night, not now. **Doc 345 §3's staleness
paragraph is retracted on the same grounds.**

## 2. I LED WITH SNAP SHARE, WHICH IS THE ONE NUMBER THAT POINTED MY WAY

Week 1, from `form_2026.csv`: **Brooks 56% of snaps, 7 carries, 1 target, 2.9 half-PPR · Lloyd 44%
of snaps, 13 carries, 1 target, 3.7.**

I opened with 56 against 44. **Matt's blurb had already explained that number: "Brooks is also an
excellent pass blocker, so he'll still get time on the field even if it doesn't convert to rushing
attempts."** A high-snap, low-touch blocking role is not a path to a backfield, and **this project
measured that and wrote it down** — doc 235, the pop is the workload; doc 320, the usage order names
the inheritor. I used the metric our own work says does not name the inheritor, to defend a body on
his bench. That is not a reasoning slip, it is picking the supporting number.

**His four factual points all hold:** Brooks is not the next man up · he has not played week 2 ·
Lloyd is the lead back with Jacobs out · Brooks is on the losing side of the timeshare.

## 3. THE SEAT ROW IS VOID AND STILL PRICED — HIS POINT 1, AS A DEFECT

`inherit_2026.csv` carries `team=GB, holds_the_job=Josh Jacobs, next_man=Chris Brooks`, and its own
`why` field says: *"this seat is not an option any more, the job is already open."* **Both are in the
row, and the row still prints an odds column.**

**A SEAT IS AN OPTION ON A JOB OPENING. Jacobs went on the Commissioner's Exempt List on 30 August,
indefinite. The job opened three weeks ago and week 1 says Lloyd took the carries.** So the page
prints a probability for an event that has already happened, on a man who already lost the split it
resolved. `[OPEN]` **The testable form, written down so it is not re-invented: for a job already
vacant, the quantity is not P(it opens) × value, it is the man's SHARE of the vacated work times
what that work is worth, and the week-1 split is the only estimate of the share we have. Nobody has
run it.** §0.5(a4): NOT YET RUN, input named.

## 4. HIS POINT 5 IS RIGHT AND THE MARGIN IS NOT SMALL

The seat table on the page he is reading **ranks by what the job pays and prints a flat 46% on every
row.** Doc 343's per-man odds have never rendered: the only thing that touched `WEEK_SHEET.html`
after `sheet_engine.py` was written was `todo_page.py` re-stamping the masthead link, which moved the
file's timestamp and not its body.

Re-priced here with doc 343's bands, same "if it fires" values the page computed:

| be first to | behind | job | if it fires | wk1 share | band | odds | expected | in his league |
|---|---|---|---|---|---|---|---|---|
| **Dylan Sampson** | **Quinshon Judkins** | 210.6 | **6.1** | 0.000 | flat | 46% | **2.90** | **free** |
| Kaelon Black | McCaffrey | 302.4 | 2.4 | 0.455 | 40+ | 64% | 1.53 | taken (DUCK) |
| Tank Bigsby | Barkley | 251.6 | 2.4 | 0.048 | <20 | 48% | 1.14 | free |
| Emari Demercado | K. Walker III | 248.9 | 2.4 | 0.100 | <20 | 48% | 1.14 | free |
| Samaje Perine | Chase Brown | 239.4 | 2.4 | 0.267 | 20-30 | 44% | 1.05 | free |
| **Chris Brooks** | **Josh Jacobs** | 241.0 | **1.9** | 0.364 | 30-40 | 53% | **1.01** | **Matt's** |

**Four free men price above the one he is holding, and the top one prices at three times.**
Sorting by the job rather than by the value is what hid it, and that is the exact defect doc 343 was
written to fix.

**THE CAVEAT ON SAMPSON, AND IT IS TWO DIFFERENT OBJECTS.** His 6.1 is large because Judkins is
**Matt's own back**, so the seat is priced against the bar he would have WITHOUT Judkins. That is
the size of the hole, not a forecast of Sampson. And Sampson was **on the field in week 1 and
touched the ball zero times**, which doc 343 measured at **0 of 41** on reaching the RB bar over
weeks 2 to 14. Insurance on a starter, not a lottery ticket, and it must be sold as neither.

## 5. WHAT IS ACTUALLY AT STAKE

Expected values run 1.0 to 2.9 points. **The gap between the best free seat and the one he holds is
about 1.9 expected points**, which is real and small. Doc 240's rule is what makes it a decision at
all: a bench running back earns his spot by the job he would inherit and the fragility of the man
ahead of him, and Brooks' man is already gone.

**THE DROP AND THE CLAIM ARE MATT'S (§0.4).** Brooks was a waiver add, so he carries no keeper
eligibility to lose.

## 6. OPEN

- The open-job seat calculation in §3. `[NOT YET RUN]`
- The page has not rendered doc 343's odds. `ff.bat` does it; it is item 1 on his list.
- Doc 345 §3's "the workload lane is reading week one" paragraph is retracted (§1 above).
