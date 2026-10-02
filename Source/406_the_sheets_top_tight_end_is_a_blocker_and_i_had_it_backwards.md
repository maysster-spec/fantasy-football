# 406 — The sheet's top tight end is a blocker, and my afternoon recommendation was backwards

*23 Sept 2026, 19:45 ET, 7 hours before the Thursday 03:00 run. Matt: "my waivers need to be final TONIGHT.
What needs to be done to fix the week sheet now?" Answer: nothing tonight. Bypass it, do not rebuild it.*

---

## 1. THE ANSWER TO WHAT HE ASKED

**The week sheet does not get fixed tonight.** Patching `sheet_engine.py` or the wire builder seven hours before
his deadline is doc 144 exactly: three scripts shipped in one session, all three died on his machine, and he had to
debug my code. The page is not what he needs. **The numbers are**, and those can be computed here with no risk to
anything he runs.

The builder fix is real and it is mine, after the run.

---

## 2. WHAT THE VINTAGE CHECK WAS ACTUALLY SCREAMING ABOUT

`ff.bat` failed its vintage check this morning on 12 rows: the page prints preseason rates this season refutes. I
reported it as a page defect and **declined to compute the correction**, on the grounds that extrapolating two games
over fifteen weeks is §4.35's overreach.

**That was right about the extrapolation and wrong about the decision.** Ranking two candidates against each other
on two games of measured volume is not the same act as projecting a season, and I conflated them.

**Measured, 2026, 2 games each, half-PPR. Volume is the part that predicts:**

| tight end | pts/game | targets by week | snaps | the sheet's VOR |
|---|---|---|---|---|
| **Dalton Schultz** (HOU) | **12.8** | 8, then **14** | 66%, 68% | −36.8 (4th) |
| Pat Freiermuth (PIT) | 9.2 | 5, 5 | 73%, 66% | −33.9 (3rd) |
| Brenton Strange (JAX) | 6.0 | 3, 2 | 68%, 83% | −27.4 (2nd) |
| **Hunter Henry** (NE) | **4.8** | **3, 5** | **76%, 91%** | **−18.3 (1st)** |

**Hunter Henry is the sheet's number one and he is a blocker.** Ninety-one percent of snaps in week 2 and five
targets. He is on the field for everything and thrown to for nothing. **Schultz plays fewer snaps than Henry and
gets nearly three times the targets** (25.3% target share against 15.4%).

**The sheet has them in exactly the wrong order**, because the sheet is preseason projection and the vintage guard
had already flagged Schultz's specifically as understated by 6.7 a week.

---

## 3. WHAT I GOT WRONG AT 13:25 TODAY

Doc 404 recommended: **pass on Schultz, wait for Hunter Henry in week 5.** The reasoning was that Henry is the
better board player at −18.3 against −36.8 and nobody is chasing him, so waiting is cheap.

**Nobody is chasing Henry because Henry is a blocking tight end.** The flat ownership I read as "the quiet option is
still available" was the market correctly declining him. I treated an absence of demand as an opportunity when it
was information.

**And doc 404 named the test that would change my mind:** *"a recomputed VOR for Schultz on corrected inputs that
clears Henry's −18.3. The third is mine to run and it is NOT YET RUN."* I wrote that down as the falsifier, left it
unrun, and shipped the recommendation anyway. **It took Matt saying he needed to act tonight for me to run my own
stated test**, which is §0.5(a4) inverted: I named the stopping condition and then did not meet it.

---

## 4. THE DISCIPLINE THAT SURVIVED, AND THE ONE THAT ALMOST DID NOT

**Two traps were live in this data and both would have produced a confident wrong answer:**

**(a) The feed does not score passing or kicking (doc 375).** Jalen Hurts computes to 3.1 pts/game and Eddy Pineiro
to 0.0. Caught because those numbers are absurd for a starting QB and kicker. **Every measured rate in this doc is
RB, WR and TE only.**

**(b) Name substring matching pulled the wrong men.** "Henry" matched Derrick Henry, "Tucker" matched Tucker Kraft,
"Mitchell" matched Keaton Mitchell — and the concatenated output looked like one player with nine weekly rows.
§3's identity rule, caught by the rows not making sense. Redone on exact `name_key`.

**And one screen did its job.** **Mike Gesicki ranks first in the whole claimable pool at 16.3 pts/game — on ONE
game, at 33% snaps, with ownership FALLING (own_chg −4.35).** One target-light blowup by a part-time player.
Discarded. **Darren Waller, same shape:** 16.8 points in week 2 on three targets, which is touchdowns, and §4.5
says red-zone TD rate is noise. Discarded.

