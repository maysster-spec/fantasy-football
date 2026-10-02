# 456. BELL'S ROW EXPLAINED, THREE MEASUREMENTS, AND THE PAYLOAD WE NEVER READ

*30 Sept 2026, 23:40 ET. Claude (Cowork). Matt's twelve points of 30 Sept 22:30, after his 21:46 run (every term 0,
P3 and P4 live, the crowd table on the sheet). 456 reserved by listing `Source\` (455 is the catalog). No em dashes.*

---

## 0. WHAT TO DO

1. **Nothing changes tonight: Gordon first for Vele, Mayer second for Perine, two claims.** Gordon is a claim, not a start:
   the sheet never said start him, and the podcast's two reasons (one projected target, a bad week-4 draw then the bye)
   are both inside our price, which is the job for the weeks Achane is out, not this Sunday.
2. **Bell's row, read plainly.** "worth now" (renamed "this week, as he is") is what he adds to your nine if you started him
   this week at his current rate: 0, because 3.9 a game is under your 10.0 bar. The week cells are what a HIT adds (12.7 a
   game against the bar, so +2.7 most weeks, +4.7 in the Adams and Nacua bye, +4.1 in Pickens'); "if it fires" sums them
   (19.5). "odds" was "out of reach: needs 38% of the passing game" and "expected" a dash because the reach gate zeroed
   him: at his points per target, the hit size needs 10.8 of Miami's 28 targets a game, over the most any receiver has
   held. **I tested the gate on the screened men and it does not hold there (section 1), so the row now prints 27% and
   an expected 5.2, with the stretch beside it as a caution.** Bell is a priced ticket now; at 5.2 he sits under Badie
   (6.9) and above Mitchell (4.0), so he is not in the five shown and he is not a claim ahead of the two tonight.
3. **Your draft hunch about two Rams receivers is measured and it dies: a same-team pair neither busts together nor
   cannibalises week to week** (section 2; 148 pairs, 1,636 pair-weeks, every difference inside the noise). What cost you
   was Nacua's availability, which is finding 4.22 and was known: prior-season games missed predicts. The lesson for
   August 2027 is the one already on file, not a new stacking rule.
4. **The job's size does not move the relief rate: the flat 12.1 stands** (section 2; 30 absences, slope minus 0.08 a
   point, interval minus 0.29 to +0.20). Gordon on Achane's job and Badie on Coleman's are priced the same on purpose now.
5. **The wire writes your standings every run from tonight, and the sheet prints them first in the watch list** (record,
   seed, points for against the league median and the sixth-best total, ESPN's projected finish). Until the next run I
   cannot check "my team has not been putting up enough points"; no file held it. Section 4 says what to do with it.
6. **The payload audit found what else ESPN sends that nothing reads** (section 3): this week's news blurb for 312 men,
   `droppable` (16 men the league will not let you cut), `injured` (the IR-eligible set exactly), ESPN's expert ranks by
   source, and the position-against-opponent ratings. **Weekly projected points are NOT in the payload: the pull never
   asks for them.** One possible defect to test: ESPN counts 17 games on every D/ST projection row and 14 on everyone
   else's, so the sheet's D/ST season rate may run about a fifth high; the matchup rule, not that rate, picks your
   defense, so nothing on THE CALL moves.
7. **A parked man due back prints on the sheet now:** Nacua, questionable, back 4 Oct: to start him you move him to an
   active seat first, which costs a drop no claim makes for you, and the ladder names the man. Do it before his kickoff.
8. **Paste nothing tonight. Tomorrow's first batch is directive v9.38:** index rows for the two measurements above and the
   gate amendment, and the crowd check as a standing line in 0.5(c)6. One paste for all of it.

---

## 1. THE REACH GATE ON THE SCREENED MEN

**The claim in testable form (Matt: "I still don't understand why we have him as low given upside"):** on doc 453's week-3
population (young receivers, NFL years 1 to 3, not startable before, read on weeks 1 to 3, n=174, 29 hits), apply the
page's gate exactly as `reach_check` does (need = his targets a game times 12.71 over his points a game; share = need over
his team's targets a game; out of reach above 37.8%). If the gate rules out the men who went on to HIT, its assumption
(his points per target stay where they are) is wrong for this population. `Scripts\research\wk1\reach_gate_test.py`.

| cell | hit rate |
|---|---|
| whole population, out of reach by the gate | 5 of 66, 7.6% |
| whole population, in reach | 24 of 108, 22.2% |
| three of three, out of reach | 1 of 3 |
| three of three, in reach | 16 of 36, 44.4% |
| three of three and under the bar (the wire, doc 453's cell), out of reach | 1 of 3 |
| three of three and under the bar, in reach | 3 of 12, 25.0% |
| points per target, weeks 1 to 3 then 4 to 14, median: hits | 1.32 then 1.51; rose for 66% of hits |
| the same, misses | 1.25 then 1.24; rose for 44% |

The gate is a real screen on the broad population and nothing on the screened men: three men, one hit, and the hit it
would have excluded is George Pickens, 2024, at 43% of Pittsburgh's throws, who became startable at 11.7 a game. The cell
rates of doc 453 were measured on a population that INCLUDES the gated men, so zeroing a screened man applies the
constraint twice. The fix: for a man who clears the three marks (preseason or in-season), the odds stay the cell's, the
expected is priced, and the row says "a stretch: needs 38% of the passing game; men asked for that much hit 8% against 22%
for the rest". The workload lane (Otton, Helm) keeps the gate as it was: the gate was not tested on that population.

## 2. TWO MEASUREMENTS, BOTH NULL

**The same-team pair (Matt's point 5).** Testable form: for each team-season 2021 to 2025, the top two receivers by
targets (both with 8+ weeks), weeks 1 to 14, half-PPR; do their weekly points correlate more (bust together) or less
(cannibalise) than the same receivers re-dealt across teams, and is the pair's 30-point week any rarer? n=148 pairs,
1,636 pair-weeks; among starter-quality pairs (both 10+ a game) 33 pairs, 367 weeks. Within-pair weekly correlation
+0.012 against a control of +0.007 (difference +0.005, interval minus 0.05 to +0.06); median pair +0.009; 30-point weeks
15.6% against 14.8%; spread of the sum 10.2 against 9.8 points. Among starter pairs every number is under 0.05 either
way. The pooled +0.09 is a level effect (good offences carry two good receivers, +0.40 across pairs), not a weekly one.
Nothing supports a same-team penalty. `Scripts\research\wr_pair.py`, `wr_pair_results.md`.

**The job's size (catalog B1).** Testable form: across running-back absences 2021 to 2025 (a starter who led his team in
carries plus targets at 10+ a game, out for 2+ consecutive team games), the relief back's points a game during the
absence against the starter's points a game before it. n=30 absences, 24 starters. Relief rate mean 11.1 (10.0 to 12.3),
median 11.3; slope minus 0.076 a point (se 0.14, 95% minus 0.29 to +0.20); terciles of job size 11.0, 11.8, 10.6; with
the relief back's own prior scoring held fixed the job slope is +0.08 (minus 0.43 to +0.52). A 260-point job and a
150-point job come out 0.5 a game apart, the wrong way. The flat 12.1 stands; n=30 caps the slope near +0.2 rather than
proving zero. `Scripts\research\job_slope.py`, `job_slope_results.md`, `job_slope_absences.csv`.

## 3. THE PAYLOAD AUDIT (Matt's point 9)

`Scripts\research\payload_audit.md` and `payload_keys.csv`: 103 key paths in the 30 Sept 21:46 raw pull, each marked read
or unread by the pull, the wire and the sheet. Read: id, name, position, team, injury status, ownership (owned, +/-,
started), the four stat rows the pull asks for, waiver status and clear time. Unread and possibly material, in the order
I would wire them: (1) `outlooksByWeek` for this week, 312 men, about 550 characters each, ESPN's own news blurb, with
`lastNewsDate` beside it: the wire's news column could carry it the day it lands; (2) `droppable`, false on 16 men
(Gibbs, Chase, Allen, Jackson, Robinson, and others): the drop ladder should never offer one; (3) `injured`, true on
exactly the 66 OUT or INJURY_RESERVE men: the IR-eligible set, read off ESPN rather than inferred; (4) `rankings`, expert
ranks by source with an average, 571 men, keys unlabelled, worth one look against the crowd table; (5)
`positionAgainstOpponent.positionalRatings`, every position against every opponent with an average and a rank, this
season (window not stated), where the wire uses last season's `pos_allowed_2025.csv`; (6) `stats[].appliedAverage` and
stat 210, the games a projection covers: 14 on backs and receivers, **17 on every D/ST row** (Seahawks 101.7 total, 5.98
a game by ESPN, 7.26 by our divisor). The 24 to 30 Sept pair reads as a burn-off for D/ST too (new plus week 3 over old,
median 0.97), so the divisor may be right and ESPN's average wrong; the clean test is the 7 Sept pull. Weekly projected
points: not in the payload, never requested (the pull lists stat sets 002026, 102026, 002025, 102025); whether ESPN serves
them under another id is untested. The blurb and the undroppable flag are the two I would wire first; both are a
column each on the wire.

## 4. RUNNING THE BATTLESHIP (Matt's points 4, 6, 7, 8, 10)

**On turning it around.** The decision you are describing is a posture, and the number that sets it is one no file held
until tonight: where you stand in points for, not in record. Three weeks in, a 2-1 team with the sixth-best points total
is a playoff team on form and should buy floor; a 2-1 team with the ninth-best total is not and should buy variance. From
the next run the sheet prints both. Until then, one measured fact cuts against your estimate: on ESPN's rest-of-season
projection (the 30 Sept 07:30 pull, 14 games left), the best nine on each roster in the league averages 119.0 a week at
the top and 103.4 at the bottom, and yours is THIRD of twelve at 116.5 (behind 119.0 and 117.2; `LEAGUE_ROSTERS.csv`
against the pull, every rostered man counted, Nacua at his full projection). You are 8 of 12 in priority, which is 5th of
12 in standings since the order is inverse standings. Points scored so far are the half I cannot see yet. Variance is bought on the wire in exactly two ways that have
measured: a screened young receiver (27% to 44% to startable, three of three) and an open job at 12.1 a game while it is
open. Both are on the sheet. What does not buy it: a bench back behind a healthy starter (your own record, 4.19), and a
third claim that costs a starter (tonight's Raymond for Dobbins). So the posture rule I would run: one upside ticket held
at all times on the bench (Bell is the current one, at 4% rostered he is a free agent on Friday if nobody claims him
tonight), the seat behind your own backs filled, and the bye cover claimed the week before, never earlier.

**On spot-checking the way you do (point 6).** The crowd table is that, mechanically, on Wednesday: every man the
consensus is adding, with our answer. Point 6's second half, "take a player that does not match the model and examine his
attributes", is the batch I will run at every week close from now: the crowd rows we price under the consensus, one line
each on which attribute the page cannot see. Tonight's: Jaylen Wright (the chart holder, a stash behind Gordon the seat
lane cannot see because the chart has him first), Mariota and Cousins and Brissett (quarterbacks, worth nothing beside
Hurts), Waller and Hollins (below the bar on the blend; the crowd is adding week-4 matchups, which this page does not
price for receivers and tight ends: that is the gap, and it is the weekly projection the payload does not carry).

**On rookie pedigree (point 7).** It is measurable and it is measured: NFL round is the one receiver signal that has ever
held here (4.28, 4.30, 4.43). What is not on file is the finer grain the industry uses: draft pick number, college
production (yards per team attempt, breakout age), combine testing. Inputs, named: nflverse publishes a combine file
(free, no key, same release channel as the weekly cache) and the draft picks file we hold has the pick number; college
receiving yards per game and team attempts come from the collegefootballdata API (free key, rate-limited). NOT YET RUN;
the testable form is 4.43's population with pick number and the two college columns added, outcome unchanged. "The cards"
section is hand-written (`cards_2026.csv`, six men, two of them no longer free), rebuilt by nobody, and it sits below
the bar tables; I will move it under the bet lane and have the wire mark a card whose man is gone, but I would not
promote hand-written cards above measured rows.

**On claiming a week ahead (point 8).** Measured in scope, 4.31 and doc 258: a claim for a bye fill a week early bets on
a depth chart, which is the week-1 kind of bet and the worst kind (9.4% become season assets); a claim for a defense's
matchup weeks ahead bets on the schedule, fixed since May, and is sound. The calendar's "claim in the week on the left,
not earlier" is the first case. What is not measured is whether the man you want is still there a week later (the
legibility test in 4.31's open list); NOT YET RUN, and it is a one-evening script on the waiver reports.

**If I were running it, the three things I would build next, in order:** the posture line (points for against the
league, on the sheet from the next run: done tonight); a weekly matchup term for receivers and tight ends, which is the
one thing the crowd prices and this page does not (the inputs exist: ESPN's position-against-opponent block in the
payload, and the pregame line we already pull); and the decision diff, so nothing on THE CALL can vanish unseen again.

## 5. OPEN, BY NAME

- **Matt's:** the two claims tonight and `py claim_order_log.py`; Thursday's pair; Sunday: Nacua off the IR slot if he is
  active (the sheet names the drop); the routes purchase; the D/ST box score; the Opus chat and the podcast transcripts
  (not tonight, his words).
- **Mine, tomorrow:** directive v9.38 (two findings, the gate amendment, the crowd line); the first standings line on the
  07:30 run; the D/ST divisor test on the 7 Sept pull; the news blurb and `droppable` onto the wire; the decision diff.
- **Mine, on events:** the +/- cadence; the week-6 re-fit; the 6 Oct run; status pairs from 20 Oct; 4.34 from week 10.
