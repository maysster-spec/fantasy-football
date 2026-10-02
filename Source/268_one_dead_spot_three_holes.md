# 268 — One dead roster spot, three empty weeks

2026-09-10, week 1. Matt: *"set aside the moves that I recommended and provide to me the waiver
moves and roster moves that you calculate are most in my favor."* So this is computed from his
roster and the free pool, not argued from the docs.

**Testable form, stated before running (§0.5a2).** A roster move is worth what it adds to the nine
he actually starts across weeks 1–14, and nothing else. **Population:** his 15, plus the 339-player
free pool from the Sept 8 snapshot, plus the 18 defences and 22 kickers nobody drafted. **Baseline:**
his current roster's best legal nine every week — 1,865.8 points. A bye is a **zero in a required
slot**, not a missing row; that is the whole point. Weekly rate = season projection ÷ 14, doc 259's
convention. **His roster is full at 15, so every add is priced net of its drop.** Script:
`Scripts\research\moves.py`.

**What this cannot see, stated up front (§0.6):** projections do not price missed weeks, so nothing
below is an injury model; and a projection has no opinion about a job changing hands, which is what
§4.27 and §4.30 are for. Both qualifications are used where they bind.

---

## The roster, and the three weeks it breaks

| | | |
|---|---|---|
| QB | Hurts (bye 10), Shough (8) | |
| RB | Jeanty (13), Judkins (11), Dowdle (9), Dobbins (10), Spears (9), Washington Jr. (13) | **at the cap** |
| WR | Nacua (11), Adams (11), Worthy (5), Pickens (14) | |
| TE | LaPorta (6) | **one body** |
| D/ST | Browns (11) | |
| K | Pineiro (8) | |

Three weeks put a **zero** in a slot that must be filled:

| week | slot | who is off | the week scores |
|---|---|---|---|
| **6** | tight end | LaPorta | 126.6 |
| **8** | kicker | Pineiro (and Shough) | 126.2 |
| **11** | defence | Nacua, Judkins, Adams **and** the Browns | 114.3 |

Nothing else in the fourteen weeks is short a body. Week 11 is the worst week of his season and the
defence is the only part of it he can fix — the three receivers are covered by Worthy and Pickens
and the flex.

## Two of his fifteen contribute nothing, and one of them is free to move

Cost of dropping each man, measured as points off the season's starting nine:

| player | round | drop costs | 2027 keeper cost |
|---|---|---|---|
| **Tyjae Spears** | 9 | **0.00** | §4.18b measures a round-9+ keeper at or below zero |
| **Mike Washington Jr.** | 11 | **0.00** | same |
| J.K. Dobbins | 8 | 2.47 | inside the 5–8 audition band |
| Rico Dowdle | 7 | 4.52 | inside the 5–8 audition band |
| Xavier Worthy | 10 | 10.37 | — |
| Tyler Shough | 12 | 21.87 | — |

**Spears never enters the lineup in any of the fourteen weeks**, which reproduces doc 240 on the live
roster rather than on the preseason board, and Matt's own read — *"holding Spears on my bench was of
negative value"* — a second time.

**Washington measures the same 0.00 and should still be held**, and the reason is doc 240's rule, not
this table: a bench back earns his spot by the job he would inherit and the fragility of the man
ahead, never by his own projection. Washington sits behind a **247** job whose holder is flagged;
Spears sat behind a **171** job whose holder played 33 of 34 games. Same number, opposite verdicts.
He is also the only insurance §4.19 says cannot be bought later — four of five backs Matt adds never
give him a startable stretch.

**So one spot is free. Exactly one.**

## Nothing on the wire upgrades a working slot — measured, not asserted

Best free player at each position, added in Spears' place:

| pos | best available | what it adds |
|---|---|---|
| K | Trey Smack (GB) | **+10.31**, entirely in week 8 |
| TE | Brenton Strange (JAX) | **+8.07**, entirely in week 6 |
| D/ST | Chiefs | +7.22, entirely in week 11 |
| QB | Daniel Jones (IND) | **+0.00** |
| WR | Tre Tucker (LV) | **+0.00** |
| RB | Samaje Perine (CIN) | **+0.00** |

`[TESTED — 339 free players × every legal drop]` Every single one of the gains is a **hole being
filled**, and every skill-position add is worth exactly nothing. That is doc 259's conclusion
reproduced on the live roster: the wire cannot upgrade a working slot, it can only fill a broken one.

It also settles the second quarterback. **Daniel Jones is 0.05 points a game behind Shough** and
Shough's entire contribution is one start, week 10, worth 21.87. Doc 259 flagged that as `[OPEN]`
because projections do not price missed weeks; that is still true, and it is exactly why the spot
should not be spent — **holding Shough costs nothing and insures the 2.98 weeks §4.17b says a
starting quarterback misses.** Do not trade this spot for a fifth of a point.

## The one spot covers all three holes, because they do not overlap

