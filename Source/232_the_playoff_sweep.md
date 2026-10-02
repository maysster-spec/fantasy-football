# 232 — THE SECOND WAIVER SWEEP: THE PLAYOFFS, AND THE WEEK NOBODY CHECKED

*2026-09-08. Matt: "did you uncover any other waiver wire strategies? not just week-to-week but for
playoffs and important matchups later in the season… if you use techniques we covered as keywords
you'll turn up other people discussing waivers."*
*Scoped his way again. Two measured findings, one correction to an earlier "no literature" verdict,
and an honest note on what the published playoff material actually is.*

---

## 1. THE LIST

1. **THE RESTING-STARTERS PANIC MISSES US BY ONE WEEK, AND THAT IS WORTH KNOWING BEFORE DECEMBER.**
   Every published week-17 waiver column leads on NFL teams resting starters. **Our championship is
   NFL week 17 and the cliff is in week 18.** Share of genuinely startable players who gave you
   nothing at all: **week 16 14.3% · week 17 19.3% · week 18 27.6%.**
2. **BUT WEEK 17 IS STILL WORSE THAN A NORMAL WEEK — by five points of blank rate, one starter in
   five.** The fix is not a stash; it is **carrying one extra live body into week 17**, which is
   also the week the roster seat matters most (doc 231).
3. **AND THE POINTS ARE NOT THE PROBLEM — THE ABSENCE IS.** Among players who actually played,
   week-17 scoring is 97% of their own recent average and week-18 is 95%; neither is distinguishable
   from no effect. **Availability again, a fourth time in this project.**
4. **THE WIRE DOES NOT GO QUIET LATE — IT GOES QUIET IN THE PLAYOFFS.** Weeks 11–14 run at **87%**
   of the mid-season add rate and only **2 of 46 team-seasons** went silent. Weeks 15–17 drop to
   **4 to 5.5 active teams of twelve**. **Claims are cheapest exactly when you are playing for the
   title — week 15 is the softest week you can still use.**
5. **A VERDICT THAT CHANGES: blocking.** Doc 227 recorded "no literature found" for claiming a
   player purely to deny a rival. **Literature exists and it is entirely ethical, not empirical** —
   the published discussion argues about sportsmanship and retaliation and contains no numbers at
   all. Re-tag it: `[LITERATURE EXISTS, UNQUANTIFIED]`, not `[NO LITERATURE]`.
6. Nothing to run, and **nothing new built** — a week-17 feature in September would be gold-plating
   a sheet that has to survive fourteen weeks first.

---

## 2. WEEK 17 AGAINST WEEK 18

**POPULATION: 601 player-seasons, 2021–2025, QB/RB/WR/TE who played ≥10 games and averaged ≥8.0
half-PPR points a game — men who were genuinely being started, not the whole pool.
BASELINE: each player's OWN mean over weeks 10–16 of that season, 13.5 points a game.**

| week | n who played | mean points | ratio to own baseline | p(ratio = 1) | **gave you nothing** |
|---|---|---|---|---|---|
| 16 | 521 | 13.87 | 1.016 | 0.52 | **14.3%** |
| **17 — our championship** | 490 | 12.96 | 0.970 | 0.33 | **19.3%** |
| 18 | 442 | 12.33 | 0.950 | 0.15 | **27.6%** |

`[TESTED]` **The scoring effect is null at both weeks.** What moves is whether the man appears at
all, and it moves monotonically: a normal week costs you one startable player in seven, week 17
one in five, week 18 more than one in four.

By position, week 17 → week 18 as a share of own baseline: **QB 0.96 → 1.02 · RB 1.02 → 0.91 ·
WR 0.95 → 0.98 · TE 0.90 → 0.81.** Backs and tight ends carry the week-18 damage; nothing at any
position is resolved at week 17.

**WHY THIS MATTERS FOR US SPECIFICALLY.** The NFL regular season runs to week 18 and our fantasy
season ends at 17. Most published week-17 advice is written for the whole market, much of which
plays a week later or reads week-18 experience back onto 17. **Do not import that panic wholesale.
Do plan for one extra live body.**
**NOT TESTED, and it is the obvious refinement:** whether the week-17 lift is concentrated on teams
that have already clinched. That needs a clinch table we do not hold. `[OPEN]`

## 3. WHEN THE WIRE ACTUALLY SOFTENS

**POPULATION: 1,230 executed adds, 2022–2025, by week.**

| stretch | adds per week | teams active, of twelve |
|---|---|---|
| weeks 4–7 | 82 | 6.5–7.2 |
| weeks 11–14 | 71 | 5.8–7.0 |
| **weeks 15–17** | **51** | **4.0–5.5** |

Weeks 11–14 are **87%** of the weeks 4–7 volume, and only **2 of 46 team-seasons** made zero adds
in that stretch. `[TESTED]` **So the "everyone checks out down the stretch" intuition is wrong for
the regular season and right for the playoffs**, which is exactly when half the league is
eliminated. Roughly **six or seven of twelve managers touch the wire in any given week all season**
— he is competing with about half the room, not all of it.

## 4. WHAT THE PUBLISHED PLAYOFF MATERIAL ACTUALLY IS

Sources dated before use (`ERROR_PATTERNS` B7). The playoff-schedule waiver genre is large and
almost entirely *weekly content*, not method: RotoBaller's weeks-15–17 streamers and stashes piece,
CBS's week-15 and week-17 columns, FantasyPros' weeks 16 and 17 pickup lists, NFL.com's week-16
playoff-boost list. **Each names players for one season; none states a rule, a rate or a sample.**
**They are not dismissed — they are simply not testable objects.** The one general claim running
through all of them is the resting-starters point, and §2 above is that claim measured.

**And the one method they share, we already have and have already measured:** buy the man whose
weeks 15–17 draw is soft. Doc 229 measured where that is real — **tight end, about +3 points a
side, and nothing at quarterback, back or receiver** — and doc 230 measured the defence version and
turned it into a hold rather than a weekly shop. **Those two are our playoff-schedule strategy, and
they are further along than the published version because they carry a number.**

## 5. WHAT WOULD ACTUALLY HELP NEXT

Matt offered a podcast transcript. **The useful kind is specific:** an episode where somebody
describes their waiver PROCESS — how they rank claims against each other, when they spend priority,
what they do with a roster spot — rather than an episode naming this week's adds. A process claim
can be turned into a testable form and run against four seasons of this league. A list of names
cannot. `[OPEN — and the offer is worth taking up on those terms]`

## 6. STILL OPEN AFTER THIS SWEEP

- Whether week-17 absence concentrates on clinched teams. Needs a clinch table. `[OPEN]`
- Blocking: no empirical treatment exists anywhere I can find, so if it is ever to be answered it
  will be answered here, on `lineups.py` output, or not at all. `[OPEN]`
- The reachable pool, and the starters question — both waiting on `py waivers.py` and
  `py lineups.py` (docs 230, 231).
