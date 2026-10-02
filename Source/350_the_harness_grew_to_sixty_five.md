# 350. THE HARNESS GREW TO SIXTY-FIVE, AND ONE CONTROL PASSED AGAINST THE CODE IT WAS WRITTEN TO FAIL

*18 Sept 2026. `Scripts\research\redteam\redteam_controls.py`, 29,356 bytes and 56 checks at the
start of the night, 34,559 and 65 at the end.*

## 1. C23 PASSED, AND IT SHOULD NOT HAVE

C23 asks whether a named man is on the priority list. My `page_section` helper returned
`txt[heading:]`, which is the heading to the **end of the page**, so "Kaelon Black is on the priority
list" was true because he sits in the seat table two sections further down. **The control passed
against exactly the code it was written to fail.**

Fixed with an explicit end-marker list; an **unbounded section now returns the empty string** rather
than the rest of the document, because a section with no end is not a section. This is §0.2's
"a guard that has never been executed is not a guard" one level in: it HAD been executed, and the
thing it executed against was the whole page.

## 2. C24, AND THE RENAME THAT PROVED THE ANCHOR

C24 checks that the seat table drops anyone rostered or unavailable. It plants injured reserve on a
live seat holder and asserts the row leaves the table and the reason prints. **It failed four ways
the moment the heading was renamed to THE SEAT LIST, which is the anchor working**, not a defect:
the marker tuple named the old heading. Re-anchored, plus a fifth check for the new indicator cells.

## 3. THE CONTROL FILE WAS NEVER PINNED

`redteam_controls.py` had never been in `check_kit.py`, so nothing would have caught a stale copy of
the file whose whole job is catching stale copies. **Pinned for the first time**, through
`os.path.join('research', 'redteam', 'redteam_controls.py')` in both `SCRIPTS` and `MANIFEST`, which
works because the `Scripts` canonical entry is `exact=False`.

And a comment in `check_kit.py` claiming "Verified by C22 and C22c, 65 of 65" was false: C22, the
LOAD_PROBLEM control, has never run. Replaced with a §0.5(a4) **NOT YET RUN** and the testable form.

**65 of 65 at the end of the night, C0 through C24.**
