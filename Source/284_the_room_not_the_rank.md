# 284 — Personnel shape and what a promotion is worth: his premise holds, his conclusion inverts, and the mechanism is the size of the room

**2026-09-10.** Matt asked for the potential-value idea to be pushed further, and gave a mechanism
this project had never looked at. **Answering his point 4 first, because it is a fair question:
no, I had not accounted for any of this. Nothing in 283 documents had measured a team's personnel
shape.** §4.21 measured team pass VOLUME (7.5% of the variance against a player's own share at
93.4%) and explicitly said not to add an environment column. **Shape is a different variable from
volume and it was never tested.**

---

## 0. HIS CLAIM, QUOTED, AND THE FOUR TESTABLE FORMS (§0.5a2)

> *"Teams who favor 3 WR sets have more target distribution and perhaps even more so if they have a
> productive pass catching RB and TE (Bowers). However, there are also teams that run heavy
> personnel with two TE sets … less target distribution due to fewer WRs on the field … a team with
> more common 2 WR sets may favor a WR3 who moves up to WR2 due to injury vacancy or skill."*

1. **Is personnel shape a TEAM TRAIT at all** — does it persist year to year? (§4.24a: persistence
   before payoff. A shape that does not persist cannot be planned around in August.)
2. **THE PREMISE** — on a heavier team, do fewer receivers get fed?
3. **THE CLAIM** — among receivers who actually moved up the order, is the gain bigger there?
4. **HIS OTHER MECHANISM** — does a pass-catching tight end or back eat the WR2's share?

**POPULATION: every team-season 2022–2025 in `pff_receiving_<year>.csv`, 128 team-seasons, and the
57 within-team promotions across the three transitions. Reproduce with `Scripts\width_study.py`.**

---

## 1. THE MEASUREMENT THAT KILLED THE FIRST VERSION (§0.2)

The obvious measure is *receivers on the field per pass play* = WR routes ÷ team pass plays. **The
PFF file has no team pass-play column.** `pass_plays` is per player: the team's pass plays while
*he* was on the field. Using the team's maximum as the denominator gave **Buffalo 4.13 receivers
per pass play in 2025** — impossible, alongside 1.44 tight ends and 1.26 backs, which is 6.8 route
runners on a five-eligible play. Their most-used receiver was on for only 453 snaps.

**The error is largest on exactly the teams that rotate or lose receivers, which is the thing being
measured — so it is a confound, not noise.** Worse, it is circular: a team that concentrates targets
has a WR1 on the field nearly always, which *raises* the denominator and *lowers* the measure, so
"narrow teams concentrate" would have come out true by construction.

**Every measure in the final study is a ratio of two route counts or a share of targets, both of
which cancel the missing denominator:** `heavy` = TE routes ÷ WR routes · `te_share` = TE targets ÷
team targets · `fed` = how many receivers drew 8%+ of the team's targets.

---

## 2. SHAPE IS A TEAM TRAIT — WEAKLY, AND ENOUGH

| trait | persistence year to year | league mean | range |
|---|---|---|---|
| **heavy** (TE routes per WR route) | **r=+0.294, p=0.0042** | 0.412 | 0.22–0.68 |
| back routes per WR route | **r=+0.600, p=0.0001** | 0.326 | 0.17–0.55 |
| TE share of targets | **r=+0.333, p=0.0013** | 22.2% | 9%–41% |
| RB share of targets | **r=+0.484, p=0.0001** | 18.2% | 8%–32% |
| receivers fed 8%+ | r=+0.189, p=0.068 | 2.92 men | 1–5 |

n=96 pairs. **`heavy` persists at about the same rate as offensive EPA per play (+0.382, §4.24a)
and better than a defence (+0.204), on a threefold spread from 0.22 to 0.68.** `[TESTED]`
**2025 heaviest: ARI 0.61 · NO 0.60 · BAL 0.60 · PIT 0.55 · CLE 0.54 · LV 0.52. Lightest: JAX and
LAC 0.32 · MIA 0.33 · HOU 0.34 · TB and BUF 0.35 · DET 0.35.**

---

## 3. THE PREMISE IS CONFIRMED

| on a heavier team | |
|---|---|
| **receivers fed 8%+ of targets** | **r=−0.441, p=0.0001** |
| WR2's share of TEAM targets | **r=−0.343, p=0.0001** |
| WR3's share of TEAM targets | **r=−0.430, p=0.0001** |
| WR1's share of the RECEIVERS' targets | **r=+0.209, p=0.018** |
| WR3's share of the RECEIVERS' targets | r=−0.195, p=0.032 |

