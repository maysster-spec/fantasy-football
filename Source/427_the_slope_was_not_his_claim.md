# 427 — The slope was not his claim, and two defects that shipped against the wrong object

> **BANNER, 28 Sept 2026 (doc 435), reproduced cold.** Every number reproduces from `qb_matchup.py`. **One thing the doc does not say: the generosity it uses is a leave-one-out mean over ALL of weeks 1 to 14, so the "softest matchup" rule as measured used games not yet played.** With prior weeks only, which is what Matt can see on Wednesday, the gain is +1.75 to +2.01 a week (se 0.88, n=65 to 70). The decision survives; quote the ex-ante number on a page.

*25 Sept 2026. Directive v9.30. Three things, and Matt caught all three.*

---

## 1. §0.5 GAINS (a7): a decision claim is tested by the decision

His words: *"I need to play matchups when I'm streaming QB because I'm not going to have a stud that
can put up points regularly no matter the matchup."*

**That is a claim about which lever he has.** A stud starts every week and there is nothing to
choose; a streamer must be chosen, and choosing needs next week's opponents before next week.

I turned it into a **slope** comparison instead: does opponent generosity move a streamable QB's
points more than an elite one's. Population 2,078 QB starts, nflverse REG weeks 1-14 2021-2025,
scored under §2, leave-one-out opponent generosity centred within season, tiers 1-6 and 13-24.

| tier | n | pts/wk | slope | se | t |
|---|---|---|---|---|---|
| elite | 359 | 26.09 | 0.448 | 0.159 | 2.83 |
| streamable | 685 | 18.40 | 0.216 | 0.097 | 2.22 |

**Difference −0.232, se 0.186, t = −1.25.** Null, and the point estimate runs backwards: the better
quarterback exploits a soft defence harder. `[TESTED]`

**And I opened the reply with "not for the reason you gave."** He never said that sentence. **The
number that confirmed him was in the same run:** among streamable QBs in a week with three or more
options, taking the softest matchup returns **20.36 a week against 18.43 at random, +1.93, se 0.90,
t = +2.14**, 70 season-weeks. `[TESTED]` His claim, confirmed, buried under a null to a question
nobody asked.

**THE RULE, now §0.5(a7): does the thing I am about to measure CHANGE WHAT HE WOULD DO? If not, it
is not his claim, whatever vocabulary it shares.** And the tone half, which is (a5)'s mirror: a null
against a form I invented is evidence about my form, never about his judgement.

His reply: *"I don't have time to write these long descriptions you do, so I'm sure something was
lost in my short form."* §0.5(a) already said read through to intent and never challenge the
expression. Short wording is not a defect.

---

## 2. The `form_2026` join used a raw name lookup

`rates()` did `_season.get(r[namecol])`. `norm_name` has existed for this since doc 58 and that call
site never used it. Nine men fell back to a preseason projection carrying a vintage of `proj`, which
reads as deliberate:

| page name | form name | measured/g | printed | correct |
|---|---|---|---|---|
| **Kyle Pitts Sr.** | Kyle Pitts | 1.0 over 2 | **7.89** | **5.41** |
| Travis Etienne Jr. | Travis Etienne | 7.7 | 10.50 | 9.49 |
| Tre' Harris | Tre Harris | 4.65 | 6.04 | 5.54 |
| Michael Pittman Jr. | Michael Pittman | 7.3 | 8.63 | 8.15 |
| James Cook III | James Cook | 14.4 | 15.70 | 15.23 |
| Oronde Gadsden | Oronde Gadsden II | 6.5 | 5.79 | 6.05 |

All suffix or apostrophe, which is §3's own example list. **Pitts was the page's top cover for the
week-6 tight end bye at 7.89.** With the fix the calendar row reads **Pat Freiermuth 7.3**.

---

## 3. A seat is void when the backup has left the job's team

`inherit_2026.csv` had **Emari Demercado** behind **Kenneth Walker III** on Kansas City. He is on
**Dallas** — the wire, `form_2026` and the engine's own rate dict all say so. The seat table printed
**"Demercado KC · bye 5"**, which is Walker's team and Walker's bye, gave him 51% of a 248.9 job he
cannot inherit, and THE CALL promoted the 4.5 into a claim against dropping Devaughn Vele at 8.6.
His real rate is 2.66 on 12% of snaps.

**Doc 411 checked whether the STARTER had gone. Nobody checked whether the BACKUP had.** The new gate
cuts exactly 1 of the 10 live seat rows.

---

## 4. THE PART THAT MATTERS MOST: both fixes shipped once against the wrong object

**The seat guard read `team`. Free rows spell it `tm`** — `wire.py` builds each one as
`dict(rate[pid])`. Every lookup returned None, the comparison was never true, **and the filter did
not fire a single time.** I verified it against the WIRE CSV, which does spell it `team`.

**That is doc 80 word for word: a test must exercise the object PRODUCTION builds.** The project has
had that rule since August and I walked into it and reported the work done. Matt: *"doesn't appear
you fixed Demercado. You need to check your work before you finish the run."*

The real check was one line: `has 'team'? False | has 'tm'? True`.

**A key contract is now asserted in `render()`** — free rows must carry `name/pos/tm/wk/bye` or it
raises — **and its negative control was run**, handing it rows shaped the way the broken fix assumed.
It fires on `tm`. A guard that has never been seen to fail is not a guard (§0.2).

## ASSUMPTIONS

1. The nine join misses are the complete set on today's wire. Re-measured after the fix: zero
   RB/WR/TE carry vintage `proj` while a measured rate exists under `norm_name`.
2. The seat gate compares live team to the job's team via `team_key()`, so ARZ/ARI and WAS/WSH do
   not register as moves. Verified: 3 rows differ on the raw string, 1 on the normalised one.
