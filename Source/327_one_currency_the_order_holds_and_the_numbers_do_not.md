# 327 -- JOB 1: in one currency the order of the priority list holds, and the numbers on it do not

**16 September 2026.** *(First committed as 326 and renamed: another session had taken 326 for a different doc twenty-six minutes earlier, which section 0.2's folder-listing rule exists to catch and this session's listing was forty minutes stale. The 326 stub with this title on the drive is empty and can be deleted.)* JOB 1 from `REDTEAM_TASKING_PROMPT.md` section B: *the priority list ranks
three lanes in one column and they are not priced on the same scale.* Built the add-minus-drop
matrix on the live wire (`WIRE_20260916.csv`, the 18:35 sheet), every free player against every
man Matt owns, 1,500 paired draws, and re-sorted the list on it.

---

## 0. WHAT TO DO

1. **Nothing changes on the page this week. Schultz first, then the same four receivers.** In one
   currency the top five is the same five names; the only order change is Douglas and Vele
   swapping places, and the page prints them as equal (3.3 and 3.3), as does the correction
   (4.82 and 4.80 gross, 2.2 and 2.2 net).
2. **Read every number on the list as gross, and the cost line as a floor.** Netted against the
   cheapest man he can actually drop (Hockenson, 2.7 in this currency), Schultz is **+8.0**, the
   four receivers **+2.1 to +2.6**, and **every seat on the page is negative** (−0.6 to −0.8).
   The seats are worth 2.0 gross, the same as the page's 1.1 doubled by absences, and none of them
   clears a real drop. "It clears what it costs. Do it." holds for Schultz and for nobody below him.
3. **The cheapest drop is not 0.0.** Hockenson 2.7, Shough 3.1, Worthy 5.6, Washington 6.1 (his
   seat behind Jeanty, priced at the relief rate), Dobbins 8.6, Dowdle 12.3. The Browns defence is
   1.5, but that is a swap of defences, not a seat a bench body can take.
4. **Two swaps on the whole wire are positive at a man's own projection: Juwan Johnson for
   Hockenson (+0.3) and Strange for Hockenson (+0.03).** The other 276 free skill players are
   negative against every drop. What puts a man above zero on this page is the bet lane's hit
   rate, never his projection.
5. **Nothing to run, and no code change.** A 13-minute simulation cannot be the sort key on a page
   that rebuilds in seconds, and the sort it would produce is the sort the page has.

---

## 1. THE CLAIM, THE FALSIFIER, AND THE VERDICT

> **TESTABLE FORM, written before the run:** on the live wire, re-pricing all three lanes in one
> currency changes the TOP FIVE of the priority list.
> **FALSIFIER, fixed first:** if the top five, and the top man in each of the three lanes, are the
> same under both arms, the lane mixing costs nothing the page acts on and JOB 1 closes as a null.

**The falsifier fires in letter and not in substance, and the honest reading is a null.** The
top five are the same five names; the one order change inside them is a tie the page itself
prints as equal. The top man in the bet lane is Schultz both ways. The seat lane's top man goes
from Kaelon Black to Samaje Perine, which is a six-way tie at 1.1 on the page resolving to
2.06 against 2.05 gross (SE 0.05) under the correction: a coin landing. The fill lane has no row
on this week's list under the page (its three fills are calendar rows for weeks 6, 8 and 11) and
gains three under the correction, Jones, Spears and Ridley, at −0.1, −1.7 and −2.3 net: rows the
page is right to leave off. **The lane mixing does not change what the page tells him to do.**

**POPULATION, restated (0.6):** the 316 free players ESPN prices (the 7 Sept pull minus the twelve
rosters in `LEAGUE_ROSTERS.csv`), of whom 253 are on the wire file; the wire supplies the screens,
the week-1 workload, the touches and the status. Twenty rows are on the page: 3 fills, 8 bets
(2 pedigree screens, 1 first-round rookie, 5 workload), 9 free seats; the correction re-chooses
the fill lane per position and adds three fills the page prices at zero. Weeks 1 to 14, the
page's own horizon. Rates `[INHERITED]` from `sheet_constants.json`: absence (doc 297, n=318),
streamer (doc 92 and doc 12), hit size 12.71 for 6.4 weeks (doc 276), seat 12.13 for 3.02 weeks at
46% (doc 302). Matt's DO NOT rulings apply at selection in every arm, as on the page.

**THE TWO ARMS, one draw shared by every cell:**

