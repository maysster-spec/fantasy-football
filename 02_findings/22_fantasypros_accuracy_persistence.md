# 22 — DOES ANALYST DRAFT ACCURACY PERSIST?  [SUPERSEDED]

> **RETRACTED 2026-08-23 by `claude/24_accuracy_powered_test.md`.** This doc used top-30
> overlap as a proxy because the full tables were not loaded. They now are. On the full
> tables the 2024→2025 persistence this doc calls "nothing (p=0.78)" is **Spearman +0.268,
> p=0.0004, n=173**. The headline below — *"it stopped working last year"* — is wrong.
> The underpowered-proxy warning in the LIMITS section was right and should have been
> weighted higher. Read doc 24 instead. Kept for the audit trail.
**Aug 23, 2026.** Pulled live from your FantasyPros session via the browser.
`[SOURCED: fantasypros.com/nfl/accuracy/draft.php, captured 2026-08-23]`

This is the question the project has been stuck on: *which analysts should the board weight?*
It is now tested rather than assumed.

## THE ANSWER

**Weakly, and it stopped working last year.**

| year pair | repeaters in both top 30 | expected by chance | p |
|---|---|---|---|
| 2022 → 2023 | **9** | 3.8 | **0.0058** |
| 2023 → 2024 | **8** | 3.9 | **0.0227** |
| 2024 → 2025 | **3** | 3.8 | **0.78 — nothing** |

Three tests, so the Bonferroni threshold is p < 0.0167. **Only 2022→2023 clears it.**

**Nobody finished top 30 in all four years.** Six did it in three of four:

`Jared Smola - Draft Sharks`
`Jeff Ratcliffe - FTN`
`Jody Smith - Draft Sharks`
`Joe Bond - Fantasy Six Pack`
`Sean Koerner - The Action Network`
`Wolf of Roto Street - Roto Street Journal`

**Independent replication (B3).** FantasyPros' own Multi-Year Draft Accuracy table, which I did
not use to build the list above, ranks: **1 Jody Smith · 2 Sean Koerner · 3 Joey Wright ·
4 Jeff Ratcliffe · 5 Dave Kluge · 7 Jared Smola.** Five of my six appear in its top seven.
The shortlist replicates on a second construction of the same data.

Position-specific accuracy from that table, which is more useful than the overall rank:
**RB — Jody Smith (1), Ryan Weisse (2), Chris Raybon (3), Kev Wheeler (4).**
**WR — Jeff Bell (1), Sean Koerner (6), Joey Wright (7), Nick Mariano (8).**
**TE — Dave Kluge (3), Jody Smith (9), Ryan Weisse (12).**
**QB — Sean Koerner (4), Joey Wright (15), Jared Smola (23).**

## THE PART THAT MATTERS MOST TO YOU

**None of the seven analysts you named as the ones who actually find breakouts appears in any
top 30, in any year:** Harmon, Zachariason, Siegele, McFarland, Silva, Gretch, Hartitz.
**Neither does Boone.**

This is not evidence that they are bad. It is evidence that **the accuracy contest and
breakout-finding are different skills measured by different instruments** — which is what
`HANDOFF_v2` §4 argued and this now supports with data. The contest scores closeness to the
final order. Being right about one player nobody else saw barely moves that score.

**So there are two separate questions and only one of them now has an answer:**
1. *Who ranks the field most accurately?* → the six names above, weakly, and the signal broke
   down in 2025.
2. *Who finds breakouts?* → **still unanswered, and the accuracy contest cannot answer it.**

## LIMITS

- Three year-pairs. Top-30 is an arbitrary cut; a different cut could move the result.
- Matched on the displayed `Name - Site` string. An analyst who changed employer between years
  reads as two different people, so **every overlap count above is a lower bound.** Andy
  Behrens and Dalton Del Don both appear under The Deep Shot in different years — exactly this
  pattern. This is `ERROR_PATTERNS` C1 in a place where I could not avoid it.
- The ranked population shrinks each year: 247 → 236 → 225 → 212.
- The powered version of this test is a **rank correlation across the full table**, not top-30
  overlap. That needs the whole table, which the browser channel cannot move — see below.

## HOW TO GET THE POWERED VERSION — one click

Every accuracy page has a **`Download data`** button, an icon at the top right of the table,
next to the printer icon. The pages are:

`https://www.fantasypros.com/nfl/accuracy/draft.php?year=2022`
`https://www.fantasypros.com/nfl/accuracy/draft.php?year=2023`
`https://www.fantasypros.com/nfl/accuracy/draft.php?year=2024`
`https://www.fantasypros.com/nfl/accuracy/draft.php?year=2025`
`https://www.fantasypros.com/nfl/accuracy/multi-year-draft.php`

The `?year=` parameter works — I verified all four load the right year. One click per page,
five files, and the full-table rank correlation replaces the top-30 overlap test above.
