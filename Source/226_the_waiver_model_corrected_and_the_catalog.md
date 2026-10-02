# 226 — The waiver model corrected, the automation shipped, and the catalog of what is still missing

**2026-09-08.** Matt, in five messages: the Windows scheduler instead of running commands · the
within-week waiver-order mechanic · *"i typically have a winning record which hurts my waiver
order so i think you need to reevaluate some of your claims and logic"* · the bye-week trade idea ·
and the instruction that ends this doc: *"make sure your DB is full of the info you need prior to
fully developing a strategy that is half baked. We both have a history of doing this."*

**He is right about that too, and §3 of this doc is the catalog rather than another strategy.**

---

## 1. THE CORRECTION HE FOUND — AND IT WAS A HARD ERROR, NOT A NUANCE

Doc 223 shipped this rule: *"Priority resets weekly to inverse standings, so using it costs you
nothing — there is no budget to protect and no reason to save it."*

**Half of that sentence is false, and it is the half that matters.** From ESPN's own documentation:

> *"No matter which option is selected, once a team successfully makes a waiver claim, they move to
> the bottom of the waiver priority list."* — ESPN Fan Support, *Waiver Order Overview*

**So the order resets ACROSS weeks and collapses WITHIN one.** Matt's words: *"waiver order on the
second waive/round is bad for me because i usually take waivers 1st waive."* Exactly right.

**Measured in the transaction record, 460 team-weeks with claims, 2022–2025:**

| claims submitted that week | mean that EXECUTE | max |
|---|---|---|
| 1 | 0.74 | 1 |
| 2–4 | 1.45 | 3 |
| 5–9 | 2.00 | 4 |
| **10+** | **2.15** | 4 |

**65% of team-weeks end with 0 or 1 claim landing.** Volume buys a little and then stops: the step
from 5–9 to 10+ is worth 0.15 of a claim. **Matt at 10+ averages 2.44, the best in the league at
that band** — his long list is not the problem.

> **THE RULE THAT REPLACES THE WRONG ONE: the first claim that clears is the only one you get at
> your real priority. Everything below it is a leftover taken from the back of the line. Rank the
> list by value, never by convenience — and he starts near the back anyway, because the order is
> inverse standings and he wins.**

## 2. AND HIS OTHER INSTINCT — "I GET THERE FIRST" — IS DEAD

**§0.5(a2), the testable form he asked for:** *among players two or more managers went after in one
season, does claiming him a waiver period or more before anybody else predict that he was any
good?*

**POPULATION:** 312 executed waiver adds, 2022–2025, of which 66 are on players at least one other
manager also pursued that season. **BASELINE:** rest-of-season points per game from the week after
the move through week 14, under §2 scoring, against the position's measured replacement.

| lead over the next manager to want him | n | hit rate | ppg |
|---|---|---|---|
| **2+ weeks early** | **16** | **0.0%** | 4.86 |
| 1 week early | 1 | 0.0% | 2.40 |
| same week or later | 49 | **32.7%** | 10.03 |

**Sixteen tries at being early, zero hits, league-wide. Seven of the sixteen are Matt's** — he does
it more than anybody. `[TESTED]`

**The mechanism is not that he picks badly.** What makes a wire player good becomes visible to all
twelve managers on the same day. Two weeks ahead of that day there is nothing to see, so an early
claim is a hunch. **Being early wins the player; it has never once won the right one.**

**This closes §4.19's paradox for the third and last time.** Doc 111 found him 1.05 weeks ahead of
the field with no conversion; doc 205 ruled out the drop side; doc 225 showed the earliness buys
ACCESS (56% vs 16%). **This says the access is real and the timing premium is worth nothing beyond
about one waiver period.** Claim in the run right after the news, not before it.

### 2a. RETRACTED THE SAME DAY — THE TABLE ABOVE ANSWERS A QUESTION HE DID NOT ASK

**Matt, on the table in §2:** *"I quoted the wrong sentence. this stuff — lead over the next manager
to want him: 2+ weeks early 16, 0.0% · 1 week early 1, 0.0% · same week or later 49, 32.7%"* and
*"maybe not with the logic i intended i see now."*

**He is right and this is §0.5(a2) failing for the fourth time in this project.** His claim, in his
own words earlier the same day, was *"a week earlier or waiver period earlier."* **The table has
n=1 in that bucket.** It cannot speak to his claim at all; it speaks to being two or more weeks
early, which is a different behaviour.

