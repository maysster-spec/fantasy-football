# 19 — INTEGRITY AUDIT, Aug 22 2026
**Method:** deterministic scan of all 32 project data blobs + both shipped artifacts, in code.
Reproduce with `python code_audit_v1.py --src <source dir>`. Register: `defects_20260822.csv`.
**22 checks · 18 FAIL · 2 CRITICAL · 8 HIGH · 1 false positive caught and discarded.**

Nothing below is an opinion about strategy. Every line is a number in a source file
disagreeing with a number in a shipped artifact or in the project directive.

---

## THE HEADLINE: the directive is pinned to the v2 build; the spine is v4

`00_PROJECT_DIRECTIVE_v4.md` is injected into **every turn of every chat in this project**.
Its §4.1 and §4.7 numbers do not reproduce from the current data. `HANDOFF_v2.md` §7 and
`GEMINI_REDTEAM_PACKAGE.md` §3 carry the *correct* values. The governing document is the
stale one, so every new session starts from bad constants and only discovers it late —
which is the failure mode you described.

| directive §4.1 claim | current `code_universe.csv` | gap |
|---|---|---|
| RB30 = 168.0 | **168.6** | +0.6 |
| WR30 = 168.5 | **163.5** | **−5.0** |
| QB12 = 341.7 | **341.6** | −0.1 |
| TE12 = 137.7 | **140.3** | +2.6 |
| Gibbs +163.5 · Nacua +126.5 · Allen +79.7 · Bowers +53.3 | **162.3 · 131.3 · 80.3 · 51.2** | up to +4.8 |
| §4.3 McBride +50.4 · Warren +27.8 · Andrews +2.9 @ pick 80 | **47.6 · 28.1 · 0.0 @ ADP 113** | Andrews *is* TE12 |

WR30 falling 5.0 moves every WR +5 against every RB. §4.10's strategy ranking (top four
span 6.5 points) was computed before that shift. **The strategy table is inside its own
noise band relative to a correction it has not absorbed.**

---

## CRITICAL 1 — `code_universe.ADP` is not average draft position

**0 of 341** matched rows equal `espn_adp`. Median gap inside the draftable range: **7.6 picks**.
The gap is structured, not noise:

| espn_adp band | mean(ADP − espn_adp) | mean(ADP − dense rank) |
|---|---|---|
| ~19 | −2.2 | **0.0** |
| ~52 | −6.6 | **0.0** |
| ~92 | −13.0 | +1.3 |
| ~122 | −10.4 | +4.8 |
| ~149 | −3.7 | +8.4 |
| ~167 | +15.9 | +15.8 |

Through the top ~60 players, `ADP` is **exactly the dense rank** of ESPN ADP. It is an
ordinal, and it is used everywhere a pick number is required.

**Downstream uses, enumerated (directive §3 requires this):**
1. §2.1(c) effective-ADP table — mixes rank against pick numbers; the offset at 41 is understated.
2. §4.12 opponent noise `sd = 0.135 × ADP` — fitted on a rank, applied as pick noise.
3. Every `p(available)` on the grid.
4. `keeper_eligibility_VERIFIED.csv` `ESPN_ADP` carries the same rank (Pickens 27, Rice 21) —
   so the *"ADP-based keeper prediction beat projection-based 3-for-3"* finding was measured
   on this column.
5. **HANDOFF §9.6 — "nearly every manager drafts ~5 picks ahead of ADP, beyond what keeper
   depletion explains."** Mean(ADP − espn_adp) across the relevant range is ≈ −5.
   `[HYPOTHESIS, high prior]` — that residual is probably this artifact, not manager behaviour.
   Confirm against `code/resid.csv`; if it holds, open thread #6 closes and survival
   probabilities are biased in a *known* direction rather than an unknown one.

**Second-order:** ESPN ADP is censored. **492 of 700 rows (70%) sit in a 1.56-pick blob at
~170** — the undrafted sentinel. Pick 152 has effective ADP ~164 and pick 161 ~173.
**Pick 161 is past the end of the informative ADP range.** No ordering exists there.

