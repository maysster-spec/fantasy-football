# 163 — The replay passed, and the page explaining the board had no builder

**2026-09-04, morning.** Two things Matt asked for, and one defect that fell out of the second.
Everything below was executed, not reasoned.

---

## 1. `py live_draft.py --replay 2025` — **PASS. The last §8 item that needed his ESPN session
   is now closed except for `fetch_keepers.py --dry`.**

Run at 08:51 EDT, redirected to `replay_log.txt` (`py -u ... > replay_log.txt 2>&1`) because I
have no shell on his machine and console output never reaches me. The `-u` matters: without it
Python block-buffers 8 KB and a hang loses the log.

```
replay: 180 rows fetched (12 flagged keeper). unmapped player ids: 45
your team (9): 15 rows in the 2025 feed, 12 will appear on the 'Draft complete' panel.
  not shown: playerId 4426354 / -16002 / 4362081
replay complete -> ...\live_board.html
```

- **180 rows, 12 keeper rows.** That is §2.1(b2) — the twelve keepers ESPN rides at round 15 /
  overall 169–180 — flagged and filtered on a **real ESPN feed**. Doc 58's failure (the clock
  running twelve picks ahead) cannot happen. This is the one thing docs 79–82 could not verify,
  because every response in those tests was mocked.
- **181 renders, no traceback**, and the `len(picks)!=180 or nk!=12` guard did not fire.
- **45 unmapped ids** — 2025 players not on the 2026 board. Expected.
- **`playerId -16002`** — a D/ST arriving as a negative id, third independent confirmation of the
  `-16000 − proTeamId` convention (§8 item 2, closed in doc 155 from the write side).

### The one defect it exposed: the slot banner gives draft-night advice during a dry run

The log opens with

```
!! SLOT MISMATCH. The tool is planning for slot 8; ESPN's published
   order puts team 9 at slot 11. Order: [3, 12, 13, 5, 11, 4, 1, 10, 7, 2, 9, 6]
   EVERY turn is being planned for the wrong picks. Restart with --slot 11
   before the draft starts.
```

`verify_slot` (doc 125) checks whatever season it is given, and `--replay 2025` gives it **2025** —
a season in which team 9 genuinely sat at slot 11, in a league that still had a team 13 and no
team 8. **The check is correct and working.** What is wrong is that a dry run prints an
instruction (`--slot 11`) which would corrupt every turn of Monday night if followed. Same class
as doc 149 finding 6: a message that names the wrong remedy. **Fix pending — suppress or re-word
under `--replay`. Not applied yet: `live_draft.py` was executing at the time and doc 0.2 says do
not edit the object under test.**

---

## 2. `GONE_ROWS` 8 → 14, and 14 is not a taste

Matt: *"Raise to 14 or 12, that's easier to see what i missed in the prior round."* He offered two
numbers. **14 is the right one and 12 is not, for a reason his own pick structure supplies.**

From slot 8 the gaps alternate 9 and 15 picks — 8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137,
152, 161 — so the number of picks made by **other** managers between two of his turns is exactly
**8 or exactly 14**, every time, all night.

- At **14 rows this column always holds everything taken since he last picked**, on all fourteen
  turns. On the long waits (32, 56, 80, 104, 128, 152) it is precisely that window, ending at `-13`.
- At **12** it truncates every long gap by 2 — including **pick 32**, the longest-gap and most
  decisive turn on the board (§2.1, §7).
- Past 14 there is no question it answers.

### Layout: measured, not assumed — A/B on the same states

doc 147 fixed this column at 8 rows *to stop the page changing height*, so raising it is exactly
the change that could undo doc 139's fixed shape. Both files were run through the production
`Engine` and `step()` at all twelve of Matt's flexible turns, rendered in headless Chrome, and the
element boxes measured:

| pick | 8 rows | 14 rows |
|---|---|---|
| 8 / 17 / 32 / 41 | gone 493 · split 495 · board 416 | **identical** |
| 56 | gone 512 · split 514 · board 436 | **identical** |
| 65 … 137 | 493/495/416 and 512/514/436 | **identical** |

