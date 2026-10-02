# 453. THE YOUNG-RECEIVER SCREEN READ ON THIS SEASON, AND THE ROOKIE IT COULD NOT SEE

*30 Sept 2026, 00:20 ET. Claude (Cowork). Matt, 29 Sept, pushing back on doc 451's Chris Bell take with
`Chris Bell Fantasy Football Outlook.md`: "We are not going to get diamonds on the waiver wire, instead we have to find those
nuggets to mine that could come in all shapes and sizes. The fact he's young and talented and broke out his first game at
the NFL level with a suspect QB speaks volumes. This is what I've been calling upside, and this player didn't even make the
week sheet." 453 reserved by listing `Source\` (452 is the v9.36 apply). No em dashes.*

---

## 0. WHAT TO DO

1. **Claim Chris Bell third on Wednesday night, behind Gordon and Mayer, and drop Devaughn Vele for him** (a waiver add, no
   keeper cost, 2.1 on the sheet). It is a near tie with Tyler Allgeier on the arithmetic (about +2.5 against +2.3 net of the
   third drop) and it breaks toward the wider bet: a receiver who hits is startable for the rest of the season, a seat pays for
   about three weeks. The take contract's five lines are in section 2. If you would rather hold Vele, the third claim is
   Allgeier for the same drop; nothing else on the list clears a third drop.
2. **You were right about the sheet and half right about the player, and both halves are measured now (finding 4.43).** The
   young-receiver screen (rounds 1 to 3, yards per target, targets a game) had only ever been read on a full prior season, so a
   rookie could not be screened at all. Read on weeks 1 to 3 it works: three of three became startable 43.6% of the time over
   weeks 4 to 14 against 0 to 20% below (n=174, 2021 to 2025); the men still under the bar at week 3, which is the wire, 26.7%
   against 5.6%. Bell clears all three (round 3, 9.2 a target, 3.3 targets a game). That is a real ticket, and the sheet had no
   way to see it. The other half: "broke out his first game" is the level, not a separate signal. A breakout last game is worth
   +51 points at week 3 among rookies, and nothing past week 3 once the marks are read (+5.6 and +9.0 points, p 0.45 and 0.36).
3. **The sheet carries him now, with the caveat the arithmetic owed you.** The wire screens any year-1-to-3 receiver on his own
   games (`in-season screen 3 of 3`, with his round, yards a target, targets a game and games printed beside it), the bet lane
   prices it at 27%, and four free men clear it tonight: Tre' Harris, Antonio Williams, Ted Hurst III and Bell. Bell's row prints
   "out of reach, needs 38% of the passing game": on Miami's 28 targets a game the average hit (12.7 a game) needs 10.9 targets
   a game, a hair over the 37.8% ceiling anyone has held; the bar itself needs about 30%. That is your "suspect QB" as a number.
