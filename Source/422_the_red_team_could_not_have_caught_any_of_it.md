# 422 — the red team could not have caught any of it, and that is the actual defect

**24 Sept 2026.** Matt, after the fourth correction of the day:

> *"how are we still at the stage of 'pulling the wrong numbers'. that's what the red team process
> is meant to solve for"*

He is right, and the answer is not that the process was skipped. **It was followed. It cannot catch
this class of error.**

---

## WHY, CONCRETELY

**§0.5(c) steps 1 to 5 are internal-consistency checks. They compare a file against another file.**
Every error today passed that bar perfectly:

| the error | what the red team would have seen |
|---|---|
| **`/17` divisor** (doc 419) | nothing. Every file consistently believed `proj_2026` was a full-season total. **Perfect internal agreement on a wrong belief about an outside system.** |
| **the defense rate** (doc 421) | nothing. Every file agreed on 5.7. It was a correct number answering a question nobody asked. |
| **`not priced` read as droppable** (doc 420) | nothing. No file disagreed with anything. It is a HUMAN-READING defect and no file-vs-file check can see one. |
| **"replaced by Tre Tucker"** (doc 420) | **here two files DID disagree** — `MY_ROSTER.csv` said owned, `WIRE_*.csv` said free — **and nothing compares those two files.** |

The directive already confesses the first half: step 6 exists because steps 1 to 5 *"cannot find a
thing nobody here has thought of."* But step 6 is one batch out of many **and I choose when to run
it.**

**AND THE PART THAT ACTUALLY ANSWERS HIM: every red team this project has run was run BY me, against
files I wrote, using a catalog I chose.** Matt's record (§0.5(a2)) is the real detector here. That is
not a process. That is him doing QA on my work, which is precisely what he is objecting to.

## WHAT WOULD NOT HAVE HELPED: ANOTHER RULE

There are 43. The instruction-following literature puts that on the flat part of the curve, so the
count is not the lever — and §0.5(a6), which names the exact "right number, wrong question" failure,
**was added this morning and I committed that failure again four hours later.** A rule is something I
have to remember. **A guard is a rule that fires whether I remember or not.**

## WHAT SHIPPED: `Scripts\check_sources.py`, RUN BY `ff.bat`

It states a BELIEF about outside data in one sentence and then tries to break it.

| belief | how it breaks |
|---|---|
| **`proj_2026` is rest-of-season** | between two pulls it must fall by exactly what the man banked. A FULL-season total stays flat while the actual grows. **This is the sentence that would have caught doc 419 in week 2.** |
| **owned and free are disjoint** | a man in both `MY_ROSTER.csv` and `WIRE_*.csv` |
| **every status string is known** | ESPN sends one nobody here has reasoned about (the IR slot accepts exactly two, so a new spelling silently refuses a legal park) |
| **the roster joins the pull by id** | a rostered man absent from the pull is priced at nothing and still holds a seat (doc 281) |

**Seven controls, each reproducing the real defect it exists for, all firing.** Live on his data
right now it reports the rest-of-season belief holding on 191 players (median gap −1.8 against a
typical move of 16.8) and **fails on Tre Tucker, owned and free at once** — a real live defect that
no existing guard could see.

A belief that cannot be tested with the files on hand prints **SKIP**, not OK (§0.2: cannot check is
not the same as passed).

## AND THE SECOND HALF: `WEEKLY_VALUE`

Doc 421 removed the defense constant. That fixed one row and protected nothing else. The real
property is that **some positions are worth what they do THIS WEEK** and this page only computes
season rates, so printing one against them is a horizon mismatch — §0.5(a6)'s failure with a number
instead of a sentence.

```
WEEKLY_VALUE = {'D/ST', 'K'}
```

The drop table consults the property rather than the accident of an empty wire, so even if a free
defense appears there, a season rate for it is still refused. **The next position that behaves this
way is protected by joining a set, not by someone remembering doc 421.**

## ALSO

`defence` → `defense` throughout the page copy, at Matt's note. 56 occurrences across three files;
the JSON key set and every lookup string verified identical before and after.

## OPEN

- **[OPEN] §0.5(c) still has no step that tests an external assumption.** `check_sources.py` is that
  step for four beliefs; the catalog of beliefs this project holds about ESPN's data has never been
  written down. **NOT YET RUN**, and it is the parent of today's whole batch.
- **[OPEN]** The red team is still self-administered. The outside check (step 6) is the only
  structural answer and it fires only when I invoke it. **NOT YET RUN.**
- **[OPEN]** The weekly D/ST pool, the kicker replacement level, the draft-era board hiding 72
  available players, and the duplicated ESPN credentials, all carried from doc 421.
