# 354. THE FILTER ASKED WHOSE STARTER IT WAS, WHEN THE QUESTION WAS WHETHER THE BACKUP COULD PLAY

*18 Sept 2026. Matt, on a page built after the fix was supposed to be in: "Dylan Sampson is still
at the top of the seat list."*

## 1. HE WAS RIGHT, AND THE FILTER THAT WAS BUILT TO DROP HIM RAN AND LET HIM THROUGH

Doc 347 added the seat filter yesterday: a seat holder who is rostered in this league, or carrying
OUT / INJURY RESERVE / SUSPENSION / PUP / NOT ACTIVE, leaves the table and is named in a footnote.
Sampson is on injured reserve. He led the list anyway, for a full day.

**The check sat inside `if not yours:`.**

```
hp = roster_match(roster, r['holds_the_job'], r['team'])
yours = hp is not None
if not yours:                      # <-- the defect
    ... free-pool lookup, GONE_FOR_WEEKS test, drop ...
```

`yours` is true when the man ahead is on **Matt's own roster**. **Sampson is behind Quinshon
Judkins, who is Matt's.** So the row took the `yours` branch and skipped the availability test
entirely.

## 2. IT IS THE OBJECT ERROR, INSIDE A FILTER

Whether the STARTER belongs to Matt has nothing to do with whether the BACKUP can be claimed or is
playing. Two different men, two different questions, and the code answered the second by testing
the first. That is 0.5(a2) in four lines of Python rather than in a study.

`yours` has exactly one legitimate job in that loop and it is three lines further down:
`b = alt.get(hp['name'], bar) if hp else bar`, which picks the alternative bar for pricing. It
should never have gated anything else.

**FIXED:** the lookup and the `GONE_FOR_WEEKS` test run on every row. Dropped rows are still
counted and named under the table, never silently removed.

## 3. WHY THE HARNESS MISSED IT, AND WHAT THAT SAYS

C24, written yesterday for exactly this filter, plants injured reserve on a live seat holder and
asserts the row leaves the table. **It passed.** It plants the status on **Tank Bigsby**, whose man
ahead is not on Matt's roster, so the control only ever exercised the `not yours` branch. **The
branch that contained the defect had no control at all** , doc 340's finding, in a new place, four
days later.

**NOT YET RUN, with the form written: C24 needs a second case that plants the same status on a
seat holder whose man ahead IS on Matt's roster, and it must be shown failing against the old
code before it ships.** The inputs are all present; this is the next thing on the harness.

## 4. THE PATTERN WORTH KEEPING

Three defects in two days, same shape: doc 345's cap ate the row the page was shouting about,
doc 347's filter let three non-seats through, and this one. **All three were a correct rule applied
to the wrong population.** The rule is never the thing to check first; the rows it runs on are.
