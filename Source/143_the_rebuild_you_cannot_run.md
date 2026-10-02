# 143 — The REBUILD verdict you cannot act on, and three of my scripts that broke on your machine

**2026-09-03 evening · the Sept-3 refresh, run live · T-4 days**

---

## The do-this list

1. **Do NOT try to rebuild the board.** There is nothing to run — see §1. Your board is in the
   correct state and `apply_news.py` is not needed, because no rebuild happened to undo.
2. **Take the new `OVERRIDE_CARD.pdf` to the draft alongside the board.** Six names, one page.
   That sheet is doc 62 Option A's missing instrument.
3. Re-run `py parse_ladder.py` then `py mkvalue.py` — both now work without scipy, and the
   ladder's columns are pinned.
4. If `wkhtmltopdf` is still missing, open the `.html` each script writes and print to PDF.
   Worth checking whether you opened a new terminal today — it worked at 14:03 and not at 14:4x.

---

## 1. THE VERDICT SAID REBUILD. THERE IS NO REBUILD.

`sept5_check.py` returned **REBUILD — only 97/161 held within 2 slots**, and pointed at doc 62 §5.

**Doc 62 is the reason you must not chase it.** Verified again tonight by reading the code:
`sept5_check.py` contains no `to_csv` and imports no builder — **it only reports.** And doc 62's
finding stands: **`board_v8_fixed.csv` has no builder at all.** No script produces it; it came out
of ad-hoc code during the Aug-27 red team and was never saved. `code_build_board_v7.py`, the file
the handover calls "the board builder," is hardcoded to the **Aug-23** pull and writes
`board_v7_2026.csv` — a filename deliberately trashed as a trap.

So the REBUILD verdict has no executable answer, and doc 62 §5 already chose between the two:

> **A — FREEZE.** Draft off the verified board. Handle the news manually as overrides at the pick.
> **B — RECONSTRUCT** — only if a new builder reproduces the existing board **byte for byte**
> from the Aug-23 inputs first. *"Do B only if it reproduces exactly. If it does not, take A. A
> rushed board rebuild is the larger risk."*

Four days out, B is precisely the rushed rebuild that sentence forbids. **Take A.**

### What the board actually holds right now — checked, not assumed

| player | board proj / rank | the 09-03 pull says |
|---|---|---|
| **Josh Jacobs** | **0.0 / 435** | 152.5 / 93 |
| Isiah Pacheco | 114.9 / 143 | 66.6 / 208 |
| Kyler Murray | 289.3 / 141 | 327.2 / 90 |

The board carries the **08-30 projections** with the **09-03 ADP** — which is exactly Option A
working as designed, and it is **good news in the one place it matters most**: Josh Jacobs is on
the Commissioner's Exempt List (`news_overrides.csv`, Aug 30, "draft as if he does not play"), the
board still has him at **0.0, rank 435**, and the pull is trying to restore him to **rank 93**.

**Nothing needs `apply_news.py --write`.** That command exists to re-apply the overrides *after* a
rebuild wipes them. No rebuild happened, so the override was never wiped. Running it is harmless;
needing it is what would have been the emergency.

## 2. THE MISSING INSTRUMENT — `mkoverride.py` / `OVERRIDE_CARD.pdf`

Doc 62 Option A says "handle the news manually as overrides at the pick" and **nobody ever built
the thing you hold while doing that.** Written tonight. It compares the shipped board against the
newest pull, recomputes VBD on §4.1's replacement levels so both ranks sit on one scale, and prints
every player inside pick 175 whose projection moved 15+ points.

**Six names. That is the whole exposure.**

| player | adp | board rank → now | projection |
|---|---|---|---|
| **Josh Jacobs** | 72 | 435 → 93 | 0.0 → 152.5 — **NEWS OVERRIDE HOLDS, IGNORE THE PULL** |
| **Isiah Pacheco** | 160 | 143 → **208** | 114.9 → 66.6 — the board has him **65 ranks too high** |
| MarShawn Lloyd | 120 | 184 → 131 | 78.2 → 124.4 |
| Kayshon Boutte | 171 | 188 → 143 | 72.3 → 113.4 |
| **Kyler Murray** | 137 | 141 → **90** | 289.3 → 327.2 — live at your pick 137 |
| **De'Zhaun Stribling** | 139 | 145 → **116** | 109.0 → 134.1 — Boone's dart, now better |

