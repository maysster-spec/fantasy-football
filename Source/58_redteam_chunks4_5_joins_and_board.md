# 58 — RED TEAM CHUNKS 4 AND 5: IDENTITY/JOINS (J1–J6) AND BOARD ASSEMBLY (B1–B6)
**Aug 27, 2026.** Two independent adversarial agents on a shared evidence package, then
adjudication and direct measurement here. **Both agents independently found the same defect: the
live draft tool would never have fired on draft night.** Eight confirmed defects, all fixed.

---

## THE ANSWER, IN ONE LINE

**ESPN carries this league's 12 keepers inside `draftDetail.picks` at overall 169–180 — verified
on the real 2024 and 2025 drafts — and the poller counted them as picks.** `pick_no` read 20 when
the true pick was 8, `on_clock` never matched, and the board would have sat on "WAITING" for the
entire draft.

---

## RECONCILIATION — ALL TWELVE ROWS CARRY EXACTLY ONE VERDICT

### Chunk 4 — identity and joins

| id | constraint | verdict | evidence |
|---|---|---|---|
| J1 | joins key on `espn_id`, never a name | **CONFIRMED DEFECT** | `code_live_engine.py` merged the board to the prerank `on='player'`. `espn_id` existed on the DataFrame that wrote both files and was dropped from the export. **55 of 544 names (10%) carry a suffix, period, apostrophe or hyphen**, 17 inside the top 100 |
| J2 | every join asserts and fails loudly | **CONFIRMED DEFECT** | 2 of 5 joins had an assert. The two on the live path had none, and used `how='left'`. `live_draft.py` printed an unmapped-id count **only in `--replay` mode** |
| J3 | the keeper join asserts | **CONFIRMED DEFECT (partial)** | The assert exists and 12/12 match today, but it tests the *missing-name set*, never the *row count*. Injecting a duplicate spine row gave `is_keeper.sum() = 13` and the assert still passed — a real player silently removed from the pool |
| J4 | D/ST naming handled | **CLEAN** | 32 D/ST in every file, 0 unmatched through every join |
| J5 | alias table covers suffixes and initials | **CONFIRMED DEFECT** | 8 entries, **one inverted** (`'DJ Moore'→'D.J. Moore'` rewrote a valid spine name into one that does not exist), and **38 real suffix variants uncovered** — including Deebo Samuel, Aaron Jones and Kyle Pitts |
| J6 | no duplicate `espn_id` survives a merge | **CONFIRMED DEFECT** | No file holds a duplicate today, but `Engine.__init__` had no row-count check. Injecting one duplicate gave 481 rows against 480 `by_eid` keys — one row unreachable by id and permanently "available" |

### Chunk 5 — board assembly

| id | constraint | verdict | evidence |
|---|---|---|---|
| B1 | 12 keepers removed before pick 1 | **CLEAN** | All 12 absent from the 480-row board by identity; keepers ∩ prerank = ∅ |
| B2 | `eff_pick` = adp − keepers ahead | **CONFIRMED DEFECT** | The formula is right; the inputs were two different vintages. Pool ADP came from the 08-23 pull, keeper ADP from the older `predicted_keepers_v5.csv`. **Rhamondre Stevenson 98.56 vs 86.11.** 22 of 480 rows carried a wrong `gone_ahead`, max error 2 picks |
| B3 | synthetic rows never ranked | **CLEAN (incidentally)** | 26 synthetic in the spine, **0** on the board — but the gate is `vbd.notna()`, not the `synthetic` flag. Containment is a side effect |
| B4 | injury flags surfaced, never scored | **CLEAN** | `proj − vbd` yields exactly one value per position → no injury term in any score. 93 flags on the board, 0 flagged-but-blank, all 14 top-60 flags surfaced |
| B5 | week-14 Pickens clashes flagged | **CLEAN** | 31 bye-14 rows, **31/31** marked, 0 false positives |
| B6 | ordering deterministic | **CONFIRMED DEFECT** | `sort_values('vbd')` used pandas' default **unstable quicksort** with no secondary key. **6 exact tie groups, 37 rows, 4 inside the top 100.** A spine rebuild can permute them with no code change |

**Coverage: 12 of 12. No holes.**

---

## THE ONE THAT WOULD HAVE COST THE DRAFT

`live_draft.py` parsed ESPN's `keeper` flag at line 43 and **never used it**. `pick_no` was
`len(picks)+1` over every row ESPN returned.

