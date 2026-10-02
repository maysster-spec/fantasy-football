# 99 — There is no ceiling number, and the word "breakout" has two meanings

**Date:** 2026-08-30 (late) · **Matt asked two things:** how is "higher ceiling" calculated, and
can we find a trend among analysts for late breakouts the way we did for VBD vs rollout.

**Short answers: it isn't calculated at all, and no — for four measured reasons, not for lack of
trying. Chasing the second question turned up a defect in how §4.13's headline number is quoted.**

---

## 1. "HIGHER CEILING" IS NOT A METRIC. I WROTE IT ANYWAY.

Nothing in this project computes a per-player ceiling. The card said "take the higher ceiling"
as though the board could tell him which one that is. It cannot — the engine has **no variance
term at all** (doc 98 §3). That wording has been replaced.

## 2. THE ANALYST QUESTION IS ALREADY ANSWERED, FOUR WAYS, AND THE ANSWER IS NO

| # | measurement | source |
|---|---|---|
| 1 | **The accuracy contest is structurally blind to breakout skill.** Being 10% tidier on ordinary players is worth **2.80×** as much accuracy score as perfect foresight on every breakout; the breakouts are **3.4%** of total rank error. | doc 23, 240 players, 2025 |
| 2 | **The six-ranker panel is one opinion measured six times** — mean pairwise **r 0.81** against an external baseline. | doc 23, n=157 |
| 3 | **In ADP 100–170, "all six rankers are ahead of ADP" is the DEFAULT state — 40% of the band**, because ADP is censored there. Deep unanimity is arithmetic, not insight. | doc 35, n=144 |
| 4 | **Disagreement, controlling for ADP level, predicts finishing WORSE: −0.244, p=0.0009.** The players the experts fight about underperform. | `ERROR_PATTERNS` A8 |

Plus §4.13's own three draft-day signals on 324 player-seasons, all null, with "the market is
sleeping on him" the **worst** of the three (rho −0.079).

**And the direct test cannot be run.** The FantasyPros tables in the project carry **per-analyst
positional ranks only** — no per-player rankings, no per-round breakdown. Nothing in this project,
and nothing FantasyPros publishes, would let us score analysts on picks 104+ specifically.
Doc 24's framing stands: **you cannot use the contest to justify following an analyst, and you
cannot use it to dismiss one either.**

## 3. THE THING I FOUND WHILE CHECKING — AND IT CHANGES HOW WE QUOTE §4.13

§4.13's "17%" is a **ratio**: actual ppg ÷ projected ppg > 1.35. Re-scored on the same 324 rows
against an **absolute** bar — did he finish at or above his position's measured replacement ppg
(QB 20.09 · RB 9.92 · WR 9.62 · TE 8.25, doc 12) — the gradient **reverses**:

| ADP band | n | ratio "breakout" | **absolute: startable at all?** |
|---|---|---|---|
| 1–24 | 48 | 6.2% | **91.7%** |
| 25–48 | 48 | 2.1% | 75.0% |
| 49–84 | 71 | 8.5% | 57.7% |
| 85–120 | 69 | 7.2% | 37.7% |
| **121–180** | 88 | **17.0%** | **20.5%** |

**Band vs ratio: rho +0.149, p=0.007. Band vs absolute: rho −0.501, p<0.0001.**

Both are real. They answer different questions. Late players beat their **price** more often
because the price is near zero; they deliver a **startable player** far less often — 4 of 5 do
not. This is `ERROR_PATTERNS` **A8** exactly: the outcome was defined as actual-minus-expected and
the expectation was the confound.

**§4.13 is not retracted.** Its own verdict was already *"free and mildly positive but not
statistically resolved — a costless option, not an edge,"* and this is **why** it is only that.
What must change is the quoting: never present 17% as though a late pick is likely to become
useful. The card now says *"you are buying lottery tickets, not starters."*

I caught this by suspecting my own result. The first version of the test said low-projection
players break out more (MWU p=0.003) — which is what a ratio with a small denominator does. The
absolute re-test flipped the sign to **+0.350, p=0.001**. Had I stopped one cell earlier I would
have shipped an artifact as a finding.

## 4. LATE DARTS BY POSITION — SUGGESTIVE, NOT RESOLVED

Same 88 late rows:

| pos | n | ratio boom | absolute hit |
|---|---|---|---|
| **RB** | 28 | **28.6%** | 17.9% |
| TE | 18 | 16.7% | 16.7% |
| QB | 9 | 11.1% | 11.1% |
| **WR** | 33 | **9.1%** | **27.3%** |

RB vs WR on the ratio: Fisher **p=0.092**. Four-position chi-square **p=0.228**. On the absolute
definition it **reverses** (p=0.451). **Neither is significant. Do not cite either as a finding.**
Late RB hits are bigger when they land (median **1.82×** vs WR 1.72×, QB 1.38×).

What actually carries "prefer RB darts" is **§4.18** (a hit RB is a +80–95 keeper, a hit QB +2–5)
and **doc 12's waiver table** (RB adds hit 22%, QB 62% — RB is the hole you cannot patch). Those
have different inputs from this, so the agreement is real convergence — but this row is the weakest
of the three and must not be quoted as if it were the strongest.

## 5. THE PATTERN MATT DESCRIBED IS VISIBLE — AS AN OBSERVATION, NOT A TEST

The 15 late ratio-booms, 2022–2024:

> Tyrone Tracy Jr. 2.05× · Bucky Irving 2.02× · Tyler Allgeier 1.92× · Josh Downs 1.83× ·
> Jordan Mason 1.82× · D'Onta Foreman 1.81× · Jamaal Williams 1.78× · Christian Watson 1.72× ·
> Brock Bowers 1.61× · Taysom Hill 1.56× · Rashod Bateman 1.49× · J.K. Dobbins 1.48× ·
> Ray Davis 1.41× · Cade Otton 1.38× · Baker Mayfield 1.38×

`[OBSERVED, not tested]` **Eight of the fifteen are backs who inherited a backfield.** That is
Matt's stated archetype, and it is his instinct beating the instrument again — but "unsettled
backfield" is not a coded variable anywhere in this project and was **not** tested. It is an
eyeball on fifteen names. Treat it as a place to look, not as a number.

---

**Files:** directive → **v5.8** (§4.13b, 4.13c, 4.13d added) · `DRAFT_CARD.pdf` swings block
rewritten. Nothing in the board or the engine changed.
