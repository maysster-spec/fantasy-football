# 465. WHAT EACH SEAT HAS RETURNED SO FAR

*1 Oct 2026, 10:55 ET. Claude (Cowork). Doc 463 section 3, item 5, built. 465 reserved by listing `Source\`. No em dashes.*

---

## 0. WHAT TO DO

1. **Nothing to run.** `py research\seat_weeks.py` prints the table any time; it reads the executed moves and the form
   file, nothing else.
2. **Read it as a baseline, not a verdict: three weeks is too thin to say anything about your churn yet.** Your
   added men have held 8 seat-weeks and returned 2 startable weeks (4.0 seat-weeks per startable week); your drafted
   men 29 and 9 (3.2). Backs, receivers and tight ends only, bar at the position's startable rate, a man-week counted
   whether or not he was in the lineup (lineups are not on file). The number to watch is the added men's ratio at
   week 8 against the drafted men's: if it is still above 4, the churn is paying in seat-weeks and not in starts, and
   doc 460's rule (a ticket only with a seat that costs nothing) is the fix; if it comes down, the adds are working.
3. **Two things it already shows, for what three weeks are worth:** the only added man to return a startable week on
   his own was Jonah Coleman (13.3 in week 2, then hurt); Hockenson's one week was a bye fill. Among the drafted men,
   Dobbins, Judkins and Dowdle have nine seat-weeks and no startable week between them, which is the same thing the
   standings line said (the deficit is men under their rates) in the seat's own unit.

---

## 1. WHAT CHANGED

`research\seat_weeks.py` (new, pinned): rebuilds the roster week by week from `waiver_report_2026.csv` walking back
from `MY_ROSTER.csv`, scores every man-week off `form_2026.csv` (name and position, since the form file carries no
id), counts seat-weeks against startable weeks, drafted against added. Quarterbacks are left out because the form
file scores rushing and receiving only (doc 375); kickers and defenses likewise. `run_seat_weeks.txt` is the 1 Oct
table. `check_kit.py`: one pin.

## 2. OPEN, BY NAME

- The fixture roster for the mutation harness (catalog A5): a frozen `Source\fixture\` where a parked man is the
  cheapest drop and a starter is the cheapest same-position drop, so the two parked-man mutations and the own-position
  mutation can be shown caught rather than NO EFFECT. Half a day; not started.
- The live playoff number the morning the schedule lands (doc 464), then v9.39.
- `audit_directive.py` on the drive tree; the catalog's remaining batch (A2, A3, A6, B3); the payload wiring; the
  store move when it crosses 1.6 million.
