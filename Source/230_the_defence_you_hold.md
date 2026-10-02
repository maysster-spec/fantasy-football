# 230 — THE DEFENCE YOU HOLD, AND THE CLAIMS IT BUYS BACK

*2026-09-08. Matt, correcting my "plainly" answer: "the point was to find soft schedule of
matchups for a defence… we want to hold a d/st for weeks and not be at the mercy of waivers week
to week where I could land with a bad defense facing a high powered offense… at that point my
waiver position is even less favorable… no one tries to pick up a bad defense to face a good
offense on waivers. it's just not a thing and so you're not going to see it if you're only running
numbers across our league history. you won't see the worst possible outcomes. but they are there."*

*He is right that the measurement was incomplete. He is right about which direction it fails in.
He is wrong about the specific mechanism, and the correction makes his case stronger, not weaker.*

---

## 1. THE LIST

1. **STOP STREAMING THE DEFENCE WEEK TO WEEK. Buy one with a soft run ahead and hold it.**
   That is his instruction and it is now measured from three directions.
2. **THE REASON IS THE BAD END, NOT THE GOOD END.** Chasing the best weekly matchup is worth about
   a point. **Avoiding the worst one is worth more:** in the hardest fifth of draws more than a
   quarter of defence-weeks score BELOW ZERO and 37% score under two points. In the easiest fifth
   that is 9% and 17%.
3. **AND IT BUYS BACK YOUR PRIORITY IN ROUGHLY TEN DIFFERENT WEEKS.** *(Precision, added
   2026-09-08: the order RESETS every week to inverse standings, so a claim does not cost you
   anything next week. The cost is WITHIN the week's run — the defence claim you win first is the
   reason the back you wanted goes to somebody else that same run.)* **41% of Matt's claims went to a
   defence in 2024 AND in 2025** — 13 of 32, then 12 of 29 — against a league average of 3.4.
   Only the first winning claim in a run comes at his real priority, so every one of those pushed
   him behind the field for the running back the wire cannot replace (§4.19).
4. **A NUMBER THAT MUST NOT BE QUOTED THE WAY I QUOTED IT:** "at defence take the schedule, pick
   whichever free defence draws the worst offence" frames a WEEKLY choice. That is the behaviour
   that costs him the claims. The instruction is **hold**, not **shop**.
5. **SHIPPED, nothing to run:** the weekly sheet now prints *the defence to HOLD* — free defences
   ranked by the whole four-week run ahead, softest first, with his own defence included so he can
   see whether to keep it. Four negative controls run first.
6. Nothing else to run.

---

## 2. WHAT I GOT RIGHT, WHAT I GOT WRONG, AND WHICH HALF HE CAUGHT

**His truncation worry does not bite the number I quoted, and I should say so plainly.** Doc 212's
**POPULATION was 2,718 team-weeks, 2021–2025 — every defence, every week, started or not.** The
bad cells nobody would ever start ARE in it. So "the spread you measured is truncated because
nobody starts a bad defence" is not what went wrong.

**What went wrong is that I measured the GRID and he is asking about the POOL.** Every number in
doc 212 answers *how much does the matchup move a defence's score*. None of them answers *what can
Matt actually obtain, when, and at what cost to the rest of his roster*. Those are different
objects (§0.5(a2)), and the second one is the one that decides the strategy. Two costs were
missing entirely:

- **The reachable set is not the grid.** He gets whichever defences are unowned when his turn
  comes. Late in the order, shopping weekly, that is the leftovers.
- **Streaming spends the one resource he cannot buy back.** Nothing in any defence calculation in
  this project has ever charged for a waiver claim.

**And one thing he named is genuinely not measurable here, which I am recording rather than
working around:** *"I risk getting in one of those bad scenarios that could have been avoided and
I'm just not sure you can measure that because it didn't happen and I was able to avoid it."*
Correct. The weeks he swerved leave no trace. What CAN be measured is the size of the hole he was
swerving, and §3 below measures exactly that.

---

## 3. THE TAIL IS ASYMMETRIC — THIS IS THE FINDING

**POPULATION: 1,664 defence-weeks, 2022–2025, weeks 1–14, every team every week whether anyone
started it or not. PREDICTOR, preseason-knowable: the opponent's PRIOR-season points scored per
game. BASELINE: the grid's own mean, 5.15 points a week, sd 6.43.**

| draw | n | mean | median | 10th percentile | share of weeks BELOW ZERO |
|---|---|---|---|---|---|
| **1 hardest** | 377 | **3.52** | 3.0 | **−4.0** | **27%** |
| 2 | 325 | 5.25 | 5.0 | −3.0 | 18% |
| 3 | 338 | 5.07 | 4.0 | −2.0 | 18% |
| 4 | 312 | 5.73 | 5.0 | −2.0 | 18% |
| **5 easiest** | 312 | **6.53** | 6.0 | **0.0** | **9%** |

