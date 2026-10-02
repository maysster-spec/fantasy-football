# 468. THE MATCHUP IS WORTH A POINT AT BACK AND TIGHT END, AND NOTHING AT RECEIVER

*1 Oct 2026, 19:30 ET. Claude (Cowork). Matt, 19:00: "directive is updated. i see items on the claude todo list. Can any
of those be actioned now that the directive is in?" Nothing on the list was waiting on the paste; four items were
waiting on me. 468 reserved by listing `Source\`. No em dashes.*

---

## 0. WHAT TO DO

1. **A new tiebreak, measured, not yet on the page: at running back and tight end, the opponent's points allowed per
   game to the position so far this season is worth about a point a week between the softest and hardest quarter of
   defenses, net of the man's own rate and of the pregame line; at receiver it is worth nothing.** Use it only
   between two men within a point of each other at RB or TE, and never at WR. Running back: +1.2 a week, positive
   in all five seasons. Tight end: +0.9, positive in four of five. Receiver: +0.4 and the sign flips by season.
2. **Sunday's flex line does not move.** Dobbins against San Francisco reads +0.1 on three weeks of this season
   (SF allows 19.8 a game to backs against a league mean of 18.5), which is inside the noise of three weeks. Nacua if
   he is active (drop Barner for the move); otherwise Dobbins over Raymond, as before.
3. **`audit_directive.py` runs clean, 51 of 51.** It had never been run in season; its first run reported 15 false
   failures because it read the keeper table against the NEWEST projection pull (section 1.1: ESPN's ADP drifts once
   the season starts) and against the actual keepers, when the draft book says the table was solved on the 09-03
   pull of the predicted list. On that pull and that list the twelve ADPs reproduce exactly. One real correction:
   finding 4.14's sentinel count is 330 of 482 on the shipped board, not 328 of 480.
4. **The scheduled runs are checked (claude_todo, doc 439):** 30 Sept 07:30, 1 Oct 07:30 and 1 Oct 17:30 all logged
   the RESULT line in the new shape (form, snaps, depth, lines, inherit, projections, then the guards). The 17:30 run
   built tonight's page with doc 467's engine on your machine: no defense on the priority list, the week-8 kicker row
   on the calendar, every guard 0 including the two new ones.
5. **v9.38 is in and nothing else waited on it.** The crowd-check line it carries closes one item. v9.39 waits on
   tomorrow's 07:30 run writing the schedule file (the posture trigger as your simulated playoff odds), and this
   doc's finding rides with it as 4.49 so you paste once.
6. **Nothing to run.**

---

## 1. THE MATCHUP TERM

**THE CLAIM IN TESTABLE FORM:** among receivers and tight ends with three or more games played so far, the coming
opponent's half-PPR points allowed per game to the position through the previous week (centred on that week's league
average, so "soft" is relative to the field) predicts the man's points in the coming week, net of his own half-PPR
rate to date; direction positive. POPULATION: nflverse regular season 2021 to 2025, weeks 5 to 18, defenses with four
or more weeks of record; 17,799 player-weeks (8,444 WR, 4,114 TE, 5,241 RB, the backs added as a comparison).
DECISION FORM (0.5(a7)): between two men of equal rate, the gain in points a week from taking the softer matchup, top
quartile of defenses against bottom. The bar was set before the run at a point a week, the size byes are worth
(4.11); under it, the term is not a page term.

| position | coefficient per point allowed above the mean (se) | same, net of the own implied total (se) | top against bottom quartile, points a week | seasons positive |
|---|---|---|---|---|
| WR | 0.022 (0.014) | 0.021 (0.014) | +0.37 | 3 of 5 (2023 +1.16, 2024 minus 0.60, the other three within half a point of zero) |
| TE | 0.118 (0.028) | 0.111 (0.028) | +0.89 | 4 of 5 (2023 flat) |
| RB | 0.113 (0.023) | 0.096 (0.024) | +1.24 | 5 of 5 (+0.5 to +1.6) |

TESTED. The own rate carries the forecast (rho 0.50 to 0.60 with next week at every position); the defense term is a
small, real second read at RB and TE and nothing at WR, which is the same shape 4.39 found for the line (real at D/ST
and QB, nothing at kicker). The own implied team total, added as a control, takes little from it (+0.04 to +0.06 a
point of implied total at TE and RB, nothing at WR). This is the crowd's own instrument (ESPN's positionAgainstOpponent
is this number for this season), measured on the question it is used for.

**AGAINST WHAT WE ALREADY HELD (0.5(b), surfaced because it binds).** Doc 227 measured the matchup on the PRIOR season's
points allowed (what a drafter can see in August): QB about a point, RB +0.56, WR and TE null, and set the rule "never
move a receiver or a tight end for a matchup." It also measured the same season's full-year average at about three
times that size and set it aside as hindsight. This season's points allowed TO DATE is the third instrument, the one a
lineup decision can actually use, and it lands between the two: real at RB and TE, nothing at WR. So doc 227's rule
stands at receiver and is qualified at tight end, and 4.33's "elsewhere, take the player" stands with a within-a-point
tiebreak at RB and TE. The wire's streaming sentence said "receivers and tight ends: matchup is worth zero week to
week"; it now says backs and tight ends take it as a tiebreak within a point and receivers not at all (`wire.py`,
re-pinned).

**THE OUTSIDE CHECK (0.5(c)6):** points-allowed-by-position rankings are published everywhere and used as a start/sit
input at every position. The measurement says that is right at RB, marginal at TE and wrong at WR, where the receiver's
own rate is the whole forecast.

**THIS WEEK, ON THREE WEEKS OF 2026** (thin; the measurement needed four): his backs read Dobbins at SF +0.1, Jeanty
at KC minus 0.1, Judkins at PIT +0.1, Dowdle at CLE minus 0.4; his tight ends LaPorta against CAR +0.1, Barner at LAC
minus 0.2. Nothing moves across a point.

`Scripts\research\matchup_term.py` (new, pinned; `games.csv` beside it from nflverse for the line control, optional)
and `run_matchup_term.txt` (without the line), `run_matchup_term_line.txt` (with it).

## 2. THE AUDITOR

Two instrument errors, both the auditor's. The keeper table now solves on `predicted_keepers_v5.csv` and the last pull
dated on or before the 09-03 freeze, which is what the draft book says it was solved on, and prints the post-lock
table beneath as information (the lock moved nine rows by one keeper: a kicker and a defense replaced two predicted
keepers). The sentinel count: the shipped `board_v8_fixed.csv` has 482 rows, 330 inside the blob; 4.14 said 328 of
480 and is corrected in place with the old number struck. `check_kit.py`: two pins (the auditor was never pinned).

## 3. OPEN, BY NAME

- WIRE THE MATCHUP COLUMN, NOT YET RUN: a "this week" number on the roster rows and the drop ladder for RB and TE
  only, from `sched_2026.csv` (the opponent) and `form_2026.csv` (points allowed per game by defense and position this
  season), coefficient 0.10 at RB and 0.11 at TE on the centred term, printed as a plain number beside the rate and
  never sorted on; thin until week 5. One evening.
- 4.49 into the findings file and the index at v9.39, with the posture trigger, after the schedule file lands.
- The three NO EFFECT mutations; the catalog's remaining batch (A2, A3, A6, B3); the payload wiring; the week-8
  seat-weeks reading; the store move at 1.6 million; the 6 Oct checks (the first real bye in `build_form.py`, the
  Tuesday projection pull).
