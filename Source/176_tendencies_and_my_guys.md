# 176 — League tendencies beyond ADP, and every "My Guy" placed

**Date:** 2026-09-05 (Sat night ET) · Run without prompting, per Matt's instruction.

---

## PART 1 — THE RED-TEAM CATALOG, STATE OF PLAY

| ladder | check | state |
|---|---|---|
| A1–A6 | board data vs today's pull | **DONE** (doc 173). 6 rows cross the printed cut; **23 injury flags stale**; ADP verified correct |
| **A7** | **positional draft speed vs keeper-adjusted ADP** | **DONE** (doc 175). WR +5 significant, RB null |
| **A8** | **first-at-position timing, D/ST and K** | **DONE — below** |
| **A9** | **§4.7 and §5 audited against the draft history** | **DONE, then CORRECTED by doc 180 — one claim wrong, not two** |
| B1 | the nine "My Guys" | **DONE — below** |
| B2 | the 23 stale injury flags, in pick order | **PENDING** — the largest remaining surface |
| B3 | AVOID/DISCOUNT grade dates (sweep is 08-31) | pending |
| B4 | Gemini-sourced claims re-verified | pending |
| C1–C4 | this week's changes carried through | pending |

## PART 2 — D/ST: MATT'S LEAD IS RIGHT, AND IT EXPIRED TWO YEARS AGO

*"I do know that more than one team drafts D/ST earlier."* Teams taking a D/ST **before round 11**:

| season | teams early | first D/ST |
|---|---|---|
| 2021 | 3 | round 8 |
| **2022** | **7** | round 7 |
| **2023** | **5** | round 6 |
| **2024** | **1** | round 10 |
| **2025** | **1** | round 10 |

**The behaviour was real and it collapsed.** In 2022–23 nearly half the league reached; in the last
two drafts exactly one team did, and never before round 10. **Matt is remembering 2022.**

**This supports his current plan rather than threatening it.** He takes D/ST at **152 = round 13**,
and the pooled distribution puts the mass at rounds 11–13 (14, 16, 18 picks). §4.8 stands anyway:
11–12 of 12 teams stream, so draft-day D/ST value is not realisable and being last costs nothing.
**No change. Stay at 152.**

**K:** median first-K round **14**, and 32 of 59 first-kickers come in round 14. **161 is exactly
right.** One manager once took a kicker in round 5.

## PART 3 — §4.7 AND §5 AUDITED

> **[CORRECTED 2026-09-05 by doc 180. THE ORIGINAL VERSION OF THIS SECTION WAS WRONG IN THREE
> WAYS AND ITS HEADLINE — "TWO CLAIMS ARE WRONG" — DID NOT SURVIVE RE-DERIVATION.** It (1) counted
> TE picks in **rounds 1–3** and reported them against a directive claim about **before round 3**,
> i.e. rounds 1–2 — `ERROR_PATTERNS` **A14**, a convention-dependent count reported without its
> convention; (2) **counted KEEPER rows as draft selections.** In 2021–2023 the keeper was charged
> to **round 1**, so every "round 1 TE" in those years is a keeper, not a pick — §4.7's population
> is explicitly "true draft selections only"; and (3) **listed two rows that are not in the file**
> — "2021 Brown/Collins r3 Waller" and "2023 Wilson Kam r3 Andrews" do not exist in
> `draft_history_2021_2025.csv` — `ERROR_PATTERNS` **B5**. The text below is the re-derivation.]

**Every TE selected in rounds 1–3, keepers excluded, 2021–2025 — the complete list, n=60
manager-seasons:**

| year | manager | rd | overall | player |
|---|---|---|---|---|
| 2021 | Buffalow Expectations *(2021 identities are unresolved — see below)* | 2 | 22 | Kelce |
| 2021 | Wilson Kam | 3 | 35 | Kittle |
| 2022 | **Cary** | 3 | **30** | Kelce |
| 2023 | Pierce *(departed)* | 2 | 20 | Kelce |
| 2025 | **herman allen** | 2 | **22** | Bowers |
| 2025 | *Matt Mays* | 3 | 35 | Kittle |

**On the directive's own convention (before round 3 = rounds 1–2): 3 of 60 all years, 2 of 48 on
2022–2025.** §4.7's "1 of 43 team-seasons" is not reproducible on this file under any convention I
can construct, and has been replaced in the directive with **2 of 48**.

