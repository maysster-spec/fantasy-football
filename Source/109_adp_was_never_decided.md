# 109 — ADP freshness was decided by accident, and the accident was the wrong way round

**Date:** 2026-08-31 · **Matt:** *"Should ADP be re-frozen on Sept 5? I thought we discussed."*

**We discussed a different question.** What was settled (directive §8, doc 79) is that
**FantasyPros** ADP is not a runtime input. Nobody ever decided whether **ESPN's own `espn_adp`**
should be re-pulled. It has been riding along as a side effect, and the side effect is backwards.

## THE MEASUREMENT — Aug 23 pull vs Aug 30 pull, board top 161

| | changed | median move | max |
|---|---|---|---|
| **projections** (`proj_2026`) | **47 of 161** | — | 46.5 pts |
| **ADP** (`espn_adp`) | **160 of 161** | **1.43 picks** | **12.77 picks** |

**Only 104 of 161 stayed within 2 slots of their old ADP order.** Against the same 150/161
threshold `sept5_check.py` applies to projections, ADP would be a screaming REBUILD.

`sept5_check.py` reads `proj_2026` and **nothing else** — verified in the source. So the verdict
is entirely about projections, and ADP freshness is coupled to it by accident: FREEZE keeps the
old market, REBUILD happens to bring a new one. **The thing the test watches barely moves. The
thing it ignores moves a lot** — and ADP is what drives `eff_pick`, every survival number, every
"take at 104" on the paper sheets and `p(next)` on the live board.

Movers that change a real decision:

| player | ADP | your pick moves |
|---|---|---|
| George Kittle | 97.5 → 84.8 | 86 → **75** |
| Justin Herbert | 107.4 → 97.4 | 96 → **87** |
| Tony Pollard | 107.7 → 98.7 | 97 → **89** |
| Kenny Gainwell | 119.1 → 110.2 | 108 → **100** |
| **Jonathon Brooks** | 118.7 → 110.6 | 108 → **101** — *he no longer reaches 104* |
| Tyjae Spears | 161.3 → 152.4 | 149 → **141** |

## THE FIX

**`refresh_adp.py`** re-freezes the market from the newest good pull: it rewrites `adp_pick`,
recomputes `gone_ahead` and `eff_pick` against the current keeper list, and **does not touch
projections, VBD or rank** — those belong to the FREEZE/REBUILD decision and are not its business.
It archives the old board, re-pins `check_kit`, and **stamps the vintage** in `adp_vintage.txt`
so `board_audit` checks against the right pull instead of a hard-coded date. A gate that is
guaranteed to fail after a legitimate refresh is a gate you learn to ignore.

It **refuses to run** if it cannot match all twelve keepers by a normalised name key: one missing
keeper shifts `gone_ahead` by 1 for everyone behind him. A raw name match found 11 of 12.

**Applied now, on the Aug-30 pull** — the mock is tonight and every sheet was quoting a
week-old market. `board_audit`: **39 of 39 before and after.** Re-run it on Sept 5.

## AND THE SHEETS NEEDED A BUILDER, AGAIN

`AUDITION_WINDOW`, `LATE_RB_SHEET` and `ANALYST_CALLS` were built by hand in a chat — exactly the
failure `FALLBACK_BOARD` had, where the board could be corrected in seconds and the paper could
not. Every `goes at` on all three just moved. **`make_sheets.py`** rebuilds all three from current
data in one command. That is now four artifacts with builders and none without.

## COLLISIONS FOUND ACROSS THE CORPUS

Scanning 28 documents for numbers that have since been corrected:

- **`02_findings_ledger.md` (69 KB, Aug 19) is the real problem.** It still carries WR30 = 168.5,
  the 15.25 streaming baseline, +8.6 for the rollout and 0.14 for Allen's survival — and it is
  corrected by a **separate file**, `02b_LEDGER_CORRECTIONS_v5.md`. That is precisely the pattern
  the project's own naming rule exists to prevent. Anyone reading the ledger alone is reading four
  retracted numbers. **It needs a header pointing at its corrections; it does not need rewriting.**
- **`DRAFT_DAY_GUIDE.md` said the board's ADP is the frozen 08-23 pull.** True this morning, false
  as of this file. Corrected, and the Sept-5 row now carries the `refresh_adp.py` step.
- `ERROR_PATTERNS_1.md` and the directive quote the old numbers **in order to retract them**. That
  is correct usage and was left alone — a grep cannot tell the difference, which is why this list
  is shorter than the raw hit count.
