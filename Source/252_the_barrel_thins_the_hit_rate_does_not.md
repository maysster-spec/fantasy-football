# 252 — THE BARREL DOES THIN, AND THE HIT RATE DOES NOT MOVE. THE ONE WEEK THAT IS DIFFERENT IS WEEK 1, AND IT IS WORSE.

*2026-09-09. Matt: "how high is the hit rate on the following weeks, 3 and 4? Or really any time of FF*
*season... perhaps so many injured players there is more scarcity of available quality players because*
*by then we are at the bottom of the barrel and fewer players to choose from? Idk, that's an open*
*question from me."*

---

## 0. WHAT TO DO

1. **CLAIM IN WEEK 2, NOT WEEK 1.** Week-1 claims hit **9.4%**; week-2 claims hit **34.6%**
   (p=0.010). It is the only week-level difference in the whole season.
2. **After week 1 the season is FLAT.** Weeks 2–4 = 25.3%, weeks 5–14 = 23.1%, p=0.59.
   Week 3 is 15.4% and week 4 is 26.0% — that spread is noise on n≈50 a week.
3. **His mechanism is HALF right and it is the half nobody would have guessed.** The pool really
   does thin — usable free players fall from ~15 in weeks 1–5 to ~10 in weeks 9–13 — **but the hit
   rate does not fall with it.** Scarcity is real and it does not cost you anything.
4. **A number that must be qualified: doc 250's "claim often and claim early."** Still true — the
   claim is free. **"Early" now means WEEK 2, not week 1**, and the reason is information, not cost.
5. **What to send me: the PFF receiving Premium Stat export, not another transcript.** Named
   exactly in §6. The web has no hit-rate-by-week measurement to replicate — I looked.

---

## 1. THE TESTABLE FORM, STATED BEFORE THE RUN (§0.5(a2))

> **POPULATION:** every EXECUTED waiver or free-agent ADD in this league, 2022–2025, all twelve
> managers, that matched a QB/RB/WR/TE with a real weekly line — **718 adds in weeks 1–14.**
> **BASELINE:** a "hit" is the added player's points per game from the add week onward reaching his
> position's measured replacement rate — **QB 20.09 · RB 9.92 · WR 9.62 · TE 8.25** (doc 12).
> **OUTCOME, two forms:** **A** = rest of season through week 14. **B** = the **next four weeks
> only**, which removes the shrinking-window confound in A.
> **DIRECTION (his):** the hit rate FALLS as the season goes on, because the pool is picked over.

**§0.6 — THE POPULATION AND WHAT IT EXCLUDES, WITH ITS SIZE.** 1,230 executed adds. **248 of them
(20.2%) are D/ST**, and another 151 are kickers or players who never recorded a snap. **The 718
rows below are 58% of all adds, and D/ST — the most-churned position in this league — is not in
them.** That is doc 228's rule applied to its own dataset; the D/ST version of this table is
NOT YET RUN and needs a weekly D/ST scoring table under our settings, which §2 does not record.

## 2. THE ANSWER: FLAT

| add week | adds | A: rest of season | B: next four weeks | mean 4-week ppg |
|---|---|---|---|---|
| **1** | 32 | **12.5%** | **9.4%** | 7.01 |
| **2** | 52 | 26.9% | **34.6%** | 9.55 |
| 3 | 52 | 17.3% | 15.4% | 7.85 |
| 4 | 50 | 24.0% | 26.0% | 9.19 |
| 5 | 66 | 15.2% | 22.7% | 7.90 |
| 6 | 62 | 21.0% | 22.6% | 7.80 |
| 7 | 59 | 18.6% | 25.4% | 10.27 |
| 8 | 60 | 25.0% | 30.0% | 9.89 |
| 9 | 57 | 19.3% | 21.1% | 8.43 |
| 10 | 44 | 15.9% | 18.2% | 8.50 |
| 11 | 55 | 20.0% | 20.0% | 8.12 |
| 12 | 50 | 22.0% | 18.0% | 8.33 |
| 13 | 37 | 24.3% | 24.3% | 8.19 |
| 14 | 42 | 33.3% | 28.6% | 9.10 |