4. **The inherit file names the absent starter as the holder** (Achane, not the chart's stand-in Wright), reads his tag from the
   live roster and the injuries feed rather than the week-old pull, and the seat list now cuts the Miami row by name: "De'Von
   Achane is already out, so this is not a seat." The item on my list is closed.
5. **Paste directive v9.37** (one index row for 4.43); it replaces v9.36, which you have not pasted yet, so paste v9.37 instead.
   Nothing else to run: the 07:30 run rebuilds the form file with the new columns and the pages on them.

---

## 1. THE CLAIM IN TESTABLE FORM, AND WHAT CAME BACK

**The form, stated before the run:** among receivers in NFL years 1 to 3 (drafted 2021 or later) not startable the season
before (under 9.62 a game, this league's replacement) or with no season before, read at the end of week W on weeks 1 to W
alone: rounds 1 to 3, yards per target over 7.13 on 5+ targets, targets a game over 3.20, and a breakout last game (60+ yards
or 7+ targets); outcome startable (9.62+) over weeks W+1 to 14 on 4+ games. 4.30 (doc 248) measured the three marks on a full
prior season predicting the next; this is the same three marks on three weeks predicting eleven, which is what the sheet would
be applying them to for a rookie. `Scripts\research\wk1\rookie_screen.py`, `run_rookie_screen.txt`; nflverse weekly 2021 to
2025 and `nfl_draft_picks.csv`.

| read at week 3, n=174, base 16.7% | startable weeks 4 to 14 |
|---|---|
| 0 / 1 / 2 / 3 of 3 marks | 0.0% (35) / 3.9% (51) / 20.4% (49) / **43.6% (17 of 39)**, p=0.0000 |
| rookies 3 of 3 / rookies below 3 | 57.9% (11 of 19) / 9.1% (6 of 66) |
| 3 of 3 and still under the bar through week 3 (the wire) / below 3 and under | **26.7% (4 of 15)** / 5.6% (7 of 124) |
| breakout last game / not | 40.0% (50) / 7.3% (124); rookies rounds 1 to 3: 59.1% against 8.1%, p=0.0000 |
| the same breakout cut at weeks 4 and 5 | +5.6 and +9.0 points, p=0.45 and 0.36; 3 of 3 with it 36.4%, without 35.0% |
| Bell's own shape: 3 of 3 and under 6.0 a game / under 4.0 targets a game | 0 of 4 / 0 of 2 (Alec Pierce 2022, Xavier Worthy 2024) |

The shape holds at weeks 4, 5 and 6 (3 of 3: 35.7, 36.6, 41.2%). The rookies who cleared at week 3 and hit: Chase, Dell,
Olave, Tetairoa McMillan, Egbuka, Flowers, Addison, Rice, Reed, Brian Thomas, Nabers; who cleared and missed: London, Rondale
Moore, Pierce, Burks, Harrison, Legette, Odunze, Worthy. Most of the hits were already near the bar at week 3; Bell is at 3.9.
The cell he sits in is empty of hits and too small to say more than that.

## 2. THE TAKE: CHRIS BELL, WR, MIAMI, THIRD CLAIM

- **Vintage.** 2026, 3 games: 10 targets, 5 catches, 92 yards, 11.7 points; week 3 with Douglas out, 7 targets, 4 for 67, 71% of
  the snaps, a third of Miami's air yards. Round 3, pick 94, Louisville; a November 2025 ACL, active from week 1.
- **Population.** 26.7% is the under-the-bar three-of-three cell (n=15, a screen, not his forecast); 4.6 expected on the sheet's
  hit size, or nothing if the reach gate is read strictly (38% of Miami's throws needed against a 37.8% ceiling). Harris, Hurst
  and Williams print the same 27%, so it is a base rate.
- **The men ahead of him for targets.** Malik Washington, 27.1% of Miami's targets over three games; Caleb Douglas, 26% and 13%
  in his two games, questionable (ankle) for week 4; Greg Dulcich at tight end, 7 targets in week 3.
- **The standing rule and the roster after.** Section 6: bench priority is RB to the cap, then WR; you hold five active backs
  and this is the WR seat. From round 9 and on the wire, break a near tie toward the wider bet (4.13): 17.4 if it fires against a
  seat's 7.4. After Gordon for Malik Washington, Mayer for Perine and Bell for Vele: RB Jeanty, Judkins, Dobbins, Washington Jr.,
  Gordon (Coleman, Dowdle parked); WR Adams, Pickens, Tucker, Bell (Nacua parked); TE LaPorta, Mayer; QB Hurts; two defenses, one
  kicker. Fifteen, every cap met, the second tight end for the week 6 hole and no longer.
- **The counterfactual.** Vele's 2.1: 10.2 a game this season over three games, 8.3 on the blend, never in your nine, and the
  receiver who would fill a bye. Allgeier's seat at the same drop is 4.4 expected on a 62% chance Love's job opens for three weeks.
  If you take neither, the third drop stays in your pocket and the choice is a coin flip on the arithmetic; the wider bet is the
  tiebreak, not a measured edge.

## 3. WHAT CHANGED IN THE BUILDERS

`build_form.py` writes `rec_yds`, `rec` and `games` on every row. `wire.py` `inseason_screen()` labels a WR in NFL years 1 to
3 with no preseason screen when this season's marks clear on 2+ games and 5+ targets, and the potential lane prints his numbers;
`load_pedigree_all()` supplies the round and year the preseason loader dropped. `sheet_engine.py`'s bet lane knows the label and
prints the population sentence. `sheet_constants.json` carries `potential.in_season.inseason_3of3` (0.267, n=15, with the week-4
and all-3-of-3 cells and the re-fit rule). `build_inherit.py`: in the stand-in case the absent starter is the holder with his
projection, and every holder's tag is read from `LEAGUE_ROSTERS.csv`, the wire and `news_2026.csv` before the pull. Guards:
check_pages (C6 clean), check_plain, check_page_logic (P3), check_vintage, check_page_rules, check_inputs, check_locals all quiet
on the rendered pages; four unit controls on the screen (year 5, round 4, four targets, a form file without the columns all
blank). Every changed script re-pinned; `rookie_screen.py` pinned from birth.

## 4. THE OUTSIDE READ, DATED

`Chris Bell Fantasy Football Outlook.md` is a generated research report (29 Sept, citing SI, NBC Sports, FantasyPros, RotoBaller,
PFF and the Dolphins' site). Its load-bearing facts check against our files: round 3 pick 94 (`nfl_draft_picks.csv`), 4 of 7 for
67 (the form file), Douglas out in week 3 and questionable now (`news_2026.csv`), Achane on injured reserve. Two of its
sentences do not: Slowik never coached Willis in Green Bay, and it lists Braelon Allen as both a Jet and a Dolphins backup. Its
verdict, a stash rather than a start, is the same as this doc's; its route participation figure (69%) is a feed this project
does not hold (4.40).

## 5. OPEN, BY NAME

- **Matt's:** the v9.37 paste; the three claims Wednesday night; the claim-order runs; the routes purchase; the D/ST box score;
  the Opus chat (blocked).
- **Mine, waiting on events:** the 07:30 run (projections 0, the form file with the new columns, the bet lane with four
  in-season rows); the re-fit of the in-season cell at week 6; the Tuesday 6 October run; the status pairs from about 20
  October; the 4.34 column from week 10; wiring item 7 (low).