| | page (P) | one currency (U) |
|---|---|---|
| availability | byes only | every man drawn at his position's absence rate, the candidate too |
| an empty slot | charged at zero | a waiver body at the streamer rate sits in the pool every week, so nobody below it ever starts and no slot is empty |
| a fill | `price()`: gain over the bar | the swap: season with him and without the man dropped, minus the season as it stands |
| a bet | odds × mean per-week gain at 12.71 × 6.4 weeks | the same, inside the swap and the draw; at his own projection in the miss world |
| a seat | 46% × mean per-week gain at 12.13 × 3.02 weeks | the same, inside the swap and the draw |
| the drop | a separate line; the cheapest man at 0.0 | every row is netted against every drop; the headline is the best skill drop |
| his own handcuff | the drop table prices Washington's seat (doc 317) | Washington scores 12.13 in any week Jeanty is out, on bye, or dropped |

**CONTROL (0.2): the page's list is reproduced exactly before anything is priced** (Schultz 11.1,
Washington 3.7, Vele 3.3, Douglas 3.3, Raymond 3.3; calendar Smack 8.5, Johnson 6.7, Chiefs 5.9),
and arm P through the simulator reproduces `price()` for all 316 rows to 0.05 and `drop_costs()`
for all 15 to 0.05, which is the page rounding each week's bar to a tenth.

---

## 2. THE TWO ORDERINGS, SIDE BY SIDE

This week's list. Gross is the one-currency value with no drop charged; net is against the best
skill drop, which is Hockenson for every row but one. Paired SE 0.03 to 0.06.

| # | page | | one currency | gross | **net** | best drop |
|---|---|---|---|---|---|---|
| 1 | Dalton Schultz | 11.1 | Dalton Schultz | 9.8 | **8.0** | Hockenson |
| 2 | Malik Washington | 3.7 | Malik Washington | 5.3 | **2.6** | Hockenson |
| 3 | Devaughn Vele | 3.3 | Caleb Douglas | 4.8 | **2.2** | Hockenson |
| 4 | Caleb Douglas | 3.3 | Devaughn Vele | 4.8 | **2.2** | Hockenson |
| 5 | Kalif Raymond | 3.3 | Kalif Raymond | 4.7 | **2.1** | Hockenson |
| 6 | Kendrick Bourne | 3.0 | Kendrick Bourne | 4.5 | 1.9 | Hockenson |
| 7 | Jalen McMillan | 2.9 | Jalen McMillan | 4.2 | 1.6 | Hockenson |
| 8 | Pat Bryant | 2.9 | Pat Bryant | 4.2 | 1.5 | Hockenson |
| 9 | Kaelon Black (seat) | 1.1 | Daniel Jones (fill) | 0.5 | −0.1 | Shough |
| 10 | Ty Johnson (seat) | 1.1 | Samaje Perine (seat) | 2.1 | −0.6 | Hockenson |
| 11 | Ollie Gordon II (seat) | 1.1 | Kaelon Black (seat) | 2.0 | −0.6 | Hockenson |
| 12 | Tank Bigsby (seat) | 1.1 | Ty Johnson (seat) | 2.0 | −0.6 | Hockenson |
| 13 | Emari Demercado (seat) | 1.1 | Ollie Gordon II (seat) | 2.0 | −0.6 | Hockenson |
| 14 | Samaje Perine (seat) | 1.1 | Tank Bigsby (seat) | 2.0 | −0.6 | Hockenson |

The calendar rows, which neither arm puts on this week's list: Juwan Johnson (week 6) 6.7 on the
page, **1.3 gross, +0.3 net for Hockenson**; Chiefs D/ST (week 11) 5.9 on the page, **0.0 gross,
−2.7 net**, because a defence that projects 5.9 a week is the streamer; Trey Smack (week 8) 8.5
both ways, and that row is not comparable: the constants carry no kicker streamer (doc 302), so his
week-8 hole is still charged at zero in every arm. Full table, every row, both ranks and all
fifteen per-drop values: `J1_orderings.csv`.

**LARGEST SINGLE ROW CHANGE: Chiefs D/ST, 5.9 to −2.7, −8.6 points.** Among this week's rows it is
Schultz, 11.1 to 8.0, −3.1: 1.3 of it is the absence draw and the streamer (his week-6 hole is
worth 1.2 against the average waiver tight end rather than the whole slot), and 1.8 is Hockenson's
drop net of the cover Schultz gives back.

**WHAT MOVES WHERE, and why the order survives it:**

- **The bet lane rises 1.5 gross and falls 1.1 net, evenly.** A receiver who hits at 12.7 a game
  clears a lower bar in the weeks Adams, Pickens or Nacua are out, so every receiver bet gains
  about 1.5 with absences drawn; the drop then takes 2.7 from all of them alike. Rows that move
  together do not reorder.