The Jacobs row renders amber with the override note on it, so the one row where the board beats
the pull cannot be misread as the one row to correct.

**Note what is NOT here: nothing inside pick 89.** `sept5_last.txt` shows picks 32 and 41 at 5/5
unchanged and 56/65 at 4/5. The churn is all rank 90+ — September roster cuts turning on
projections for players who made rosters. **The top of your board did not move**, which is why
Option A is cheap here even though the verdict looked alarming. `[The aggregate cost of Option A
remains unmeasured — doc 62 §4 — and this does not measure it. It bounds where it can come from.]`

## 3. THREE OF MY SCRIPTS BROKE ON YOUR MACHINE, AND ONE WAS A REAL DEPENDENCY MISTAKE

**(a) `parse_ladder.py` needed scipy, which you do not have.** It died on the import before
reading a row. The only thing it used scipy for was one normal CDF; that is now `math.erf` from
the standard library, identical to 1e-15. **I shipped you a script with a dependency I had in my
container and never checked you had.** Also fixed the `SyntaxWarning` your Python 3.12 printed —
an unescaped `\ ` in my own docstring.

**(b) `mkvalue.py` crashed when `wkhtmltopdf` went missing** instead of falling back to HTML the
way `make_fallback.py` does. Already fixed in the copy on your disk; I kept that fix and built on
it. Your PATH is the open question, not the script — it rendered PDFs at 14:03 and not at 14:4x.

**(c) The column drift you remembered is real, and now closed by measurement.** Each PICK section
is its own `<table>` with no declared widths, so every table sized its columns to its own content.
Fixed widths plus fixed layout. **Verified in PDF geometry, not by eye:** the `STILL THERE` header
now starts at x = **213.879329** points in **all eleven** tables.
**A method note, because I nearly shipped the wrong answer:** my first check used
`pdftotext -layout`, which reported seven different offsets *after* the fix and made it look like
it had failed. That tool quantises to an ASCII character grid — it was measuring its own
approximation. `pdftotext -bbox` reads the real coordinates. **Same lesson as the scratch-pad's
own retraction on this item: test the object, not a proxy for it.**
Fixed layout then squeezed two badge cells (`JOB` printed on top of `DISC`); the badge column is
wider and badges wrap now.

**(d) Answered on the sheet, so it stops being a question:** rows are ordered by **how many
sources agree**, then by how far the analysts sit ahead of ADP — deliberately *not* by VBD or
board rank. Ranking by value is the draft board's job; this sheet answers where several
independent things happen to point at the same name.

## 4. Two things from your log that are not defects

- **`board_audit.pyd`** — a typo. The command is `py board_audit.py`. It passed 39/39 once run.
- **`refresh_adp.py` reporting "0 of 161 changed"** — a second run against a pull already applied.
  Closed independently by the scratch-pad against three `_archive\board_v8_fixed_preADP_*.csv`
  snapshots. The script is fine.
- **COMMANDS.html ordering `depth_map.py` before `make_fallback.py`, against `refresh_adp.py`'s
  own footer.** `make_fallback.py` reads the board, `depth_map.py` reads the board and writes
  `player_context.csv`. You ran make_fallback first, then depth_map — **run make_fallback again**,
  so the paper board carries the job labels depth_map just stamped. Harmless either way tonight;
  worth one line in COMMANDS.html.

---

## 5. Close (§7)

**Top 3 assumptions → what would invalidate each**
1. *Option A is the right call.* Rests on doc 62's byte-for-byte gate and on the movers being
   rank 90+. Invalidated if a top-40 player's projection moves before Monday — re-run
   `py mkoverride.py` after the Sept-5 pull and look at the ranks, not the count.
2. *The board's ADP is current and only its projections are stale.* `adp_vintage.txt` reads the
   09-03 pull and `refresh_adp.py` wrote it. Invalidated by another pull without another
   `--write`.
3. *Six movers is the whole exposure inside pick 175.* Threshold is 15 points; a 14-point move on
   a pick-104 dart would not appear. Lower `MOVE` in `mkoverride.py` to see more.

**The missing input that would most improve this:** a builder for `board_v8_fixed.csv` that
reproduces it byte for byte — doc 62's Option B, done properly, after the draft. Until that exists
every REBUILD verdict for the rest of this season resolves to this same card.
