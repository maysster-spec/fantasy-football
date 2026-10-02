# DIRECTIVE FINDINGS: SECTION 4 OF `00_PROJECT_DIRECTIVE.md`, MOVED WHOLE AT v9.8

*Moved out of the resident directive on 18 Sept 2026 (doc 367), word for word and in the order v9.7 held
it. The directive carries a one-line index of every finding below and no numbers; this file carries the
finding, its baseline, population and sample size, and its strike-through trail. Read a finding when a
question touches it; grep its id. Nothing here was retracted by the move, and nothing here is edited
without the directive's index line being checked in the same commit.*

*`Scripts\research\audit_directive.py` reads §4.14's two counts out of THIS file, by the wording
"(N of M rows on the DD-DD freeze" and "Only ~N rows". Reword either and it falls back and says so.*

---

> ### DRAFT-ERA RETRACTIONS, moved here from the directive's DO-NOT-QUOTE table at v9.32 (doc 435).
> Still dead. They left the resident table because nothing in season quotes them; the directive keeps the
> season rows only. Each finding below carries its own strike-through as well.
>
> | dead number or claim | what is true |
> |---|---|
> | *"about 20 points"* for Allen at pick 8 | the direction holds, **the size is not established** (§4.2) |
> | *"+8.6"* for the rollout | **a superseded spec. Quote the range** (§4.10) |
> | *"78 points"* for the D/ST defect | **measured at +0.26** (directive §0.2) |
> | *"a young riser is worth about three times an older one"* | **withdrawn. Youth is not a tiebreak** (§4.34) |
> | *"Cary finished last"* / the draft grade's back half | **void and retracted** (§4.29) |

---

## SECTION 4 — ESTABLISHED FINDINGS

> **[v9.5] ALL 37 NUMBERED FINDINGS ARE IN THIS SECTION.** §4.16–§4.33 were moved here from §6 on
> 18 Sept, word for word. If you are looking for a finding, it is here and nowhere else.


Full detail in `02_findings_ledger.md`. **[v5] Numbers below are the shipped board's, not v4's.**

**4.1 Replacement (corrected).** RB30 = **168.589** · WR30 = **163.540** · QB12 = **341.603** ·
TE12 = **140.295**. *(v4's 168.0 / 168.5 / 341.7 / 137.7 came from a 200-row export the ledger
itself records as 39% fabricated; WR was 5.0 too high.)*
Elite VBD: Gibbs **+162.3** · Nacua **+131.3** · McCaffrey +134.9 · Bowers **+51.2** ·
McBride **+47.6** · Andrews **0.0**.

**[v5] 4.1b The cutoffs encode a 6/6/0 FLEX split** (24 base RB + 6, 24 base WR + 6, 12 TE + 0 =
the 12 FLEX slots). Honest uncertainty **RB28–31, WR29–32**, worth ~±1.5 VBD per player on
RB-vs-WR. **Do NOT make this self-refitting** — the same method on 2024's projections gives
RB25/WR35, a ten-rank swing off one season's noise.

**4.2 Josh Allen — [v5.4, docs 69/70. Replaces the +24.2-over-Henry claim, which compared
against the wrong player.]** The old test forced Henry (eff_pick **19.10** — the *pick-17*
alternative) into pick 8, baking an ~11-pick reach into the baseline. Against the true pick-8
alternative — **St. Brown, eff 8.30, vbd +101.33** vs Allen's **+80.31** — measured in **dollars**
(§0.3) under the final §4.12 noise, paired: **Allen@8 − wait = −$23.86 [−$36.12, −$11.61]**
(N=1000, QB-conditioned outcomes) and **−$13.30 [−$28.6, +$2.0]** (N=600, position-blind pool).
Same sign in every measured configuration; wait also leads P(1st), P(top6) and p10.
**PLAN: best board player at 8, QB later. PICK 8 IS CLOSED (doc 70) — open no further
sensitivity on it.**
**[v7.2 — THE PICK SURVIVES, THE CUSHION DOES NOT. doc 182.]** Doc 139's margin was measured on
**ONE board state** — the same defect doc 140 corrected at pick 32, and the same caveat v6.7
already attached to doc 139's pick-56 number. Re-run through the production `Engine` on a modal
pick-8 state (top seven by `eff_pick` gone, `top=12, rollout_inner=60`): **margin over the
runner-up 7.8, not ~20**, and the runner-up is **Derrick Henry**. The board's own arithmetic
agrees — St. Brown **+101.33** against Henry **+95.38** is a **5.9 VOR** cushion. **WHO to take is
robust: St. Brown is #1 in every state anyone has run (10/10 doc 139, 96/100 doc 140, 13/13 doc
182). The SIZE of the edge is NOT established and "about 20 points" must not be quoted.** A
30-state generator built for doc 182 produced no variation at pick 8 — the top seven are too
tightly clustered for §4.12's noise to reorder them — so 7.8 is also one state, and the
disagreement with doc 139 is OPEN.

**[v6.6, doc 139] A THIRD, UNRELATED ROUTE TO THE SAME PLAYER.** The shipped rollout, run ten
times at pick 8 under ten different seeds and at three Monte-Carlo sample sizes (24 / 60 / 150):
**Amon-Ra St. Brown 10/10 every time, margin over the runner-up 19.96 → 20.20 points.** The
largest margin anywhere on this board by an order of magnitude, and reached without the dollar
simulation, the QB-conditioned pool or the Snyder model. **Pick 8 stays closed.** Allen is VBD rank 14 on the shipped board and the **QB2–QB6 tier spans
~11.8 points** — the cliff is real, the plateau behind it is flat, which is why waiting wins.
**Survival to 17 ≈ 0.03 (w8) / ≈ 0.00 (w22)** at q=0.90 under the final noise — the old 0.14 was
generous. Allen is a pick-8 decision or nobody's.
**[v5.4] The ±30-point QB-replacement band CANCELS** in any comparison where both paths start
exactly one QB — every realistic path (verified analytically and in-sim: flat to 0.6 pts across
the whole ±60 sweep, doc 70). **It no longer hedges any pick decision.** It still applies only to
*absolute* payout or points projections, and to hypothetical strategies differing in QB count.

**4.3 Only two TEs carry a premium:** Bowers +51.2, McBride +47.6, then Warren +28.1 and a long
flat tail. Do not pay for TE5–TE10.

**4.4 Consensus divergence — STATE THE BASELINE EVERY TIME.**
vs **FantasyPros ECR**: TE +18.0 · QB +15.7 · RB +8.1 · WR −8.3
vs **Boone**: TE +23.9 · QB +29.5 · RB +6.4 · WR −7.0
vs **ESPN's own board**: QB +1.7 · TE +8.5 · RB +3.5 · WR −6.3 **[v5 — remeasured; v4's
+5.5/+5.0/+8.1/−6.4 was on an older board]**
**RANKINGS MODE edits ESPN's board. Do NOT apply the FantasyPros TE block move there.**

**4.5 Sticky vs luck** (n=37, ≥10 RZ targets both years, 2024→2025): inside-10 targets r=+0.59 ·
RZ target volume r=+0.51 · RZ target share r=+0.48 · **RZ TD rate r=+0.02 — noise, ignore.**

**4.6 Already priced by ESPN:** TD regression, rushing efficiency. Only after-contact ability
underweighted — tiebreaker, not thesis.

**4.7 Structural tendencies — true draft selections only, keepers excluded:**
Rounds 1–4 are **83.3%** RB/WR · **TE before round 3: 2 of 48 manager-seasons [v7.2, doc 180 — 
re-derived on true selections only; the old "1 of 43" was never reproducible, and 2021 cannot be 
attributed at all because 6 of its 12 Manager fields hold a TEAM name, not a person]** · median first TE
round 7 · **median first D/ST round 12** (IQR 11–13) · first K round 11+ in **95.8%** ·
**zero TEs inside the first 17 picks in 2024 and 2025.**

**4.8 D/ST and K draft value is not realizable.** 11–12 of 12 teams stream a D/ST every season.
Draft-day VBD for both is an illusion. **Cost of ignoring this: +105.6 pts/manager-season.**

**4.9 ESPN ADP is broken for K and D/ST.** Field-minus-ESPN median: K +55.0, D/ST +33.2.
**Exclude K and D/ST from keeper prediction entirely.**

**4.10 Pick-rule ranking — [v5, doc 54; v5.4 provenance note].**
**The board is worth six times more than the rule.**
**[v5.4] The +8.6 in the table was measured under a SUPERSEDED noise spec** (doc 57, N=200,
`0.30×min(ADP,70)`); the original-noise N=300 result is **+4.2 [+2.9, +5.6]**, and the race has
never been re-run under §4.12's final affine spec. Direction is stable across all three specs —
rollout first, VONA and the penalty lose everywhere. **Treat the magnitude as +4 to +9 points,
≈ $15 of expected payout with an interval touching zero (docs 68/69). Ship the rollout; do not
quote +8.6 as current.**

| rule | vs constrained VBD | verdict |
|---|---|---|
| **Rollout (full lookahead)** | **+8.6 [+6.5, +10.8]** *(superseded spec — see note)* | **ship this** |
| Static VBD + roster caps | baseline | fallback, costs 8.6 |
| Need-penalty heuristic | **−5.7** | **do not build** |
| Static VBD, no caps | −8.7 (drafts 1.46 WRs) | caps are mandatory |
| VONA (the published method) | **−8.8** | **do not build** |
| Follow ADP | −24.5 | — |
| Myopic lineup-marginal | −84.0 | why replacement level exists |

Opening: **RB-RB-RB in 64–65%** of drafts under both winning rules — an independent replication
of the "RB in rounds 2 and 3" finding on a different simulator. **Dead:** Zero RB, pop-and-trade,
Hero RB, and now VONA and the positional penalty.

**[v5.9] 4.11 BYES ARE A LAST-RESORT TIEBREAKER, NOT A CONSTRAINT — Fable doc 94, N=1500.**
Measured across the whole board, **a bye collision costs at most 1.2 points, ever**; the worst case on
this board is **Lamb + Pickens in week 14 at 1.16 points**. The list below is retained for awareness and
for the BYE CHECK line, but **a bye must never move a pick that has any real margin behind it.**
`[TESTED]`

**4.11b Bye traps. [v7.2 — renumbered; two sections both carried 4.11.]** Week 13: Taylor, Jeanty, Henry, Hall, Bowers, Flowers, Warren.
Week 11: Bijan, Jacobs, Kyren, Judkins, Stafford, Adams.
**Week 14: Pickens (keeper), McBride, Jeremiyah Love.** From slot 8 the live collisions are
**Taylor or Henry (13) with Bowers or Warren (13)**, and **anything at week 14 stacking on Pickens.**

**4.12 Opponent calibration — [v5.1, doc 60]. THE NOISE MODEL IS AFFINE, NOT PROPORTIONAL.**

**`sd = 0.111 × ADP + 5.40`** (generative; the *observed* sorted residual is `0.139 × ADP + 6.75`).

Refit on all five seasons, n=680 picks. Weighted RMSE per band, against the observed sd:

| model | RMSE |
|---|---|
| **affine refit (this)** | **0.89** |
| doc 16's independent fit `0.1255 × rank + 5.31` (n=271, this league only) | 2.65 |
| v5's `0.30 × min(ADP, 70)` | 3.06 |
| v4's `0.135 × ADP` | 8.56 |

**A proportional form cannot be right.** It sends dispersion to zero at the top of the board,
where the observed sd is **7.5 picks**. The floor term is the whole point, and it is exactly where
Matt picks — 8, 17, 32, 41. v4 under-dispersed by **4×** at pick 12 and only 1.2× at pick 100, so
the correction is largest precisely where it matters most.

This also **reconciles doc 16 with doc 53**, a conflict left open by the red team: two independent
datasets converge on nearly the same line. That agreement is the strongest calibration result in
the project.
Plus: **TE effective ADP +15 picks** (fitted) and **Snyder takes Josh Allen at q ≈ 0.90** **[v5.4: Jeffreys fit on 4-for-4 when available, 95% CI [0.56, 1.00]; the 2024 miss was a two-pick snipe and 2025 was 1.01 overall — doc 70]**.
RB/WR pace gaps rest on 2 drafts — left uncorrected, `[HYPOTHESIS]`.

**[v5] 4.13 The ceiling — doc 55.** Each player returning >1.35× projection roughly **doubles**
the title: 0 breakouts → **4.7%**, 1 → **14.4%**, 2 → **26.8%**, 3 → **54.6%**.
**You cannot predict which player.** Three draft-day signals tested against 324 player-seasons,
all null; "the market is sleeping on him" (ADP rank minus projection rank) is the **worst**
(rho −0.079, and its coldest quintile breaks out at 3.1% against ~11%). **Retired.**
**You can predict where.** Breakout rate **17.0%** at ADP 121–180 versus **2.1–6.2%** at 25–84.
**Therefore: risk from round 9 (picks 104, 113, 128, 137). Never before.** A global upside tilt
costs **$22–41** of expected payout (p=0.003); a round-9+ tilt is free and mildly positive but
**not statistically resolved** — a costless option, not an edge.
**Perspective:** season luck is **6×** draft luck; corrected for sampling error the spread in
title odds between one good draft and another is **zero**.

**[v5.8] 4.13b THE WORD "BREAKOUT" CARRIES TWO DEFINITIONS AND THEY POINT OPPOSITE WAYS — doc 99.**
§4.13's rate is a **ratio**: `actual ppg / projected ppg > 1.35`. Re-scored on the same 324
player-seasons against an **absolute** bar (finished at or above the position's replacement
ppg — QB 20.09 · RB 9.92 · WR 9.62 · TE 8.25, doc 12; **[v9.4] derived, not measured: §4.1's season totals ÷ 17**):

| ADP band | n | ratio "breakout" | **absolute: was he startable at all?** |
|---|---|---|---|
| 1–24 | 48 | 6.2% | **91.7%** |
| 25–48 | 48 | 2.1% | 75.0% |
| 49–84 | 71 | 8.5% | 57.7% |
| 85–120 | 69 | 7.2% | 37.7% |
| **121–180** | 88 | **17.0%** | **20.5%** |

**Band vs ratio: rho +0.149, p=0.007. Band vs absolute: rho −0.501, p<0.0001.** Both real, and
they answer different questions. Late players beat their *price* more often because the price is
near zero; they deliver a *startable player* far less often. **§4.13 is not retracted — its own
verdict was already "a costless option, not an edge," and this is the reason why.** But never
quote the 17% as though a late pick is likely to become useful: 4 of 5 do not.
**Always say which definition you mean.** This is `ERROR_PATTERNS` A8 — the outcome was defined
as actual-minus-expected, and the expectation was the confound.

**[v5.8] 4.13c LATE DARTS BY POSITION — suggestive, NOT resolved. Same 88 rows.**
RB **28.6%** (8/28) vs WR **9.1%** (3/33) on the ratio definition — Fisher **p=0.092**, and the
four-position chi-square is **p=0.228**. On the absolute definition it **reverses**: WR 27.3%, RB
17.9%, **p=0.451**. **Neither is significant; do not cite either as a finding.** Late RB hits are
larger when they come (median 1.82× vs WR 1.72×, QB 1.38×). What carries "prefer RB darts" is
§4.18 (keeper option value) and doc 12's waiver table (RB adds hit 22%, QB 62%) — **not** this.
`[OBSERVED, not tested]` 8 of the 15 late ratio-booms are backs who inherited a backfield
(Tracy, Irving, Allgeier, Mason, Foreman, Jamaal Williams, Ray Davis, Dobbins). That is Matt's
stated archetype and it is visible in the names, but "unsettled backfield" is not a coded
variable and was not tested.

**[v5.8] 4.13d THERE IS NO CEILING NUMBER, AND ANALYSTS DO NOT SUPPLY ONE — doc 99.**
Nothing in this project computes a per-player ceiling, and four separate measurements say the
analyst panel cannot stand in for one:
1. **The FantasyPros accuracy contest is structurally blind to breakout skill** (doc 23): being
   10% tidier on ordinary players scores **2.80×** as much as perfect foresight on every
   breakout; the breakouts are 3.4% of total rank error.
2. **The six-ranker panel is one opinion measured six times** (doc 23): mean pairwise r **0.81**
   against an external baseline, n=157.
3. **In ADP 100–170, "all six rankers are ahead of ADP" is the DEFAULT state** (doc 35): 40% of
   the band, because ADP is censored there. Deep unanimity is arithmetic, not insight.
4. **Disagreement, controlling for ADP level, predicts finishing WORSE** (`ERROR_PATTERNS` A8):
   **−0.244, p=0.0009.** The players the experts fight about do not outperform.
Add §4.13's own three null draft-day signals (324 player-seasons; "the market is sleeping on him"
was the **worst**, rho −0.079). **The accuracy tables carry per-analyst positional ranks only — no
per-player and no per-round data — so the direct "who calls late breakouts" test cannot be run on
anything in this project, and FantasyPros does not publish what it would need.** Doc 24's framing
stands: you cannot use the contest to justify following an analyst, and you cannot use it to
dismiss one either. **A "swing" is therefore a human call on a near-tie, with no metric behind it.
Say so; do not imply the board ranks ceiling.**

**[v5] 4.14 Known-unsound regions.** **Two thirds of the board (330 of 482 rows on the 09-05 freeze as shipped in `board_v8_fixed.csv`, measured by `audit_directive.py` on 1 Oct, doc 468; ~~328 of 480~~ was the count as first written on 09-05; 327 on 09-03; 323 on 08-23) sits inside
ESPN's undrafted sentinel**, a 2-pick-wide blob where ESPN supplies no real ADP. Only ~152 rows
carry a genuine draft position (the sentinel moved from ~158 to ~170 with the 09-03 ADP) and Matt picks through 161. **Do not quote a survival number past
roughly pick 120** without saying it rests on a fabricated ordering.

**[v5.5] 4.15 ADP dispersion alone is NOT a survival model — doc 82.** Measured: applying §4.12's
affine noise to `eff_pick` with no opponent model gives **P(Allen survives to pick 17) = 0.736**.
§4.2's calibrated figure is **≈ 0.03**. That is wrong by **25×**, and it is wrong precisely where
this league is most predictable — Snyder picks at 9 and 16 and takes Allen at q ≈ 0.90.
**§4.12's noise is an INPUT to the §5 opponent model, never a substitute for it.** A survival
number computed from dispersion alone is biased optimistic and must not be quoted.

**QB tier structure, from the shipped board:** QB1 Allen 80.31 · QB2 Lamar 33.02 · QB6 Stafford
21.19. **QB1→QB2 is a 47.3-point cliff; QB2→QB6 is 11.8 points in total.** One cliff, then a
plateau — so **there is no correct "target pick" for QB.** Take one when the board offers value,
not on a schedule. (The draft card carried "target pick 41" with no source until doc 82.)

**[v5.5] 4.16 The doctrine above is now MEASURED, not just preferred — doc 88.** Three tests:
1. **His league 2022–2025, n≈50 team-seasons: NULL both ways.** One QB vs two+: −0.04 sd, p=0.87.
   One TE vs two+: +0.10 sd, p=0.71. The history neither supports nor refutes; it cannot resolve an
   effect under ~1 pt/week. **Do not cite it as vindication.**
2. **Streaming volume, 1,132 executed adds:** TE **3.15** and QB **2.71** adds per team-season
   (RB/WR ≈ 5.1, D/ST 5.17). Both positions are already streamed here.
