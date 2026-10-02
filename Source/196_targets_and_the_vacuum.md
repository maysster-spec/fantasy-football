# 196 — Where vacated targets actually go, and a growth model that collapsed

**2026-09-06 (T−1).** Matt: *"Vacated targets not having a measurable impact breaks my brain…
the ball will be distributed."*

## 1. THE BALL IS DISTRIBUTED. TO SOMEBODY NEW.

Never asked directly before. I traced every target on every team, 128 team-seasons, splitting on how
much walked out the door.

| | **HIGH-vacated teams** | LOW-vacated teams |
|---|---|---|
| share of targets vacated | 49% | 11% |
| targets that walked | **272** | 59 |
| team total targets, change | **−30** | +3 |
| **RETURNING players gained** | **−12** | −41 |
| **NEW arrivals took** | **253** | 103 |

**Of the 272 targets a high-vacated team loses, its returning receivers recover −12. Roughly zero.
New arrivals take 253 of them.** And corr(vacated share, team total target change) = **−0.183,
p=0.039** — a team that sheds targets also throws *less*. **The pie shrinks; it does not
redistribute to the guys already in the building.**

Matt's common sense was right about the ball being distributed and wrong about *to whom*. A team
that loses its number one signs or drafts a replacement — it does not hand the volume to the
returning number three.

**Holding team volume constant, vacated share is still negative** (−1.87, p=0.080). `[TESTED]`

**LIVE READ: this is the third strike on the Luther Burden case.** His bull argument is *"steps into
a massive target vacuum following D.J. Moore's departure."* Measured, the vacuum goes to whoever
Chicago brought in. Docs 185 (one archetype signal), 187 (zero inside-10 targets) and 189
(10.1% share with Odunze on the field) said the same thing three other ways.

## 2. THE RIGHT QUESTION — and a model that did not survive its own red team

Every test until now used **beat vs price** as the outcome. Matt reframed it correctly: the upstream
question is **who gets more targets next year.** New outcome, n=601 WR/TE with 40+ targets.

**What predicts target growth:**

| | r |
|---|---|
| years of experience | **−0.250** |
| age | −0.246 |
| **prior games played** | **+0.222** |
| his own prior targets/game | −0.173 |
| **vacated targets (excluding himself)** | **−0.095 (negative)** |
| his target share | −0.007 |
| aDOT | +0.057 |

**Young, healthy, not yet saturated.** A three-term model explains **13%** of who gains targets, and
its top quintile grows by **+1.8 targets/game more** than its bottom quintile. Predicted growth
against beat-vs-price: **+13.4, p=0.0001**, top quartile beats bottom by **18.9 points**.

**AND THEN THE RED TEAM KILLED IT.** Put predicted growth and prior games in together:

> **predicted growth −5.74 (p=0.190) · prior games +6.56 (p<0.0001)**

**The growth model is prior games played wearing a different hat** — the identical trap that killed
the workload signal in doc 191. `[TESTED — SUBSUMED]` Placebo clean (p=0.85); 2023 does not
replicate on its own (r=+0.095).

**So: no new signal, and the one receiver signal we have gets stronger.** It now predicts two things
from one input — who stays on the field *and* who gains targets.

## 3. WHAT THIS CHANGES ON THE SHEETS: NOTHING

The RB composite badge stands. The WR games mark stands and is **reinforced** — the thing that
predicts target growth turns out to be the thing already printed. **One player read moves: Burden.**

## 4. THE OPEN PART, STATED PLAINLY

Matt is asking for the pattern behind a receiver *earning* a bigger role — a wider route tree,
separation at more places on the field. **Everything that would measure that is data this project
does not have:** routes run by alignment, separation at the catch point, snap share by formation,
PFF grades. **aDOT is depth, not versatility.** What is left after that — age, experience, health,
current volume — explains 13% of target growth and collapses into one term.

**That is not a proof there is no edge. It is a statement that the edge he is describing lives in
data we do not own,** and the honest next step is buying it, not squeezing nflverse harder.
