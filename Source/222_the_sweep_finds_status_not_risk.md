# 222 — Nacua's suspension review: the sweep asked the right question and read the wrong sources

**2026-09-08 (draft +1).** Matt sent the New York Post piece on Nacua addressing his anxiety over a
possible suspension and said *"we seem to have missed this."* **He is right. We did, twice, and the
reason is not the one I first reached for.**

---

## 1. WHAT IS ACTUALLY TRUE, WITH DATES (`ERROR_PATTERNS` B7)

- **2026-03**: a woman filed a civil suit alleging Nacua bit her and a friend on **2025-12-31** and
  made an antisemitic remark. He denied it and entered a rehabilitation programme. **No criminal
  charge.** *(CBS Sports, 2026-09-03)*
- **2026-08-11**: **Adam Schefter reported a suspension was "within the realm of options."**
  *(NBC Sports player news, 2026-08-11)* — **twenty days before our sweep ran.**
- **2026-09-03**: the NFL is reviewing him under the personal conduct policy; no discipline issued;
  the commissioner exempt list was never seriously considered. *(CBS Sports, 2026-09-03)*
- **2026-09-07**: Schefter — *"He's gonna be out there against the San Francisco 49ers. Doesn't
  sound like he's going to face any discipline this year right now."* *(Newsweek, 2026-09-07)*

**Bottom line for the roster: no action. He plays Thursday 2026-09-10 against San Francisco.**
The league can still act at any point in the season, and the civil case is unresolved.

---

## 2. THE DIAGNOSIS I NEARLY SHIPPED WAS WRONG (§0.2 — a diagnosis is a claim)

**My first read was "the sweep only asked about injuries."** One `grep` killed it.
`GEMINI_INJURY_SWEEP.txt` line 41 asks for *"illness, holdout, suspension, legal matter, or a
placement on PUP / NFI / IR"* and line 56 gives **`SUSPENDED / EXEMPT_LIST / HOLDOUT`** as
permitted status values. **The scope was right and the vocabulary was there.**

## 3. THE REAL DEFECT: THE SWEEP FINDS *STATUS*, NOT *RISK*

`sweep_20260831.csv`, Nacua's row, in full:

```
status_now = HEALTHY          injury_current = Groin        risk_grade = NEUTRAL
one_line   = Returned to practice from a groin injury.      confidence = HIGH
source_url = en.as.com/nfl/fantasy-football-injury-report-16-players-who-could-change-your-2026-draft
```

**One source, and it is an injury-report aggregator.** A page that lists injuries cannot report a
conduct review, so the suspension vocabulary had nothing to fire on.

**And the contrast inside the same file proves the mechanism.** Of 143 rows, exactly one came back
non-injury: **Josh Jacobs, `EXEMPT_LIST`** — *"Placed on Commissioner's Exempt List after May
arrest; expect suspension,"* sourced to a roster-cutdown tracker. **Jacobs had a TRANSACTION.
Nacua had a REVIEW.** A transaction has a status field and appears on trackers; a pending review
has neither and appears only in reporting.

> **The rule this earns: a sweep keyed on STATUS is blind to RISK, and availability risk is not
> only medical.** §4.22 measures availability as the strongest downside signal in this project
> (−19.4 points, p=0.00004, n=735) — and every instrument we built for it reads a medical source.

**It failed twice, not once.** The Sept-3 news pass reached the same row and also returned only the
groin. Two passes, both pointed at injury sources, both silent — and the player card's bear line
ended up reading *"anxiety about his conditioning,"* which is the right word attached to the wrong
subject.

---

## 4. WHAT IT WOULD HAVE CHANGED ON THE NIGHT: NOTHING, AND THAT IS NOT THE POINT

Pick 8's rule is **highest VOR on the board** (§7, doc 200). Nacua at **+131.3** leads Taylor
(+122.5) and St. Brown (+101.3). A discount large enough to move him below Taylor would need to be
about **9 points**, and the honest pre-draft estimate — *no charge issued, no discipline expected,
a first offence under the personal conduct policy* — is nowhere near that.

**So this is a process defect with a measured cost of approximately zero on Sept 7.** Reporting it
anyway, per §0.2: report the defect, then measure, then report the cost. **The cost is in the
season, not the draft** — if discipline lands in November, a suspended player is **not IR-eligible**
on ESPN, so he occupies one of six bench spots while scoring nothing, on a roster already carrying
six running backs.

---

## 5. THE FIX, FOR THE SEASON AND FOR NEXT AUGUST

1. **A second axis on any sweep: a per-player news query that is not injury-shaped** — conduct
   review, legal matter, holdout, discipline — run against general reporting, not injury trackers.
   Silence there must be reported as `NO NON-INJURY NEWS FOUND`, the same way `HEALTHY` is, because
   silence is the failure mode the sweep exists to fix and it recurred on a second axis.
2. **`confidence = HIGH` must not be issued off one source.** Nacua's row was HIGH on a single
   aggregator page. Confidence should be a function of independent sources, not of how clean the
   one page read.
3. **Post-season, not now:** whether a pending conduct review is priced by the market at all. It is
   testable on the §1.1 registry — players under public review before a draft, against their beat —
   but the population will be small and it is not a draft-week question.

**Open, and named so it is not dropped (§0.5(e)): the Nacua review is unresolved, and the civil
suit is unresolved. This is a weekly watch item, not a closed file.**

---

*Sources, with dates stated before use: CBS Sports suspension watch (2026-09-03) · NBC Sports
player news, Schefter (2026-08-11) · Newsweek, Schefter (2026-09-07) · New York Post (2026-09-07,
supplied by Matt; the site blocks retrieval here and it was corroborated from the three above).*