3. ~~**The board is decisive.** Every QB at 113/128/137 is BELOW replacement, so QB2 IS CLOSED.~~
   **[v5.6 — RETRACTED, doc 91. The premise was false.]** That argument rested on
   *"VBD is measured against QB12 = the streaming baseline."* **QB12 is not the streaming
   baseline.** Doc 12 (F34) measured it from **951 executed waiver adds**: a waiver QB returns
   **15.25 ppg**, while QB12 = 341.603 is **20.09 ppg**. VBD-against-QB12 overstates streaming by
   **4.84 pts/week at QB**. Re-scored against the measured streamer, Jared Goff is **+3.95
   pts/week**, worth **+8 to +12 points** over two or three missed weeks — which matches doc 12's
   independent paired-sim figure of **+10.1** almost exactly.
   **QB2 IS NOT CLOSED. It is a live judgement worth roughly +10 points.**

**[v5.7] 4.17 QB2 MEASURED ON THE SHIPPED BOARD — doc 92 (Fable), reviewed doc 93.**
The streaming baseline was re-derived from the raw waiver files, not inherited:
**doc 12's sample sizes are NOT reproducible** (raw files hold **1,230** executed adds, not 951;
QB adds **135 events / 82 player-seasons**, not 34 — independently corroborated: this session
counted 1,230 and ~130 QB adds before the question arose). Re-measured **QB streamer = 16.65 ppg
per played week [15.51, 17.78]**; hit rate reproduces at 0.60 vs doc 12's 0.62. Doc 12's 15.25 is
re-tagged `[SOURCED, n irreproducible]`, and **doc 91's "4.84 pts/week overstatement" was itself
overstated — the real gap is 3.44.**

Paired grid, N=600, second QB gated to picks ≥104, holes filled at the measured rates:
**QB2/TE1 = +11.04 ± 3.08 points, +$18.16 ± 8.08.** The rule buys Goff 46% / Mayfield 21% at
pick 104 (33%) or 113 (26%). **Crossover: QB2's edge reaches zero only at a streaming fill of
≈21.7 ppg — ABOVE QB12's own 20.09 season rate** (verified independently: the sweep is linear to
0.01, slope −2.20 pts per ppg, implying the backup starts ~2.2 weeks). No measured streaming in
this league's four-year record reaches that.

**CAVEATS THAT MATTER (doc 93):** "three methods agree" is **one** clean measurement — doc 12 is
irreproducible by doc 92's own step 1, and doc 91's arithmetic was derived from doc 12's number.
The sim gives the streamer **no week-to-week matchup selection**, which is where a good streamer's
edge lives; the mean-rate sweep only partly stands in for it. **Treat as: QB2 at 104/113 is worth
roughly +11 points, measured once, on machinery that flatters the rostered backup slightly.**

**[v5.7] 4.18 THE GAP MATT FOUND: doc 92 NEVER PRICES KEEPER VALUE.** The word "keeper" appears
**zero times** in it; its objective is 2026 dollars only (§0.3). But §6 makes every round-5+ pick a
keeper audition, and the keeper ceiling is **structurally positional**, from the shipped board:

| a hit that becomes | RB | WR | QB | TE |
|---|---|---|---|---|
| position rank 5 | **+95** | +78 | +21 | +6 |
| position rank 10 | **+80** | +39 | **+2** | 0 |

**A hit RB dart is a +80 to +95 VBD keeper. A hit QB is +2 to +5.** One starting QB slot against
twelve startable QBs compresses QB VBD to nothing — QB1 is +80 and all of QB2–QB12 spans 37 points
— so a QB is almost never worth a keeper slot while a hit RB always is.

**[v5.7, MEASURED — this corrects my own first estimate.]** I first sized this with §4.13's 17%
*breakout* rate. **Breaking out and becoming a keeper are different events**, and the second is
measurable from `draft_history_2021_2025.csv` across four transitions (2021→22 … 2024→25):

| drafted in | n | became a keeper the next year |
|---|---|---|
| rounds 1–4 | 156 | **0.0%** (ineligible — confirms §2.1a) |
| rounds 5–8 | 186 | **15.1%** |
| **rounds 9–12** | **192** | **8.3%** |
| rounds 13–15 | 132 | 1.5% |

Within rounds 9–12 by position: **QB 16.7% (3/18) · RB 10.0% (5/50) · TE 9.1% · WR 9.0% · K and
D/ST 0%.** `[TESTED, n=192, 4 transitions]`

**A late QB is kept MORE often than a late RB, not less** — which cuts against the shape of my
argument. But frequency is not value: at 10.0% × ~+85 VBD the RB dart's keeper option is worth
**~+8.5 expected 2027 points**, against **16.7% × ~+3 ≈ +0.5** for the QB. **Net edge to the RB:
about +8** — real, but smaller than my first estimate of +15, and now *below* doc 92's +11 rather
than above it.

**The two effects very nearly cancel.** That is why the rule below is "take the better player"
rather than a position preference. Still unmeasured: whether next-year VBD persists for a kept
player. n is thin — 5 RBs and 3 QBs.

~~**DRAFT-NIGHT RULE — the resolution of §4.16/§4.17/§4.18: at 104 or 113 take the second QB only
if the tier is Goff or better AND no RB with a plausible 2027 role is on the board. If a genuine RB
is there, take the RB.**~~ **[v6.6 — SUPERSEDED. Its premise, the +8 keeper option, was an assumed
number and has now been measured at ≈ +0.7. See 4.18b.]**

**[v6.6] 4.18b THE +8 WAS AN ASSUMPTION AND IT IS GONE — doc 138 (Fable), `[TESTED, n=18 kept RBs
+ n=21 NFL late hits, 2021–25]`.** §4.18 priced the RB dart's keeper option as 10.0% × **~+85**,
where +85 came from *what an RB5–RB10 finisher is worth on the 2026 board* — a ceiling, used as an
expectation. Measured on the seasons that actually happened:
**BASELINE — state it every time: VBD14 = weeks-1–14 points minus the SAME season's RB30 / WR30 /
QB12 / TE12 weeks-1–14 total.** On that scale an RB5–RB10 finisher averages **+81.4** (n=30), so
§4.18's anchor translates almost exactly and the comparison is fair.
- **A kept RB returns +6.7 VBD14 [−20.1, +31.4]** in his keeper season (n=18, this league,
  2022–25), against the +81 assumed. **Option = 10.0% × 6.7 ≈ +0.7 [−2.0, +3.1].**
- Kept RBs drafted round 9+ the prior year: **+31.3 → −2.5** (n=7). Kept QBs: **+29.6 → −55.7**
  (n=9), so the QB dart's option is **≤ 0** as well.
- **Not a league quirk.** NFL-wide on the sanctioned preseason registry (§1.1; no historical
  `espn_adp`): an RB who hit from ADP **97+** returned **−3.9 VBD14 [−26.4, +20.4]** the next
  season (n=21) against **+47.5** for the same hit from ADP 1–48 (n=60). Size-matched (20 ≤ VBD14
  ≤ 80): early **+44.2**, late **−23.1**. Same sign at WR, QB and TE.
- **Mechanism is per-game, not injury:** late hits' VBD per game falls +2.8 → +0.3 while games fall
  only 12.3 → 10.9. The early band regresses toward the mean; **the late band regresses THROUGH
  replacement. A late hit is, on average, a role that existed for one year.**
- Survivorship controls both ran: a kept player beats a matched non-kept look-alike by ~+30, so
  **manager selection is real — it is the LEVEL that is wrong.** The favourable side is +12, not +81.
- Falsifier was fixed BEFORE computing (option < +4 → resolves to QB2; > +11 → to the RB; CI
  spanning both → unchanged). The whole interval sits below +4.
**Every positional cut is UNDERPOWERED and doc 138 says so. What carries it is that two
populations, three hit thresholds, the early-ADP benchmark and the per-game decomposition all land
on the same side of a threshold fixed in advance.**

**[v6.6] 4.18c AND THE BOARD IS BLIND ON THE OTHER SIDE — doc 139 §9 `[TESTED]`.** The shipped
rollout scored QB2-vs-RB at 104/113 as a **tie** (margin 0.64 / 0.93 across 24 opponent
realisations each — inside §7's own "coin flip" band, in both directions). That looked like it
contradicted §4.17/§4.17b's +5 to +11. It does not. **`_lineup()` models ONE kind of absence — the
bye week. There is no injury model, so in the entire rollout a backup QB can enter the starting
lineup in exactly one week of the season.** Measured on a pick-104 roster: a second QB on a
different bye adds **+2.49**; a second QB sharing QB1's bye adds **+0.00**.
**So the rollout can price at most 1 of QB2's 2.98 measured missed weeks (§4.17b, n=48
team-seasons). The other ~2 weeks — roughly +3.6 to +5.2 points — are invisible to the ordering by
construction, and they exceed the tie.**
**This does NOT apply to TE2:** FLEX is RB/WR/TE, so `_lineup` gives a second TE a lineup path in
all 14 weeks and prices it fully. §6's "TE is a different question and must not be answered by
analogy to QB" now has its mechanical reason.
**AND IT CONFIRMS MATT'S SAME-BYE TRAP BY MEASUREMENT.** §6 records "a same-bye second QB/TE
doubles the hole" as a *preference*. A same-bye QB2 measures **+0.00** — not worse, zero, because
he never starts. The doctrine's reason was right.
**DO NOT TEACH `_lineup` AN ABSENCE MODEL BEFORE SEPT 7.** §4.10's rule ranking, §4.2's pick-8
dollars and §4.12's calibration were all fitted against this objective. Changing what the objective
measures four days out invalidates the measurements that make the tool worth running. Post-draft.

**[v6.6] DRAFT-NIGHT RULE — REPLACES THE STRUCK TEXT ABOVE. At 104 or 113, if a QB of Goff's tier
or better is on the board, TAKE THE QB2.** Take the RB only when no such QB is there, **or when the
RB is the better 2026 player by the board's own VBD** — the 2027 keeper story is not a tiebreaker
any more. Three independent measurements point the same way: the option that used to cancel QB2 is
≈ +0.7 not +8.5 (§4.18b), the board's "tie" is a tie only because it cannot see two thirds of QB2's
value (§4.18c), and QB2's own edge is +5 to +11 (§4.17/§4.17b). **The DIRECTION is supported from
three unrelated angles; the SIZE is one measurement per side. Quote the rule, not a number.**
**Do not re-derive any of this at the draft.**
**Unchanged by all of the above:** §4.19's "bench RB to the cap" — that rests on Matt's own waiver
record (four of five RBs he adds never give him a startable stretch), not on keeper value.
**And §4.24(a)'s tiebreak still applies underneath this one:** at a genuine late-QB tie, prefer the
better-protected line.

**[v5.9] 4.17b WHAT THE 15th ROSTER SPOT WOULD OTHERWISE HOLD — doc 111. Doc 92 priced QB2 against
NOTHING.** Measured from `draft_history_2021_2025.csv` joined to nflverse game logs, weeks 1–14,
n=48 team-seasons: **a drafted starting QB is missing 2.98 weeks a season** (median 1, p75 5);
**the top-2 drafted RBs are short 5.54 slot-weeks** (median 4, p75 8). Goff at 19.20 ppg over a
re-measured waiver QB at **17.38 ppg** = 1.8–2.6 ppg × 2.98 weeks = **+5.4 to +7.6 points** — below
doc 92's +11.04, and the difference is doc 92 also charging for the weeks the streamer fails to be
*available*. **Treat QB2 as +5 to +11, low end better supported.** The counter that the sixth RB
covers those 5.54 weeks is FALSE — RB3/4/5 cover them; the sixth body plays only when three are out
at once. **The extra RB spot is worth its §4.18 keeper option (≈ +8 in 2027), not lineup
insurance.** ~~The two remain within noise; the §4.18 draft-night rule is UNCHANGED.~~
**[v6.6 — BOTH CLAUSES SUPERSEDED, doc 138. That keeper option measures ≈ +0.7, not +8, so the
extra RB spot is worth neither lineup insurance NOR a meaningful keeper option, and the rule DID
change. See §4.18b. The +5 to +11 for QB2 in this section is unaffected and is now the whole of the
comparison.]**

**[v5.9] 4.19 MATT'S OWN WAIVER RECORD — doc 111 `[TESTED, n=88 of his adds, 4 seasons]`.**
1,230 executed adds, teams resolved through `manager_identity_map.csv`, joined to nflverse weekly
scoring under §2. **BASELINE — state it every time: rest-of-season ppg from the add week through
wk 14 ≥ the position's replacement ppg.** This is NOT doc 12's bar, which is unrecoverable from its
text, so both sides below were re-measured under one definition.

| pos | league (all 12) | **Matt** |
|---|---|---|
| QB | 26.5% (n=113) | **35.7%** (n=14) |
| RB | **17.2%** (n=233) | **20.5%** (n=39) |
| WR | 20.1% (n=219) | 12.5% (n=24) |
| TE | 26.1% (n=142) | 18.2% (n=11) |

**RB, Matt vs the other eleven: 20.5% against 16.5%, Fisher p=0.64; ppg 6.59 vs 6.48, MWU p=0.98.**
Top of the per-manager table and **not resolved**. He IS earlier than the field — **1.05 weeks ahead
of the median at RB, first to the player 57% vs 42%** (p=0.22) — but it does not convert: his RB
adds' 3-week before/after lift is **+0.39** against the league's **+0.74**.
**FOUR OF FIVE RBs HE ADDS NEVER GIVE HIM A STARTABLE STRETCH.** Nobody in this league beats his
rate and the wire still cannot patch an RB hole. **This is the measured argument for "bench RB to
the cap" — on his own record, not the league's.**

**[v5.9] 4.20 THE COMMITTEE FLAG WAS POLARISED BACKWARDS — doc 111.** The team RB "pie" (sum of the
top three RB projections) **barely varies: IQR 317–355, ±6% across 32 teams.** There is no big-vs-
small backfield here, so it cannot be a second axis. What the RB1−RB2 gap actually measures is
**ESPN's uncertainty about who wins the job** — Matt's target, not his avoid. `depth_map.py` now
emits **UNSETTLED (gap < 60) · contested (60–150) · LEAD BACK (≥ 150)**, computed from the **SOURCE
pull** — the board has the 12 keepers removed, which deleted DAL's, NYG's and NE's lead backs and
made those gaps fiction — plus a **`job worth`** column = ESPN's projection for the man currently
holding the job, the closest thing to a ceiling number this project has (cf. §4.13d). It separates
**Brooks/Hubbard (unsettled, job worth only 154)** from **Monangai/Swift (unsettled, job worth
196)**. Darts gated to `adp_pick < 168` per §4.14. **Whether the winner of an unsettled job is worth
having remains untestable here (doc 110).**
**[v6.7] AND THE FLAG DOES NOT PICK THE WINNER — doc 141 `[TESTED, n=19 team-seasons, UNDERPOWERED]`.**
Matt asked whether the INCUMBENT is worse off than the challenger in an unsettled backfield (his
case: Kyren Williams). Population: every team-season in the 2022 + 2024 preseason pulls, top two RBs
by projection, UNSETTLED if the gap < 60. "Incumbent" = whoever the MARKET prices higher (lower
preseason ADP from the §1.1 registry). BASELINE: expected VBD14 from price alone — `v_t` regressed
on `log(adp)` across all RBs that season (2022 r=−0.592 n=60; 2024 r=−0.609 n=85); beat = residual.
Unit is the TEAM-SEASON, not the player (A5). Result: **incumbent − challenger = +8.2, p=0.604,
CI [−22.9, +38.1]**; LEAD BACK teams +4.1, p=0.816; difference of differences p=0.863.
**NULL, and the point estimate leans the OPPOSITE way to the intuition.** What is real is the
VARIANCE: Brooks −80 vs Dowdle +53, and Moss −24 vs Chase Brown +87, are Matt's story exactly —
and Pollard +60 vs Spears −51, and Jones +59 vs Chandler −50, are its mirror at the same magnitude.
**BUY THE JOB, NEVER THE NAME.** The flag says the job is unresolved and worth 215 points; it has
no opinion on who gets it, and neither does this test. Now stated in plain English on the ladder.

**[v6.0] 4.21 "OPPORTUNITY ENVIRONMENT" IS THE SMALL HALF — doc 128. NO NEW FLAG.**
Decomposition of a pass-catcher's year-over-year target change, nflverse only, 3 transitions:
**team pass VOLUME 7.5% of the variance, his own SHARE 93.4%** (n=221 WR/TE with ≥50 targets and
≥12 games both years). RBs: **5.7% / 95.9%** (n=113). Team volume moves ±11% a year; a player's
slice moves ±39%. `[TESTED]`
**Oracle upper bound** — regress fantasy-point beat on the team's *realised* pass-volume surprise,
so it is a ceiling on any forecast: **WR/TE +2.1 pts per +50 team attempts** [−0.3, +4.4], p=0.084,
n=239, against sd(beat) = 47. WR +3.3 [+0.4, +6.2]. TE −0.9. **RB −5.4** [−10.3, −0.5], p=0.035 —
more team passing was **worse** for backs, the opposite of the dump-off premise. +50 attempts is a
~9% change, the size of a real coordinator or QB swap. `[TESTED, 2022 + 2024, the only two usable
ESPN projection pulls — 2023's raw_stats are empty for 98 of 103 QBs]`
**Nobody forecasts team volume, ESPN included:** ESPN r=+0.231 (n=62 team-seasons; +0.345 in 2022,
−0.035 in 2024); last year's actual as the forecast beats it at +0.315. **Unpriced and predictive
are different claims** — this dimension is unpriced because it is close to unforecastable.
**Vacated target share was built and FAILED its test.** Team-clustered (the §4.20 / A5 correction —
it is a team constant, so honest n is 32 teams not 138 players): **r=+0.125, p=0.50, +1.84 pts per
+10% vacated, CI [−3.38, +7.05]**. One season. `[HYPOTHESIS]` The table survives as a *targeting
list* only: MIA 56% · WAS 53% · PIT 46% · GB 38% · NE 37% · PHI 37%; LA 0% · DEN 1% · CIN 7%.
**Two independent measurements now agree.** §4.20 found the team RB pie varies ±6% across 32 teams;
this finds ESPN's 2026 team pass-volume repricing has sd 7.4%. **Rushing side and passing side both
say the team environment barely varies and the job does.** The flag Matt asked for already exists —
`depth_map.py`'s UNSETTLED / contested / LEAD BACK plus `job worth` — it is simply not named after
the environment. **Do not add an environment column, and do not re-derive this.**
Reproduce with `Scripts\env_study.py`. Gemini task retargeted to open jobs: `GEMINI_OPEN_JOBS.txt`.

