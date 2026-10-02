# 423 — the kicker number was on the drive all along

**24 Sept 2026.** Doc 420 left the kicker replacement level **NOT ESTABLISHED** and said the row
should stay honest rather than numbered. That was the right call at the time and it was also a
failure of §0.5(a4), which says a "no" needs a named blocker and a path. The path was one script and
data already in `_nflverse_cache`.

---

## MEASURED

**Population**, stated rather than inherited (§0.6): nflverse weekly, 2021–2025, `season_type` REG,
position K, **weeks 1 to 14** because that is this league's regular season, and a man counts as
rosterable at **8 or more games** in that window — 29 to 31 kickers a year. Scored under **this
league's own rules** from `2026_League_Settings.txt` (§2): PAT 1 · FG 0–39 = 3 · 40–49 = 4 · 50+ = 5 ·
FG missed −1. A missed PAT is not penalised in these settings.

Ranked by season total, exactly as doc 265 ranked D/ST12:

| season | K1 | **K12** |
|---|---|---|
| 2021 | 11.08 Nick Folk | **8.46** Tyler Bass |
| 2022 | 9.85 Tyler Bass | **8.08** Evan McPherson |
| 2023 | 11.31 Brandon Aubrey | **8.38** Harrison Butker |
| 2024 | 12.54 Chris Boswell | **8.08** Younghoe Koo |
| 2025 | 11.85 Jason Myers | **8.31** Cam Little |

**REPLACEMENT = 8.26 a week, sd 0.16, n=5 seasons.** That is tighter year over year than almost
anything else measured here. **K1 runs 9.9 to 12.5**, so the whole spread from the best kicker in the
league to a replacement is about **2 to 4 points a week**.

→ **A kicker's drop cost is his rate minus 8.26**, because the slot is mandatory and what replaces
him is another kicker.

**For Matt right now: Pineiro is 9.2 a week, so he is worth about +0.9 over a replacement**, roughly
ten points across the rest of the fantasy regular season. Not free to drop. Not sacred either. That
is the answer to *"who am i replacing my kicker with?"* — anybody, and it costs you about a point a
week.

## THE LIMIT, AND IT IS ON THE LINE ITSELF BECAUSE DOC 421 HAPPENED FOUR HOURS AGO

**This is a SEASON number answering a season question**, which is the question the drop table asks:
what does the starting nine lose over the weeks still ahead. **It says nothing about any given week.**
A kicker's week is his matchup and his leg.

`WEEKLY_VALUE` in `sheet_engine.py` still refuses to print a season rate against a weekly decision,
and that stands. The difference between this and the defense error is the horizon of the QUESTION,
not the horizon of the number: *"should I roster this kicker or a different one"* is a season
question. *"Should I start this defense on Sunday"* is not.

## WHY A SCRIPT AND NOT A NUMBER IN A DOC

`Scripts\research\k12_replacement.py`. Doc 417's lesson applied without needing to be reminded: the
first `BLEND_W` table was fitted inline from a population nobody wrote down, and eighteen definitions
later none of them reproduced it. **A measurement with no script is a memory.**

## WHAT IS NOT CLOSED BY THIS

The drop table still prints the honest sentence rather than 0.9, because wiring the number in means a
seventh edit to `sheet_engine.py` tonight and it would re-open the `WEEKLY_VALUE` rule shipped hours
earlier. **The number exists and is reproducible; putting it on the page is queued deliberately, not
forgotten.** **NOT YET RUN.**

## OPEN, carried

- **[OPEN]** Wire 8.26 into the kicker row of the drop table. **NOT YET RUN**, and deliberately so.
- **[OPEN]** The weekly D/ST pool onto the page — still the largest in-season gap, and the direct fix
  for what went wrong tonight.
- **[OPEN]** §4.8 and §4.9 are draft-era findings now load-bearing in season, and both should be
  re-read with a season scope. This doc is the second thing in two days to trip over them.
- **[OPEN]** The draft-era board hiding 72 available players; the duplicated ESPN credentials in
  `Espn_pull_projections.py`; doc 369's cards section and print.
