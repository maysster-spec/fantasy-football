# 405 — There is no Tuesday run. He asked the one question, and the rule had the sign backwards.

*23 Sept 2026. Directive v9.25 → v9.26. The Sunday-night placement rule, live since v9.15 and repeated by me a
dozen times today, is retracted in full. Ledger row 179.*

---

## 1. THE QUESTION

> **Matt: "Sunday's claims? Why would i place a claim on Sunday??"**

Nine words. The rule had been in §2 since 20 Sept, in `matt_todo.txt` as a STANDING item, in findings §4.36's
title, and in four of my replies today.

---

## 2. THE MEASUREMENT

**Population: this league, every WAIVER transaction with Status EXECUTED, 2022 to 2026, n=626.** `Date` on an
executed row is the execution timestamp — confirmed because every one falls between 03:00 and 06:00, while PENDING
rows spread across all 24 hours, which is people placing claims.

| claims execute | n | share |
|---|---|---|
| **Thursday, 03:00 to 06:00 ET** | **540** | **86.3%** |
| Friday to Sunday (secondary cycle) | 86 | 13.7% |
| **Monday, Tuesday or Wednesday** | **0** | **0.0%** |

**By season, Thursday: 115 · 117 · 158 · 139 · 11. Every season. Zero Mon/Tue/Wed in any of them.**

Placements, for contrast (PENDING rows, `Date` = when entered): Tuesday 120, **Wednesday 174**, Thursday 21.
**The league already places Wednesday night.** So does Matt — his own claims are stamped Tuesday 23:00, Wednesday
23:43, Monday 23:07.

---

## 3. WHAT THIS KILLS

**The placement day does not choose the run. The run is Thursday.** A claim placed Sunday night and a claim placed
Wednesday night land in the same batch.

So the Sunday rule's entire benefit was imaginary, and its cost was real:

| | Sunday night | Wednesday night |
|---|---|---|
| when it runs | **Thursday** | **Thursday** |
| Sunday night football | not seen | seen |
| Monday night football | not seen | seen |
| Tuesday + Wednesday practice reports | not seen | seen |
| Monday and Tuesday drops in the pool | not available | available |

**The rule was not "free and therefore dominant". It was strictly dominated, with the sign backwards.**

→ **PLACE CLAIMS WEDNESDAY NIGHT.**

---

## 4. THE SENTENCE NOBODY TESTED

`Waiver Period: 2 Days`, settings line 125.

I read it as **how long a CLAIM waits**. It is **how long a PLAYER sits on waivers after being dropped.**

Today's own pull is the confirmation and I looked straight past it this morning: **all 283 unowned players share
ONE clear time, 24 Sept 03:00.** That is not 283 individual two-day clocks started on 283 different days. It is one
cohort that went on waivers together and clears together.

---

## 5. WHY THIS IS THE WORST OF THE THREE

§0.5(a5) exists because of this exact failure on 22 Sept, and this is its third instance in two days.

**The ring was measured, and measured well:** the settings line was quoted for the first time in the project's
history, the D+2 reading was "confirmed" against three of his own pending claims, the seat life got n=1,431, the
injury-report timestamps got their own script and a retraction.

**The centre — that the placement day determines the run day — was never tested.**

And unlike 22 Sept's centre, which genuinely needed a live observation, **this one was answerable in one query
against a file that has been on the drive all season.** I opened `waiver_report_*.csv` four separate times today —
for the drop rule, for the claim-order gradient, for the D/ST regex trap, for the free-agent question — and never
once asked it which day claims actually run.

**The "confirmation" was the tell I missed.** Three claims placed Tuesday and processing Thursday is consistent
with D+2. It is equally consistent with "everything runs Thursday". I had a fact that fit two models and treated it
as evidence for the one I had already written down.

---

## 6. AND THE FILE SAID IT OUT LOUD

The directive's DO-NOT-QUOTE table has carried this as a live retraction since v9.15:

> *"the injuries feed lands after the Tuesday run"* → **"there is no Tuesday run."**

And §2's own placement table, two screens below it, said:

> **"Sunday night → Tuesday morning"**

**v9.21's batch A was a sweep for exactly this class of defect** — the resident set contradicting itself — and it
did not catch this one, because that sweep compared files against files and this contradiction needed a
measurement to resolve which side was wrong. **A consistency check cannot tell you which of two disagreeing
statements is the true one.** That is a real limit on batch A's method and it belongs next to it.

---

## 7. WHAT DOES NOT CHANGE

- **Put a drop on every claim** (884 for 884 with one, 6.1% failure without). Unaffected.
- **Rank the contested man first**, as a dominance argument with no number attached. Unaffected: ESPN still demotes
  a winner mid-run, whichever day the run happens.
- **The IR material** — the sourced ESPN rules, the seat-validity curve, the 24.5% lineup freeze. All measured
  independently of the clock, all stand.
- **Thursday morning roster check** when claims process. Now better founded, since Thursday is *the* run day rather
  than one possible run day.

---

## 8. HOUSEKEEPING

A defect in this run, caught by counting (§9 rule 6): the first attempt to banner findings §4.36 matched the string
`4.36 ` inside a prose sentence instead of the finding's heading and landed mid-paragraph. Redone from a clean
drive copy against the real `**[v9.15] 4.36` anchor and verified to sit before it.

Fixed in: §2's CLOCK block (replaced), the DO-NOT-QUOTE table (new row), findings §4.36 (banner at its heading, the
D+2 model voided, (g)(h)(i) untouched), `matt_todo.txt` (the STANDING Sunday item closed with its reason, replaced
by the Wednesday one), and the changelog.
