# 280 — The lock rule, the window, and three numbers that were measuring a mechanic

Matt, 2026-09-10, on doc 278/279's timing argument:

> *"most FA are locked by game time on or after Sunday… The window for FA is right after waivers
> run and players are added to rosters. Players dropped however are not open until next waiver
> period. This is a good way to block your opponent if they need the player you are dropping. The
> common scenario is that a player is reported injured after waivers clear and before their game
> time starts."*

**Every one of those is right, and two of them mean my headline numbers were measuring the
league's rules rather than the room's behaviour.** The Sunday task has been moved from 7:30pm to
**11:40am** because of it.

---

## 1. The lock rule — and it kills my most-quoted figure

`2026_League_Settings.txt`, line 122: **`Lineup Changes: Lock individually at Scheduled Gametime`.**

So a player cannot be added once his own game has kicked off. **Doc 278's "only 5.8% of free-agent
adds ever happen during a live game window" was therefore never a measurement of reluctance — it
was very close to a measurement of a rule.** The residue is players on later kickoffs: the 4:05 and
4:25 teams while the 1pm games are running, Sunday night, and Monday.

**RETRACTED, and it must not be quoted again in any form.** It was the load-bearing number under
doc 278's whole "nobody races" argument, and it could not have carried that weight.

---

## 2. The free-agency window OPENS when the waiver run clears — which is what my Thursday spike was

**POPULATION: every EXECUTED add in this league 2022–2025 carrying a timestamp; 616 free agency,
614 waivers.**

**THE RUN FIRES THURSDAY 03:00–05:00 ET, all four seasons** — 279 executed claims at 03h, 227 at
04h, 23 at 05h. `[TESTED]` *(Matt says "Wednesday"; the file's processing stamp is early Thursday.
Same event, different clock — a claim filed Wednesday settles overnight. Worth pinning only because
the task time depends on it.)*

**And then the pool opens.** Free-agent adds by hour, Thursday:

| Thursday | n |
|---|---|
| before 06:00 | 22 |
| **06:00–11:59** | **148** |
| 12:00 onward | 124 |

The two single busiest hours of the entire week for free agency are **Thursday 07:00 (40) and
Thursday 06:00 (36)** — the two hours immediately after the batch clears.

**SO DOC 279'S READING OF THAT SPIKE WAS WRONG.** I wrote that 48% of free-agent adds landing on
Thursday showed a room that only looks once a week. **It shows a room arriving the moment the pool
becomes available.** Everyone unclaimed in the batch hits free agency at once, and Thursday morning
is the scramble. That is a mechanic, not a habit, and reading it as sloth is the same error as the
5.8%.

**THE SECOND WINDOW IS SUNDAY MORNING AND IT IS EXACTLY THE ONE HE DESCRIBED.** The busiest Sunday
hours are **12:00 (38 adds)** and **11:00 (23)**, with 08:00–09:00 adding 29 more. That is the
pre-kickoff scramble: inactive lists are final **90 minutes before kickoff**
`[SOURCED: legionreport.com, 26 Aug 2026]`, so for the 1pm games the news lands at 11:30 and the
door shuts at 1:00.

---

## 3. What that does to the Sunday task — it was aimed at the wrong hour

**The 7:30pm slot was the worst possible moment**, and his mechanic is why: by Sunday evening every
player who played is locked, and an injury from those games becomes a **Thursday waiver claim
settled on priority**, where being early buys exactly nothing.

**MOVED TO SUNDAY 11:40am ET.** Inactives for the 1pm slate are out; those players lock at 1:00.
The task now reads the inactive list against the fourteen claimable backfields and Matt's own
roster, and **prints each man's kickoff time next to his name**, because "is he still addable" is
the whole question and it has a different answer for a 1pm team than a 4:25 team.

Its brief also now states the thing that makes it worth running at all: **the only window in the
week where speed decides an outcome is a starter ruled out while his backup is unowned and his game
has not kicked off.**

---

## 4. The drop rule, and a weapon this project had never recorded

`Waiver Period: 2 Days` (settings, line 125). **A dropped player does not hit free agency — he goes
onto waivers**, so a rival who wants him must file a claim and win it on priority.

Checked on his own file: **419 dropped players who were later re-added. Only 2% came back inside 24
hours; 83% took more than 72.** `[TESTED]` Consistent with a real waiting period on every drop.

**AND THE STRATEGIC POINT IS HIS, NOT MINE, AND IT IS NEW HERE:** *"This is a good way to block your
opponent if they need the player you are dropping."* Dropping a man a rival needs does not hand him
over — it puts him behind a two-day claim that anyone with better priority can take first. **No doc
in this project has ever priced the drop as anything but a cost.** It is also a tool.
**NOT YET RUN, and the testable form is written down: among his 1,230 executed adds, does a drop
made by one manager get claimed by a rival more often when that rival had a hole at the position?
`waiver_report_*.csv` carries both sides.**

---

## 5. The honest scorecard on my last two docs

| claim | verdict |
|---|---|
| "5.8% of adds happen in a live game window, so nobody races" | **RETRACTED.** Measuring the lock rule, not behaviour |
| "48% of free-agent adds on Thursday shows a slow room" | **RETRACTED.** Thursday is when the pool opens |
| the per-add null: early 10.5% vs Thursday 11.2%, p=0.66 | **WEAKENED, §0.6.** Those are two different pools — Thursday is the fresh post-waiver crop, off-Thursday is the residue plus never-rostered players. The comparison was never like-for-like |
| doc 279's volume finding — Taylor 89 adds at 10.1%, Matt 23 at 17.4% | **STANDS.** It has no timing term in it |

**THE PATTERN ACROSS ALL THREE RETRACTIONS IS ONE THING: I read a distribution shaped by the rules
as a distribution shaped by choices.** §0.6 says to ask what is *not* in the data before defending a
number. The rule here is stronger than that — **ask what the data was ALLOWED to contain.** A
transaction file records only legal transactions, so any hour where a move is impossible reads as an
hour where nobody wanted to move.

**Matt caught all three from the outside, by knowing the rules of his own league.** That is the
fourth time (§0.5's record) that a process he says is wrong turned out to be wrong.