---

## CRITICAL 2 — the D/ST projections were never missing; the join dropped them

Open thread #12 says *"D/ST projections are all exactly 50.0 for 29 defenses. Pick 152 is
uninformed."* **Misdiagnosed.** ESPN's own pull carries 32 real, differentiated D/ST
projections:

- range **55.4 → 128.4** (Dolphins → Broncos), sd 20.7 — a **73-point spread, ~5.2/week**
- `corr(proj_2026, espn_adp) = **−0.823**` — the market prices them and tracks the projection
- `proj_2025` reconciles against `actual_2025` (Texans 128.3 → 153, Broncos 129.2 → 129)

`code_universe.csv` instead holds 29 rows keyed `"Houston Texans"` against ESPN's
`"Texans D/ST"`, `proj_src = v2_carryover`, `TOT` hard-set to **50.0** for all 29, `VBD` null.
**Falcons, Saints and Colts are absent entirely.** This is name-join failure **#8**.

Caveat, stated honestly: §4.8 (11–12 of 12 teams stream a D/ST every year) survives and caps
how much this is worth. It changes pick 152 from a coin flip to an ordered choice; it does
not make D/ST a draft asset. **19 of 44 kickers are also `v2_carryover`** — pick 161 same story.

---

## HIGH — 32 injury flags inside ADP 170 appear on neither artifact

`injuryStatus` is in the ESPN pull. `code_universe.csv` has **no injury column**; the HTML
board contains the string "injury" **zero** times. Inside ADP 170: **28 QUESTIONABLE, 3 OUT,
1 DOUBTFUL**. Ten sit inside ADP 50:

> **Puka Nacua**, **Christian McCaffrey**, Jeremiyah Love, Josh Jacobs, Malik Nabers,
> Breece Hall, DeVonta Smith, **Emeka Egbuka**, **Tyler Warren**, Quinshon Judkins

The handoff flagged Love alone. It is 32, and it includes **the pick-8 primary and two of
your own keeper candidates**. **Zero of the 32 have `proj_2026` zeroed** — ESPN's projection
does not price its own flag, so this is not double-counting.

*Discipline:* an August ESPN "QUESTIONABLE" is a low bar with untested predictive value here.
**Surface it, do not score it** — a red dot on the board, not a VBD haircut.

---

## HIGH — the early-TE read, and a correction to my own first pass

**I got part of this wrong and `ERROR_PATTERNS.md` A14 already had it right.** A14's rule is
*do not count in rounds in this league; count in overall pick numbers, which are unambiguous* —
because keepers occupied round 1 in 2021–23 and round 15 in 2024–25, so "round" means two
different things depending on the year. My first pass counted in rounds and then told you the
handoff had cited the wrong evidence for Cary. **On the keeper-adjusted convention the directive
mandates, Cary's Kelce at overall pick 30 in 2022 counts, the handoff was right, and my
correction was the error.** Logged below as a caught false positive.

Recounted in overall pick numbers only, true picks, keepers excluded, from
`draft_history_2021_2025.csv`:

**First TE off the board, by year: pick 22 · 30 · 20 · 41 · 22. Median 22.**
- 2021 pick 22 — Travis Kelce — *Buffalow Expectations*
- 2022 pick 30 — Travis Kelce — **Cary**
- 2023 pick 20 — Travis Kelce — *Pierce (departed)*
- 2024 pick 41 — Travis Kelce — *Wilson Kam*
- 2025 pick 22 — Brock Bowers — **herman allen**

**A TE left the board before pick 32 in three of the last five drafts.** You took Kittle at
pick 35 in 2025 yourself.

What is still wrong in the shipped documents:
- **Directive §4.7 / §5** — *"1 of 43 team-seasons… allen is the league's ONLY early-TE
  manager."* **False.** Two threats sit ahead of you: **Cary at slot 1 (picks 1 and 24)** and
  **herman allen at slot 5 (picks 20 and 29).**
