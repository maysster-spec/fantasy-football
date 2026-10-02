# 146 — The paper stopped following the board, and nothing said so

**Sept 3 2026, T-4 days.** Matt asked two things: make the command page understandable
("the scenarios need to be written in plain English… I need to easily understand when to use
them"), and tell him whether his Desktop shortcuts need adding, modifying or removing. Both
answers turned out to sit on top of a defect that had been running silently for four days.

---

## 1. THE DEFECT — every printout on the desk was older than the board it came from

`shutil.which('wkhtmltopdf')` returns **None** on Matt's machine. Not a guess — his own console,
Sept 3:

```
py make_fallback.py
wkhtmltopdf not on PATH. Wrote ...\Source\FALLBACK_BOARD.html -- open it and print to PDF.

py mkvalue.py
TypeError: expected str, bytes or os.PathLike object, not NoneType     <- exe was None
```

Every page in this project is built the same way: write an `.html`, then shell out to
`wkhtmltopdf` to make the `.pdf`. **Five builders do this** — `make_board`, `make_fallback`,
`mkvalue`, `mkoverride`, `make_sheets`. Four of the five handle the missing program politely:
they print a line and `return`, **exit code 0**. So:

| what happened | what it looked like |
|---|---|
| the page rebuilt | a line of output nobody reads twice |
| the PDF did not | no error, exit 0, batch carries on |
| `sync_desk_copies.py` copied the old PDF to the desk | `OK  board  DRAFT_BOARD_20260903.pdf  269,739 bytes` |

**A byte count is not freshness.** On Drive right now: `DRAFT_BOARD.html` Sept 1,
`DRAFT_BOARD.pdf` Sept 1, `FALLBACK_BOARD.html` **Sept 3 16:47**, `FALLBACK_BOARD.pdf`
**Aug 31**. The Saturday refresh, run as designed, would have refreshed every page and left every
PDF, and then handed him a Sept-1 board with a Sept-5 date stamped in the filename.

This is doc 109's failure — *the paper cannot follow the board* — rebuilt as an automatic process
with a success message on it.

### The fix needs no install
`to_pdf.py` (new). Tries wkhtmltopdf, then Chrome, then Edge; Chrome is already on the machine.

**MEASURED, not assumed — the zoom.** Chrome maps 1 CSS pixel to 1/96 inch. wkhtmltopdf assumes a
1024px-wide page. Same HTML, different paper:

| page | wkhtmltopdf | Chrome @1.0 | Chrome @**0.78** |
|---|---|---|---|
| DRAFT_BOARD | 7 | 12 | **7** |
| VALUE_LADDER | 3 | 3 | **3** |
| FALLBACK_BOARD | 2 | 4 | **2** |

Swept 1.0 / 0.85 / 0.80 / 0.78 / 0.75 / 0.70. **0.78 reproduces wkhtmltopdf's page count exactly
on all three.** 816/1024 = 0.797, so the constant is the page-width ratio, not a fudge. Without it
Matt's main paper board goes from 7 sheets to 12.

**Landscape had to be carried twice.** `make_fallback.py` passed `-O Landscape` — a wkhtmltopdf
flag Chrome ignores. Added `@page{size:Letter landscape}` to its CSS; wkhtmltopdf honours both.
Verified by reading the PDF's MediaBox: 792×612.

**`make_fallback.py` deleted its own .html on success.** That page is now the freshness reference,
so deleting it turns the new check into a silent skip. It is kept.

**Negative controls, both run.** No renderer at all → refuses, changes nothing, names the pages to
print by hand, exit 1. A renderer that exists but writes nothing → `FAILED`, says the old PDF is
now wrong, exit 1, and `sept5_after.bat` skips the desk copy rather than distributing it.

`sync_desk_copies.py` now **refuses to copy any PDF older than the page it came from**, and gets
that page list by importing `to_pdf.PAGES` rather than keeping a second copy of it.

### What is deliberately NOT rebuilt
`DRAFT_CARD.pdf` and `DRAFT_DAY_GUIDE.pdf`. They *are* built from `Scripts\card.html` and
`guide.html` — **verified, not assumed: all 364 distinct words in DRAFT_CARD.pdf appear in
card.html.** But `card.html` declares `@page{size:Letter landscape}` while the PDF on the desk is
**portrait**, because it was built without `-O Landscape`. Chrome honours the CSS, so rebuilding
would silently rotate the two-page card Matt has already read, four days out, for no gain —
nothing in the Saturday refresh changes their content. That is a decision, not a side effect.

---

## 2. I HAD SHIPPED A DUPLICATE OF AN EXISTING FILE

`after_pull.bat`, written Sept 3, ran refresh_adp → board_audit → depth_map → make_fallback →
mkoverride → parse_ladder → mkvalue. `sept5_after.bat`, written **Aug 30**, already ran nearly the
same sequence — and better, because it shows the market moves and asks before writing.

I wrote the second one without listing the folder first. That is the doc-138 doc-number collision
in a different costume, and the naming rule (`00_PROJECT_DIRECTIVE.md`: one name, no version) does
not cover it, because these were two *names* for one *job*.

**Resolved:** `sept5_after.bat` is the one file. `after_pull.bat` is now a two-line stub that calls
it and says it is safe to delete. It is deliberately **not** pinned in `check_kit.py`, so deleting
it does not turn a tidy-up into a FAIL.

### And the merged sequence was missing a step
`sept5_after.bat` ran `make_sheets.py` (the three sheets doc 116 retired) and **never ran
`make_board.py`** — the builder of `DRAFT_BOARD.pdf`, the board Matt actually drafts from. Ten
steps now, in dependency order, with the first three as gates:

```
refresh_adp (look) -> prompt -> refresh_adp --write   gate
board_audit                                            gate
depth_map                                              gate
make_board  ->  make_fallback  ->  mkoverride  ->  parse_ladder  ->  mkvalue
to_pdf
sync_desk_copies
```

Steps 4–8 no longer halt the run; they record which printout failed and the run ends with a loud
list of what is now stale. Halting there was worse: one failure meant the other four printouts
never rebuilt either.

---

## 3. `draft_night.bat` WOULD HAVE SHOWN NOTHING ALL NIGHT

Step 5 was still `cd live_draft` + `py live_draft.py`. **Doc 136 proved ESPN's read replica does
not publish a draft until it has ENDED.** The directive's §8 runbook was updated on Sept 3 to start
`bridge_server.py` first; the batch file that Matt's 6:55 PM scheduled task actually runs was not.

Step 5 is now three sub-steps: start the listener in its own window → load the extension and open
the draft room in Chrome → `py live_draft.py --bridge`.

**`draft_night.bat` and `sept5_after.bat` are now pinned in `check_kit.py` for the first time.**
Batch files that drive a whole evening are exactly the "wrong file gets run" failure the checker
exists for, and neither had ever been hashed.

All three batch files were also rewritten with **CRLF line endings**. Every `.bat` in the tree was
LF-only; `cmd.exe` tokenises on both, but `goto` against an LF-only label is a documented soft
spot and these two files are nothing but gates and gotos. CRLF costs nothing — `check_kit`
normalises line endings before hashing, so the pins are unaffected.

---

## 4. THE ANSWER TO MATT'S SHORTCUT QUESTION: two were already dead

| shortcut | state |
|---|---|
| `5 - Draft card` | fine |
| **`6 - Fallback board`** | **dead** — doc 116 retired it as a desk copy and `sync_desk_copies` now DELETES its dated root copy |
| **`7 - Injury sheet`** | **dead**, same reason |
| `8 - Draft day guide` | fine |
| — | **missing: the draft board itself, the value ladder, the override card** |
| `4 - Refresh printouts` | description still read "card, guide, fallback board, injury sheet" |

Two links pointing at files that had not existed since Aug 31, and no link at all to the two
documents built since. A generated folder that quietly rots is worse than no folder, so
`make_shortcuts.py` now **sweeps anything it no longer generates** (matching `^\d+ - .+\.(bat|url)$`,
so Matt's own files are untouched), writes an index of what each entry is, and `--remove` no longer
deletes files he put there himself.

`VALUE_LADDER.pdf` and `OVERRIDE_CARD.pdf` were being built into `Source\` where nothing looked at
them — they are now desk copies, which is what made the links possible.

The new folder: command page, then **check everything · Saturday refresh · DRAFT NIGHT ·
fix ESPN sign-in · refresh printouts**, then **draft board · value ladder · draft card ·
override card · guide**. Two-digit numbering so the order holds outside Explorer's natural sort.

**Matt's answer in one line: he changes nothing. `py make_shortcuts.py` rebuilds the folder.**

---

## 5. COMMANDS.html — rewritten in plain English

Every section heading and every "when" line is now a sentence about a **situation**, not about the
software. The worst offenders, before → after:

| before | after |
|---|---|
| `if the batch stops on a gate` | *it tells you which step it stopped on — start again from that one* |
| `401 / 403 / Update Failed` | *a command stops with 401, 403, or "Update Failed". Your ESPN sign-in has expired — nothing is broken.* |
| `the pull fires itself at 8:00 AM` | *your computer downloads the new projections by itself at 8:00 AM. You read one line, then run one command.* |
| `the task opens this by itself; these are the manual fallback` | *the keepers lock at 7:00. One command does the whole hour.* |
| `already done — re-run only when the printouts change` | *after ANYTHING gets rebuilt — otherwise you are reading last week's board* |

Plus a collapsible **glossary** at the top of every tab — twelve terms that cannot be avoided,
one sentence each: the board, value (VBD), draft position (ADP), effective draft position,
still there / p(next), the ranking list, the bridge, "it stops / a gate", 401/403, STALE,
FREEZE/REBUILD, the keeper lock.

Structural: 96 cards, 16 sections, five tabs renamed (*This week · Saturday — the refresh ·
Monday — draft night · Something is wrong*). `parse_ladder.py`, `mkvalue.py`, `mkoverride.py` and
`to_pdf.py` had **no card at all** — Matt had been running them off chat messages. They have one
now. The bridge got its own section, on both the practice tab and the draft-night tab.

Verified by rendering the page in a browser and reading it, not by reading the source.

---

## 6. Two small things, measured while in there

**The ladder's header ran two words together.** `still&nbsp;there` forced STILL THERE onto one line
inside a 7.5% column, so it overflowed into AGREE and the printout read `STILL THEREAGREE`.
Removing the `&nbsp;` lets it wrap to two lines. Fixed and re-rendered.

**`check_kit` was already correct about the two data files.** `board_v8_fixed.csv` reads 41,573
bytes on disk against a pin of 41,092, and `player_context.csv` 76,697 against 76,431 — but
`check_kit` normalises CRLF before hashing, and the normalised sizes match exactly. Checked before
re-pinning. Re-pinning them would have been a change made to fix a problem that was not there.

---

## WHAT THIS COST, AND THE PATTERN

Three of the six things above are the same mistake: **a step that cannot do its job, reporting
success.** The PDF builder that returns 0 when it built nothing. The desk sync that copies a stale
file and prints its byte count. The draft-night batch that starts a board against a feed that will
be empty. None of them would have raised anything on Sept 7.

`ERROR_PATTERNS`, new entry: **an exit code is not a result.** A step that cannot do the thing it
is named after must fail, or the step after it must check the thing itself. `to_pdf.py` and the new
guard in `sync_desk_copies.py` are the second kind; both were built with their negative controls
run first.

And the one that is mine alone: **before writing a file, list the folder.** It cost a doc number on
Sept 2 and a whole batch file on Sept 3.
