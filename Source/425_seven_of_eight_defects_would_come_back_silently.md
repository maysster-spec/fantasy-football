# 425 — seven of eight defects would come back silently

**24 Sept 2026.** Matt, on the guard shipped four hours earlier:

> *"I agree with this 100%, 'I have to remember and a guard fires whether I remember or not', but
> also **the guard has to be designed correctly because those have been faulty too**, lol."*
> *"The check doesn't seem to cover all critical components else this wouldn't have been missed for
> so long. And those checks too need to be part of the catalog."*

Both true. Neither is answerable by writing more guards, because the thing being asked is **which
defects slip past the guards that exist** — and a blind spot is invisible by definition.

---

## THE OUTSIDE PRACTICE (§0.5(c)6)

**Trail of Bits, *Use mutation testing to find the bugs your tests don't catch*, 18 September 2025**
(page loaded, not a snippet). The argument: coverage measures whether code was **executed**, not
whether it was **checked for correctness**. *"100% coverage doesn't mean that all legitimate and
malicious use cases are being tested."* The real measure is *"systematically introducing bugs and
checking if your tests catch them."* Their cost advice is taken here too: group mutations by
priority rather than generating them exhaustively, or nobody runs it twice.

**Soda, *The Definitive Guide to Data Contracts*, 2 Feb 2026, updated 10 Aug 2026** (page loaded).
A contract is not a schema: it carries semantic rules and **aggregate checks that summary statistics
stay in range**, and enforcement is a checkpoint that **blocks propagation** rather than logging.
`check_sources.py` is the first half of that. The blocking half is not built.

## WHAT SHIPPED: `Scripts\check_guards.py`

Eight mutations, each re-introducing a defect this project actually shipped. For each: patch a copy
of the engine, rebuild the page, run every guard, record whether anything went red.

**IT IS BASELINE-RELATIVE, and that was the first thing it taught.** Its very first run refused to
start because `check_sources.py` was already failing on a live defect. Refusing was correct, and it
also made the harness useless exactly when the project has an open problem, which is most of the
time. So it records which guards are red BEFORE any mutation and counts a mutation as caught only
when it turns a **green** guard red.

## THE RESULT, AND IT IS THE ANSWER TO HIS QUESTION

| mutation | doc | |
|---|---|---|
| divisor back to 17 | 419 | **SURVIVED** |
| weekly positions priced on a season rate | 424 | **SURVIVED** |
| losing moves recommended | 424 | **SURVIVED** |
| blend switched off | 417 | caught, `check_vintage.py` |
| drop may empty a starting slot | 420 | **SURVIVED** |
| add paired with a drop at its own position | 417 | **SURVIVED** |
| a man replaces himself | 420 | **SURVIVED** |
| negative drop cost inflates the net | 416 | **SURVIVED** |

**SEVEN OF EIGHT.** Every one of those was found today, fixed today, and **would come back tomorrow
without a single guard going red.**

## WHY, AND IT IS ONE REASON

**`check_vintage.py` recomputes from the same engine it is checking.** Doc 418 made it "stricter" by
having it verify the page's number against `sheet_engine.rates()`. Change the divisor and the page
and the check move together, agree with each other, and both are wrong. It is an excellent
consistency check and it is structurally incapable of catching an error inside `rates()`.

That is doc 422's finding one level deeper. It is not that the red team compares our files to our
files. **It is that our guards compare our code to our code.**

## THE LAYER THAT DOES NOT EXIST

Every guard here is one of two kinds: it recomputes from the engine (so it agrees with itself), or
it checks ESPN's data (so it never sees our logic). **Nothing checks the PAGE against the LEAGUE'S
RULES, independently of the code that built it.**

That one missing guard closes five of the seven, because all five are visible in the rendered HTML
without knowing anything about how it was produced:

1. no row under THE CALL has a negative net
2. no defense or kicker appears as an add or a drop there
3. no add is paired with a drop at its own position
4. `net == worth − max(0, cost)` on every row
5. the roster still fields a legal nine after every recommended move

**NOT YET RUN**, deliberately: doc 420's lesson was that a half-finished sweep reads as coverage
(§0.5(c)2), and this is the eighth edit to the engine today.

## OPEN

- **[OPEN] `check_page_logic.py`** — the five assertions above, reading only the rendered page and
  §2's rules. Closes five of the seven blind spots. **NOT YET RUN.**
- **[OPEN]** The divisor blind spot needs a different shape: a cross-check between the semantics
  `check_sources.py` establishes and the divisor the engine applies. **NOT YET RUN.**
- **[OPEN]** Enforcement. `ff.bat` logs a broken belief and builds the page anyway. Soda's guidance
  is that a contract checkpoint blocks propagation. **NOT YET RUN.**
- **[OPEN]** The catalog Matt asked for: a component-by-component table of what exists, what can go
  wrong with it, and which check covers it, so an uncovered component is visible at a glance rather
  than discovered. **NOT YET RUN**, and it is the parent of this whole batch.