n=128 team-seasons. **"Fewer WRs on the field means less target distribution" is exactly right, and
measured.** A heavy team feeds fewer receivers and the concentration goes **to the WR1**: his share
of the receiver room rises while the WR3's falls. `[TESTED]`

---

## 4. THE CONCLUSION INVERTS, AND THE MECHANISM IS THE SIZE OF THE ROOM

**POPULATION: 57 receivers who moved up their own team's target order between consecutive seasons,
same team both years, 100+ routes in both, starting at WR2 or lower. BASELINE: the 175 receivers on
the same teams who did not move up. OUTCOME: change in his share of team targets.**

**First, the promotion itself is real and large: +4.2 share points against −2.4 for everyone else,
a difference of +6.6 pp, CI [+5.3, +7.9], p=0.0001.** `[TESTED]` So "potential value from moving up
the order" is a genuine object, worth about a seventh of a receiver room.

**Then his claim, and it runs the other way:**

| | promoted receivers' gain |
|---|---|
| **LIGHTEST third** of teams (heavy 0.35) | **+5.2 pp** |
| **HEAVIEST third** (heavy 0.52) | **+2.4 pp** |
| difference | **−2.8 pp, CI [−5.1, −0.6], p=0.0215** (n=19 v 19) |
| continuous, player level | r=−0.317, p=0.0145, n=57 |
| **clustered by team-season (the honest n)** | **r=−0.268, p=0.064, n=47** |

**A promotion is worth roughly TWICE as much on a team that spreads the ball as on a tight-end-heavy
one.** Significant at the player level, **suggestive and not significant once clustered** — and
shape is a team constant, so the clustered figure is the one that counts (A5; this trap has already
cost this project three results). Minimum detectable difference here is about 2.5 pp against an
effect of 2.8, so it sits right at the edge of what 57 promotions can see.

**AND THE ROBUSTNESS TEST FOUND THE MECHANISM, WHICH IS BETTER THAN THE HEADLINE.** Re-run on his
share of the **receivers' own** targets, holding the pie constant:

> **heavy +7.3 pp · light +8.3 pp · difference −1.0, CI [−5.5, +3.3], p=0.67 — NULL.**

**So moving up the order is worth the same on any team. What differs is the room you move up inside:
the receivers on the light teams held 61.3% of all targets against 51.9% on the heavy ones.**

**That is the whole finding, and it does not rest on the fragile 57 at all** — it follows from the
128-team-season facts in §3, where the pie difference is measured at p=0.0001. **His premise and his
conclusion are both about concentration; the concentration is real and it is swamped by the receiver
room being nine points of team targets smaller.**

---

## 5. HIS BOWERS MECHANISM — CONFIRMED, AND IT IS A WHOLE-ROOM EFFECT

| | WR1 | WR2 | WR3 |
|---|---|---|---|
| TE share of targets vs his share of TEAM targets | −0.265 (p=0.002) | **−0.432 (p=0.0001)** | −0.420 (p=0.0001) |
| TE share vs his share of the RECEIVERS' targets | +0.164 (p=0.065) | −0.116 (p=0.19) | −0.169 (p=0.059) |
| RB share vs his share of TEAM targets | −0.169 (p=0.056) | −0.267 (p=0.002) | −0.279 (p=0.002) |
| RB share vs his share of the RECEIVERS' targets | +0.090 (p=0.31) | −0.056 (p=0.52) | −0.084 (p=0.34) |

n=128. **"A productive pass-catching TE and RB means less to go around" is confirmed — and it is a
tax on the whole receiver room, not on the WR2 in particular.** The bottom rows are the test that
separates a real effect from the arithmetic that shares must add to 100, and they are null. **Bowers
is the right example: Las Vegas gave 33.5% of its targets to tight ends and fed two receivers.**
`[TESTED]`

---

## 6. HIS POINT 3 — THE TEA LEAVES, AND WHICH ONES ARE WORTH READING

> *"dropped balls, poor separation, not being on the same page and running the wrong route, not
> knowing the play book, poor attitude, not making clean breaks, giving up too early on a play …
> these are tea leaves we need to read … this needs to come from the news because i don't have time
> or money to watch these games."*

**The frame is right and two of the specific leaves are measurably the worst ones available.** From
the stability table in §4.28 (4for4, 8 July 2024, carried in doc 251) — how much of a receiver trait
carries from one season to the next:

| trait | stability |
|---|---|
| **slot rate (his role)** | **0.75** |
| targets per game | 0.70 |
| points per game | 0.68 |
| targets per route run | 0.64 |
| **red-zone TD rate** (§4.5) | **0.02** |
| **drop rate** | **0.14** |
| **contested catch rate** | **0.02** |
| route rate | 0.01 |

