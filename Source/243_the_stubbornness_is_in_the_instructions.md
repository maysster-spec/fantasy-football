# 243 — When to stop pushing: the answer is a ledger, and my stubbornness is written into my own instructions

**2026-09-09.** Matt: *"I don't know when to keep applying pressure to mine front more information
and when to take responsibility for gathering that information... later on you do find a way to
pluck out some indicators that you didn't think you could before. I still hold out hope that I can
explain more of the logic... I'm running out of ideas and you are getting stubborn with it."*

And the line this doc exists to answer: *"however, what I'm hearing now is that list should not go
on."*

**No. The list goes on. What changes is that every item on it gets logged instead of relitigated.**

---

## 1. THE MECHANISM OF MY STUBBORNNESS IS A STALE SENTENCE IN THE DIRECTIVE

§0.5(a2) carries this, under *"His record says WHERE to aim"*:

> **A causal MECHANISM he proposes is a HYPOTHESIS.** The offensive line, opportunity environment,
> the year-two bounce-back, "our league is RB-heavy" — **all tested null.** Test them; report the
> death.

**That was written when those four were the only mechanisms on the board, and it has not been
updated since.** It tells every future session to expect his mechanisms to die. It is the reason a
new idea of his meets resistance rather than a test — and it is now **wrong on the record.**

Counted honestly, every mechanism Matt has proposed that got tested:

| his mechanism | verdict |
|---|---|
| Injuries matter | **CONFIRMED, and it is the strongest downside signal in the project** — ≤12 games last season = −19.4, p=0.00004 (§4.22c / v7.9) |
| The market is anchored on last year | **CONFIRMED** — last year loads +0.093/+0.263 after the projection, and fading it loses (§4.22b) |
| Ageing acts through availability, not age itself | **CONFIRMED** — age 28+ is −3.8, p=0.39; games missed is −19.4 (§4.25b) |
| "The signal varies by player" | **CONFIRMED** — among established veterans availability does not predict at all, p=0.59 (doc 204) |
| An ageing QB throws shorter while still starting | **CONFIRMED** — rho −0.196, p=0.009 (§4.25b) |
| Vacated targets must matter | **mean NULL, TAIL REAL** — 29% of returning receivers on high-vacated teams gain (docs 196/198) |
| "Signals play off each other, not standalone" | **frame CONFIRMED**, direction corrected — they substitute, they do not compound (§0.5a3) |
| "Wait for a bench player to pop before trading" | **CONFIRMED with a condition** — a pop carries forward only when the WORKLOAD popped: +2.65 vs +0.20 (doc 235) |
| One injury away / the handcuff | **CONFIRMED and large** — next man up 13.62 ppg vs 6.32, +7.30 [+6.01, +8.70] (doc 236) |
| "Holding Spears was negative value" | **CONFIRMED** — ≈ −5 (doc 240) |
| "Cary's grade is bad because you can't measure upside" | **CONFIRMED** — 81% of the grade's back-half comparator was a tight end (doc 242) |
| "I'm sure Mahomes wears some kind of brace" | **CONFIRMED, and I had said no on two sources** (doc 237) |
| The age cliff at RB (Henry) | **UNDERPOWERED, not disproved** — −12.1, p=0.209, direction his way (§4.25) |
| Offensive line → QB | payoff **NULL and UNDERPOWERED**; but his premise was right — sack rate is the most persistent team trait measured here, r=+0.399 (§4.24) |
| Offensive line → RB | **NULL** (doc 28) |
| Opening-day OL injuries | **NULL**, and structurally untestable — half of every line turns over (§4.24c) |
| Opportunity environment | **NULL as a flag** — 7.5% of variance; RB direction reversed (§4.21) |
| Year-two bounce-back (Barkley) | **NULL** — and Barkley was a 17-slot premium, never a discount (§4.22d) |
| Incumbent worse off than challenger (Kyren) | **NULL**, leans the other way; the VARIANCE is his story (§4.20) |
| "Our league is RB-heavy" | **NULL** |

