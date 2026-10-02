# 174 — Lloyd: Matt found a real inconsistency, and it is ours

**Date:** 2026-09-05 (Sat night ET) · **Trigger:** *"He's a starting RB for GB… He needs a higher
VOR. Think about it. Correct me if I'm misguided."*

**He is right about the inconsistency and wrong about the bell cow. Both matter.**

---

## 1. THE INCONSISTENCY IS IN OUR BOARD, NOT ESPN'S

| | |
|---|---|
| our board | **Josh Jacobs = 0.0** — `news_overrides.csv`, "draft as if he does not play in 2026" |
| our board | **Lloyd = ESPN's number** |
| ESPN's number was computed with | **Jacobs projected for 152.5** — about **63% of a full season** |

**We took half of ESPN's world and kept the other half.** Lloyd's 124.4 is his value *as the backup
to a Josh Jacobs who plays two thirds of the year.* We then deleted that Jacobs and left Lloyd
priced as his backup. **A −44 VOR is not defensible under our own override.** That is Matt's point
and it is correct.

## 2. HOW MUCH HIGHER — BOUNDED, NOT INVENTED

§4.20 measured that a team's RB "pie" (top-three RB projections) barely varies: **IQR 317–355 across
32 teams.** Re-checked on today's pull as a control: **median 339, IQR 317–363** — reproduces.
**Green Bay's pie is 338.1, the 45th percentile. Dead average.** So the framework applies cleanly
and the only free variable is Lloyd's *share*.

**If Jacobs plays zero and the pie holds at 338:**

| Lloyd's share of the backfield | projection | **VOR** |
|---|---|---|
| 45% | 152 | **−16** |
| 50% | 169 | **+1** |
| 55% | 186 | **+17** |
| 60% | 203 | **+34** |
| **64.5% — ESPN's own implied split among the non-Jacobs backs** | **218** | **+50** |
| 70% | 237 | **+68** |

**Every cell in that table beats −44, and the worst one beats it by 28 points.** The board is not a
little low on him; it is answering a different question.

**I am not going to pick one of those numbers.** §0.2 forbids reporting a magnitude I have not
measured, and the driver — his share — is the one thing nobody will state (see below).
**Carry the range. The centre of it is +17 to +34, i.e. roughly RB22–RB27, a startable flex.**

## 3. WHERE MATT IS MISGUIDED — the head coach says committee, on the record

`[SOURCED: Matt LaFleur via Yahoo Sports / Heavy, Sept 2026]` Asked directly about Lloyd's workload:

> **"That's to be determined; I couldn't tell you right now. So we'll see how he's feeling."**

and on what Lloyd needs to win the lead job: **"Obviously, his availability… his ability to stay out
there and make plays."** The same reporting describes a **rotation, not a bell cow**, and the
supporting facts point the same way: **Green Bay traded for Kaleb Johnson on Aug 30** — you do not
trade for a back in September if you have already decided who the workhorse is — and **Chris Brooks
took 106 carries last season.** Lloyd is also "recovering from two years of injuries," which is
exactly the thing LaFleur named as the gate.

**So "they want a bell cow replacement, not RB by committee" is contradicted by the coach.** That
does not rescue −44; it argues for the middle of the table rather than the top.

**And §4.20's own measured law applies directly here: BUY THE JOB, NEVER THE NAME.** The flag says
the job is unresolved and worth ~338 points; measured on 19 unsettled backfields, incumbent versus
challenger is a **NULL, p=0.604** — the flag has no opinion on who wins, and neither should we.
Matt is buying a 338-point job at roughly even odds of holding the biggest slice. That is a good
buy at pick 89. It is not a bell cow.

## 4. WHAT I DID NOT DO, AND WHY

**I did not inject an adjusted projection into the board.** `apply_news.py` supports `out` and
`remove` — there is no "set to X". Writing one would mean editing a pinned draft-path file at T−2
and breaking `board_audit.py`'s 1e-6 equality against the spine (docs 62/143/144). The cost of a
broken audit on Monday is far higher than the cost of carrying this on paper.

**The paper rule, alongside the Jacobs one:**

> **MarShawn Lloyd — the board's −44 prices him as Jacobs' backup, and we deleted Jacobs. His real
> range is +0 to +50 VOR. He is drawn at cell 88, the pick before yours. Take him at 89.**

The grid already shows `−90 →−44` in blue for him; that correction is ESPN's, and this doc is the
second correction on top of it, which the blue number cannot carry.

## 5. TWO SMALLER ITEMS

**The grid had no Desktop shortcut.** `sync_desk_copies` has dated `ADP_GRID.pdf` since it was
built, but `make_shortcuts.DOCS` never gained the entry — **doc 161's defect exactly**: a desk copy
that re-dates on every refresh with nothing pointing at it, which is worse than a dead link because
it fails silently. Added as **`12 - Draft board grid.url`** and re-pinned. `audit_desk.py`
cross-checks those two lists precisely for this.

**The To Do list, triaged against what is already true.** Most of it is done or superseded. Three
live items:
1. *"How is access going to work when live draft starts… without my cookies?"* — **Answered and it
   is not cookies.** Doc 136 proved ESPN's read replica publishes a draft only *after* it ends, so
   the cookie path cannot work on the night at all. The mechanism is the **browser bridge**:
   `bridge_server.py` → draft room open in Chrome with the `espn_bridge` extension →
   `py live_draft.py --bridge`. Confirmed end to end on 2026-09-02, 179 picks captured live.
2. *"Explore running `Espn_pull_projections.py` on my behalf. Can I give permission?"* — **No, and
   not for permission reasons.** This session has no shell on his machine; the remote tools read,
   write and list files only. Anything executable is his to run. Windows Task Scheduler already
   covers the recurring case.
3. *The breakout / ranker hit-rate project* — **large parts are already answered and he may not know
   it.** §4.13d: the FantasyPros accuracy contest is **structurally blind to breakout skill**
   (tidiness on ordinary players scores 2.80× perfect foresight on every breakout); the six-ranker
   panel is **one opinion measured six times** (mean pairwise r 0.81); and **disagreement predicts
   finishing worse** (−0.244, p=0.0009). The per-player, per-round data the full project needs
   **is not published by FantasyPros.** Post-draft work, and smaller than it looks.
