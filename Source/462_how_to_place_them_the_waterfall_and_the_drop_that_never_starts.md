# 462. HOW TO PLACE THEM: THE WATERFALL UNDER THE CALL, AND THE DROP THAT NEVER STARTS

*1 Oct 2026, 09:10 ET. Claude (Cowork). Matt, 1 Oct 08:20, four points: Wilson "has not earned much"; THE CALL's "you
would drop" is not the complete picture and the waiver mechanics should be inked under it, collapsed; ff.bat run; run
the open items. 462 reserved by listing `Source\`. No em dashes.*

---

## 0. WHAT TO DO

1. **Nothing to run. Tomorrow's 07:30 run carries both changes onto the live sheet** (the 08:04 run you made has the
   long-shot lane, not these). **Your moves, read off the waiver report at 08:16: Pat Bryant for Vele and Tyler
   Allgeier for Malik Washington, both free agents, both executed at 08:14; LaPorta untouched; no Wilson claim.**
   The LaPorta row was the page's defect, not a take; you paired Bryant with Vele yourself, which is what the fixed
   page prints.
1b. **The Allgeier add settles a question the directive has carried as NOT ESTABLISHED since v9.19: a man in the IR
   slot does not count against the position limit.** You held four active backs and two on IR; ESPN accepted a fifth
   active back, seven in all against a cap of six. One observation, consistent with the IR seat being outside the
   fifteen (section 2's reading of settings line 29). Goes into v9.38.
1c. **With Vele and Malik Washington gone, a Wilson claim now costs a real man, so do not place it.** Allgeier is the
   same shape and already yours. Sunday's seat for Nacua, if he is active, comes from AJ Barner (the week-6 tight end
   is re-claimable in week 5, as the calendar says) rather than the Bengals or either new man; the page's ladder will
   price it Sunday morning.
2. **THE CALL now pairs Pat Bryant with Vele and Allgeier with Malik Washington** (+4.9 and +3.4), not Bryant with
   LaPorta. The drop ladder refused any same-position drop since doc 417, written for a starter who IS the bar; it
   now refuses one only when the man starts (his cost on the bye grid is above zero). Vele never starts, so dropping
   him moves no bar and the pairing is exact. Your sentence was the rule: the lowest-value man comes first.
3. **"How to place them" sits under THE CALL, folded.** Your rank off the standings file (11 of 12 this week), what
   a claim is worth at that rank (a contested man priced at nothing in the bottom half of the order; an uncontested
   claim lands about 78% whatever the rank; a free agent is immediate), the order rule (the contested man first,
   ESPN demotes a winner mid-run), each row as a sentence (CLAIM or ADD, the drop, the contested share by his last
   game, the expected points at your rank against the table's net), the drops two ways (all land: a different drop
   on each; first-wins: the same cheapest drop on every claim, which is the hedge), the run times, and the line that
   the long shots are claims too whose drop is the hedge man.
4. **Your Wilson challenge, tested, in the reply at 08:50 and filed here:** a man's own efficiency on weeks 1 to 4 does
   not predict his tail at these sizes (section 1). The claim stands with its confidence stated; the directive's
   4.6 and 4.20 already say the job is the signal and efficiency is priced.
5. **Not quoted anywhere on the page, on purpose:** the 61.1 / 29.1 / 11.2 ladder (retracted, doc 401). The waterfall
   uses doc 396's 71.4% uncontested share and 78% uncontested landing, doc 314's contested share by last-game usage,
   and doc 224's 16%, your own contested record; all in `sheet_constants.json` under `claims`.

---

## 1. THE WILSON TEST

**The claim in testable form (his words: "I doubt he has earned much ... the coach thinks much will improve with
swapping him out"):** among committee partners at the end of week 4 (the second back with 8 to 14 touches a game,
under the bar; doc 460's cell, n=59), the man's own yards per touch and points per touch on weeks 1 to 4 predict the
big-hit columns over weeks 5 to 14. nflverse 2021 to 2025; `tail_tickets.py`'s builder with the ratios added (run
inline, not a script of its own; the cells are in `run_tail_tickets.txt`'s companion lines below).

| split | n | 4+ startable weeks | 6+ weeks | a 15-point month |
|---|---|---|---|---|
| committee, under 4.0 yards a touch | 25 | 12.0% | 4.0% | 4.0% |
| committee, 4.0 and over | 32 | 34.4% | 12.5% | 21.9% |
| handcuff, under 4.0 | 25 | 24.0% | 8.0% | 4.0% |
| handcuff, 4.0 and over | 30 | 3.3% | 0.0% | 6.7% |
| lead under the bar, under 4.0 | 21 | 47.6% | 14.3% | 28.6% |
| lead under the bar, 4.0 and over | 20 | 50.0% | 15.0% | 25.0% |
| all three pooled, under 4.0 | 71 | 26.8% | 8.5% | 11.3% |
| all three pooled, 4.0 and over | 82 | 26.8% | 8.5% | 17.1% |

Inside his cell the split leans his way (Fisher on four-plus weeks p=0.067); inside the handcuff cell it runs the other
way as hard (p=0.039); pooled it is flat; and yards per touch on weeks 1 to 4 against yards per touch on weeks 5 to 14
among the same men correlates at 0.09 (Spearman, n=122). Points per touch: no correlation with either outcome (rho
minus 0.06 and 0.03). The one lean that is not noise-shaped: backs with targets under 15% of their touches trail on
six-plus weeks (4.7% against 10.0%, n=43 and 110, not significant). Wilson: 3.30 yards a touch, one target in three
games, the 8th percentile of his cell on points per touch. **TESTED: his efficiency read does not predict the tail at
this sample; the direction inside his own cell is his and the pooled and stability tests are not.** The coach's view
is BLOCKED except through the touches themselves (9 to 8 last game, with Price questionable).

## 2. WHAT CHANGED

`sheet_engine.py`: `waiver_rank()` (off the standings file); `waterfall_html()`; `_contest_share()`; the pairing loop
allows a same-position drop whose bye-grid cost is zero (`_grid`), collects the waterfall rows and names the hedge man
before any drop is spent; `render()` takes `wrank`. `sheet_constants.json`: `claims`. `check_guards.py`: the
own-position mutation re-aimed at the new predicate (NO EFFECT on today's roster, where the cheapest men are the
same-position non-starters either way; the fixture roster, catalog A5, is what would show it). `check_kit.py`: two
pins. Guards clean on the rebuilt page; the waterfall's claim branch exercised directly at ranks 11, 3 and none.

## 3. OPEN, BY NAME

- The waterfall prints THE CALL's rows; a long shot he claims is covered by one sentence, not a row. A row per long
  shot when the lane leads is the next step if he asks.
- The contested share by last game is a league base rate (doc 314); whether `own_chg` predicts contention in THIS
  league is still NOT ESTABLISHED (doc 396) and starts being answerable mid-October.
- Directive v9.38 (4.44 to 4.48, the open-job amendment, the crowd line), next.