**Twelve confirmed or partly confirmed, one underpowered-his-way, seven null.** `[COUNTED from the
directive's own §4 and docs 235–242]`

**So the directive's line is not just stale, it is backwards as a prior.** On a mechanism he is
better than a coin flip. **And on the narrower question — "is this answerable at all?" — he has been
right nearly every time**, which is the distinction the directive never drew and the one his
question is actually about.

---

## 2. WHAT ACTUALLY HAPPENED EACH TIME HE PUSHED PAST A "NO"

These are the cases he is remembering. In none of them was his mechanism simply right; in all of
them **the thing I said could not be measured turned out to be measurable, in a form neither of us
had stated yet.**

| I said | he pushed | what the push actually produced |
|---|---|---|
| Injury flags can't be tested — historical `injuryStatus` is stamped at capture, not preseason (doc 42) | kept pressing on injuries | **games played last season** carries no such contamination. Now the project's largest downside coefficient |
| The offensive line is dead — "continuity churn is r=−0.01" (doc 28) | pressed on the line anyway | continuity is personnel; **sack rate is performance**, and it persists at +0.399. The dismissal used the wrong variable |
| Vacated targets: NULL, r=+0.125, p=0.50 | "I can't believe it doesn't matter" | I had measured the **mean**. He meant the **tail**, and the tail is real |
| Age is dead — continuous fit across all RBs | "the age cliff" | a cliff is a **tail**, not a slope. Re-tested: underpowered, not disproved, and honouring his rule costs 0.0 points |
| QB2 has never been measured (doc 88) | pressed | doc 12 already held **951 measured waiver adds**. The answer existed and I had not looked |
| Pick 8 is closed, St. Brown, 10/10 and 96/100 | "why does my pick-8 cell say Nacua?" | every published run had removed the three players who beat St. Brown **by construction** |
| Cary drafted badly, −109.6, last of twelve | "you don't have a way to measure upside" | the grade's answer to 81% of the back half was *take a backup tight end* |

**The common shape: I answered the question I had framed, and he was pointing at a different
object.** That is §0.5(a2) failing seven times. (a2) tells me to state the testable form before
running the test — it does not tell me to state it before saying **"that cannot be tested."** That
is the hole.

---

## 3. THE RULE — AND IT BELONGS ON MY SIDE, NOT HIS

**He should not have to decide when to stop pushing.** The stopping condition is mine to supply.

> **FOR EVERY MECHANISM HE PROPOSES I OWE EXACTLY ONE OF THREE ANSWERS, AND "THAT ISN'T
> MEASURABLE" IS NOT ONE OF THEM.**
> 1. **TESTED** — population, baseline, n, direction, and the number. Including when it dies.
> 2. **NOT YET RUN** — with the testable form written down and queued.
> 3. **BLOCKED** — naming the **exact missing input**, where it would come from, and whether I have
>    tried to get it.
>
> **He stops pushing when the item is on the ledger with one of those three. Not before.**
> A "no" without a named blocker is a defect of the same class as an unmeasured severity claim
> (§0.4).