**[v6.1] 4.22 PRIOR-SEASON AVAILABILITY IS PREDICTIVE, AND THE BOARD NOW SHOWS IT — doc 129.**
Three results, in the order they were found.
**(a) The defence/QB pass-rate mechanism is half right and unforecastable** `[TESTED, n=128
team-seasons]`. corr(QB EPA/att, pass rate) = **−0.184**, p=0.038 — worse QB play meant MORE
passing, not less; game script beats coaching intent. Defence r=+0.104, p=0.24, Matt's direction
but not significant. Together R²=0.041. And **defensive quality persists year to year at r=+0.204**
(EPA per play allowed, n=160 transitions 2020–2025; offence persists at +0.382) — **[v6.3, doc 131:
this CORRECTS the +0.113 published in v6.1, which used season totals on a 3-transition window.
Direction survives, number was wrong by nearly 2×.]** A defence carries ~4% of next year's variance
against an offence's ~15%: weakly predictable, not unpredictable, and nowhere near enough to carry
the mechanism. Prior pass rate (r=+0.440) is the only usable predictor and is
already in the projection. **Does not change §4.21's magnitude — a better story about the 7.5% is
still the 7.5%.**
**(b) The market IS anchored on last year, and fading it loses.** Preseason boards only
(`load_preseason_adp`, 2022 + 2024; never historical `espn_adp`, §1.1). ADP rank regressed on
projection rank and last-year-points rank: last year still loads **+0.093 / +0.263** after the
projection. **But** rho(market-cheaper-than-projection, beats projection) = **−0.173, p<0.001,
n=409** — an independent replication of §4.13's retired signal, on a different market, and
*stronger*. **When the market and the projection disagree, the market is the one that is right.**
**(c) WHY: availability. THE ACTIONABLE PART.** Players who played ≤12 games the prior season beat
their projection by **−16.2 points less**, controlled for position, log(ADP) and season, se 7.2,
**p=0.025**. It is **entirely a WR effect**: WR −25.4 (n=45, p=0.003); **RB null** (+5.7, p=0.63).
Mechanism is recurrence and rests on a large sample — prior games predict next games at **r=+0.50,
n=1,806 pairs**; a WR who missed time averages **9.1 games** next season vs **12.7**. The market
discounts them only ~5.5 rank slots. **This closes doc 42's open question** — doc 42 correctly
refused a flat per-position haircut as double-counting and could not test August injury flags
(historical `injuryStatus` is stamped at capture, not preseason); **games played last season carries
no such contamination.**
**SHIPPED:** `make_board.py` prints a `12g` badge for any player under 13 games in 2025, from a
committed static `Source\games_2025.csv`. 46 of 180 rows. **Surfaced, NOT scored** — same call as
doc 42, same reason: one measurement on 45 receivers does not become a VBD coefficient.
**LIVE ROWS THIS CHANGES:** drafted-range WRs at ≤12 games in 2025 that the sweep graded NEUTRAL
"no injury news found" — **McLaurin (10 g, adp 60) and Odunze (12 g, adp 65) are live at picks 56
and 65; Marvin Harrison Jr. (12 g, adp 82, carries BUY) is live at pick 80.** Also London (12 g,
adp 19), G. Wilson (7 g, adp 37), Hunter (7 g), Reed (5 g, BUY), Godwin (9 g, BUY).
**Carry the conservative number (−16), not the WR headline (−25).** Two seasons, two positions
tested, one hit.

**[v7.9] RE-MEASURED ON FIVE SEASONS, AND IT IS BIGGER AND NOT WR-ONLY — doc 203.** n=735
player-seasons 2021–2025, §1.1 registry prices, OLS with season, position and log(ADP) controls:
**played ≤12 games last season = −19.4 pts, se 4.7, p=0.00004.** All positions, not "entirely a WR
effect". **This is the strongest downside signal in the project.** The `12g` badge was already
position-blind, so the CODE was right and this paragraph's description was too narrow; the badge is
if anything understated. `[TESTED]` **Carry −19 now, all positions.**

**[v6.2] (d) YEAR TWO BACK IS A NULL — doc 130 `[TESTED, n=338 classified]`.** Cohorts on players
with BOTH prior seasons on the field: **A healthy both (n=179, beat −13.3) · B hurt last year
(n=89, −25.4) · C healthy last year but hurt two years ago (n=70, −10.8)**. **C vs A: +2.4 pts,
p=0.77 — and the market discount is +2.7 slots, p=0.54, also null.** The injury discount fully
unwinds after one healthy season: the year-2 player is neither cheap nor better. C vs B is +14.6,
p=0.14 — the right shape, unresolved. **C hit 42.9% against a 39.7% baseline.**
**THE CASE ITSELF: Barkley 2022 went at ADP rank 19 against PROJECTION rank 36 — a 17-slot
PREMIUM.** He beat his projection by +53.5, but he was never cheap; the market was ahead of ESPN on
him. The same cohort and season also held Deebo −86 and Damien Harris −83. **Do not pay up for a
bounce-back narrative and do not expect a lingering discount.**
**[v6.2] (e) THE YEAR-1 PENALTY IS DOSE-DEPENDENT — this is what doc 130 actually found.**
Mean beat by games played the prior season: **1–6 g −40.8 (n=19) · 7–9 g −27.1 (n=30) · 10–12 g
−16.9 (n=40) · 13+ g −12.6 (n=249)**. The market's discount scales the right way (+7.7 / +1.0 /
−2.1 slots) and nowhere near far enough. **An eleven-game season and a four-game season are not the
same warning — read the NUMBER on the badge, not its presence.** `[SUGGESTIVE — pooled r=+0.083,
p=0.128; bands hold 19/30/40. Carry (c)'s −16.2 as the finding and this as the shape.]`
**SHIPPED:** the badge is now shaded in three tones, ≤6 g darkest. 12 players in the worst band,
21 middle, 27 lightest. **Jayden Reed (5 g) and Chris Godwin Jr. (9 g) both carry BUY.**

**[v6.3] 4.23 TWO SWINGS AT THE BOARD'S OWN PROJECTION — BOTH NULL. DO NOT RE-DERIVE — doc 131.**
**(a) Positional calibration.** ratio = actual ÷ projected, all drafted players with a preseason ADP,
no selection on games: **QB 0.905 · RB 0.917 · WR 0.858 · TE 0.928**. RB−WR = **+5.8pp**, replicating
in direction both seasons — but **bootstrap 95% CI [−0.035, +0.150] INCLUDES ZERO.** `[HYPOTHESIS]`
If it were real, WR VBD would be inflated ~6% against RB VBD and every RB-vs-WR near-tie would break
to the back. **It is not established. Do not tilt the board.**
**THE TRAP THAT NEARLY SHIPPED IT:** the first cut showed ESPN under-projecting rushing yards by
**20.7%** among players with 15+ games — but **selecting on games played selects on success** (a bust
loses snaps). Ratio is 1.13 at 15+ games and **0.63 under 15, at BOTH positions.** The 20% was the
selection. **Never condition on an outcome-correlated filter and read the result as a projection bias.**
**(b) ADP-band calibration.** ratio by band: 1–12 **0.977** · 13–24 0.955 · 25–48 0.944 · 49–84 0.849
· 85–120 0.839 · 121+ 0.887. Top-24 minus 85+ = **+0.093, CI [−0.026, +0.206] — not resolved.** And
the gradient tracks **mean games played** (15.04 → 12.28) almost exactly, so what is there is
availability, not rate — doc 42's result a third time, consistent with §4.22(e).
**INCIDENTAL, and worth keeping: mean games played is 12.94 for RBs and 12.95 for WRs — identical.**
An independent confirmation of doc 42's "RBs are not meaningfully more fragile."
**(c) VERIFIED, NO DEFECT: the board reconciles to §2 scoring.** `proj_leaguepts` recomputed from
`raw_stats` under §2's rules: **r=0.9914, median absolute error 0.30 pts.** 6-pt passing TDs confirmed
live (Allen 422; at a 4-pt TD he would be 369). The residual is 7-day drift between the 08-23 board
and the 08-30 pull, plus the news overrides. **Do not re-audit this.**

**[v6.4] 4.24 THE OFFENSIVE LINE — FORECASTABLE, NOT ACTIONABLE — doc 132.**
Doc 12 §2.7 surveyed it; doc 28's dead list already carries **OL quality for RUNNING BACKS**. The
**QB version** was flagged live and untested. Tested now.
**(a) CORRECTION.** Doc 28 dismissed forecastability with *"line-CONTINUITY churn is r=−0.01."*
Continuity is personnel; **sack rate is performance**, and it persists: **r=+0.399** year to year
(nflverse, n=160 transitions, 2020–2025) — **above offensive EPA per play (+0.382) and nearly double
a defence (+0.204). The most persistent team trait measured in this project.** Split by whether the
primary passer changed: same QB **+0.444**, **QB CHANGED +0.245 (p=0.049)** — roughly half survives a
new quarterback, so the line and scheme carry a real share. `[TESTED]`
**(b) AND THE PAYOFF IS NULL.** Prior-season team sack rate vs a QB's beat: **r=+0.092, p=0.53,
n=50 QB-seasons**; same-season hindsight is −0.160, p=0.27 — **the two disagree in sign.** Against a
QB beat sd of **108 points**, an effect under ~25 points is invisible. **`[UNDERPOWERED — not "no
effect"]`. The RB version failed PREDICTION; this one failed POWER.** Keep the distinction if anyone
revisits. The 2023 and 2025 preseason pulls would take it to n≈100.
**NO BOARD CHANGE.** One carry-forward only, at the same standing as byes (§4.11): **at a genuine
late-QB tie under the §4.18 rule at 104/113, prefer the better-protected line.** A tiebreak, never a
number, and never over real margin. Reproduce with `Scripts\ol_study.py`.

**[v6.5] (c) OPENING-DAY OL INJURIES — NULL, AND THERE IS NO CONTROL GROUP — doc 133.**
nflverse snap counts + weekly injury reports, **n=128 team-seasons, 2022–2025** (both releases were
fetched for this and are new to the project). Three disruption measures:
**(A) OL listed Out/Doubtful on the week-1 report: mean 0.20; only 19% of teams have even one** —
a team IRs a lineman who is genuinely out, so he never reaches the report. **The thing being asked
about is largely invisible in the source a drafter consults.**
**(B) last season's top-5 OL playing ≥50% in week 1: mean 2.77 of 5. ALL FIVE in 4 of 128.**
**(C) share of last season's OL snaps not on the field in week 1: mean 48.8%, sd 21.3%.**
**HALF THE LINE TURNS OVER EVERY YEAR, EVERYWHERE.** That is why nothing separates: there is no
intact-line comparison group. Twelve tests across three measures, weeks 1–4 and full season —
**every sign intuitive, no p below 0.33.** Extremes, top vs bottom quartile of (C): sack rate
**7.86% vs 6.61%, +1.25pp, p=0.090** — worth ≈ −12 QB points a season at §4.24(b)'s own null point
estimate. ypc and rush EPA, p=0.63 and 0.41.
**THE CLUSTERING TRAP, THIRD TIME:** RB beat vs (A) is **r=−0.171, p=0.041 at player level (n=142)**
and **r=−0.149, p=0.42 clustered by team (n=32).** OL disruption is a team constant. After PROE (A5),
vacated share (§4.21) and the positional tilt (§4.23(a)), **cluster FIRST on any team-level variable.**
**NO BOARD CHANGE, NO FLAG, NO CARD NOTE.** If a left tackle is announced out on Sept 6: roughly a
point a week to that QB, unresolvable at this sample, and nothing to the running back.
Reproduce with `Scripts\ol_study.py --injuries`.

**[v7.9] 4.25b AGE IS REAL AND ITS NAME IS AVAILABILITY — doc 203. THIS IS THE HEADLINE; READ IT
BEFORE 4.25.** Same n=735, same controls, both terms in one model:

| term | effect on beating price | p |
|---|---|---|
| **age 28+** | **−3.8** | **0.39 — null** |
| **≤12 games last season** | **−19.4** | **0.00004** |

**Matt's mechanisms are right and they act THROUGH availability.** Wear, re-injury, slower
recovery, CTE — each shows up as games missed, and games missed is measured at **five times** the
size of age with a p four orders of magnitude smaller. **Age NET of availability is
indistinguishable from zero on 735 seasons.** So do not fade a player for being old; fade him for
having missed time, which the board already prints.
**THE INTERACTION HE ASKED FOR IS NULL AND UNDERPOWERED:** RB +19.7 (p=0.411), WR −9.6 (p=0.457),
pooled −12.2 (p=0.370). The one cell worth naming is **WR 28+ AND ≤12 games: −36.3 (n=24)**, the
worst on the table and **Terry McLaurin exactly** (31, 10 games, bottom-quartile snaps, live at
pick 56). n=9 in the RB equivalent. **A shape, not a finding.**
**[v8.0] AND IT VARIES BY PLAYER — doc 204, Matt again, and this QUALIFIES the −19.4 above.**
Restricted to players with THREE prior seasons on file (n=290, same controls): **last season's games
+0.63 pts/game, se 1.16, p=0.59** · **own 3-year rate +0.52, p=0.77** · both together, nothing.
Bands non-monotone. **Not a power failure — −19.4 is about −5 pts per missed game and this
coefficient is four standard errors the other way. Among ESTABLISHED VETERANS, availability does
not predict.** The pooled penalty is carried by players who wash out; a veteran has already survived
the filter — the §4.18b survivorship structure again. **BADGE STAYS, READING CHANGES: `12g` is a
warning on a young or unestablished player and close to noise on a ten-year veteran.** Live rows it
re-reads: McLaurin (yr 7), Godwin (9), Kelce (13), Kittle (10) lighter; Reed (yr 4) and Odunze
(yr 3) keep theirs.
**[v8.0] THE SECOND CHANNEL — THE RIVERS EFFECT, MEASURED.** QB seasons with 200+ attempts,
2021–2025, n=177: **rho(age, air yards per attempt) = −0.196, p=0.009**; deep-throw rate −0.176,
p=0.019. aDOT 7.91 under 28 → **7.62 at 32+**. `[TESTED]` **An ageing QB throws measurably shorter
while starting every week, and availability cannot see it.** Whether it costs fantasy POINTS is not
established (healthy-QB cut −13.8, p=0.438) and it may already sit inside the projection (§4.6).
The RB and WR equivalents — breakaway rate, yards after contact, deep target share by age — are not
run. Post-draft.

**STILL UNTESTED, and he named it: age conditional on a SITUATION CHANGE** — new team, new role,
new QB (his Randy Moss case). §4.21 measured the environment but never age × environment change.
Post-draft; it needs the 2023 and 2025 preseason pulls.
**AND THE METHOD POINT IS HIS:** *"the fact that you haven't found the signals is the short coming
instead of the fact players age."* That is the correct reading of an underpowered null, and §4.24(b)
already codifies it. **Report null, underpowered, AND what would resolve it — one of those sentences
invites more data and the other closes the file.**

**[v7.8] 4.25 RB AGE — UNDERPOWERED, NOT DISPROVED, AND HONOURING MATT'S RULE IS FREE — doc 201.**
Matt, 2026-09-06: *"At no point will i take Henry in the first... I don't want to be on the wrong
side of his age cliff."* Tested as the TAIL, not the mean — §0.5(a2), and the earlier "age is dead"
result was a continuous fit across all RBs, which is the wrong object for a cliff claim.
**POPULATION: 273 RB seasons, 2021–2025, with a §1.1 preseason ADP ≤ 180. BASELINE: half-PPR
weeks 1–14 minus what log(preseason ADP) predicts, fit within season. sd(beat) = 55.1.**

| age at Sep 1 | n | mean beat |
|---|---|---|
| <24 | 75 | −8.9 |
| 24–25 | 82 | +6.4 |
| 26–27 | 69 | +8.9 |
| **28–29** | **35** | **−12.1** |
| **30+** | **12** | **−4.0** |

