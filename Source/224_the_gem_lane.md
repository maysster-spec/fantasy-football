# 224 — The gem lane: he loses five of six contested claims, and that decides the whole scheme

**2026-09-08.** Matt, correcting doc 223's framing: *"remember, this is the late round gems to look
for and we are not focusing on players we can start today"* · *"think high value RB backups who
immediately have value if starter is hurt. Same for WR"* · *"one injury away guys they also call
it"*

**He is right and doc 223 was wrong in a specific, correctable way.** It built one lane — patch the
hole — and priced every free agent on what he is worth *this week*, which is the wrong instrument
for the thing that actually wins a season. Worse, its closing line said **"wait for the games."**
For the gem lane that is exactly backwards, and the measurement below is why.

---

## 1. THE LOAD-BEARING NEW MEASUREMENT — WHY THE GEM MUST BE CLAIMED BEFORE THE INJURY

**POPULATION:** every `Type == WAIVER` claim-add in `waiver_report_2024.csv` and
`waiver_report_2025.csv` — **903 claim-adds, 449 distinct player-weeks.** Matt resolved as
`The Poetry of Junkyard Juggers` (2025) and `Ja'Marracle Whip Juggernauts` (2024).
**BASELINE:** a claim is WON if its `Status == EXECUTED`. **UNIT: the player-week**, not the row —
see §2, because the row is the wrong unit and it nearly produced the wrong finding.

| | he chased | he won | |
|---|---|---|---|
| **players another team also claimed that week** | **63** | **10** | **16%** |
| **players only he claimed** | **91** | **51** | **56%** |

**Five of every six contested players go to somebody else.** `[TESTED]`

**The mechanism is in the settings, not in his behaviour.** `2026_League_Settings.txt` line 126:
*Waiver Order: Reset Each Week to Inverse Order of Standings.* A good team picks last, every week,
forever. **The week a starter goes down his backup is the most-claimed name in the league, and that
is precisely the week Matt is at the back of the line.**

> **THE RULE THIS EARNS: the only claims he reliably wins are the ones nobody else has made yet.
> So the gem is claimed BEFORE the job opens, or it is not claimed at all.**

**And this is the first measured argument in the project FOR his archetype rather than around it.**
§4.13's ladder already said the title comes from breakouts (0 → 4.7%, 1 → 14.4%, 2 → 26.8%,
3 → 54.6%) and §4.13c noted that 8 of 15 late booms were backs who inherited a backfield. What was
missing was why you cannot simply buy that player when it happens. Now it is measured: you cannot,
because you lose the auction 5 times in 6.

## 2. THE §0.5(a2) SAVE — THE FIRST CUT MEASURED THE WRONG UNIT

Counting **rows**, Matt executes 6.7% of contested claims against a league 28.4%, and 24.1% of
uncontested against 49.0%. Read naively that says he is bad at waivers in every condition.
**He is not. He submits a median of TEN claims per week against a league median of TWO** (32
team-weeks vs 206), and **181 of his 362 claim rows are `PENDING`** — the status of a queued claim
that never had to run because something earlier in his own list landed.

**Measured at the right unit — did he land at least one claim in a week he tried — he is at 31 of
32, or 97%, against a league 90%.** The long conditional list is a strength and the row-level
number was an artifact of it. **Report the machinery as working; point it somewhere better.**

## 3. THE STASH LIST, AND WHY RB ≠ WR

**RB.** Built from `depth_map.csv`: every free agent at depth 2 whose `job_ceil` is large, ranked by
what the job pays rather than by his own value. Top of it: **Brian Robinson Jr. behind Bijan
Robinson's 315-point Atlanta job** (and he carries 2 of 3 back signals), then Jordan James (SF 302),
DJ Giddens (IND 291), Ty Johnson (BUF 262), Ollie Gordon II (MIA 261), Tank Bigsby (PHI 252).
**All twelve are unrostered.**

**WR — AND THE FIRST BUILD OF THIS WAS WRONG.** `depth_map.py` is an RB instrument: its `job_ceil`
and `job` columns are computed from the team's *backfield*, so the WR rows came out reading
"Greg Dortch, DET, lead back job worth 332" — that 332 is **Gibbs**. Caught before it shipped;
§0.2, a test must exercise the right object. The receiver list is rebuilt from the 09-03 projection
pull directly: for each team, WR2–WR4 against their own WR1's projection.

**And the honest calibration, which is the part he should read:**
- **A back who inherits a backfield roughly doubles his weekly output — about 12.0 against 6.1.**
  A step change.
- **A receiver whose rival is off the field gains about 3.0 points of target share — 17.0% → 20.0%**
  (doc 189 M1, n=205 player-seasons, p<0.0001). An increment.

**So "same for WR" is the one part of his framing the measurements push back on.** The play exists
at receiver and it is roughly a third of the size. **Spend the stash spots on backs.**

## 4. WHAT CHANGED ON THE PAGE

`Source\THE_WEEKLY_WIRE.html` rebuilt:
- the routine now names **two lanes** — the hole (a body for Sunday) and the gem (one injury away) —
  and says to keep them apart;
- **"nothing here is worth a claim before Week 1 · wait for the games" is REMOVED.** It was correct
  for lane 1 and actively wrong for lane 2;
- the stash tables for RB and WR, ranked by what the job pays;
- the contested-claim measurement, in plain English, as the reason for the timing;
- a note closing the one inconsistency a reader would catch: **Tutu Atwell heads the receiver table
  only because Nacua is the biggest name ahead of anyone on it, and his own column reads 26 points.**
  He is the illustration of why that lane is weak, not a claim to make.

## 5. OPEN

- **`wire.py` still has to point at both lanes.** Today it ranks the pool on our value, which is
  lane 1's instrument. It should also emit the depth-2 stash list. Not built yet.
- **`depth_map.py` has no receiver version** and its RB columns are silently wrong when read for a
  WR. Nothing guards that. A `pos == 'RB'` assertion inside any consumer would have caught it.
- §4.19's paradox is still open and this doc does not touch it: he is 1.05 weeks earlier to the
  player than the field at RB and it does not convert.
