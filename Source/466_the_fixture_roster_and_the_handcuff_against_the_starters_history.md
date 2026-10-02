# 466. THE FIXTURE ROSTER, AND THE HANDCUFF AGAINST THE STARTER'S HISTORY

*1 Oct 2026, 11:40 ET. Claude (Cowork). Matt, 11:20: "You have been running open items? If so, what is the status."
The honest answer was no: nothing runs between replies, and the last reply promised otherwise. These two ran in
this turn. 466 reserved by listing `Source\`. No em dashes.*

---

## 0. WHAT TO DO

1. **Nothing to run.** `py check_guards.py --fixture` is the new harness mode; the plain run is unchanged.
2. **The mutation harness can now prove the three mutations it could only shrug at.** On a frozen synthetic
   roster (`Source\fixture\MY_ROSTER.csv`: a priced man in the IR slot, no bench receiver under the bar, a receiver
   carrying a starter's value), the two parked-man mutations and the own-position mutation change the page and
   `check_page_logic.py` catches all three (P1, P2, P5). On the live roster they stay NO EFFECT, which is the right
   reading of a roster where the cheapest men are bench receivers either way.
3. **Said plainly, because the harness's own line overstates it:** the fixture run prints "every mutation that
   changed the page was caught", and four of those catches (the divisor, the weekly positions, the losing moves, the
   blend) are P5 reading a side effect, a starter walking onto the drop ladder when the rates shift, not a guard
   reading the named defect. The two rate mutations still have no guard of their own. Three mutations stay NO EFFECT
   on both rosters (an emptied starting slot, a man replacing himself, the negative drop cost) and need a second
   fixture or a re-aim.
4. **The handcuff against the starter's prior-season availability (4.48's last open line): suggestive in one cell,
   underpowered, not a page term.** Among handcuffs at week 4 whose lead back missed four or more games the season
   before (n=19), the lead missed three or more of weeks 5 to 14 36.8% of the time and the handcuff gave a 15-point
   month 10.5%; at zero games missed (n=12) 16.7% and 8.3%; at one to three (n=24) 4.2% and 4.2%. Four-plus against
   the rest on the starter falling: p=0.084. Not monotone, cells of 12 to 24, and the seat constant's own note (doc
   276: 45.9% against 46.3% by history) measured the same question on a bigger population and found nothing. The
   direction in the four-plus cell is 4.22's and it is recorded here as NOT a change.

---

## 1. THE HANDCUFF TEST

**The claim in testable form:** among handcuffs at the end of week 4 (the second back by touches on his team, under
8 a game, behind a lead at 12 or more, himself under the bar; doc 460's cell), the lead back's games missed the
season before (nflverse, weeks with 3 or more touches against 17) predicts whether he misses three or more of weeks
5 to 14, and the handcuff's big-hit columns. POPULATION: 2022 to 2025 (the prior season must be in the cache), 58
handcuffs, 3 of whose lead backs had no prior-season line. RESULT: in the table above; Spearman between prior games
missed and the handcuff's startable weeks 0.20 (p=0.15, n=55). TESTED, underpowered; the doc 276 note stands. Run
inline off `tail_tickets.py`'s builder; the cells are in this doc and nowhere else on purpose.

## 2. THE FIXTURE

`Source\fixture\MY_ROSTER.csv` and its README. Synthetic by design: Malik Washington in the IR slot and OUT (a priced
man, the cheapest he owns), Vele removed (no bench receiver under the bar), Raymond at value 20 (a starter by the
roster file's own value and the cheapest same-position drop for a receiver add), Dowdle on the bench so the IR
count stays three, fourteen active. `check_guards.py --fixture` lays the folder's CSVs over the harness's working
copy and never touches the live tree; nothing in `ff.bat` reads the folder. Result on the fixture: 7 caught, 3 NO
EFFECT, 0 survived; on the live roster, unchanged (1 caught, 2 survived, 7 NO EFFECT). `check_kit.py`: one pin.

## 3. OPEN, BY NAME

- A second fixture, or re-aimed mutations, for the three that stay NO EFFECT; a guard of their own for the two
  rate mutations (the divisor, the weekly positions), which no fixture can supply.
- The live playoff number the morning the schedule lands, then v9.39 at the week close (one paste, not two).
- `audit_directive.py` on the drive tree; the catalog's remaining batch (A2, A3, A6, B3); the payload wiring; the
  store move when it crosses 1.6 million; the week-8 seat-weeks reading.