- **The seat lane doubles gross and goes negative net.** 1.1 becomes 2.0 for the same reason (the
  RB bar falls when a back is out), and 2.0 does not clear a 2.7 drop. This is doc 318's verdict
  on Black (+1.1 against Washington's +3.7) reached from the other side: **no seat on this page is
  worth the man it costs**, which is why the page's own sentence says the seat is the bet you make
  BEFORE the injury.
- **The fill lane is dead at a man's own projection.** Of 278 free skill players, two swaps are
  positive against any skill drop: Johnson for Hockenson +0.27, Strange for Hockenson +0.03. Every
  other cell of the matrix is negative. Doc 319's finding (nothing on the wire above 2.2 gross)
  becomes, once the drop is charged, nothing on the wire above zero. **A projection never puts a
  free man on this page; a hit rate does.**

---

## 3. THE DROP COSTS IN ONE CURRENCY

| | page (byes only, hole at zero) | one currency |
|---|---|---|
| Browns D/ST | 79.3 (not priced on the page) | **1.5** (a swap of defences, not a freed seat) |
| T.J. Hockenson | 0.0, "honest figure nearer 3" | **2.7** |
| Tyler Shough | 18.0 | **3.1** |
| Xavier Worthy | 8.5 | 5.6 |
| Mike Washington Jr. | 0.0, priced as the handcuff | 6.1 |
| J.K. Dobbins | 2.6 | 8.6 |
| Rico Dowdle | 4.3 | 12.3 |
| Sam LaPorta | 22.8 | 22.3 |
| Davante Adams | 21.7 | 28.8 |
| George Pickens | 30.9 | 31.2 |
| Ashton Jeanty | 60.0 | 31.8 (Washington inherits at 12.13) |
| Quinshon Judkins | 30.0 | 34.3 |
| Jalen Hurts | 64.1 | 43.2 |
| Puka Nacua | 93.3 | 90.0 |
| Eddy Pineiro | 118.7 | 118.7 (no kicker streamer exists; not priced) |

Doc 297's table on the 12 Sept roster had the same shape (Washington first, then the defence,
Shough, Hockenson, Worthy); this one prices Washington's seat, which moves him from cheapest to
fifth, and that is the whole reason Hockenson is the drop every row is netted against.

---

## 4. WHAT THIS DOES NOT LICENSE

- **Not a sort key.** The one-currency value needs 1,500 paired draws over 316 men and fifteen
  drops, 13 minutes here, and the page must rebuild in seconds. Its order is the page's order, so
  there is nothing to ship.
- **The seat lane's constants are still the soft spot** (ledger row 2, catalog B4): p_opens 0.46
  is applied flat and is under re-check. The negative net on every seat is robust to it only in
  the sense that a seat would need p_opens near 0.6 to clear Hockenson at these relief numbers.
- **Kickers are unpriced against a streamer** in every arm, so the matrix's largest "swaps" are
  kickers at 5.8 net; that is the deleted constant, not a finding.
- **Weeks 1 to 14 is the page's horizon and week 1 is played.** Every arm charges it identically,
  so it moves levels and not order; a weeks-2-to-14 run was not made.
- **The bet's hit is scaled, not placed.** As on the page, a hit is the season-average per-week
  gain at 12.71 times 6.4 weeks; which six weeks is not modelled, and neither is the miss world's
  drop of the man after the bet fails.

## 5. OPEN

- **NOT YET RUN:** JOB 2, the inheritor's share (section B of the tasking prompt). Next.
- **NOT YET RUN:** the same matrix on the week-3 wire, once the usage re-rank (doc 320) has moved
  the seat rows; the seat lane is where the constants are weakest and where this run changed the
  least.
- **OPEN:** whether a seat should be netted against the drop at all when the claim is a stash for
  a man who is not hurt yet; this run says no seat clears one, the page's sentence says the same,
  and the decision it serves is the order of three claims, which neither arm changes.

**Reproduce:** `Scripts\research\j1\j1_one_currency.py`, numpy plus `sheet_engine`; reads the
newest projection pull, `MY_ROSTER.csv`, `LEAGUE_ROSTERS.csv`, the newest `WIRE_*.csv`,
`inherit_2026.csv`, `cards_2026.csv`, `matt_todo.txt` and `sheet_constants.json` from `Source\`.
`J1_N=20` for a one-minute smoke test; the shipped run is N=1500, seed 20260916, log in
`run_j1_20260916.txt`. Outputs: `J1_orderings.csv` (every page row, both ranks, all fifteen
per-drop values), `J1_add_minus_drop_matrix.csv` (316 men × 15 drops, the fill lane),
`J1_drop_costs.csv`, `J1_summary.json`.
