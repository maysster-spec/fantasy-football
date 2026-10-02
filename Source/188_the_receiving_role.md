# 188 — Matt's pass-protection fade is the first mechanism of his that survives

**2026-09-06 (T−1).** Matt: *"One of the fades that I had on TreVeyon was the fact that he's not
as good in pass protection. Do you see any legitimate signal with that statement that can be
applied to other players?"*

**Short answer: yes, and it is the strongest new finding this project has produced.**
`[TESTED, n=211 RB-seasons with a §1.1 preseason ADP, 4 transitions 2021→22 … 2024→25]`

---

## 1. WHAT I CANNOT MEASURE, SAID FIRST

**Nothing in this project measures pass protection.** PFF grades are the only public per-player
blocking measure and we do not have them. So the direct test cannot be run, and I am not going to
pretend otherwise.

**What I can measure is the thing pass protection buys: the passing-down role.** If a back can't
block, he doesn't play on third down, and the observable consequence is a small share of his team's
targets. So the honest version of Matt's hypothesis is: **is a running back's receiving role a real,
durable, unpriced trait?** Three questions, in order.

**Data:** nflverse weekly player stats 2021–2025 (fetched for this; new to the project), regular
season, RBs with **≥50 carries** in the signal year. Scoring converted to **§2's 0.5 PPR**
(`fantasy_points_ppr − 0.5 × receptions`). Preseason ADP from the **§1.1 registry** — never a
historical `espn_adp`.

---

## 2. DOES IT PERSIST? YES — MORE THAN THE RUNNING ROLE DOES

Year *t* → year *t+1*, both seasons with 50+ carries, **n=189**:

| trait | persistence |
|---|---|
| **target share** | **r = +0.676** (p=1.4e-26) |
| targets per game | r = +0.646 |
| carries per game | r = +0.607 |
| half-PPR points per game | r = +0.587 |

**A running back's slice of the passing game is more durable than his slice of the carries.**
For scale: §4.24(a) called team sack rate *"the most persistent team trait measured in this
project"* at **r=+0.399**, above offensive EPA (+0.382) and a defence (+0.204). **This is +0.676.**
It is the most persistent thing this project has measured, full stop.

---

## 3. IS IT PRICED? PARTLY — AND NOT ENOUGH

**BASELINE — state it every time: half-PPR points, weeks 1–14 of year *t+1*, regressed on
log(preseason ADP) within each season. BEAT = the residual. sd(beat) = 55.0 points.**
Price alone explains a lot (r = −0.549 to −0.720 by season), which is why the residual is the test.

| prior-year signal | correlation with the beat |
|---|---|
| **target share** | **r = +0.121, p=0.079** |
| targets per game | r = +0.139, **p=0.043** |
| carries per game | r = +0.091, p=0.189 |

Extremes, on cut points taken from the full panel and not from this board:

> **Top quartile of prior-year target share (n=53): +11.6 points over price.**
> **Bottom quartile (n=53): −15.6.**
> **Difference +27.1 points, p=0.011, 95% CI [+6.4, +47.8].**

**The market does pay for it** — corr(prior target share, log ADP) = **−0.560** — it just does not
pay enough. **Same shape as §4.22(c):** the discount runs the right way and stops short.

---

## 4. I RED-TEAMED MY OWN RESULT FOUR WAYS AND IT HELD

Three nominally significant results have already died in this project on exactly these checks, so
they ran before this doc was written.

1. **Is it just "good players are good"?** Multiple regression, beat ~ target share + prior ppg +
   prior games + prior carries/game: **target share +248.3, p=0.030.** A ten-point share gap is
   **+24.8 points.** And **prior ppg goes NEGATIVE (−3.94, p=0.046)** — production regresses toward
   the mean while the role does not. Target share is not standing in for last year's points; it is
   the opposite of it.
2. **The same back appears up to four times.** Player-clustered standard errors, **95 unique backs,
   211 observations: +155.9, clustered se 69.3, p=0.024.** Holds.
3. **Is one season carrying it?** Top vs bottom tercile by year: **+12.4 / +15.1 / +28.8 / +9.0.**
   Same sign all four.
4. **PLACEBO.** The identical pipeline on prior-year **catch rate** — a skill stat with no role
   content, which should be null: **r=−0.070, p=0.314, quartile gap +1.5 points.** The pipeline does
   not manufacture significance.

**Matt's record on causal mechanisms was 0-for-4** (the offensive line, opportunity environment, the
year-two bounce-back, "our league is RB-heavy" — all null, §0.5(a)). **This one lives.**

---

## 5. AND IT KILLS THE BULL CASE THAT REBUTS IT

The standard answer to "he can't pass protect" is *"he's a second-year back, he'll learn it and
take the third-down job."* Measured, on rookies who cleared 50 carries and returned, **n=71**:

| | rookie year | year two | change |
|---|---|---|---|
| targets per game | 2.84 | 2.85 | **+0.01, p=0.953** |
| target share | 0.087 | 0.089 | **+0.002, p=0.628** |

