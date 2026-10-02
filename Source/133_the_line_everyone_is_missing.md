# 133 — Opening-day offensive-line injuries: there is no control group

*2026-09-01. Matt: "what about offensive line injuries starting the season. does that move the needle at all?"*

**No — and the reason is the interesting part. The average team opens week 1 having lost 48.8% of
last season's offensive-line snaps. Half the line turns over every year, everywhere. There is no
intact-line comparison group to measure a disrupted one against.**

**Twelve tests, three measures, four seasons. Every sign points the intuitive way. Not one reaches
significance.** And the one nominal hit dies on the clustering correction, for the third time this
session.

---

## 1. Data

nflverse **snap counts** and **weekly injury reports**, 2021–2025 (both fetched tonight; neither
was in the project before). Three ways to measure opening-day disruption, from crudest to best:

| measure | what it is | spread across 128 team-seasons |
|---|---|---|
| **(A) injury report** | OL listed **Out or Doubtful** on the week-1 report | mean **0.20**; only **19%** of teams have even one |
| **(B) continuity** | how many of last season's **top-5 OL by snaps** played ≥50% in week 1 | mean **2.77 of 5** — 0:6 · 1:15 · 2:27 · 3:39 · 4:37 · **5:4** |
| **(C) quality-weighted** | **share of last season's OL snaps** not on the field in week 1 | mean **48.8%**, sd 21.3%, range **11%–100%** |

**(A) barely exists as a variable.** Teams place a lineman who is genuinely out on IR before week 1,
so he never appears on the report at all. **The thing you asked about is largely invisible in the
source a drafter would actually consult.** That is worth knowing on its own.

**(B) and (C) are the real measures, and they say the same thing: disruption is universal.** Only
**4 of 128** team-seasons opened with all five of last year's top linemen. The median team opens
with three.

## 2. Does it degrade the offence?  `[TESTED, n=128 team-seasons, 2022–2025]`

Outcomes measured over **weeks 1–4** (when a disrupted line would bite hardest) and the full season.
No projections needed, so this is the well-powered half.

| disruption measure | sack rate allowed | yards per carry | rush EPA/carry |
|---|---|---|---|
| (A) OL Out/Doubtful | r = −0.10 | +0.14 | +0.02 |
| (B) returning top-5 *(higher = more intact)* | −0.07 | +0.06 | +0.11 |
| **(C) share of OL snaps lost** | **+0.086** | −0.061 | −0.076 |

*(For (C), positive on sack rate and negative on the rushing measures is the intuitive direction —
a more disrupted line allows more sacks and gains less on the ground.)* **No p-value below 0.33.**

**At the extremes**, where an effect should be easiest to see:

| weeks 1–4 | most disrupted | most intact | difference | p |
|---|---|---|---|---|
| sack rate — top vs bottom quartile of (C) | 7.86% (n=32) | 6.61% (n=32) | **+1.25pp** | **0.090** |
| sack rate — 0–1 vs 4–5 returning starters | 7.79% (n=21) | 6.97% (n=41) | +0.82pp | 0.318 |
| yards per carry — 0–1 vs 4–5 | 4.21 | 4.35 | −0.15 | 0.439 |
| rush EPA/carry — 0–1 vs 4–5 | −0.065 | −0.023 | −0.042 | 0.135 |

**Every direction is right and nothing is resolved.** The most suggestive number, +1.25pp of sack
rate at p=0.090, is worth about **−12 fantasy points to a quarterback over a season** at doc 132's
point estimate of −9.6 points per +1% — which is itself a null. Small effect, small sample,
consistent story.

## 3. The fantasy step — and the clustering trap, a third time

| | player-level | **team-clustered (the §A5 correction)** |
|---|---|---|
| **RB beat vs OL Out/Doubtful** | **r = −0.171, p = 0.041**, n=142 players | **r = −0.149, p = 0.42, n=32 teams** |
| RB beat vs returning top-5 | +0.009, p=0.92 | — |
| QB beat vs OL Out/Doubtful | −0.164, p=0.26, n=50 | −0.145, p=0.44, n=31 teams |
| QB beat vs returning top-5 | +0.103, p=0.48 | — |

**The one nominally significant result in this entire document is an artefact of counting teammates
as independent observations.** OL disruption is a team constant; the honest n is 32, not 142.
Same correction that killed PROE (`ERROR_PATTERNS` A5), vacated target share (doc 128 §4) and the
positional-calibration tilt (doc 131 §2). **Three times in one session. It should be the first thing
checked on any team-level variable, not the last.**

## 4. Why this is null when the intuition is so strong

Because the intuition imagines a contrast that does not exist. "Team X is starting a backup guard"
sounds like information, but **the average team has lost half its line's snaps from last year** and
only 3% of teams open fully intact. Everyone is starting a backup somewhere. A variable with no
meaningful control group cannot separate anybody.

It also fits doc 132 exactly: **sack rate persists at r=+0.399, and it persists at +0.245 even
through a quarterback change** — a line's *performance* is a stable team property that survives its
personnel churning. The unit that persists is the scheme and the coaching, not the five men.

**VERDICT: no board change, no flag, no note on the draft card.** If you hear on Sept 6 that a
team's left tackle is out, the measured answer is that it is worth roughly a point a week to that
quarterback, unresolvable at this sample, and nothing at all to the running back.

## Assumptions

1. **Week-1 participation is used as the disruption signal, which is very slightly hindsight** — in
   August you have the injury report, not the snap counts. That makes §2 an **upper bound**, and it
   is null anyway.
2. **Snap counts do not distinguish a good lineman from a bad one**, only how much he played.
   Measure (C) weights by prior-season snaps, which is a workload proxy for quality, not a grade.
   A PFF pull would do this properly (doc 6 §8 ranks it third on that list).
3. **128 team-seasons on the intermediate outcome; 32 clusters on the fantasy outcome.** An effect
   under roughly 1.5pp of sack rate would not be visible here.
4. **Four seasons, 2022–2025.** Snap-count and injury releases go back further and would extend it
   cheaply if this is ever worth revisiting.

## 5. Reproducing it

`Scripts\ol_study.py --injuries`. Needs the nflverse `snap_counts_<year>.csv` and
`injuries_<year>.csv` releases in `Source\nfl\`, 2021–2025. Run 2026-09-01; the output above is
that run.
