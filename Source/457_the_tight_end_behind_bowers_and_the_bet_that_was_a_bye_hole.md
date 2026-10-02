# 457. THE TIGHT END BEHIND BOWERS, AND THE BET THAT WAS A BYE HOLE

*1 Oct 2026, 01:00 ET. Claude (Cowork). Matt, 1 Oct 00:20: "why am i being asked to roster TE Michael Mayer who is
behind Brock Bowers? This must be some kinda mistake." With his three claims attached. 457 reserved by listing
`Source\` (456 is the payload doc). No em dashes.*

---

## 0. WHAT TO DO

1. **Your third claim: Packers D/ST over Bears D/ST, same drop (Chiefs D/ST), if you are still up.** The wire's rule is
   the free defense facing the lowest opponent implied total this week: Packers at Tampa 17.5, Bears against the Jets
   20.0 (the line read 30 Sept 21:16). Green Bay also wins the Chiefs' bye week (week 5: Packers against Chicago 21.5,
   Bears at Green Bay 24.0). Two and a half points of implied total is worth under a point of D/ST a week, so if you are
   asleep it does not matter; if you are not, drag Packers in.
2. **Mayer was a defect and it is fixed: the man ahead.** He cleared the week-1 workload screen honestly, as the Raiders'
   top tight end in weeks 1 and 2 while Bowers was out (7 and 4 targets); Bowers came back in week 3 with 13 targets to
   his 3, and the page never re-read who was ahead. Measured on the screen's own population (section 1): every tight end
   who ever cleared it led his team at the position in week 1 (15 of 15); a second receiver cleared it 22 times and hit 5
   (22.7%) against 25 of 54 (46.3%) for the leaders. The bet lane now reads the newest game's target leader at each
   position: a second tight end gets no rate ("behind Brock Bowers, 13 targets to 3 last game"), a second receiver gets
   22.7%. Mayer is off THE CALL.
3. **And the row that replaced him was the same shape, so that is fixed too: a bet that is mostly a bye hole is a
   calendar claim.** AJ Barner's +11.1 was 43% the week-6 hole (any tight end enters whole when LaPorta is off). The
   calendar two inches below said claim that man in week 5; THE CALL said this week. Now a tight end or quarterback bet
   whose hole weeks carry 40% or more of "if it fires" takes the week before the hole as its claim week, prints "week 5"
   in THE CALL, says so on the pick, and is left out of tonight's total ("Taking both this week nets +32.6"). Waller is
   a fine candidate for that week-5 claim (7.0 a week on the blend, off his bye); the week-5 sheet names the best man then,
   and Coker's return would cut Waller's targets, which the newest-game leader check will see.
4. **Your other two claims match the sheet** (Gordon for Vele; Raymond, for Tucker rather than Dobbins, a WR-for-WR swap
   the page would not pair but which nets more than its own row: 7.4 minus 0.8). Nothing else to run tonight.
5. **The D/ST divisor stands (doc 456's open question).** On the 7 Sept to 30 Sept pair, (new projection plus points
   scored) over the old projection is 0.92 for D/ST, 1.00 for backs, 1.02 for receivers, 0.99 for kickers: a rest-of-
   season total for every position, so dividing by the games left is right and ESPN's own 17-game average on the D/ST
   row is the odd one out. TESTED, no change.

---

## 1. THE MEASUREMENT

**The claim in testable form (Matt: "There is some kinda bug promoting him where he shouldn't be"):** within the week-1
workload screen's own population (doc 308: every WR and TE 2022 to 2025 who played week 1 with a target, was below his
position's replacement the prior season, played 4+ of weeks 2 to 14, n=517), the men who cleared two or three marks
(n=76, 39.5% startable over weeks 2 to 14) split by whether he was the top man at his position on his own team by week-1
targets. `Scripts\research\wk1\te2_split.py` (the screen's own builder, `wk1_wr_composite.py`, with the rank added; it
fetches the nflverse snap counts the screen reads).

| cell | startable weeks 2 to 14 |
|---|---|
| cleared, led his team at the position | 25 of 54, 46.3% |
| cleared, second or lower at the position | 5 of 22, 22.7% |
| tight ends who cleared | 15 of 15 led their team; 8 of 15 hit |
| tight ends who cleared as the second tight end | none in four seasons |

So the 38% is a leader's rate. Mayer's shape (a second tight end behind a healthy leader who out-targets him four to one)
is a cell the screen has never contained; the honest answer is no rate, not 38% and not zero. `workload_second_man` in
`sheet_constants.json` carries the cells; re-fit after the season.

## 2. WHAT CHANGED

`sheet_engine.py`: `pos_leaders()` reads the newest week's target leader at each team and position off the form file;
the workload lane marks a man whose leader is a different man with 6+ targets and twice his (a second tight end: no
rate, a dash; a second receiver: 22.7%, priced); a tight-end or quarterback bet whose hole weeks carry 40% or more of
its "if it fires" takes the week before the hole as its claim week (printed in THE CALL and on the pick, excluded from
the total). `sheet_constants.json`: `potential.in_season.workload_second_man`. Guards quiet on the rebuilt page
(check_plain, check_vintage, check_page_rules, check_page_logic, check_inputs, check_locals). Both re-pinned.

## 3. OPEN, BY NAME

- **Matt's:** the Packers swap if awake; Thursday's pair; Sunday's Nacua move; the week-5 tight end (the calendar names
  him); the routes purchase; the D/ST box score; the Opus chat and the podcast transcripts.
- **Mine, tomorrow:** directive v9.38 (now with 4.46, the man ahead on the workload screen); the first standings line;
  the blurb and `droppable` onto the wire; the decision diff; a check_page_logic control for a second tight end on
  THE CALL.