Weeks 6, 8 and 11 are three different weeks. One roster spot, rotated, fills all of them:

| when | do this | worth |
|---|---|---|
| week 5 | claim a startable tight end for week 6 | **+8.07** |
| week 7 | drop him, claim a kicker for week 8 | **+10.31** |
| week 9 | drop him, claim a second defence and **hold it** | see below |

Measured on the board model, the first two alone take the season from **1,865.8 to 1,884.2, +18.38**,
and dropping Spears costs **nothing in any week** on the way.

## The second defence, restricted to what is actually free

Doc 267 measured the ceiling — the best pair of all 32. The realistic version is: which of the
**18 defences nobody drafted** best complements the one he holds? Same shrunk model (opponent
generosity × 0.325, own quality × 0.269), and this time the baseline is **Cleveland alone**, not the
best defence in the league.

| window | Cleveland alone | best free partner | gain | median free partner |
|---|---|---|---|---|
| weeks 2–14 | 70.24 (5.40/wk) | **+ Chicago** 79.66 | **+9.42 (+0.72/wk)** | +5.07 |
| weeks 9–14 | 30.12 (5.02/wk) | **+ Buffalo** 37.12 | **+7.00 (+1.17/wk)** | +4.69 |
| weeks 15–17 | 15.81 (5.27/wk) | **+ Indianapolis** 17.88 | +2.07 (+0.69/wk) | +0.44 |

And week 11 on its own, where the slot is empty: **Chicago 6.20**, San Francisco 6.07, Buffalo 5.61.

**Chicago is the answer if he picks one name**, because it is the best partner over the whole
regular season and the best single body in the week he has a hole. Buffalo is 0.07 a week better
over weeks 9–14 alone, which is not a difference. **The playoff partner is different** — Chicago is
the *worst* free partner for weeks 15–17 (+0.00) and Indianapolis the best — so the partner gets
swapped once, in week 14.

**Read the median column before getting attached to a name.** Most of the gain is having a second
defence at all; choosing the right one is worth about two points over six weeks. That is the honest
size, and it is smaller than doc 267's ceiling number implies.

## When to claim, which is the part with a real measurement behind it

**Not this week.** §4.31 measured every executed add in this league 2022–2025: a **week-1** claim
returns a startable stretch **9.4%** of the time against week 2's **34.6%**, Fisher p=0.010. A week-1
claim bets on a depth chart; a week-2 claim bets on a snap count. And nothing free improves any week
between now and week 5, so there is nothing this week that patience costs.

The scope note in §4.31 (v9.1) is what lets the rest of the plan ignore that finding: **filling an
empty slot is a different object** — there the alternative is zero, not a replacement-level body —
and **a forward claim on a schedule** bets on a fixture list that has been fixed since May. Weeks 5,
7 and 9 above are both of those, not speculation.

## The plan, in order

1. **This week: no claim.** The worst-hitting week of the season, and nothing on offer moves a slot.
2. **After week 1's games: drop Spears.** Costs zero in every week and his keeper option is at or
   below zero. Use the spot on the best receiver week 1's snap counts support — `pedigree_2026.csv`'s
   screen has **Ricky Pearsall** as the standing favourite (first-round pick, 3-of-3 on §4.30, 39.4%).
3. **Week 5:** if that receiver has not produced, the spot becomes a tight end for week 6. **+8.07**
4. **Week 7:** the spot becomes a kicker for week 8. **+10.31**
5. **Week 9:** the spot becomes Chicago's defence and stays. **+6.6 to +7.0** through week 14.
6. **Week 14:** swap the partner to Indianapolis for the playoffs. **+2.07**
7. **Hold Washington, hold Shough.** Both measure 0.00 and 21.87 respectively, and both are
   insurance against the one thing this model cannot see.

**Total measured value of one dead roster spot: about +25 to +27 points of starting lineup**, against
a season baseline of 1,866. Roughly a point and a half a week, taken entirely out of weeks that
currently score a zero.

## What is deliberately not on this list

- **No trade.** §4.33: 3.5 completed league-wide a season, and all four offers Matt has ever received
  came from one manager. The levers needing no counterparty are the whole of it.
- **No skill-position claim for value.** Every one measures +0.00 (table above).
- **No drop of Dowdle or Dobbins** to make room. They cost 4.52 and 2.47, they are inside the
  rounds-5–8 audition band §6 protects, and nothing free replaces them.

## Open, with the inputs named

- **Ownership is a Sept 8 snapshot.** `py wire.py` is what confirms Pearsall and Chicago are still
  free. It is on `matt_todo.txt`.
- **Not yet run:** the injury half. This model prices byes, not absences — §4.18c's point about
  `_lineup()`, one level up. The nflverse weekly injury release would let the same rotation be
  re-scored against a real absence rate.
- **Open:** whether the week-11 defence should be claimed in week 9 or week 10. Term 5 of §4.32 —
  losing a claim usually delays a player rather than removing him — argues for the later date, and it
  has never been measured.