**37 of 71 gained targets per game. A coin flip.** The receiving role a back has as a rookie is,
on average, the receiving role he has in year two. `[TESTED — NULL]`

---

## 6. APPLIED TO THE BOARD — and it costs me two of my own calls

Panel quartiles: **BOTTOM ≤ 4.6% · TOP ≥ 10.8%.** 2025 target share for live RBs:

**BOTTOM QUARTILE — the fade, with a price attached**

| player | adp | VOR | 2025 tgt share | note |
|---|---|---|---|---|
| **Bhayshul Tuten** | **61.2** | +19.8 | **2.9%** | **the expensive one. A pick-56/65 price on a bottom-quartile receiving role.** |
| J.K. Dobbins | 111.6 | −4.3 | 4.2% | |
| **Blake Corum** | **125.8** | −17.6 | **2.4%** | **I called him Batch C's best dart (doc 187).** |
| **Jacory Croskey-Merritt** | **136.4** | −17.2 | **3.0%** | **I called him best VOR of the C-band backs (doc 187).** |
| Jordan Mason | 139.3 | −24.8 | 3.5% | |
| Tyler Allgeier · Chris Rodriguez Jr. · Brian Robinson Jr. | 163–168 | — | 3.1 / 1.3 / 2.3% | |

**TOP QUARTILE, available past pick 55**

| player | adp | VOR | 2025 tgt share |
|---|---|---|---|
| **Kenny Gainwell** | 99.9 | −16.9 | **16.3% — highest of any back available after pick 90** |
| Aaron Jones Sr. | 114.4 | −15.1 | 13.8% |
| Tyjae Spears | 147.4 | −38.9 | 12.0% |
| Bucky Irving | 56.7 | +20.0 | 11.3% |

**TreVeyon Henderson is 8.7% — MIDDLE, not bottom.** Matt's direction is right and the magnitude
is not: Henderson is an ordinary receiving back, not a non-factor. The bottom quartile is where the
fade has teeth, and **Tuten at ADP 61 is the name it points at.**

**This board prices the trait exactly as the historical market did** — corr(2025 target share,
log adp) = **−0.643** against the historical **−0.560** — which is the condition under which the
+27-point residual existed.

### The methodological correction this forces on doc 185

**Archetype A5 ("pass-catching back") was scored on ESPN's PROJECTED 2026 targets. That is a
forecast, not a role, and it is the same mistake I made on Henderson in doc 187.** Re-checked
against observed 2025 share, the nine A5 flags with 2025 data split **4 TOP · 4 middle · 1 BOTTOM
(Tuten)**. **A5 should be re-based on prior-year observed target share.** Doc 185's flag was a
coin-flip proxy for the thing that actually pays.

---

## 7. SEPARATELY — THE DRAFT GRID IS STALE AND THE RUNBOOK CANNOT REFRESH IT

Matt asked whether the grid needed updating. It does, and the reason is a live defect.

- **`make_gridboard.py` is in NO rebuild path.** It is absent from `sept5_after.bat`, from
  `to_pdf.py` and from `check_kit.py`'s pins.
- It reads **`board_v8_fixed.csv`, `values.csv` and `player_context.csv`.** On the desk right now:

| file | last written (UTC) |
|---|---|
| **ADP_GRID.html / .pdf** | **2026-09-05 19:23** |
| board_v8_fixed.csv | 2026-09-05 20:03 — **40 minutes later** |
| player_context.csv | 2026-09-05 23:46, **and again 2026-09-06** — **hours later** |

- And **`sync_desk_copies.py` carries `ADP_GRID.pdf` to the desk anyway**, under a comment reading
  *"It builds its own PDF … so it can never be [stale]."* **That is doc 146's defect in a new
  place** — the reasoning is about the PDF matching its page, and they go stale *together* because
  nothing runs the builder. **`to_pdf.py --check` cannot catch this class by construction.**

**FIXED AND COMMITTED:** `sept5_after.bat` is now **eleven steps**, with `py make_gridboard.py` at
step 9 — after `mkoverride` (step 6) and `parse_ladder` (step 7), which write its inputs, and before
`sync_desk_copies`. It sets `STALE=ADP_GRID` on failure rather than exiting 0. **`check_kit.py`
re-pinned: `sept5_after.bat` 8,041 / `e17d803e809e51ce`, `player_context.csv` 85,644 /
`1cbd84e1ac8f2027`.** Pin method verified against the shipped hashes before either was touched.

---

## 8. WHAT THIS DOES NOT DO

- **No board edits.** Surfaced, not scored — §4.22's rule, and one measurement on 211 RB-seasons
  does not become a VBD coefficient the night before a draft.
- **It does not measure blocking.** It measures the role blocking buys. A back could earn the role
  a different way; the finding does not care which.
- Reproduce with `Scripts\research\` — the nflverse pull, the panel and the four red-team checks.
