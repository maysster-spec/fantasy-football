# 391. The waiver period is two days, so the gate is WHEN YOU PLACE IT, not what day it is. And the IR seat is a two-week loan, not an asset.

> **CORRECTED IN PLACE THE SAME DAY BY DOC 392. READ THAT FIRST.**
> **AND CORRECTED AGAIN ON 23 SEPT BY DOC 399 (directive v9.22). §3's SEAT-LIFE CURVE IS RETRACTED.**
> Two separate defects. **(a) THE EVENT IS WRONG.** This doc counts the seat as dying when the man **takes a
> snap**. ESPN's football help, sourced at v9.19 (doc 394), invalidates the IR slot only when he **loses his
> injury designation entirely** — Questionable and Doubtful keep it, and NFL IR keeps it. Re-measured on this
> doc's own 1,431 rows, **the seat is SAFER than stated here in week one (75.5% valid against 70.4% not-playing)
> and SHORTER from week three (35.2% against 41.9%)**. **(b) THE CURVE DOES NOT REPRODUCE AT ALL**: six
> population definitions were tried against the n=1,035 block below and **none matches it**. The state table
> above it reproduces to the decimal, so the defect is in the curve. **The conclusion survives — the median seat
> still dies between two and three weeks — and the position ordering does NOT: a parked QB is the second
> riskiest seat, not the safest.** See doc 399 and `Scripts\research\ir\ir_seat_validity.py`.
> **§2 of this doc is RETRACTED.** The figure *"91.9% of Out designations are filed Thursday or later,
> so a Thursday-morning run beats the official designation channel about 92% of the time"* **does not
> measure that.** `date_modified` is the timestamp of the **last edit** to a player-week row and nflverse
> keeps only that one row, so the number says when a row stopped changing, not what it said on Wednesday,
> and separating those two cases was the whole claim. **Supportable floor only: at least 7.88% were
> settled by Wednesday. The complement is unobservable. Timing is BLOCKED, not measured.** (n was 1,219,
> not 1,218.)
> **§6's item 1 is also demoted:** the Sunday-night rule stands on a **dominance argument** (placing
> earlier cannot expose a claim to more, and costs nothing), **not on a measured edge. No effect size
> attaches to it.**
> **And the load-bearing premise of this whole doc is Matt's and was never tested:** that ESPN refuses
> the add once the parked man's status flips. Everything measured here sits around it. See §0.5(a5).
> **§1, §3, §4 and §5 stand.** The 2-day waiver period, the state table, the seat-life numbers and the
> break-cost section are unaffected.


**22 Sept 2026. Supersedes the IR paragraph written into directive v9.14 earlier today, which Matt
correctly called under-specified.** His words: *"I'm certain it could have been worded better and more
precisely thoroughly with richer context. There are other scenarios where somebody might be ruled out
and yet the status changes before waivers go through."*

He is right on both counts, and the second one is the more important. v9.14 captured one scenario,
a man ruled Out who stays Out, and wrote it as if that were the rule. It is one row of a table.

---

## 1. WHAT THE SETTINGS FILE ACTUALLY SAYS, AND WHY IT CHANGES THE SHAPE OF THE RULE

`Source\2026_League_Settings.txt`, read today, lines 29, 44 and 115–127:

```
Roster Size: 15   Total Starters: 9   Total Bench: 6
Injured Reserve (IR): 3                       <- listed SEPARATELY from the 15
- Lineup Changes: Lock individually at Scheduled Gametime
- Player Acquisition System: Waivers
- Waiver Period: 2 Days
- Waiver Order: Reset Each Week to Inverse Order of Standings
- Observe ESPN's Undroppable Players List: Yes
```

**`Waiver Period: 2 Days` is the line the whole mechanic turns on and no file in this project had
ever quoted it.** It means the processing time is **not a fixed weekday**. A claim placed on day D
processes on the morning of **D+2**. Matt's three current claims were placed Tuesday 22 Sept and he
reported them as *"Processes on the morning of Sep 24"*. Thursday. That is the 2-day clock, and it
confirms the setting against live behaviour rather than against the text alone.

v9.14 said *"put the waivers in before the status changes."* That is his instinct and it is correct,
but as written it is untestable, because it does not say what the clock is. **With the clock named,
the instinct becomes an instruction: the placement day chooses which injury reports your claim has to
survive.**

---

## 2. THE CLOCK. WHICH REPORTS EACH PLACEMENT DAY HAS TO SURVIVE

The NFL week's injury paperwork lands in a fixed order: practice reports Wednesday, Thursday and
Friday afternoons, the final game designation (Out / Doubtful / Questionable) on Friday for a Sunday
game, and inactives 90 minutes before kickoff. A player's designation from LAST week persists until
something in that sequence replaces it.

