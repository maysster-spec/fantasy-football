# 164 — Three defects in the 7:00 PM path, and one keeper the board has wrong today

**2026-09-04.** Matt ran `py fetch_keepers.py --dry` and pasted the output. It printed **PASS**.
Reading what it actually returned, rather than its verdict, turned up one live board error and
three defects in the keeper-lock sequence. All three were reproduced before being fixed.

---

## 0. THE FACT THAT STARTED IT: one predicted keeper is wrong, and it is not a skill player

ESPN's `teams[].draftStrategy.keeperPlayerIds` (doc 90's "right door") now holds **7 of 12**
selections. Against `predicted_keepers_v5.csv`:

| team | predicted | ACTUAL | |
|---|---|---|---|
| ChatCTE (Cary) | Rashee Rice | Rashee Rice | ok |
| MATT (JUG) | George Pickens | George Pickens | ok |
| Multiple Scorgasms (Taylor) | Chris Olave | Chris Olave | ok |
| Breece up those Tets (Lobsinger) | Tetairoa McMillan | Tetairoa McMillan | ok |
| Jaxson Bates (Grenier) | Cam Skattebo | Cam Skattebo | ok |
| Send'em Packin (Snyder) | Travis Etienne | Travis Etienne Jr. | ok |
| **Window is Always Open (Brown/Collins)** | **Stefon Diggs** | **Brandon Aubrey (K)** | **MISS** |

**6 of 7 correct.** The miss is the case §4.9 explicitly excludes — *"Exclude K and D/ST from
keeper prediction entirely"* — so the model was not wrong so much as blind by instruction, and
doc 90 already anticipated it. Two consequences, both verified against the shipped files:

- **Stefon Diggs is NOT a keeper and is missing from `board_v8_fixed.csv` right now.** He returns
  at rank 118, `adp_pick` 101.6, `eff_pick` 90.6, vbd −35.1. Below replacement, so he does not
  change a pick — but "a wrongly-removed player is invisible all night" is doc 82's own warning,
  and this is that, four days out.
- **A kicker keeper does not deplete the skill pool**, so §2.1(c) moves. Re-solved as the same
  fixed point on the current freeze (PROVISIONAL — five teams have not chosen):

| pick | v7.1 keepers ahead | with the current set | eff ADP v7.1 → now |
|---|---|---|---|
| 8 · 17 · 32 · 41 · 56 · 65 · 80 · 89 | 0 0 4 10 10 10 11 11 | unchanged | unchanged |
| **104 · 113 · 128 · 137 · 152 · 161** | **12** | **11** | 116→115 · 125→124 · 140→139 · 149→148 · 164→163 · 173→172 |

Diggs at 101.6 was the deepest of the twelve, so only the rows behind him move. **Do not edit the
directive yet** — the table is a function of all twelve, and five are still open.

---

## 1. `keeper_swap.py` WAS READING AN 11-DAY-OLD MARKET, AND `draft_night.bat` NEVER RESTORES IT

The worst of the three. `keeper_swap.py` hardcoded
`ADP23 = espn_projections_2026_20260823.csv` for **both** the projection column and the market
column. But `refresh_adp.py` (doc 109) re-froze the market on 08-30 and again on **09-03**, and
`Scripts\live_draft\adp_vintage.txt` says so: `espn_projections_2026_20260903_0902.csv`.

**Measured against the shipped board: 426 of 480 rows differ.** Median 0.1 picks, but inside the
drafted range the movers are large — **Kittle 73.72 → 97.54 (24 slots), Godwin 121.69 → 144.77
(23), Herbert 85.83 → 107.39 (22), Aaron Jones 113.68 → 133.74 (20), Pollard 87.90 → 107.73 (20),
Hockenson 152.34 → 133.01 (−19).**

`adp_pick` drives `eff_pick`, which drives every survival number on the live board and §2.1(c).
`draft_night.bat` runs `keeper_swap.py --write` at step 4 and **never runs `refresh_adp.py`**, so
the 09-03 freeze would have been rolled back at 7:00 PM and never restored. The script even
printed the alarm — `eff_pick changed on 426 of 480 shared rows` — but that line reads as a
statistic, not a failure, and its own docstring still claimed *"run with the predicted keepers it
reproduces the shipped board exactly."* True on Aug 30; false since Sept 3; never re-checked.

**FIX — and the two pulls had to be separated, not swapped.** doc 101 is explicit that the
projection side must stay on 08-23 or `board_audit.py` fails at 7:05 PM on draft night. So:
- **projections / replacement**: still `ADP23`, untouched.
- **market (`adp_pick`)**: read `adp_vintage.txt`, coalesced the way `refresh_adp.py` composed it
  (`new.espn_adp` where present, else the 08-23 value — the newer pull is smaller). Falls back to
  08-23 with a printed warning if the stamp is missing or names a file that is not there.

