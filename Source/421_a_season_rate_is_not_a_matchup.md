# 421 — a season rate is not a matchup, and his Chiefs are the best defence in the league

**24 Sept 2026, four hours after doc 420 shipped the thing this retracts.**

Matt sent one screenshot: `ESPN Week 3 Defense Projections.jpg`.

| | ESPN week 3 PROJ | |
|---|---|---|
| Eagles | 7.8 | owned |
| **Chiefs** | **7.8** | **his** |
| Seahawks | 7.6 | owned |
| 49ers | 7.3 | owned |
| Lions | 6.9 | owned |
| **Giants** | **6.8** | **free** |
| Vikings · Steelers · Panthers | 6.8 / 6.7 / 6.7 | owned |
| **Saints** | **6.4** | **free** |
| Texans · Jaguars | 6.1 / 6.0 | owned |
| **Bengals** | **5.9** | **his** |

**His Chiefs are tied for the best defence in the league this week.** Doc 420 priced them at **5.7**,
called them below replacement, and annotated the row *"the replacement is better: this is an upgrade,
not a cost."* Then THE CALL offered them as the drop against Dalton Schultz.

---

## WHAT WENT WRONG, AND IT IS §0.5(a6) ON THE FIRST PAGE

**5.7 and 7.8 are different objects.** 5.7 is a season-long per-game rate: a blend of ESPN's
rest-of-season projection and what the Chiefs have averaged so far. 7.8 is **this week, at Miami**.

For a running back those two are close enough to argue about. For a defence they are barely related,
and **this project had already measured that**: §4.33, *at D/ST take the schedule, elsewhere the
player*. A season average answers "is this a good defence to roster all year." The question on the
page is "should I drop him now." Different questions, different answers, and **the wrong one is not a
partial answer, it is a wasted one.**

## AND THE BAR WAS WRONG TOO, WHICH IS THE PART I WOULD HAVE DEFENDED

I used **5.99**, D/ST12's season average (doc 265, n=2,576, five seasons). That number is fine for
what it measures. It is the wrong bar for this decision.

**The bar for dropping a defence is the best defence actually FREE that week.** In his pool that is
the Giants at 6.8, with the Saints at 6.4 behind them. Against that bar:

- **Chiefs 7.8 — the best thing available to anybody. Never drop.**
- **Bengals 5.9 — about a point light.** A real, small, one-week upgrade, and nothing like "both are
  at or below what you can stream," which is what I told him.

## WHY THE PAGE COULD NOT SEE ANY OF IT

**§4.8 and §4.9 keep K and D/ST off the wire on purpose.** That is right for a draft board and wrong
in week 3. The page does not know the Giants and Saints are sitting there free, which is exactly why
doc 420 reached for a constant: the pool was missing and a constant was the nearest thing to hand.

**That is the whole lesson. The blank made him ask. My number would not have.** Doc 420's own
sentence was *"rejecting a wrong number is not the same as supplying a right one"* — and then it
supplied a wrong one, four hours later, in the same file.

> **When the input is missing, NAME THE GAP. Do not reach for the nearest constant and call it a
> price.** A blank is an honest defect that invites a question. A confident wrong number is a defect
> that closes it.

## WHAT SHIPPED

`STREAMED` is gone. Both rows now name the gap and point at where the answer lives:

> **Chiefs D/ST** — *a defence is worth its MATCHUP, not its season average, and this page cannot see
> which defences are free this week — check ESPN's weekly D/ST projections before you move one*

THE CALL is back to three skill-position moves and offers no defence at all. Doc 420's other three
fixes stand: the kicker row names its gap, the ladder will not empty a required starting slot, and
nobody is replaced by himself.

## OPEN

- **[OPEN] Get the weekly D/ST pool onto the page.** It is the single highest-value in-season gap
  left: the decision is weekly and matchup-driven, ESPN publishes exactly the number needed, and the
  page currently cannot see it. `wire.py` already reaches the endpoint that carries it; the exclusion
  is a filter written for the draft. **NOT YET RUN.**
- **[OPEN] Measure K12 the way D/ST12 was measured in doc 265.** §2 carries this league's kicker
  scoring and five seasons exist. Until then the kicker row stays honest rather than numbered. **NOT
  YET RUN.**
- **[OPEN]** §4.8 and §4.9 are draft-era findings now load-bearing in season. Both should be re-read
  with a season scope rather than inherited. **NOT YET RUN.**
