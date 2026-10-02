# 46 — SECOND PROJECTION SOURCE: ESPN AND FANTASYPROS AGREE (r = 0.982)
**Aug 25, 2026.** Doc 45 named this the largest open gap: the board rested on one vendor's
projection, and doc 44 had shown that vendor's greedy rule loses to real managers. B3 requires a
load-bearing number be replicated on a second source. **Done — pulled live via the browser
session, no manual export needed.**

## METHOD
FantasyPros consensus **projections** (not rankings) scraped for QB/RB/WR/TE — 524 players —
as raw stat lines: passing yards/TD/INT, rushing yards/TD, receptions, receiving yards/TD,
fumbles lost. **This league's scoring was then applied to those raw stats** (0.04/pass yd,
6/pass TD, −2 INT, 0.1/rush+rec yd, 6/TD, 0.5 PPR, −2 FL) — the identical scoring map the ESPN
pull uses. FantasyPros' own FPTS column was discarded; it is standard scoring and wrong for
this league. Replacement levels recomputed independently on the FantasyPros pool.

**POPULATION:** the 139 non-K/DST players inside board_v7's top 220 that appear in both sources.
**SAMPLE:** n=139. **Name match: 139 of 139, zero unmatched** (suffix-normalised join).

## RESULT — THE TWO SOURCES SUBSTANTIALLY AGREE

| | ESPN | FantasyPros |
|---|---|---|
| QB12 replacement | 341.6 | **345.3** |
| RB30 replacement | 168.6 | **166.6** |
| WR30 replacement | 163.5 | **165.0** |
| TE12 replacement | 140.3 | **137.3** |

Replacement levels — computed independently, on different player pools — land within 3 points of
each other at every position. That is a meaningful independent check on the VBD machinery itself.

- **Pearson r between the two VBD columns: 0.982** (n=139)
- **Median rank shift: 5 places. Max: 30.**
- Mean VBD gap by position: QB −0.2 · WR −1.1 · RB −1.8 · **TE +5.0**

**The top of the board is nearly identical.** ESPN's top 10 versus FantasyPros' ranks: Gibbs 1/1,
Bijan 2/2, McCaffrey 3/3, Nacua 4/5, Taylor 5/4, Chase 6/6, Smith-Njigba 7/7, St. Brown 8/9,
Henry 9/8, Cook 10/11. **No pick-8 decision changes.**

## WHERE THEY DISAGREE — THE ONLY PLACES WORTH LOOKING

**FantasyPros higher (ESPN may be underrating):**
Kyler Murray QB +20.4 · **Bijan Robinson RB +17.5** · **Bucky Irving RB +16.8 (ADP 54.5)** ·
RJ Harvey RB +16.3 · **Drake London WR +16.1 (ADP 18.6)** · Dalton Schultz TE +15.2 ·
**Trey McBride TE +15.0 (ADP 20.4)** · Mike Evans WR +14.8 · **Kyle Pitts TE +13.9 (ADP 65.2)**

**FantasyPros lower (ESPN may be overrating):**
**Breece Hall RB −23.5 (ADP 33.1)** · Carnell Tate WR −20.7 · **CeeDee Lamb WR −19.3 (ADP 10.7)** ·
Matthew Golden WR −19.1 · Blake Corum RB −18.5 · **Justin Jefferson WR −16.9 (ADP 12.1)** ·
**Jeremiyah Love RB −15.8 (ADP 21.7)** · **Puka Nacua WR −15.0 (ADP 5.1)** ·
Matthew Stafford QB −13.2 · **Ashton Jeanty RB −12.9 (ADP 16.6)**

**The TE +5.0 systematic gap is the one structural finding here** — FantasyPros rates tight ends
about 5 VBD points higher across the board, and four of the twelve largest positive gaps are TEs
(Schultz, McBride, Pitts, Juwan Johnson). This is a *different* claim from §4.4's TE divergence,
which measured board-vs-ADP; this is projection-vs-projection and is new.

## WHAT THIS DOES AND DOESN'T SETTLE

**Settles:** the board is not an artifact of one vendor. At r=0.982 with matching replacement
levels, ESPN's projection is not idiosyncratic, and doc 45's "single-source risk" is closed.

**Does NOT settle:** agreement is not accuracy. Both sources could share the same blind spots —
consensus projections are correlated by construction, since FantasyPros aggregates analysts who
read the same information. **Doc 44's finding stands unchanged:** a greedy rule built on *either*
projection would still have lost to these managers once injury luck is removed. Two sources
agreeing tells you the input is stable, not that it is right.

**Practical read:** trust the board's ordering. Where the two disagree by more than ~15 VBD —
Breece Hall, CeeDee Lamb, Drake London, Trey McBride, Bucky Irving — treat the pick as genuinely
uncertain rather than as a number, and let judgment decide.

## LIMITS
1. Consensus vs consensus. Not independent in the strict sense — overlapping analyst pools.
2. FantasyPros' half-PPR page was used as the stat source; the raw stat lines are scoring-agnostic,
   but any position-scarcity assumptions baked into their projections are not.
3. K and D/ST not compared — FantasyPros does not publish comparable stat lines, and per
   `code_kdst_guard` those positions carry no cross-position VBD anyway.
4. n=139, restricted to board_v7's top 220. Deeper players were not compared.
5. Captured 2026-08-25. Re-pull at the Sept 5 refresh.
