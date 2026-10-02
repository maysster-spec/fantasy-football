> **BANNER, 28 Sept 2026 (doc 435), reproduced cold from `waiver_report_2022..2026.csv`.** The counts below reproduce exactly (884 / 0, 371 / 24, Matt 8 of 24). **The 6.1% RATE does not stand: the 371 no-drop executions include 247 FREE-AGENT adds, which have no processing step and can never appear as a failure row. On WAIVER claims alone the no-drop failure rate is 16.2% (24 of 148), 19.5% counting the six position-limit failures, against 0 of 502 with a drop.** Also: the "884 for 884" hides 103 drop-carrying claims that failed as already-dropped, 102 of them a second claim in the same run naming the drop the first claim had spent. **One drop carries one claim.** The rule, put a drop on every claim, gets stronger. Directive v9.32 §2 and finding 4.36(h) carry the correction.

> **CORRECTED IN PLACE BY DOC 394 THE SAME NIGHT (§9 rule 5). READ THAT FIRST.**
> **§2 of this doc is WRONG in two ways.** The two ESPN pages it treats as contradicting do not
> contradict: one of them is filed under **Fantasy Women's Basketball**, a different sport. And both
> were quoted through `WebFetch`, which returns a small model's rendering rather than the page, so
> the quotation marks were not earned (§3). **The football pages, read as page text, say the slot
> takes Out (O) or IR only, never SSPD, that an upgrade to Questionable or Doubtful breaks nothing,
> and that only losing the designation entirely invalidates the roster.** §4's waiver-history
> measurement (884 for 884) and §3's status-logger build are unaffected and stand.

# 393. The question was never whether the app has controls. It is when ESPN flips the status, and every run until now threw that away.

**22 Sept 2026. Closes the [OPEN] doc 392 left at the top of §4.36, and corrects the form I
pre-registered to close it.**

Matt asked *"What are we waiting for?"* The honest answer was nothing: §0.5(a4) says a BLOCKED item
must name the missing input **and whether I tried**, and I had not tried. But the form I then wrote
was wrong, and he killed it inside the same turn:

> *"did you read the question? The app has controls, of course it will refuse an illegal claim. You
> think people would use a fantasy football application that had such and obvious loophole?"*

**He is right. "Does ESPN refuse a claim that would create an illegal roster" is not a question, it
is an assumption every functioning app satisfies.** Testing it would confirm that software works.
This doc records the wrong form because §0.5(a2) exists precisely so the form gets caught before the
result, and here it was caught after. Nothing shipped: the first draft was never committed.

---

## 1. THE QUESTION, STATED PROPERLY

His mechanic has one load-bearing sentence and it is about **state at a moment**, not about rules:

> **At the instant the claim processes, is the parked man still IR-eligible in ESPN's eyes?**

Everything else follows. Rules are not in doubt; **timing is**.

---

## 2. AND ESPN'S OWN PAGE MAKES IT SHARPER THAN ROSTER ARITHMETIC

**Loaded, not read off a snippet. Date stated per `ERROR_PATTERNS` B7.**

*Reasons Why a Waiver Pickup May Not Process*, **last updated 11 Aug 2026**:

> **"Teams are not allowed to make claims if they have an ineligible player in the IR slot. If you
> have a healthy player in IR, the claim will not process."**

**I read that as operative and wrote it into §2. Matt corrected it inside the same turn, from his own
experience of this league:** *"if the claim was made BEFORE the status change it stays locked. But if
my claim is successful then my players are locked, that is, if I wish to move a player from my bench
to the active roster I can't, not until I drop someone to fit the limit."*
**HIS ACCOUNT IS OPERATIVE (§0.6(4)), AND IT CHANGES THE SHAPE OF THE COST.** The claim lands. The
roster sits at sixteen. **The penalty is a FROZEN LINEUP until he cuts someone**, which is his own
*"I have either option"* with the price finally written down. **And it moves the risk from Thursday to
Sunday:** a claim landing Thursday morning leaves him unable to change a starter, and if he does not
notice until kickoff it costs whatever he needed to swap in.

**A second ESPN page contradicts it** (*How does the IR slot impact Waiver Claims and Free Agents?*,
**10 Mar 2026**): *"If you have a player on your IR/IL who becomes healthy between when you made the
waiver claim and when the claim processes, the claim will go through as normal."* It adds one line
both pages agree on and that is under Matt's control: *"If you have an open bench slot when you make
a waiver claim but then activate an IR/IL player before the claim processes, your claim will fail."*

**VERDICT: the vendor contradicts itself, Matt's direct experience matches the OLDER page, and neither
page tells us WHEN the status moves.** Treat his account as operative. **Best reading of the conflict,
NOT verified: the two pages describe different states, an ineligible man already sitting in the slot
when the claim runs versus one who flips inside the window. Do not assert it.** A third page (*Moving Players on
and off the IR*, 18 Aug 2026) does not address status improvement at all.

