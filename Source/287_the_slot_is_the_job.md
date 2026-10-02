# 287 — He caught my own card contradicting itself, and "out-targeting the man ahead" is the wrong bar

**2026-09-10.** Matt: *"why do two players need to get hurt. you just provided that they have
different roles and one was deep and the other possession."*

**Both halves of that card are mine and they do not cohere.** The news line says *"Mims is a deep
threat and Bryant is a possession receiver, so they are not competing for the same snaps"* and the
bear line says *"a third receiver in Denver has to survive two people getting hurt to matter."*
**If they are not competing for the same snaps then nobody has to get hurt — that is the whole point
of the first sentence, and I wrote the second one anyway.** The bear case was a generic "WR3s don't
matter" line that never looked at the alignment data sitting in `pff_receiving_2025.csv`.

---

## 1. WHO PLAYS WHERE — MEASURED, NOT ASSERTED

**POPULATION: every receiver with 100+ routes in 2025, n=154. SOURCE: `pff_receiving_2025.csv`.**

| | routes | **slot %** | wide % | target depth | yards per route |
|---|---|---|---|---|---|
| **Courtland Sutton** | 628 | **18.5** | **81.5** | **13.3** | 1.62 |
| **Jaylen Waddle** *(2025 at MIA)* | 416 | 23.0 | **76.5** | **13.2** | 2.19 |
| Troy Franklin | 489 | 45.1 | 54.7 | 13.0 | 1.45 |
| Marvin Mims Jr. | 275 | 30.7 | 65.2 | 9.6 | 1.17 |
| **Pat Bryant** | 309 | **57.8** | 40.6 | **10.0** | 1.22 |

League medians among the 154: slot 35.3% · wide 63.0% · target depth 12.1. `[SOURCED]`

**SUTTON IS THE X — the boundary receiver, 81.5% wide at 13.3 yards deep, the most wide-aligned of
the five.** Waddle is the same shape (76.5% wide, 13.2 deep), which is what makes Denver's two
starters a matched pair rather than a complement.

**BRYANT IS THE ONLY ONE OF THE FIVE WHO PLAYS MOSTLY IN THE SLOT — 57.8%, at 10.0 yards.** He and
Sutton overlap almost nowhere. **So Matt is right and my bear line was wrong: Bryant does not need
Sutton or Waddle to get hurt. He needs the slot.**

**AND THE MAN HOLDING THE SLOT IS TROY FRANKLIN, WHO WAS 31st OF 33 AT 6.95 YARDS A TARGET** among
receivers with 90+ targets — against Bryant's 8.04 on 47 looks (doc 286). **That is one man to beat,
on performance, with no injury required.**

**THE COMPLICATION, STATED BECAUSE IT CUTS THE OTHER WAY: Denver ADDED Waddle**, a 76.5%-wide
receiver, so the boundary is now Sutton and Waddle. **Franklin, at 54.7% wide, is the man squeezed —
and where he gets squeezed to is inside, onto Bryant.** So the same signing that locks the boundary
also sharpens the fight Bryant has to win. `[SOURCED, not modelled — 2026 alignment does not exist yet]`

---

## 2. HIS SECOND POINT IS THE BIGGER ONE, AND IT IS NOW MEASURED

> *"a player doesn't ahead of him in targets doesn't need to happen for the FA to have increased
> value. Not with all these indicators we have been discussing."*

**He is right, and I have been quoting the wrong number all day.** §4.28 / doc 251's headline —
**60% of first-round rookies displaced the man ahead** — defines the outcome as *out-targeting the
incumbent*. That is a **threshold that requires beating the team's best receiver**. Value does not
work that way: it accrues continuously with targets, against replacement, and a man can go from 47
looks to 90 without ever touching Sutton's 120.

**THE TESTABLE FORM (§0.5a2): among young receivers behind a returning 60+-target team leader, how
often does one become STARTABLE without out-targeting him?**

