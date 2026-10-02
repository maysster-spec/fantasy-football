# 469. THE CARD, THE ODDS, AND THE BACKUP WHO IS ONLY A BACKUP

*1 Oct 2026, 20:40 ET. Claude (Cowork). Matt, 20:00, five points: the waterfall against ESPN's Pending Moves card; "what is
the deal with Tank Bigsby"; "why do we wait on this?"; the scheduled task that ran out of tokens; "can this not be run
now? audit_directive.py". 469 reserved by listing `Source\`. No em dashes.*

---

## 0. WHAT TO DO

1. **Paste directive v9.39** (on your list). One finding (4.49, the matchup tiebreak at RB and TE, doc 468) and one rule
   change: the long-shot lane leads the seat list when your SIMULATED odds of a top-six finish are under 30%, not when
   you are outside the top six by points. The standings line prints the odds every run now.
2. **Your number tonight: 39% to make the top six, simulated on the weeks left; +5 a week for the rest of the season
   would make it 58%.** At 39% a long shot and the same points spread evenly are worth the same (doc 464: the long shot
   wins only under 30%), so tonight the seat list leads and the lane follows it. "Take a chance before it is too
   late" is the right rule, and the measurement says it is not yet late.
3. **Tank Bigsby: do not spend the claim. He is a pure backup behind a healthy man, and his seat is the thinnest shape
   on the lane.** The take, in the contract's five lines, is in section 2. If you want a backup back with a real
   tail, Tyler Goodson is the same shape, free (no priority spent) and behind a bigger job; MarShawn Lloyd is the
   fattest shape on the wire but costs a claim. Your receiving hunch tested in your direction and is too thin to
   call (section 2).
4. **The waterfall is a card now, in the shape of ESPN's Pending Moves:** one row per move, the add, the drop, the
   morning it processes (ESPN's own clear time), the priority to set, the odds it lands and the expected points.
   Free agents first as "now", claims in the order to set them. The prose under it carries only what the card
   cannot show. Next build.
5. **The scheduled task that ran out of tokens is the Tuesday wire read** (29 Sept, 33 minutes, the only failure
   among your four). Its prompt is a 2,500-word research program that recomputes three lanes `wire.py` now builds
   every morning. It is rewritten to the judgement layer only (news on your men and the page's top names, a verdict
   on the pages your machine built); the old prompt is archived on the drive. Windows Task Scheduler cannot take it:
   it needs the web and a judgement. Section 4.
6. **`audit_directive.py` was run this evening, doc 468: 51 of 51.** The to-do line that said it needed the bridge
   shell was closed there; the kit was staged into the sandbox instead.
7. **Nothing to run.**

---

## 1. THE ODDS, AND WHY THE WAIT WAS MINE

Doc 464 queued v9.39 for "the morning the schedule lands", and doc 468 repeated it at 19:30, after the 17:30 run had
already written `schedule_2026.csv` (84 matchups, 18 scored). I did not look. The number ran the moment I did.

`playoff_odds.live_numbers()` is the one place the number is computed; the week sheet's standings line prints it with
the +5 lift, the lane reads it for its placement, `check_page_logic.py` P6 reads the printed odds to judge the
placement and P6b holds the printed odds to the simulator within a point. The points-for rank is the fallback when the
schedule file is absent, and the lane's lede says which rule placed it.

## 2. BIGSBY, IN PLAIN TERMS

**The take: do not claim Tank Bigsby (PHI RB) this week.**
- VINTAGE: 2026, 3 games: 5.7 touches a game, 1 target a game, 1 touch last game, 3.4 points a game on 16% of the
  snaps. Projection: 3.1 a week.
- POPULATION: the lane puts him in "handcuff behind the number 29 job": of men in that shape at week 4 over five
  seasons, 6% went on to six or more startable weeks and 6% to a 15-point month; a shape's rate, not his forecast.
- THE MAN AHEAD: Saquon Barkley, 13.3 touches a game this season (an unusually light load for him), played 16 of 17
  last season, no injury tag today.
- THE STANDING RULE AND THE ROSTER AFTER: "buy the job, never the name" (4.20); the job he would inherit is the 29th
  by this season's touches. The claim as THE CALL pairs it drops AJ Barner (TE2), which leaves fifteen with one tight
  end and LaPorta's bye in week 6 to cover again. Bigsby would be your sixth back, at the cap.
- THE COUNTERFACTUAL: +1.3 expected on the card (+1.9 if he lands, 70% at your rank). Tyler Goodson (DAL, free,
  behind Javonte Williams at 18.3 touches a game, the number 13 job) is the same 6% shape for no priority and behind a
  job worth more; MarShawn Lloyd (GB, a claim, 9.7 touches a game as the lead) is the fattest shape on the wire (a
  thin cell: about 22% to a 15-point month, 56% to four startable weeks).

**Why THE CALL named him anyway, and the honest tension.** THE CALL prices a seat on the mean: the job's size on the
August board (252 for Barkley's) times the odds the man ahead goes down, so a backup behind a big name prices well.
The lane prices the tail, which is the unit you asked for, and it says 6%. Two lists, two currencies; at 39% to make
the playoffs the mean is the right unit tonight, and the mean says +1.3 for a seat that costs a tight end. That is not
a claim worth a priority.

**Your hunch, tested.** The claim in testable form: among week-4 bench backs in doc 460's cells (handcuffs and
committee partners, under the bar, 2021 to 2025, n=130), the back's own targets a game on weeks 1 to 4 predicts the
big-hit columns over weeks 5 to 14, direction positive. RESULT: among the 71 handcuffs, under 1 target a game 0 of 27
reached six startable weeks, 1 or more 2 of 44 (4.5%); the 15-point month runs the other way (7.4% against 4.5%);
Spearman +0.10 (p=0.39). Among the 20 handcuffs whose lead did go down, 1 or more targets a game gave 2.6 startable
weeks on average against 1.3, 15% against 0% to six weeks, on cells of 13 and 7. TESTED, direction yours on the
column that matters, underpowered, not a page term. Bigsby sits at exactly 1.0 a game, on the line.

## 3. THE CARD

`waterfall_html()` rebuilt: a table with the columns priority, move, lands, expected. A free agent reads "Add X now,
TEAM POS, a free agent / drop Y, TEAM POS / no claim, no priority spent"; a claim reads "Conditionally add X, TEAM POS
from Waivers / Conditionally drop Y / processes the morning of DAY, contested N% of the time by men with his last game;
+Z if he lands", with the morning read off ESPN's own clear time on the wire row (`clears`, carried through `wire.py`
and the harness now). Claims are listed in the order to set the priorities, the contested man first. Open by default.
`check_page_logic.py` P7 reads "Conditionally add" as a claim; two controls added. On tonight's inputs the card reads:
Add Tre' Harris now (drop Pat Bryant), +5.3; 1, Conditionally add Tank Bigsby (drop AJ Barner), processes the morning
of Sat 3 Oct, 70% to land, +1.3 expected.