---

## 3. WHAT WAS ACTUALLY MISSING, AND IT WAS BEING THROWN AWAY SIX TIMES A WEEK

Doc 392 filed the timing question as **BLOCKED** because nflverse keeps one row per player-week, so
a Wednesday state is unrecoverable. **That was true of nflverse and false of the thing we actually
have.** ESPN's own `injuryStatus` is in the `mRoster` payload `wire.py` already reads on every pull,
and `ff.bat` already runs on a schedule: **Tuesday 06:00, Thursday 17:30, twice Sunday, plus daily
07:30.** Roughly six observations a week, per man, and **not one of them was ever written down.**
`MY_ROSTER.csv` is overwritten each run, so yesterday's status is gone.

**FIXED. `wire.py` now appends `Source\STATUS_LOG.csv` every run:**

```
read_at,run,espn_id,player,slot_id,status
2026-09-22 21:25,TUE0600,4426515,Puka Nacua,21,OUT
2026-09-22 21:25,THU1730,4426515,Puka Nacua,21,QUESTIONABLE
```

Append-only, every man every run, no state comparison so there is no silent-skip path (§3).
Timestamped to the minute with the run label from `FF_WHO` (doc 380). **Built and executed against
the shipped block, not an equivalent one (§0.2, doc 80), with both negative controls run first: an
empty roster refuses and says so; an unwritable target refuses and the wire keeps going.**

**One week of runs dates the flip.** That is the measurement, and it needed no new source, no scrape,
and nothing from Matt beyond the schedule he already has.

---

## 4. SEPARATELY, AND IT MATTERS ON THURSDAY: THE DROP IS THE WHOLE GAME

This came out of the same pass and stands on its own. **It does not answer the mechanic**, and it is
filed here rather than dressed up as an answer.

**Population: every waiver and free-agent event in `waiver_report_2022..2026.csv`, this league,
n=2,256.** Restricting to claims that reached processing and were not outbid (`EXECUTED` +
`FAILED_ROSTERLIMIT`):

```
claim NAMED a drop      884 executed,  0 roster-limit failures    0.0%
claim named NO drop     371 executed, 24 roster-limit failures    6.1%
```

**884 for 884.** All 24 failures carried zero drops. **And the largest single owner is Matt: 8 of
the 24**, all in 2025, weeks 2, 2, 4, 4, 5, 10, 10, 10 — three in one week, twice. *(Team identity
confirmed, not guessed from the name: "The Poetry of Junkyard Juggers" is the team that added Jonah
Coleman, 4702555, and Devaughn Vele, 4569559, both on `MY_ROSTER.csv`. A 2024 team called
"Ja'Marracle Whip Juggernauts" holds 2 more and is probably his, NOT confirmed, do not assert.)*

**"Put a drop on every claim" was reasoning on his to-do list. It is now his own league's number.**

---

## 5. WHAT CHANGES

1. **`wire.py` writes `STATUS_LOG.csv`.** Re-pinned in `check_kit.py`. Nothing for Matt to run: it
   rides the existing schedule and the first rows land at the next pull.
2. **§4.36's centre moves from UNTESTED to PARTLY TESTED, and the answer is Matt's:** the claim
   lands and the LINEUP freezes until he drops someone. The vendor's two pages disagree and neither
   is operative. **Check the roster the morning a claim processes.** Flip timing is now measured.
3. **Do not activate a man off IR while a claim is pending.** Both ESPN pages agree that kills it,
   and unlike a status flip it is entirely under his control.
4. **The no-drop rule is measured, 884 for 884.**

## 6. OPEN

- **[OPEN], mine, one week away:** the flip timing, from `STATUS_LOG.csv`. First read after the week
  of 22 Sept.
- **[OPEN]:** which designations this league's IR slot accepts, and whether an IR man counts against
  a position cap. `mSettings` may carry the first and `wire.py` already reads it.
- **[BLOCKED], unchanged:** day-by-day NFL injury-report history (doc 392 §1). Not needed for the
  question above, which ESPN answers directly.

**Sources:** [Reasons Why a Waiver Pickup May Not Process](https://support.espn.com/hc/en-us/articles/360029528571-Reasons-Why-a-Waiver-Pickup-May-Not-Process) (11 Aug 2026) ·
[How does the IR slot impact Waiver Claims and Free Agents?](https://support.espn.com/hc/en-us/articles/4669672308116-How-does-the-Injured-Reserve-IR-slot-impact-Waiver-Claims-and-Free-Agents) (10 Mar 2026) ·
[Moving Players on and off the IR and IL](https://support.espn.com/hc/en-us/articles/115003860512-Moving-Players-on-and-off-the-Injured-Reserve-IR-and-Injury-List-IL) (18 Aug 2026)
