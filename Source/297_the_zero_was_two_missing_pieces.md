# 297 -- A1: the zero on the drop table was two missing pieces, not one

**12 September 2026.** Catalog item A1, the first of batch 1's second half: *no injuries anywhere
in the pricing*. Tested. The answer is yes, the missing model changes the drop order, and the
bigger of the two distortions turned out not to be injuries at all.

---

## 1. The claim in its testable form, written before the run

> On Matt's 15, weeks 1-14, with each man's weekly availability drawn from measured position
> absence rates instead of byes alone, the cheapest-drop ORDER changes: Hockenson stops pricing at
> 0.0 because he enters the lineup in the weeks LaPorta is out, and the ordering of the cheap
> bodies is not the bye-only ordering.

Right claim, and incomplete. Running it exposed a second assumption nobody had stated.

---

## 2. Step 1: how often does a starter-quality player actually miss a week?

**POPULATION, chosen so nothing about the season being measured enters it:** for season t, the men
who finished top-24 at RB, top-24 at WR, top-12 at QB and top-12 at TE in season **t-1** by
half-PPR over weeks 1-14. Their availability is then read in season t.
**DENOMINATOR: his team's weeks 1-14 that were actually played**, so the team bye is removed; the
sheet already models byes and this is the other kind of absence.
**SOURCE: nflverse `stats_player_week`, 2021-2025, regular season. n = 318 player-seasons over four
transitions.** `[TESTED]`

| pos | n | weeks missed a season | share of weeks missed | played every week | missed 3+ |
|---|---|---|---|---|---|
| QB | 47 | 1.79 | **13.7%** | 60% | 30% |
| RB | 94 | 2.22 | **17.1%** | 44% | 36% |
| WR | 96 | 1.95 | **15.0%** | 42% | 31% |
| TE | 47 | 1.79 | **13.7%** | 34% | 32% |
| K | 34 | 2.76 | 21.3% | 56% | 35% |

Per season it is stable and not one bad year: QB 8/13/13/22%, RB 22/16/16/14%, WR 13/7/18/21%,
TE 13/13/17/12%.
**The kicker row is the shakiest cell on the table and should not be quoted:** 14 of the 48 prior
year top-12 kickers were not in the league at all the next season, and they are excluded from the
denominator, so 21.3% understates the risk of owning one.

**AGAINST doc 111 [INHERITED]: it measured a drafted starting QB missing 2.98 weeks a season in
this league; this measures 1.79.** The populations differ and doc 111's is the harsher one -- his
is the quarterback a manager DRAFTED as a starter, mine is a man who had already finished top-12.
**So these rates are a lower bound**, and every table below is also run at doc 111's level, scaled
by 2.98/1.79.

---

## 3. Step 2: the 2x2, because two things change at once

The simulation runs Matt's 15 through the production `week_points()` (the object the page builds,
not an equivalent one), fourteen weeks, availability drawn per man per week, **paired**: one draw
per simulation reused for the full roster and for every candidate drop. n = 6,000.

The second assumption, which nobody had written down: **what happens to a slot when you drop the
man in it.** The page charges an empty slot as ZERO. Matt streams. Those are different worlds, so
both are run.

**Drop cost, cheapest men, measured rates:**

| | hole left EMPTY (what the page charges) | hole STREAMED (what Matt does) |
|---|---|---|
| **byes only** *(the page today)* | Washington 0.00 · Hockenson 0.00 · Dobbins 2.60 · Dowdle 4.29 · Worthy 8.54 · Shough 18.01 | Washington 0.00 · Hockenson 0.00 · Shough 1.36 · Browns 1.48 · Worthy 2.00 · Dobbins 2.60 |
| **measured absences** | Washington 1.73 · Hockenson 13.33 · Worthy 15.73 · Dobbins 16.44 · Dowdle 20.49 · Shough 40.17 | **Washington −0.98 · Browns 1.48 · Shough 3.05 · Hockenson 3.73 · Worthy 4.86 · Dobbins 12.59** |

