# 73 — INJURY HANDLING AND KEEPER SWAP, IN PLAIN TERMS

**Aug 29, 2026.** Answers `NEXT_PROMPT_injury_handling.txt` and Matt's keeper questions.
Everything below was measured or read out of the code today. Nothing is eyeballed.

---

## PART A — INJURY

### A1. The flag is DISPLAY-ONLY. [TESTED — code read]

`code_live_engine.py:101` loads `flag` into `self.flag` and `:232` passes it into the output row.
`live_draft.py:98` wraps it in a red span. **That is every use.** It never enters `vbd`, the
rollout, the ranking, or any decision. It is a sticker on the screen.

It is also **frozen** as of whatever pull built `board_v8_fixed.csv`. The live tool never
re-checks injury status during the draft. ESPN's own draft room shows live tags; the tool does not.

> **[SUPERSEDED Aug 29 by doc 74 — READ THAT FIRST.]** The measurement in A2 stands, but its
> interpretation does not. The `QUESTIONABLE` tag is **not an injury designation**: 33 of the 36
> flagged players in the top 180 carry `injured = False` in ESPN's own data. A2/A3 below read the
> residual as an injury discount; that reading is retracted. A1 and A4 are unaffected.

### A2. `proj_2026` does NOT price injury risk. [TESTED, n=480 — INTERPRETATION RETRACTED, see 74]

The direct question was whether ESPN's projection already discounts injured players. It does not —
and the evidence runs the other way. Fitting projection against log(ADP) within each position and
comparing residuals (positive = projects **above** what its draft cost implies):

| pos | n | flagged | resid, flagged | resid, clean | difference |
|---|---|---|---|---|---|
| RB | 112 | 27 | +5.04 | −1.60 | **+6.64** |
| TE | 106 | 12 | +7.48 | −0.95 | **+8.43** |
| WR | 193 | 33 | +19.96 | −4.12 | **+24.08** |
| QB | 69 | 8 | −37.92 | +4.97 | −42.89 *(n=8, ignore)* |

**Read it this way: the MARKET discounts flagged players. ESPN's projection does not.** A flagged
WR is drafted meaningfully later than his projection justifies, because human drafters are pricing
risk that the projection ignores.

### A3. THE CONSEQUENCE, and it is the only thing here that touches a pick

`vbd` is built from `proj_2026`. If the projection carries no injury discount, **neither does the
board** — so the board systematically rates flagged players above the market's view of them.
When the engine surfaces a flagged player with a large edge, some unknown part of that edge is
the market's injury discount rather than value the market has missed.

**MAGNITUDE NOT MEASURED.** The table above is a residual in projection-versus-ADP space, not a
dollar cost, and per §0.2 it does not get one until a paired experiment produces it. **Do not
quote +24 as a WR penalty.** Whether the market or ESPN is right is exactly the open question,
and one board cannot settle it.

### A4. Whether the flag predicts anything is NOT TESTABLE with data on hand. [NO SOURCE]

`injuryStatus` behaves like a current player attribute, not a season stat. The 2024-season pull
(taken Aug 2026) agrees with the 2026-season pull on **74.8%** of players and shows a nearly
identical QUESTIONABLE share — consistent with both carrying *today's* status four days apart, not
with the 2024 file preserving 2024 preseason status. Same contamination mechanism as §1.1's ADP.
**A historical backtest of flag informativeness cannot be run.** Do not attempt one.

### A5. THE PROCEDURE — unchanged, with one addition

"Ignore the flag, treat a known injury as a manual override at the pick" was already right, and
A1 explains why: the flag isn't in the math, so there is nothing to turn off. **One addition:**
when the engine recommends a flagged player, remember the board has not discounted him at all.
The market has. That is the moment for judgment, not arithmetic.

Matt's own three cases are the right frame, and no single word can separate them:
  1. misses two weeks, then fine — costs ~2/14 of the projection, roughly nothing at draft cost.
  2. misses one week, hobbled all year — the expensive one, and invisible to any flag.
  3. the McCaffrey pattern — repeat soft-tissue history, healthy today, tagged QUESTIONABLE at
     rank 3. The tag tells you nothing you didn't already know; the history does.

**Handcuffs are the lever the flag isn't.** If a flagged RB is taken inside the first four rounds,
his backup is worth a round-9-or-later dart under §4.13's rule. That is a real hedge with a known
cost, unlike a discount nobody has priced.

---

## PART B — KEEPERS

### B1. What is true right now [VERIFIED]

- `board_v8_fixed.csv` holds 480 rows and **0 of the 12 predicted keepers**. They were removed
  before the board was built. They can never be recommended, which is correct — they are not
  draftable.
- `live_draft.py` marks **everyone** in ESPN's feed as taken, keeper rows included
  (`ids = [p['pid'] for p in picks]`). Keepers are excluded only from the pick *clock*, never
  from availability.

### B2. THE TWO SCENARIOS, answered

**Scenario 1 — a team keeps someone we did NOT predict.**
Two players are affected, and only one is handled automatically.
  - The player they actually kept: he IS on the board, and ESPN's live feed marks him taken the
    moment the tool polls. **Handled. No action.**
  - The player we wrongly predicted: he is genuinely draftable, but he is **not on the board at
    all** — so the engine cannot see him, cannot rank him, and will never recommend him, all night.
    **This is the hole.** It is not a display problem; a real asset becomes invisible.

**Scenario 2 — a team keeps exactly who we predicted.** Nothing to do. He was never on the board.

### B3. THE FIX, and what Matt actually does at 7:00 PM

`keeper_swap.py` (in `...\2026\Scripts\`) rebuilds the board from the 12 actual keepers: it
re-adds any freed player with correct `vbd` and re-ranks. It was validated to reproduce the
shipped 480-row board exactly from the 12 predictions — which also means **doc 62 is closed: the
board has a builder again.**

**The file you edit is `G:\My Drive\_Fantasy\2026\Scripts\actual_keepers.csv`.**
Plain CSV, two columns, already pre-filled with the 12 predictions:

```
Team,Player
ChatCTE (Cary),Rashee Rice
** MATT (JUG) **,George Pickens
...
```

Change only the Player cell on any row that guessed wrong. Keep all 12 rows. Then:

```
py keeper_swap.py --check     # shows the diff; says IDENTICAL if all 12 were right
py keeper_swap.py --write     # only if --check showed changes; archives the old board
```
then restart the live tool. If `--check` says IDENTICAL, **skip the write entirely.**

### B4. What can still go wrong, and what to do

- **A name you type doesn't match.** The script refuses and suggests the correct spelling. Fix the
  spelling; do not force it.
- **You end up with 11 or 13 rows.** The script refuses. Every team keeps exactly one.
- **You run out of time at 7:00.** Skip the swap and draft off the board as-is. The only cost is
  that one or two genuinely available players stay invisible — annoying, not fatal, and the
  FALLBACK_BOARD printout still lists them.