| you place the claim | it processes | injury reports it must survive |
|---|---|---|
| **Sunday night, after the games** | **Tuesday morning** | **none. The new week's paperwork does not exist yet** |
| Monday | Wednesday morning | none, if the morning run beats Wednesday afternoon's practice report |
| **Tuesday** *(where his three sit now)* | **Thursday morning** | **Wednesday's practice report** |
| Wednesday | Friday morning | Wednesday's and Thursday's practice reports, and possibly Friday's final designation |

**Measured, so the last column is not a guess** (nflverse official injury reports, regular season,
QB/RB/WR/TE, 2021–2024, the four seasons that carry the `date_modified` stamp; 2025 dropped it):
of the rows that ended the week as **Out**, the designation was last filed

```
  Monday      0.00%        Thursday     4.27%
  Tuesday     0.25%        Friday      80.56%
  Wednesday   7.88%        Saturday     6.64%
                           Sunday       0.41%
```

~~91.9% of Out designations are filed Thursday or later; 8.1% by Wednesday, and those are
overwhelmingly teams playing Thursday night, whose week closes early. n=1,218 Out rows.
So a Thursday-morning run beats the official designation channel about 92% of the time.~~
**[RETRACTED, doc 392. See the banner at the top of this file. The only supportable reading of the
table above is a FLOOR: at least 7.88% of Out designations were settled by Wednesday, because those
rows' final edit was Wednesday or earlier. Nothing in this feed can say what the other 92% said on
Wednesday. n=1,219.]**

**BLOCKED, and naming it per §0.5(a4):** I cannot measure the Wednesday practice report's effect,
because nflverse keeps **one row per player-week, the final one**. A row stamped Friday may have
existed Wednesday saying something else, and that earlier state is not in the file. The missing input
is a day-by-day snapshot of NFL.com's injury report. It would have to be scraped daily going forward;
it cannot be recovered for past weeks. **I have not tried, and it is now an open thread.**

**And a second unknown sits on top of it:** whether ESPN's `injuryStatus` field even moves on a
Wednesday *practice* report, or only on the Friday *game designation*. ESPN shows game designations;
practice participation is not one. If it is the latter, a Thursday-morning run is nearly airtight and
only transactions and news can break it. **Unverified. Do not assert either way.**

---

## 3. THE SCENARIO TABLE, the thing Matt asked for

"Ruled out" is not one state. These are the states a man can be in when you want to park him, and
they do not behave the same way.

| # | the state he is in | how long it holds | survives a 2-day claim? | what to do |
|---|---|---|---|---|
| 1 | **Placed on NFL injured reserve** | four games minimum, by rule | **yes, for weeks** | park him without thinking about it. This is the only one that is safe at any placement day |
| 2 | **Ruled Out on the final report, did not play** | until the next designation replaces it | **usually, 92% of replacements land Thursday or later** | the main case. Place Sunday night and it is not close |
| 3 | **Ruled Out, then upgraded in-week**, activated off IR, a practice window opened, or the injury simply resolved | can flip **any day, including Monday or Tuesday** | **no. This is the one that breaks** | the case v9.14 missed. Nothing on a schedule protects you; only placing early does |
| 4 | **Questionable, then inactive 90 minutes before kickoff** | never carried a formal Out at all | **unreliable** | do not build a claim on it. Whether ESPN back-fills an Out here is unverified |
| 5 | **Doubtful** | Doubtful is not Out | **no** | do not park. He is very likely not slot-eligible |
| 6 | **Suspension, PUP, NFI** | the full term, fixed and known in advance | **yes** | park. §6 already says these cost nothing, and this is why |
| 7 | **Out in week w, his team on bye in week w+1** | no new report exists that week | **yes, nothing can change it** | 7.9% of Out cases. The single safest week to spend a claim |
| 8 | **Out, and his team plays Thursday night next** | the new designation is filed **Wednesday** | **first to break** | the one schedule check worth making before placing |

Row 3 is Matt's point, stated as a row. Rows 4, 5 and 8 are the ones neither of us had.

---

## 4. HOW LONG THE SEAT ACTUALLY LASTS, the number that stops it being treated as an asset

**Pre-registered form (§0.5(a2)), written before the run:** population = QB/RB/WR/TE carrying
`report_status == 'Out'` on the final official report of regular-season week w, 2021–2025, whose team
also plays in week w+1. Outcome = does he take an offensive snap in w+1, and what is his designation
in w+1. **This is a base rate, not a hypothesis test, nothing is confirmed or killed by it.** Join is
`gsis_id → pfr_id` through nflverse `players.csv`, never a name join (§3). **n = 1,431** after
excluding 122 bye weeks (7.9%) and 1 unmatched id.

```
he plays a snap in week w+1 ............... 29.6%
still carries 'Out' in w+1 ................ 38.9%
downgraded to Questionable in w+1 ......... 19.5%
Doubtful in w+1 ............................ 3.4%
no designation at all in w+1 .............. 38.2%   of which 40.4% never play in the
                                                    next four weeks, which reads as NFL IR
```

