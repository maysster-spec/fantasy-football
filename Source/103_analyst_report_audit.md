# 103 — Audit of the Gemini analyst-call report

**Date:** 2026-08-31 · **File:** `Comprehensive Fantasy Analyst Call Scraping, Fact-Checking, and
Custom League Draft Report.md` (24 KB, dropped at the 2026 root).

**Verdict up front: do not draft off it. It is useful as a reading list and nothing more.**
Checked its 21 player recommendations against the shipped board, the 2026 depth charts and the
predicted keeper list: **17 of 21 disagree**, and the disagreements are not close calls.

---

## 1. IT DOES NOT KNOW THIS IS A KEEPER LEAGUE IN PRACTICE

It recites the keeper rule correctly and then recommends **five players who cannot be drafted**:

> **Drake Maye** (pick 41 "6-pt QB pivot flag") · **Javonte Williams** (picks 41–56 "RB workhorse
> flag") · **Stefon Diggs** (picks 104–128) — all three are **predicted keepers**.
> It also tells you to *fade* **Cam Skattebo** and **Rashee Rice**, who are likewise kept, so those
> calls are moot.

Two of its five tactical "flags" — the pick-41 QB pivot and the 56/65 workhorse flag — are built on
players who will be on someone else's roster before pick 1. It had the keeper *rule* and not the
keeper *list*.

## 2. FOUR TEAM ASSIGNMENTS ARE WRONG, AND THREE OF THEM CARRY THE ARGUMENT

| player | report says | board **and** 2026 depth chart | why it matters |
|---|---|---|---|
| **Jaylen Waddle** | MIA | **DEN** | called "the most mispriced receiver in fantasy" on the wrong offence |
| **Dontayvion Wicks** | GB | **PHI** | its entire thesis is *"regardless of Green Bay's crowded receiver room"* — he is not in it |
| **Rico Dowdle** | DAL | **PIT** | "clearest path to goal-line touches in Dallas"; he is behind Jaylen Warren in Pittsburgh |
| **Charbonnet / Walker** | says Charbonnet's PUP "solidifies Kenneth Walker III's volume floor" | **Charbonnet is SEA, Walker is KC** | the event is real and already on our injury sheet; the inference is impossible |

This lands in the section the report calls its own *"player movement cross-check."*

## 3. THE ROUND ADVICE IS NATIONAL ADP, NOT THIS DRAFT

Its target windows come from public ADP, not from our keeper-depleted board. Measured against
`eff_pick`:

| its advice | reality here |
|---|---|
| Trey McBride "picks 32–41" | goes at **20** — gone before your pick 32 |
| Chase Brown "picks 32–41" | goes at **22** — gone |
| Parker Washington "picks 113–137" | goes at **86** — gone by round 10 |
| Tucker Kraft "picks 113–137" | goes at **80** — gone |
| Jonathon Brooks "picks 65–89" | goes at **108** — you can wait |
| Josh Downs "picks 89–104" | goes at **120** — you can wait |
| Pat Freiermuth "picks 128–137" | goes at **157** — you can wait |

Four of its named targets are already gone when it says to take them; three are free 15–30 picks
later than it claims. Also, two of the four pick-slot annotations are simply wrong arithmetic —
it calls pick 41 "Round 4, Pick 5" and pick 89 "Round 8, Pick 5". Both are slot 8.

## 4. THE PROVENANCE PROBLEM

Almost every specific claim cites footnote **1** or **2** — `favorite-analysts-calls-2026.csv` and
`raw-analyst-calls-v2.csv`, two files that are **not in this project** and that I have never seen.
The report's own audit section says those files contain 2024 sleeper lists, August-2025 entries and
phonetic transcription errors. So the bulk of it rests on a source of unknown vintage that the
report itself describes as contaminated. Of the nine web citations, one is a **2025** sleepers
article, three are podcast-transcript aggregators, and one is a generic cheat-sheet index page.

Per §1.1 this is exactly the shape of an unusable market source: confident, specific, and
undated.

## 5. WHAT IS ACTUALLY WORTH KEEPING

**Seven of its 21 UP calls also appear on our own residualised BUY list**, built from two
independent analyst panels. That agreement is worth something because the two were constructed
differently:

| player | pos | goes at | our note |
|---|---|---|---|
| Jaylen Waddle | WR DEN | 48.0 | BUY on both |
| Chase Brown | RB CIN | 21.9 | BUY on both — but he is a **pick-17 decision here, not pick 41** |
| Jonathon Brooks | RB CAR | 107.7 | BUY on both, behind Chuba Hubbard — already the top name on the late-RB sheet |
| Parker Washington | WR JAX | 85.5 | BUY on both |
| Josh Downs | WR IND | 119.8 | BUY on both |
| Jalen Coker | WR CAR | 148.4 | BUY on both |
| Malik Willis | QB MIA | 154.7 | BUY on both, and irrelevant — we take one QB |

Its **Sam LaPorta fade agrees with our injury sheet** (AVOID, back). Its Bucky Irving and DJ Moore
fades are unsupported here — neither is flagged on our side, and no reason it gives is checkable.

**Nothing on the board was changed as a result of this file.** The one genuinely new item it
raises — Luke Musgrave to PUP elevating Tucker Kraft — is worth a look on the Sept 5 sweep, but
Kraft is already graded AVOID on our own injury sheet for a November ACL, so it does not move him.

---

## 6. THE LESSON, WHICH IS NOT ABOUT THIS FILE

This is a well-written document that is wrong in the specific ways a generated document is usually
wrong: **stale rosters, national ADP substituted for the actual market, and a confident tone over
sources it cannot show.** Every error above was found by joining it to data we already had — the
board, the depth charts, the keeper list — in about ten minutes.

**The rule for anything like this from here to Sept 7: it may add names to read about. It may not
add numbers, rounds, or teams.** Those come from the board, and the board gets corrected through
`news_overrides.csv` with a source attached.