**And the population was wrong as well as the bucket.** §2 counted **waiver claims only**. But a
player nobody else has claimed yet is very often taken as a **free agent**, not on waivers — which
is the exact mechanism being tested, excluded by construction. `ERROR_PATTERNS` A19 and §0.2's
"test the object production builds" both point at this.

**RE-RUN on all 2,201 ADD attempts, waiver AND free agent, 245 scored adds where at least one other
manager also went after the same player that season:**

| lead over the next manager to want him | n | hit rate | ppg |
|---|---|---|---|
| 3+ weeks early | 34 | **20.6%** | 9.03 |
| 2 weeks early | 12 | **33.3%** | 10.84 |
| **one week early — HIS CLAIM** | **4** | 0.0% | 7.05 |
| same week | 81 | **30.9%** | 9.81 |
| behind the field | 114 | **25.4%** | 9.05 |

> **THE "SIXTEEN TRIES, ZERO HITS" HEADLINE IS WITHDRAWN AND MUST NOT BE QUOTED.** It was correct
> arithmetic on a population that excluded the adds most likely to be early. On the full record
> **timing is flat** — 21% / 33% / 31% / 25% across the bands, no monotone pattern and nothing that
> survives these sample sizes. **Being early is not measured to help and is not measured to hurt.**

**His own cut still leans his way and cannot carry weight:** 2+ weeks early **n=7, 0 hits**; behind
the field **n=12, 33.3%**. Seven events.

**WHAT SURVIVES §2, UNCHANGED:** the *access* finding, which is a different measurement — he lands
**56%** of the men nobody else claimed and **16%** of the ones they did (doc 224). That is where
the earliness pays, and it does not depend on this table.

**WHAT WOULD RESOLVE IT:** the one-period question needs the bucket populated, and four events in
four seasons says this league will never populate it. It is answerable only NFL-wide, and only with
a transaction feed we do not have. **Report it as unmeasurable rather than as a null.**

## 3. THE EXTERNAL SWEEP, AND THE ONE MECHANISM IT OFFERED THAT WE COULD TEST

Sources read, dates stated before use (`ERROR_PATTERNS` B7): ESPN Fan Support *Waiver Order
Overview* (undated, official) · 4for4 *Waiver Wire & FAAB Strategy* (2023-08-28) · Footballguys
forum thread *Waiver Wire Priority* (2018-09-11).

**The published material is thin on priority waivers** — 4for4's guide is FAAB-first and offers
nothing for a team low in the order. The forum thread supplies four competing mechanisms:

| mechanism | verdict |
|---|---|
| **hoard priority for a genuinely impactful player** | **TESTED — NULL.** Weeks waited before spending a claim vs the next claim's hit rate: **r = −0.022, n=266, p=0.715.** Waiting two, three or five weeks makes the next one no better. |
| spend it actively every week | consistent with the above; nothing distinguishes it |
| "stay last on purpose and take the leftovers" | partly supported — the uncontested pool does hit 22.6% — but it is a description of Matt's forced position, not a choice |
| strong team guards it, weak team churns | untestable here; needs the standings join in §5 |

**"Elite waiver players rarely emerge" is the one point the forum and our own data agree on.**
Ours: **4 of 312 scored pickups over four seasons returned twice replacement.**

## 4. HIS BYE-WEEK TRADE IDEA — SIZED, AND IT IS THE BIGGEST SINGLE NUMBER IN THIS DOC

Matt: *"trading away a player who has a bye week later in the year before your player has a bye
week... can null the loss of a bye week if done correctly."*

**Computed on his actual roster** (projection ÷ 17 for a weekly rate, best legal starting eight,
K and D/ST excluded):

| week | off | costs |
|---|---|---|
| 5 | Worthy | 0.0 |
| 6 | LaPorta | **8.8** |
| 8 | Shough | 0.0 |
| 9 | Dowdle, Spears | 0.0 |
| 10 | Hurts, Dobbins | 3.5 |
| **11** | **Nacua, Judkins, Adams** (+ Browns D/ST) | **13.1** |
| 13 | Jeanty, Washington | 4.5 |
| 14 | Pickens | 1.6 |
| | **season total** | **31.6** |

**His mechanism is right and the prize is real: swap one of the three week-11 men for a comparable
player whose bye is 5, 8 or 9, and about thirteen points of hole stops existing.**