**FALSIFIER, fixed before running: does `--check` with the PREDICTED twelve reproduce the shipped
board?** Before: 426 of 480 `eff_pick` rows differ. After: **15**, all of them ±0.01–0.03 on
players at ADP ≈ 170 — inside §4.14's undrafted sentinel, ranks 242–476, where the ordering is
fabricated anyway. Nothing inside pick 161 moves at all. Independent confirmation: the rebuilt
keeper ADP vector is `[28.2, 29.4, 29.4, 32.9, 41.0, 42.2, 42.4, 44.2, 45.1, 47.3, 78.7, 101.6]`
— **exactly the list v7.1 published**, which was solved separately on the 09-03 freeze.

---

## 2. A KEPT KICKER STAYS ON THE STREAMER SHEET AND WOULD BE OFFERED AT PICK 161

`keeper_swap.py` already recognised a K/D-ST keeper (doc 90) and said *"nothing to remove; he was
never on `board_v8_fixed.csv`."* True, and incomplete: **he is on `board_v7_kdst_separate.csv`,
and nothing removes him from it.**

`Engine.streamers()` filters only against players already in the live pick feed — and this
league's keepers do not enter that feed until overall **169–180** (§2.1 b2), *after* picks 152 and
161. So at pick 161 the board would have named **Brandon Aubrey, the top kicker on the sheet by 10
projected points**, and Matt would have learned otherwise from ESPN rejecting the pick with the
clock running.

**Cost is not points — §4.8 says draft-day K value is an illusion — it is a wasted turn at 60
seconds.** State it that way; do not inflate it.

**FIX:** `prune_streamers()` in `keeper_swap.py`. It runs only when a non-skill keeper exists
(so the common path is byte-unchanged), names the player and the pick he would have polluted,
archives the sheet before writing, and **refuses** if pruning would drop either position below the
12 rows `code_live_engine` asserts. Executed end to end: sheet 64 → 63 rows, K 32 → 31, Aubrey
gone, **Cameron Dicker is now the top kicker**, and the same run re-added Diggs to the board
(481 rows) and archived both files first.

---

## 3. `fetch_keepers.py` THREW AWAY THE RIGHT ANSWER FOR A BIGGER WRONG ONE

This is the defect that produced the output Matt pasted, and the one most likely to hurt on the
night. Traced through the shipped code:

1. `from_keeper_ids()` returned **7 real keepers with names** → `how = 'mTeam/keeperPlayerIds (INCOMPLETE)'`.
2. The fallback loop breaks only on `len(rows) == 12`, so it ran on. `mRoster` returned **194
   last-season roster rows**, and `if len(got) > len(rows)` was **true** — `rows` and `how` were
   overwritten with the roster dump.
3. The correct message, *"ONLY 7 OF 12 TEAMS HAVE SELECTED A KEEPER — nothing is broken"*, is
   gated on `how.startswith('mTeam/keeperPlayerIds')`. It could no longer fire.
4. So it printed the roster-dump message instead: *"if it still shows full rosters THEN, the
   automatic path is dead: type the 12 names into actual_keepers.csv by hand."*

**At 7:00 PM with eleven of twelve chosen — doc 90's own scenario, a manager who misses the
deadline — that is the worst advice the tool could give: hand-typing under time pressure while it
is holding eleven of the names.** A bigger pile of rows is not a better answer.

**FIX:** only an exact 12 may displace the right door; a fallback that returns anything else is
reported and ignored. **Reproduced first, with stubbed ESPN responses, and the fix verified across
four scenarios:**

| scenario | expected | |
|---|---|---|
| A keeperPlayerIds returns all 12 | writes from `mTeam/keeperPlayerIds` | PASS |
| B right door dead, `mRoster` holds a real 12 | falls back to `mRoster` | PASS |
| C right door dead, `mRoster` holds 192 roster rows | `NOT LOCKED YET` | PASS |
| **D right door partial (7), `mRoster` 192** | **`ONLY 7 OF 12 TEAMS HAVE SELECTED`** | **PASS** (was FAIL) |

Scenario D is the one that was broken. C proves the roster-dump message still fires where it is
correct.

---

## Pins

| file | bytes (LF-normalised) | sha256[:16] |
|---|---|---|
| `keeper_swap.py` | 16073 | `823617362e3acff4` |
| `fetch_keepers.py` | 15797 | `d71f5bb38cb8553a` |

Both re-staged off Matt's machine after committing and re-verified against `check_kit.py`'s
MANIFEST: **PINS MATCH**. Superseded copies in `_archive\` as `*_20260904.py`, hashes confirmed
equal to the old pins.

## What is still open

1. **Five teams have not chosen a keeper.** Re-run `py fetch_keepers.py --dry` any day this
   weekend; it is a live view and needs no lock. When all twelve are in, §2.1(c) gets re-solved
   for real and the directive updated.
2. **`refresh_adp.py` is still absent from `draft_night.bat`.** With fix 1 in place it is no
   longer *needed* there — `keeper_swap` now writes the correct market itself — but the Sept-5
   refresh will stamp a new vintage, and the stamp is what `keeper_swap` now reads. Nothing to do;
   recorded so nobody re-adds it as a duplicate step (§0.2's folder-listing rule, applied to
   sequences).
3. The `--replay` slot banner from doc 163 (prints draft-night advice during a dry run).