**Every measurement is byte-identical; the only difference in the DOM is `li` 8 → 14.** The
column was already allocated 493 px by the flex row and 8 names used ~199 px of it. The board side
governs the height and still does. `SHAPES: [(12, 3)]` — one shape, doc 139's invariant intact.

---

## 3. The defect that fell out: **HOW_TO_READ_IT had no rebuild path at all**

Raising `GONE_ROWS` meant editing `live_draft.COLGLOSS`, whose gone-column entry read *"The last
**eight** players taken … it is deliberately short."* Both clauses were now false. doc 159 built
`make_howto.py` precisely so the paper could not drift from the screen — so I went to re-run it,
and found the wiring was never finished:

- **`sept5_after.bat` never called `make_howto.py`.** Ten steps, and that is not one of them.
- **`to_pdf.py`'s `PAGES` list did not contain `HOW_TO_READ_IT`.** Four printouts, not five.
- **`sync_desk_copies.py` *does* carry it** (`("how-to  ", "HOW_TO_READ_IT.pdf")`) and doc 146's
  guard refuses a PDF older than its page.

So the desk copy was live, the guard was live, and **neither half of the rebuild was**. Editing
the board's own legend would have changed the screen and frozen the page that explains it — and
doc 146's guard *cannot catch it*, because a page that is never rebuilt never becomes older than
its PDF. **This is doc 146's defect in a fifth place, and the first one where the guard was
already installed and still blind.**

**Fixed, both halves, and executed:**

- `to_pdf.py` `PAGES` += `HOW_TO_READ_IT`. Negative control run first: PDF deleted → `OUT OF DATE
  … never built` → `rebuilt HOW_TO_READ_IT`. Also verified down the Chrome+`ZOOM=0.78` path with
  wkhtmltopdf hidden from `PATH`, which is what Matt's machine will use (doc 146).
- `sept5_after.bat` step 9 now runs `py make_howto.py` **before** `py to_pdf.py`, with
  `if errorlevel 1 set STALE=%STALE% HOW_TO_READ_IT`.
- `make_howto.py` is now **pinned in `check_kit.py`** for the first time — same argument as the two
  batch files in doc 146: a script the Saturday chain depends on, unhashed, silently freezes the
  only page that explains the board.
- Page and PDF regenerated (its own guard passed: *all 14 badge labels found in live_draft.py*),
  written to `Source\`, dated copy to `2026\HOW_TO_READ_IT_20260904.pdf`, and the Desktop shortcut
  `11 - How to read the board.url` re-pointed — doc 161's failure was a link that silently opens
  an older document than the one beside it.

---

## 4. The six-hour bridge guard, executed both ways

§0.2: *a guard that has never been executed is not a guard.* The bridge staleness check
(doc 137 v1.8, re-aimed in doc 148 finding 3) has never been run against a genuinely old file.
It can be, for free, because `bridge_picks.json` is the 09-02 capture:

```
NEGATIVE CONTROL 1 — the real file, updated 2026-09-02T20:00
  !! STALE BRIDGE FILE -- its newest pick is 41.2 hours old.
  returned picks: 0            <- correct, the 179 picks are refused

NEGATIVE CONTROL 2 — same file, `updated` re-stamped to now
  returned picks: 179          <- correct, a fresh listener is accepted
```

**Both directions correct.** The guard discriminates on data age, not on process ordering — which
was doc 148's whole point, and it had never been shown.

---

## Pins after this doc

| file | bytes (LF-normalised) | sha256[:16] |
|---|---|---|
| `live_draft.py` | 123542 | `8e6f229e0e21dec7` |
| `to_pdf.py` | 11061 | `cd4ed3f2f31d28a8` |
| `sept5_after.bat` | 7388 | `d44877f068c0e3e0` |
| `make_howto.py` | 15413 | `8f12a17ff2e68346` (new entry) |

All four re-staged from Matt's machine after committing and re-verified against `check_kit.py`'s
MANIFEST: **ALL PINS MATCH.** The superseded board is archived at
`_archive\live_draft_20260904_0812.py`.

## Still open

1. `py fetch_keepers.py --dry` — the **last** untested item that needs his ESPN session.
2. The `--replay` slot banner (§1 above) — mine to fix, once nothing is running.
3. Re-run `01 - Check everything` to confirm the file tree after today's four writes.
