# 467. A DEFENSE ENTERS THE PICKS ONLY TO FILL A HOLE, AND THE HARNESS COULD NOT SEE ONE

*1 Oct 2026, 17:40 ET. Claude (Cowork). Matt, 12:30: "Can you start? If so please do." The row I told him to ignore
at 08:50 (the Chiefs defense leading the priority pickups) was still on the 12:04 page, because the fix was promised
in a reply and filed nowhere. 467 reserved by listing `Source\`. No em dashes.*

---

## 0. WHAT TO DO

1. **Nothing to run.** The 07:30 run picks up `sheet_engine.py`, `check_page_logic.py` and `check_guards.py` as they
   are now; `ff.bat` is unchanged.
2. **The rule, restated as the page applies it now: a defense or kicker enters the priority pickups only to fill a
   hole (a week with nobody in the slot), chosen and priced on the hole weeks alone.** The matchup lane on the wire
   prices the rest of their season. "Chiefs D/ST +7.8, outscores your defense in 10 weeks" cannot print again, and
   the week-8 kicker row on the bye calendar ("claim in week 7, no kicker in week 8, Harrison Mevis") is back.
3. **Two guards that did not exist read the page now, and both fire on the real defect:** P8 fires on the 08:04
   page that carried the Chiefs row; P9 fires when a projected rate is the file's total over 17 instead of over the
   games left (the week-4 page divides by 14). The mutation harness reports both rate mutations caught on the live
   roster by a guard of their own, which closes the "no guard covers it" line docs 463 and 466 carried.
4. **The lesson, filed where it bites (0.5e, 0.5f):** "ignore that row, I will fix it" is a promise, and a promise
   that is not in `claude_todo.txt` before the reply goes out is how a defect survives a morning. The 08:50 reply
   named the row and the fix went in no file; the 12:04 page printed it again and Matt did not have to find it only
   because I re-read the page before he did.
5. **The store is at 1,583,727 of 2,000,000**, read this turn; the move at 1.6 million is not yet due.

---

## 1. WHAT WAS WRONG, AND WHAT THE FIRST FIX BROKE

Doc 424 put `season_priced()` on THE CALL and the drop table. The priority pickups list under them was never covered:
a defense with the biggest season total over his two defenses' bars led the list on a season rate, which 4.39 says is
the wrong currency for the position. The first cut of the fix kept the season-total selection and then cut the man to
his hole weeks; on the kicker that chose a man whose own bye was the hole, so the hole total was zero and the week-8
calendar row vanished. The selection now runs in the position's own currency: for a weekly position every candidate
is priced on the hole weeks before the best one is chosen.

**And the harness could not have shown either outcome (0.2: the object production builds).** `WIRE_<date>.csv` and
`FREE_UNRANKED_<date>.csv` carry backs, receivers, tight ends and quarterbacks only; the live run's free pool is
every free id on ESPN, kickers and defenses included. Both the sandbox harness and `check_guards.py`'s render built
pages with no free kicker or defense at all, so the Chiefs row's absence after the first edit was the pool, not the
fix, and the kicker row's absence was the pool too. Both renders now add every priced kicker and defense on no league
roster (`LEAGUE_ROSTERS.csv`), and the hand-made "Jets D/ST" row the harness used to carry is gone: it collided with
the real Jets D/ST and P9 read it as a divisor error.

## 2. THE TWO GUARDS

**P8** (`check_page_logic.py`): a defense or kicker on "Priority pickups, in order" must carry a hole line ("No kicker
in week 8") and never a season line ("Outscores your defense in 10 weeks"). Four controls: the 08:04 page's Chiefs row
fires; Mevis filling week 8 is quiet; a receiver on a season rate is quiet (his currency); no list is quiet. Run on
the real 08:04 page from the drive: fires, naming the Chiefs row.

**P9**: every rate the grids mark as ESPN's own projection (`data-vintage="proj"`) equals that man's rest-of-season
total in the newest `espn_projections_2026_*.csv` over the games left, 17 less the weeks played, read off the grid's
own first week column; a name the file spells differently is skipped, a missing projection file fails outright. Four
controls: the file over 14 games is quiet; the same total over 17 fires; a blended rate is skipped; no file fails.
On the harness page: 18 projected rows checked, none off.

**`check_guards.py`**, live roster: divisor caught (P9), weekly positions caught (P8), blend caught (check_vintage),
seven NO EFFECT. Fixture: all seven mutations that change the page caught, three NO EFFECT as before. 53 controls in
`check_page_logic.py --selftest`; check_plain, check_vintage, check_page_rules, check_inputs, check_locals clean;
`check_kit.py` three pins.

## 3. OPEN, BY NAME

- The three NO EFFECT mutations (an emptied starting slot, a man replacing himself, the negative drop cost) still need
  a second fixture or a re-aim.
- The per-position "worth a look" grid still prints a season column for defenses and kickers. It is a display grid
  and drives no decision, so it is left alone under 0.5(a)'s v9.17 line; it is named here so nobody reads it as a
  pick.
- The live playoff number the morning the schedule lands, then v9.39; `audit_directive.py` on the drive tree; the
  catalog's remaining batch (A2, A3, A6, B3); the payload wiring; the week-8 seat-weeks reading; the store move at 1.6
  million.