**Easiest minus hardest = +3.01 points a week, MWU p<0.0001.** `[TESTED]`

**The halves are not equal.** Against the grid mean, the easiest fifth is **+1.38** and the hardest
fifth is **−1.63**. A start under two points — a wasted roster slot — happens **37%** of the time on
a hard draw and **17%** on an easy one. **The thing worth buying is the absence of the disaster.**

## 4. HOLDING A RUN

Best forecastable k-week window per defence per season, then held through it:

| window | top 1 defence per season | top 3 | top 5 | top 8 | grid mean |
|---|---|---|---|---|---|
| 3 weeks | +6.25 | +6.06 | +6.18 | +5.96 | 5.15 |
| 4 weeks | +5.38 | +5.48 | +4.81 | +4.84 | 5.15 |
| 5 weeks | +6.20 | +6.15 | +5.92 | +4.90 | 5.15 |

**About +1 point a week at three and five weeks; four weeks is weaker and noisier.**
`[SUGGESTIVE, NOT RESOLVED — 4 to 32 stretches per cell.]` The direction is consistent across two
of the three window lengths and all four selection depths, and it agrees with §3, which is the
result carrying the weight. **Do not quote the +1; quote §3's 27%-versus-9%.**

## 5. THE CLAIM COST — MEASURED, AND IT IS THE LARGEST NUMBER HERE

**POPULATION: 2,201 transaction rows, 2022–2025, executed adds only, split by ESPN's own
WAIVER / FREEAGENT type.**

- **D/ST is 26.9% of every waiver claim made in this league** — 165 of 614. Roughly **3.4 defence
  claims per team-season**.
- **Matt is at 41%, twice running: 13 of 32 claims in 2024, 12 of 29 in 2025.** His 2025 defence
  adds land in weeks 1, 2, 2, 3, 4, 5, 6, 8, 8, 8, 8, 11, 12, 12, 13, 14, 15 — that is not
  streaming occasionally, that is shopping the position nearly every week of the season.
- Against his own corrected waiver model: only the first successful claim in a run comes at his
  real priority, and a winning record already starts him near the back. **He is spending four in
  ten of his claims, at the front of his own queue, on the one position where holding works — and
  paying for it at running back, where §4.19 says four of five of his adds never produce a
  startable stretch.**

`[TESTED]` **This is the strongest argument for his position and neither of us had counted it.**

---

## 6. WHAT IS STILL NOT MEASURED

1. **The reachable pool.** What was actually unowned each week, and how much worse the best free
   defence was than the best defence. **Matt asked whether the transaction log could rebuild weekly
   rosters. It can in principle and it cannot with the file we hold — measured, not assumed.**
   Draft roster + every executed `ADD x | DROP y` in date order rebuilds cleanly on the drop side
   (only 0–4 drops per season name a player the rebuild did not think was owned, out of ~200). But
   **7 to 9 executed adds per team per season carry NO paired drop**, and the balancing drops are
   simply not in the file — every row begins with ADD, none contains TRADE. A roster is 15 plus 3
   IR; the rebuild reaches 27–32 by week 14, which is impossible.
   **Matt then supplied the mechanism I had missed: "when a player is moved to IR before waivers."**
   An IR move frees a slot, so an add against it legitimately has no drop. **Tested: real, and not
   sufficient.** IR holds three men at most, but rosters breach 18 by a median of week 6–8 and peak
   at **29 to 38** — eleven to twenty over legal. So both things are true: some unpaired adds are
   IR moves, and drops are genuinely missing from the file as well.
   **He was also right that roster shape varies by manager — one of twelve teams drafted only
   thirteen players in three of the four seasons**, so a size control cannot assume fifteen.
   **The fix is one command: `py waivers.py` reads ESPN's own `mTransactions2` for standalone drops
   and trades, and `py lineups.py` (new) reads the weekly lineup view, which returns each team's
   roster, slot and points directly — making the rebuild unnecessary rather than merely fixed.**
   `[OPEN — one command away]`
2. **The counterfactual he named** — the bad weeks he avoided by acting early. Structurally
   unobservable. §3 prices the hole; it cannot price his swerving. `[NOT MEASURABLE HERE]`
3. **Whether holding beats streaming *for him specifically*.** §3 and §5 both point that way, and
   §4 is underpowered. One season of the new sheet would settle it.

## 7. SHIPPED

- **`Scripts\wire.py`** gains `dst_runs()` and a *defence to HOLD* block: free defences ranked by
  the mean scoring of their next four opponents, softest first, his own defence included so he can
  judge whether to keep it. **Four negative controls run before the feature: no schedule, no team
  file, no week number, and a schedule that runs out. All four print why the box is missing rather
  than rendering an empty one** (§0.2).
- The page's own wording was rewritten. It used to say to take the schedule and not agonise over
  which defence — a weekly instruction. It now says to hold one through a run, and gives the
  27%-versus-9% as the reason.
