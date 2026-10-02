# 353. THE COMMAND PAGE HAD NO BUILDER, AND TWO BATCH FILES WERE ONE JOB WEARING THREE NAMES

*18 Sept 2026. Matt: "i wanted this updated: COMMANDS.html ... if there are commands that live
better in a bat file for simplicity do that. same on the wire.py, and other commands, if those py
files can be consolidated instead of needing multiple commands for me, then lets explore that."*

## 1. WHAT THE FOLDER SAID BEFORE ANYTHING WAS TOUCHED

`COMMANDS.html`, 47,036 bytes, last modified **3 September**. Fifteen days. It describes draft
night, which was the 7th.

- **No builder.** Five files mention the name; none writes it. `make_shortcuts.py` points a
  desktop link at it, `sync_desk_copies.py` copies it, `tidy_docs.py` protects it from cleanup.
- **Not pinned.** `check_kit.py` had no entry for it, so nothing could notice it going stale.
- **Two copies**, root and `Source\`, both 47,036 bytes, both from the 3rd.
- **The to-do page already knew.** `sheet_engine.TODO_LINKS` labels it *"the old command page ...
  superseded by the list below."*

**Section 9 of the directive already carries the rule it broke:** every prose map in this project
went stale within hours, and the answer is that the map has to be generated. `make_howto.py` does
exactly this for HOW_TO_READ_IT, off `live_draft.COLGLOSS`.

## 2. AND THE BATCH FILES WERE WORSE THAN STALE, THEY WERE LYING

| file | what it ran | its own header claimed |
|---|---|---|
| `ff.bat` | lineup, wire, to-do page, kit check | correct |
| `weekly.bat` | `py wire.py --html` ONLY | *"Registered by setup_tasks.ps1 as FF2026 - Tuesday wire"* |
| `gameday.bat` | `py lineup.py --html` ONLY | *"task FF2026 - Lineup check"* |

**`setup_tasks.bat` DELETES both of those task names** and registers four tasks that all call
`ff.bat`. So both headers were false, and both files were a second and third NAME for one JOB,
which is doc 146's `after_pull.bat` defect exactly. **Running `gameday.bat` out of habit got the
lineup check and left the wire, the week sheet, the to-do page and the kit check stale** while
looking like the quicker option.

Both are now stubs that `call ff.bat` and pass their arguments through, the same treatment
`after_pull.bat` got. An old shortcut still works and now gets the whole run.

## 3. SO THE ANSWER TO "CAN THE PY FILES BE CONSOLIDATED" IS THAT THEY ALREADY WERE

`ff.bat` has run all four steps since the 17th, and `py wire.py --html` builds the wire AND the
week sheet in one call. **The only command left that ff.bat does not run is
`py research\wk1\build_form.py`, and its exclusion is deliberate and documented in ff.bat's own
comment block:** it needs the internet and it writes the file the sheet reads, so a half-write on
a schedule would poison the page. That is a real reason, not an oversight.
**NOT YET RUN, with the form written: make `build_form.py` write to a temp file and rename
atomically, then it can join `ff.bat` and Matt's last standing weekly command disappears.** The
missing input is nothing; it is a small change to one script and a re-pin.

## 4. WHAT SHIPPED

**`make_commands.py`**, new and pinned on its first day. It generates `COMMANDS.html` from:
- **`sheet_engine.TODO_CMDS`** , the same list the to-do page prints, so the two cannot drift.
  One source, two renderings.
- **the batch files themselves** , every `py X.py` line each one really runs, parsed out.
- **`setup_tasks.bat`** , the four scheduled tasks, their days and times, parsed out.

It uses `sheet_engine.CSS` and `TODO_CSS`, so the page looks like the to-do page, which is what
Matt asked for on the masthead link in the same message.

**THE GUARD, AND IT WAS SHOWN FAILING FIRST (0.2).** Every script the page would name is checked
against the folder before any HTML is built; the page **refuses to write** and names the misses.
The negative control was a deliberately absent `research\close_check.py`: it refused, exit 1, with
the name printed. The file was then created and it passed. **A guard that has never been executed
is not a guard.**

## 5. TWO DEFECTS THE TEST CAUGHT, BOTH REAL

1. **The page claimed `ff.bat` runs `build_form.py`.** The step parser matched inside ff.bat's own
   `echo` reminder line. **A page asserting that a batch file runs a step it deliberately refuses
   to run is worse than no page.** Echo lines are skipped now.
2. **The schedule's "runs" column came back empty.** `/tr` carries escaped quotes
   (`/tr "cmd /c \"%S%ff.bat\" TUE"`), so anchoring on the closing quote found `cmd /c \` and no
   batch file. Taken from the rest of the line instead.

Neither would have raised anything. Both were found by looking at the rendered page rather than
the exit code.

## 6. ALSO IN THIS PASS

- The masthead link is a `<p class="jump">` now, the **same rule** the to-do page's jump links
  use. It lived in `TODO_CSS`, so only that page could reach it; it moved to the shared `CSS`.
  One rule, two pages, which is doc 351's defrag at stylesheet scale.
- The masthead carries a second link, to the commands page.
- `ff.bat` gained the commands step and checks that artifact alongside the other four.
