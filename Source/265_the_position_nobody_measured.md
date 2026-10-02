# 265 — D/ST off the wire: the flat answer is clean, the size is not, and my own falsifier caught me twice

> **BANNER, 29 Sept 2026 (doc 441). THE 5.99 BELOW IS RETRACTED: it was measured on `dst_weekly_2021_2025.csv` as `build_dst.py` then wrote it, which emitted a row only when the defence recorded an event, so 142 team-weeks scored by the points-allowed band alone (mean minus 3.88) were missing (2,576 rows of 2,718). On every team-week, with the blocked-kick and fumble-lost terms section 2 scores, D/ST12 is 5.51 a week (5.57 without the two terms) and a D/ST week is 4.99, sd 6.59, not 5.46 sd 6.28. The builder is fixed, the file rebuilt, `sheet_constants.json` and `dst_k_supply.py` carry 5.51, and the directive's DO-NOT-QUOTE table carries 5.99 and 5.46 from v9.34. The flat-supply conclusion of this doc stands on the full file (13.6 / 13.4 units above the bar early and late); its baseline does not.**

**Date:** 2026-09-09. Matt, from the gym: *"please run what you can now."* This is the item
§4.31 has carried as **"the D/ST version (blocked — §2 records no D/ST scoring rules)"** and doc 264
showed was never blocked at all.

---

## 1. THE TESTABLE FORM, STATED FIRST (§0.5a2)

**Matt's claim, from doc 228:** being early on the wire works **at D/ST**, where the skill-position
measurement said it does not. That is the belief §0.6 was written about — the conclusion *"being
early does not work"* was drawn on a population that excluded the position he meant.

**POPULATION — and it is the one that was missing: every EXECUTED D/ST add in this league,
2022–2025, weeks 1–14, matched to a team-week line. n = 208.** These are the adds §4.31 declared out
of scope (248 of 1,230, 20.2%). D/STs carry NEGATIVE ESPN ids; the id → team map was taken from
his own 2026 projection pull, all 32 rows, **not typed from memory** (§3), and the join is
**asserted** — the run refuses rather than defaulting, which is doc 251's lesson.
**BASELINE: D/ST12's season average, measured per season and pooled = 5.99 points a week.**
This project had no D/ST replacement number before today. **OUTCOMES: A = rest of season through
wk 14; B = the next four weeks — §4.31's own two, so the tables are comparable.**

**SHIPPED FIRST:** `dst_weekly_2021_2025.csv` — **2,576 team-weeks, five seasons**, scored under the
league's own bands. Doc 212's reproduce line named this file and it had never been committed.
Mean **5.46**, sd **6.28**, against doc 212's **5.10 / 6.56** — close, not identical, and the gap is
unexplained; likely week-18 handling. Flagged, not smoothed.

## 2. THE ANSWER TO HIS QUESTION IS CLEAN AND IT IS NULL

| add week | n | A | B |
|---|---|---|---|
| 1 | 7 | 42.9% | 57.1% |
| 2 | 17 | 35.3% | 17.6% |
| 3 | 16 | 50.0% | 75.0% |
| 4 | 15 | 46.7% | 26.7% |
| 5–8 | 60 | 41.7% | 50.0% |
| 9–14 | 93 | 41.9% | 40.9% |
| **all** | **208** | **42.3%** | **43.8%** |

**FLAT: rho(week, hit) = −0.027 (p=0.70) on A and −0.037 (p=0.59) on B.** Weeks 1–4 against 9–14 is
**43.6% vs 41.9%**. `[TESTED, n=208]`

**So the shape at D/ST is the same as §4.31 found at the skill positions, and being early is worth
nothing here either.** That answer does not depend on any baseline choice — it is a comparison
within one population — so it is the firmest thing in this doc.

**AND WEEK 1 IS NOT THE WORST WEEK AT D/ST.** 42.9% / 57.1% against every other week's 42.3% / 43.3%
— but **n = 7**, so this is a row to watch, not a finding. §4.31's week-1 penalty is a skill-position
result and must not be generalised here.

## 3. THE SIZE IS NOT ESTABLISHED, AND MY FIRST TWO ATTEMPTS BRACKET IT FROM BOTH SIDES

**42.3% against the skill positions' ~22% looks like the best position on the wire by a factor of
two. That is only true if a defence CHOSEN AT RANDOM does worse.** Two falsifiers, and they land on
opposite sides:

| baseline | A | B | managers' edge |
|---|---|---|---|
| **random from all 32 defences** | 39.4% | 41.0% | **+2.9 / +2.7 — and 20% of draws beat them** |
| **random from the season's bottom 20** | 18.2% | 24.9% | **+24.1 / +18.8 — 0 of 400 draws beat them** |

**BOTH ARE WRONG AND I CAN SAY WHY.** Drawing from all 32 includes the twelve already rostered, so
it hands random a pool of elites nobody could have claimed — **too kind**. Drawing from the bottom
20 by season average defines the pool by the OUTCOME, which is §4.23's trap exactly: a defence that
finishes in the bottom 20 is one that scored badly, by construction — **too harsh**.

**THE HONEST STATEMENT: the D/ST claim edge is somewhere between +3 and +24 points of hit rate and
is NOT RESOLVED.** Do not quote 42.3% as skill and do not quote it as noise.

**AND I WOULD HAVE SHIPPED THE FIRST ONE.** The all-32 falsifier ran first, said +2.9 and not
significant, and I had the conclusion written — *"the position is simply easy, picking the unit adds
nothing."* It was the second falsifier, run because the first one flattered random in a direction I
could name, that showed the number moves 21 points on the pool definition alone. **§0.2 says a
diagnosis is a claim; this says a BASELINE is a claim too, and a null against a generous baseline is
not a null.**

## 4. WHAT RESOLVES IT — NOT YET RUN, INPUT NAMED (§0.5a4)

**Doc 252 already rebuilt the rostered pool week by week** from the draft plus all 1,230 executed
adds and drops in date order. That is the correct free pool: who was actually claimable in week W,
with no hindsight. **Every input is now in hand** — the four `waiver_report_*.csv` carry the adds AND
the drops, and `draft_history_2021_2025.csv` carries the openings. The script from doc 252's session
was never committed and has to be rebuilt; it is one loop.

## 5. IF THE EDGE IS REAL, IT LANDS EXACTLY WHERE DOC 264 SAID THE POINTS WERE

Doc 264 measured that over a four-week hold **the unit is 65% of the movable spread and the schedule
35%** — the reverse of the per-week picture. This doc measures whether anyone in the league captures
the unit half when they claim one. **Those two are the same question from opposite ends, and the
answer to the second decides whether `slate.py` is aiming at value nobody takes or at value already
taken.** Settle §4 first.

## 6. SHIPPED

`Scripts\research\`: **`dst_all.py`** (five seasons of play-by-play → `dst_weekly_2021_2025.csv`,
plus the measured D/ST12 replacement) and **`dst_waivers.py`** (the table above, both falsifiers,
and the permutation test). Standard library only, 3.12-clean, join asserted.

**§4.31's line *"the D/ST version (blocked — §2 records no D/ST scoring rules)"* is RETRACTED** — the
third such retraction in two days (docs 262, 263). **And §2 still does not carry the D/ST bands.
That is the actual defect and it is queued for v9.3.**