~~**Seat life, from the week he FIRST goes Out (n=1,035):**~~ **RETRACTED, doc 399 — UNREPRODUCIBLE.**

```
~~still had not played by w+1 .... 73.8%~~     RETRACTED: no population definition reproduces
~~still had not played by w+2 .... 53.8%~~     this block. Six were tried (all Out-weeks, first
~~still had not played by w+3 .... 40.8%~~     Out per player-season, gap-separated episodes,
~~still had not played by w+4 .... 31.2%~~     each with and without the bye filter); the
~~still had not played by w+5 .... 23.8%~~     nearest lands n=1,040 and runs 4 to 11 points
                                               high in the tail. Do not quote it.
```

**REPLACED BY THE SOURCED EVENT (doc 399, same 1,431 rows as the table above):** seat still VALID
**w+1 75.5% · w+2 51.2% · w+3 35.2% · w+4 26.4% · w+5 22.2%**, and **the roster is invalid with the lineup
frozen the following Sunday 24.5% of the time** (351 of 1,431). **The median parked seat still lasts between two
and three weeks.** It is a loan, not an asset. Any plan
that spends the free seat on a body you intend to hold all season is mispriced by roughly a month.

**By position, plays in w+1:** QB **19.2%** (n=156) · RB **26.7%** (n=296) · TE **31.4%** (n=309) ·
WR **33.0%** (n=636). **A parked quarterback holds his seat longest and a parked receiver shortest**,
the opposite of what the roster wants, since QB is the position §6 says to stream.

**The 19.5% Questionable cell is the quiet one.** That is a man who is no longer Out, so the seat ends,
but who has not yet played, so you have given the seat back and gained nothing. It is the most common
way the arrangement fails, and it is more common than him simply being healthy and playing well.

---

## 5. WHAT BREAKS, AND WHAT IT COSTS, both directions

**Break BEFORE the run.** The occupant is upgraded, the IR slot no longer holds him, and the roster
that the pending claim would create is illegal. **Whether ESPN fails the claim, or processes it and
forces an immediate drop, is unverified**, and the difference matters, because a failed claim keeps
Matt's waiver position (10 of 12) and a forced drop spends it. This is worth one live observation and
is on the open-threads list.

**Break AFTER the run.** Sixteen bodies for fifteen seats. ESPN blocks roster moves until one is cut.
This is Matt's *"if you really need to play him then you can drop whoever you want"*, and it is a real
option, not a penalty, because the trigger for it is the parked man being healthy again. **Two caveats
that v9.14 did not carry:** `Observe ESPN's Undroppable Players List: Yes`, so "whoever you want" has
exceptions the settings file imposes; and any drop spends that player's keeper eligibility, which
§2.1(a) requires be stated at the moment a drop is recommended.

**And one that is not about injuries at all:** `Lineup Changes: Lock individually at Scheduled Gametime`.
A player cannot be moved into or out of the IR slot once his own game has kicked off. A Sunday-morning
realisation is already too late for the 1pm games.

---

## 6. WHAT THIS CHANGES

1. **Place claims Sunday night, not Tuesday.** The 2-day clock means a Sunday-night claim processes
   Tuesday morning and crosses no injury paperwork at all. It is free, it is the general form of Matt's
   own instinct, and it was invisible while nobody had quoted the waiver-period line.
2. **His three current claims process Thursday morning and cross Wednesday's practice report.** That is
   the exposure, it is small, and Nacua's Wednesday report was already on his list for other reasons.
3. **Stop calling the seat an asset.** Median two to three weeks.
4. **§4.35's index line says the injuries feed "lands after the Tuesday run."** There is no Tuesday run.
   Retracted and restated against the 2-day clock.

## 7. OPEN

- **[OPEN]** Does ESPN's `injuryStatus` move on a Wednesday practice report, or only on the Friday game
  designation? One live observation settles it. OWNER: me, from the `ff.bat` pull.
- **[OPEN]** On a break before the run, does ESPN fail the claim or force a drop? OWNER: me, first time
  it happens.
- **[BLOCKED]** Day-by-day injury-report history. Missing input: a daily scrape of NFL.com's report.
  Not recoverable for past weeks. Not tried.
- **[OPEN]** Which ESPN designations this league's IR slot accepts, and whether a man there counts
  against a position cap. Carried over from doc 390, still unverified.

**Script:** `Scripts\research\ir\ir_return_rate.py`, with the pre-registered form in its docstring.
**Defect found and fixed during the run, worth recording:** the 2021–2024 injury files carry
`game_type` and `date_modified`; the 2025–2026 files carry `season_type` and dropped `date_modified`.
A `season_type == 'REG'` filter therefore **silently discarded four of the five seasons** and the first
run printed n=410 with no error. The script now asserts that every season survives the filter. This is
§3's silent-skip trap in a fifth place.
