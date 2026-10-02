# 192 — The tier sheet, and why the composite has three signals and not more

**2026-09-06 (T−1).**

## 1. THE TIER SHEET — new artifact, `make_tiers.py` → `TIER_SHEET.pdf`

Matt: *"a new draft grid that shows our rankings like we have them on the board… turning the draft
board into a grid may help more with the tiering making sense because ADP won't be in order of the
tiering."*

**Correct, and neither shipped artifact answers the question he is describing.**

| artifact | what it is | why it fails the tier question |
|---|---|---|
| `DRAFT_BOARD.pdf` | our ranking, 180 rows, 7 pages | tier lines are there (doc 134) but RB tier 3 and WR tier 3 are forty rows apart |
| `ADP_GRID.pdf` | 12-wide snake in **pick** order | a positional tier is scattered across it **by construction** — the market does not sort by our value |

**`TIER_SHEET.pdf`:** one column per position, one row per tier, best first inside each cell.
Every player carries **VOR** and **`~n`, the pick he is expected to go at**. That second number is
the point: *how many names in this tier have a `~n` below my next pick* is a count instead of a
search.

**Design decisions, and why:**
- **`add_tiers` is IMPORTED from `make_board.py`, not reimplemented.** One derivation, two
  consumers — the rule doc 146 established for `to_pdf.render`. A second copy of the gap logic is
  the two-names-for-one-job defect (§0.2).
- **New file, touches nothing that already prints.** Docs 157 and 158 were both render edits to
  shipping artifacts; this deliberately is not one.
- Wired in as **step 11 of 12** in `sept5_after.bat` (after the board exists, before the desk sync)
  and added to `sync_desk_copies.py`.

**Verified before commit** — rendered locally, then the §0.5(c)5 missing-row check by name against
the decisions each row serves: pick-8 names, all six of the §7 pick-32 tie, Stafford and Odunze for
56, the QB2 candidates for 104/113, and every name that moved this session. **143 players, 10 tiers,
all present.**

**And the output validates the tiers:** TIER 1 is **QB Allen alone · TE Bowers + McBride · RB Gibbs
alone · WR Nacua alone** — §4.15's 47-point QB cliff and §4.3's two-TE premium, visible in one look.

## 2. THE COMPOSITE BADGE (doc 191) IS NOW ON THE BOARD

`marks()` in `make_board.py` draws **`3/3`** (green) and **`1/3` / `0/3`** (brown). **Nothing at
2/3** — that rung measures −0.4, and a badge there would be noise. It parses the stamp already
sitting in `player_context.csv`'s `why` field, so **no new column and no schema change**, which
keeps `depth_map.py`'s write guard out of it. Rendered and cross-checked: the green mark landed on
exactly the seven expected backs and on no 2/3 player.

## 3. WHY THREE SIGNALS — Matt asked, and the answer is that a fourth was tested tonight

**Vacated targets, computed historically for the first time** (share of a team's year-*t* targets
that left the roster before *t+1*; 126 team-seasons, mean 8.7%, sd 7.2%):

| model | R² | vacated-targets term |
|---|---|---|
| vacated targets alone | 0.0043 | **+8.3, p=0.335** |
| the shipped three | 0.0461 | — |
| the three **+ vacated** | 0.0485 | **+6.3, p=0.447** |
| count of 3 | 0.0449 | — |
| count of 4 | 0.0456 | — |

**It does not earn its place.** Adding it moves R² by 0.002 and the four-count is no better than the
three-count. Consistent with §4.21, which measured it team-clustered at **r=+0.125, p=0.50**.

**The full accounting of candidate signals:**

**IN — tested, contributes:** top-quartile target share · played 13+ games · NFL rounds 1–3.

**OUT — tested, contributes nothing:** age (p=0.71) · second-year (p=0.73) · **vacated targets
(p=0.45)** · teammate dependence (p=0.70) · after-contact / YAC / EPA per carry / EPA per target
(all p>0.30) · prior workload (subsumed by target share).

**CANNOT BE TESTED AT ALL — and this is the category I had not named:**
- **the UNSETTLED job flag** — `depth_map.py` computes it from the **2026 source pull only**. There
  is no historical version, so it cannot enter a backtest. It stays a §4.20 flag, not a signal.
- **the analyst BUY flag** — same problem; it is a 2026 sweep artifact.
- **red-zone role (§4.5)** — ours, and the *strongest* candidate left: inside-10 targets persist at
  **r=+0.59**, and it is what surfaced Sutton and Warren. It has never been given a payoff test
  because that needs **multi-season red-zone data**, i.e. nflverse play-by-play, which is a build
  and not a lookup. **This is the top post-draft item.**

**So: three because six others were measured and added nothing, and three more have no historical
version to measure against.** Not because three was the number I stopped at.
