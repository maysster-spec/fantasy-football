# 131 — Three swings at the projection itself: one correction, two nulls, one trap

*2026-09-01. Matt: "can you think of other dynamics to look into? ... We can't predict strong
defenses is what you indicated earlier?"*

**Yes — and I was wrong about how badly. Correcting that led to three tests of the board's own
input, which is where an edge would be worth the most. Two came back null and one found a silent
data trap. Recording all four, because a session that only writes up its hits is how this project
got the errors it has.**

---

## 1. CORRECTION — defences persist about twice as well as I told you

Doc 129 §2 published **r = +0.113** for a defence's year-to-year stability. That number used
**season-TOTAL EPA allowed** over **three transitions**. A season total is contaminated by pace and
by how many plays a team faced; the rate is the right measure, and the window was needlessly short.

Redone on per-play rates, **2020–2025, n=160 transitions**:

| measure | r |
|---|---|
| season-total EPA allowed *(what I quoted, longer window)* | +0.206 |
| **EPA per play allowed** | **+0.204** |
| yards per play allowed | +0.170 |
| **TDs allowed** | **+0.271** |
| pass EPA per attempt allowed | +0.190 |
| rush EPA per carry allowed | +0.185 |
| *for contrast:* **offensive** EPA per play | **+0.382** |

**A defence carries about 4% of next year's variance; an offence about 15%.** So defences are
weakly predictable, roughly half as predictable as offences — **not the near-zero I implied.**

**Does it change doc 129's conclusion? No.** The chain was: the mechanism explains 4% of pass rate
(R²=0.041), pass rate is 7.5% of a receiver's target variance (§4.21), and the whole channel is
worth about +2 points with perfect foresight. Doubling a 0.11 to a 0.20 at the front of that chain
does not rescue it. **The conclusion survives; the supporting number was wrong by nearly 2× and is
now fixed in doc 129, the directive and `anchor_study.py`.**

`ERROR_PATTERNS` class: a summary statistic chosen without asking what contaminates it. Same family
as A5 — the arithmetic was right and the quantity was the wrong one.

## 2. NULL — is the board's projection biased BY POSITION?

This was the swing worth taking. VBD compares a running back to a running back and a receiver to a
receiver, so if ESPN's projections are inflated more at one position than another, the **whole
board tilts** — and that would move pick 8, where §4.2's decision is Allen against St. Brown.

Ratio = league-total actual ÷ league-total projected, all drafted players with a preseason ADP, **no
selection on games played.** Below 1.0 means ESPN projected too high.

| pos | n | projected | actual | **ratio** |
|---|---|---|---|---|
| QB | 51 | 15,447 | 13,986 | 0.905 |
| **RB** | 151 | 19,884 | 18,226 | **0.917** |
| **WR** | 211 | 27,060 | 23,228 | **0.858** |
| TE | 62 | 6,612 | 6,136 | 0.928 |

RB minus WR = **+5.8 percentage points**, and it replicates in direction both seasons (2022: .885
vs .836; 2024: .945 vs .879). If real, WR VBD is inflated relative to RB VBD by ~6% and every
RB-vs-WR near-tie on the board should break toward the back.

**Bootstrap 95% CI on the gap: [−0.035, +0.150]. It includes zero.** `[HYPOTHESIS — NOT SHIPPABLE]`

**Do not act on this.** Two seasons is not enough, and I nearly talked myself into it: the first
cut showed ESPN under-projecting *rushing yards by 20.7%* among players who played 15+ games, which
looked enormous — until I noticed that **selecting on games played selects on success.** A bust
loses snaps and falls below the cutoff. The same split gives a ratio of 1.13 for 15+ games and
**0.63 for under 15, at both positions**. The 20% was the selection, not the projection.

**Incidental replication worth having:** mean games played is **12.94 for RBs and 12.95 for WRs** —
identical. That independently confirms doc 42's finding that RBs are not meaningfully more fragile
than receivers, from different data.

## 3. NULL — does ESPN over-project the TOP of the board more than the bottom?

Also bears on pick 8: if the elite tier is systematically inflated, waiting is better than it looks.

| ADP band | n | ratio | mean games played |
|---|---|---|---|
| 1–12 | 24 | 0.977 | 15.04 |
| 13–24 | 24 | 0.955 | 14.25 |
| 25–48 | 48 | 0.944 | 14.67 |
| 49–84 | 74 | 0.849 | 13.45 |
| 85–120 | 70 | 0.839 | 13.50 |
| 121+ | 235 | 0.887 | 12.28 |

