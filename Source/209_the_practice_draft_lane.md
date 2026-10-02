# 209 — the practice draft lane, and the fallback that could not work

**2026-09-07, draft day.** Matt asked for the mock-draft commands and sent a screenshot of the
**Practice Draft** button on his league page. Two things were wrong on his drive; both are fixed
and committed.

---

## 1 — THE COMMAND

```powershell
# window 1
cd "G:\My Drive\_Fantasy\2026\Scripts\live_draft"
py bridge_server.py

# window 2 — Chrome: click Practice Draft, leave the room open

# window 3
py live_draft.py --bridge --mock
```

`--bridge --mock` is the pair he half-remembered.

---

## 2 — DOC 126 SAID DON'T, AND THAT IS NOW STALE

`00_HOW_TO_RUN_IT.md` §C carried, in bold: *"Do not point the tool at an ESPN mock… It cannot
work."* That was correct on 2026-08-30 and was measured (doc 126): ESPN's read API serves a
practice room's opening state and never its live picks.

**The bridge (doc 137) made it irrelevant six days later and nobody went back to the sentence.**
The picks come out of the browser. `espn_bridge/manifest.json` matches
`https://fantasy.espn.com/*` — the whole domain, not one league — so a practice room is hooked
exactly like the real one. Verified by reading the manifest, not by assuming.

**`--mock` is not optional in that room.** It clears keeper depletion and keeper-row detection.
A practice room has no keepers; without the flag the board runs 12 picks ahead of it all night
and says nothing about it (doc 149 finding 4). The tell Matt can see: if Pickens is in the
available pool, the room has no keepers.

`00_HOW_TO_RUN_IT.md` §C rewritten. `live_draft.py`'s own usage header rewritten too — it still
showed `py live_draft.py` as "live draft night", the path doc 136 killed.

---

## 3 — AND THE DOCUMENTED FALLBACK COULD NOT WORK. FIXED.

`detect_shape()` calls ESPN for the league's size and draft order. On failure it exits with:

> `SHAPE DETECTION FAILED (…). Pass both explicitly: --mock --league N --slot N --teams N`

**The GET ran unconditionally, BEFORE `teams`/`slot` were looked at.** So obeying that instruction
re-issued the same failing request and printed the same line again. Forever. And a practice league
is precisely where the GET fails — doc 126 measured that ESPN deletes it (`"This League has been
deleted."`) — so the one room the fallback exists for is the one room it could not rescue.

**Fix:** if both are supplied, believe the operator and skip the network entirely.

```
if teams and slot:
    print("  shape supplied on the command line: %d teams, slot %d (ESPN not consulted)")
    return teams, slot
```

`ERROR_PATTERNS`: an error message that names a remedy the code cannot honour. Not "an exit code
is not a result" (§0.2) — worse, because the remedy *looks* tested.

**NEGATIVE CONTROL RUN FIRST (§0.2).** The real module imported, `requests.get` stubbed to raise:

| case | before | after |
|---|---|---|
| `--slot 5 --teams 12`, ESPN dead | SystemExit, same message | **returns (12, 5)** |
| `--teams 12` only | SystemExit | SystemExit *(unchanged)* |
| `--slot 5` only | SystemExit | SystemExit *(unchanged)* |
| neither | SystemExit | SystemExit *(unchanged)* |
| ESPN alive, both supplied | 1 network call | **0 network calls** |
| ESPN alive, auto-detect | slot 8 from `pickOrder` | slot 8 from `pickOrder` *(unchanged)* |

**Draft night is untouched by construction.** `main()` calls `detect_shape` only under
`if a.mock or a.slot or a.teams`; `py live_draft.py --bridge` takes the else-branch and runs
`verify_slot()`, which still cross-checks the compiled slot 8 against ESPN's published order.
The diff is two hunks: the docstring and this guard. Nothing else in 124 KB moved.

3.12-safe (no invalid escapes), LF endings preserved, `py_compile` clean.

---

## 4 — COMMITTED

| file | pin |
|---|---|
| `Scripts\live_draft\live_draft.py` | **124802 / `85eda73deade4e26`** |
| `Scripts\check_kit.py` | re-pinned for the above |
| `Scripts\00_HOW_TO_RUN_IT.md` | §C rewritten |

