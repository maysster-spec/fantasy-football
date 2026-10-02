# 342 -- the list was six of forty-three, and the branch under it had never run

**17 September 2026, 20:45 ET.** Matt: *"the to do list is buried for me. Please put a link here, or
somewhere else of your choosing that makes sense. I'm going to be checking that page anyway"* and,
twenty minutes later, *"can't we do better than a text file, but you can still update it without me
running a python file since i don't need to scrape the info for you from espn."*

**Both are right, both are shipped, and neither needs him to run anything.** A live crash was found
while testing the second one.

---

## 1. THE ANSWER FIRST

1. **`Source\MY_TODO.html`** -- every open item, grouped by what it asks of him, with the full
   reasoning under each one. **Already on his drive.** I wrote it there directly.
2. **The week sheet's masthead carries `to-do list -- 44 open` as a link**, in the header line,
   where he drew the arrow on his screenshot. **Already on the live sheet**, patched in place.
3. **`Scripts\todo_page.py`** rebuilds both with **no network and no ESPN session**, so the list is
   never hostage to a pull. It calls `sheet_engine.write_todo_page` -- the same function
   `py wire.py --html` calls -- so the two routes cannot drift (0.5(c)4).
4. **A LIVE CRASH, unrelated to his ask: `wire.py`'s `load_form()` returned THREE values on its
   normal path and TWO on all three of its error paths.** Fixed.
5. **`redteam_controls.py` has been failing its own base control since doc 320** for that reason,
   and nobody noticed because the failure is on a line of his to-do list he has not run.

---

## 2. WHY IT WAS BURIED -- THREE DEFECTS, NOT ONE

He said "buried". The measured answer is that the page was losing the list in three independent
places at once, and any one of them alone would have done it:

| where | what it did |
|---|---|
| `load_todo(src, cap=6)` | returned **6 of 43** open items |
| the same function | took the **first line only**, never the reason under it |
| `.todo li` in the stylesheet | `overflow:hidden; text-overflow:ellipsis; white-space:nowrap` -- **clipped every surviving line at the box width** |
| where `todo_html` lands | **last** in section 0, after the moves, the calendar, the ruled-out list and the watch list |

**The box also never said what it was not showing.** Six items with no count reads as a complete
list of six. That is the whole of the defect in one sentence, and it is `0.5(c)5` -- the missing-row
check -- one level up from where that rule usually bites: nothing was missing from a *table*, the
*list itself* was a truncation with no label.

**FIXED, AND THE BUILDER NOW REFUSES.** `write_todo_page` counts the `[ ]` lines in
`matt_todo.txt` itself and **raises rather than write a page carrying a different number.** A list
that silently shows six of forty-three is exactly the failure it replaces, so the guard is aimed at
the specific historical defect (0.2).

---

## 3. THE BUCKETS ARE MECHANICAL, BECAUSE A JUDGEMENT ON HIS OWN LIST IS ONE HE CANNOT AUDIT

Four kinds, read off the words he wrote, no inference:

| kind | rule | n |
|---|---|---|
| **run** | the line contains a command (`py ...`, `....bat`) | 8 |
| **do** | everything else | 24 |
| **later** | the title starts with a week marker (`week 9`, `~week 6`) | 6 |
| **read** | he wrote READ ONLY / NOTHING TO RUN, or it is a standing DO NOT | 6 |

**The first version had three buckets and put 32 of 43 in `do`** -- a label that sorts nothing.
`later` and the DO NOT rule were added for that reason and for no other.

**And the in-page box is now RUN-FIRST, not file order.** In file order the six it showed included
two commands at positions 2 and 5 and missed the two at 12 and 13. Same six slots, better six.

---

## 4. THE CRASH: `load_form()` RETURNS TWO VALUES ON EVERY PATH THAT MATTERS

`wire.py` line 1577: `form, form_note, form_weeks = load_form()`.

```
def load_form():
    if not os.path.exists(FORM):
        return {}, "no form_2026.csv -- run py research\wk1\build_form.py"        # TWO
    ...
    except Exception as exc:
        return {}, f'form_2026.csv could not be read ({type(exc).__name__})'      # TWO
    if not out:
        return {}, 'form_2026.csv has no cumulative rows ...'                     # TWO
    ...
    return out, note, len(done)                                                   # THREE
```

