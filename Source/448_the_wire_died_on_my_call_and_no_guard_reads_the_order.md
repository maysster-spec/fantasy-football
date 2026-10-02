# 448. THE WIRE DIED ON MY CALL AT 20:06, NO GUARD READS THE ORDER A FUNCTION RUNS IN, AND ONE DOES NOW

*29 Sept 2026, 21:20 ET. Claude (Cowork). Found while staging the three pages for the doc 439 trim: `MY_TODO.html` carried a
20:06 stamp and the week sheet did not. 448 reserved by listing `Source\` (no doc has landed since 447). No em dashes.*

---

## 0. WHAT TO DO

1. **Run `.\ff.bat` when you can.** Your 20:06 run died in the wire on my defect, so the wire page and the week sheet on
   the drive are the 18:16 ones, and the online copy republished the 18:16 page under a fresh stamp. The fix is on the
   drive; this run rebuilds both on the new engine. Expect `wire 0` and a new term, `locals 0`, on the RESULT line. It is
   on your list.
2. **The defect, mine**: the status-pair logging call added at doc 445 read `week` fourteen lines above the line in
   `main()` that assigns it. The function had a unit test and passed it; `main()` needs ESPN and was never walked. That
   is 0.2's rule broken in the plainest way and it is in `METHOD_TRAPS.md` now.
3. **The guard, `check_locals.py`**: for every function in every shipped script, a local whose first read comes before
   its first write, in evaluation order, is reported with both lines. It fired on the file that died (`week`, line 2291
   read, line 2301 assigned) and on nothing else in 21 scripts; the selftest fires on the defect's shape and stays quiet
   on a correct function with a loop, a lambda, a nested def, a try, a with and comprehensions. `ff.bat` runs it after
   the kit check; pinned from birth.
4. **Nothing else changed.** `wire.py`'s week read moved above lane 2 (one line); `wire.py` and `ff.bat` re-pinned.

---

## 1. WHAT HAPPENED

The 20:06 log: form, snaps, depth, lines, inherit all 0; the wire's usage and depth blocks printed; then
`UnboundLocalError: cannot access local variable 'week' where it is not associated with a value` at the new call;
`wire 1`. The to-do page, the threads, the online copy and the commands page all built after it, each with exit 0, and
`make_online.py` printed `written` beside a page whose build stamp it read as 18:16. Every check in the tree was green,
because every check reads what a script writes and none reads the order a script runs in.

Why the test missed it: `log_status_pairs()` was tested by calling it with three synthetic rows, which is a test of the
function and not of the line that calls it. `main()` cannot run here (ESPN, cookies), so the call path was never walked,
and the only thing that could have caught it before Matt did was a read of `main()` in order. That read is now a script.

## 2. THE GUARD

`check_locals.py` parses each file, and for each function walks its body in evaluation order (an assignment's value
before its target; a comprehension's first iterable in the enclosing scope, the rest skipped; nested functions, lambdas
and classes skipped as later scopes; except-as, with-as and import binds merged in by line), records the first read and
first write of every name the function assigns, and reports a read that comes first. Two false positives were found and
removed before it shipped: an `except SystemExit as e` bound later than a `for e in` (the extra binds were merged by
line), and a walrus in the test of a conditional expression that runs before the body on the line above it (order is
evaluation order, not line order). Standard library only; the same on 3.11 and 3.12; exit 1 on a hit, 2 on a file that
does not parse.

## 3. OPEN, BY NAME

- **Matt's:** `.\ff.bat` now; the v9.35 paste; go or no on v9.36; the claim-order runs; the routes purchase; the D/ST box
  score; the Opus chat (blocked).
- **Mine, next:** the page trim (doc 439), which is where this was found.
- **Mine, waiting on events:** the first run after this fix (wire 0, locals 0, a sheet on the new engine); the
  Wednesday and 6 October runs; the status pairs from about 20 October; the 4.34 column from week 10; wiring item 7.
