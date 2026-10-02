# 156 — The ladder has no "top", and the one fact about rookies was already computed

*2026-09-04 (Sept 3 evening Eastern), T-4. Three questions from Matt.*

---

## 1. THE VALUE LADDER'S HTML IS A BUILD INTERMEDIATE, NOT AN ARTIFACT

Matt: *"the html view of the value ladder is garbage. I've never seen the use for it."*

He is right that it is not for reading. `mkvalue.py` writes `VALUE_LADDER.html` and then converts
it; the HTML only still exists because `to_pdf.py` consumes it (Chrome headless `--print-to-pdf`,
built because **wkhtmltopdf is not installed on his machine** and every PDF builder was silently
leaving a stale PDF behind). It is the *source* for the PDF, not a second copy of it.
**Nothing should ever hand him the .html.** The PDF is the artifact. Same for `DRAFT_BOARD.html`,
`FALLBACK_BOARD.html` and `OVERRIDE_CARD.html`. Post-draft cleanup: move all four to
`Source\_build\` and repoint `to_pdf.py`. Not before Monday — doc 79 records three sessions moving
one tree in a day and every prose map going stale within hours.

---

## 2. "HOW DO I DETERMINE HIGHEST VALUE ON THE LADDER?" — IT HAS NO TOP, ON PURPOSE

The ladder's own legend says it: *"this is a reading order, not a ranking — and deliberately not by
VBD or board rank, because that is the draft board's job and a second copy of it would be worse."*

Inside a PICK block the rows are ordered **fact first, then AGREE, then how big the open job is,
then the analyst gap.** So the top row of a block *is* the ladder's answer — but it is an
agreement count, not a value estimate, and BOARD is greyed out and not counted.

**The clean rule, and it comes from doc 153 §8's measured margins:**

| where | the board's margin over its runner-up | who decides |
|---|---|---|
| picks 8 · 17 · 32 · 41 · 56 | **13.6 / 5.0 / 13.4 / 7.8 / 2.3** | **the board.** Take row 1 and do not shop the ladder |
| picks 65 → 137 | **2.5 falling to 0.06** | **the ladder.** The board cannot separate its top rows; this is what the ladder is for |

**So the ladder is not a shortlist to pick from — it is the tiebreaker for the half of the night
where the board has no opinion.** Reading it as a ranking in rounds 1–5 would override a 13-point
measured edge with an agreement count that this project has repeatedly measured as unpredictive
(§4.13d).

---

## 3. ROOKIES — THE FACT WAS ALREADY IN THE PIPELINE AND NOTHING SHOWED IT

Matt: *"I do want exciting rookies promoted... I don't want someone flat that will put up
consistent points when all those points will be in the single digits."*

**(a) The data already knew.** `games_2025.csv` carries **`g25 = -1`** for a player with no 2025
regular-season snap — 81 rows. `make_board.py`'s availability badge correctly *excludes* it
(`if 0 < g25 <= 12`), because a rookie is not an injury warning. **Verified, no defect there** — a
rookie was never mislabelled as the worst injury band. But nothing displayed it either, so the one
unambiguous fact about these players fell through every crack.

**(b) `-1` is NOT rookie status, and the conflation matters.** It also catches a veteran who missed
the whole season. In the drafted range that is **3 of 12** — Jonathon Brooks (ACL), MarShawn Lloyd,
Tank Dell. Calling Tank Dell a rookie on draft night would be worse than saying nothing. The test
used is **no 2025 snaps AND absent from BOTH the 2023 and 2024 ESPN player pulls** — two seasons,
both already on disk, no new source, re-derivable. `[TESTED]`

**9 rookies inside the drafted range:**

| player | pos | tm | adp | board rank |
|---|---|---|---|---|
| Jeremiyah Love | RB | ARI | 26.1 | 18 |
| Jadarian Price | RB | SEA | 67.3 | 49 |
| Carnell Tate | WR | TEN | 77.6 | 66 |
| Makai Lemon | WR | PHI | 132.1 | 117 |
| De'Zhaun Stribling | WR | SF | 138.9 | 145 |
| **KC Concepcion** | WR | CLE | 146.9 | 122 |
| Mike Washington Jr. | RB | LV | 163.9 | 211 |
| Kenyon Sadiq | TE | NYJ | 164.7 | 97 |
| Jonah Coleman | RB | DEN | 166.6 | 204 |

**(c) SHIPPED — a grey `R`, and deliberately NOT a third badge.** Doc 105 caps the row at two
*marks*, a caution and an edge, and both were measured. A rookie is not a judgment, so it renders
grey and borderless beside the name, reading as part of it. `mark_rookies.py` writes the flag into
`player_context.csv` under the same guard as `depth_map.py` (refuses if any other column or the row
count changes; archives; re-pins). **It moves no number, no VBD, no rank.** Same standing as the
`12g` badge (§4.22) and the backfield label (§4.20): surfaced, never scored.

**(d) AND THE HONEST HALF, because "promoted" could mean two things.** Marking them is a fact.
*Ranking* them higher would be inventing a ceiling metric, and **§4.13d says four separate
measurements show this project has none and the analyst panel cannot stand in for one.** Worse,
§4.13b measured the thing Matt is trying to avoid and found it points the other way: in ADP
121–180 the "beats his price" rate is 17%, but the **"finished at or above replacement — was he
startable at all" rate is 20.5%. Four of five never become useful.** A late dart is not the
alternative to a single-digit player; it usually *is* one. What makes it costless is not upside —
it is that **the board's margin at 104/113/128/137 is 0.31 / 0.28 / 0.06 / 0.06**, so nothing
measurable is given up by breaking those ties however he likes. §6 already says exactly that: from
round 9, break near-ties toward the wider bet. Before round 9, never.

**(e) KC CONCEPCION, MEASURED.** WR, CLE, bye 11 · proj 125.1 · **VBD −38.4, board rank 122** ·
adp 146.9, eff_pick 134.9. Carries a **BUY**: both residualised analyst panels ahead of ADP
(residual +5.9, 6 of 6 ahead, 2 calling him a target — Kev Mahserejian, Sean Koerner). Injury sheet
NEUTRAL, shoulder sprain cleared 2026-08-03.

**Is the buzz moving the market? Barely.** ESPN ADP across five pulls:
**150.3 → 146.6 → 145.0 → 145.4 → 146.9**, with rostered% 62.4 → 65.9. He firmed about three picks
in two weeks and then drifted back. That is a mild firming, not a surge. `[SOURCED: five 2026
pulls]` — and §4.22(b) is the relevant finding: when the market and the projection disagree, the
**market** has been the one that is right, so if real buzz arrives it will show up as ADP movement
and `refresh_adp.py` on Sept 5 is what captures it.

**Is Matt right that he will not last to 113? Broadly yes.** Simulated across 12 rooms, still on
the board when Matt arrives: **pick 104 → 9 of 12 · pick 113 → 7 of 12 · pick 128 → 4 of 12 ·
pick 137 → 4 of 12.** §4.15 says these run **optimistic**, so read them as ceilings.
**Pick 104 is the turn where he is reliably there; 113 is a coin flip; by 128 he is usually gone.**
Note this collides with §4.18's draft-night rule, which says take a Goff-tier QB2 at 104 or 113 —
that conflict is Matt's to resolve, not the board's.

---

## 4. RED TEAM OF THIS CHANGE

- **Full sweep re-run on the patched file**: board shape `[(12, 3)]` at all twelve picks; strip
  height 33px / board top 199px unchanged across five states and four viewport widths; all six
  starter-strip branches still fire at the right turn; `goes first` counts unchanged (0 at picks
  8/17/32, 4 at 65 and 80, 3 at 113). **The rookie mark changed nothing else.**
- **Rendered and screenshotted, not read**: the `R` appears on Kenyon Sadiq at pick 128, before the
  DISC badge, grey and bordered — an attribute, not a judgment.
- **The conflation check is the guard that matters** and it was run before writing: Brooks, Lloyd
  and Dell all have `g25 = -1` and all three are correctly **not** marked.
- `mark_rookies.py` **asserts** that both prior-season pulls exist rather than silently treating a
  missing file as "everyone is a rookie" — the fail-open pattern doc 151 found in the news loop.