**AND THIS MUST NOT BE READ AS CONTRADICTING §4.11.** That section measured a *bye collision as a
draft tiebreaker* — worth at most 1.2 points, and it is still right that a bye should never move a
pick. **This is a different object: the realised in-season cost of the whole bye structure on one
roster.** 1.2 belongs to the draft; 31.6 and 13.1 belong to the season. Quote them apart.

`[COMPUTED, not tested]` — it is arithmetic on projections, not an outcome measurement, and the
trade half is untestable because **we hold no trade history at all (see §5).**

## 5. THE CATALOG — WHAT THE DATABASE IS MISSING, AT HIS INSTRUCTION

**Ranked by what each unlocks. Nothing below has been built; this is the shape, for him to re-order.**

| # | gap | what it blocks today | cost to get |
|---|---|---|---|
| **1** | **TRADE HISTORY — we have NONE.** `waivers.py` pulls ESPN's `mTransactions2` feed and then filters to `WAIVER` and `FREEAGENT`. **The trades were in the response and we threw them away.** | Every trade recommendation in this session is unmeasured, including §4's. "The league averages three trades a season" is a number from doc 12 that nothing here can check | **One line.** Re-run the existing script without the filter, four seasons |
| **2** | **Weekly standings → the actual waiver order.** `historical_scoreboard_2022_2025.csv` is in the project and has never been joined to the transaction record | The entire "he is at the back of the order" model is inferred from the settings and his own report. **His position has never been observed in a single week** | A join. No new pull |
| **3** | **Drops.** The `Transaction` string carries `DROP` and this session parsed only `ADD` | What a claim actually cost — doc 205 measured add-minus-drop once, on 2024–25 only | Parsing only |
| **4** | **Start/sit decisions.** No record of who he benched | "The bench covers week 9" is a projection claim. Whether he plays his best lineup is unmeasured, and it is plausibly worth more than the whole wire | ESPN box scores per week; a real pull |
| **5** | **A dated news timeline.** Nothing links a claim to the event that made the player interesting | "Claim in the run right after the news" cannot be verified — §2's finding is measured against *other managers*, which is a proxy for the news, not the news | Hard. Probably not worth it |
| **6** | **External breadth.** Three sources read this session, all generic priority-waiver advice | Bye-week trade arbitrage, trading into a low-trade league, in-season contender roster construction, and handcuff value studies are all unsearched | Cheap. Do it before the next strategy, not after |

**THE HONEST HEADLINE OF THIS SECTION: gaps 1, 2 and 3 are all recoverable from files and feeds we
already have, and two of the three are self-inflicted — we filtered the data out.** Doing those
three first is the difference between the next strategy doc and another half-baked one.

## 6. SHIPPED THIS SESSION

