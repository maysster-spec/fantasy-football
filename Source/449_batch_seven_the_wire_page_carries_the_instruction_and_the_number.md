# 449. BATCH SEVEN: THE WIRE PAGE CARRIES THE INSTRUCTION AND THE NUMBER, ITS ROUTINE SAYS WEDNESDAY, AND THE OTHER TWO PAGES WERE ALREADY SHORT

*29 Sept 2026, 21:50 ET. Claude (Cowork), batch seven of "continue the batches": doc 439's trim ("strike the verbose notes...
the page carries the instruction and the number") applied to the three pages it left NOT DONE. 449 reserved by listing
`Source\` (no doc has landed since 448). No em dashes.*

---

## 0. WHAT TO DO

1. **The wire page's routine now says what the directive says**: put claims in Wednesday night before 3am Thursday (the page
   said Tuesday night, and that claims had no sourced processing day); a drop on every claim (one in six no-drop claims
   fails on the roster limit); the same drop on several claims is a hedge and two men you want both need two drops;
   never a man in the IR slot; Add before Claim. Six one-line items where there were four paragraphs.
2. **The wire page's text is a third shorter (10,967 to 7,162 characters on tonight's rows) and every number it carried
   is still on it** (checked by set difference; the only numbers gone are the build stamp and the time). Gone: the
   scheduler history, "thirty-one for thirty-one", the two-day-period story, "that is the waiver order doing its job", the
   long defense-run and playoff-slate explanations, the paragraph forms of the four claim rules.
3. **`MY_TODO.html`'s frame and command lines are trimmed; `LINEUP_CHECK.html` had one note and it is shorter.** Their
   text was already mostly the items themselves, which are yours.
4. **Guards on the rendered wire page**: `check_plain.py` clean, `check_pages.py` clean but for the sandbox's missing
   commands page, `check_guards.py`'s anchors all match, `check_locals.py` quiet. `wire.py`, `sheet_engine.py` and
   `lineup.py` re-pinned.
5. **Nothing to run beyond the `.\ff.bat` already on your list**; it rebuilds all three pages on these builders.

---

## 1. THE RULE, APPLIED

The same rule doc 439 applied to the week sheet: a caption states what the table is ranked on and the one instruction that
follows from it; a standing rule is one sentence with its number; history, mechanism and reassurance go. The page is
rendered offline in a harness that feeds `write_page()` the rows `WIRE_20260929.csv` holds (the lanes empty), before and
after, and the two texts are compared: 35% shorter, the set of numbers on the page unchanged except the stamp. The one
number that fell out on the first pass (the 16% landing rate on a contested man) was put back beside the 56%.

Two things on the old page were wrong, not merely long, and the trim caught them: the routine's "Tuesday night: put in
claims" (v9.26 measured the run at Thursday 03:00 to 06:00 and set the rule to Wednesday night) and "the league settings
file gives a two-day waiver period and names no day, so this page has never had a source for one" (doc 405 is the source).
Both had survived since the routine block was written (doc 372) because nothing reads a static string against the directive.
`check_page_logic.py` reads the sheet against the roster; nothing yet reads a page's standing rules against §2. That is a
guard to write and it is on my list.

## 2. OPEN, BY NAME

- **Matt's:** `.\ff.bat`; the v9.35 paste; go or no on v9.36; the claim-order runs; the routes purchase; the D/ST box
  score; the Opus chat (blocked).
- **Mine, next:** a guard that reads each page's standing-rule sentences against the directive's rules (the Tuesday-night
  line lived on the wire page for a week after the rule changed).
- **Mine, waiting on events:** the first run after doc 448; the Wednesday and 6 October runs; the status pairs from about
  20 October; the 4.34 column from week 10; wiring item 7.
