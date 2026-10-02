# 197 — The web search ran, it pointed at a hole, and the hole had a signal in it

**2026-09-06 (T−1).** Matt: *"I don't recall you accessing the web when I've asked for research"*
and *"I suspect you are sweeping across all players again, and in the process spreading the signals
thin."*

## 1. HE IS RIGHT ABOUT THE WEB, AND HALF RIGHT ABOUT WHY IT MATTERED

**I used the web twice this session and then stopped** — the two breakout-archetype searches before
doc 185, and the Robinson/Henderson news check before doc 187. **Everything from doc 188 onward was
my own computation on nflverse.** Both times it ran through a subagent, so nothing appeared on his
screen, but the honest problem is not visibility: **doc 189 concluded "power is not the constraint,
ideas are" and I then stopped going out to get ideas.**

**Fixed. A literature search on WR role-growth signals, ~30 sources, every one dated.**

**The headline is a null about the entire field: almost nobody measures ROLE GROWTH.** Essentially
every published "predictive WR stat" study measures next-season *fantasy points* or *year-over-year
stability*. Dated examples:
- `[2024-07-08 | 4for4 | Hoopes]` targets per route run, YoY r=0.64, predictive r=0.53 **to points**.
- `[2023-10-01 | Sharp Football | Hribar]` target-per-route R²=0.32 against **targets/game R²=0.59** —
  raw volume is *stickier* than the rate. That cuts against the TPRR marketing.
- `[2023-07-20 | 4for4 | Hernandez]` targeted air yards YoY 0.68, target share 0.55, RZ targets 0.38.
  **Stability, not growth. And the most stable thing is the worst growth candidate — stable means it
  does not move.**
- `[2024-10-10 | PFF | Bryan]` is the **only** source with a forward target-share validation
  (+0.18 R² over actual share, for *next week*). `[2025-08-27 | KoalatyStats]` year-N+1 residual
  R²=0.07. Small, and paid data.
- **Route participation change, alignment change, separation-as-growth: nobody has measured any of
  them.** Every article recommending them does so on anecdote.

**So Matt's open question is open in the literature too.** That is worth knowing before buying data.

## 2. THE SEARCH POINTED AT A GAP I COULD ACTUALLY FILL — AND IT PAID

nflverse ships **snap counts** free from 2016. Snap share is the closest public proxy for "did the
coaching staff put him on the field more" — Matt's exact framing.

**BASELINE: half-PPR wks 1–14 on log(§1.1 preseason ADP) within season; BEAT = residual; WR/TE;
player-clustered; n=315.**

| model | result |
|---|---|
| snap-share change alone | **+0.794 per point of share, p<0.0001** |
| snap-share level alone | +0.571, p=0.0002 |
| **change + PRIOR GAMES** | **change +0.769 (p<0.0001) · prior games −0.38 (p=0.73)** |
| placebo | −0.24, p=0.90 |

> **Top quartile of snap-share growth beat their price by +12.6. Bottom quartile −13.2. Gap 25.7.**
> By season: 2022 r=+0.368 · 2023 +0.213 · 2024 +0.402 — **all three positive.**

**THIS IS THE FIRST THING TONIGHT THAT SURVIVES THE PRIOR-GAMES CONTROL.** Every other candidate —
workload, the growth model, vacated targets — collapsed into availability. This one inverts it:
**prior games goes to p=0.73 and snap share holds.** `[TESTED]`

**And it does NOT work the way the story says.** Snap-share change does **not** predict target growth
(r=+0.063, p=0.227). So it is not "coaches play him more → he earns targets." It is a role signal the
market underprices directly. **Level and change are collinear** — with both in, the level carries it
(+0.808, p=0.0002). Honest version: **snap share, not its change.**

## 3. LIVE READS — 62 receivers, 2025 snap share

**TOP quartile (≥85%), inside Matt's range:** **Wan'Dale Robinson 91% (+15)** · **Alec Pierce 86%
(+6)** · **Courtland Sutton 85%** · Michael Pittman 86% · DK Metcalf 87% · Jordan Addison 85% ·
Sam LaPorta 91% · Kyle Pitts 88% (**+26, the biggest riser on the board**) · Tucker Kraft 86% ·
Dallas Goedert 85% (**+20**).

**BOTTOM quartile (≤70%):** **Luther Burden III 40%** · **Matthew Golden 53%** · Mark Andrews 62% ·
Isaiah Likely 56% · Josh Downs 59% · Khalil Shakir 60% · Rashid Shaheed 61% · Keenan Allen 55%
(**−31**) · Dalton Kincaid 37% (**−20**).

**Burden at 40% is the fifth independent thing pointing away from him** — after one archetype signal
(185), zero inside-10 targets (187), 10.1% target share alongside Odunze (189), and the vacated-target
mechanism (196). **He was not on the field.**

**THE HONEST LIMIT: Puka Nacua is bottom-quartile at 68%.** This is a residual signal against price,
not a value ranking. It does not say Nacua is bad; it says the *cheap* players with high snap share
have beaten their price. Do not read the list as a board.

## 4. NOT SHIPPED TO THE SHEETS — Matt's call

The paper is built, verified and pinned. Doc 193 is tonight's lesson about shipping a mark and
testing it after; **this one is tested the other way round**, and it is better evidenced than the
games mark already printing. But it is one night, unreplicated, at T−1.
**Surfaced, not shipped. If he says add it, it is a ten-minute edit to the same `why` field.**