- **`Scripts\wire.py`** — rewritten. Now writes `Source\THE_WEEKLY_WIRE.html` itself (`--html`),
  carries the one-injury-away stash list, and **asserts `pos == 'RB'` before reading `depth_map`'s
  job columns** (doc 224's defect, guarded). **Its negative control was run first:** with ESPN
  refused it writes the page with a red banner saying the tables are not current, rather than
  leaving yesterday's sheet looking live. §0.2 — an exit code is not a result.
- **`Scripts\weekly.bat`** — new. What the scheduler runs; logs every run to `weekly_log.txt`.
- **`Scripts\setup_tasks.ps1`** — rewritten. **Deletes the two spent draft-night one-shots** and
  registers **`FF2026 - Tuesday wire`, weekly, Tuesday 06:00, `-StartWhenAvailable`** so a machine
  that is off at six runs it at next logon instead of silently skipping. Also drops one Desktop
  shortcut at a filename that never changes.
- **`Source\THE_WEEKLY_WIRE.html`** — the "priority costs nothing" line replaced, the early-claim
  finding added, hoarding recorded as null, and the week-11 trade named.

- **`Scripts\lineup.py` + `Scripts\gameday.bat`** — **AMENDED 2026-09-08, later the same day.
  Matt: *"that's for Tue, did we skip Thurs, or whatever the 2nd window was?"* He is right, I did.**
  The routine on the page has always had two windows and only the Tuesday one was scheduled.
  `lineup.py` answers one question — is there a man in the starting nine who will not be on the
  field — flagging OUT / DOUBTFUL / IR / SUSPENDED, **anyone whose team is on bye**, an empty
  starting slot, and QUESTIONABLE as amber, then listing the healthy bench men at that position.
  Registered as **`FF2026 - Lineup check`** on three triggers: **Thursday 17:30** (before the night
  game), **Sunday 11:45** (inactives publish 90 minutes before the 1pm kickoffs) and
  **Sunday 15:30** (the late slate). Second Desktop shortcut, `Lineup check`.
- **`Source\byes_2026.csv`** — new, and it closes a gap nothing in this project had: **a
  team-to-bye table.** Derived from the board itself, 32 teams, and every team's players agree
  unanimously, so it needed no external source. The board excludes the 12 keepers, so without this
  file Pickens has no bye anywhere on disk and a lineup check would have silently passed him.
- **`Scripts\set_cookies.py`** — `lineup.py` added to its `FILES` list in the same commit, and the
  rewrite was executed against it, not assumed: both patterns match exactly once and the rewritten
  file still parses. Six files now carry the cookies and one command refreshes all six.

**GUARDS RUN BEFORE THE FEATURE, NOT AFTER (§0.2):** `lineup.py` was tested with its negative
controls FIRST — ESPN refusing (writes **"CANNOT CHECK YOUR LINEUP"** in red rather than a stale
all-clear) and the bye file missing (prints a warning instead of skipping the check silently) —
then against a fabricated week-11 roster carrying a bye, an OUT, a QUESTIONABLE and an IR man.
All four fired correctly and the IR player was correctly kept off the replacement list.

**[AMENDED AGAIN, 2026-09-08 evening — ONE TASK, NOT FOUR.]** Matt: *"I didn't know that Tuesday
meant all scheduled things. I'm fine with one scheduled [task] but that does it all."* And before
that, twice: *"I still don't see thurs."*

**Two failures, and the second is the one worth recording.** The first was mine and simple — he ran
the registrar before I had shipped the lineup half. **The second is that I shipped PowerShell I
could not execute.** The task's three triggers lived inside an array inside a hashtable; I checked
its brackets and quotes and sent it, and the Thursday trigger did not appear. **There is no
PowerShell in my container, so §0.4's rule — a script that runs in your container is not a script
that runs — was not even satisfiable. I shipped something I had never run at all.**

**The replacement removes the whole class of failure.** The schedule is now a **static Task
Scheduler XML file**, `Scripts\ff_task.xml`, registered with `schtasks /create /xml`:
- **ONE task, `FF2026`, with FOUR triggers** — Tue 06:00, Thu 17:30, Sun 11:45, Sun 15:30. One
  entry in Task Scheduler, one Triggers tab with four rows, one log.
- **It runs `ff.bat`, which rebuilds BOTH pages on every run**, whatever day it is. **No
  day-of-week branching** — branching is where the bug would be, and two ESPN calls cost nothing.
  Whichever shortcut he opens is current.
- `setup_tasks.bat` is now the single registrar; it **deletes the older split-up task names first**
  so exactly one `FF2026` survives, then queries the task back and prints its four schedule lines.
- `setup_tasks.ps1` and `setup_tasks_simple.bat` are **stubs** pointing at it — one name, one job.
- **What I could verify, I did:** the XML is valid UTF-16-with-BOM, parses, carries four
  `CalendarTrigger` blocks on the right days and times, and its `Settings` children are in the
  order Windows itself exports. **What I could not verify is whether `schtasks` accepts it**, which
  is why the registrar prints the task back rather than printing SUCCESS.

**SUPERSEDED ABOVE:** the `FF2026 - Tuesday wire` / `FF2026 - Lineup check` two-task design, and
the `weekly.bat` / `gameday.bat` split. Their logs (`weekly_log.txt`, `gameday_log.txt`) are
replaced by one `ff_log.txt`.

**HE RUNS ONE THING, ONCE:**
`Set-ExecutionPolicy -Scope Process Bypass -Force; & "G:\My Drive\_Fantasy\2026\Scripts\setup_tasks.ps1"`
in an **admin Command Prompt**: `"G:\My Drive\_Fantasy\2026\Scripts\setup_tasks.bat"`
then `schtasks /run /tn "FF2026"` to prove it, and read `Scripts\ff_log.txt`.
**A scheduled task that has never run is not a scheduled task.**

## 7. OPEN

- `wire.py`'s ESPN half is **still untested against a live session** — `py wire.py --check`.
- `depth_map.py` has no receiver version; `wire.py` now guards against reading it wrongly, nothing
  else does.
- The catalog in §5, items 1–3, in that order.
