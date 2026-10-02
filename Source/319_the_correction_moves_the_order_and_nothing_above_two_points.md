# 319 -- B1: the absence-aware bar moves the order of the free pool, and nothing on it above two points

**16 September 2026.** Catalog item B1, from `REDTEAM_TASKING_PROMPT.md` section B: *doc 297
corrected the DROP costs only; the bar every free player is measured against still assumes
everybody plays fourteen weeks.* Run in full: Matt's 15 plus every free skill player, fourteen
weeks, 3,000 paired draws, five arms, through the production lineup code.

---

## 0. WHAT TO DO

1. **Nothing to run, and no code change to the sheet's price.** The correction reorders the free
   pool, but every price it produces is under **2.2 points for the season** (Spears, the largest),
   and 235 of 252 rows land under half a point. A sort key that moves rows worth 0.3 and 0.7 past
   each other is not a decision the page can act on.
2. **Read the page's tight-end prices as week-6 numbers against an empty slot.** Johnson 6.7,
   Strange 6.7, Freiermuth 6.3, Schultz 6.1 are almost entirely the LaPorta-plus-Hockenson bye.
   Against an average waiver tight end in that slot they are **2.0 / 1.9 / 1.3 / 1.2**. The choice
   among them is worth about a point; the decision that matters is whether to fill week 6 at all,
   and doc 315 already put that in week 5.
3. **The page's zeros are not zero, and they are not two points either.** Every free QB, RB and WR
   is 0.00 on the page. With absences seen they are worth 0.2 to 0.9 a season with the hole
   streamed, 1 to 3.6 with the hole left empty. Spears is the one row above 2.
4. **Do not read Daniel Jones's 7.2 as a case for a third quarterback.** That number exists only if
   an empty QB slot is charged at zero. Streamed, he is 0.5. Section 6's doctrine holds.
5. **One sentence for the sheet, not shipped tonight** because another session has
   `sheet_engine.py` open (docs 317 and 318 landed at 02:59 and 03:27): the week-6 tight-end fill
   should print both ways, *"6.7 against an empty slot, 1.2 against the average waiver tight end."*
   Two lines in `render()`. Mine, queued.

---

## 1. THE CLAIM IN ITS TESTABLE FORM, WRITTEN BEFORE THE RUN

> On Matt's 15 plus every free QB/RB/WR/TE in `WIRE_20260915.csv`, weeks 1-14, with every man's
> weekly availability (the candidate included) drawn at the position absence rates in
> `sheet_constants.json` and an empty slot filled at the streamer rate, the RANKING of free players
> by what they add to the starting nine differs from the page's byes-only ranking.
> **FALSIFIER, fixed first:** if the top five overall and the top man at every position are the
> same under both arms, the correction changes nothing the page acts on and B1 closes as a null.

**The falsifier did not fire.** The top man overall changes (Juwan Johnson to Tyjae Spears) and the
top man at three of four positions changes. So the claim survives as stated. **What the falsifier
did not ask, and should have, is by how much.** That is section 3, and it is the finding.

