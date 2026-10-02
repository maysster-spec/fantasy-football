# 233 — THE BYE TRADE HAD NO TRIGGER, AND THE NUMBER I GAVE HIM WAS HALF THE REAL ONE

*2026-09-08. Matt: "we also discussed trading based on bye weeks. did that get baked in with a
trigger?"* **No. And checking turned up two defects of mine, one of them a silent regression.**

---

## 1. THE LIST

1. **A NUMBER THAT MUST NOT BE QUOTED: week 11 is not 13 points, it is 28.** I gave him ~13 this
   morning. That was the raw points of the men who are off. **The right number is what his BEST
   LEGAL NINE loses, and losing four starters at once is not four times losing one** — the bench
   cannot cover it. **Week 11 costs 28.1 points of lineup.**
2. **AND THERE IS A SECOND HOLE NOBODY HAD LOOKED AT: week 6 costs 10.7 points, from ONE man.**
   Sam LaPorta is his only tight end, so his bye empties the slot outright. It is the second worst
   week on his season and it arrives first.
3. **THE FULL SEASON, IF NOTHING IS DONE: 49.6 points of lineup.** Weeks 5, 8, 9 and 14 cost him
   nothing at all — those are the bye weeks to ASK for in a trade.
4. **SHIPPED, and it is a real trigger now, not a sentence:** `wire.py` computes the table from
   his live roster every week and raises the trade box when the next expensive week is five weeks
   out or nearer. It names who is off, what it costs, who he can afford to send, and which bye
   weeks to ask for.
5. Nothing to run.

---

## 2. THE TWO DEFECTS, BOTH MINE

**(a) IT NEVER HAD A TRIGGER — it had a sentence.** The Sept-8 morning sheet carried a hand-written
paragraph headed *"The trade that is sitting there"* naming week 11 and "about thirteen points."
Static text, hardcoded to one week and one wrong number.

**(b) AND THE SENTENCE IS GONE TOO — a silent regression.** The page was generated at 11:37. The
builder was edited at 12:23. **The current `wire.py` on the drive contains the word "trade" zero
times.** Somewhere in the day's patching the section was dropped out of the generator, the page
stopped carrying it, and **nothing anywhere said so.** This is exactly §0.5(c)5 — a thing that
SHOULD be on the page and is not — and the guard for it does not exist for this sheet.
`check_plain.py` watches the two in-season pages for doc-voice; **nothing watches them for missing
sections.** `[OPEN — a section-presence check for the weekly pages]`

## 3. WHAT THE BYE WEEKS ACTUALLY COST

**POPULATION: his 15-man roster. BASELINE: best legal nine (1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX,
1 D/ST, 1 K) from his own roster with everybody available = 117.1 points a week. COST = that,
minus the best legal nine with the week's bye men removed.**

| week | who is off | raw points off | **actual lineup cost** |
|---|---|---|---|
| **11** | Nacua, Judkins, Adams, Browns D/ST | 50.3 | **28.1** |
| **6** | LaPorta | 10.7 | **10.7** |
| 13 | Jeanty, M. Washington | 22.1 | 6.0 |
| 10 | Hurts, Dobbins | 37.9 | 4.3 |
| 9 | Dowdle, Spears | 21.5 | 0.5 |
| 5 · 8 · 14 | Worthy · Shough, Pineiro · Pickens | — | **0.0** |

`[TESTED — arithmetic on the shipped board's projections, not a simulation]`

**Read the gap between the last two columns, because it is the whole point.** Week 10 loses 37.9
raw points and costs 4.3, because the bench absorbs it. Week 6 loses 10.7 raw and costs the whole
10.7, because there is no second tight end. **Raw points off is the wrong number and it is the
number I quoted.**

**AND THE 28.1 IS AN UNDERSTATEMENT.** Browns D/ST, Pineiro and Pickens are not on the 480-row
board, so they are priced at zero. The Browns are one of the four men off in week 11, and week 14
(Pickens) shows 0.0 when it is not. **This is the board-universe gap that also let a Tyreek Hill
be invisible.** The sheet now says so on the page rather than hiding it.

**§4.11's "a bye collision costs at most 1.2 points, ever" IS NOT CONTRADICTED and must not be
cited against this.** That measured a DRAFT-DAY collision between two players on a full board. This
is an in-season count of four starters off at once on a fifteen-man roster. Different object,
different population, different answer — §0.5(a2).

## 4. WHAT SHIPPED

`bye_plan()` in `wire.py`. Every week it rebuilds the table above from his live ESPN roster and the
board, then raises the box when the next week costing 6+ points is **five weeks away or nearer**.
It prints who is off, the lineup cost, the men whose own bye falls LATER and whose position he
doubles up (so sending one opens no new hole), and the weeks that cost him nothing — the byes to
ask for. **The prose carries the one thing the rule cannot: match the value both ways, and do not
send the best man at a position unless what comes back starts in the same slot.**

**Controls run before shipping, all four fire:** an empty roster, a roster with no board rows, and
the timing — silent before the window, fires at week 1 on the week-6 hole, switches to week 11 at
week 7, silent once the last costly week has passed. **Week 13 sits at 5.99 against a 6.00 bar and
is correctly silent** — checked, because a threshold that is nearly met is exactly where a missed
trigger hides.
