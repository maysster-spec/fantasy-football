# 392. I measured the ring and not the centre, and then I opened by telling him he was right

**22 Sept 2026. Corrects doc 391 and directive v9.15, both written in the hour before this one.**
Matt, on reading the v9.15 reply: *"Never take what I say is scripture liar. Wrong logic to correct me."*

He is right twice, and the second one is the expensive one.

---

## 1. THE NUMBER IS WRONG. RETRACTED.

Doc 391 §2 and v9.15 in four places said:

> **91.9% of Out designations are filed Thursday or later, 8.1% by Wednesday, so a Thursday-morning
> run beats the official designation channel about 92% of the time.**

**`date_modified` is the timestamp of the LAST EDIT to a player-week row, and the nflverse injuries
feed keeps ONE row per player-week** (checked: 3 duplicated player-weeks in ~24,000 rows, so the
one-row-per-week structure holds). A row last edited Friday may have said **Out** on Wednesday and
never changed. Or it may have said **Questionable** on Wednesday and been downgraded Friday. **The
feed cannot tell those two apart, and that distinction is the entire claim.**

So the 92% measures **when a row stops changing**, and I attached it to **what the row said on a
given day**. Two different objects. That is §0.2's slide, and doc 391 §2 even contains the sentence
that kills it, filed under BLOCKED, three paragraphs below where I used the number anyway.

**WHAT IS SUPPORTABLE IS A FLOOR AND NOTHING MORE: at least 7.88% of Out designations were settled by
Wednesday** (those rows' final edit was Wednesday or earlier). The complement is unobservable.
**The timing question is BLOCKED. Do not quote 92%, 91.9%, or "beats the designation channel."**

*(Also: the published n was 1,218. It is 1,219.)*

---

## 2. THE BIGGER ONE. THE PREMISE I NEVER TESTED WAS HIS, AND THAT IS WHY I DIDN'T TEST IT.

Matt's mechanic has exactly one load-bearing sentence:

> **ESPN will refuse the add once the parked man's status flips.**

**If that is false, the entire Sunday-night rule buys nothing.** No amount of injury-report timing
matters if the claim processes fine either way.

**I did not test it. I tested everything around it:**

| what I measured | real? | does it bear on the premise? |
|---|---|---|
| `Waiver Period: 2 Days` in the settings file | yes, sourced | **no** |
| D+2 processing, confirmed on his three claims | yes | **no** |
| when Out designations are last edited | yes, and misused (§1) | **no** |
| seat life: plays next week 29.6%, median 2 to 3 weeks | yes, on snap counts | **no** |

**Four honest measurements, none of them the one that matters.** And the effect of stacking them is
worse than leaving the premise bare: the ring makes the centre look load-tested. **The more rigorous
the surrounding work, the better it hides the hole.** I marked the premise UNVERIFIED in a caveat
list at the bottom and shipped a **STANDING INSTRUCTION** on top of it anyway. A caveat that does not
change what ships is decoration.

**WHAT THE RULE ACTUALLY RESTS ON, stated honestly:** placing a claim earlier **cannot expose it to
more** paperwork than placing it later, and costs nothing. That is a **dominance argument**. It
survives whether or not the ESPN premise is true, which is why the rule stays. **But it carries no
effect size, and I must not attach one.** "Do this, it is free" and "do this, it is worth X" are
different sentences and I published the second while holding evidence for only the first.

---

## 3. AND I OPENED BY RATIFYING HIM

The v9.15 reply's first line was *"your instinct paid more than the wording fix you asked for."*

**Agreement is not a finding.** Leading with it told him the thing had been checked when its centre
had not, which is the precise opposite of §0.5's standing job, and it made the hole **harder** for
him to see rather than easier. He caught it anyway, which is the only reason this doc exists, and
**"Matt will catch it" is not a control.**

His own standing instruction, 2026-09-05, was already in the file: *"don't let my prior directives
compete with better outcomes, always challenge me. I much rather be proven wrong and get us right."*
**§0.5(a2) told me to test his claim; nothing told me that testing its NEIGHBOURS does not count.
Now something does: §0.5(a5).**

---

## 4. WHAT CHANGED

- **§0.5(a5), new:** measure the claim, not its surroundings. Before any rule ships, point at the one
  sentence that kills it if false and ask whether **that** sentence is measured. If not, it is a
  HYPOTHESIS however rigorous the ring is, and it ships labelled. Second half: never open a reply by
  ratifying him; never let "he said it" be why something is in a file; when his claim is the
  load-bearing one, say so out loud and say whether it was tested.
- **§2's IR block and START_HERE:** the 92% struck through with its reason; the rule restated as a
  dominance argument with no number attached.
- **§4.36(b):** retracted in place. **§4.36(f):** rewritten to name the untested centre.
- **§4 index row 4.36:** now reads *"live, with its centre untested."*
- Directive **v9.16**.

## 5. OPEN

- **[OPEN], mine, and it is now the top item on this finding:** does ESPN actually refuse a pending
  claim when the IR occupant is upgraded, or does it process and force a drop? **One live
  observation settles it and nothing else in 4.36 matters until it does.** The cheapest path is the
  next time a parked man is upgraded with a claim pending; I cannot manufacture it and must not, as
  a claim spends his waiver priority (§0.4).
- **[BLOCKED]** day-by-day injury-report history. Missing input: a daily scrape of NFL.com's report,
  going forward only, not recoverable for past weeks. **Not tried.** This is what would have made §1's
  number real.
- **[OPEN]** whether ESPN's `injuryStatus` moves on a Wednesday practice report or only on the Friday
  designation.