**"He is dropping balls" is the single least informative thing the news can tell you, and
"contested catch" is no better.** What carries is **role** — and role shows up in the news as snaps
and routes, not as adjectives. Doc 248 adds that on our own rows **drop rate was fluff** and
**speed measured backwards a third time.**

**So the rule that comes out of his instinct, and it is the same one doc 283 put on LaPorta:**

> **Read the news for WORKLOAD, not for adjectives. "Played 38 snaps, down from 52" is a signal.
> "Dropped two and looked disengaged" is the least stable thing measured at the position.**
> Separation is the one leaf on his list that is neither confirmed nor dismissed — **+6.7 points,
> direction right, unresolved** on a 45-row volume-selected subsample (doc 248, §4.23's trap).

**NOT YET RUN, input named (§0.5a4):** whether a dated news item of the kind he describes predicts a
ROLE change — which is the object, not the player's points. The testable form: *among receivers with
a negative coaching or performance note in weeks 1–8, does route share fall over the following three
weeks more than for matched teammates?* It needs a dated news corpus keyed to a week;
`apply_research.py` already stamps dated notes onto `player_context.csv`, so the pipe exists and the
corpus does not.

---

## 7. HIS POINT 2 — THE PROJECTION IS A SNAPSHOT, AND THAT PART IS SIMPLY TRUE

> *"The ESPN projection may not always show that fact if the window of that happening is either
> before the projection was released or some time after. The projection is a point in time and has
> some fragility baked in."*

**Correct and already load-bearing in this project**, from the other end: §1.1's whole hard rule
exists because a re-pulled ADP has drifted toward what happened. The same applies to projections.
**Two live instances today:** the sheet printed `QUESTIONABLE` on LaPorta, who is cleared, because
the pull predates the injury report by two days (doc 283); and Pearsall and Tank Dell carry **blank**
projections because ESPN does not project an IR player, which is what silently dropped Pearsall off
the page (doc 277) and invented a free roster seat (doc 281). **Three defects this week, one cause:
the projection is a photograph and the page treated it as a fact.** `[OPEN]` — the fix is a staleness
stamp on anything derived from the pull, not a faster pull.

---

## 8. SHIPPED

- **`Scripts\width_study.py`** — the whole study, standard library only, reproducible.
- **`Source\team_shape_2025.csv`** — 32 teams: `heavy`, `te_share`, `rb_share`, `wr_share`, `fed`.
- **`wire.py`** — every free receiver now carries **his team's target share** in plain English
  ("spreads it · fed 4 · tight end took 18%, backs 14%"), with a caption saying it matters only for
  the promotion case and is **not** a reason to prefer him today.
- **Three negative controls run, and the first version of the assertion did not fire.** Checking
  `len(teams)==32` passes happily when an alias is wrong, because the unmapped spelling becomes its
  own key. It now validates every code against the 32 ESPN spellings and refuses, naming the bad
  code. PFF and ESPN disagree on five teams and **ESPN writes Washington `WSH` where PFF writes
  `WAS`** — that one was one board column away from being live.

---

## OPEN AFTER THIS — and his point 5 asked for these

- **RUNNING BACKS, the same question.** Testable form: *among backs who moved up their team's
  carry order, is the gain bigger on teams with a narrow backfield (two backs taking 90%+ of
  carries) than on a committee?* `pff_rushing_2022-2025.csv` is on the drive and carries attempts
  and snaps. **NOT YET RUN.** Doc 244's Wally Pipp result says the trigger is production in relief;
  this is the complementary question of what the job is worth when it opens.
- **D/ST.** Testable form: *does a defence's target value come from its own quality or from the
  schedule?* Already half answered — §4.33 measured the matchup at **108%** of the spread between
  the units, the only position where the schedule beats the player. The unasked half is whether
  **personnel churn** (a new coordinator, a lost pass rusher) predicts the unit, which is §4.22(a)'s
  r=+0.204 persistence restated. **NOT YET RUN.**
- **The clustered p on §4 is 0.064.** Two more transitions (the 2021 and 2026 PFF files) would take
  n from 47 team-seasons to about 75. `pff_receiving_2021.csv` is not on the drive.
- **Whether `heavy` should gate the §4.30 receiver composite.** The composite fires at 39.4% on
  three signals; if the promotion premium is really pie size, a fourth gate of "his room holds 60%+
  of the targets" is free to test on the same 185 rows. **NOT YET RUN.**
