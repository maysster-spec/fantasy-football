# 464. THE TICKET PRICED IN PLAYOFF ODDS, AND THE LEVEL READING THAT DID NOT HELP

*1 Oct 2026, 10:30 ET. Claude (Cowork). Matt, 10:05: "You can continue running." Two of doc 463's four metrics run,
one unblocked at the source. 464 reserved by listing `Source\`. No em dashes.*

---

## 0. WHAT TO DO

1. **Nothing to run. Tomorrow's 07:30 run writes `schedule_2026.csv` off ESPN's matchup view (one more read in
   `wire.py`), and the playoff-odds simulation runs on it the same day.**
2. **A measurement that qualifies yesterday's posture rule, surfaced because it binds (0.5b).** At equal expected
   points, a lottery ticket beats the same points spread evenly only for a team UNDER about 30% to make the
   playoffs (+0.5 to +1.3 points of playoff probability over the steady version); it is a wash from 30 to 60% and
   loses above 60%. Your rule "take a chance before it is too late" is measured true exactly when it is nearly too
   late, and not before. Until your own number is on the page, the operating rule is: **a ticket is bought with a
   seat that costs nothing (a man worth 0.0 on the grid, which is what Bryant and Allgeier cost) and never with a
   man who gives you a steady point a week.** v9.38's rule (rank the lane on the tail when outside the top six by
   points) stays for now; the trigger should become your simulated top-six odds under 30%, and that is queued for
   v9.39 once the schedule file exists and your number is real.
3. **The exchange rate, for the next time a ticket is priced (section 2):** for a mid-table team at the end of
   week 3, +2 a week for the rest of the season is worth about +8 points of playoff probability, +5 a week about +20,
   a +15 flex for six of the eleven weeks about +30. A committee-partner ticket (8.5% to six-plus weeks) is therefore
   worth about +2.5 points of playoff probability; a lead back under the bar (19%) about +6; a handcuff (5%) about
   +1.5. A steady +1 a week is worth +4. That is the number the seat list's "expected" column was missing.
4. **The level reading does not help (4.48's open line, closed).** Reading each back's shape off the team's last game
   before the cut rather than the four-week average does not separate the cells (lead 26% a big month against 28%,
   committee 13% against 14%, handcuff worse), and only 72% of men land in the same cell under the two readings. The
   average stays the shipped reading; `tail_tickets.py --last-game` is the record.
5. **The model's honesty (section 1):** at the end of week 4 it scores 0.23 by Brier across four seasons against a
   coin flip's 0.25 and the naive "current top six" rule's 0.38; by week 8 it is 0.19 and by week 10 0.15. Four weeks
   of scores barely separate twelve teams, and the page will say so beside the number.

---

## 1. THE PLAYOFF-ODDS MODEL AND ITS BACKTEST

**THE CLAIM IN TESTABLE FORM:** a team's probability of a top-six finish, simulated from each team's scoring to date
(shrunk toward the league mean by four weeks' worth) and the league's measured weekly spread (21.2 points within a
team, 2022 to 2025) over the remaining schedule, predicts the actual top six better than the current standings do.
POPULATION: every team, 2022 to 2025, cut at the end of weeks 3, 4, 6, 8 and 10; `Scripts\research\playoff_odds.py
--backtest`; ESPN's "Playoff Bye" placeholder rows dropped. RESULT, Brier (lower is better, 0.25 is a coin flip on
each team): week 3 0.230, week 4 0.231, week 6 0.192, week 8 0.193, week 10 0.152; the naive binary rule 0.375,
0.375, 0.333, 0.250, 0.208. TESTED: better than the standings at every cut, and only modestly better than a coin
flip before week 6. Standings are wins then points for; the simulator has no week-specific lift, so a six-week burst
is approximated as its average over the weeks left, which understates a burst's lumpiness a little.

## 2. THE CONVEXITY TEST

**THE CLAIM (0.3, and Matt's "take a chance before it is too late"):** at equal expected points a ticket (probability
p of +15 a week for six weeks, else nothing) raises playoff probability more than the same expected points spread
evenly, and more so the further behind the team is. `playoff_odds.py --convexity`, every team at the end of week 3,
four seasons, p at 8.5% (the committee cell), 19% (the lead-back cell) and 30%.

| the team's odds at week 3 | n | p | steady, points gained | ticket, points gained |
|---|---|---|---|---|
| under 30% | 11 | 8.5% | 1.3 | 1.8 |
| under 30% | 11 | 19% | 3.1 | 4.0 |
| under 30% | 11 | 30% | 5.1 | 6.4 |
| 30 to 60% | 19 | 8.5% | 2.7 | 2.6 |
| 30 to 60% | 19 | 19% | 6.0 | 5.7 |
| 30 to 60% | 19 | 30% | 9.5 | 9.0 |
| over 60% | 18 | 8.5% | 1.7 | 1.2 |
| over 60% | 18 | 19% | 3.6 | 2.6 |
| over 60% | 18 | 30% | 5.5 | 4.2 |

TESTED: the direction is the convex one and the size is about a point. The practical reading is in section 0.

## 3. WHAT CHANGED

`wire.py`: `write_schedule()` and the mMatchupScore read after the standings, every run, `schedule_2026.csv`
(unit-tested on a synthetic payload; the live shape is ESPN's and the first run reports its count). `research\
playoff_odds.py` (new, pinned): live, `--lift`, `--backtest`, `--convexity`; `run_playoff_odds.txt`. `research\wk1\
tail_tickets.py`: `--last-game`. `check_kit.py`: three pins. `check_locals.py` clean on `wire.py`.

## 4. OPEN, BY NAME

- The live number: `py research\playoff_odds.py --lift 5` the morning after the schedule lands, and the standings
  line on the week sheet to carry it (the page says "ESPN projects you to finish 4"; it should say your top-six odds
  and what +5 a week would do to them).
- v9.39: the posture rule's trigger as simulated odds under 30%, with this doc as the measurement.
- Seat-weeks per startable week on his bench; the fixture roster for the harness; `audit_directive.py` on the drive
  tree; the catalog's remaining batch; the payload wiring; the store move when it crosses 1.6 million.
