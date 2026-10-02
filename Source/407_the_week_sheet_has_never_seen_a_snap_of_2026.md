# 407 — The week sheet has never seen a snap of 2026

**23 Sept 2026. Matt, on the week sheet: *"It's telling me to pick up a kicker even though my
current doesn't have a bye until week 8. Mevis is next to last on the year for points scored.
Completely nuts."***

**He is right, and the kicker is the cheapest symptom of the largest defect this page has ever
carried. The page is not mis-ranking kickers. THE PAGE IS READING AUGUST.**

---

## THE ROOT CAUSE, AND IT IS ONE LINE

`sheet_engine.py`, `rates()`:

```python
pulls = sorted(_glob.glob(os.path.join(src, 'espn_projections_2026_*.csv')))
...
'wk': pr / PROJ_GAMES        # pr = proj_2026, PROJ_GAMES = 17.0
```

`pulls[-1]` on his drive is **`espn_projections_2026_20260907_1258.csv`**, whose own
`captured_at` field reads **`2026-09-07T12:58:59-04:00`** — draft day, seven hours before the
draft, **before a single snap of the 2026 season**. Its `actual_2026` column is **empty for every
row**.

**Every `wk` rate on the week sheet is a preseason season-total forecast divided by 17.** His
roster, the entire free pool, the bar grid, every priority pickup, every drop cost, the "cheapest
man you own" table. **Three weeks of football have been played and the page has seen none of it.**

**AND THE HORIZON IS PRESEASON TOO.** `WEEKS = list(range(1, 15))`, hardcoded, never advanced. On
23 September the page is still pricing weeks 1, 2 and 3 as though they were ahead of him.
**Three of the fourteen weeks it sells are already played** — 21% of every total on the page is
dead weeks.

---

## WHAT IT DID TO THE KICKER — reproduced exactly

Mevis and Pineiro in that pull:

| | proj_2026 | page's wk rate | rank among 32 K |
|---|---|---|---|
| Harrison Mevis (LAR) | 159.4 | **9.38** | **3rd** |
| Eddy Pineiro (SF) | 155.2 | 9.13 | 6th |

**In August, Mevis was the third-best kicker in football. The page still believes that.** Matt is
reading the year; the page cannot see the year.

`bar_grid` bisects the rate a new player must beat to change the best legal nine. Pineiro is the
only kicker, so:

| week | bar | Mevis gain |
|---|---|---|
| 1–7, 9–10, 12–14 (12 weeks) | 9.1 (Pineiro, rounded to 1dp) | **0.3** each |
| **8 — Pineiro's bye, no kicker at all** | **0.0** | **9.4** |
| 11 | Mevis' own bye (LAR) | — |

**9.4 + 12 × 0.3 = 13.0, the exact number on the page.**

**72% of that 13.0 is week 8 alone**, where an empty slot drops the bar to zero, so *any* kicker
scores full value. The remaining 3.6 is a quarter-point a week — and **0.6 of that 3.6 is pure
rounding**: the true weekly edge is 0.25, `bar_grid` rounds the bar to 9.1, and 0.25 prints as 0.3.

**Then the 13.0 is sorted against Hunter Henry's 11.1 and ranked above it.** The 13.0 is a
one-week hole five weeks out. The 11.1 is expected points. **They are not the same unit and the
page ranks them against each other.** §4.31's own scope line says the waiver finding is *"not for
empty slots or forward claims"* — and the page is doing precisely that inside the list §4.31
governs.

**AND THE PAGE SAYS OUT LOUD IT CANNOT PRICE THIS AND PRINTS THE NUMBER ANYWAY.** *"nothing free
is measured at this position"* is the `_alt is None` branch: the constants' `absence.streamer`
block has no `K` entry, so the page cannot net Mevis against the ordinary kicker he would claim
instead. That branch exists to warn the figure is **a floor**. It then prints the un-netted floor
as the headline and sorts the whole list on it. Against a replacement kicker the real week-8 edge
is near zero, because **all 32 of them fill an empty slot**.

---

## THE SAME DEFECT PRODUCED THE SCHULTZ TAKE, AND THAT ONE WAS MINE

From the same pull:

| | page's wk rate (August) | measured 2026 |
|---|---|---|
| Hunter Henry | **7.20** | **4.8 ppg**, 3 and 5 targets at 76%/91% snaps — a blocker |
| Dalton Schultz | 6.06 | **12.8 ppg**, 8 then 14 targets |

**The page ranked Henry above Schultz because ESPN projected Henry higher in August.** Doc 404's
recommendation — pass on Schultz, wait for Henry — came off that ordering, and doc 406 retracted
it. **One root cause explains the kicker, the tight-end ranking, and my own backwards take.**

---

## WHAT I HAD WRONG ABOUT MY OWN OPEN THREAD

This sat in `OPEN_THREADS.md` as *"the week sheet's vintage failure: 12 rows printing preseason
rates this season refutes."* **That scoping is wrong and it is mine.** It is not 12 rows and it is
not a display problem. **It is the pricing model**, and scoping it as a row-level cosmetic is why
it survived three weeks of the season.

**§0.5(a5): I measured the ring, not the centre — again.** Doc 406 caught one wrong tight end.
Nothing asked the question one level up: *what vintage is the number that ranked him?*

---

## THE FIX — MINE, NOT SHIPPING TONIGHT

**Not tonight, and the reason is doc 144: three scripts shipped in one session and all three died
on his machine.** His waivers finalise tonight and this is not a claim decision. A pricing-model
rewrite pushed at 21:00 on waiver night is the §0.4 failure in its most expensive form.

**[NOT YET RUN] The four changes, in order:**

1. **Advance `WEEKS`.** Price from the current week forward, never from 1. Read the week from the
   same place `wire.py` does; refuse the page if it cannot be determined (§0.2: an exit code is
   not a result).
2. **Blend measured 2026 into `wk`.** `form_2026.csv` week 0 carries season-to-date half-PPR for
   **RB/WR/TE only** (doc 375 — the feed does not score passing or kicking). So QB, K and D/ST
   need their rate from a fresh pull's `actual_2026`, not the form feed. **State the blend weight
   and its population on the page**, per §3.
3. **Never rank a forward hole against season points.** A bye cover is priced at the **marginal**
   value of acting now versus acting the week before the bye — which for a kicker is
   approximately zero. Either net it against the replacement at that position or **exclude
   empty-slot rows from the priority list entirely** and print them in their own "byes ahead"
   block. §4.31's scope line already required this.
4. **Refuse rather than print a floor.** Where `absence.streamer` has no entry for a position,
   the row does not get a headline number and does not enter the sort.

**[NOT YET RUN] A guard, built with its negative control first (§0.2):** a check that refuses the
sheet when the newest projection pull predates the current week's kickoff. Today's page would have
failed it on 8 September and every day since.

---

## WHAT HE SHOULD DO TONIGHT

**Nothing about a kicker.** His own to-do already carries *"week 7 add a kicker for week 8"*, and
the page's own hot-kicker rule reads *"from week 6"*. The page contradicts both his calendar and
its own stated rule. Picking up Mevis in week 3 spends a roster spot and a claim for five weeks to
solve a one-week hole that any of 32 kickers solves in week 7.

**His four claims stand, and they stand because he did not build them off this page.** Schultz's
two good weeks, Tucker rising, Puka's unknown return, the Bengals defence — every one of those is
a 2026 read. **The page could not have produced any of them.**

**His check was cheaper than mine.** *"Mevis is next to last on the year"* is a vintage test, run
in one sentence, and it found a defect three levels below the kicker.