**rho(week, hit) = +0.045 on A (permutation p=0.234) and +0.003 on B (p=0.926).** `[TESTED, n=718]`
**Weeks 2–4 22.7% versus weeks 9–14 22.1%, p=0.905.** **His direction is not there, and the point
estimate is very slightly the other way.**

**By position, and this is where the flatness holds up best:**

| | weeks 1–4 | weeks 5–8 | weeks 9–14 | all |
|---|---|---|---|---|
| RB | 19% (62) | 14% (87) | 18% (90) | **17%** |
| WR | 20% (61) | 21% (81) | 19% (78) | **20%** |
| TE | 21% (38) | 27% (41) | 28% (64) | **26%** |
| QB | 28% (25) | 24% (38) | 26% (53) | **26%** |

Every one of the twelve cells is inside its position's own season average. **The RB row is the
§4.19 result restated: the back you add is a one-in-six shot in September and a one-in-six shot in
December.**

## 3. WEEK 1 IS THE EXCEPTION, AND IT IS THE WORST WEEK

**Week 1: 9.4% on the four-week bar. Week 2: 34.6%. Fisher p=0.010** — the only week-level result
in this study that clears significance. Against every other week pooled, week 1 is 9.4% vs 23.6%,
p=0.083. `[TESTED, n=32 vs 686]`

**THE MECHANISM IS INFORMATION, AND OUR OWN TIMESTAMPS SHOW IT.** The 32 week-1 adds were executed
between the Thursday opener and the Sunday night game — most of them **before or during** the first
slate. They are bets on a depth chart. The week-2 claim is a bet on a **snap count**, and doc 235
already measured that the thing that predicts is the workload, not the box score.

**AND THAT QUALIFIES MY OWN POSTURE (§0.2).** Doc 250 said *"claim often and claim early; failure
is free."* The free part is untouched — no FAAB, no season limit, order resets weekly on standings,
so the only cost is the drop. **But "early" was doing work it had not earned. One week of patience
is measured at roughly three times the hit rate, and it costs a roster spot for seven days.**

## 4. HIS MECHANISM, MEASURED DIRECTLY — THE POOL, NOT THE ADDS

The hit rate is the wrong instrument for "is the barrel emptier." So the pool was rebuilt: **every
player rostered anywhere in the league, week by week, from the draft plus all 1,230 executed
adds and drops in date order.** A player is **usable** in week W if he averages his position's
replacement rate over weeks W–W+3. Averaged over the four seasons:

| week | rostered | **usable AND free** | of which RB | WR | TE | QB | best free player |
|---|---|---|---|---|---|---|---|
| 1 | 178 | **13.8** | 2.0 | 6.8 | 2.0 | 3.0 | 24.1 |
| 2 | 184 | **16.8** | 3.5 | 6.8 | 2.5 | 4.0 | 25.0 |
| 4 | 197 | 14.8 | 3.5 | 5.0 | 4.2 | 2.0 | 24.4 |
| 5 | 200 | 15.5 | 2.8 | 5.8 | 4.0 | 3.0 | 25.3 |
| 7 | 209 | 12.0 | **0.8** | 5.8 | 3.5 | 2.0 | 25.3 |
| 9 | 214 | **10.0** | **0.8** | 3.8 | 3.2 | 2.2 | 22.9 |
| 11 | 221 | **10.0** | 2.2 | 3.2 | 3.0 | 1.5 | 22.4 |
| 12 | 222 | **9.8** | 3.2 | 2.5 | 3.0 | 1.0 | 19.8 |
| 14 | 225 | 11.5 | 2.5 | 3.8 | 2.5 | 2.8 | 25.0 |

**HE IS RIGHT ABOUT THE BARREL: the usable free pool falls by about a third**, from 15–17 in the
first five weeks to 10 from week 9 on, while the rostered population grows from 178 to 225.
`[TESTED, n=56 season-weeks]`
**AND THE RUNNING BACK IS THE EXTREME CASE: 3.5 usable free backs in week 2, 0.8 in weeks 7 and 9.**
In half the league-weeks after week 6 there was **not one** startable back on the wire. That is
§4.19's "the wire cannot patch an RB hole" from the supply side, and it is a much starker number
than the hit rate ever showed.
**BUT THE CEILING DOES NOT FALL.** The best free player is worth 22–26 points a game in almost
every week of the year. **There are fewer of them; they are not worse.**