## 4. THE TUESDAY TASK AND THE TOKENS

Four scheduled tasks on the account: the publish at 08:54 (succeeds daily, about a minute), the pocket sheet Sunday and
Tuesday at 12:30 (succeeded 29 Sept, 13 minutes), the Sunday 11:40 window (succeeded 27 Sept, 6 minutes), and the
Tuesday wire read at 08:00 (FAILED 29 Sept after 33 minutes). The Tuesday prompt grew
from "the judgement layer" to a program: news on every man plus the newly free, two nflverse downloads, the usage lane,
the late-pick signals, the share behind a healthy starter, the drop pricing, the legal-drop check and the IR check, all
of which `wire.py` and `sheet_engine.py` compute every morning since docs 300 to 462. A task that redoes the arithmetic
in prose, at the model's pace, is the one that runs out. The replacement prompt reads the pages and the log, does the
news half and the verdict, and keeps every boundary; it is `Source\TUESDAY_WIRE_PROMPT.md` and on the task, and the old prompt is `_archive\tuesday_wire_prompt_20260923.md`. Nothing deterministic was
moved off Task Scheduler, because nothing deterministic was on the Claude side to move.

## 5. WHAT CHANGED, AND OPEN

`sheet_engine.py`: the card, `playoff_odds()`, the odds on the standings line, the lane's trigger. `wire.py`: `clears`
on the free rows. `research\playoff_odds.py`: `live_numbers()`. `check_page_logic.py`: P6 on the odds, P6b, P7 on the
card, P10 (THE CALL's net equals worth minus the cost with a negative cost at zero: the negative-cost mutation had
SURVIVED the harness on tonight's roster, where Pat Bryant is the drop at minus 2.4); 61 controls. `check_page_rules.py`:
two dead sentences, two live lines, six controls. `Source\fixture\`: Pat Bryant in the IR slot in place of Malik
Washington, who is on the wire now. `check_guards.py`: live roster 7 caught, 3 NO EFFECT; fixture 6 caught, 4 NO
EFFECT; the two never caught on either are "drop may empty a starting slot" and "a man replaces himself". Directive
v9.39, findings 4.49, changelog, `00_START_HERE.md` version 23. `check_kit.py` pins.

Open, by name: the matchup column on the page (RB and TE, doc 468); the two mutations no fixture reaches; the catalog's
remaining batch (A2, A3, A6, B3); the payload wiring; the week-8 seat-weeks reading; the store move at 1.6 million; the
6 Oct checks. Yours: paste v9.39; Sunday's flex and the Nacua move; the Opus chat export.
