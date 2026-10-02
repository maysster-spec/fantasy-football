# 285 — The other three receivers, re-ranked by the room, and two cards that went stale in a day

**2026-09-10.** Matt: *"Wasn't there the other WRs beyond Ricky Pearsall?"* **Yes — three, all still
free, and doc 284's measurement reorders them.** Checking also found two cards recommending players
somebody else had already claimed.

---

## 1. THE FOUR SCREENED RECEIVERS, ALL STILL FREE, RANKED BY THE ROOM

**POPULATION: every player on the 09-10 evening wire (279 free) carrying a pedigree screen. SOURCE
for the room: `team_shape_2025.csv`, built in doc 284.**

| receiver | tm | owned | screen | his receiver room in 2025 |
|---|---|---|---|---|
| **Jalen McMillan** | TB | 33.0% | 3 of 3 | **67% of team targets, fed 5 — the most spread offence in the league** |
| **Pat Bryant** | DEN | **1.9%** | 3 of 3 | 61%, fed 4 |
| **Omar Cooper Jr.** | NYJ | 5.2% | **first-round rookie** | 60%, fed 3 |
| ~~Ricky Pearsall~~ | SF | 2.8% | 3 of 3 | **45%, fed 3 — third smallest room in the league** |

**PEARSALL NOW HAS A SECOND REASON AGAINST HIM AND IT IS INDEPENDENT OF THE KNEE.** San Francisco's
receivers took **45%** of the team's targets. Doc 284 measured that a promotion inside a small room
is worth roughly half what it is worth on a spread team, and the mechanism is the pie, not the rank.
So even in the world where his PCL had held, he was sitting in one of the three worst rooms to be
promoted inside. **The verdict does not change — he is out for the season — but the reasoning is no
longer single-threaded.**

**AND THE ONE THE MEASUREMENT IMPROVED IS McMILLAN.** Yesterday's card called him *"the same screen
on a thinner base"* and ranked him last of the three live names because his rates come off **four
games**. That caveat stands. What has changed is the other half: **Tampa Bay fed FIVE receivers and
gave the room 67% of all targets, the widest in the league.** On doc 284's finding that is the single
best room on this page to be promoted inside.

**THE TWO SIGNALS ARE ABOUT DIFFERENT SEASONS AND MUST NOT BE BLENDED (§4.13b's lesson, a new place).**
- **Bryant and McMillan carry the three-signal screen**, whose headline — 39.4% — is *startable the
  FOLLOWING season* (doc 248). Its in-season form is 33.3% against an 8.3% base (p=0.028).
- **Cooper carries draft capital**, whose number is about *THIS season*: a first-round rookie paired
  with a returning target leader out-targeted him **9 times in 15**, and **40% of those rookies were
  startable in year one** (doc 251).
**So Cooper is the one whose evidence is about 2026 and Bryant is the one whose evidence is about
2027.** Both are real, neither is a forecast for a person.

**THE RECOMMENDATION, AND IT IS TO DO NOTHING THIS WEEK (§0.1f).** The roster is **15 of 15**, so
every one of these costs a drop, and the cheapest drop is the Hockenson blanket at **0.0**. Against
that, **§4.31 is decisive about the calendar and not about the players: a week-1 claim converts at
9.4% and a week-2 claim at 34.6%, Fisher p=0.010.** One week of patience measures at roughly three
times the hit rate, because a week-1 claim bets on a depth chart and a week-2 claim bets on a snap
count. **Hold. At week 2 the seat goes to Pat Bryant** — healthy, 3 of 3, **1.9% owned so nobody
else is bidding**, and a room that feeds four — *unless* a Jets receiver goes down, in which case it
is Cooper, whose signal is the one about this season.

---

## 2. TWO CARDS WENT STALE INSIDE ONE DAY, AND THE PAGE WOULD NOT HAVE SAID SO

**`cards_2026.csv` is hand-written. The pool is not.** Checked against the evening wire:

| card | lane | still free? |
|---|---|---|
| Ricky Pearsall · Omar Cooper Jr. · Pat Bryant · Jalen McMillan | screen | **yes** |
| **Jordan James** (SF) | seat | **NO — claimed today** |
| **Brian Robinson Jr.** (ATL) | seat | **NO — claimed today** |

Both were on yesterday's seat list as live recommendations — Robinson at the top of it, behind Bijan
on a **314.8** job. **They are gone, and nothing on the sheet would have told him.** This is the
missing-row check inverted: §0.5(c)5 catches a row that should be on the page and is not; **this is a
row that should NOT be on the page and is.** Nothing in the project covered that direction.

**THE FIX, AND IT MARKS RATHER THAN DROPS.** `load_cards()` now reads the newest `WIRE_*.csv` and
stamps `gone` on any card whose man is no longer free; the page prints **"NO LONGER FREE — somebody
claimed him"** on the card and keeps it. **Deleting it would be the wrong repair** — *"he was on here
yesterday and now he is not"* is itself information, and in this case it is the second piece of
evidence this week that the room is moving on backfield seats faster than on receivers.

**NEGATIVE CONTROLS, RUN ON THE PRODUCTION RENDERER:**

| control | expected | got |
|---|---|---|
| live files | the two backs marked, the banner naming them, 2 notices on the page | **pass** |
| **no WIRE file at all** | nothing marked, and the reason SAID | **pass — never guesses** |
| a wire listing all six | nothing marked, no banner | pass |

`sheet_engine.py` 38747 → 40250 (`e44de5e63a84ac15`), re-pinned. The four receiver cards also gained
their room in plain English.

---

## OPEN AFTER THIS

- **`py wire.py --html` still unrun since these three changes** — the tight-end sort, the receiver
  room column, and now the card staleness check all land on the same single run.
- **The seats are being taken and the receivers are not.** Two of fourteen backfield seats went in a
  day against zero of four screened receivers. `NOT YET RUN`: whether the claim rate on a backfield
  seat is measurably faster than on a receiver in this league — `waiver_report_*.csv` holds the
  timestamps, and `py waivers.py --live` would add 2026.
- **Cooper's 40% is n=15** (doc 251) and **Bryant's 33.3% is an in-season cut of n=152**. Both are
  the thinnest kind of evidence this project acts on, and the page says 39%/40% without saying n.
  `[OPEN]` — whether a rendered card should carry a sample size is a §0.1 scope-rule question and it
  has not been decided.