**SO THE TWO HALVES RESOLVE LIKE THIS, AND IT IS THE interesting part:** the pool shrinks by a third
and the hit rate does not move, which means **the players who remain are easier to identify.** In
week 2 there are seventeen usable free players and nobody knows which; in week 10 there are ten and
everybody can see the one who just inherited a job. **Scarcity and legibility move in opposite
directions and they cancel.** `[TESTED for both halves; the cancellation is the INFERENCE, not a
separate measurement — it is the only account consistent with both tables, and it is not itself
tested.]`

## 5. WHAT THE OUTSIDE HAS, DATED (B7)

**There is no published hit-rate-by-week measurement.** Six searches across the analytics outlets
returned weekly advice columns, not studies. Two dated sources bear on it:

- **Fantasy Footballers, published 13 Sep 2021, last modified 15 Aug 2025** — nflfastR, half-PPR,
  2015 onward. A "week-1 wonder" is a player drafted after pick 97 who scored 12+ in week 1:
  **58% beat their ADP the rest of the way, but only 13% finished top-12 at the position and 39%
  top-24.** `[SOURCED]` Different population from ours — theirs is week-1 *performers*, ours is
  week-1 *claims* — but **their 13% and our 9.4% are the same shape**, and their object is what our
  week-2 bucket actually buys.
- **4for4, "The Ultimate Guide to Waiver Wire & FAAB Strategy," published 28 Aug 2023**, quoting
  Pat Fitzmaurice on four years of waiver articles: recommended spend of **1% of budget on QB, 8.1%
  RB, 9.1% WR, 5.7% TE.** `[SOURCED]` **Not applicable here — it is a FAAB allocation and we have no
  FAAB** (doc 250). Its 2026 successor, **published 28 Aug 2026**, contains no numbers at all.

**So on this question we are not replicating anybody. The measurement above appears to be the only
one of its kind, and it is on our own league's rows.**

## 6. WHAT I WANT FROM HIM, AND IT IS NOT A TRANSCRIPT

The transcript lane paid (doc 249 replicated Ray Garvin's data points). **On this question there is
nothing published to replicate, so the marginal value is in PFF, which he has.** Two items, both
currently BLOCKED under §0.5(a4) with the input named:

1. **PFF Premium Stats → Receiving, season export, 2021–2025.** The two fields nothing else has
   are **slot rate** (slot snaps ÷ total snaps) and **targets per route run**. 4for4 (8 July 2024)
   measures slot rate as the single most stable receiver trait at **0.75**, ahead of targets per
   game at 0.70 — and §4.28's list of Matt's indicators is null on everything we *could* compute.
   **This is the last untested item on that list.**
2. **PFF Premium Stats → Rushing, season export, 2021–2025** — for **elusive rating** and **yards
   after contact per attempt**, which is the one thing §4.6 flags as underweighted by ESPN and the
   project has never had a source for.

CSV export is on the PFF+ / PFF Pro tiers. If it exports per-season with a player id column, both
tests are a day's work; if it is screen-only, screenshots of the sortable table are enough for the
top 150 at each position.

## 7. WHAT IS STILL OPEN

- **D/ST hit rate by week — NOT YET RUN**, 248 adds, 20.2% of the wire, blocked on a weekly D/ST
  scoring table under our settings (§2 does not record the D/ST scoring rules at all).
- **Whether being first to the claim raises the landed value** — `waiver_report_*.csv` holds the
  order. NOT YET RUN, carried from doc 227.
- **The cancellation in §4 is an inference, not a test.** The testable form would be: among the
  free-and-usable pool in week W, what share were actually added within two weeks? Rising over the
  season is the legibility story. NOT YET RUN.
- **Week 1's 9.4% rests on 32 adds.** Direction is clear and the p is 0.010 against week 2, but a
  fifth season would matter more here than anywhere else in this doc.
