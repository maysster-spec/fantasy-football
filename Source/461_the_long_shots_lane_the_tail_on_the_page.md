# 461. THE LONG-SHOT LANE: THE TAIL ON THE PAGE, AND A HARNESS THAT READ THE CLOCK

*1 Oct 2026, 08:15 ET. Claude (Cowork). Doc 460's section 4 built, in the same turn. 461 reserved by listing `Source\`.
No em dashes.*

---

## 0. WHAT TO DO

1. **Run `.\ff.bat` when you are next at the machine** so the live week sheet carries the new lane; until then the lane
   exists only on the harness build here. Nothing else to run.
2. **Read the lane as a shape's rate, never a man's forecast.** "The long shots, ranked by the odds of a BIG hit" sits
   above the seat list while you are outside the top six in points for, and below it otherwise. Every free back and
   receiver under the bar is placed in the cell his own team's usage puts him in (lead back under the bar, committee
   partner, handcuff by the job's rank, young receiver with the three marks), and the row prints the cell's share of men
   who went on to six or more startable weeks of the next ten, a four-week stretch at 15 a game, and four or more
   startable weeks. A tilde marks a cell measured on under twenty men. At most three men of one shape, best first.
3. **What the lane does not list, on purpose:** third-string backs (0 of 249 on both big-hit columns; the wire's relief
   lane buys that man AFTER the game that shows it, which is finding 4.27's trigger) and receivers without the three
   marks (under 2% on both). They are in the folded "Left off" list with the reason.
4. **The mutation harness now ignores the clock.** Two clean builds a minute apart differ in the title, the masthead and
   the inputs box's file ages ("4 minutes old" against "just now"), and on 1 Oct that read as two parked-man mutations
   SURVIVING when they had no effect. The byte comparison strips all three now; the run reads 1 caught, 3 survived (the
   divisor, weekly positions on a season rate, the own-position drop), 6 no effect on today's roster.

---

## 1. WHAT CHANGED

`sheet_engine.py`: `rb_usage()` carries points a game; `wr_usage()` (targets and points a game off the form file's
week-0 row); `pf_rank()` (his rank by points for off the standings file); `tail_shape()` (the cell, with the same cut
points as `tail_tickets.py`); `longshot_lane()` (the table, the lede that says why it leads or follows, the note, the
folded left-off list); `render()` takes `wr_use` and `pf`; the nav carries "long shots". `sheet_constants.json`:
`tail_tickets` (the cells, the handcuff-when-the-starter-falls split, the already-startable shares, the population
header). `check_guards.py`: the stamp regex. `check_kit.py`: the three pins and `research\wk1\tail_tickets.py` pinned.

Guards on the rebuilt page: check_plain fired once on a draft of the lane's note ("n=32") and the words were removed;
then clean. check_vintage, check_page_rules, check_page_logic (P1 to P4), check_inputs, check_locals clean. The
missing-row check by name: Wilson, Allgeier, Lloyd and Harris are on the lane; Badie, Miller and Tracy are in the
left-off list with the third-string reason.

## 2. OPEN, BY NAME

- A check_page_logic control for the lane: no third-string back and no already-startable man on it, and the lane above
  the seat list only when the standings file puts him outside the top six. One evening, with doc 457's two controls.
- The lane reads the four-week average; 4.38 says the level of the latest game is the better signal. The row prints both
  numbers so he can see a fall (Allgeier: 10.7 a game, 6 last game). The cells are not re-fit on the latest game.
