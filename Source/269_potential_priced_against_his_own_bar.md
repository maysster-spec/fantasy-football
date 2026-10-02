# 269 — Potential, priced against his own lineup bar

2026-09-10. Matt: *"did you factor in potential value to your waiver/roster recommendations?"*

**No. Doc 268 priced every add on this season's projection alone, which is exactly why every skill
claim in it came out at +0.00.** The potential screens were reported in doc 267 and printed as
wire.py's lane 3, and then not carried into the ranking — two lanes, one of which never met the
arithmetic. He caught it in one line. This doc puts them in the same currency.

---

## What he already did, read off the files rather than asked

`WIRE_20260910.csv` (278 free, down from 339 on Monday) shows **Tyjae Spears back in the free pool**,
and his ESPN screen shows him **WA (Fri)**. So the drop is done and the roster is **14 with one open
spot**. All four pedigree names are still unowned: **Omar Cooper Jr. 5.2% rostered · Ricky Pearsall
2.6% · Pat Bryant 1.9% · Jalen McMillan 33.9%.**

**And a mechanic nobody in this project had written down: FA is not WA.** On his free-agent screen
only **Spears (clears Friday)** and **Baker Mayfield (Saturday)** carry a waiver period. Everything
this plan wants — Boswell, the Chiefs, Daniel Jones, McMillan, Tre Tucker, Jerry Jeudy — is marked
**FA**, which means the green plus adds him immediately, **no claim, no priority spent**.

**This qualifies §4.32.** Its whole cost side — *"the resource is one turn at his real priority,
twice a week"* — applies only to a player inside his waiver period. A player who has cleared costs
**nothing but the roster spot**. §4.31's week-1 finding is untouched, because that is about the
player's outcome and not the price, but the reason to ration claims disappears for anyone marked FA.
**Do not treat an FA add as though it spends something.**

---

## The measurement he asked for

**Testable form, stated before running (§0.5a2):** the value of a potential add is
**E[ points he adds to the nine Matt actually starts ]**, taken over the measured distribution of
what players clearing that screen went on to score — not over the hit rate, and **not against
replacement, but against Matt's own lineup bar**.

**Populations.** For §4.30's screen: WR seasons 2021–2024, NFL years 1–3, under 9.62 half-PPR per
game, 4+ games, who played 4+ games again the next season; outcome is next season's half-PPR per
game. **n=43 in the three-of-three cell, 143 below it.** For §4.28's: every WR taken in NFL round 1,
2021–2025, with 4+ games as a rookie; outcome is his own rookie rate. **n=26.** Games played come
from nflverse snap counts; receiving only, so a receiver's rushing and return work is not counted
and both are slight under-reads. Script: `Scripts\research\potential.py`, `moves.py`.

| screen | n | mean next-year ppg | median | max | reached 9.62 |
|---|---|---|---|---|---|
| **3 of 3** | 43 | **7.34** | 6.58 | 14.51 | **30.2%** |
| under 3 | 143 | 3.54 | — | — | 2.8% |
| **NFL round-1 rookie** | 26 | **8.62** | 8.83 | 15.51 | **38.5%** |

`[TESTED]` The 30.2% reproduces §4.30's 39.4% in shape and not in level — different games-played
source and a receiving-only outcome — so **quote 4.30's own number for the screen and these for the
distribution**, and do not treat the two as one measurement.

## And then the number that decides it: his bar is 14.2, not 9.62

Bisecting the weekly rate at which a new receiver first changes his best legal nine:

| week | 1–10 | **11** | 12–13 | **14** |
|---|---|---|---|---|
| rate a new WR must beat | **14.2** | **10.4** | 14.2 | **12.4** |

**A receiver who becomes "startable" by the league's measure does not crack Matt's lineup.** Nacua
21.1, Pickens 14.2, Adams 14.2 and Dowdle 12.2 in the flex sit above the bar the whole way. So the
39% screen mostly converts into nothing *for him*, and what it does convert lives in the tail and in
week 11, when Nacua and Adams are both off.

Averaged over the whole measured distribution — the misses included:

