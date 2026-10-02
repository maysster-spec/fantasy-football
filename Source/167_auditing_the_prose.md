# 167 — Stribling's shoulder, and a checker for the prose on the board

**2026-09-05.** Matt asked two things: how bad is Stribling's hamstring, and can we fact-check the
board and keep it current. The second turned into a tool, because the answer to "check it by hand"
is no — there are 144 cards inside the drafted range and two contaminations have now been found by
eye, one of them **by Matt, reading his own board.**

---

## 1. STRIBLING — **the hamstring is not the issue, and the shoulder is minor** `[SOURCED]`

The card said *"Hamstring and shoulder | (2026-08-31) | Dealing with both hamstring and shoulder
injuries."* That reads as one player carrying two live problems. The timeline says otherwise:

| when | what |
|---|---|
| early Aug | **hamstring tightness**, missed practice |
| **Aug 6** | **back at practice.** Hamstring not mentioned again |
| ~Aug 20 | **shoulder**, in the preseason game vs the Chargers |
| — | watched practice with the other receivers. *"Doesn't seem to need surgery or anything drastic"* |
| **Aug 23** | **practiced, in a non-contact jersey** |
| late Aug | held out of the preseason finale — precaution, *"he has shown enough"* |
| **Sept 3** | **not on the league-wide injury tracker at all** |

**So: one old resolved soft-tissue issue and one minor shoulder he practiced through twelve days
ago.** And the detail that matters more than either — before the shoulder he had **leapfrogged
Deebo Samuel on the depth chart and was in the starting lineup.** The board calls him "direct
backup (WR2)"; the reporting has him ahead of that, and Pearsall is out for the season.

**CARD CORRECTED**, dated 09-05, with the timeline and the depth-chart note. **Grade left at
DISCOUNT** — the grade comes from the injury sweep's own rubric and I am not overriding a scored
judgement on my own reading (§0.2). Facts fixed, score untouched.

---

## 2. "MAKE IT CURRENT" HAS A HARD CEILING, AND IT IS WORTH KNOWING

I pulled the **official NFL Week 1 injury report**. It says **"No Injuries Reported" for all
sixteen games.** That is not a bug — **official practice reports do not publish until game week**,
and Week 1's first ones land Wednesday Sept 9. **Matt drafts Monday Sept 7.**

**There will be no authoritative injury report before this draft.** Everything available is beat
reporting and practice observation — which is exactly what the 08-31 sweep and the Gemini pass
used. So the board is not five days behind an official source; it is five days behind *the beat*,
and the only thing that closes the gap is Friday-through-Sunday practice notes.

That reframes the job: **not "verify the board", but "re-read the beat on the twenty names that
can actually cost a pick, on Sunday."**

---

## 3. `context_audit.py` — NOTHING WAS CHECKING THE PROSE

`board_audit.py` checks the arithmetic. `audit_directive.py` checks the directive. `check_kit.py`
checks the bytes. **Nothing checked the words** — and the words are what gets read at 60 seconds a
pick. Two contaminations, both found by eye:

- **Kenneth Walker III** — ankle claim sourced to an article about **Kenyon Sadiq**. Caught by an
  earlier session and annotated in the card itself.
- **Puka Nacua** — carried **Jordan Addison's** DUI discipline, from an aggregator page titled
  *"is Puka Nacua suspended NFL week 1"* — a question read as a finding. **Caught by Matt.**

One caught by the user is one too many. Four mechanical checks, reported **by the pick they
affect**:

1. **STALE** — a judgement whose newest date is older than `--days` (default 4).
2. **UNDATED** — a judgement with no date at all.
3. **CROSS-NAME** — the card names a different player on the board. Usually innocent, but it is
   the exact shape of both contaminations, so it is listed for the eye, never auto-failed. Badge
   vocabulary (Dart, Love, Brown, Jones…) is excluded or every DART card would fire.
4. **RISK CLAIM** — suspension / discipline / arrest / legal / exempt. doc 166's rule applies:
   **two independent primary reports, and a headline phrased as a question is not one of them.**

**First run: 39 of 144 cards inside adp<168 raise something.** The ones worth Matt's eye:

| pick | player | flag |
|---|---|---|
| 41 | **Emeka Egbuka** | **STALE 18d** — by far the oldest, and he is live at 41 |
| 80 | **Sam LaPorta** | **STALE 16d** |
| 56 | **Quinshon Judkins** | **UNDATED** — a DISCOUNT with no date anywhere on it |
| 32 | Kenneth Walker III | names Sadiq — the known mismatch, surfaced automatically |
| 65 | **Josh Jacobs** | RISK CLAIM — **verified, see below** |
| 8–128 | 30 more | STALE 5d, which is the whole 08-31 sweep |

**Negative control, run first:** before the doc-166 fix the audit flagged Nacua as a RISK CLAIM;
after it, he is gone from the list and Jacobs is the only one left. The check fires on the defect
it was built for and stops firing when it is fixed.

## 4. JOSH JACOBS — **verified under the new rule, board is right**
Commissioner's Exempt List, Aug 31, after an offseason domestic-abuse arrest. Reported by
**NFL.com itself, ESPN, Yahoo and Spectrum News** — four independent primary reports against a
rule that asks for two. **The AVOID and the zeroed projection are correct. Do not draft him.**

---

## 5. THE PLAN FOR THE WEEKEND

1. **Today (Sept 5):** the refresh — `refresh_pull.bat`, then `02 - Saturday refresh`. That moves
   ADP, not news.
2. **Sunday:** one beat sweep, scoped to the audit's list — **Egbuka and LaPorta first** (18 and 16
   days old), then Judkins (undated), then the ten DISCOUNTs live at picks 8–65. Three batches of
   ~12 per doc 166 §5, one line each, fact + URL + date.
3. **Monday before the lock:** `py context_audit.py` once more. Anything still STALE by then is
   STALE for the draft, and that is a known-unknown rather than a surprise.
