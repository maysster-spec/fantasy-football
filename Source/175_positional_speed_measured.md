# 175 — How fast each position comes off the board, against keeper-adjusted ADP

**Date:** 2026-09-05 (Sat night ET) · **Trigger:** Matt: *"my ask was to compare how fast RBs come
off the board compared to normalized ADP, effective ADP for our keeper league"* — then *"do the same
for each position… I think you did this before and that forecast may already be baked in."*

**Both corrections were right. And the answer is WR, not RB.**

---

## 1. WHAT WAS BAKED IN: almost nothing

§4.12 fits exactly **two** things — *TE effective ADP +15 picks*, and *Snyder takes Josh Allen at
q ≈ 0.90*. `eff_pick` bakes in **keeper depletion**, which is normalisation, not tendency.
**No positional timing tendency other than TE existed anywhere in this project.** §4.12 even says so:
*"RB/WR pace gaps rest on 2 drafts — left uncorrected, `[HYPOTHESIS]`."*

## 2. WHY MY FIRST ANSWER WAS THE WRONG TEST

I measured RB **relative to WR**, controlled for price — a *contrast*. A contrast cancels anything
the whole board shares, and this board shares a lot: **12 keepers come off before pick 1**, which
compresses everything by ~10–12 picks. Matt asked for the **absolute** speed against the
keeper-adjusted market. That is a different quantity and it needed a different measurement.

**BASELINE, stated: `speed = actual slot − effective ADP`.** `slot` = position among true
selections, 1–168. `effective ADP` = preseason ADP minus the keepers priced ahead of him.
Negative = comes off the board **faster** than the market.
**POPULATION: 5 seasons (2021–25), n = 680 true selections**, §1.1 preseason registry only — never
historical `espn_adp`. Keeper rounds differ by era (round 1 in 2021–23, round 15 in 2024–25) and are
converted to the same coordinate.

## 3. THE RESULT

| eff ADP | RB | WR | TE | QB |
|---|---|---|---|---|
| **1–24** | −0.1 (t −0.16) | **+3.5 (t +4.55)** | **+4.3 (t +4.43)** | **−9.3 (t −3.40)** |
| **25–60** | −2.2 (t −1.25) | **+6.6 (t +5.00)** | +3.2 (t +1.26) | −3.1 (t −1.04) |
| **61–120** | +1.8 (t +0.81) | **+5.8 (t +3.53)** | −4.3 (t −1.28) | +1.4 (t +0.37) |

n per cell: RB 53/48/88 · WR 53/80/103 · TE 6/20/37 · QB 6/24/41. Board-wide mean **−1.90**.

**WR IS THE FINDING.** Significant in all three bands, same sign, large n. **Receivers last 3–7
picks longer in this league than the keeper-adjusted market says.** It is the most robust
positional-timing result the project has.

**RB IS A NULL IN EVERY USABLE BAND.** So the "RB-heavy league" is **real as an experience and wrong
as a mechanism**: it is not that backs fly, it is that **receivers fall**. From slot 8 that
distinction matters — it means the WR you want is more likely to be there, not that you must reach
for a back.

**TE at the top is trusted despite n=6** because it reproduces year by year: the first TE off the
board went **+5.0, +5.0, +1.8, +9.0, +6.0** across the five drafts. **QB top-24 is n=6 and
underpowered**; kept only because it agrees with §5's independent timing table.

**THE 121+ BAND IS EXCLUDED AND MUST STAY EXCLUDED.** The draft is 168 picks long, so a player
priced near it can only ever be taken *earlier*. Every position looks fast there (RB −16, WR −35,
TE −19) and all of it is **censoring, not tendency**. This is §4.23's trap in a new place.

## 4. AND IT CORRECTS §4.12's TE NUMBER — BY 3×

**§4.12's "+15 picks" is a RAW-ADP number.** Measured in the keeper-adjusted coordinate the same
statistic is **+3 to +5**. The gap is the keeper compression, charged to tight ends alone.

I had already shipped **+15** onto the grid yesterday citing §4.12, and then **−15** for QB on my own
two-draft contrast. **Both were about 3× too large and both are now the measured values: TE +5,
QB −4, WR +5, RB 0.** RB moving by nothing is its measurement, not an omission.

**THIS CHANGES WHAT THE GRID DRAWS AT PICK 32.** With +15, Bowers and McBride were drawn as
available at 32. At the measured **+5** they are drawn at **cells 25 and 24 — gone before 32** —
and **Judkins lands exactly on cell 32**. §7's rule at 32 is *"any of them, first one showing"*, so
this does not contradict §7; it predicts which of the five shows. **§7's own verdict is untouched:
it rests on the engine's dollar simulation over 100 board states, not on this shift.**

## 5. WHAT WAS NOT TOUCHED

The board, the engine, `_lineup`, the prerank, `news_overrides.csv`: **none.** This is the grid, a
reference sheet, plus this doc. §4.18c stands — do not change what the objective measures before
Sept 7.

**Honest provenance caveat:** this measurement is twenty minutes old on the night of T−2. It is
better evidenced than what it replaces (5 seasons and n=680 against §4.12's unstated fit, and
against my own 2-draft contrast), and it is applied only to a page that decides nothing. **If any
of it feels wrong at the table, the live board is what drafts.**