**2021 CANNOT BE ATTRIBUTED AT ALL.** Six of that season's twelve `Manager` values are TEAM names
("Buffalow Expectations", "Antonio Gimpshin", "CeeDee Lambs", "Charlotte SweatyBallerz", "Nick
Cannon FanClub", "Sutton My Face Until I Kareem"). The 2021 Kelce-at-22 pick belongs to somebody,
but the file does not say who. Every manager-level statement here is therefore **2022–2025 only**.

**§5's "herman allen is the league's ONLY true early-TE manager" SURVIVES as written** — for
rounds 1–2 he is the only *current* manager who has ever done it, and the other two instances
belong to a departed manager and to an unattributable 2021 row. **The line stays; the directive
now carries a note under §5's table saying what it does NOT mean.**

**WHAT IS ACTUALLY TRUE, AND IT STILL LANDS ON PICK 32.** Matt's pick 32 is **round 3**, so the
round-1–2 framing is the wrong lens for his decision. First TE by **overall pick**, 2022–2025,
true selections (n=45): **3 of 45 at ≤32, 6 of 45 at ≤41.** The managers holding picks between
Matt's 17 and his 32 are **Wilson Kam (19, 30) · herman allen (20, 29) · Cary (24, 25)** — and of
those three, **allen has gone TE at overall 22 and Cary at overall 30.** Kam's earliest is 35.
**Brown/Collins is NOT a threat — his earliest first-TE is overall 45**, contrary to the original
version of this section. Rychlicki is out this year regardless: Loveland is his keeper.

**So: two of the three managers picking in that window have taken a TE at or before overall 30.**
That is a weaker claim than this section first made and a real one.

**Read together: do not plan on Bowers or McBride at 32.** §7's rule still governs — *any of the
five, first one showing* — and both the grid and this now say the one showing is **Judkins**, who
the grid draws at exactly cell 32. **§7's verdict is untouched; this only predicts which name it
resolves to.**

## PART 4 — EVERY "MY GUY", PLACED AGAINST MATT'S TURNS

| player | host | VOR | grid cell | his turns | verdict |
|---|---|---|---|---|---|
| **Colston Loveland** TE | Mike | — | — | — | **KEEPER (Rychlicki). Not draftable at any price. Dead.** |
| **Omarion Hampton** RB | Jason | **+67.3** | **17** | 8, 17 | **Drawn exactly on your pick.** Coin flip. If he is there, he is the second-best VOR available |
| **Kenneth Walker III** RB | Mike | **+81.2** | **19** | 17, 32 | **Best available VOR at 17 by any position bar Allen.** Two picks early — a reach the board endorses |
| **Garrett Wilson** WR | Jason | **+36.4** | **31** | 32 | **One pick before yours** — and he is the best WR available at 32. Borderline; the WR +5 tendency helps |
| **Ladd McConkey** WR | Andy | +17.7 | **37** | 32, 41 | Between your turns. Reach at 32 or hope at 41 |
| **Carnell Tate** WR | Jason | +1.6 | **60** | 56, 65 | Between. **Board says ACTIVE, ESPN says QUESTIONABLE** — collision stiffness, missed practice Sept 1 `[SOURCED: NBC Sports, 09-01]`. Beat reporting says "expected to be fine" |
| **Caleb Williams** QB | Andy | −9.7 | **66** | 65, 80 | A QB2-tier body, not a QB1. Relevant under §4.18 at 104/113, not here |
| **Christian Watson** WR | Mike | −5.9 | **71** | 65, 80 | On the VALUE LADDER with BUY. **Carries DISCOUNT and played 10 games in 2025** (§4.22e: −16.9 for that band) |
| **De'Zhaun Stribling** WR | Andy | −54.6 → **−29** | **111** | 104, 113 | Between. Hamstring tightness, returned to practice; was making a case to open as **WR2** `[SOURCED: 49ers Webzone]`. VOR is 26 points better than the board prints |

**THE CONVERGENCE WORTH KEEPING.** At **pick 17** the Footballers' two running backs — Hampton and
Walker — are drawn at cells 17 and 19, and the board independently says the best available VOR at 17
is **Walker +81.2**. Three unrelated sources agree on the same turn. **At pick 32**, §7's dollar
simulation, the grid's corrected placement, and the early-TE manager history all resolve to
**Judkins**.

**Eight of nine are live at one of his turns. The ninth is a keeper.**

## PART 5 — WHAT IS STILL OPEN

**B2 is the big one: 23 stale injury flags inside the printed 180, seven at picks 8–65.** That is a
larger surface than anything found tonight and it needs external verification per name, so it
batches. Ja'Marr Chase at board rank 6 now reads QUESTIONABLE on ESPN's own feed.