- **HANDOFF §0** — *"none (2024)."* A14 reads this as *none early*, which is right; a TE did
  go, at pick 41.
- §4.7 median first TE round is **6**, not 7. Rounds 1–4 RB/WR is **82.8%**, not 83.3%.
  First K at 11+ is **94.9%**, not 95.8%. All three match the red-team package and contradict
  the directive.

**Net effect on pick 32:** with the median first TE at pick 22 and a TE gone before 32 in
three of five years, HANDOFF's McBride p≈0.58 is the better read. Note it was computed on the
rank-scale ADP (CRITICAL 1), so it needs recomputing either way.

## MED / other confirmed

| # | finding |
|---|---|
| E1 | Team codes disagree: universe **WAS** vs ESPN **WSH**; `proe_team_season` uses **LA** for LAR; the depth-chart file has **155** distinct `Team` values where 32 belong. Any team-level join — the OL-status work in HANDOFF §1 — silently drops Washington, the Rams and Arizona. |
| H1 | **2022, 2023 and 2024 hold 178 picks, not 180.** Two picks missing per year. Every §4.7 percentage and every franchise-bias z-score runs on incomplete drafts. |
| I1 | **7 of 53 eligible keepers carry no projection** — Travis Hunter, Stefon Diggs, Joe Mixon, David Njoku, Xavier Legette, Hollywood Brown, Jaylin Lane. Lobsinger's keeper is predicted from 2 of 3 candidates. |
| X1 | **The grid contradicts itself in round 1.** Hard rule: *"NEVER London/Allen/McBride/Jeanty."* Same row lists **Ashton Jeanty (+7, p0.89) as the top RB** and **Drake London (+1, p0.92)** as the third WR. |
| X2 | **Grid rows 13 and 14 (picks 152, 161) are empty** — the direct consequence of CRITICAL 2. |
| X3 | Grid predicts **Cary keeps Rashee Rice**. HANDOFF §7 says *"Rashee Rice (22.3) is live at pick 17."* Both cannot hold. |
| X4 | Grid Opponent-needs still ships **"Aubrey (K) unreliable"** for slot 4 — the known error, and §4.9 says exclude K from keeper prediction entirely. Excluding K, Brown/Collins' best eligible is Quentin Johnston (VBD −30.1). |
| X5 | HTML board is **364 rows** vs universe 494 vs ESPN 700, sorts on **Boone-minus-ADP** (the retracted spine), and shows **no p(available)** — which the grid does show. The two artifacts disagree on what a pick needs. |
| X6 | The Fade sheet's `Why` column is **the same sentence on all 18 rows**, all of it Boone-derived. |

## PASSED — do not re-litigate

- **§4.11 bye traps: all 16 named players verified correct.** One bye per team, 32 teams, no conflicts.
- **§2.1(b) pick structure: 8·17·32·41·56·65·80·89·104·113·128·137·152·161 is arithmetically right**, and pick 176 is the round-15 keeper slot. Confirmed against 12-team snake math.
- Keeper file covers all 12 teams; every predicted keeper is in it.
- ESPN pull carries a capture date, 2 days old.

## FALSE POSITIVE — caught and discarded

**Two, both mine.**

1. First pass reported **33 duplicate `espn_id` values in the universe**. There are none.
   `pandas.duplicated()` treats `NaN == NaN`, and 33 rows have no `espn_id` (29 D/ST + 1 K +
   1 RB + 2 TE).
2. First pass said the handoff cited the wrong evidence for Cary as an early-TE manager. It
   did not. I counted in rounds; `ERROR_PATTERNS.md` A14 says not to, and A14 was already in
   the project. This is D2 — *before declaring a premise dead, search the project for an
   existing test of it* — committed against the very file that documents D2.

Verifier false-alarm rate: **2 in 22 checks.** Both caught before they changed a
recommendation, one of them only because the user supplied `ERROR_PATTERNS.md`.
