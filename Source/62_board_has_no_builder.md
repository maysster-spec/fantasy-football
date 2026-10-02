# 62 — THE SHIPPED BOARD HAS NO BUILDER

**Aug 28, 2026.** Found while checking whether the Sep 5 re-pull reaches the board.
**Status: CONFIRMED DEFECT. Severity NOT measured — see §4. Do not quote a magnitude.**

---

## 1. THE FINDING

**No script anywhere produces `board_v8_fixed.csv` — the board the live engine actually loads.**

Grepped every `.py` in `2026\Source\` (17 files, staged and searched, not sampled) plus the five
kit files and the three local scripts. Result:

| what | result |
|---|---|
| scripts writing `board_v8_fixed.csv` | **zero** |
| scripts *reading* `board_v8_fixed.csv` | 3 — `code_live_engine.py`, `live_draft.py`, `code_integrity.py` |
| every `to_csv` board target found in Source | **`board_v7_2026.csv`** — and nothing else |

`board_v8_fixed.csv` (41,127 bytes) was produced by ad-hoc code during the Aug 27 red team
(doc 58) and **never saved as a script.** It is a 480-row artifact with no builder.

## 2. THE BUILDER THAT DOES EXIST IS ALSO STALE-WIRED

`code_build_board_v7.py` — the file the handover calls "the board builder" — line 30:

```python
e = pd.read_csv(SRC + 'espn_projections_2026_20260823.csv')
```

Hardcoded to the **Aug 23** projection. The patched pull script now writes
`espn_projections_2026_YYYYMMDD_HHMM.csv`. Same defect class as doc 61's D5, one layer further
down the chain, and it means the Sep 5 re-pull does not reach the board by *either* path.

Line 79 writes `board_v7_2026.csv` — the file trashed Aug 28 as a trap. Re-running the documented
builder **recreates the trap** and does not produce the board the engine needs.

## 3. WHAT THIS DOES TO THE RUNBOOK

Directive §8 says: *"Sep 7, 7:00 PM: keeper lock — swap predicted for actual, **rebuild the
board**, re-inject the prerank file, restart the live tool."*

**There is no rebuild path.** Running `code_build_board_v7.py` yields a differently-named board
built on Aug-23 projections. `live_draft.py` then hard-exits (it asserts `board_v8_fixed.csv`
exists) — so this fails **loud, not silent**, which is the one piece of good news.

## 4. SEVERITY — NOT MEASURED, AND DO NOT GUESS

Unknown and untested:
- The point cost of drafting off an Aug-23-based board versus a Sep-5 one. Two weeks of
  projection drift. **Plausibly small. Nobody has measured it. Do not assert a number.**
- Whether doc 58 contains the v8 fix code inline and recoverable.

**The reconstruct-vs-freeze decision must not be made on an unpriced assumption.** Measure the
Aug-23 board against a Sep-5 board on the objective before deciding a rebuild is worth the risk.

## 5. THE TWO OPTIONS

**A — FREEZE (lower risk).** Do not rebuild. Draft off the verified 41,127-byte board. Handle
Sep 5 news manually as overrides at the pick. Costs whatever two weeks of projection drift is
worth — unmeasured. Requires no new code nine days out.

**B — RECONSTRUCT.** Recover the v8 fix from doc 58, write `code_build_board_v8.py`, verify it
reproduces the existing 41,127-byte board **byte for byte from the Aug-23 inputs** before pointing
it at Sep-5 inputs. That byte-for-byte reproduction is the whole test; without it the new script
is an unverified builder, not a recovery.

**Do B only if it reproduces exactly. If it does not, take A.** A rushed board rebuild is the
larger risk, and the objective difference is unmeasured in both directions.

## 6. HOW IT WAS MISSED

Chunk 8 audited the spine builder. Chunks 4–5 audited the board's *contents*. **Nothing asked
whether the shipped board could be regenerated at all.** This is the same gap doc 59 named —
"nothing compares an artifact to its builder" — one step further: here there is no builder to
compare against. `check_kit.py` (doc 61) verifies the kit's *bytes*, which is correct and useful,
and would not catch this: the board is present and its hash is right. It just cannot be remade.
