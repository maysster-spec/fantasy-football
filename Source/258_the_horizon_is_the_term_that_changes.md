# 258 — LATE SEASON CHANGES ONE TERM, NOT THE CALCULATION. HIS D/ST INSTINCT IS THE STRONGEST-MEASURED THING IN THE WHOLE WAIVER FILE.

*2026-09-09. Matt: "logic changes for late season as well, since I need to plan weeks in advance.*
*That is where I do need to handcuff my own players, and fill gaps elsewhere, and find favorable*
*D/ST. We know I'm not going to win all my waiver bids so we need to calculate early and often."*

**Confirmed at D/ST, confirmed at the handcuff, and MEASURED AGAINST HIM at the skill positions.**

---

## 0. WHAT TO DO

1. **Doc 257's term 1 changes from "this week" to "the weeks he is actually needed."** That is the
   whole late-season difference. The other five terms are unchanged.
2. **"Find favorable D/ST" is the best-supported instinct in this file — 108%.** At defence the
   matchup is worth MORE than the difference between the units. At every other position it is not.
3. **AND THE HORIZON IS WHERE THE MONEY IS: the best-to-worst D/ST spread is 3.56 points over ONE
   week and 11.72 over FOUR** (doc 212). Planning weeks ahead triples the signal. That is his point,
   already measured, and neither of us connected it to the wire until now.
4. **"Plan my skill-position playoff schedule" is measured near-noise** — doc 10: the entire
   32-team weeks-15–17 spread is **≤5.5 points**, and that doc says in terms *"it is not a
   playoff-planning tool."* **One exception, and it contradicts doc 10:** §4.26(b)'s tight end.
   Named in §4 below, not resolved.
5. **This does NOT collide with §4.31's week-1 penalty.** A forward claim on a SCHEDULE bets on
   something known. Week 1 was bad because it bets on a depth chart. Different object.

---

## 1. D/ST — HIS LANE, AND THE ONE THE MODEL HAS NEVER SEEN

| measurement | number | source |
|---|---|---|
| streaming a defence beats the median defence | **55.9% of the time, +1.92 a start** (n=227) | doc 228 `[TESTED]` |
| matchup swing vs the spread between the defences themselves | **2.22 against 2.06 — 108%** | doc 227 §3b `[TESTED]` |
| opponent identity's share of a D/ST week | **15.6%**, against the defence's own **9.4%** | doc 212 `[TESTED]` |
| best-to-worst spread, **one week** | 3.56 | doc 212 |
| best-to-worst spread, **four weeks** | **11.72** | doc 212 |

> **AT DEFENCE, TAKE THE SCHEDULE. AT EVERY OTHER POSITION, TAKE THE PLAYER.** (doc 227 §3b, verbatim.)

**And this is the blind spot, restated because §0.6 requires it: D/ST is 248 of 1,230 executed adds
(20.2%) and it is EXCLUDED from every waiver hit-rate measurement in the project, including doc
252's by-week table.** Doc 228 opened the position for the first time. **So the lane he is naming as
where the model helps most is exactly the lane the model has never scored.**

## 2. THE HANDCUFF — CONFIRMED, WITH A GATE

"Handcuff my own players" is on §0.5(a4)'s confirmed list at **+7.30**. §4.27 supplies the applied
form and it is not "own the backup" — it is **the man ahead's fragility × the backup's ability to
produce in a two-week window** (11.2 half-PPR a game, the median relief rate across 40 measured
events). Doc 251 §6 already runs that gate on the live wire.
**And §4.27's counter-intuitive half matters more late than early: a SHORT absence flips a job more
often than a long one** (3+ weeks out measures −10.6 pp against one or two, p=0.108). The
one-week cameo is the danger, which is an argument for holding the handcuff BEFORE the injury, not
after — exactly his "calculate early and often."

## 3. WHY "EARLY AND OFTEN" SURVIVES §4.31

§4.31 says week-1 claims hit 9.4% against week 2's 34.6%. **That is not a general argument against
claiming early. It is an argument against betting on a DEPTH CHART before any football.** A claim
filed in week 12 for a week-16 defensive matchup is betting on the **schedule**, which was fixed in
May and cannot surprise anyone. **Same calendar direction, opposite epistemics.** Doc 253 made this
distinction for the start/sit case; it applies here too and for the same reason.

## 4. WHERE THE MEASUREMENTS DISAGREE — NAMED, NOT RESOLVED

- **Doc 10 (18 Aug 2026):** playoff-window SOS, shrunk by measured stickiness — full 32-team
  weeks-15–17 spread **QB 5.1 · RB 5.5 · WR 4.8 · TE 3.2**, one sd ≈ 1.3. Verdict in its own words:
  ***"It is also not a playoff-planning tool."***