| candidate | screen | **expected points, weeks 1–14** | chance it adds anything | p90 |
|---|---|---|---|---|
| **Omar Cooper Jr.** (NYJ, bye 13) | first-round rookie | **+1.53** | 23% | +3.0 |
| Ricky Pearsall (SF, bye 8) | 3 of 3 | **+0.58** | 16% | +1.0 |
| Pat Bryant (DEN, bye 10) | 3 of 3 | +0.58 | 16% | +1.0 |
| Jalen McMillan (TB, bye 10) | 3 of 3 | +0.58 | 16% | +1.0 |
| — | — | — | — | — |
| Brenton Strange, week-6 tight end | fills an empty slot | **+8.07** | certain | — |
| Chris Boswell, week-8 kicker | fills an empty slot | **+10.20** | certain | — |

**So the answer is: potential is real, it is measurable, and on this roster it is worth about a tenth
of a hole fill.** Not because the screens are weak — a 39% conversion rate is the strongest
receiver signal in the project — but because **his receiving corps is good enough that a merely
startable player never plays.** The same screen on a thin roster would be worth many times this.

**Cooper Jr. is the pick of the four**, and by the right reason: a first-round rookie's distribution
sits a point above the three-of-three distribution at every quantile, and his week-13 bye is the one
that does not stack on Nacua, Adams or Judkins.

## The half that makes potential worth holding anyway

The bar of 14.2 exists only while his receivers play. Re-running with one of them gone for the
season:

| scenario | new bar | Pearsall | Cooper Jr. |
|---|---|---|---|
| everyone healthy | 14.2 | +0.58 | +1.53 |
| Adams out | 12.4 | +2.08 | +3.97 |
| Nacua out | 12.4 | +2.08 | +3.97 |
| **Pickens out** | 12.4 | **+8.77** | **+11.67** |

**Pickens is the one whose absence is different, and the reason is a collision, not his rate.** Nacua
and Adams are both on bye in week 11. If Pickens is out, that week has **no second receiver at all**
— an empty starting slot, which is the one situation where any body is worth full value (§4.31's
v9.1 scope note). **A held receiver is insurance priced at zero today and at +9 to +12 in the one
branch that leaves a hole.**

## Two things that bound this, and one of them is decisive

1. **No waiver or free-agent pickup can ever be a keeper.** §2.1(a): *"Trade and free-agency
   acquisitions are ineligible regardless of draft round."* So the 2027 half of potential — the part
   §4.18 and §4.26(a) argue about — **does not exist for anything added off the wire.** Everything
   above is a 2026-only asset, and that is the whole of it. This is why the numbers are small and
   why they are also complete.
2. **The model prices byes, not absences.** The scenario table is the bound, not a forecast.

## Mike Washington Jr.

Matt: *"0% chance i drop him."* **Agreed, and that was the recommendation** — doc 268's table listed
his drop cost at 0.00 alongside Spears' and then said in terms to keep him. The reason is his own
rule, doc 240's: a bench back earns his spot by the job he would inherit and the fragility of the
man ahead, never by his own projection. Washington sits behind a **247** job whose holder is
flagged. Spears sat behind a **171** job whose holder had missed one game in two years. **He is the
one potential asset on the roster that this doc's arithmetic cannot price**, because §4.27's trigger
is a two-week cameo and a projection has no opinion about one.

## What shipped

- `Scripts\wire.py` — **defect found in its own first live output.** `WIRE_20260910.csv` carried a
  Python dict printed into a `ped` column, because the CSV writer takes its fieldnames from
  `rows[0].keys()` and yesterday's patch hung the whole pedigree row on `r['ped']`. Moved to a side
  map. The `screen` column is correct and stays.
- `Scripts\wire.py` — now writes **`Source\MY_ROSTER.csv`** every run. "What is on his roster right
  now" was a question no artifact on the drive could answer, so it was being asked in chat instead,
  which is the §0.4 failure. It refuses to write an empty file and says so.
- `Scripts\research\potential.py` — rebuilds both distributions from play-by-play and snap counts.
- `Scripts\check_kit.py` — wire.py re-pinned.

## Open, with inputs named

- **Not yet run:** the absence model. Everything above prices byes only. nflverse's weekly injury
  release plus §4.17b's measured 2.98 missed weeks would turn the scenario table into an expectation.
- **Not yet run:** the same potential pricing at running back, where §4.27's two gates are the screen
  and Washington Jr. is the live row. It needs a per-game relief rate the depth map does not carry.
- **Open:** `trade_report_2022..2025` now exist — 25 rows in 2025 alone. **§4.33's "every trade claim
  in this project is unmeasured" is closed as of today** and the reports have not yet been read.
