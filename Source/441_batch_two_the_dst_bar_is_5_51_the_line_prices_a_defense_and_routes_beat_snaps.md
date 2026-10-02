# 441. BATCH TWO OF THE TO-DO LIST: THE D/ST BAR IS 5.51, THE PREGAME LINE PRICES A DEFENSE AT +3 A WEEK, ROUTES BEAT SNAPS ON HISTORY, RED ZONE IS INSIDE EXPECTED POINTS, AND THE SEAT LANE HAS A DAILY CHART

*29 Sept 2026. Claude (Cowork), batch two of "complete the to do list... in batches to ensure fidelity" (doc 440 was batch one).
441 reserved by listing `Source\` at 13:40 ET. No em dashes.*

---

## 0. WHAT TO DO

1. **The D/ST replacement is 5.51 a week, not 5.99, and it is live.** `build_dst.py` is fixed (every team-week is a row; blocked
   kicks +2 and fumbles lost minus 2 added), `dst_weekly_2021_2025.csv` is rebuilt (2,718 rows, the 2,576 old rows byte-identical
   on every old column), and `sheet_constants.json` and `dst_k_supply.py` carry 5.51. An empty D/ST slot is now charged 5.51, and
   every D/ST drop cost rises by 0.48 against the other positions. Do not quote 5.99, or "5.46 sd 6.28": a D/ST week is 4.99,
   sd 6.59. The DO-NOT-QUOTE row lands at v9.34.
2. **A defense IS worth its matchup, and the number is about +3 a week: pick the streamable D/ST facing the LOWEST opponent
   implied total** (from the pregame line, free, Wednesday). 7.79 a week against 4.62 at random (t 4.4), the same as picking
   on the opponent's season-to-date scoring (+3.40), which needs two prior weeks. The page prints neither today; wiring the
   implied total into the D/ST lane is batch three's first item. Your standing rule "check ESPN's weekly D/ST projections"
   stays until then.
3. **At quarterback the own-team implied total clears random (+4.5, t 5.1) and does not robustly beat doc 427's softest-matchup
   rule** (+2.8 under one tier definition, minus 0.3 under the other). It goes beside the rule as a second read, not in place
   of it. At kicker nothing works (+0.3 to +0.8, under two se).
4. **Route participation beats snap share on history and buys nothing today.** On 2023 to 2025 (n=4,596 claimable WR/TE weeks)
   dropback participation predicts the next four weeks better than snap share and absorbs it (route +0.09 a point, snap minus
   0.02); as a fourth signal on the screen it adds +1.9 points, under the bar. The free file lands after the season. **A paid
   live feed is your call (money): the one use it would serve is the 40 to 80% snap band, where the route-minus-snap tilt moves
   startable-next-four by 5 to 17 points. I recommend not buying until that use is on a page.**
5. **Red zone is inside expected points.** Net of the two-game expected and snap share, red-zone share adds 0.000 per 10 points
   of share; end-zone targets are NEGATIVE (minus 0.39 a target). No builder ships; the ffverse model already prices field
   position. `redzone_te_2025.csv` leaves the inputs list in batch three.
6. **The seat lane gets a daily chart.** `build_depth_daily.py` writes `Source\depth_daily.csv` (ESPN's depth chart as nflverse
   carries it, newest snapshot per team, today's is 06:02 ET) and `Source\practice_2026.csv` (the newest injury report with
   practice status); `ff.bat` runs it after the snap counts. Against the 8 August chart the lane was built on: 12 backfields are
   stale at RB1 or RB2 (RB1: GB Jacobs to Kaleb Johnson, MIA Achane to Jaylen Wright, SEA Charbonnet to Jadarian Price), 12
   receiver rooms, 5 tight-end rooms. Wiring the new file into `wire.py`'s `load_depth()` and `build_inherit.py` is batch three.
7. **Your list gains one decision line** (the routes purchase) and keeps the box-score check from doc 440. Nothing to run: the
   next `ff.bat` builds the depth files and its RESULT line gains `depth`.

---

## 1. THE D/ST BAR (ledger 202 closes)

`build_dst.py` iterated the events it had counted and wrote a row per team-week that had one; a week whose score was the
points-allowed band alone was absent (24 / 28 / 23 / 38 / 29 by season, mean minus 3.88). Fixed: it iterates the games,
looks events up, writes 2,718 rows sorted season, week, team, refuses a game with no final score or a duplicate team-week,
and adds `blk` (field goal, extra point or punt blocked, +2 to the blocking side; 195 in five seasons, +0.143 a week) and
`fuml` (a fumble lost by the return or defensive side; 171, minus 0.126 a week). Proofs, `run_build_dst_check.txt`: all
2,576 old rows found with every old column identical and old `dst_pts` equal to new minus 2·blk plus 2·fuml on every row;
544 / 542 / 544 / 544 / 544 rows by season; identical to the price script's file on every shared column.

| number | published (doc 265) | all 2,718 rows, no new terms | with blocked kicks | with blocked kicks and fumbles lost (SHIPPED) |
|---|---|---|---|---|
| D/ST12, weeks 1 to 14, five-season mean | 5.99 | 5.57 | 5.75 | **5.51** (5.62 / 5.08 / 6.62 / 5.15 / 5.08) |
| a D/ST week, mean (sd) | 5.46 (6.28), n=2,576 | 4.97 (6.51) | 5.12 (6.56) | **4.99 (6.59)** |
| D/ST1 to D/ST3 | | 10.02 / 8.94 / 8.03 | | 10.08 / 9.12 / 8.14 |
| supply, units above the bar, early / late | 13.5 / 13.6 | | | 13.6 / 13.4, still flat |

Rank-by-total and rank-by-mean agree on the full file because every unit has 13 games in weeks 1 to 14; they differed on the
old file only because the dropped rows made the game counts unequal. **The fumble term is carried because section 2 scores
it; whether ESPN charges the D/ST slot for a return fumble lost is NOT ESTABLISHED and one league box score settles it (on
Matt's list since doc 440). If ESPN does not, the bar is 5.75.**

## 2. THE LINE (finding 4.39)

Testable form, stated first: among streamable units (ranks 13 to 32 by season-to-date average, 2+ prior games), does the
unit facing the lowest opponent implied total score more than the unit facing the lowest opponent season-to-date scoring, and
more than random; same at QB against doc 427's rule, same at kicker. The falsifier as first written (+1.0 over random with
se under 0.5) was unattainable at 75 season-weeks, since a pick's own spread over the square root of n is 0.72 at D/ST; the
reading that stands is a gain of 1.0 or more at two se, and +0.5 to replace a season rule.

| lane, pick rule | mean a week | over random | se | t |
|---|---|---|---|---|
| D/ST, lowest opponent implied total | 7.79 | +3.16 | 0.72 | 4.4 |
| D/ST, lowest opponent season-to-date points scored | 8.02 | +3.40 | 0.81 | 4.2 |
| D/ST, most-favoured defense | 7.65 | +3.02 | 0.69 | 4.4 |
| D/ST, random (pool) | 4.62 | | | |
| QB, highest own implied total | 22.00 | +4.53 | 0.89 | 5.1 |
| QB, doc 427 softest matchup, prior weeks | 19.17 | +1.70 | 1.08 | 1.6 |
| QB, random (pool) | 17.47 | | | |
| K, highest own implied total | 8.12 | +0.32 | 0.41 | 0.8 |
| K, opponent season-to-date K points allowed | 8.65 | +0.84 | 0.50 | 1.7 |

Line minus season rule: D/ST minus 0.23 (se 1.10), QB +2.84 (se 1.41) under the streamable-by-prior-weeks tier and minus
0.33 (se 1.22) under doc 435's full-season tier. The D/ST rule is wired because the page has no opponent term at all today
and the line needs no prior weeks; the QB rule stands and the line joins it as a second read.

## 3. ROUTES (finding 4.40)

Route participation here is dropback participation from the free nflverse participation files (2023 to 2025, 100% of
dropbacks join), which lag a season. Rank correlation with the next four weeks: route .531 against snap .487, every season
and both positions; in a regression together route takes everything (+0.091, se .005; snap minus 0.020). Route-only top
fifth against snap-only: startable next four 34.2% against 27.4% (n=190 and 193). One sd of the route-minus-snap tilt is
worth +0.52 a week at WR and +1.15 at TE net of snap share. Targets per route run alone is noise. As a fourth signal on the
2-of-3 bar: +1.0 spike, +1.9 startable next four, under the bar; swapping it for the snap signal changes nothing.

## 4. RED ZONE (finding 4.41)

Net of the two-game expected points and snap share, position held: red-zone share +0.000 per 10 points of share (t 0.0);
end-zone targets minus 0.39 per target (se .07). Inside the expected-points top fifth the pooled red-zone cell is +7.0 points
of startable-next-four, which is position composition; cut within position it is +3.7 (se 2.2, p=0.18), TE minus 1.0. End-zone
targets inside the same fifth minus 5.7 (p=0.015). Display only; no 2026 builder.

## 5. THE DAILY CHART

`build_depth_daily.py` (run from `Scripts\research\wk1\`, `--probe` for an offline test) fetches nflverse's daily depth
charts (ESPN's, one snapshot per team per day since March, 578,918 rows; `pos_rank` is the depth within position; WR has
three starting slots) and the injuries file, and writes `depth_daily.csv` (573 rows: team, pos, depth, player, name_key,
gsis_id, espn_id, as_of; QB 92, RB 120, WR 217, TE 144) and `practice_2026.csv` (301 rows: the newest week's report with
report and practice status). `name_key` is imported from `build_form.py` and asserted equal on every name; teams through
`sheet_engine.TEAM_ALIAS`. Joins to `form_2026.csv` on name, position and team: 191 of 192 depth-1 and depth-2 skill men
(the miss has no 2026 stat line). Guards: 32 teams, a QB1 / RB1 / WR1 / TE1 on every team, contiguous ranks, a chart older
than three days warns. One caveat for the wiring: the chart demotes an injured starter (Achane, Jacobs), so RB1 today is
the man playing, not the job holder; `inherit_2026.csv`'s holds-the-job semantics need the practice file beside it.
`depth_diff.py` (read-only) prints where the 8 August chart disagrees: RB1 3 teams, RB2 11, WR3 12, TE1 5.

## 6. OPEN, BY NAME

- **Batch three, mine, in this order:** the opponent implied total into the D/ST lane and beside the QB rule (`games.csv`
  is free and daily); `depth_daily.csv` and `practice_2026.csv` into `wire.py` `load_depth()` and `build_inherit.py` (join on
  espn_id); `redzone_te_2025.csv` out of `check_inputs.py`'s list with this doc as the reason; then the page and engine items
  already listed (xfp columns, the blend beside the measured rate, inherit columns, the form join, the QB look-ahead, the
  check_pages display rule, the claim-order pairing, the spot-check card, the pocket sheet, the four live findings with no
  page term).
- **Batch four:** the directive diet diff and v9.34 (index rows 4.38 to 4.41, 4.18 to "both", the D/ST retraction row).
- **NOT YET RUN:** the rise on an eight-week horizon (4.38); charted routes against dropback participation (4.40, needs a
  paid file).
- **Matt's:** the ESPN D/ST box score (doc 440 item 8); the routes purchase decision.