**Verified against the real draft history:**

| season | keeper rows | round | overall picks |
|---|---|---|---|
| 2024 | 12 | 15 | **169–180** |
| 2025 | 12 | 15 | **169–180** |

`2026_League_Settings.txt` confirms the same setting is in force: *Keeper Designated Round: End of
Draft*, lock one hour before the draft. If ESPN pre-populates those twelve rows when the draft
opens — which is what a T-60min lock implies — then `len(picks)` is 12 before pick 1.

**Reproduced end to end:** feeding the real `step()` twelve keeper rows at 169–180 plus seven real
picks, the pre-fix code rendered *"WAITING — pick 20"*. Post-fix it renders **"ON THE CLOCK —
PICK 8"**.

```python
real = [p for p in picks if not p.get('keeper')]
ids  = [p['pid'] for p in picks]      # keepers still mark players TAKEN
pick_no = len(real) + 1               # they just do not advance the clock
```

The distinction matters both ways: keepers must come **off the board** (they are unavailable) but
must **not advance the clock**. The fix does both, and is correct whether or not ESPN
pre-populates — so it needs no live verification to be safe. The poller now also prints the keeper
row count on every poll, so the assumption is visible on draft night rather than assumed.

---

## THE ONE MATT WOULD HAVE SEEN AND NOT TRUSTED

The engine held one long-lived RNG, mutated by `survival`, `recommend`, `rollout_scores` and
`cliffs`. `live_draft.py` builds one `Engine` and calls it on every poll — so **the same board
state returned different recommendations on successive polls.** Measured, identical state, ten
calls at the off-clock setting:

- pick 32: Judkins ×5, **Davante Adams ×4, Joe Burrow ×1**
- pick 41: D'Andre Swift ×8, **Tee Higgins ×2**

The Monte Carlo standard deviation was ~3.4 points against a 6.0-point spread across the whole top
six — the ranking was inside its own noise. Worst at the off-clock setting, which is the board he
stares at for 59 of every 60 seconds and forms his plan from.

**Fixed:** the RNG is now reseeded per call from the board state itself
(`pick_no`, players taken, roster size). Verified: six identical calls, one answer.

---

## THE SILENT-FAILURE CLASS — J1/J2/J6, AND THE TEST THAT PROVED IT

The agent constructed the failure rather than describing it: **one trailing space** appended to
`Jahmyr Gibbs` on the board — the single most common real-source mutation.

```
Engine constructed. NO exception, NO warning.
Gibbs taken at pick 1.
Engine at pick 8:  #1 'Jahmyr Gibbs '  RB  vbd=162.3  p_next=0.00
>>> #1 recommendation was drafted at pick 1: True
```

The hero panel would have rendered *ON THE CLOCK — PICK 8 / Jahmyr Gibbs* with the timer running,
on a player gone seven picks earlier. `p_next = 0.00` was the only tell, and it reads as "he will
not last," not "he is gone." A curly apostrophe on Ja'Marr Chase produced the same result.

**Fixed three ways:**
1. `board_v8_fixed.csv` now carries `espn_id` directly — **the name join is gone from the live path.**
2. Where a board without ids is loaded, the fallback join now asserts row count, no nulls, and uniqueness.
3. Re-ran the adversarial test: `AssertionError: 1 board rows have NO ESPN_ID and would stay 'available' for the whole draft: ['Jahmyr Gibbs ']`

---

## B2 AND B6 — FIXED AT SOURCE, BOARD REBUILT

**B2.** Keeper ADPs now resolve from the same pull as the pool, with an assert that all 12 resolve.
22 rows change; the largest effect was **Emeka Egbuka `eff_pick` 39.33 → 37.33**, which moves him
inside the pick-41 planning window.

**B6.** `kind='mergesort'` plus an explicit secondary key (`adp_pick`, then `player`). Ordering is
now total and reproducible; 31 of 544 prerank rows moved, max 9 places.

**J5.** `KEEPER_ALIAS` is now **generated from the spine** (45 entries), not hand-maintained. Every
key is verified absent from the spine and every value present, with an assert. This matters at
**7:00 PM on Sept 7**: if Kam, Ray or Fleming names Deebo Samuel, Aaron Jones or Kyle Pitts as
their actual keeper, the old table would have hard-stopped the rebuild sixty minutes before the
draft.