**The difference between Gesicki and Schultz is the whole method**: one is a points spike at low snaps with the
market walking away, the other is a stable two-thirds snap share with targets growing 8 to 14 and the market buying
hard (+22.99%, first of 283).

---

## 5. THE BOARD FOR TONIGHT

Claimable RB/WR/TE ranked on measured volume rather than projection, after discarding the one-game spikes:

| | player | pos | bye | pts/gm | tgt share | snaps | own chg |
|---|---|---|---|---|---|---|---|
| 1 | **Dalton Schultz** | TE | 8 | 12.8 | 25.3% | 67% | **+22.99** |
| 2 | **Tre Tucker** | WR | 13 | 12.0 | 19.0% | 65% | +8.30 |
| 3 | **Adonai Mitchell** | WR | 13 | 8.4 | 25.4% | 75% | +7.85 |
| 4 | Pat Freiermuth | TE | 9 | 9.2 | 13.5% | 70% | −0.38 |

**The top three are also the three the market is buying.** That is not independent confirmation — ownership change
and recent production measure nearly the same thing — but it does mean all three are likely contested, which
decides the order.

---

## 6. CAVEATS CARRIED

- **n = 2 games.** §4.35: in the claimable pool, the next week is a spike 4.3% of the time; the best signal we hold
  takes that to about one in ten. **None of this forecasts a week.** It ranks two men against each other on the
  volume they have actually earned.
- **The data is 11 hours old** (08:31 pull). Schultz was 44.4% owned and rising. He may already be gone.
- **Half-PPR, RB/WR/TE only**, doc 375.
- The sheet's `value` column is a season-long VOR on preseason projections and answers a different question. It is
  not wrong to exist; it is wrong to use for this.

---

## 7. HIS ACTUAL PENDING CLAIMS, SENT MID-TURN, AND THE ROSTER MATH BREAKS

He sent the ESPN Pending Moves screen. Three claims, processing the morning of Sep 24:

| priority | claim | drop |
|---|---|---|
| **1** | add **Dalton Schultz**, HOU TE, to bench | **none** |
| **2** | add **Tre Tucker**, LV WR, to bench | **none** |
| 3 | add **Bengals D/ST**, CIN, to bench | drop **Xavier Worthy**, KC WR |

**His order is right and it was set before this analysis existed.** Schultz first, Tucker second, which is exactly
the measured ranking in section 5, arrived at independently. Doc 396's rule is rank the contested man first, and
Schultz at +22.99 ownership is the most contested thing on the board.

**BUT TWO OF THE THREE CARRY NO DROP, AND THE ARITHMETIC DOES NOT CLOSE.**

Active roster is **14 of 15** (Nacua occupies the IR slot, which is separate from the fifteen), so there is **one**
free seat.

```
   14   start
 + 1    Schultz, no drop      -> 15   consumes the only free seat
 + 1    Tucker,  no drop      -> 16   OVER THE LIMIT
 + 1/-1 Bengals, drops Worthy -> 16   net zero, but already over
```

**Roster limit is 15. If all three win, one fails.** This is doc 393's measured failure mode precisely: among
claims that reached processing, **884 with a drop executed with ZERO roster-limit failures; 371 without produced 24
failures, and Matt owns 8 of those 24, all in 2025.** Every one of the 24 carried no drop.

**AND THERE IS A SECOND, LARGER RISK TONIGHT.** The free seat exists only because Nacua is parked and QUESTIONABLE.
By the rules sourced at v9.19, **if Nacua loses his injury designation entirely before 03:00, he is a healthy man in
the IR slot, and ESPN's own page says "the claim will not process" — all three fail, not one.** A drop on each claim
is what makes that irrelevant.

**THE FIX, one change per claim, nothing else:**

| claim | add a drop of | why |
|---|---|---|
| 1 Schultz | **J.K. Dobbins** (RB, 3.6 pts/gm 2026 2g, QUESTIONABLE, bye 10) | lowest measured scorer on the roster, and questionable |
| 2 Tucker | **Rico Dowdle** (RB, 4.2 pts/gm 2026 2g, QUESTIONABLE, bye 9) | second lowest, also questionable |

RB sits at **6 of 6, at the cap**, so both drops come from the only position with no room, and both land him at 4
backs against 2 starting slots plus FLEX. Pickens is the keeper and never moves. Washington is his stated 0%.
Worthy is already spoken for on claim 3.

**One thing flagged, not relitigated:** claim 3 spends **Xavier Worthy, 7.2 pts/gm measured**, on a second D/ST in
week 3, when his own calendar books the second defence for week 9. He has a stated reason (Cincinnati's run of
matchups) and it is his call with seven hours on the clock, but Worthy is the highest-scoring man being given up
in the batch and the plan of record disagrees with the timing.
