# 225 — The gem lane, priced: he is right about the timing and wrong about the position

**2026-09-08.** Matt: *"if it helps you find patterns you can look at hit rate in my league for
waiver pickups. I had a few alone last year, which may be higher than the norm"* · *"I'm also able
to score them earlier than other managers"*

**Both suggestions were run. One of them resolves §4.19's two-year-old paradox and the other kills
the position half of his own archetype.**

---

## 0. THE TESTABLE FORMS, STATED BEFORE THE RUNS (§0.5(a2))

1. *Among executed waiver adds in this league, does a player only ONE team claimed produce as well
   as a player several teams claimed?*
2. *Among the players he got alone, does being early on one the league later chased predict a hit?*

**POPULATION:** every `Type == WAIVER` claim-add, `waiver_report_2022..2025`, **1,585 claim-adds →
312 executed adds that can be scored.** **BASELINE — state it every time: rest-of-season points per
game from the week AFTER the move through week 14, scored under §2 from nflverse weekly, against
the position's measured replacement (QB 20.09 · RB 9.92 · WR 9.62 · TE 8.25).** Contested = 2+
teams claimed the same player in the same week.

---

## 1. THE CROWD IS RIGHT ABOUT WHO IS GOOD — AND IT DOES NOT MATTER

| | n | hit rate | ppg |
|---|---|---|---|
| **contested** (2+ teams wanted him) | 122 | **32.0%** | 9.49 |
| **uncontested** (one team wanted him) | 190 | **22.6%** | 8.83 |

**His hunch that his lone pickups beat the norm is WRONG in the direction he guessed.** The players
several managers chase are meaningfully better. `[TESTED]`

**And it still does not change the instruction, because getting them is the binding constraint.**
Doc 224 measured the access side: **he wins 16% of contested players and 56% of the ones nobody
else claimed.** Multiply:

| | P(he gets him) × P(hit) = **per attempt** |
|---|---|
| **contested** | 0.16 × 0.320 = **5.1%** |
| **uncontested** | 0.56 × 0.226 = **12.7%** |

**The lane he can actually win pays two and a half times more per attempt even though its players
are worse.** That is the arithmetic that vindicates his framing, and the reason is access, not
quality.

## 2. THE POSITION HALF OF THE ARCHETYPE IS THE PART THAT DIES

Per attempt, by position — same two multipliers:

| | contested | **uncontested** |
|---|---|---|
| **TE** | 4.0% | **19.6%** |
| **QB** | 8.0% | **16.8%** |
| **WR** | 5.2% | **11.8%** |
| **RB** | 4.6% | **5.3%** |

**Running back is a wash between the lanes and the worst square on the table.** Uncontested RBs hit
**9.4%** (n=53) against contested RBs at 28.6% (n=49) — the biggest quality gap of any position, and
the one where being alone hurts most. **The one-injury-away back is the emotionally satisfying play
and the lowest-paying one measured here.** `[TESTED]`

**This is doc 12's waiver table for a third time** (RB adds hit 22%, QB 62% on its own bar) and
§4.19's for a second (his own RB adds 20.5%, four of five never startable). **Three independent
measurements, three different baselines, one conclusion: the wire does not produce running backs.**

## 3. THE TAIL, BECAUSE "STARTABLE" IS NOT WHAT HE ASKED ABOUT (§4.13b)

A hit above is *could I start him*. The gem lane is about a league-winner, so the bar was raised:

| bar | contested | uncontested | per attempt |
|---|---|---|---|
| ≥ replacement | 32.0% | 22.6% | 5.1% vs **12.7%** |
| **≥ 1.5× replacement** (a real weekly starter) | 6.6% | 3.7% | 1.0% vs **2.1%** |
| **≥ 2.0× replacement** (a league-winner) | 0.8% | 1.1% | 0.1% vs 0.6% |

**Uncontested wins at every bar.** But read the last row honestly: **across four seasons and 312
scored pickups, FOUR became a 2× player.** Two contested, two uncontested. **Nothing can be
concluded from four events, and the honest headline is the base rate: a waiver pickup becomes a
league-winner in this league about 1% of the time.** `[TESTED, and UNDERPOWERED at the tail]`

**§4.13's breakout ladder is not a counter-example — it measured DRAFTED players.** The wire is a
different and much thinner population.

## 4. §4.19'S PARADOX IS RESOLVED, AND THE ANSWER IS "ACCESS, NOT QUALITY"

§4.19 (doc 111) found he is **1.05 weeks ahead of the field at RB** and **first to the player 57%
vs 42%** — and that his three-week lift is **+0.39** against the league's **+0.74**. Doc 205 ruled
out the drop side. The remaining candidates were *wrong names* or *too early on the right ones*.

**Tested today, third look:** among uncontested executed adds, split by whether any other team came
for the same player in a LATER week —

| | n | hit rate |
|---|---|---|
| nobody ever chased him | 102 | **23.5%** |
| somebody chased him later | 88 | **21.6%** |
| *RB only, nobody chased* | 25 | 16.0% |
| *RB only, chased later* | 28 | **3.6%** |

**Being early on a player the league eventually wanted predicts nothing, and at running back it
points the wrong way.** `[TESTED — NULL]`

> **THE RESOLUTION: his earliness is real and it buys ACCESS, not QUALITY.** Being first is
> identical to being uncontested, and uncontested is how he wins 56% instead of 16%. It is the
> entire reason the gem lane works for him. **It is not evidence that he identifies better players
> early, and three measurements now say he does not.** Both halves matter and they have been
> conflated since doc 111.

## 5. WHAT THE SCHEME SHOULD SAY NOW (§0.5(b) — surfaced, not silently applied)

**His preference:** stash one-injury-away backs.
**The measurement:** that square pays 5.3% per attempt; uncontested TE pays 19.6% and QB 16.8%.
**Recommendation, his call:**
- **Keep the RB stash — but ONE spot, not three.** The list exists, the jobs are real (Brian
  Robinson behind 315 points), and doc 224's access finding means the spot has to be taken early or
  not at all. What the data denies is *volume* there, not the play.
- **Point the other bench spots at the lane that pays.** Uncontested TE and QB are the best two
  squares on the table and they are the two positions §6's doctrine already says to buy on waivers
  rather than draft.
- **Do not chase the popular name after an injury.** 16% get rate, and the roster spot is spent
  waiting either way.

## 6. OPEN

- **The 2× bar is 4 events.** It cannot be resolved on this league. The NFL-wide version could be
  built on the §1.1 registry and is a post-season item.
- **Matt's own contested cut is n=4** (2 hits). His personal split is unmeasurable; everything
  personal above rests on §4.19's n=88.
- `wire.py` still emits lane 1 only — the depth-2 stash list is not in it yet.
- `depth_map.py` still has no receiver version and its RB columns read as garbage for a WR row with
  no guard (doc 224 §5).
