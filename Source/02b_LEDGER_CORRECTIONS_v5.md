# 02b — LEDGER CORRECTIONS, v5
**Aug 27, 2026.** Keep this file **beside `02_findings_ledger.md`**. Where the two disagree, this
file wins. Every entry traces to a measured result in docs 53–59.

---

## SUPERSEDED NUMBERS — do not quote the ledger's version of any of these

| ledger says | corrected | source |
|---|---|---|
| Replacement RB30 **168.0** | **168.589** | doc 57 — recovered as `proj − vbd`, constant to 6.6e-07 |
| Replacement WR30 **168.5** | **163.540** | doc 57 — the 168.5 came from a 200-row export the ledger's own F42 records as **39% fabricated** |
| Replacement QB12 **341.7** | **341.603** | doc 57 |
| Replacement TE12 **137.7** | **140.295** | doc 57 |
| Nacua VBD **+126.5** | **+131.3** | follows from WR replacement |
| McBride **+50.4** | **+47.6** | follows from TE replacement |
| Bowers **+53.3** | **+51.2** | ″ |
| Mark Andrews **+2.9** | **0.0** | ″ |
| Gibbs **+163.5** | **+162.3** | ″ |
| Opponent noise `sd = 0.135 × ADP` | **`sd = 0.30 × min(ADP, 70)`** | doc 53 + doc 55 §B1 — refit on 5 seasons of clean preseason ADP, CI [0.279, 0.363] |
| §2.1(c) pick 32: **5 keepers / eff ADP ~37** | **3 keepers / eff ADP ~35** | doc 58 — fixed point on the 08-23 keeper ADPs |
| §2.1(c) pick 80: 10 / ~90 | **11 / ~91** | ″ |
| §2.1(c) pick 89: 10 / ~99 | **11 / ~100** | ″ |
| §4.4 vs ESPN's board: QB +5.5, TE +5.0, RB +8.1, WR −6.4 | **QB +1.7, TE +8.5, RB +3.5, WR −6.3** | doc 45 — remeasured on the current board |
| "all four F1 replacement levels reproduce exactly" | **false** — WR was off by 5.0 | doc 57 |
| "Trades functionally dead — 3 league-wide per season" | the settings impose **no limit and no deadline**; the read is **behavioural**, not a rule | doc 56, `2026_League_Settings.txt` |

---

## RETIRED LINES OF INQUIRY — tested and dead, do not reopen

| idea | result |
|---|---|
| **Sleepers identified by ADP-vs-projection gap** ("the market is low on him") | rho **−0.079**, p=0.157, n=324. The coldest quintile breaks out at **3.1%** against ~11% for everyone else. Not just null — **directionally wrong** (doc 55) |
| Predicting *which* player breaks out, from anything on the draft board | three signals, three nulls (doc 55) |
| **VONA**, the published dynamic-VBD method | **−8.8** points vs plain constrained VBD (doc 54) |
| **A hand-set positional penalty** | **−5.7** points (doc 54) |
| VONA measured in marginal lineup points (my own proposal) | **−3.6** points (doc 54) |
| A **statistical detector** for contaminated ADP | failed its negative control in both directions; no threshold separates clean from dirty (doc 53) |
| **Self-refitting the FLEX split** each year | the method gives RB25/WR35 on 2024's projections — a ten-rank swing off one season's noise (doc 57) |
| 2023 ESPN **projections** | dead, confirmed three ways. Its **ADP** is recoverable from Underdog (doc 53) |

---

## NEW ESTABLISHED FINDINGS — not in the ledger at all

- **The board is worth 6× the pick rule.** Follow-ADP → constrained VBD = **+24.5**;
  constrained VBD → rollout = **+8.6** (doc 54, re-verified doc 57).
- **Roster caps are mandatory.** Unconstrained VBD drafts **1.46 WRs** and costs 8.7 (doc 54).
- **Each breakout roughly doubles the title:** 0 → 4.7%, 1 → 14.4%, 2 → 26.8%, 3 → 54.6% (doc 55).
- **Breakout rate by draft cost:** **17.0%** at ADP 121–180 versus **2.1–6.2%** at 25–84 (doc 55).
- **Risk from round 9 only.** Global upside tilt −$22 to −$41 (p=0.003); round-9+ tilt free and
  mildly positive, **not statistically resolved** (doc 55, re-run doc 59).
- **Season luck is 6× draft luck**, and between-draft variance in title odds is **zero** once
  corrected for sampling error (doc 55).
- **Per-game outcome dispersion nearly doubles** from the top of the draft (sd 0.24) to the bottom
  (sd 0.45), while the mean stays flat (doc 55, n=324).
- **QB replacement carries a ±30-point band** — projected-vs-realised QB12 error was +30.8 in 2022
  and −30.2 in 2024, roughly double RB's or WR's (doc 57).
- **ESPN puts the 12 keepers inside the live pick feed at overall 169–180** (doc 58).
- **Two thirds of the board sits in ESPN's undrafted sentinel.** Only ~157 of 480 rows carry a real
  ADP; Matt picks through 161 (doc 58).

---

## PROVENANCE RULES ADDED

1. **Never use `espn_adp` from a historical pull as a market.** Use
   `code_adp_guard.load_preseason_adp(season)` — registry holds 2021–2025 (doc 53).
2. **Never report a severity you have not measured** with a paired experiment. Three agent-reported
   magnitudes were wrong by 1–2 orders of magnitude (docs 56–58).
3. **A guard that has never been executed is not a guard.** Run it against the historical defect it
   was written for (doc 59).
4. **Nothing compares an artifact to its builder.** Three of the defects found on Aug 27 were stale
   artifacts, not bad code (doc 59).