Originals archived to `2026\_archive\` as `live_draft_20260906.py` / `check_kit_20260906.py`.
`player_context.csv` verified against its pin (109468 / `96f92c5fa2ea9d70`) — unchanged by this
morning's `sept5_after.bat` run, so nothing else needs re-pinning.

---

## 5 — WHAT A PRACTICE DRAFT DOES NOT TEST

The bots are ESPN's, not §5's twelve managers. **The room is a plumbing test and a reflex drill —
where the eye goes, how fast `cost vs #1` reads, whether the page keeps up. It is not a rehearsal
of the opponent model, and nothing that happens in it should move a pick.**

---

## 6 — COMMANDS.html WAS THREE THINGS OUT OF DATE

Matt asked. It was, in four ways — one of them a command that could not work.

**(a) It carried `py live_draft.py --mock --url "…"` — no `--bridge`.** That is the pre-bridge
form: the board would read ESPN's feed, which serves nothing during a practice room. The one
command on the page for the thing he was about to do was the one command that could not do it.
Replaced with the three-line lane from §1, `--bridge --mock` first.

**(b) Section 6b listed TEN Saturday steps. `sept5_after.bat` runs THIRTEEN.** Missing entirely:
both grids (`make_gridboard`, `make_gridboard --board`), the tier sheet (`make_tiers`), the key
rebuild (`make_howto`) and the plain-English check (`check_plain --warn`). Five shipping steps and
three shipping printouts had no entry anywhere on the console. Added, in the batch's own order.
*(The batch's own header comment still reads "TEN STEPS" — cosmetic, inside a REM line, and not
worth a re-pin an hour before the scheduled run. Post-draft.)*

**(c) Nothing on the page named TIER_SHEET, ADP_GRID or BOARD_GRID** — three of the six sheets on
his desk. Section 5 now says which sheets build their own PDFs, and therefore which ones
`to_pdf.py --check` **cannot** report stale.

**(d)** Two copies exist — `Source\COMMANDS.html` and `2026\COMMANDS.html`. Not a collision:
`sync_desk_copies.STABLE` copies the first to the second undated, because it is bookmarked. Both
written.

103 entries, parsed and checked after editing; zero malformed rows.

---

## 7 — AND THE DESK AUDIT COULD NEVER HAVE RUN

Following (c) turned up two more, both of the same family doc 161 and doc 174 already named.

**`make_shortcuts.DOCS` had no link for `BOARD_GRID_` or `TIER_SHEET_`.** Both ship, both are on
the desk, both re-date on every refresh — and nothing on the Desktop pointed at either. That is
**doc 174's defect, a third and fourth time, with doc 174's own warning comment sitting directly
above the list.** Added as links 13 and 14.

**`audit_desk.py` is the guard written to catch exactly that, and it has never once run.** It does
`open(os.path.join(HERE, 'sync_desk_copies.py'))` where `HERE` is `Scripts\research\` and both
files it reads live one level up in `Scripts\`. Every invocation ever given it raised
`FileNotFoundError` on line 6.

> **§0.2: a guard that has never been executed is not a guard.** A guard with a broken path is
> worse — it looks like one on the shelf, and its existence is why nobody checked by hand.

**NEGATIVE CONTROL RUN FIRST.** The shipping file, on the real two-folder layout:
`FileNotFoundError`. Patched (walk up one level when `HERE` is `research`), same layout:

```
  ok   06..12  (unchanged)
  ok   13 - Our board grid.url          -> BOARD_GRID_*.pdf
  ok   14 - Tier sheet.url              -> TIER_SHEET_*.pdf
  PASS
```

Nine desk copies, nine links, no "re-dated but not linked" note for the first time.

**It is still not wired into `sept5_after.bat`.** Post-draft — that is a batch edit and a re-pin,
and today is not the day.

---

## 8 — COMMITTED (section 6/7)

| file | note |
|---|---|
| `Source\COMMANDS.html` + `2026\COMMANDS.html` | 42,639 → 46,152 bytes |
| `Scripts\make_shortcuts.py` | **9273 / `949219f3e674d3d2`** — links 13 and 14 |
| `Scripts\research\audit_desk.py` | path fixed, guard runs, PASS |
| `Scripts\check_kit.py` | re-pinned for `make_shortcuts.py` |

Originals archived to `2026\_archive\`.

**STILL OPEN, and he should know before he prints:** `DRAFT_CARD` and `DRAFT_DAY_GUIDE` are
deliberately excluded from the rebuild (doc 146 — `card.html` is landscape and the desk PDF is
portrait, so rebuilding rotates it). Their desk copies still carry **today's** date while their
content is Sept 5 and Sept 1. **Do not print either.**