**POPULATION: transitions 2022→23, 23→24, 24→25. Same team both years, the leader still on the
roster, the teammate in his first three NFL seasons with 4+ games. n=141 pairs. BASELINE: startable
= 9.62 half-PPR points a game, doc 12's measured WR replacement. EXCLUDED, and it matters: 225
teammates had no row in `nfl_draft_picks.csv` — undrafted men, dropped, so this is a drafted-receiver
population. Receiving points only (0.1/yd, 6/TD, 0.5/rec); rushing excluded, which understates.**

| | out-targeted the leader | did NOT |
|---|---|---|
| **became startable** | **9** | **5** |
| did not | 13 | 114 |

- displacement rate **22/141 = 15.6%**
- startable rate **14/141 = 9.9%**
- **OF THE 14 WHO BECAME STARTABLE, 5 — 36% — NEVER OUT-TARGETED THE MAN AHEAD.** `[TESTED, n=141]`
- **AND IT FAILS IN THE OTHER DIRECTION TOO: 13 of the 22 who DID out-target him were still not
  startable.** Displacement is neither necessary nor sufficient.

**The five: DeVonta Smith behind A.J. Brown (112 targets to 152, 11.82 a game) · Jaylen Waddle behind
Tyreek Hill (104 to 167, 11.53) · Jameson Williams behind St. Brown (88 to 138, 11.41) · Quentin
Johnston behind McConkey (78 to 102, 10.50) · Josh Downs behind Pittman (102 to 106, 10.45).**

**THE RULE THAT REPLACES THE ONE I WAS USING: the question is whether he clears replacement, never
whether he passes the man ahead.** They agree about half the time, which is why quoting the 60%
displacement rate as "his chance of mattering" is wrong in both directions. **This is §4.13b's
two-definitions lesson — ratio versus absolute — arriving at receiver for the second time, and the
same lesson doc 251 already applied to itself when it reported "40% were startable in year one" and
then let the displacement headline do the talking anyway.**

**FOUR OF THE FIVE ARE YEAR THREE, and every one of them is the second receiver in a two-man room,
not a rookie fighting for scraps.** `[OBSERVED, n=5 — a shape, not a finding]`

---

## 3. WHAT CHANGED ON THE ARTIFACTS

- **`cards_2026.csv`** — Bryant's signal and bear lines rewritten. The bear is no longer "two men
  must get hurt"; it is **"he has to take the slot from Troy Franklin, and Waddle's arrival pushes
  Franklin inside toward him."** The alignment numbers are on the card.
- **`matt_reads.md`** — two new rows, both **CONFIRMED**: the role-overlap read, and "a receiver does
  not need to pass the man ahead."
- **Nothing else moves.** The recommendation is unchanged and so is its timing: Bryant at week 2, not
  week 1 (9.4% against 34.6%, doc 252).

---

## OPEN AFTER THIS

- **The wire has no alignment column and now clearly should.** `pff_receiving_*.csv` carries
  `slot_rate`, `wide_rate` and `inline_rate` for every receiver, and doc 251 records that slot rate
  is the **most stable receiver trait measured anywhere** (0.75, above production). **NOT YET RUN:**
  put slot / wide / target depth on every free receiver, so "who does he actually compete with" is
  on the page instead of in a doc.
- **And that is the §4.28 BLOCKED line, retractable.** §4.28 says the slot-rate indicator is
  *"the one indicator we still cannot compute — BLOCKED on a true slot rate (a PFF field)."* **The
  PFF field is on the drive and has been since 09-09** (doc 263 already retracted the same claim
  once). **§4.28's blocked line should be struck at the next directive edit.**
- **n=141 with 14 startable is thin**, and the undrafted exclusion removes 225 teammates — including
  the archetype Nacua-at-round-5 sits next to. The 2021 PFF file would add a fourth transition and is
  not on the drive.
- **Whether a slot receiver's value is more or less dependent on the room than a boundary
  receiver's** is the natural extension of doc 284 and is `NOT YET RUN`.