Streamer rates used, declared `[INHERITED]`: QB 16.65 (doc 92, re-derived from the raw files),
TE 5.53, WR 6.54, RB 5.43 (doc 12), D/ST 5.99 (doc 265).

**THE ANSWER TO A1: yes, the order changes, in three of the four cells, and never in the page's
own.** The cheapest man does not change -- it is Washington in every cell -- but the cheapest FOUR
do.

**AND THE BIGGER DISTORTION IS THE ONE NOBODY WAS LOOKING FOR.** Adding streaming alone, with no
injury model at all, moves Shough from 18.01 to **1.36** and Worthy from 8.54 to **2.00**. Adding
injuries alone moves Hockenson from 0.00 to 13.33 and Shough to 40.17. **The two corrections push
in opposite directions and the page has neither**, so its errors do not cancel, they compound in
whichever direction the man happens to sit.

**Tyler Shough is the clearest case: 18.01 on the page, 3.05 when both corrections are made.**
That is 4.17b's quarterback-two argument arriving at his live roster from a third direction, and it
lands at the low end of that section's own +5 to +11 band or below it.

---

## 4. THE HANDCUFF, AND MATT'S INSTINCT IS BACKED BY THE MEASUREMENT

§6's rule, through doc 240: *a bench running back earns his spot by the job he would inherit, never
by his own projection.* The simulation above breaks that rule, because in the weeks Jeanty is out
it scores Washington at **his own 3.68 a game** -- which is exactly what the page does. Re-run with
his rate in those weeks set three ways (measured absences, hole streamed, n=6,000):

| what Washington scores in the weeks Jeanty is out | his drop cost |
|---|---|
| his own projection, 3.68 *(what the page assumes)* | **−0.98** ± 0.02 |
| doc 244's median relief rate, 11.2 | **+3.84** ± 0.05 |
| the job itself, 248 ÷ 17 = 14.6 | **+10.02** ± 0.10 |

**His entire value sits in that one assumption, and the page picks the least favourable of the
three.** Matt's standing line is *"Mike Washington Jr. -- 0% chance i drop him."* Under either
measured assumption he is right, and under the page's own arithmetic he is wrong. **Surfaced, not
overridden (0.5b), and it is a point for his record: this is the third live case where a price he
rejected turned out to be the instrument's fault rather than his.**

---

## 5. What I told him last night was low, and this corrects it

Doc 295 and `matt_todo.txt` said Hockenson's only value is LaPorta insurance, *"about a point,
maybe two if LaPorta misses two or three games."* **Measured here: 3.73 with the hole streamed, and
5.69 at doc 111's absence rates.** The direction was right and the size was about half. The to-do
line is corrected; the Kaelon Black recommendation is unaffected, because the drop it costs is
still the cheapest thing he owns under every cell of the table except one where it is second.

---

## 6. What this does NOT license

* **No code change shipped today.** The sheet still prices byes only and says so on its own face
  ("this page prices byes and not injuries"). Teaching it an absence model touches the bar grid,
  every price and the bet, and 4.18c's warning about changing what the objective measures applies
  to the sheet as much as to the draft engine. **The next item, and it is now specified:** put the
  handcuff's relief rate into the drop table so a carded handcuff is priced by the job, which is
  the single change with the largest measured effect and the smallest blast radius.
* **The absence rates are position averages, not player forecasts.** §4.25b is the governing
  finding: age nets to zero, availability is the signal, and 4.22's own qualification is that among
  established veterans last season's games do not predict next season's. Nothing here forecasts
  WHICH man misses time.
* **The kicker cell should not be quoted.**

**Reproduce:** `Scripts\research\a1\absence_rates.py` then `a1_injury_sim.py`, stdlib only, the
nflverse weekly files named in the header.