**age ≥ 28: −12.1, p=0.209, boot CI [−29.4, +6.1]. age ≥ 30: −4.2, p=0.831.** `[TESTED]`
**NULL, direction slightly Matt's way, and UNDERPOWERED — against sd 55 at n=47, anything under
~22 points is invisible.** §4.24(b)'s distinction applies: this failed POWER, not PREDICTION. **No
monotone cliff:** 30+ is LESS negative than 28–29, and the 29+ tail is bimodal — Mostert −97.6 and
+149.1 are the same player two years apart. **Henry's own three seasons in the window: +38.4 at
29.7, +89.4 at 30.7, −9.1 at 31.7.** The 30+ population is 12 seasons in five years because teams
stop giving old backs the job, which is §4.20 restated: **buy the job, never the name.**
**AND THE COST OF HIS RULE IS ZERO, WHICH IS WHY IT STANDS (§0.5b).** Measured on the production
`Engine` at pick 8, `top=12, rollout_inner=60`: in the published state Henry is the **#2** row at
−7.9 behind St. Brown, so he never binds. In the only state where he is #1 — top seven **plus**
St. Brown gone — **James Cook III is −0.0 and Achane −0.1.** Passing on Henry at 8 costs **0.0
points**, and Cook's week-7 bye also steps off §4.11b's week-13 pile (Taylor, Jeanty, Henry, Hall,
Bowers, Flowers, Warren). **Preference honoured, no argument needed at the table.**
**METHOD NOTE, because it nearly shipped wrong:** removing Henry from the engine's pool measures a
world where he never existed (−8.5 for everyone, because the rollout's future gets worse) — not the
decision. **The decision is `cost vs #1` in the same state.** Same object-versus-question error as
§0.5(a2), caught before it was quoted.

**[v8.4] 4.26 TWO RESULTS FROM MATCHING OUTSIDE DRAFT STRATEGY TO OURS — doc 229.**

**(a) THE KEEPER RULE INVERTS: TAKE THE EXPENSIVE HIT, NOT THE BARGAIN.** `[TESTED, n=135]`
**POPULATION — state it every time: 2021–2024 top-12 finishers at RB and WR and top-6 at QB and TE,
scored weeks 1–14 under §2, who carried a §1.1 preseason ADP in the hit season AND were priced
again the next season. BASELINE: finishing top-12 (top-6 at QB/TE) again the following season.**

| price in the hit season | repeat rate |
|---|---|
| cheap, preseason ADP 61+ | **22.7%** (n=44) |
| expensive, preseason ADP ≤ 60 | **56.0%** (n=91) |

**+33.3 points, Fisher p=0.0004, and four of four positions point the same way** (QB is the
significant single cell at 10.0% vs 66.7%, p=0.011). The published figures — Dynasty Nerds,
26 May 2026, RB1 56.25% and WR1 48.84% over 2009–2025 — are correct and POOLED, which is §0.6.
**Why it binds HERE and not in most leagues: our keeper costs round 15 for anybody**, so the cost
advantage that normally offsets a bargain hit's lower repeat rate does not exist, and the repeat
rate is the whole of the decision. Same result as §4.18b from the other side (a kept RB returns
+6.7 VBD14, not +81), on a different outcome.
**AND THE ELIGIBILITY RULE FIGHTS IT.** Round 5+ only ≈ ADP 50+, so §2.1(a) draws the entire
candidate pool from the low-repeat band by construction. ~~**Among eligible candidates, prefer the one
drafted CLOSEST to round 5.**~~ **[v9.10, doc 382: WITHDRAWN AS A TIEBREAK INSIDE ROUNDS 5 TO 8.
Within ADP 50 to 96 the price carries nothing (log ADP −17.6, se 31, n=101 on the true 2024 ADP, doc 383)
and the late-season share change carries +42 top third against bottom third, net of price
[v9.13: +36 on four seasons, doc 385; price −20, se 24, n=138]. The band
effect above stands ACROSS bands; it was never measured inside one. §4.34 is the rule that replaces
this sentence.]**

**(b) THE TIGHT END'S WEEKS 15–17 DRAW IS THE ONE SCHEDULE EFFECT THAT MEASURES.** `[TESTED]`
**POPULATION: player-seasons 2022–2025, QB/RB/WR/TE, §1.1 preseason ADP ≤ 180, ≥1 game played in
the window, n=551. PREDICTOR: mean prior-season points allowed per game to his position across his
team's week 15/16/17 opponents — preseason-knowable. BASELINE: what log(preseason ADP) predicts,
fit within season × position. CLUSTERED BY NFL TEAM (A5).**
Per +1 sd of easier draw: **QB −0.71 (p=0.85) · RB −0.39 (p=0.66) · WR −0.47 (p=0.64) · TE +3.39
(p=0.031, n=70)**. The identical test on weeks 1–14 is **null at all four**. Positive in all four
seasons alone; leave-one-season-out β +2.54 to +4.35; per-game +1.12 (p=0.027); quartiles monotone
at −4.9 / +0.3 / +0.9 / +4.4, so **softest minus hardest ≈ +9 points across the three weeks**
(MWU p=0.093).
**MECHANISM, and it is why a three-week effect can exist where a season effect cannot:** the slate
measure's spread over three opponents is 1.5–2.5× its spread over fourteen. Tight end has the widest
ratio (2.47×) and much the widest relative spread — last season teams allowed **6.4 to 17.5** TE
points a game, a factor of 2.7 against ~1.4 at receiver.
**HOW TO USE IT: a tiebreak between two tight ends you rate the same, never a reason to move off a
better one, and never at another position.** One live cell out of ten tests.
**DOWNSTREAM CORRECTION (§0.2):** doc 212's "matchup is zero for WR and TE" is a WEEK-level
start/sit result and remains true as such. The wire sheet's sentence covered both objects and was
rewritten. `Source\pos_allowed_2025.csv` is the new input; `wire.py` prints the box and refuses to
render an empty one.

**(c) THREE NULLS WORTH KEEPING, AND ONE OF THEM IS A POWER STATEMENT NOT A REFUTATION.**
- **Positional runs.** Published: a player at the end of a run goes ~0.25 picks early (Fantasy
  Footballers, 19 Aug 2021, upd. 15 Aug 2025, 15 mock drafts). Ours, on 680 true selections with a
  §1.1 price: raw −7.3 picks (p=0.002) is a **round artifact** — demeaned within year × round it is
  −2.9, p=0.307. **Minimum detectable difference 6.3 picks against a claimed 0.25, so this test
  could not have seen it if it were 25× larger.** §4.24(b): failed POWER, not PREDICTION.
- **No QB run has ever happened in this room.** Max same-position QB streak is 3 across five drafts;
  P(next pick is a QB | this pick was a QB) is 2 of 14 in rounds 1–3 against a 10.4% base, and
  BELOW base in every later band. **§7's doc-142 §4a soft spot is smaller than it reads.**
- **Backs are not more fragile than receivers, a third time.** RB 10.66 games vs WR 10.90,
  p=0.551 (n=273/346), priced players 2021–2025 — after doc 42 and doc 131's 12.94 vs 12.95. This
  kills Zero RB's stated PREMISE only; its inheritance channel is a different claim and is untested.

**[v8.7] 4.27 WALLY PIPP, MEASURED — IT IS A RUNNING-BACK EVENT AND THE TRIGGER IS PRODUCTION —
doc 244.** Matt's phrase and his mechanism: *"a temporary replacement performed so well that they
took over your role."* Doc 236 measured what the next man scores WHILE the starter is out; nothing
had asked whether he KEEPS the job.
**POPULATION: every team-season 2021–2025 where the weeks-1–4 usage leader at a position group later
missed a week AND CAME BACK — 88 events.** (If he never comes back the job was vacated, a different
event.) **BASELINE: the replacement's share of team usage — carries + targets at RB, targets at
WR/TE — in the weeks BEFORE the absence. OUTCOME: his share in the first 4 weeks after the starter
returns, minus that.**
**THE UNCONDITIONAL AVERAGE IS NULL AND +9.8 MUST NOT BE QUOTED.** The first pass gave RB +9.8 pp,
CI [+4.4, +15.4] — contaminated by **stars returning from an early-season absence** (Chubb 2024,
Kamara 2023, Jacobs 2021 were all scored as takeovers). With the guard — the replacement must have
played 2+ of weeks 1–4 and been under 60% of the lead man's early usage — **RB drops to +4.2 pp,
CI [−1.5, +10.1]** and WR/TE to **−0.9 pp, CI [−3.1, +1.3]**. It failed its own falsifier.
**THE CONDITIONAL EFFECT IS THE ONE HE DESCRIBED AND IT IS STRONG.** RB, n=40, median relief scoring
11.2 half-PPR ppg: **produced in relief +12.4 pp [+4.2, +21.1] · did not −4.1 pp · difference
+16.6 pp, p=0.006** (permutation, 4,000 draws). `[TESTED]` **A back who produces keeps a fifth of
the job; a back who does not LOSES ground.** §0.5(a3) again — the average is null, the subgroup is
+12.
**THE ECONOMICS HE PROPOSED DO NOT SHOW UP.** Rookie deal (≤3 yrs) +2.1 pp, p=0.73 · three-plus
years younger −1.4, p=0.85 · younger than the starter +10.8, p=0.079 (his direction, suggestive) ·
starter 27+ +8.6, p=0.23. **Being cheap and young is not what moves the job; being good in the two
weeks you get is.**
**AND ONE THAT INVERTS THE INTUITION: a SHORT absence is more dangerous to the starter than a long
one — 3+ weeks out measures −10.6 pp against one or two, p=0.108.** `[SUGGESTIVE]` A long absence
gets planned around and the starter walks back into a defined role; **a one- or two-week cameo with
a big number is what flips a job.** Stevenson 25.4 ppg over one week, Dowdle 31.4 over two,
Monangai 21.3 over one.
**WHY IT IS NULL AT RECEIVER, AND IT IS STRUCTURAL: a backfield is ONE job and a receiver room is
three to five.** An absent WR1's targets scatter, every other receiver already has a defined role,
and the incumbent walks back into his. **Do not build a receiver handcuff flag — for THIS event.**
**BOARD IMPLICATION:** `dart_shape` should be conditioned on the man ahead, not merely on there
being one. The live trigger is *the starter's fragility × the backup's ability to produce in two
weeks*, and doc 236's availability table plus a per-game rate already hold both.
**[v9.4] SUPERSEDED IN THE CODE, AND THIS PARAGRAPH WAS NEVER UPDATED: BOTH GATES BELOW ARE GONE.** Doc 275
tested gate 2 forward (a backup's best two weeks last season against his relief scoring, rho +0.006, n=39) and
made 11.2 a label only; doc 276 found gate 1's fragility split null (45.9% against 46.3%, n=115) and removed it.
The wire's inheritance list now sorts direct backups by the job. **Doc 276's null is itself under re-check**
(doc 290 item B4: its population held only backs who were healthy through week 4).
**[v8.9] THE APPLIED FORM, AND THE FIRST VERSION OF THE WIRE LIST BROKE IT — doc 251.** Ranking
unowned backs by `job_ceil` alone surfaced third- and fourth-string bodies behind healthy elite
starters. **That is the Spears error of doc 240 in a new place.** The list is two GATES and then a
sort, never a sort alone:
- **Gate 1, fragility:** the man ahead missed a game last season, or carries a news-override flag.
- **Gate 2, can he produce:** the backup's best CONSECUTIVE TWO-WEEK stretch last season averaged
  **11.2 half-PPR a game** or better — the median relief rate across this section's 40 events, and
  the right object because the finding is about a two-week cameo, not a season rate.
- **Direct backups only (depth 2).** Then rank the survivors by the job.
**AND JOIN ON A NORMALISED NAME OR NOT AT ALL (§3):** the depth map's `ahead` field and
`games_2025.csv` disagree on suffixes and capitalisation (`Christian Mccaffrey`, `Kenneth Walker`),
and the first run silently printed `?` for the man ahead's availability on 4 of 13 rows — the
availability half of the gate, missing, with no error. **Assert on the join; never default it.**

**[v8.7] 4.28 RECEIVER TURNOVER IS REAL AND THE DISPLACER IS AN INCOMING FIRST-ROUND ROOKIE —
doc 245. THIS CORRECTS §4.27's LAST PARAGRAPH AS A GENERAL CLAIM.** §4.27's receiver null is about a
**two-week cameo**. Matt's claim was about a **season boundary**, and writing "the mechanism isn't
there at receiver" generalised one into the other — §0.5(a2), mine.
**POPULATION: every team-season 2021–2024 where one receiver led his team with 60+ targets and was
still on the roster the next year, paired with each teammate at ≤3 years' experience — 372 pairs.
OUTCOME: the young teammate out-targets him the following season.**
**BASE RATE 9.9% — 37 displacements in four offseasons.** `[TESTED]` And not only weak incumbents:
**Nacua over Kupp · Egbuka over Mike Evans · Smith-Njigba over Lockett · Tre Tucker over Davante
Adams · Addison over Justin Jefferson (108–100) · Odunze over DJ Moore · Michael Wilson over Marvin
Harrison Jr.** **His "there wouldn't be turnover if not" is confirmed by count.**
**EVERY INDICATOR HE NAMED IS NULL AND TWO POINT BACKWARDS.** separation above median +5.5 pp
(p=0.60) · separates more than the incumbent +6.1 (p=0.61) · forty under 4.45 +2.0 (p=0.68) · faster
than the incumbent +2.9 (p=0.63) · **changed teams −6.2 (p=0.16)** · **entering year 3 −3.1
(p=0.46)** · incumbent 28+ +4.6 (p=0.20). Combinations all null on cells of 11 to 29.
**TWO WARNINGS ON THOSE ROWS:** the separation rows run on **81 of 372 pairs**, because NGS only
gives a season line to a receiver who already has volume — a selection group whose base rate is
22%, not 9.9% (§4.23's trap in a new place). And the whole design is **UNDERPOWERED**: against a
9.9% base rate it needs a 10–12 point difference to see anything. `[TESTED, null, underpowered]`
**THE ARCHETYPE THE DATA DOES SHOW, AND NEITHER OF US NAMED IT.** By the challenger's year:
**year 1 = 14 · year 2 = 8 · year 3 = 7 · year 4 = 8.** **NINE OF THE FOURTEEN ROOKIE DISPLACERS
WERE FIRST-ROUND PICKS** (Olave, G. Wilson, Addison, Johnston, Legette, Nabers, Worthy, McMillan,
Egbuka), plus Wan'Dale in round 2, Ayomanor and Dike in round 4, **Nacua in round 5** and Shaheed
undrafted. **Receiver turnover mostly walks in the front door with draft capital.**
**[v8.9] AND THAT SENTENCE IS NOW A RATE — doc 251. NINE OF FOURTEEN WAS A NUMERATOR WITHOUT A
DENOMINATOR AND MUST NOT BE QUOTED AS A RATE.** Same pair set, restricted to challengers in their
FIRST NFL season, teammates who played ≥1 game (n=364, base rate 9.6% — reproduces this section's
9.9%):

| challenger, year 1 | n | displaced | rate |
|---|---|---|---|
| **NFL round 1** | **15** | **9** | **60.0%** |
| NFL rounds 2–3 | 30 | 1 | 3.3% |
| NFL round 4+ / undrafted | 293 | 4 | 1.4% |
| everyone else in the pair set | 349 | 26 | **7.4%** |

**Round 1 vs everyone else: Fisher two-sided p = 0.000001.** `[TESTED, n=364]` On the looser
population (every rostered teammate, n=794, base 4.4%) it is 9 of 16 = 56.2%, p<0.000001 — **the
effect does not depend on the population choice.** **THE CLIFF IS AT ROUND 1, NOT ROUNDS 1–3** —
§4.30's composite uses rounds 1–3 because it predicts a three-year conversion; this is a one-year
event and it is a first-round event.
**AND IT CONVERTS TO THE CURRENCY THAT MATTERS.** Rookie season, weeks 1–14, half-PPR per game
against doc 12's WR replacement of 9.62: **the 9 who displaced — 6 startable, mean 9.77 · the 7 who
did not — 0 startable, mean 6.18.** So **40% of all first-round rookie receivers in this spot were
startable in year one** (Nabers 12.74 · McMillan 11.32 · Olave 11.23 · Egbuka 11.12 · G. Wilson
10.98 · Addison 10.88). **Two of the seven misses lost by a single target** (Pearsall 46–47, Golden
44–46) and two were non-football (Jameson Williams on a torn ACL, 2 games; Travis Hunter playing
both ways, 0 targets).
**WHY EVERY INDICATOR ABOVE WAS NULL AND THIS ONE IS NOT: they were all attempts to out-scout the
NFL draft. Draft capital IS the scouting, already aggregated, already public, and free.**
**n=15, and it will be 19 after this season.** The size is not in doubt; the precision is.
**THE BOARD IS MISSING ONE COLUMN AND IT IS FREE.** **Jordyn Tyson was the 8th overall pick of the
2026 NFL draft** `[SOURCED: nflverse draft_picks, 2026]`, and our board had him at **82.0 points,
81.5 BELOW receiver replacement**, priced inside §4.14's fabricated blob. §4.13's RB composite
already uses "NFL rounds 1–3" and was never extended to receivers. **PUT NFL ROUND AND OVERALL PICK
ON THE BOARD.** 2026 first- and second-round receivers: Tate (4, TEN) · **Tyson (8, NO)** ·
Lemon (20, PHI) · **Concepcion (24, CLE)** · Cooper Jr. (30, NYJ) · Stribling (33, SF) ·
Boston (39, CLE) · Bernard (47, PIT).
**OUTSIDE RESEARCH, dated (B7): 4for4, 8 July 2024** — the most STABLE receiver trait is not
production, it is **role: slot rate 0.75**, ahead of targets per game 0.70, points per game 0.68,
aDOT 0.65, targets per route run 0.64; least stable are route rate 0.01, contested catch 0.02, drop
rate 0.14, TD rate 0.19. **That is Matt's own "there isn't one type of WR."** ~~It is the one indicator we still cannot compute,
BLOCKED on a true slot rate.~~ **[v9.4] Not blocked: `pff_receiving_2022-2025.csv` carries `slot_rate`
(doc 263), and docs 284 and 287 already use it.**

**[v8.7] 4.29 THE DRAFT GRADE'S BACK HALF IS VOID — doc 242.** Across rounds 7–12, all 12 managers,
**62 picks**, `draft_analysis.json`'s "best available" comparator was one of **six** players, and
**50 of 62 (81%) were a tight end** — Dallas Goedert alone 34 times. **The grade measures dart count,
not drafting.** Cary's −109.6 and his last place are retracted; 88% of his charged gap and 94% of
Matt's sits in rounds 7–12. Rounds 1–6, against real ADP and real replacement, survive. **Matt
called this before it was measured:** the grade could not see upside. **[v9.4] His claim was never that
upside cannot be measured; it is that potential value is the right currency at the bottom of the roster,** and
§4.28 and §4.30 are what the grader could not see.

**[v8.8] 4.30 THE RECEIVER COMPOSITE — THREE SIGNALS FROM THE OUTSIDE VOCABULARY, TESTED ON OUR
OWN ROWS — doc 248.** Matt: *"explore what other people have recognized this signals. maybe it turns
out to be fluff, but sometimes there is a real indicator when taken together with other factors."*
**POPULATION — state it every time: WR seasons 2021–2024, years 1–3, who were NOT startable (under
9.62 half-PPR ppg, doc 12's WR replacement, which is §4.1 ÷ 17 **[v9.4]**), 4+ games, and who played 4+ games again the
next season. n=185. OUTCOME: startable the following season. BASE RATE 11.4%.** Permutation, 6,000.

| the composite: count of three | n | rate |
|---|---|---|
| 0 signals | 23 | **0.0%** |
| 1 | 40 | 5.0% |
| 2 | 56 | 7.1% |
| **3 of 3** | **33** | **39.4%** |

**THE THREE: NFL draft rounds 1–3 · yards per target > 7.13 · targets per game > 3.20.**
**3-of-3 against under-3: +34.4 points, p=0.0000, and 13 of the population's 21 converters sit in
that cell — 62% of the hits in 22% of the players.** `[TESTED, n=152 with complete data]`
**Singly:** targets/game +18.5 (p=0.000) · team target share +16.3 (p=0.000) · **draft round 1 +25.5
(p=0.001)** · **yards per target +14.4 (p=0.004)** · rounds 1–2 +15.5 (p=0.007) · rounds 1–3 +12.0
(p=0.044).
**RECEIVING EFFICIENCY — PLAIN YARDS PER TARGET — IS NEW TO THIS PROJECT** and came off a
**PlayerProfiler article dated 14 Mar 2020** (B7). Nothing here had ever looked at it.
**FLUFF ON OUR ROWS, and two of them are the outside sources' own headline metrics:** **weight
+2.3 (p=0.80)** — PlayerProfiler calls it *"the most positive indicator of future NFL success"* —
**average target distance −2.2 (p=1.00)**, age +6.1 (p=0.31), and **speed measures BACKWARDS a third
time: forty faster than 4.43s = −7.7 points**, after doc 245's displacement null and doc 246's growth
curve. Three objects, three negative signs. **Separation (+6.7) and air-yards share (+11.1) are the
right direction and UNRESOLVED**, on 45-row NGS subsamples that are themselves volume-selected —
§4.23's trap.
**IT IS A 39% SCREEN, NOT A PROPHECY.** Rashod Bateman scored 3-of-3 twice and fell to 3.82; Treylon
Burks, Kadarius Toney, Rondale Moore and Terrace Marshall all cleared it and fell.
**BLOCKED, INPUTS NAMED (§0.5a4): Breakout Age and College Dominator Rating** — every outside source
leads with them and both need a college receiving table nflverse does not carry; `draft_picks.csv`
holds a `cfb_player_id`, so the join key exists, and LevelUpFantasy and PFF both publish the data.
**Slot rate** (4for4's most-stable trait at 0.75) and **targets per route run** (0.64) are PFF fields,
**and both are on the drive (doc 263) [v9.4].**
**HOW TO USE IT: as a screen on young non-startable receivers, on the wire and at the late picks —
never as a per-player forecast (§4.13d still holds: nothing here computes a ceiling).**

**[v9.0] 4.31 THE WAIVER HIT RATE IS FLAT ALL SEASON, AND WEEK 1 IS THE WORST WEEK — doc 252.**
Matt asked whether the rate falls late because the pool is picked over.
**POPULATION — and state what it excludes: every EXECUTED add in this league 2022–2025 that matched
a QB/RB/WR/TE weekly line, n=718 in weeks 1–14. That is 58% of the 1,230 executed adds; 248 (20.2%)
are D/ST and are NOT in it** (§0.6, doc 228's own dataset). **BASELINE: points per game from the add
week onward reaching the position's replacement rate — QB 20.09 · RB 9.92 · WR 9.62 ·
TE 8.25 (doc 12; **[v9.4] derived from §4.1 ÷ 17, not measured**). Two outcomes: A = rest of season through wk 14; B = the NEXT FOUR WEEKS, which
removes the shrinking-window confound.**

| add week | n | A | B |
|---|---|---|---|
| **1** | 32 | **12.5%** | **9.4%** |
| **2** | 52 | 26.9% | **34.6%** |
| 3 | 52 | 17.3% | 15.4% |
| 4 | 50 | 24.0% | 26.0% |
| 5–8 | 247 | 19.8% | 25.1% |
| 9–14 | 285 | 22.1% | 21.4% |

**FLAT: rho(week, hit) = +0.045 on A (p=0.234) and +0.003 on B (p=0.926). Weeks 2–4 vs 9–14 is
22.7% vs 22.1%, p=0.905.** `[TESTED, n=718]` Every position holds its own average in all three week
bands — RB 19/14/18, WR 20/21/19, TE 21/27/28, QB 28/24/26. **The RB row is §4.19 from the other
side: a one-in-six shot in September and a one-in-six shot in December.**
**THE ONE REAL RESULT IS WEEK 1 AND IT IS NEGATIVE: 9.4% against week 2's 34.6%, Fisher p=0.010**
(9.4% vs 23.6% against every other week pooled, p=0.083, n=32). Our own timestamps say why — the
32 week-1 claims were executed between the Thursday opener and Sunday night, most before or during
the first slate. **A week-1 claim bets on a depth chart; a week-2 claim bets on a snap count**, and
doc 235 already measured that the workload is the thing that predicts.
**THIS QUALIFIES DOC 250 (§0.2).** *"Claim often and claim early, failure is free"* — the free half
is untouched (no FAAB, No Limit, order resets weekly on standings, the only cost is the drop).
**"EARLY" NOW MEANS WEEK 2.** One week of patience measures at roughly three times the hit rate.
**AND MATT'S SCARCITY MECHANISM IS HALF CONFIRMED — the half neither of us expected.** The pool was
rebuilt week by week from the draft plus all 1,230 executed adds and drops in date order.
**Usable-and-free players (averaging replacement over the next four weeks) fall from 13.8/16.8/15.5
in weeks 1/2/5 to 10.0/10.0/9.8 in weeks 9/11/12** while the rostered population grows 178 → 225.
**Free startable RBs go 3.5 in week 2 to 0.8 in weeks 7 and 9 — in half the league-weeks after week
6 there was NOT ONE startable back on the wire.** `[TESTED, n=56 season-weeks]` **But the ceiling
does not fall: the best free player is worth 22–26 a game in nearly every week.** There are fewer of
them; they are not worse. **So scarcity is real AND free.** The only account consistent with both
tables is that the survivors get easier to identify as the pool shrinks — **that is an INFERENCE,
not a measurement, and it is flagged as such.**
**OUTSIDE, DATED (B7):** nobody publishes this. Six searches returned advice columns. The two
usable dated sources are **Fantasy Footballers (pub. 13 Sep 2021, upd. 15 Aug 2025, nflfastR,
half-PPR, 2015+)** — a week-1 "wonder" beats his ADP 58% of the time but finishes top-12 only
**13%** and top-24 39%, the same shape as our 9.4% on a different population — and **4for4
(28 Aug 2023)** quoting Fitzmaurice's FAAB split QB 1% / RB 8.1% / WR 9.1% / TE 5.7%, **which does
not apply to us because we have no FAAB.** Its 28 Aug 2026 successor carries no numbers at all.
**NOT YET RUN, with the inputs named:** ~~the D/ST version (blocked, §2 records no D/ST scoring
rules)~~ **[v9.4] the D/ST version was run in doc 265: flat by add week, managers' edge unresolved** · whether claim ORDER raises landed value (`waiver_report_*.csv` holds it) · the legibility
test (of the free-and-usable pool in week W, what share is claimed within two weeks — rising over
the season is the cancellation story).
**[v9.1] SCOPE — AND I MISAPPLIED THIS SECTION WITHIN AN HOUR OF WRITING IT (docs 253, 258).**
**§4.31 measures whether a CLAIM BECOMES A SEASON ASSET. It does not govern two other decisions
that look like it:**
1. **FILLING AN EMPTY STARTING SLOT.** There the alternative is **zero**, not a replacement-level
   body, and almost any startable player wins. The 9.4% is the chance a week-1 add becomes a
   season starter; it is not the chance he outscores nobody. Doc 253.
2. **A FORWARD CLAIM ON A SCHEDULE.** Week 1 is bad because it bets on a **depth chart** before any
   football. A week-12 claim for a week-16 defensive matchup bets on the **schedule**, fixed since
   May. Same calendar direction, opposite epistemics. Doc 258.

**[v9.1] 4.32 THE CLAIM LIST IS A CALCULATION, NOT A RANKING RULE — docs 255, 256, 257.**
**THE MECHANIC FIRST, because two thirds of it was stated wrong three times:**
- **ACROSS weeks the order resets to inverse standings** (settings file). Winning last week does not
  push him back this week.
- **WITHIN a run the first claim that clears spends his position** — ESPN Fan Support: *"once a team
  successfully makes a waiver claim, they move to the bottom of the waiver priority list."*
- **AND THERE ARE TWO RUNS A WEEK, so the penalty lands inside the same week.** Matt's fact, not
  measured here; the settings record *"Waiver Period: 2 Days"*, which is a period LENGTH, not a run
  COUNT. **The resource is one turn at his real priority, twice a week.**

**THE SIX TERMS. Five are already computable; the sixth is bounded.**

| # | term | status |
|---|---|---|
| 1 | what he adds to the nine Matt actually starts, **over the weeks he is NEEDED** | HAVE IT — `_lineup()`, and byes are deterministic |
| 2 | the next-best body at that position — his bench, then the free pool | HAVE IT — doc 252 rebuilt the pool by week |
| 3 | *(folded into 1: the horizon is term 1's index)* | — |
| 4 | P(a team **ahead of him** also files) | **NOT YET RUN** (doc 254); **BOUNDED** by doc 224's 56% uncontested / 16% contested |
| 5 | recovery if lost — run 2, then free agency | **the term neither of us had.** Losing a claim DELAYS a player; it rarely removes him |
| 6 | the drop | HAVE THE METHOD — doc 240 prices a bench spot against its best alternative use |

**THE HISTORY, KEPT BECAUSE THE SWING WAS THE DEFECT.** Doc 255 turned Matt's crude example into a
rule ("order by contestedness × value"). Doc 256 demoted it to a tiebreak. **Both were wrong the
same way — I ruled on the VERDICT instead of filling in the TERMS**, and "treat it as a tiebreak" is
§0.5(a4)'s forbidden fourth answer wearing a suit. **His own objections — *"my real need is WR"* and
*"that RB may be a bye-week fill-in"* — were INPUTS, not arguments against the calculation.**
**HOW TO USE IT TODAY:** rank by term 1, let term 4 break near-ties against teams **ahead** of him,
and remember term 5 — going second on a man usually costs a delay, not the man.

**[v9.1] 4.33 WHERE THE STRIKES MATTER — doc 227 §3b, restated because Matt asked the right
question and the answer was already measured; plus doc 259 on his own roster.**
Prior-season opponent quality — the version you can act on, not hindsight:

| position | matchup swing | spread between the PLAYERS | matchup as a share |
|---|---|---|---|
| **D/ST** | **2.22** | 2.06 | **108% — chase the matchup** |
| QB | 1.13 | 4.84 | 23% |
| RB | 0.56 | 5.18 | 11% |
| TE | 0.15 | 3.07 | 5% |
| WR | 0.09 | 4.29 | 2% |

> **AT DEFENCE TAKE THE SCHEDULE. AT EVERY OTHER POSITION TAKE THE PLAYER.** "Strong matchups
> everywhere" is not a thing to fail at — it is worth about a point a week at QB and nothing at
> receiver and tight end.
**AND THE HORIZON MULTIPLIES IT AT D/ST ONLY: best-to-worst spread is 3.56 over ONE week and 11.72
over FOUR** (doc 212). Planning ahead roughly triples the signal.
**BUT NOT AT THE SKILL POSITIONS, AND TWO OF OUR OWN DOCS DISAGREE ABOUT THE TIGHT END.** Doc 10
puts the whole 32-team weeks-15–17 spread at **≤5.5 points** and says in terms *"it is not a
playoff-planning tool"*; §4.26(b) puts the TE draw at **+3.39 per sd, softest minus hardest ≈ +9**.
**Different methods, same position, same window. `[OPEN]` — settle it before building any
playoff-planning tool on either.**
**ON HIS ROSTER (doc 259, board projections ÷ 14): the best FREE body is below his worst startable
man at every position** — best free RB 6.51 against Dowdle 12.24, best free WR 8.94 against Worthy
10.40. **The wire cannot upgrade a working slot; it can only fill a broken one, and the same free
player is worth zero as an upgrade and the full 10.7 in an empty week-6 tight-end slot.**
**One live row: Daniel Jones 21.87 against Tyler Shough 21.92 — 0.05 a game**, so that bench spot is
worth almost nothing over a free agent. `[OPEN — projections do not price missed weeks; re-run
§4.17's argument on the live roster before acting.]`
~~**AND THE TRADE LANE IS NEARLY CLOSED HERE.**~~ **[v9.4] RETRACTED by doc 262 (the old header said so; the
body did not): the lane is active and hard to close.** 45 proposals in 2022–2025, about 11 a season; 14
accepted, a 31% close rate counting accepts (whether a veto undoes an accept is not established, so treat 31%
as an upper bound). Matt proposes more than anyone (9), and every offer he has received came from one manager.
`trade_report_2022-2025.csv` exist (written 10 Sept). His own read stands as his: *"trades are not frequent in
my league, and when I get offers they are most often unbalanced significantly in their favor."*

**[v9.10] 4.34 THE RISER AS A KEEPER: THE LATE-SEASON SHARE CHANGE DECIDES INSIDE ROUNDS 5 TO 8, AND
PRICE CARRIES NOTHING THERE, doc 382 (Fable), `[TESTED, n=334 pooled, n=107 in the band; 2022 to 2024]`.**
**[v9.13, doc 385: now `[TESTED, n=496 pooled, n=138 in the band; N = 2021 to 2024]`, all five registry years on
the half-PPR page. The fourth bullet below carries the numbers to quote.]**
Matt, 16 Sept: *"the model steered me to players who don't have that upside potential as keeper
candidates because they are not risers. That value was never measured."* Now it is.
**POPULATION, state it every time: player-seasons in year N at QB/RB/WR/TE with a §1.1 preseason ADP
of 50 or later in N and priced again in N+1; N = 2022, 2023, 2024 (no 2021 weekly file). [v9.13: N = 2021 to
2024 since doc 385; the 2021 weekly file is in the cache.] The "priced
again" condition drops 41% of the band; every number below holds or strengthens without it (n=433).
PREDICTOR: his share of team opportunity (carries plus targets at RB, targets at WR/TE, attempts at QB)
in weeks 10 to 14 of year N minus weeks 1 to 5. CONTROL: log preseason ADP and position. BASELINE:
§4.18b's VBD14 (N+1 weeks 1 to 14 minus the same season's RB30/WR30/QB12/TE12) and §4.13b's absolute bar.**
- **Pooled (n=322 on the true 2024 ADP): +5.7 VBD14 per ten points of team share gained, net of price
  (se 1.8); top third of risers against bottom third +16.6 [2.6, 29.2]; startable next season 38% against
  31% at each man's own price. Do not quote the pooled number: it averages a band where the effect is 42
  and a band where it is 2.** (Rank proxy, n=334: +6.0, gap 18.0 [4.0, 29.4].)
- **ADP 50 to 96 (rounds 5 to 8): +10.5 per ten (se 3.2); top third +3.2 VBD14 and 56% startable,
  bottom third −38.7 and 32%; gap net of price +41.9 [11.2, 70.6], n=101. Price inside the band: log ADP
  −17.6 (se 31), nothing.** At every position the man whose share fell is the one not to keep.
  **[v9.11, doc 383: these are the numbers on the TRUE 2024 preseason ADP. Doc 382 and v9.10 measured the
  same population on the 2024 consensus-rank proxy and read +52.1 [26.3, 78.3], n=107, 56% against 25%;
  same rule, smaller number, and that version must not be quoted.]**
- **ADP 97+ (round 9 and later, n=221): +1.8 per ten (se 2.2); a rising round-9+ man was startable 31%
  and returned −40. §4.18b stands untouched: the riser matters where the band already says audition.**
  (On the rank proxy: +1.4, se 2.0, n=227.)
- **[v9.12, doc 384] ON THE THREE-YEAR FANTASYPROS HALF-PPR REGISTRY (2022 and 2023 replaced, doc 384),
  the numbers above are superseded and these are the ones to quote:** pooled n=333, +4.3 per ten (se 1.8),
  gap +17.8 [4.7, 31.8]; **band 50 to 96, n=100: +17.2 per ten (se 3.4), gap net of price +51.0 [18.5, 73.4],
  startable 56% against 29%, price inside the band −31.6 (se 28), nothing**; ADP 97+, n=233: −0.1 per ten
  (se 2.0), gap +6.5 [−7.9, 23.0]. Sensitivities: without "priced again" the band gap is +53.8 [27.6, 79.0]
  (n=102); with a missing window scored zero, +55.2 [28.9, 78.7] (n=110). Twelve men changed side of the
  round-9 line between the registries. The verdict has now held on three instruments.
- **[v9.13, doc 385] ON FOUR SEASONS, WITH ALL FIVE REGISTRY YEARS ON THE HALF-PPR PAGE (Matt's 2021 and 2025
  exports, 22 Sept; N = 2021 to 2024), the v9.12 numbers are superseded and these are the ones to quote:**
  pooled n=496, +3.3 per ten (se 1.5), gap +15.3 [4.1, 26.0]; **band 50 to 96, n=138: +13.6 per ten (se 3.3;
  +13.5, se 3.3, with season fixed effects), gap net of price +35.6 [9.3, 56.0], startable 54% against 30%,
  price inside the band −20.3 (se 24), nothing**; ADP 97+, n=358: +0.2 per ten (se 1.7), gap +12.5
  [−0.8, 24.2], not resolved. **THE EFFECT IS NOT EVEN ACROSS SEASONS.** Band slope per season: 2021 −11.0
  (se 9.2, n=36), 2022 +17.2 (se 4.2), 2023 +18.7 (se 7.2), 2024 +9.3 (se 10.0). Without 2022 the band gap
  is +17.8 [−8.9, 42.8]; without 2023 +27.2 [−14.9, 49.6]. **That was already true of doc 384's own rows
  (without 2022: +29.1 [−8.0, 60.5]) and nobody ran it**; `j4_band_loo.py` runs it now. The falsifier's
  second branch (a floor of ten or more) sits on its edge at 9.3. Instrument check: on the full-PPR pages
  for 2021 and 2025 (the 06:30 build) the band gap is +43.1 [18.5, 61.7], n=137. The deeper 2025 file also
  moved N=2024 from 90 to 134 men, because the old 183-row file failed "priced again" for anyone it did not
  list; on three seasons with it the band gap is +53.8 [21.2, 74.1], n=102.
- Availability held out (share in games played only): +6.6 per ten (se 2.4), RB +15.5 (se 5.9). A role
  change, not a health record. Year N against N-1 share: +2.9 (se 2.3), the weaker instrument; use the
  in-season windows.
- ~~**Youth × trajectory: AMPLIFICATION.** Riser worth +3.3 per ten for a fourth-year-or-later man and
  about +11.8 for a man in his first three seasons (interaction +8.5, se 3.9); same sign in all four
  populations run, past two standard errors in two. The direction §4.30 found at receiver, not doc
  191's substitution at RB. Suggestive, not settled.~~ **[v9.12, doc 384: WITHDRAWN. The interaction was
  +8.5 (se 3.9) on the rank proxy, +6.8 (se 4.0) on the true 2024 ADP, and −0.4 (se 3.9) on the half-PPR
  registry; inside the band +24.9 (se 10.7) became +13.8 (se 10.3). A number that changes sign when the
  market file changes is not a finding. Youth is not a tiebreak; the riser is.]** **[v9.13, doc 385: on four
  seasons −1.3 (se 3.2) pooled and −6.8 (se 8.1) inside the band. Stays withdrawn.]**
- The §4.18b object: among 114 year-N hits, share rose → +3.9 VBD14 next season and 45% still above
  replacement; share fell → −18.0 and 34%. Net of price and hit size +4.2 per ten (se 5.8),
  underpowered at 38 a cell; **the size of the hit itself predicts nothing (0.02 per point, se 0.20).**
- ~~Registries differ by year (2023 Underdog best-ball, 2024 a rank proxy)~~ **[v9.12] 2022, 2023 and 2024
  are one instrument now (FantasyPros half-PPR, doc 384)** **[v9.13] and so are 2021 and 2025 (doc 385)**; on the old files, without 2024 the pooled gap
  was 20.3 [3.1, 35.3]. Name join with 13 generated fallbacks, 71 unmatched (56 of them the 2024 registry's
  kickers and defences).
**THE RULE: among round-5-to-8 keeper candidates, keep the one whose late-season share rose, and treat
a fall as a reason not to; price inside the band is not a tiebreak (4.26(a) amended). Round 9+ stays a
dart. [v9.13] Measured on four seasons and carried by two of them: quote +36, not +51, and say it is uneven. The finisher, NOT YET RUN and Fable's: the keeper-riser line on `WEEK_SHEET.html` for every
round-5-to-8 man on the roster, from `form_2026.csv`.**

---

**[v9.14] 4.35 THE SPIKE WEEK CANNOT BE CALLED. THE BEST SIGNAL WE HOLD TAKES A CLAIMABLE RECEIVER FROM 4% TO 10%,
AND TARGETS ALONE IS THE WEAK HALF OF IT, doc 389, `[TESTED, n=8,651 player-weeks, 2021 to 2025]`.**
Matt, 22 Sept: *"I wish there was a way we could have predicted the break out for him. We need more news and signals
for these players is my guess."*
**POPULATION, state it every time: WR and TE player-weeks, regular season 2021 to 2025, who were NOT startable in week
w on §4.13b's bar (WR 9.62, TE 8.25), had at least one target in w, and played in w+1. That is the claimable pool:
8,651 weeks, WR 5,699, TE 2,952. PREDICTORS, all from week w and all already in the nflverse weekly file
`build_form.py` downloads: targets, target share, air-yards share, WOPR (1.5 x target share + 0.7 x air-yards share).
OUTCOME: a SPIKE in w+1, 18.0 or more on §2's scoring, which is what Tre Tucker's week 2 was (20.4). BASELINE in the
pool: spike 4.3%, startable 21.2%, mean 5.50 points.**
- **Top fifth by WOPR: spike 10.1%, startable 38.4%, 8.73 points next week. Top fifth by targets: 9.6% and 37.0%.
  Top fifth by air-yards share: 9.2% and 35.0%. Bottom fifth by WOPR: 0.8% and 7.7%.** The signal is real and the
  ceiling is low: **the best fifth of the pool spikes one week in ten.**
- **WOPR beats raw targets by half a point of spike rate, which is nothing** (se about 0.7 on each). **The gain is in
  the CROSS, and that is the actionable part: top fifth on targets AND on air-yards share 10.8% / 39.8% (n=1,220);
  targets only 6.7% / 30.1% (n=511); air-yards share only 8.4% / 35.0% (n=511); neither 2.6% / 15.8% (n=6,409).**
  ~~A man who clears a workload screen on TARGETS ALONE is barely better than the pool he came from.~~
  **[v9.32, doc 435, reproduced cold from the nflverse cache: those four cells match TARGETS x WOPR to within two
  rows and 0.4 points, not targets x air-yards share. "Targets only 6.7%" is really "top fifth on targets but not on
  WOPR". On the true targets x air-yards cross: both 10.8% (n=969), air-yards only 7.3% (n=762), targets only 8.0%
  (n=762), neither 2.4%. So targets alone is nearly double the pool, not barely better, and the both-cell gain over
  targets-only is about 2.8 points (se about 1.1), not 4.1. The screen ordering stands; the sentence about targets
  alone is weakened, not killed.]**
- **LIVE CHECK, 2026 week 1 into week 2** (same definitions; 122 claimable men, 7 spikes, 5.7%): the top fifth by
  week-1 WOPR caught **2 of the 7**. Tre Tucker sat at the **67th percentile** on WOPR, 65th on targets and 72nd on
  air-yards share, and scored 20.4 on 5 catches for 119 yards and a touchdown with **50.5% of Las Vegas' air yards**
  that day. Davante Adams, 4.1 points in week 1, scored 35.5. **Nothing we hold would have named either.**
- **THE ABSENCE DISCOUNT** (the second test in the same script): inside the top fifth, when the team's alpha (highest
  target share over the prior three weeks, at least 20%) was OUT in week w, the next week spiked **5.0% (n=160)**
  against **6.7% when the alpha played (n=1,172)**; startable 25.0% against 30.7%. Direction is Matt's and it is about
  one standard error. **Underpowered: do not quote it as a rule.** (The rates differ from the first bullet because
  this pool needs three prior weeks and a 20% alpha, so it drops weeks 1 to 3.)
- **WHAT THIS DOES NOT COVER, and the honest answer to the "more news" half:** the nflverse injuries feed (weekly
  practice and game status, about 50 KB a season, `injuries/injuries_<season>.csv`) is held and unused. ~~The first
  reports for a week land on Wednesday, after the Tuesday waiver run, so it can inform a Sunday lineup or a Thursday
  free-agent add and never a Tuesday claim.~~ **[RETRACTED same day, doc 391, §4.36. THERE IS NO TUESDAY RUN.**
  `Waiver Period: 2 Days`, so a claim runs on the morning of the day it was placed plus two. The feed's Wednesday
  arrival is late for a claim placed Sunday night (runs Tuesday) and EARLY for one placed Tuesday (runs Thursday).
  The correct statement is that the feed informs a claim iff it is placed Wednesday or later, which §4.36 says not
  to do.] Depth charts and snap counts are already downloaded.
**THE RULE: quote the ceiling before hunting the spike. ~~A Tuesday screen~~ **[v9.15: a pre-claim screen; there is
no Tuesday run, §4.36]** buys about one spike in ten on the best fifth, and the ordering inside the list should use
targets AND air-yards share, never targets alone. `Scripts\research\wk1\wopr_spike.py`.**


**[v9.34, doc 440] THE ORDERING HALF, TESTED AS A FOURTH SIGNAL ON THE WORKLOAD SCREEN, AND IT DOES NOT ENTER.** On this
finding's own population (WR and TE, weeks 1 to 17, 2021 to 2025, not startable, 1+ target in w and w+1, n=8,718; base spike
4.3%, WOPR top fifth 10.1%, targets 9.2%, air yards 9.0%, all reproducing), the top-fifth cuts are **WOPR 0.461 and
air-yards share 25.2%** (n=1,744 each). On the screen's 2-of-3 bar (n=1,350, spike 12.1%): adding WOPR at that cut as a
fourth signal gives 12.2% with it (n=1,143) against 11.6% without (n=207), +0.1 over the bar, permutation p=0.90; adding
air-yards share gives 12.9% (n=869) against 10.6% (n=481), +0.8 over the bar, +2.3 with-against-without (se 1.8), p=0.21.
**Both fail doc 437's +2-point falsifier and stay display columns, the same verdict as expected points (4.37).** The
0-of-4 to 4-of-4 count on air yards runs 1.8 / 5.3 / 8.1 / 11.7 / 14.5% spike and 9.4% to 49.9% startable next four, so the
fourth signal separates the top cell a little; the cells are 400 to 500 rows. The cross in section 2 above still describes
the POOL; inside the screen the three signals already carry it. Script: `Scripts\research\wk1\delta_screen.py`.

---

> **RETRACTED IN PART AT v9.26 (doc 405): THE SUNDAY-NIGHT PLACEMENT RULE IS DEAD, AND WITH IT THE WHOLE
> "THE PLACEMENT DAY CHOOSES THE PAPERWORK" MODEL, INCLUDING THIS FINDING'S TITLE.** Matt killed it with one
> question: *"Sunday's claims? Why would i place a claim on Sunday??"*
> **Measured, every EXECUTED waiver claim in this league 2022 to 2026, n=626: 86.3% run THURSDAY 03:00 to 06:00,
> 13.7% Friday to Sunday, and ZERO have EVER run Monday, Tuesday or Wednesday** (115 / 117 / 158 / 139 / 11 by
> season). A claim placed Sunday night and one placed Wednesday night land in the SAME Thursday batch, so
> **placement does not choose the run: Sunday buys nothing and costs Sunday night football, Monday night
> football, and the Tuesday and Wednesday practice reports.**
> **The misread sentence:** `Waiver Period: 2 Days` is how long a PLAYER sits on waivers after being dropped, not
> how long a CLAIM waits. All 283 unowned players share one clear time, which is what that looks like.
> **THE RULE IS NOW: PLACE CLAIMS WEDNESDAY NIGHT.** Every D+2 sentence below is void; the IR seat material,
> the sourced ESPN rules in (g), the drop rule in (h) and the claim-order material in (i) all stand.

**[v9.15] 4.36 THE WAIVER PERIOD IS TWO DAYS, SO THE GATE IS WHEN YOU PLACE THE CLAIM, AND THE IR SEAT IS A
TWO-WEEK LOAN, doc 391, `[TESTED, n=1,218 Out designations 2021 to 2024 and n=1,431 Out player-weeks 2021 to 2025]`.**
**[22 Sept 2026. Replaces the IR paragraph written into directive v9.14 the same day, which
Matt called under-specified: *"There are other scenarios where somebody might be ruled out and yet the
status changes before waivers go through."* He was right; v9.14 carried one scenario as the rule.]**

**BASELINE AND POPULATION (§3, §0.6).** Two separate populations, stated here and restated in every doc
that uses them:
- **P1, the timing half:** every row of the nflverse official NFL injury report, regular season, positions
  QB/RB/WR/TE/FB, **2021 to 2024**, the four seasons that carry `date_modified`; 2025 and 2026 dropped
  that column. Restricted to rows that ended the week as `report_status == 'Out'`: **n = 1,218.**
- **P2, the seat-life half:** the same feed, **2021 to 2025**, same positions, `report_status == 'Out'`
  in regular-season week w, **whose team also plays in week w+1**, 122 bye weeks (7.9%) excluded and
  counted separately, 1 row unmatched to a `pfr_id` and dropped. **n = 1,431.** Outcome is an offensive
  snap in w+1 from nflverse `snap_counts`. Join `gsis_id → pfr_id` through `players.csv`; **no name join.**
- **Pre-registered form (§0.5(a2)), written before the run and reproduced in the script's docstring.**
  **This is a BASE RATE, not a hypothesis test.** Nothing is confirmed or killed by it. It prices one
  thing: how long a parked seat lasts.

**(a) THE CLOCK. `Waiver Period: 2 Days`, `2026_League_Settings.txt` line 125, never quoted in this
project before today.** Processing is **not a fixed weekday**. A claim placed on day D runs on the
morning of **D+2**, confirmed against live behaviour: Matt placed three claims Tuesday 22 Sept and
reported them as processing *"on the morning of Sep 24"*, a Thursday. **So the placement day chooses
which injury paperwork the claim must survive**. ~~Sunday night runs Tuesday and crosses nothing,
Tuesday runs Thursday and crosses Wednesday's practice report, Wednesday runs Friday and crosses three.~~
**[Struck at v9.32, doc 435, in place: the model is dead since v9.26 (doc 405, the banner above). The run is
Thursday 03:00 to 06:00 whatever day the claim is placed. Doc 435 adds the one true per-player case: a man
DROPPED on Wednesday clears Friday about 03:00, so a claim on him is checked Friday morning.]**

**(b) WHEN THE DESIGNATION ACTUALLY MOVES, ~~MEASURED~~ RETRACTED WITHIN THE HOUR, doc 392 (P1, n=1,219;
the published 1,218 was also one short, three player-weeks are duplicated in the feed).** Day of week the
**Out** row was **last edited**: Friday 80.56% · Saturday 6.64% · Wednesday 7.88% · Thursday 4.27% ·
Sunday 0.41% · Tuesday 0.25% · Monday 0.00%.
~~91.9% land Thursday or later, so a Thursday-morning run beats the official designation channel about 92%
of the time.~~ **THE NUMBER DOES NOT MEASURE THAT AND MUST NOT BE QUOTED. `date_modified` is the timestamp
of the LAST edit, and nflverse keeps ONE row per player-week (confirmed: 3 duplicates in 24,000 rows). A row
last edited Friday may have said Out on Wednesday and never changed, or said Questionable on Wednesday and
been downgraded, the feed cannot tell them apart, and that distinction is the entire claim. The only
supportable reading is a FLOOR: at least 7.88% of Out designations were settled by Wednesday. The complement
is unobservable.** This is §0.2's slide: a real measurement of one thing (when a row stops changing) was
attached to a different thing (what the row said on a given day). **The timing question is BLOCKED, and the
missing input is named in the finding's BLOCKED line below.**

**(c) THE STATE TABLE. "Ruled Out" is eight states, not one.** On NFL injured reserve (holds four games
by rule, safe at any placement day) · ruled Out on the final report and did not play (usually holds;
the main case) · **ruled Out then upgraded in-week, activated off IR, a practice window opened, or the
injury simply resolved, which flips ANY day including Monday, and is the row v9.14 missed** · Questionable
then inactive 90 minutes pre-kick (never carried a formal Out; unreliable) · Doubtful (is not Out; very
likely not slot-eligible) · suspension/PUP/NFI (full term, known in advance, safe) · Out with his team on
**bye** next week (nothing exists that could change it, the safest week to spend a claim, 7.9% of cases) ·
Out with his team playing **Thursday night** next (designation filed Wednesday; first to break).

**(d) SEAT LIFE (P2, n=1,431). RE-MEASURED AT v9.22 AGAINST THE RIGHT EVENT — doc 399.**
**THE STATE TABLE STANDS AND REPRODUCES TO THE DECIMAL.** An Out player **plays a snap the next week 29.6%** of the
time. In w+1: still **Out 38.9%** · downgraded to **Questionable 19.5%** · Doubtful 3.4% · **no designation at all
38.2%**, of whom 40.4% never play in the next four weeks, which reads as NFL injured reserve.

**WHAT CHANGED IS WHICH EVENT ENDS THE SEAT.** This finding counted the seat as dying when the man takes a snap. By
the rules sourced at v9.19 and carried in (g), **the slot is invalid only when he loses his injury designation
entirely**: Questionable and Doubtful keep it, and NFL IR keeps it because ESPN accepts the IR status. Both measures,
same 1,431 rows, same script:

| | w+1 | w+2 | w+3 | w+4 | w+5 |
|---|---|---|---|---|---|
| **seat still VALID (sourced event)** | **75.5%** | **51.2%** | **35.2%** | **26.4%** | **22.2%** |
| ~~still not playing (published event)~~ | 70.4% | 52.7% | 41.9% | 35.6% | 31.5% |

**The two errors run in opposite directions: safer in week one, shorter from week three.** The median seat still dies
between two and three weeks, so **the standing play is unchanged.**

~~From the week he first goes Out (n=1,035), share still not playing: w+1 73.8% · w+2 53.8% · w+3 40.8% · w+4 31.2% ·
w+5 23.8%.~~ **RETRACTED AT v9.22, UNREPRODUCIBLE (doc 399).** Six population definitions were tried against it — all
Out-weeks, first-Out-per-player-season, and gap-separated episodes, each with and without the bye filter. **None
reproduces it.** The nearest lands n=1,040 against the published 1,035 and runs 4 to 11 points high in the tail. The
headline rates in this same paragraph reproduce exactly on the same script and population, so the defect is in the
curve, not in the data or the filter. **Do not quote it. The valid-seat row above replaces it.**

**THE NUMBER THIS FINDING SHOULD ALWAYS HAVE CARRIED: parking an Out man leaves the roster invalid, and the lineup
frozen, the following Sunday 24.5% of the time** (351 of 1,431; 257 of them played, 94 were cleared without playing).
**About one parked man in four**, and it is what §2's Sunday-morning roster check is worth.

~~By position, plays in w+1: QB 19.2% (n=156) · RB 26.7% (n=296) · TE 31.4% (n=309) · WR 33.0% (n=636), a parked
quarterback holds his seat longest and a parked receiver shortest, the opposite of what the roster wants, since QB is
the position §6 says to stream.~~ **THE ORDERING INVERTS ON THE RIGHT EVENT (doc 399).** Seat invalid at w+1:
**RB 20.3% · QB 22.4% · TE 24.9% · WR 26.1%.** A parked QB was the safest park on the snap measure and is the second
riskiest on this one, because a quarterback ruled out loses his designation without playing more often than any other
position. **A parked RB is the safest seat; a parked WR is still the riskiest, which is the one half of the old line
that survives.** The §6 streaming inference drawn from the old ordering does not follow and is withdrawn.

**The 19.5% Questionable cell is the quiet failure: no longer Out so the seat ends, not yet playing so
nothing was gained. It is more common than him coming back and helping.**

**(e) WHAT IT COSTS WHEN IT BREAKS.** *Before the run:* the roster the pending claim would create is
illegal. **UNVERIFIED whether ESPN fails the claim or processes it and forces a drop**, and the
difference matters, because a failed claim keeps Matt's waiver position (10 of 12) and a forced drop
spends it. *After the run:* sixteen bodies for fifteen seats, ESPN blocks moves until one is cut. That is
Matt's *"drop whoever you want"* and it is a real option, since the trigger is the parked man being healthy
again. **Two limits v9.14 did not carry:** `Observe ESPN's Undroppable Players List: Yes` (line 118), and
any drop spends that player's keeper eligibility, which §2.1(a) requires be stated when a drop is
recommended. **And `Lineup Changes: Lock individually at Scheduled Gametime`:** a man cannot be moved into
or out of the slot after his own kickoff.

**(f) THE RULE, AND WHAT IT DOES AND DOES NOT REST ON.** ~~**PLACE CLAIMS SUNDAY NIGHT.** They run Tuesday
morning and cross no injury paperwork at all.~~ **[Struck at v9.32, doc 435, in place: retracted at v9.26, doc 405.
PLACE CLAIMS WEDNESDAY NIGHT; claims execute Thursday 03:00 to 06:00 and never Monday to Wednesday. The dominance
argument below is now about Wednesday against Sunday and runs the other way: Sunday gives up four days of news.]** **The argument is DOMINANCE, not effect size: placing earlier
cannot expose a claim to more paperwork than placing later, and it costs nothing, so it wins without needing
to be worth anything in particular. HOW MUCH it buys is NOT ESTABLISHED and no number attaches to it.**
**[v9.16, doc 392, and the reason this paragraph was rewritten matters more than the rule.** The first
version justified the rule with the retracted 92% and opened by telling Matt his instinct had paid off. Both
were wrong in the same direction: **the load-bearing premise here is HIS, that ESPN refuses the add once the
status flips, and it is the one thing in this finding that was never tested.** Everything measured (the
2-day period, the report timestamps, the seat life) sits AROUND that premise, not on it, and measuring the
surroundings does not confer credibility on the centre. Matt, 22 Sept: *"Never take what I say is scripture...
Wrong logic to correct me."* **Filed as a named failure mode in §0.5(a5).]**

**(g) THE CENTRE, ANSWERED FROM ESPN'S OWN FOOTBALL DOCUMENTATION. [v9.19, doc 394.]** (f) said the
premise was Matt's and untested. **It is now SOURCED, and it took three of my errors to get there.**
Matt, 22 Sept: *"I don't honestly know the exact rules and I don't pretend to know all the details.
I'm just going off what I've seen previously... I thought I could give you an example and from there
you could simply look up details from the documentation on ESPN and league settings I've provided. Is
that not the case? Did you corroborate everything?"* **The answer was no.**

**VERBATIM, ESPN Fan Support > Fantasy FOOTBALL > Managing Your Team, *Players on Injured Reserve
(IR)*, read as page text:**
- *"In ESPN Fantasy Football, players with either the Out (O) or Injured/Reserve (IR) status may be
  placed into the IR slot"* → **the slot accepts exactly two statuses.** This retires the
  *"which designations does this league's slot accept"* item that had been UNVERIFIED since doc 390.
- *"Suspended players (SSPD) are NOT eligible for IR on FFL."*
- *"If a player in the IR slot has their status updated from OUT or IR to QUESTIONABLE or DOUBTFUL,
  the user's roster is NOT invalid. Those players can remain in that IR slot, and the user can make
  claims/add players, adjust their lineups as they wish."*
- *"If a player goes from OUT to no longer having an injury designation, the user's roster becomes
  INVALID, and they must update it accordingly."*

**And ESPN > Fantasy Football > Trades and Waivers, *Reasons Why a Waiver Pickup May Not Process*:**
*"Teams are not allowed to make claims if they have an ineligible player in the IR slot. If you have a
healthy player in IR, the claim will not process."* → **clear the slot before entering claims.**

**WHAT THAT OVERTURNS IN THIS FINDING'S OWN EARLIER TEXT:**
1. ~~Ruled Out then upgraded in-week flips any day and nothing on a schedule protects you.~~ **An
   upgrade to Questionable or Doubtful breaks NOTHING. It is the most common upgrade and it is
   explicitly safe.**
2. ~~The 19.5% Questionable cell is the quiet failure, seat gone and nothing gained.~~ **He keeps the
   seat and keeps transacting. The cell is not a failure at all.**
3. ~~Suspension, PUP and NFI are safe to park.~~ **SSPD is never eligible.** PUP and NFI are not
   addressed, so NOT ESTABLISHED.
4. ~~The vendor contradicts itself.~~ **MY ERROR.** The "contradicting" page sits under **Fantasy
   Women's Basketball**, a different sport whose rule (*only* an IR/IL tag qualifies) differs from
   football's (Out also qualifies). **Two method failures caused it: I compared pages without
   checking which sport's section each sat in, and I quoted both through `WebFetch`, which returns a
   small model's rendering of a page rather than the page, so quotation marks went around text ESPN
   may never have written (§3).** Read support pages with the browser and check the breadcrumb.

**SO THE MECHANIC, FINALLY, AND MATT WAS RIGHT ABOUT THE SHAPE OF IT:** park an Out or IR man, keep
the free seat, ride any downgrade to Questionable or Doubtful at no cost, and **the only event that
costs anything is the designation disappearing entirely**, which invalidates the roster and freezes
the lineup until he cuts someone. **His words for it:** *"if my claim is successful then my players
are locked... not until I drop someone to fit the limit."* **It is a SUNDAY risk: check the roster
the morning a claim processes.**

**STILL NOT ESTABLISHED, and I looked:** what `Auto Reactivate: No` does in football (it is in
`2026_League_Settings.txt`, which I had grepped rather than read, and ESPN's football help does not
document it); whether an IR man counts against a position cap; whether time on IR breaks *"rostered
all season"*. **`STATUS_LOG.csv` still dates the flip and is still worth having**, but for a narrower
reason than v9.18 gave it: the event to watch for is the designation vanishing, not a downgrade.

**(i) CLAIM ORDER. THE MECHANIC IS SOURCED; THE GRADIENT THAT WAS ATTACHED TO IT IS RETRACTED (doc 401, v9.24).**

**WHAT ESPN PUBLISHES, and this is unchanged.** *Waivers Overview*: a winner *"will move to the end of the waiver
order. This process continues until all waiver claims are processed"*, so the demotion lands MID-RUN. *Claim a Player
Off Waivers*: *"Reorder claims by dragging them into your preferred priority"*, and a free-agent add *"does not
affect your waiver position"*.

**WHAT STANDS, MEASURED** (this league, WAIVER rows that reached a decision, 2022 to 2026, n=1,131 claims over 745
player-runs and 543 team-runs; EXECUTED counts as a win, every FAILED_* as a loss): **only 28.6% of player-runs are
contested**, and **an uncontested claim wins about three in four regardless**.

~~On the 586 contested claims the win rate goes 61.1% with no other win that run, 29.1% with one, 11.2% with two or
more.~~ **RETRACTED: THE STATISTIC IS DEGENERATE.** The bucket is *other wins by that team in that run*, which is the
team's total wins minus this claim's own result. **A winner therefore sits one bucket lower than a loser from the
same team-run by construction.** Permuting which contested claims won, holding each team-run's contested win count
fixed, over 3,000 draws, reproduces **61.1 / 29.1 / 11.2 exactly, with zero variance**: the observed data is
indistinguishable from randomly reshuffled data, so the gradient carries **no information about ordering at all**.
The published cells also carried no sample sizes, which §3 requires; they are **n = 211 / 223 / 152**.

**THE RULE SURVIVES ON THE SOURCED TEXT, AS A DOMINANCE ARGUMENT WITH NO EFFECT SIZE** — the same footing as the
Sunday-night placement rule. A winner is demoted mid-run and he sets the order, so his priority is highest on
whichever claim is processed first. Spending it on a contested claim cannot do worse than spending it on one nobody
else wants, and it costs nothing. **RANK THE CONTESTED MAN FIRST. Do not attach a number to it.**

**BLOCKED, with the missing input named (§0.5(a4)):** every claim in a run carries **one identical timestamp**
(03:28, 03:30, matching ESPN's "daily around 3:00 AM ET"), so `waiver_report_*.csv` can never show within-run order.
The input that would settle it is **his own claim ordering, recorded at placement and paired with the outcome**,
forward-going only. Mine to build into `wire.py`.

**AND THE TRAP THAT COST MORE THAN THE FINDING: ESPN GIVES D/ST NEGATIVE PLAYER IDS.** A first pass extracted the
player with `ADD Player ID (\d+)`, which **silently dropped 437 of 1,623 waiver rows, 27%, every one a defence**.
§0.6 exists because of a D/ST exclusion and it happened again in a new place. The population only reproduced doc
396's 745 / 543 / 28.6% / 586 once the sign was allowed.

**(h) AND THE MEASURED RISK IS NOT THE PREMISE, IT IS THE MISSING DROP. [doc 393.]** Population: every
waiver and free-agent event in `waiver_report_2022..2026.csv`, this league, **n=2,256**. Among claims
that reached processing and were not outbid (`EXECUTED` + `FAILED_ROSTERLIMIT`): **a claim naming a
drop, 884 executed and 0 roster-limit failures; ~~a claim naming none, 371 executed and 24 failures,
6.1%~~.** **[v9.32, doc 435: the 371 includes 247 FREE-AGENT adds, which have no processing step and only ever
appear as EXECUTED, so they cannot fail and the rate is diluted. On WAIVER claims alone: no drop, 124 executed and
24 roster-limit failures, 16.2% (19.5% counting the six position-limit failures); with a drop, 0 of 502. And the
"884 for 884" hides 103 drop-carrying claims that failed as already-dropped: 102 of them were the same team's
second claim in the same run naming the drop its first claim had spent. One drop carries one claim.]**
All 24 failures carried zero drops, so **the premise's own signature — a claim WITH a drop
failing anyway — has never occurred here in five seasons.** Largest single owner of the 24 is **Matt,
8 of them**, all 2025, weeks 2, 2, 4, 4, 5, 10, 10, 10. Identity confirmed from transactions, not from
the team name (*The Poetry of Junkyard Juggers* added Coleman 4702555 and Vele 4569559, both on
`MY_ROSTER.csv`); a 2024 *Ja'Marracle Whip Juggernauts* holds 2 more and is probably his, **not
confirmed, do not assert.**

**UNVERIFIED, DO NOT ASSERT:** whether ESPN's `injuryStatus` moves on a Wednesday *practice* report or only
on the Friday *game designation*; which designations this league's IR slot accepts; whether a man there
counts against a position cap; whether time there breaks *"rostered all season"* (§2.1(a)).
**BLOCKED (§0.5(a4)):** day-by-day report history. nflverse keeps **one row per player-week, the final one**,
so a Wednesday state is not recoverable for past weeks. The missing input is a daily scrape of NFL.com's
injury report, going forward only. **Not tried.**

**DEFECT FOUND DURING THE RUN, recorded because it is §3's silent-skip trap in a fifth place:** the
2021–2024 injury files carry `game_type` and `date_modified`; the 2025–2026 files carry `season_type` and
dropped `date_modified`. A `season_type == 'REG'` filter therefore **silently discarded four of the five
seasons**, and the first run printed n=410 with no error and no warning. The script now asserts that every
season survives the filter. **`Scripts\research\ir\ir_return_rate.py`.**

---

**[v9.33] 4.37 EXPECTED POINTS OVER THE LAST TWO GAMES BEAT ACTUAL POINTS AT PREDICTING THE NEXT FOUR WEEKS, AT EVERY
POSITION AND IN EVERY SEASON, AND STILL DO NOT ENTER THE WORKLOAD SCREEN, doc 438, `[TESTED, n=9,999]`.**

**BASELINE AND POPULATION (§3, §0.6).** RB, WR and TE player-weeks, regular season 2021 to 2025, weeks 2 to 16, not
startable in week w on §4.13b's bar (season-to-date average below RB 9.92, WR 9.62, TE 8.25), at least one target or
carry in w, a game row in w-1, a snap line, and played in w+1: **9,999 player-weeks (WR 4,666, RB 2,735, TE 2,598)**,
doc 389's claimable pool extended to backs. Base rates: spike in w+1 (18.0+) 4.3%, startable in w+1 20.5%, startable
over the next four weeks 17.4% (n=9,393 with two or more games ahead), 5.48 a game over the next four. Expected points
are ffverse's ffopportunity model (`ep_weekly_2021..2025.csv`), full PPR converted to ours by subtracting half a point
per expected reception; joined on gsis id, 100% of 23,097 touch-weeks.

**(a) THE TWO-GAME EXPECTED BEATS THE TWO-GAME ACTUAL.** Rank correlation with the next four weeks' average: **.497
against .417** on the pool; RB .526 against .454, WR .473 against .389, TE .493 against .406; **five seasons of five**
(2021 .445 against .402 through 2025 .511 against .416). Top fifth by expected, startable over the next four: **38.9%
against 33.3%** by actual (RB 46.3 against 38.9, WR 35.3 against 29.7, TE 32.0 against 32.5). In a regression of the
next four weeks on both, **expected +0.61 a point, points over expected +0.08 (se .02)**; the same at each position.

**(b) THE CELLS THAT DECIDE A CLAIM.** Top fifth on actual but NOT on expected (n=775): spike 4.8%, startable next four
**20.0%**, 6.42 a game, which is the pool. Top fifth on expected but not on actual (n=762): **34.5%**, 8.07. Both
(n=1,238): 41.5%, 8.87. The fifth most UNDER expected over two games (4.31 actual on 7.77 expected) scores **6.79**
over the next four and is startable 25.1%; the fifth most OVER (8.67 on 5.74) scores 5.95 and is startable 18.9%.

**(c) IT DOES NOT ENTER THE SCREEN. FALSIFIER FIXED IN ADVANCE (doc 437): under +2 points of spike rate over the
three-signal count it stays a display column.** WR and TE (the screen's gate, n=7,264): on the 2+ bar (n=906, spike
10.0%), adding the two-game expected in the pool's top fifth as a fourth signal gives **10.0% (n=659) against 10.1%
without (n=247), 0.0 points, permutation p=1.000**; the week-w expected alone, +0.1. Three of the four are the same
week's workload seen four ways: 659 of the 906 already clear the bar. On the four-week outcome the split is 40.7%
against 29.8%, real and small, and the rule was fixed on the spike. The screen reproduces on this pool: 0 of 3 spikes
1.9%, 1 of 3 6.4%, 2 of 3 10.0%, 3 of 3 10.2%, the jump still one signal to two (§4.31, doc 308).

**(d) AGAINST WOPR (doc 389's best single signal), same WR/TE pool, top fifths:** startable next four 34.5% by two-game
expected against 31.2% by WOPR; spike 7.9% against 7.7%. Expected is the better four-week read; WOPR is not worse on
the spike.

**(e) RUNNING BACKS.** Top fifths, startable next four: actual 38.9%, touches 43.9%, snap share 45.0%, **expected
46.3%**, expected and touches together 48.3%. Expected points and snap share are the same instrument at RB (9.57 a
game next four for both), which agrees with doc 434.

**(f) THE TWO FLAGS, on fixed bars, both a screen and not a forecast.** `box-score mirage`, 8+ actual on under 5
expected over his last two games: n=101, spike 3.0%, startable w+1 14.9%, **startable next four 12.0%**, 4.88 a game;
worse than the pool on every outcome. `quiet volume`, 8+ expected on under 5 actual: n=172, spike 5.8%, startable w+1
27.9%, **startable next four 28.2%**, 7.23 a game; better than the pool on every outcome. Both print in `flags` on
the wire page from `wire.py`'s 29 Sept pin; `build_form.py`'s cumulative row carries `act2` and `xfp2`. **Neither
sorts anything.**

**SCOPE.** In-season, claimable men only, two completed games. Nothing here is about a starter or the draft. The
ffverse model lags a game when it has not processed one; the column is blank then, never zero. **NOT YET RUN:** the
same on the DELTA in expected points from w-1 to w (Matt's 27 Sept claim), and the print of `xfp`/`fp_oe` as columns
on any page.

**[v9.34, doc 440] (g) THE DELTA IN EXPECTED POINTS IS FALSIFIED.** Same pool (n=9,999; 9,393 with two or more games
ahead), dxfp = expected points in week w minus the previous game. OLS of the next four weeks on the two-game level and the
delta: **level +0.60 (se .01), delta +0.03 (se .01)**; RB +0.06, WR +0.02, TE minus 0.02. Top fifth by the delta (cut
+3.30): startable next four 24.2% against 38.9% by the level; delta-only cell 17.1% against the pool's 17.4%. The two games
weighted separately: the newer +0.33, the older +0.27. **The level is the signal; a rise carries nothing over it.**

---

**[v9.34] 4.38 A RISE IN SNAPS AND TARGETS IS NOT A SIGNAL OVER THE LEVEL: AT THE SAME READING THE MAN WHO JUST ROSE TO IT
IS LESS LIKELY TO HOLD IT, doc 440, `[TESTED, n=9,999]`.**

**MATT'S CLAIM, 27 Sept, in his words:** *"counts on the field and targets combined are a signal for a player whose role
could expand... we are picking from the bottom of the bottom."* **TESTABLE FORM (§0.5(a2)):** among NON-STARTABLE RB, WR and
TE in week w (doc 438's claimable pool, REG 2021 to 2025, weeks 2 to 16, n=9,999), does a week-over-week RISE in BOTH snap
share and targets (w against his previous game) predict startable over the next four weeks (2+ games, n=9,393) OVER AND
ABOVE the level of either? Falsifier fixed before the run: under +3 points of startable-next-four net of the levels, the
level alone is the signal.

**(a) THE RAW CELLS, startable next four:** both rose 18.8% (n=2,383) · only snaps rose 17.4% (2,452) · only targets rose
19.5% (1,416) · neither 15.5% (3,142) · pool 17.4%. RB both rose 22.8% (627) against neither 16.9% (915). A stricter rise,
10+ snap points AND 3+ targets: 20.9% (n=675), RB 28.8% (153). **So the raw cell is a little better than the pool, and that
is the level showing through.**

**(b) NET OF THE WEEK-w LEVELS the sign turns:** both-rose **minus 6.7 points (se 0.9)** with snap share (+0.37 a point) and
targets (+2.3 a target) in the regression; RB minus 6.2 (2.0), WR minus 7.9 (1.3), TE minus 6.4 (2.0); every season minus 5.2
to minus 8.2; the strict rise minus 8.9 (1.7). With the two single rises entered as well the indicator is minus 0.7 (1.2) and
each rise is itself negative (minus 0.10 a snap point, minus 1.5 a target). Net of the PREVIOUS game's levels instead, +8.5,
which is only the current level again. **At the same snap share and targets this week, the man who ROSE to them is about
seven points less likely to be startable over the next four than the man who was already there, because his two-game level
is lower and the two-game level is what predicts (4.37).**

**(c) THE INTERACTION (§0.5(a3)):** both-rose minus the sum of the single rises, pooled minus 2.6 (se 1.7), WR minus 4.9 (2.4),
RB minus 3.5 (3.4), TE +2.5 (3.2). **Substitution where it is measurable, amplification nowhere.**

**THE RULE:** read the level, two-game expected points and snap share; **a rise is not extra credit, and at a given reading
it is a reason for a little caution.** Nothing here sorts a page. **SCOPE AND WHAT IS NOT TESTED:** the outcome is four
weeks; ~~"a role that could expand" on a longer horizon (eight weeks, the rest of the season) is NOT YET RUN~~ **[doc 445,
29 Sept: RUN, and the longer the horizon the worse the riser looks.** Same population, same predictors, same falsifier; the
both-rose coefficient net of the week-w levels, pooled with position held: startable next four minus 6.7 (se 0.9), next
EIGHT minus 7.7 (1.0, n=7,308), the REST OF THE SEASON minus 8.8 (1.0, n=7,527), and the best four-game stretch inside the
next eight clearing the bar minus 10.5 (1.2); RB minus 9.2 / minus 11.4 / minus 10.3 on the three long horizons, WR minus
7.6 / minus 8.2 / minus 10.9, TE minus 8.2 / minus 9.1 / minus 10.8; every season minus 7.3 to minus 8.4 on eight weeks. The
raw cells shrink to nothing as the horizon lengthens: both rose against the rest +1.9 points on four weeks, +0.8 on eight,
+0.1 on the rest of the season, +0.3 on the peak. The strict rise minus 7.4 to minus 11.2. **The level alone is the signal on
every horizon; "a role that could expand" does not live in the rise. Falsifier held four times.** Script
`Scripts\research\wk1\rise_horizon.py`, `run_rise_horizon.txt`.]** 17.5% of
the deltas span a bye or a missed week (the result holds on calendar-adjacent games only: minus 6.5). Script and output:
`Scripts\research\wk1\delta_screen.py`, `run_delta_screen.txt`.

---

**[v9.34] 4.39 THE PREGAME LINE, TESTED ON THE THREE STREAMING PICKS: AT D/ST AN OPPONENT-BASED RULE IS WORTH ABOUT +3 A WEEK
OVER RANDOM AND THE PAGE HAS NONE; AT QB THE OWN-TEAM IMPLIED TOTAL CLEARS RANDOM AND DOES NOT ROBUSTLY BEAT THE DOC 427 RULE;
AT KICKER NOTHING, doc 441, `[TESTED, 75 season-weeks a lane]`.**

**POPULATION AND BASELINE.** nflverse `games.csv` lines (spread_line = home minus away expected margin, positive = home favoured,
checked against results on 1,279 games; implied team total = total/2 + own margin/2, r=+0.39 with points scored), REG 2021 to
2025, weeks 1 to 17. D/ST points from the rebuilt full file (doc 441; 2,718 team-weeks). A pick rule is scored by the mean
weekly points of the man it picks from the STREAMABLE pool (D/ST and K: ranks 13 to 32 by season-to-date average with 2+
prior games, weeks 3 to 17, 75 season-weeks; QB: ranks 13 to 24 with 3+ prior games of 10+ attempts, weeks 4 to 17, 70
season-weeks) against the pool mean (random). **The falsifier as first written asked for se under 0.5 at n=75, which no rule
can reach (the pick's own sd over sqrt(n) is 0.72 at D/ST, 1.09 at QB); the reading that stands is the t-reading, gain of
1.0 or more and at least two se, and the replacement bar of +0.5 over the season rule.** Script `Scripts\research\vegas_streams.py`.

**(a) D/ST.** Lowest opponent implied total: **7.79 a week, +3.16 over random (se 0.72, t 4.4)**. Lowest opponent season-to-date
points scored: 8.02, +3.40 (se 0.81, t 4.2). The two against each other: minus 0.23 (se 1.10), 27 wins 29 losses 19 ties.
Most-favoured defence: +3.02. Lowest opponent season-to-date D/ST points allowed: minus 2.38 (the wrong side of the ledger).
Rank correlation with D/ST points, all 2,558 unit-weeks: opponent implied total minus 0.31, own spread +0.28, game total
minus 0.13. **THE RULE: the D/ST lane prints the opponent's implied total and picks on it; it is available Wednesday, needs no
prior weeks (the season rule needs two), and the two are equal from week 3.** "A defense is worth its matchup" now has a
number: about three points a week over a random streamer.

**(b) QB.** Highest own-team implied total: **22.00, +4.53 over random (se 0.89, t 5.1)**; doc 427's softest matchup by
opponent QB points allowed, prior weeks only: 19.17, +1.70 (se 1.08, t 1.6); line minus season rule +2.84 (se 1.41, t 2.0).
**Under doc 435's tier definition instead (full-season rank 13 to 24 with 8+ games, 80 season-weeks): line +2.21 (t 2.5),
season rule +2.54 (t 3.1), line minus season minus 0.33 (se 1.22).** So the line clears random under both definitions and
beats the doc 427 rule under one of two: **wire it beside the doc 427 rule as a second read, do not replace the rule, and say
which the two agree on.** The rank-sum of both beats neither alone.

**(c) KICKER.** Highest own-team implied total: +0.32 over random (se 0.41); opponent season-to-date K points allowed +0.84
(se 0.50); neither clears. Rank correlation of implied total with K points +0.14. **Nothing to wire.**

---

**[v9.34] 4.40 ROUTE PARTICIPATION BEATS SNAP SHARE ON HISTORY AND IS NOT A FOURTH SIGNAL; BUY NOTHING UNTIL AN IN-SEASON USE IS
NAMED, doc 441, `[TESTED, n=4,596]`.**

**POPULATION.** Claimable WR and TE weeks, REG 2023 to 2025, weeks 2 to 16 (doc 438's pool, three seasons because the nflverse
participation files begin in 2023): n=4,596 (WR 2,921, TE 1,675). Route participation = dropbacks on which he was on the field
over team dropbacks (`qb_dropback`, spikes and kneels out), from the FREE nflverse participation files, which land AFTER the
season (2025's on 10 Feb 2026); it is DROPBACK participation, an approximation of charted routes: a man who stays in to block
counts. 100% of dropbacks join. Correlation with snap share 0.945.

**(a)** Rank correlation with the next four weeks: snap share .487 (two-game .510), route participation .531 (two-game .552),
targets .449, TPRR .051. Route beats snap in every season and at both positions (TE .589 against .506). **(b)** OLS of the next
four weeks on both: **route +0.091 a point (se .005), snap minus 0.020 (se .006)**; route absorbs snap share entirely. TE
+0.113, WR +0.068. **(c)** Top fifths: route-only cell (n=190) startable next four 34.2% against snap-only (n=193) 27.4%, +6.9
(se 4.8); inside snap bands, the route-minus-snap tilt moves startable-next-four by +5 to +10 at WR and +9 to +17 at TE. One
sd of tilt is worth +0.52 a week at WR and +1.15 at TE net of snap share. **Falsifier (+0.05 a point net of snap; +3 points of
start4 in the route-only cell): NOT falsified on either arm.** TPRR alone is noise (its top fifth is worse than the pool) and
carries nothing targets and routes do not.

**WHAT IT DOES NOT DO.** As a fourth signal on the workload screen's 2-of-3 bar: spike +1.0, startable next four +1.9
(under the +2 bar); swapping route 80%+ for snaps 80%+ inside the count changes nothing (40.3% against 41.3%). **THE RULE:
use route participation in place of snap share in backtests and in any weighting; the screen's bars do not change; a PAID
live source (PFF, Fantasy Points Data) is justified only for a named in-season use, and the one this measures is the
mid-snap-band split (40 to 80% snap share). Whether charted routes add more than dropback participation is a HYPOTHESIS.**
The purchase is Matt's decision (money, §0.4). Script `Scripts\research\wk1\routes_vs_snaps.py`.

---

**[v9.34] 4.41 RED-ZONE USAGE IS ALREADY INSIDE EXPECTED POINTS: NET OF THE TWO-GAME EXPECTED AND SNAP SHARE IT ADDS NOTHING,
AND END-ZONE TARGETS ARE NEGATIVE, doc 441, `[TESTED, n=9,999]`.**

**POPULATION.** Doc 438's claimable pool (RB, WR, TE, REG 2021 to 2025, weeks 2 to 16, n=9,999; 9,393 with two games ahead).
Red-zone usage from play-by-play: carries inside the 20, 10 and 5, targets inside the 20 and 10, end-zone targets (air yards
at or beyond the goal line), each as a share of the team's that week; predictors the two-game red-zone opportunity share
(carries plus targets inside the 20 over the team's) and the two-game end-zone target count.

**(a)** Rank correlation with the next four weeks: expected points .497, snap share .390, red-zone share .281, end-zone
targets .118. **(b) OLS of the next four weeks on expected points, snap share and red zone, position held: red-zone share
+0.000 per 10 points of share (se .056, t 0.0); end-zone targets minus 0.39 per target (se .07).** R2 moves from .240 to
.252 with both. On startable-next-four: red zone minus 0.3 (se 0.6), end-zone targets minus 2.8 points per target (se 0.7).
**(c)** Inside the expected-points top fifth, the red-zone top fifth against the rest: pooled +7.0 points of start4, which
is position composition (backs carry more red-zone share and start more); with each position cut at its own fifth, +3.7
(se 2.2, within-position permutation p=0.18); RB +3.0 (se 4.6), WR +3.6 (3.2), TE minus 1.0 (4.2). End-zone targets inside
the same fifth: minus 5.7 (se 2.2, p=0.015): a man whose expected points came from end-zone shots is worse than one whose
came from the field. **Falsifier (+0.10 per 10 points of share net of expected points and snap share; +3 in the cell): the
coefficient is 0.000 and the cell is +3.7 at p=0.18. Red zone stays a display column; no builder ships, because the
ffverse model prices field position already and a weekly play-by-play download (60 to 100 MB) would buy nothing the page
does not have.** 4.5 (red-zone volume is sticky) is about the draft and stands. Script
`Scripts\research\wk1\redzone_test.py`.

---

**[doc 445, index row rides with v9.35] 4.42 THE INJURY REPORT'S GAME DESIGNATION IS THE THIS-WEEK SIGNAL AND THE PRACTICE
STATUS IS NOT: OUT AND DOUBTFUL NEVER PLAY, QUESTIONABLE IS TWO IN THREE, AND A DID-NOT-PRACTICE WITH NO DESIGNATION PLAYS
THREE TIMES IN FOUR, doc 445, `[TESTED, n=7,464]`.**

**THE QUESTION IT ANSWERS (claude_todo, doc 442):** should the practice report's Out be `next_man_up()`'s step-past trigger
beside ESPN's `injuryStatus`, and should a Doubtful man be stepped past. **POPULATION.** Every RB, WR and TE row on a week's
injury report, REG 2021 to 2025, the week's final report as nflverse carries it (one row per man per week; n=7,464 after 5 bye
rows), joined on gsis_id to snap counts and the weekly stat file; outcome = played an offensive snap or had a touch that week.

**(a) BY GAME DESIGNATION, played that week: Out 0.1% (1 of 1,435) · Doubtful 0.4% (1 of 231) · Questionable 64.4% (n=1,961)
· no designation 90.1% (n=3,836).** Doubtful is Out for the week in every season (0.0 / 0.0 / 2.3 / 0.0 / 0.0%). **(b) THE
PRACTICE STATUS INSIDE A DESIGNATION:** Questionable and did not practice on the final report 45.8% play (n=310), Questionable
and limited 67.2% (1,232), Questionable and full 69.4% (386); **no designation and did not practice 74.9% play (n=391; RB
57.5% of 80, WR 79.6%, TE 79.0%)**, no designation and limited or full 92 to 93%. **(c) HOW FAR A DESIGNATION REACHES:** of
men Out in week w, 68.0% are still not playing in w+1 and 48.9% in w+2 (n=1,241 / 1,180); of men Doubtful, 53.8% and 33.9%
(n=195 / 186): a Doubtful man is back sooner.

**WHAT CHANGED (doc 445):** the IN DOUBT lane on the wire, which is a claim for THIS week, now skips a cover who is himself
Doubtful (he played once in 231); `next_man_up()`, the rest-of-season stash, keeps Doubtful on purpose (back sooner than Out).
**WHAT DID NOT:** a did-not-practice with no designation is not a step-past trigger (three in four play; at RB a coin flip,
n=80), it stays a printed line. **BLOCKED, input named:** whether the report's designation ever leads or lags ESPN's live
status cannot be measured on history, because no file holds ESPN's status day by day; `wire.py` now logs the pair every run
to `Source\status_pairs_2026.csv` (ESPN status beside report status and practice status, per depth row, per date), and the
comparison runs when the file has a few weeks in it. Script `Scripts\research\wk1\practice_out.py`, `run_practice_out.txt`.

**[doc 453, index row rides with v9.37] 4.43 THE YOUNG-RECEIVER SCREEN WORKS READ ON THIS SEASON'S FIRST WEEKS, AND A ROOKIE
THE PRESEASON SCREEN CANNOT SEE IS SCREENED ON HIS OWN GAMES; A BREAKOUT LAST GAME IS THE LEVEL, NOT A SIGNAL, PAST WEEK 3,
doc 453, `[TESTED, n=174]`.**

**THE QUESTION IT ANSWERS (Matt, 29 Sept, on Chris Bell):** *"The fact he's young and talented and broke out his first game
at the NFL level with a suspect QB speaks volumes. This is what I've been calling upside, and this player didn't even make the
week sheet."* 4.30 (doc 248) reads NFL rounds 1 to 3, yards per target over 7.13 and targets a game over 3.20 on a FULL prior
season to predict the NEXT one; a rookie has no prior season, so `pedigree_2026.csv` carried no screen for Bell (round 3, pick
94) and the bet lane had no ticket for him. Nothing had measured the same three marks read on a few weeks predicting the rest of
the same season, which is the object the sheet would be applying them to. **POPULATION.** WR seasons 2021 to 2025 (nflverse
weekly, REG, weeks 1 to 14), drafted 2021 or later (`nfl_draft_picks.csv`, so the NFL year is known), NFL years 1 to 3, not
startable the season before (under 9.62 half-PPR a game, this league's WR replacement) or no season before; read at the end of
week W on weeks 1 to W alone; outcome startable (9.62 or more a game) over weeks W+1 to 14 on 4 or more games played.

**(a) READ AT WEEK 3, n=174, base rate 16.7%: 0 of 3 marks 0.0% (35) · 1 of 3 3.9% (51) · 2 of 3 20.4% (49) · 3 of 3 43.6% (17
of 39), +34.7 points against fewer, permutation p=0.0000.** Rookies 3 of 3 57.9% (11 of 19) against 9.1% (6 of 66) for rookies
below three; years 2 to 3 at 3 of 3 30.0% (6 of 20). The same shape at weeks 4, 5 and 6 (3 of 3: 35.7%, 36.6%, 41.2%; p at most
0.0008). **(b) THE WIRE'S CELL, still under the bar through week W:** 3 of 3 and under 9.62 a game through week 3 is **26.7% (4 of
15)** against 5.6% (7 of 124) for fewer than three; at week 4, 36.4% (8 of 22) against 7.3%. That is the rate `sheet_constants.json`
carries as `potential.in_season.inseason_3of3` (0.267, n=15), and it is the rate the bet lane prints beside an in-season screen.
**(c) THE BREAKOUT GAME IS THE LEVEL.** A last game of 60 or more receiving yards or 7 or more targets: 40.0% against 7.3% at week
3, and among rounds 1 to 3 rookies 59.1% (13 of 22) against 8.1%, p=0.0000; **at weeks 4 and 5 the same cut is +5.6 and +9.0 points,
p=0.45 and 0.36, and 3 of 3 with a breakout last game equals 3 of 3 without one (36.4% against 35.0% at week 4).** At week 3 the
breakout is a third of the level; past week 3 it adds nothing to the marks, which is 4.38's shape again (the level is the signal).
**(d) BELL'S OWN SHAPE IS THE THIN END OF THE CELL:** 3 of 3 and under 6.0 a game through week 3 (he is at 3.9) is 0 of 4; 3 of 3 with
under 4.0 targets a game (he is at 3.3) is 0 of 2 (Alec Pierce 2022, Xavier Worthy 2024). Too few to say more than that he sits at
the bottom of the 27% group, and the reach gate (doc 432) says the rest: on Miami's 28 targets a game the average hit needs 38% of the
passing game, above the 37.8% ceiling; the bar itself needs about 30%.

**WHAT CHANGED.** `build_form.py` writes `rec_yds`, `rec` and `games`; `wire.py` `inseason_screen()` labels a year-1-to-3 receiver
with no preseason screen `in-season screen 3 of 3 (N g)` when this season's marks clear on 2+ games and 5+ targets, with the round,
yards a target, targets a game and games in the flag; the sheet's bet lane prices that label at 0.267 with the population sentence.
On the 29 Sept pull four free men clear it: Tre' Harris, Antonio Williams, Ted Hurst III, Chris Bell (Bell out of reach on volume).
**WHAT DID NOT:** a screen is not a forecast (4.13d); the cell is 15 men and re-fits at week 6 and after the season
(`Scripts\research\wk1\rookie_screen.py`, `run_rookie_screen.txt`); the falsifier is the under-the-bar cell falling to the field.

**[doc 456, index row rides with v9.38] 4.44 THE REACH GATE ON A SCREENED MAN IS A CAUTION, NOT A ZERO, doc 456,
`[TESTED, n=22]`.** BASELINE: the in-season screen's under-the-bar cell, 26.7% startable over weeks 4 to 14 (4.43).
POPULATION: doc 453's week-3 population, the 3-of-3 men under the bar, 2021 to 2025, with the reach gate (doc 432:
the share of his team's passing game the average hit would need, against the 37.8% ceiling) applied after the fact.
RESULT: the men the gate would exclude hit 8% against 22% for the rest (n=22 in all; a thin split, stated as such), and
the cell's 26.7% was measured on a population that INCLUDES them, so zeroing a gated man applies the constraint
twice. The bet lane prints "a stretch: needs N% of the passing game" beside the rate and prices him; it does not zero
him. Script `Scripts\research\wk1\reach_gate_test.py`.

**[doc 456, index row rides with v9.38] 4.45 TWO NULLS: THE SAME-TEAM RECEIVER PAIR, AND THE RELIEF RATE AGAINST THE
JOB, doc 456, `[TESTED]`.** (a) BASELINE: a receiver's rest-of-season rate given his own level. POPULATION: WR pairs on
one team, nflverse 2021 to 2025, weeks 1 to 14. RESULT: holding both men of a pair moves neither man's rate against
holding one (the interaction is inside its interval), so the draft model's same-team pairing (Adams beside Nacua) is
neither a bonus nor a penalty on the page; `Scripts\research\wr_pair.py`, `wr_pair_results.md`. (b) BASELINE: the flat
relief rate, 12.1 half-PPR a game for about three weeks (`sheet_constants.json` seat). POPULATION: every absence of a
team's weeks-1-to-4 usage leader over weeks 5 to 14, 2022 to 2025, the direct backup's rate in those weeks against the
job's August worth (n=51 absences, `job_slope_absences.csv`). RESULT: no slope (the coefficient is inside its interval),
so one relief rate stands for every seat and the job's worth is not a multiplier; `Scripts\research\job_slope.py`.

**[doc 457, index row rides with v9.38] 4.46 THE WEEK-1 WORKLOAD SCREEN'S RATE IS A LEADER'S RATE, doc 457,
`[TESTED, n=517]`.** BASELINE: the screen's own rate, 39.5% startable over weeks 2 to 14 for men clearing two or three
marks (doc 308). POPULATION: every WR and TE 2022 to 2025 who played week 1 with a target, was below his position's
replacement the season before and played 4+ of weeks 2 to 14 (n=517; 76 cleared). RESULT: cleared and led his team at
the position by week-1 targets, 25 of 54 (46.3%); cleared as the second man or lower, 5 of 22 (22.7%); every tight end
who ever cleared it led his team (15 of 15, 8 hit); a second tight end has never cleared it in four seasons. So the
38% beside Michael Mayer's name was a leader's rate printed for a man Bowers out-targeted 13 to 3; the bet lane now
reads the newest game's target leader at each position (`pos_leaders()`), gives a second tight end no rate and a second
receiver 22.7%, and a bet that is mostly a bye hole is a calendar claim for the week before the hole. Script
`Scripts\research\wk1\te2_split.py`; cells in `sheet_constants.json` `workload_second_man`, re-fit after the season.

**[doc 458, index row rides with v9.38] 4.47 A DEFENSE'S OWN SEASON-TO-DATE SCORING ADDS NOTHING BESIDE THE OPPONENT'S
IMPLIED TOTAL, doc 458, `[TESTED, n=2,238]`.** BASELINE: 4.39's rule, the lowest opponent implied total, +3 a week over
random. POPULATION: every unit-week with a pregame line, 2021 to 2025, weeks 2 to 14 (n=2,238; `own_quality_dst.py`
reusing `vegas_streams.py`'s file). RESULT: the unit's own average to date is minus 0.02 a standard deviation beside the
line's minus 2.12; as a pick rule it is +1.0 over random (t 1.2) against the line's +4.1 (t 5.7); head to head in Matt's
shape (a 30th-ranked unit on the softer matchup against an 8th-ranked unit on the harder one) the better matchup wins
60% at a 2-to-3-point gap (5.9 against 4.2 a week); a tier-by-band grid is flat and the tie-break within a point and a
half is +0.18 (se 0.59), noise. The matchup rule stands unchanged; a unit's record is not a term on the page.

**[docs 460, 461 and 462, index row rides with v9.38] 4.48 THE TAIL BY TICKET SHAPE AT THE END OF WEEK 4, docs 460 to
462, `[TESTED, n=32 to 285 by cell]`.** THE CLAIM, in Matt's words: *"a high end backup CAN hit, and some actually do hit
big ... When backups do hit, they stand to gain more than what is currently sitting on my bench."* BASELINE: the mean,
which is what the seat and bet lanes priced. POPULATION: every back and receiver UNDER the bar on weeks 1 to 4 (RB 9.92,
WR 9.62 half-PPR a game), nflverse 2021 to 2025, the shape read off his own team's touches a game on those weeks;
outcomes over weeks 5 to 14 (10 weeks): six or more startable weeks (big), a four-week window at 15 or more a game (a
month), four or more startable weeks. RESULT, big and month: lead back under the bar with 12+ touches 18.8% and 28.1%
(n=32; 12 to 15 a game 6.7% and 20.0%, n=15); lead back under 12 a game 0.0% and 22.2% (n=9); committee partner (the
second back with 8 to 14 a game) 8.5% and 13.6% (n=59); handcuff behind a top-12 job 0.0% and 5.7% (n=35); handcuff
behind any other job 5.6% and 5.6% (n=36); third string or lower 0.0% and 0.0% (n=249, 1.2% four-plus weeks); young
receiver 3 of 3 on the in-season screen 4.5% and 4.5% (n=22, 36.4% four-plus); 2 of 3 4.8% and 9.5% (n=42); 0 or 1 of 3
0.0% and 0.0% (n=68); veteran receiver with 2+ targets a game 1.4% and 2.5% (n=285). THE HANDCUFF WHEN THE STARTER FALLS:
one in four (17 of 71) saw his lead back miss three or more of the ten weeks; those gave four-plus weeks 35.3%, six-plus
11.8%, a month 5.9%; the rest 5.6%, 0.0%, 5.6%. WHERE THE BIG STRETCHES COME FROM: of 67 backs with six-plus startable
weeks over weeks 5 to 14, 52 (78%) were already startable on weeks 1 to 4; 6 were lead backs under the bar, 5 committee
partners, 2 handcuffs (Kenneth Walker 2022, Tyrone Tracy 2024), none third string; receivers 54 of 66 (82%). EFFICIENCY
DOES NOT MOVE IT (doc 462): yards per touch on weeks 1 to 4 under 4.0 against 4.0 and over leans Matt's way inside the
committee cell (12% against 34% four-plus, p=0.067) and the other way inside the handcuff cell (24% against 3%, p=0.039),
is flat pooled (26.8% against 26.8%), and correlates 0.09 with yards per touch over weeks 5 to 14 (Spearman, n=122);
points per touch rho minus 0.06 and 0.03 against the two outcomes. THE POPULATION HEADER, stated every time: "could be
held on a bench", NOT "was free in a 12-team league"; a lead back with 12+ touches is almost never on the wire. WHAT
CARRIES IT: the long-shot lane on the week sheet (doc 461: every free back and receiver under the bar in his cell, ranked
on the two big-hit columns, at most three of a shape, above the seat list when he is outside the top six by points for,
tilde on a cell under twenty men), `sheet_constants.json` `tail_tickets`, `Scripts\research\wk1\tail_tickets.py`
(`--check` guards the cells). The 2017 Hunt shape is a draft-day handcuff whose starter fell in August: by week 4 that
man is a starter and off the wire, which is 4.27's trigger (production in relief) seen from the other side. NOT YET RUN:
the handcuff cell against the starter's prior-season games missed (4.22's instrument); the lead-back cell on the latest
game's touches rather than the four-week average (4.38's level). Re-fit after the season.

**[v9.39] 4.49 The matchup term in season (doc 468).** BASELINE: the man's own half-PPR rate to date (rho 0.50 to 0.60 with the
coming week at every position); the question is what the opponent adds net of it. POPULATION: nflverse regular season 2021 to
2025, weeks 5 to 18, receivers, tight ends and backs with three or more games played so far, the coming opponent with four or
more weeks of record; 17,799 player-weeks (8,444 WR, 4,114 TE, 5,241 RB). INSTRUMENT: the opponent's half-PPR points allowed per
game to the position through the previous week, centred on that week's league average (the crowd's own instrument; ESPN's
positionAgainstOpponent is this number for this season). RESULT, coefficient per point allowed above the mean (se) and the
decision form (0.5(a7): between two men of equal rate, the gain from the softer matchup, top quartile of defenses against
bottom, in points a week): WR 0.022 (0.014), +0.37, positive in three of five seasons with the sign flipping (2023 +1.16, 2024
minus 0.60); TE 0.118 (0.028), +0.89, four of five; RB 0.113 (0.023), +1.24, five of five (+0.5 to +1.6). Net of the own implied
team total the coefficients are 0.021, 0.111 and 0.096: the line takes little from it. The bar was set before the run at a
point a week (4.11's size); RB clears it, TE sits at it, WR fails it. AGAINST DOC 227: that doc measured the PRIOR season's
points allowed (QB about a point, RB +0.56, WR and TE null) and set aside the same season's full-year average as hindsight;
this season's points allowed TO DATE is the third instrument and lands between the two, so doc 227's rule stands at receiver
and is qualified at tight end, and 4.33's "elsewhere, take the player" stands with a within-a-point tiebreak at RB and TE.
THE RULE: a tiebreak within a point at RB and TE, never a reason to move a man off a better rate, never at WR. THIS WEEK ON
THREE WEEKS OF 2026 (thin; the measurement needed four): nothing on his roster moves across a point. WHAT CARRIES IT: the
wire's streaming sentence (doc 468); the page column on the roster rows and the drop ladder for RB and TE, from
`sched_2026.csv` and `form_2026.csv`, ~~is NOT YET RUN~~ **[doc 472] is built: `matchup vs OPP +x` beside the rate, the
coefficient times the centred points-allowed term, a defense with four finished weeks of record or nothing, a man on bye
nothing, never sorted on; `check_page_logic.py` P11 recomputes it from the two files independently of the engine and fails
a build that prints it on a receiver, prints a number the files do not give, or leaves it off a roster back or tight end
whose opponent has the record.** `Scripts\research\matchup_term.py` (`games.csv` beside it for the line
control), `run_matchup_term.txt`, `run_matchup_term_line.txt`.