---

## THE `eff_pick` QUESTION, AND WHY I DISAGREE WITH THE AGENT

The board-assembly agent argued the live engine applies keeper depletion **twice** — once
structurally (keepers absent from the board) and again arithmetically (`eff_pick` shifts every ADP
earlier) — and recommended feeding raw `adp_pick` to the opponent model instead.

**That is wrong, and the reason matters.** Doc 53 fitted the noise coefficient
`sd = 0.30 × min(ADP, 70)` **in keeper-depleted space** — the residuals were measured between
`draft_order` (rank of non-keeper picks) and `adp_depleted` (ADP re-ranked over the keeper-free
pool). `eff_pick` is that same depleted coordinate. Feeding raw `adp_pick` would mismatch the
model against its own calibration.

The agent's supporting point is nonetheless correct and worth recording: **the directive's §2.1(c)
table is wrong at pick 32.** Solving the fixed point on the current keeper ADPs gives
**3 keepers ahead, effective ADP 35** — the table says 5 and ~37. Pick 41 (10 keepers, ~51) is
exact. So the 32→41 window carries about **6 picks of extra depth, not the 9 the table implies.**

---

## EXTRAS WORTH ACTING ON

**The board's deep ordering is largely fabricated.** `adp_censored = True` on 492 of 700 spine
rows; **323 of 480 board rows (67%) sit in ESPN's 2-pick-wide undrafted sentinel blob**. Only ~157
board rows carry a real ADP, and Matt picks through 161. Every survival number at picks 128, 137,
152 and 161 rests on an ordering ESPN did not actually supply. The `adp_censored` flag exists on
the spine and is read by neither the builder nor the engine. **Not fixed — it needs a real deep-ADP
source, not a code change.**

**The K/D-ST board fails to an empty DataFrame.** `except Exception: pd.DataFrame(...)` around the
load, with the path derived by string substitution on the board filename. With the file absent,
picks 152 and 161 render an empty table and `best = '—'`, silently.

**`predicted_keepers_v5.csv` has no id column**, so the keeper join is a name join by necessity —
the generated alias table is a mitigation, not a fix. The spine carries `gsis_id`, `sleeper_id`,
`pfr_id` and a `name|pos|team` composite key `k2`, none of which is used anywhere.

**REFUTED — the "board is on stale ADP" claim.** Checked directly: `board_v7_2026.csv` matches the
Aug 23 capture on 480/480 rows, injury flags included.

---

## WHAT THIS CHANGES

1. **Re-inject the prerank file** — it changed again (31 rows moved, max 9 places).
2. **Use `board_v8_fixed.csv`** — it carries `espn_id`, correct `eff_pick`, and a stable order.
3. **Correct directive §2.1(c) for pick 32:** 3 keepers ahead, effective ADP ~35, not 5 and ~37.
4. **On draft night, check the first poll line.** It now prints how many keeper rows ESPN returned.
   If it says 12, the fix just saved the session; if it says 0, no harm done.
5. **Do not trust any survival number past about pick 120** until a real deep-ADP source exists.

## LIMITS

1. The keeper-pick behaviour is verified from the 2024/2025 draft *history*, not from a live 2026
   `mDraftDetail` response. The fix is safe under both behaviours, but the trigger is unconfirmed —
   **the `--replay 2025` dry run would confirm it in thirty seconds.**
2. Both agents shared one evidence package; a defect needing an unstaged file is invisible to both.
3. `code_rebuild_spine_v5.py` is still not in the audited set, so B3's synthetic gate and the
   spine's own `vbd` for K/D-ST remain unverified at source.

## §7 CLOSE-OUT

**Top 3 assumptions:**
1. **ESPN returns keeper rows in `draftDetail.picks` during the draft.** *Invalidated by:* the
   replay printing 0 keeper rows. The fix is a no-op in that case.
2. **`eff_pick` is the right coordinate for the opponent model.** *Rests on* doc 53 having been
   fitted in depleted space, which it was. Invalidated if the residual fit were re-run in raw ADP
   space and gave a materially different coefficient.
3. **Name-keyed joins are now all guarded.** *Invalidated by:* any consumer reading the board that
   was not in this audit set.

**What would most improve this:** a **real ADP source below pick 120**. Two thirds of the board is
ordered by a sentinel, and no amount of code correctness fixes that.
