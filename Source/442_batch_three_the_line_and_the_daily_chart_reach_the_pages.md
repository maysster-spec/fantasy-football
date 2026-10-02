# 442. BATCH THREE, FIRST HALF: THE PREGAME LINE AND THE DAILY CHART REACH THE WIRE, THE SEAT LANE REBUILDS EVERY RUN, AND THE SPOT CARD FOUND A JOIN MISS ON ITS FIRST USE

*29 Sept 2026, afternoon. Claude (Cowork), batch three of "complete the to do list... in batches to ensure fidelity" (docs 440 and
441 were batches one and two). 442 reserved by listing `Source\` at 14:20 ET. No em dashes.*

---

## 0. WHAT TO DO

1. **The wire page now picks defenses on the pregame line.** The defense run and the weeks-ahead section use the opponent's
   implied total (nflverse `games.csv`, free, rebuilt every `ff.bat` run into `Source\lines_2026.csv`) wherever a line
   exists, and last season's averages only where it does not. The rule sentence on the page: take the free defense facing the
   lowest opponent implied total this week; over five seasons that is worth about three points a week over picking at random.
   This week's top run moved from IND (20.3 last season) to CLE (facing PIT at 20.5 on the line). **Your standing rule "check
   ESPN's weekly D/ST projections" is retired from your list; the page has the number now.**
2. **Quarterbacks in the weeks-ahead section carry the own-team total beside the soft-matchup rule.** Where they disagree, take
   the total (it beats random by more; the two agree about half the time).
3. **The seat lane reads today's depth chart.** `wire.py` takes the order from `depth_daily.csv` (job worth still from the
   projections), attaches the practice report to every back, and `inherit_2026.csv` is rebuilt every run instead of sitting on
   the 16 September file. Today's rebuild changes the holder on MIA, GB and SEA and the next man on ten teams (DET Vaki, IND
   McGowan, KC Emmett Johnson, DAL Goodson, CLE Sanders, NYG Najee Harris, CAR Dillon, MIN DeeJay Dallas, GB Lloyd, SEA Wilson).
   **One rule decision is open and priced below (§3): a seat whose starter is already out is priced at the stand-in's job.**
4. **`py spot.py "Name"` prints every number the pages used for a man and every number held that no page prints.** Its first
   run found a live miss: ESPN spells him Joshua Palmer and nflverse Josh Palmer, so his wire row printed every workload column
   blank. The form join now accepts a first-name variant on the same team and position when it is the only candidate; he was
   the only miss on the wire (3.1% owned, no pick moved).
5. **The claim-order pairing exists.** `py claim_order_log.py --pair` joins your logged claim order to the executed and failed
   results and appends `Source\claim_order_outcomes.csv`. It needs two runs a week from you (on your list): Wednesday night
   after placing claims, and Thursday morning after `waivers.py --live`. Proved on your five real week-2 claims.
6. **`check_inputs.py` passes.** `redzone_te_2025.csv` is a documented display-only exception (doc 441) that is still checked:
   it must be read somewhere and the engine must not touch it.
7. Nothing to run. The next `ff.bat` builds the lines and the inherit file and its RESULT line gains `lines` and `inherit`.

---

## 1. THE LINE ON THE WIRE (finding 4.39 wired)

`build_lines.py` (in `Scripts\research\wk1\`, `ff.bat` after the depth chart) fetches nflverse's schedule file the way
`build_form.py` fetches, writes week, gameday, home, away, spread_line, total_line, implied_home, implied_away, has_line,
as_of, teams through `sheet_engine.TEAM_ALIAS`, unlined games blank rather than zero, and refuses to overwrite a file whose
current week had lines with one whose does not. Today: 272 games, all 16 week-4 games lined, week 5 five of fifteen.

`wire.py`: `load_lines()` keys both sides of every lined game; `dst_runs()` uses the opponent's implied total for each
week that has one and last season's points scored otherwise, and each row says how many of its weeks are on the line;
`look_ahead()` switches a week to the line axis only when every game that week has one (QB by highest own total, D/ST by
lowest opponent total), otherwise last season as before; the page prints the total beside every opponent, the rule
sentence at the top of the defense section, the read time of the lines, and in red that the lines are missing when the
file is absent (the run and look-ahead then reproduce the old order exactly; no zero prints). `main()` passes the lines
to both. Tested on the real schedule, real free pool from `WIRE_20260929.csv` and a real lines fetch; the negative control
(file removed) reproduces the before-state to the row.

## 2. THE SEAT LANE ON THE DAILY CHART (doc 441 §5 wired)

`wire.py` `load_depth()`: `depth_map.csv` stays the source of job worth and job label (they come from the projections;
the chart has none); the order comes from `depth_daily.csv` joined on ESPN id. Four cases: on both, today's depth; on
today's chart only, a new row with the team's job constants and a flag; in August only, kept below the chart (depth 50+)
and flagged "not on today's chart"; a man who changed teams (Kaleb Johnson to GB, Demercado to DAL, DeeJay Dallas to MIN)
moves with the new team's job. The practice report attaches to every row as report status, practice status and injury;
nothing acts on it yet. `usage_depth()` is unchanged: realised usage still overrides the chart from week 3, the chart is
the tiebreak, the order for men with no usage line, and the freshness source. Without the daily file the output is
identical to today's and the page says the lane is on the August chart. The chart is 3+ days old: a warning.

`build_inherit.py`: reads the daily chart's RB order when present (the August scrape otherwise), joins the pull and the
wire on ESPN id, reads the unranked-free file so a free next man prints as free, and writes the same schema plus
`chart_as_of`. Runs in `ff.bat` after the lines. Rebuilt today on every real input.

## 3. THE OPEN RULE DECISION, PRICED

The chart demotes an injured starter, so on MIA the holder is Jaylen Wright (job 24.0) and the next man Ollie Gordon;
Achane (260.3) sits at RB3 until he plays. On GB, Kaleb Johnson (28.9) over Jacobs (155.1). The seat lane therefore prices
those two seats at the stand-in's job this week, which is what a claim this week actually inherits, and doc 411 already
cuts a seat whose starter is out. When the starter returns the chart flips back and the seat re-prices. **Recommendation:
leave it; the alternative (price at the absent starter's job) would advertise a 260-point seat behind a man who is not
playing.** Noted as a rule line, not changed.

## 4. THE SPOT CARD, THE JOIN, THE PAIRING, THE INPUTS CHECK

`spot.py`: resolves the name with the engine's own rule (exact, then a first-name prefix on the same team and position,
then surname; two candidates stop it), prints roster and status, the newest wire row with every column, every form row,
the depth chart around him, the practice line, the inherit row, pedigree, the newest projection, snaps and news, names
every missing file, and closes with the columns held for him that neither page prints (decided by grepping the two page
builders for the column names as string literals, stated on the card as a floor). Pinned in `check_kit.py`.

The join fix: `_form_variant()` in `wire.py`, same team, same position, same surname, one first name a prefix of the
other, exactly one candidate. Joshua Palmer to Josh Palmer (5 targets, not blank). A second candidate stays blank.

`claim_order_log.py --pair`: per week the last logged order, one row per claim, matched to `waiver_report_2026.csv` on
team, week (or week plus one), type WAIVER and the added player's id; outcome executed, outbid (yours failed as invalid
source and another team executed on him), failed with the reason, or canceled; contested if any rival claim reached the
run; winner and rival count; appended without duplicates to `Source\claim_order_outcomes.csv`; a claim with no result row
is printed and held. The log has no entries this season, so the join is proved on a synthetic log of your five real week-2
claims: Vele executed; 49ers D/ST outbid (two rivals); Chris Brooks and CHI D/ST failed as already dropped; Chiefs D/ST
contested and won. This is the input §2's "BLOCKED" line on claim order named; it starts filling Wednesday.

`check_inputs.py`: `DISPLAY_ONLY` carries `redzone_te_2025.csv` with doc 441 as the reason; the exemption is checked
(still read somewhere; the engine must not touch it) and has a selftest.

## 5. OPEN, BY NAME

- **Batch three, second half (the engine):** the blend beside the measured rate on the lineup page; `inherit_2026.csv`'s
  unread columns (at_risk, starter_g25, best_2wk_2025); the engine's form join to name + position + team; xfp, fp_oe, act2
  and xfp2 as printed columns; the QB look-ahead onto the week sheet; the snap file as a freshness source; the four live
  findings with no page term (4.13d, 4.25b, 4.26, 4.34); the check_pages display rule; the pocket sheet builder.
- **Batch four:** the directive diet diff; a v9.35 only if a rule changes.
- **NOT YET RUN:** whether the practice report's Out should be `next_man_up()`'s step-past trigger beside ESPN's status;
  whether a cumulative-usage leader who is Out should still rank depth 1; the eight-week horizon on 4.38.
- **Matt's:** the two claim-order runs each week (on the list); the routes purchase; the ESPN D/ST box score.
