# 349. THE SEAT LIST RIDES AT THE TOP, AND EACH ROW SAYS WHAT THE MAN ACTUALLY DOES

*18 Sept 2026. Matt: "i'm still confused as to why the seat is so far down the page. I've asked for
at least the 3rd time now for it to be promoted and incorporated with the Priority pickups," and
then, on the rows themselves: "that same section should absolutely and always include the other
indicators, pedigree, running style, talent and the latest buzz."*

## 1. IT WAS ALREADY MERGED, AND THAT IS WHY I KEPT SAYING IT WAS DONE

The seats were in the Priority pickups list. They were also below a **five-row cap** that doc 316
put there, so they were sorted into a list that never printed them. **Merged and invisible is not
merged**, and three answers in a row said "it is in the pickups" because the code said so.

## 2. WHAT CHANGED IN `sheet_engine.py`

- **Page order.** Section 0 is now Priority pickups, then **THE SEAT LIST**, then the calendar. The
  bar moved from section 1 to section 2, below the priced free pool, because Matt reads for the
  names first and the bar second.
- **The heading is `THE SEAT LIST, a job you do not have yet`**, one name he and the page both use,
  so a reference in chat and a reference on paper mean the same block.
- **Doc 316's cap exception was restored.** It had silently vanished for two days: any man whose own
  line says "Put him first" is re-admitted above the cap. The re-admit keys on the SENTENCE, not on
  the 0.38 threshold, so `contest()` stays the single decision point.
- **Three rows that are not seats are now cut, with the reason printed.** A seat holder rostered in
  this league, or carrying OUT / IR / SUSPENSION / PUP / NOT ACTIVE, leaves the table and appears in
  a `Left off, and why` footnote. Dylan Sampson was the top row while on injured reserve.

## 3. THE INDICATORS, PRINTED AND NEVER SCORED

Each row now carries: **what he actually does** (carries against catches, and the role that implies,
`runs it` / `catches it` / `does both` / `barely used`), **his snap share**, **his NFL round, pick
and year**, and **the latest note** from the form or screen files.

**PRINTED, NOT SCORED, and that is deliberate.** None of it moves the odds or the sort. Matt's
mechanism is that a specialist's role does not expand when the man ahead goes down while an
all-purpose back's does. **That is a real claim and it is NOT YET RUN**; its testable form is
written into the Fable JOB 3 prompt. Until it has a number it is description, and the page says so.

## 4. WHAT IS STILL OPEN

- `share_2026()` joins on the name alone, so one live row is priced off another club's backfield
  (ledger 108).
- A seat holder with no week-one line should lose the row to a teammate who has one (Giddens against
  McGowan). No guard yet.
- The contest sentence still quotes the old claimant's-seat rate.