- **§4.26(b) / doc 229:** the TE weeks-15–17 draw is **+3.39 per sd, p=0.031**, quartiles monotone,
  **softest minus hardest ≈ +9 points**.
**Those two cannot both be the right size at tight end.** Different methods — doc 10 shrinks toward
the mean and reports expected points; §4.26 regresses the beat on raw prior-season points allowed
and does not shrink. **`[OPEN]` — and it should be settled before any playoff-planning tool is
built on either.**

## 5. THE TERM LIST, AS IT NOW STANDS (doc 257 §2, amended)

| # | term | late-season change |
|---|---|---|
| 1 | what he adds to the nine Matt starts | **→ over the weeks he is NEEDED**, not this week. Byes are known; the playoff window is weeks 15–17 |
| 2 | the next-best body at that position | unchanged — and doc 252 says the free pool is a third thinner by week 9 |
| 3 | the weeks he is needed | **this is now term 1's index, not a separate row** |
| 4 | P(a team ahead also files) | unchanged, NOT YET RUN, bounded by doc 224 |
| 5 | recovery if lost — run 2, then free agency | unchanged, and it is why "early and often" costs little |
| 6 | the drop | unchanged |

**NOT YET RUN:** the D/ST version of everything — hit rate by week, contestedness, and a
forward-slate ranker. **The inputs exist** (`dst_weekly_2021_2025.csv`, `team_2025.csv`, the 2026
schedule) and doc 228 already built the scoring. That is the next real build, and it is bigger than
the skill-position model because it is the position where the schedule beats the player.

---

## 6. AND THE TRADE HALF IS NOT OPEN — IT SHIPPED, WITH HIS OWN NUMBERS

*Added after his follow-up: "maybe I do need to trade based on favorable match ups and the bye week*
*strategy we talked about before."*

**The bye-week trade is `bye_plan()` in `wire.py`, live since doc 233.** It rebuilds from his live
roster every week and raises the box when the next expensive week is five weeks out or nearer.
**BASELINE: his best legal nine with everyone available = 117.1 a week. COST = that minus the best
legal nine with the week's bye men removed.**

| week | who is off | raw points off | **actual lineup cost** |
|---|---|---|---|
| **11** | Nacua, Judkins, Adams, Browns D/ST | 50.3 | **28.1** |
| **6** | LaPorta | 10.7 | **10.7** |
| 13 | Jeanty, M. Washington | 22.1 | 6.0 |
| 10 | Hurts, Dobbins | 37.9 | 4.3 |
| 9 | Dowdle, Spears | 21.5 | 0.5 |
| 5 · 8 · 14 | Worthy · Shough, Pineiro · Pickens | — | **0.0** |

**Season cost if nothing is done: 49.6 points.** `[TESTED — arithmetic on the shipped projections]`

**THREE THINGS THAT ARE LIVE RIGHT NOW:**
1. **The byes to ASK for in a trade are 5, 8, 9 and 14** — they cost him nothing, so a man with one
   of those byes is free to him and expensive to the other guy.
2. **The week-11 trade has a deadline of about WEEK 9** (doc 235). A trade made in week 11 fixes
   nothing, and week 11 is the 28-point week.
3. **HOCKENSON DOES NOT FIX WEEK 6.** Minnesota and Detroit share the week-6 bye. He named the
   shared bye himself and accepted it for a different reason — LaPorta's hip — and that reason is
   sound. **But week 6 is his second-worst week of the season, it costs the full 10.7 because the
   tight end slot empties outright, and it arrives FIRST.** The add covers the injury risk and
   leaves the bye hole exactly where it was. **`[OPEN — the week-6 TE hole is unfixed]`**

**AND THE SELLING RULE IS ALREADY MEASURED — doc 235, and it is not "wait for a pop":**
a pop carries forward **+1.73 a week** over the next three, but **+2.65 when the touches jumped and
+0.20 when they did not.** **Sell the touchdown pop, keep the workload pop.** Check carries +
targets, never the box score. RB pops carry hardest (+2.36), so the back who pops is the worst man
to sell and the receiver who pops is the best.

**WHAT IS STILL OPEN ON TRADES:** doc 227 §1.G — *"trading into a league that does not trade"* —
because §2 records only **three league-wide trades a season observed**. The tool tells him what to
offer and to whom; **nothing in this project has tested how to get an offer ACCEPTED here**, and on
a three-a-season base rate that is the binding constraint, not the analysis.