**POPULATION, restated (0.6):** the 280 free QB/RB/WR/TE rows in the newest wire file. **252 are
priced; 28 carry no ESPN projection in the 7 Sept pull and are NOT priced by this or by the page
(doc 277's rule: named, never dropped).** They are in `B1_unpriced.csv`: Tank Dell, Jaydon Blue,
Luke Musgrave, Justin Joly, Christian Kirk, Phil Mafah, Adam Randall, Nick Westbrook-Ikhine, Greg
Dortch, Dont'e Thornton Jr., Calvin Austin III, Trevor Etienne, Tyrell Shavers, CJ Daniels, Cedric
Tillman, Adam Prentice, Braxton Berrios, Jawhar Jordan, **Ricky Pearsall, Isaac Guerendo**, Josh
Williams, **James Conner, Devin Singletary, Trey Benson, Jerome Ford**, Stetson Bennett IV, Joe
Milton III, Mason Rudolph. **The wire file holds no D/ST and no kicker**, so neither position is
priced here. The candidate is priced at his own ESPN projection, which is the page's certain-fill
lane; the bet lane (screens at a hit rate) and the seat lane (a backup at the relief rate, doc 318)
are different objects and are not touched.

**RATES, declared [INHERITED] from the constants file, doc 297's population:** prior-season top-24
RB / top-24 WR / top-12 QB / top-12 TE read the following season, 2022-2025, n=318. QB 13.7% ·
RB 17.1% · WR 15.0% · TE 13.7% · D/ST 0 by construction · no kicker rate exists (deleted, doc 302),
so Pineiro plays every non-bye week in every arm. Streamer fills QB 16.65 · RB 5.43 · WR 6.54 ·
TE 5.53 · D/ST 5.99; no kicker fill exists either, so his bye-week hole is charged at zero in every
arm, exactly as the page does.

**THE FIVE ARMS, one draw shared across all of them and across every candidate:**

| arm | absences | empty slot | Washington behind Jeanty |
|---|---|---|---|
| **A** | none (byes only) | zero | own projection 3.68 |
| B | measured | zero | own projection |
| **C** | measured | streamed | own projection |
| D | measured | streamed | **12.13 in the weeks Jeanty is out** (the constants' relief rate) |
| E | doc 111's level (x1.66) | streamed | own projection |

**CONTROL (0.2): arm A through the simulator reproduces the page's own `price()` for all 252 rows to
within 0.049**, which is the page rounding each week's gain to a tenth. The harness is exercising
the page's object, `week_points()`, not an equivalent one.

---

## 2. WHAT THE PAGE PRINTS TODAY, AND WHAT THE BAR LOOKS LIKE WHEN IT CAN SEE AN ABSENCE

**On the page, 199 of 252 free rows are priced at exactly 0.00:** all 42 quarterbacks, all 51
running backs, all 98 receivers, and 8 of 61 tight ends. The 53 non-zero rows are tight ends and
their price is the week-6 hole: with LaPorta and Hockenson both on bye, the TE bar is 0.0 that week
and any tight end's whole projection counts.

**The bar, page against the mean absence-aware bar (arm C):**

| | wk 1-5 | wk 6 | wk 8 | wk 10 | wk 11 | wk 13 | wk 14 |
|---|---|---|---|---|---|---|---|
| QB page / C | 21.6 / 21.0 | 21.6 / 21.0 | 21.6 / 20.9 | **18.0 / 17.8** | 21.6 / 21.1 | 21.6 / 21.0 | 21.6 / 21.0 |
| RB page / C | 11.7 / 10.4 | 11.7 / 10.2 | 11.7 / 10.4 | 11.7 / 10.5 | **9.7 / 8.5** | **10.2 / 9.4** | 10.2 / 9.7 |
| WR page / C | 11.7 / 10.9 | 11.7 / 11.1 | 11.7 / 11.2 | 11.7 / 10.9 | **8.5 / 7.5** | 11.7 / 10.5 | **10.2 / 9.1** |
| TE page / C | 8.8 / 8.4 | **0.0 / 5.5** | 8.8 / 8.6 | 8.8 / 8.5 | 8.8 / 8.0 | 8.8 / 8.3 | 8.8 / 8.3 |

Full grid, all five arms, in `B1_bar_grid.csv`. **Two things are in that table.** The absence
model lowers the bar by about a point at every position in every ordinary week, which is what
turns the zeros into small positives. And streaming RAISES the week-6 tight-end bar from 0.0 to
5.5, which is what cuts the tight-end prices by three quarters. Doc 297 found the same two
corrections pushing opposite ways on the drop side; they do it on the add side too.

---

## 3. THE PRICES

**Top of the pool under the correction (arm C), with every arm beside it:**

| | pos | a game | **page (A)** | B | **C** | D | E |
|---|---|---|---|---|---|---|---|
| Tyjae Spears | RB | 7.62 | 0.00 | 2.87 | **2.16** | 1.38 | 5.97 |
| Juwan Johnson | TE | 6.74 | **6.74** | 7.76 | **1.96** | 1.84 | 4.24 |
| Brenton Strange | TE | 6.65 | 6.65 | 7.65 | 1.85 | 1.74 | 3.99 |
| Pat Freiermuth | TE | 6.25 | 6.25 | 7.08 | 1.34 | 1.24 | 3.27 |
| Dalton Schultz | TE | 6.06 | 6.06 | 6.96 | 1.16 | 1.07 | 3.00 |
| Samaje Perine | RB | 5.35 | 0.00 | 1.62 | 0.89 | 0.54 | 2.57 |
| Gunnar Helm | TE | 5.76 | 5.76 | 6.55 | 0.75 | 0.68 | 2.38 |
| Keaton Mitchell | RB | 4.93 | 0.00 | 1.41 | 0.70 | 0.44 | 2.28 |
| Kayshon Boutte | WR | 6.67 | 0.00 | 3.59 | 0.68 | 0.57 | 2.51 |
| Calvin Ridley | WR | 6.68 | 0.00 | 3.59 | 0.65 | 0.54 | 2.47 |
| Tre Tucker | WR | 6.69 | 0.00 | 3.63 | 0.63 | 0.51 | 2.41 |
| Brian Robinson Jr. | RB | 5.27 | 0.00 | 1.27 | 0.57 | 0.30 | 2.10 |
| Daniel Jones | QB | 17.97 | 0.00 | **7.23** | **0.53** | 0.53 | 1.05 |
| Kaelon Black | RB | 3.31 | 0.00 | 0.65 | 0.18 | 0.18 | 0.85 |

Paired standard errors on arm C are 0.01 to 0.05; the full table with every arm, both ranks and
the paired difference is `B1_free_pool_prices.csv` (252 rows).

**THE SCALE IS THE FINDING.** Under the correction the whole pool is worth **2.16 points at most**,
five rows reach 1.0, seventeen reach 0.5. At doc 111's harsher absence rates (arm E, a drafted
starter missing 2.98 weeks rather than 1.79) everything roughly doubles and the top is still under
6. The bare roster loses **71 points** a season to absences (1,536.6 to 1,465.2); streaming the
holes recovers 26 of them; and the best free man recovers two more. **Doc 259's sentence survives
the correction intact: the wire cannot upgrade a working slot, it can only fill a broken one, and
this roster's broken slots are the week-6 tight end and the week-11 receivers, both of which the
page already prices.**

**THE ORDER DOES CHANGE, and here is exactly how:**

- **195 of 252 rows are in at least one strict inversion** between the page's order and arm C's:
  some row the page put strictly above them is now strictly below, or the reverse. Nearly all of
  those inversions are a tight end worth 0.4 to 3 on the page (a week-6 number) dropping below a
  receiver or back worth 0.2 to 0.9 under the correction. `B1_order_changes.csv`.
- **153 rows leave zero.** 199 rows were at 0.00 on the page; 46 are under arm C (39 of them
  quarterbacks, because Hurts and Shough have different byes and two QBs must both be out before a
  third one plays).
- **Top five overall:** page Johnson · Strange · Freiermuth · Schultz · Helm; corrected **Spears** ·
  Johnson · Strange · Freiermuth · Schultz. **Top man by position:** QB Rodgers to **Jones** (both
  near zero), RB Ingold to **Spears** (a fullback at 0.00 to a back at 2.16), WR Adonai Mitchell to
  **Boutte** (0.00 to 0.68), TE Johnson to Johnson.

**Why Spears, and why the handcuff arm halves him.** He is priced at his own 7.62 a game. He
enters the nine only when three of Jeanty, Judkins, Dowdle and Dobbins are out at once, or two are
out in week 13 when Jeanty and Washington are on bye; those weeks are rare and in them he beats a
5.43 streamer by about two. In arm D, Washington scores 12.13 whenever Jeanty is out, so Spears
enters less often and his price falls to 1.38. **The sixth back is worth something now and it is
about a point and a half, which is doc 240's "about −5 net of the alternative" read from the
other side.**

**Why the tight ends fall from 6.7 to 2.** On the page a free tight end's week-6 gain is his whole
projection because the slot would be empty. Under arm C the slot is filled by a 5.53 streamer, so
his gain is what he clears over that: Johnson 1.2, Schultz 0.5. Absences give each of them back
about a point (LaPorta or Hockenson out, the free man starts). **For choosing WHICH tight end to
claim the order is unchanged: Johnson, Strange, Freiermuth, Schultz on the page and under C. For
whether the claim is worth its drop the page's number is the empty-slot number and doc 297's drop
costs are streamed numbers, and they should not be compared to each other.** Item 5 above is the
smallest change that stops that.

**Why Daniel Jones is 7.2 in arm B and 0.5 in arm C.** With the hole charged at zero, a third
quarterback covers Shough's week-8 bye when Hurts is out (13.7% × 18.0 = 2.5) and the weeks both
are out (about 2% of the season). With the hole streamed at 16.65 he covers the same weeks for 1.3
a week. **This is section 4.17's structure exactly: a spare quarterback is worth what he clears
over a streamer, not what he clears over nobody, and Matt streams.** Never three quarterbacks
holds, and it holds on the arithmetic, not only on the doctrine.

---

## 4. WHAT THIS DOES NOT LICENSE

- **No absence model in `price()`.** Doc 297 said teaching the sheet an absence model touches the
  bar grid, every price and the bet, and 4.18c's warning applies. This run is the measurement of
  what that would buy: a reordering of rows that are all worth under 2.2 points. **Not worth the
  blast radius.** The correction belongs in this doc and in the one sentence of item 5, not in
  the sort key.
- **The absence rates are position averages, not player forecasts** (4.25b, doc 204). A man ESPN
  lists OUT or on injured reserve is drawn at the same rate as a healthy one here; the wire's
  `status` column rides along in the output so nobody reads a 0.6 for a man on IR as a claim.
- **The candidate is drawn too.** Under the correction every free man misses 14-17% of his own
  weeks, which is about a sixth off every arm B-E price relative to a world where the free man is
  always available. It does not reorder within a position; it does shave RB rows a little more than
  QB rows.
- **The kicker is untouched by construction**, at both the absence rate and the streamer, because
  neither number has a source (doc 302). Pineiro's week-8 hole is charged at zero in every arm.
- **This is the certain-fill lane only.** The bet lane and the seat lane price a man at a hit rate
  or a relief rate, not at his projection, and doc 318 has just done the seat lane on Black.

---

## 5. OPEN

- **NOT YET RUN:** the same paired design on the BET lane, where a screened receiver is priced at
  the hit rate for 6.4 weeks. The absence correction should move those numbers by the same
  proportion as here, but the bar in the hit weeks is not the bar in an average week and that is
  not derivable from this run.
- **NOT YET RUN:** whether the RB drop costs in doc 297 and the RB add prices here net to the same
  swap value when both are streamed. They are on the same footing now (both arm C), which was the
  point; the swap table itself is a five-line join of the two CSVs and belongs on the page beside
  the drop table.
- **Item 5's sentence in `render()`**, once `sheet_engine.py` is not being edited by two sessions.

**Reproduce:** `Scripts\research\b1\b1_absence_bar.py`, stdlib plus `sheet_engine`; reads the
newest projection pull, `MY_ROSTER.csv`, the newest `WIRE_*.csv` and `sheet_constants.json` from
`Source\`. `B1_N=300` for a one-minute smoke test; the shipped run is N=3000, seed 20260916, log in
`run_b1_20260916.txt`. Outputs: `B1_free_pool_prices.csv`, `B1_order_changes.csv`,
`B1_unpriced.csv`, `B1_bar_grid.csv`, `B1_summary.json`.