Top-24 minus 85+: **+0.093, CI [−0.026, +0.206] — not resolved.** `[HYPOTHESIS]`

And note the fourth column: **the gradient tracks games played almost exactly.** Whatever is here
is availability again, not a rate error — which is doc 42's result a third time, and consistent with
§4.22's dose-response.

## 4. A REAL TRAP — ESPN uses DIFFERENT stat ids in projections and actuals

Discovered while mapping the raw payloads. Verified by exact match against nflverse, n=569:

| stat | id | exact match |
|---|---|---|
| carries · rush yds · rush TD | **23 · 24 · 25** | 99.6% |
| targets | **58** | 99.6% |
| rec yds · rec TD | **42 · 43** | 99.6% / 99.8% |
| **receptions — in the ACTUAL payload** | **41 and 53 (both)** | 99.6% |
| **receptions — in the PROJECTION payload** | **53 only; 41 is ABSENT** | — |

**A reader keying on id 41 gets a silent 0.0 from every projection row and no error.** This is
exactly §2's 2-pt-conversion trap (ids 19/26/44 in actuals, 62 in projections) in a second place,
and it says the pattern is general: **never assume a stat id is the same on both sides of an ESPN
payload — check both, on real rows.** `env_study.py`'s unused `REC` constant was pointed at 41 and
has been corrected.

## 5. VERIFICATION — the board does reconcile to §2 scoring

Since I was in the payloads anyway. Recomputing `proj_leaguepts` from `raw_stats` under §2's rules
(0.04/pass yd, **6-pt passing TD**, −2 INT, 0.1/rush+rec yd, 6-pt TD, 0.5 PPR, −2 fumble):

- **correlation 0.9914 · median absolute error 0.30 points · mean absolute 2.11**
- 6-pt passing TDs confirmed live: Allen 422, Lamar 375, Burrow 371. At a 4-pt TD they would be
  369 / 323 / 305 — the board is unambiguously on the league's rule.
- The residual is **projection drift between pulls**, not a scoring defect: the board is frozen at
  the 08-23 pull and I reconciled it against 08-30. That incidentally measures seven days of drift
  at a median of 0.30 points. The handful of large gaps (Jacobs 0.0, Tank Dell, Najee Harris) are
  the news overrides, working as intended.

**No defect. This was the highest-leverage thing that could have been wrong, and it is right.**

## 6. Where I would look next, with honest priors

| dynamic | testable with data on hand? | my prior | what it would change |
|---|---|---|---|
| **Age curves** — is §4.22's injury penalty really age? | yes, nflverse rosters carry birth dates | **high** — likely explains part of it | whether a 24-year-old's `12g` badge means the same as a 31-year-old's |
| **Route participation / snap share** | needs the nflverse snap-count release, one download | **high** — the best public usage predictor | a real role metric to replace "job worth" guesswork |
| **Air-yard share / aDOT** | yes, already in the weekly files | medium | whether a WR's role is improving before the targets show it |
| **Does a KEPT player's VBD persist?** (§4.18's open gap) | yes, draft history + projections | medium | what rounds 5–9 auditions are actually buying |
| **Your own draft record, pick by pick** | yes, draft history + preseason ADP registry | medium | where you gain and lose against the field |
| **Strength of schedule** | yes | **low** — §1's r=0.204 caps it | probably nothing |
| **Coaching / OC changes** | no — not a coded variable | low per doc 128 | nothing before Sept 7 |

**If only one: age.** It is the live confound sitting under a badge that is already on the board and
already changing rows at picks 56, 65 and 80.

## Assumptions

1. **§2 and §3 rest on the same two seasons as docs 128–130.** Preseason ESPN pulls for 2023 and
   2025 would roughly double both and are, for the fourth document running, the single most valuable
   missing input in this project.
2. **§1's persistence is measured on nflverse EPA, not points allowed.** Special teams and field
   position are absent. TDs allowed (+0.271) is the closest thing here to a points measure and is
   the most persistent of the six, so the true number may sit slightly above +0.20.
3. **The bootstrap in §2 resamples players independently.** Teammates are correlated; a clustered
   bootstrap would widen the interval, not narrow it. The null is safe in that direction.