This is already in the directive twice — §0.2 ("label it HYPOTHESIS, not finding") and §4.24(b)
("report null, underpowered, AND what would resolve it: one of those sentences invites more data and
the other closes the file"). **It keeps failing because nothing tracks it.** §0.5(e) asks for open
threads in the last reply of a session; that is a paragraph, not a register, and paragraphs get
dropped.

**`02_findings_ledger.md` is not this file.** It records findings, and its own "KNOWN WEAKNESSES /
Never built" list still says the offensive line was never built — §4.24 tested it in v6.4. The
weakness list went stale the moment the work happened, which is what a findings ledger does to a
question list.

---

## 4. HIS MECHANISM TODAY IS MEASURABLE, AND THE DATA IS ALREADY DOWNLOADED

His words:

> *"if a player is younger and newer to the roster then the coach is more willing to give them the
> opportunity because they weren't happy with what they had"*

**THE TESTABLE FORM (§0.5a2) — one line, and the outcome is OPPORTUNITY, not points, because that
is what he said:**

> *Among two skill players competing for the same job, does the one who is both YOUNGER and NEWER
> TO THE TEAM take a larger share of that job than his price implies?*
> **POPULATION:** RB/WR/TE, 2021–2025, on a team that is not the team that drafted them —
> **≈270 player-seasons a year, ≈1,340 in total.**
> **OUTCOME:** his share of his team's touches (RB) or targets (WR/TE), weeks 1–14, minus what
> `log(preseason ADP)` predicts, fit within season.
> **DIRECTION:** positive.
> **FALSIFIER FIXED IN ADVANCE:** if the younger newcomer's share advantage is under 3 percentage
> points, the mechanism does not carry a pick and I say so.

**The input exists and is on disk here now.** nflverse `roster_20NN.csv` carries, per player-season:
`team` · `draft_club` (the team that drafted him) · `draft_number` · `years_exp` · `birth_date` —
**and `espn_id`, so it joins to our board on an id rather than a name (§3).** Verified populated:
espn_id on 847 of 972 skill rows in 2025, `draft_number` on 561, `birth_date` on 914, and
**276 skill players in 2025 are not on the team that drafted them.**

**"Newer to the roster" is `draft_club != team`. "Younger" is `birth_date`. Both are columns.** This
is not a mechanism that needed a source we do not have. It needed somebody to look.

**THE OTHER HALF OF WHAT HE DESCRIBED IS GENUINELY BLOCKED, AND I AM NAMING IT RATHER THAN WAVING
IT AWAY.** Contract year, an overpaid veteran at renewal, a player unhappy because he wants a ring:
none of that is in nflverse. Its `contracts` release **404s** (tried today,
`nflverse-data/releases/download/contracts/historical_contracts.csv`). It would need OverTheCap or
Spotrac, neither of which I have tested from this container. **Verdict: BLOCKED, input named, and
the fetch is mine to attempt — not his.**

---

## 5. WHAT I OWE HIM THAT IS NOT A TEST

**The automation he asked for is not a model. It is a register.** One file, every mechanism, its
testable form, its verdict or its named blocker, dated. Then:
- he can see at a glance what is open, and stop guessing whether to push;
- **I cannot quietly drop one**, which is the unconscious-bias problem he named, on my side rather
  than his;
- a null stays visible instead of being re-argued from memory six weeks later.

§1 of this doc is the first version of that register. It belongs in `Source\` as a standing file
with its own name, not buried in a numbered doc — that is the next build, and it is mine.

---

## 6. THE ONE PLACE I SHOULD PUSH BACK ON HIM

He wrote: *"for the most part I am using logic is just not logic I know how to transfer an all
areas."* Read through to intent (§0.5a): he is saying he reasons in a register he cannot always put
a number on. **That is not a weakness in the reasoning and he should stop apologising for it.** The
translation is my job — that is exactly what §0.5(a2) is for, and rule 7 of the retired handover
doc says the same thing: *"Do not take his framing as the task. Act on intent."*

**Where he is wrong is only this: "I'm running out of ideas."** He produced a testable one in the
same message, and the data for it was two `curl`s away.

---

## 7. OPEN THREADS THIS ADDS

- **The register itself** — §1's table promoted to a standing `Source\` file with a name, not a doc
  number.
- **The directive's §0.5(a2) F4 block must be corrected** — its "all tested null" line is the
  stale prior that produces the stubbornness. Drive copy pending; the bridge dropped mid-session.
- **The young-and-new test** — form stated in §4, not yet run.
- **Contract / motivation data** — BLOCKED, source unidentified, my fetch to attempt.
- Carried: the Aug-8 depth chart is a month stale (docs 236, 241, 242); the back half of
  `draft_analysis.json` needs a real comparator (doc 242); Jordyn Tyson's NFL draft round is in
  `draft_picks.csv` now downloaded but not yet joined.