**Doc 320 added the week count as a third value and changed only the last return.** So the three
branches written to *name a problem in plain English* instead killed the entire run with
`ValueError: not enough values to unpack (expected 3, got 2)`. No page, no reason, no wire.

**All three forced and shown passing before the fix was called done** (0.2 -- a guard that has never
been executed is not a guard):

```
  PASS  missing file     -> 3 values, weeks=0, says: no nope.csv -- run py research\wk1\build_form.py
  PASS  no week-0 rows   -> 3 values, weeks=0, says: form_2026.csv has no cumulative rows ...
  PASS  unreadable       -> 3 values, weeks=0, says: form_2026.csv could not be read (IsADirectoryError)
  PASS  real file        -> 3 values, weeks=1
```

**THIS IS THE SECOND NEVER-EXECUTED BRANCH IN TWO DAYS.** Doc 340 was the `E(` / `_esc(` typo on
the waiver-order line, which had never run because Matt had never been anything but first in the
order. Same shape: a branch that only fires in a state the season had not yet produced.
`ERROR_PATTERNS` should carry the pair, not each alone.

**AND IT EXPLAINS A LINE ON HIS TO-DO LIST.** Item: *"OPTIONAL, SAME MINUTE:
`py research\redteam\redteam_controls.py` # 56 of 56 should pass."* **It would not have.** That
harness copies a whitelist of `Source\` files into a temp tree and **`form_2026.csv` is not on it**,
so every run hits the missing-file branch on its own base control. It has been broken since doc 320
and the only reason it was invisible is that the line was never run.

---

## 5. CONTROLS

**Twelve on the page builder, all run, all passing**, each aimed at a way a to-do line could be
lost or a page could lie:

```
C0  real file: 43 parsed == 43 [ ] lines in the file
C0b every one of the 43 open titles is ON the page, checked BY NAME
C0c the back-link to the week sheet is there
C1  no matt_todo.txt -> writes nothing, returns 0, no crash, link withheld
C2  zero open items -> page written, count 0, done items still render
C3  a title and a note carrying <script> and & are escaped
C4  43 open items -> all 43 on the page; the six-item cap governs the small box only
C5  a parse/file mismatch is REFUSED, not written
C6  the kinds are read off the line: run / read / do
C7  a left-margin section header does not leak into the item above it
```

**C7 failed on its first run** and caught a real defect: the first rule treated any `#` line as a
note, and the file's own section headers (`# ==== RUN THESE ====`) are left-margin comments, so the
header hung off whichever item preceded it. A note must be **indented**, `#` or not.

**Three more on `todo_page.py`:** a sheet with no link is left **byte-identical** rather than
silently edited (doc 303 section 6's lesson); the page still writes when there is no sheet at all;
no `matt_todo.txt` exits 1 and writes nothing. Re-running is a no-op that says so.

---

## 6. FILES

`Scripts\sheet_engine.py` 94,691 -> 106,529 (`17c0b5e52b392553`) ·
`Scripts\wire.py` 109,683 -> 110,233 (`c54f62930b739842`) ·
`Scripts\todo_page.py` **new**, 3,583 (`bae0db33217a6a89`) ·
`Scripts\check_kit.py` re-pinned for all three ·
`Source\MY_TODO.html` **new** · `Source\WEEK_SHEET.html` patched in place ·
`Source\matt_todo.txt` updated. Every overwritten file archived to `2026\_archive\` first, and
every commit **verified by reading the drive copy back**, not by the commit's own result
(AUDIT_LEDGER row 81).

**Nothing was written to ESPN, no claim was filed, nobody was dropped.**

---

## 7. OPEN

* **NOT YET RUN:** `redteam_controls.py` end to end after the `load_form` fix. The base control
  should now reach `wire.main` instead of dying in the unpack. **Inputs named:** it needs the
  harness's Source whitelist to include `form_2026.csv`, or the run exercises the missing-file
  branch every time and the workload screen is never tested.
* **[OPEN]** The three other items I owe and have not written: the seat lane merged into one
  Priority list at the top of Week 2, the next-man-up model written up, and section 4.31's
  hit-value correction into the directive. The measurements are done; the writing is not.
