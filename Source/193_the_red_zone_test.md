# 193 — I tested the mark I shipped an hour earlier. It is null. It is off the sheet.

**2026-09-06 (T−1).** Matt: *"your point about tiebreaks doesn't measure for WRs is
counter-intuitive… are you sure you are combining all the signals that are needed"* and
*"adding in signals in COMBINATION is what I intended, and not to add noise that can't be measured."*

## 1. THE RED-ZONE PANEL EXISTS NOW — 2,032 player-seasons from play-by-play

Doc 192 named this the top post-draft item because it needed nflverse play-by-play, "a build and
not a lookup." Built it: five seasons, inside-10 targets and touchdowns per player-season.
**§4.5 has always said the role PERSISTS (in-10 targets r=+0.59). Nobody ever asked whether it PAYS.**

**BASELINE: half-PPR wks 1–14 of year t+1 on log(§1.1 preseason ADP), within season. BEAT = residual.
WR/TE with ≥40 prior targets, n=390, player-clustered.**

| prior-year signal | effect | p |
|---|---|---|
| inside-10 **targets** | −0.3 | 0.641 |
| inside-10 **touchdowns** | −1.1 | 0.389 |
| **targets NET of the TDs** — the "he is owed scores" idea | **+0.4** | **0.590** |
| target share | +1.9 | 0.958 |
| **prior games played** | **+1.7 per game** | **0.043** |

**The green `rz7-0` mark I shipped an hour before this encoded exactly the third row, and it is
null.** The red-zone role persists *and the market already prices it*. Persistence is not payoff —
§0.2's oldest rule, and I walked into it by shipping a mark before testing it.

**REMOVED.** The tier sheet now prints **games played** for any receiver under 13, darker under 10.
That is the one receiver signal that measures, and it is the same thing the board's `12g` badge
carries.

## 2. AND THE WR COMPOSITE DOES NOT WORK EITHER

Three signals — top-quartile in-10 targets, 15+ games, top-quartile target share:
**count of 3 = +2.4, p=0.259**, and the ladder is **not monotone**: 0 of 3 → **−19.0**, 1 → −9.7,
2 → −9.4, 3 → **−12.7**. Against the RB ladder (−24.4 / −19.3 / −0.4 / +7.8) it is noise.

**Receivers get ONE thing: availability.** That is not me declining to combine — it is three
combinations tested and one term surviving.

## 3. AGE IN COMBINATION — Matt's specific idea, tested

*"Age is an indicator of lack of speed, more wear on the tires, more likelihood of injury."*
Interaction of **age 29+** with **missed time last year**, n=699:

| | healthy | missed time |
|---|---|---|
| **under 29** | −8.0 (n=388) | −18.8 (n=156) |
| **29+** | −9.5 (n=109) | **−25.3 (n=46)** |

**The interaction term is −5.1, p=0.534 — NULL.** Age alone −3.1, p=0.432. **Missed time alone is
−12.0, p=0.002 and does all the work.** His worst cell is real (old *and* hurt = −25.3) but it is
not separable from "hurt" at this sample. `[TESTED — the combination adds nothing]`

## 4. CHANGING TEAMS — I said it was baked in. Mostly right, with one exception.

| population | effect | p |
|---|---|---|
| all positions | −8.0 | 0.090 |
| RB | −2.7 | 0.730 |
| WR | −1.4 | 0.780 |
| TE | +2.8 | 0.663 |
| **QB** | **−32.2** | **0.013** |

**A quarterback who changed teams beat his price by 32 points less.** n=108, one measurement, and
it is the only place the move matters. Interaction with health: **+3.9, p=0.671, null.**
`[TESTED — null at skill positions, live and unreplicated at QB]`
**On this board that flags Kyler Murray (MIN) and Fernando Mendoza (LV).** Not actionable at
Matt's picks — both are past 137 — but it belongs in the record.

## 5. THE SCORECARD AFTER TONIGHT

**RB — three signals, works:** target share · 13+ games · NFL rounds 1–3. +12.2 per signal, p=0.0008.
**WR/TE — one signal:** games played. +1.7/game, p=0.043.
**QB — one signal, unreplicated:** did not change teams.
**Dead, now including the ones tested in combination:** age (alone and interacted), workload,
vacated targets, teammate dependence, after-contact, year-2, **red-zone role (alone, net of TDs,
and inside a composite)**.
