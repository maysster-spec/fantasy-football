# 38 — THE CONSENSUS SIGNAL, PROPERLY BUILT — AND HOW TO WIDEN THE SAMPLE
**Aug 23, 2026.** Answers two questions: *is the "everyone is ahead of ADP" signal worth using*
(yes, with one correction), and *what would let us actually measure who beats their ADP*
(three script runs Matt already owns the tool for).

---

## PART 1 — I UNDERSOLD THIS. HERE IS THE SIGNAL, BUILT PROPERLY.

`35` reported the base rate and stopped. That answered "is unanimity rare" and never produced
the thing actually asked for: **a list**. Deliverable is `consensus_board_v1.csv`, 142
keeper-depleted uncensored players, every one scored.

### Two selective panels, not one

- **Six-panel** — Boone, Smyth, Harmon, Pianowski, Winks, Norris. Hand-picked, not ECR.
- **Sharp-5** — Weisse, Wheeler, Zylak, Gibson, Malachovsky. Selected by *measured multi-year
  draft accuracy*, half-PPR, pulled 2026-08-23.
- **180 podcast calls** as a dissent check.

**[TESTED] The two panels correlate r=+0.888 (n=142) on their gap vs ESPN.** They are close to
the same opinion twice. "Both panels agree" therefore adds far less than it sounds like it
should — it is one signal wearing two coats. Requiring both is still worth doing as a guard
against one panel's quirk, but do not read agreement as independent confirmation.

### The correction that makes the signal work

**[TESTED] Buy/fade rate by position, raw signal, n=142:**

| pos | in pool | flagged BUY | flagged FADE |
|---|---|---|---|
| RB | 46 | **33%** | 7% |
| WR | 54 | **35%** | 9% |
| QB | 23 | 13% | **30%** |
| TE | 19 | **5%** | **58%** |

**58% of tight ends come back as consensus fades and 5% as buys.** That is not nineteen
separate reads on nineteen tight ends. It is the panels ranking for **different scoring than
this league** — public rankings assume 4-point passing TDs and full PPR; this league is
**6-point passing TDs and 0.5 PPR**. Every public panel therefore ranks QBs and TEs later than
ESPN's own board does, on every player, structurally.

Proof it is an artifact and not a read: on the **raw** signal, **Josh Allen and Trey McBride
both land on the fade list.** Allen is the single most-tested pick in this project (4.2:
+24.2 ± 2.0 at pick 8). McBride is one of only two TEs carrying a real premium (4.3: +50.4).
A signal that says fade both of them is measuring the format gap, not the players.

**So: residualise out the position effect and the ADP-band effect before reading anything.**
After doing that, Allen and McBride drop off the fade list — correctly. What survives is
player-specific.

**The operating rule: trust this signal at RB and WR. Do not use it at QB or TE at all.**
At those two positions the league's scoring makes the panels the wrong instrument, and the
project's own replacement-level math (4.2, 4.3) is the right one.

### CONSENSUS BUY — both panels ahead, position- and band-residualised, zero analyst dissent

| player | pos | ADP | resid | VBD | bye | analysts |
|---|---|---|---|---|---|---|
| Chris Godwin Jr. | WR | 147.6 | +30.2 | −36.4 | 10 | 1T/0D |
| Quentin Johnston | WR | 141.4 | +24.2 | −24.5 | 7 | 1T/0D |
| Parker Washington | WR | 99.5 | +21.0 | −8.2 | 7 | 2T/0D |
| Jacory Croskey-Merritt | RB | 137.2 | +20.9 | −17.2 | 7 | 2T/0D |
| Jonathon Brooks | RB | 125.1 | +20.5 | −14.2 | 5 | 2T/0D |
| Christian Watson | WR | 101.1 | +18.3 | −5.9 | 11 | 1T/0D |
| **Jaylen Waddle** | WR | **60.3** | +16.1 | **+11.4** | 10 | 1T/0D |
| **Tee Higgins** | WR | **57.9** | +15.9 | **+19.2** | 6 | 0T/0D |
| Jayden Reed | WR | 136.6 | +15.5 | −25.0 | 11 | 0T/0D |
| De'Zhaun Stribling | WR | 161.2 | +14.5 | −54.6 | 8 | 2T/0D |
| RJ Harvey | RB | 135.8 | +13.9 | −43.4 | 10 | 0T/0D |
| Blake Corum | RB | 140.7 | +13.5 | −17.6 | 11 | 0T/0D |
| **Luther Burden III** | WR | **77.3** | +12.3 | +4.8 | 10 | 2T/0D |
| Jordan Mason | RB | 149.2 | +11.9 | −24.8 | 6 | 2T/0D |

Chris Rodriguez Jr., Tyler Allgeier and Tank Bigsby score higher still but carry VBD of −99,
−86 and −106. They are cheap-and-liked, not good. Ignore them above pick 137.

**The four that matter are the ones with positive VBD**, because those are players the board
already wants *and* the market underrates: **Waddle (ADP 60), Tee Higgins (58),
Luther Burden III (77)**, and at a price, **Parker Washington (99)**. Waddle and Higgins both
land between picks 56 and 65 — Matt's WR-deadline window (4.10's WR deadline is pick 65). That
is the single most actionable thing on this page.

### CONSENSUS FADE — residualised

| player | pos | ADP | resid | VBD |
|---|---|---|---|---|
| **Travis Hunter** | WR | 119.3 | **−66.7** | −72.3 |
| T.J. Hockenson | TE | 133.6 | −48.8 | −20.9 |
| Matthew Stafford | QB | 79.7 | −46.3 | +21.2 |
| Jaxson Dart | QB | 76.3 | −41.7 | 0.0 |
| Khalil Shakir | WR | 126.9 | −33.7 | −27.5 |
| **Jeremiyah Love** | RB | **19.1** | −23.1 | **+77.2** |
| Courtland Sutton | WR | 84.2 | −20.2 | +6.2 |

**Travis Hunter is the cleanest fade on the board** — both panels far behind ESPN, VBD −72.3,
no analyst defending him. Everything agrees.

**Jeremiyah Love is the live conflict.** Board rank 18 on VBD (+77.2), ADP 19.1 — so he is a
plausible pick-17 target — and both selective panels put him well behind his price. RB, so the
positional artifact does not excuse it. Bye 14, which stacks on Pickens. Genuinely unresolved:
the projection likes him, the market's sharpest readers do not.

---

## PART 2 — WHAT THE NEW FILES DID AND DID NOT UNLOCK

**Straight answer: the analyst files did not move us closer to measuring who beats their ADP.**
They are 2026 opinions about a season that has not happened. There is no outcome to score them
against and there will not be one until January. They are useful as a dissent check on the
board — that is all they can be, and `36`'s annotation columns are the right ceiling for them.

**The draft-history file is a different story, and it is the more valuable upload.**
`historical_draft_results_2022_2025.csv` is 720 picks with the price **actually paid in this
league** — better than national ADP, because it is the market Matt actually drafts against,
including its keeper structure and its twelve specific managers.

So the ledger is:

| have | missing |
|---|---|
| Observed price, 720 picks, 2022–2025 (new upload) | **Player-level season fantasy points for 2022, 2023, 2024** |
| `actual_2025` (in `espn_projections_2026_20260820.csv`) | — |

**One missing item. That is the entire blocker**, and `00_MANIFEST.md` currently lists it as
"genuinely missing, not misplaced." That is now wrong — it is reachable.

### How to get it — three runs of a script already on Matt's machine

`code_espn_pull_projections.py` already captures `actual_{PRIOR}` for whatever season it is
pointed at. It is pointed at 2026, so it produced `actual_2025`. Change one line and re-run:

```
SEASON_YEAR = 2025   ->  yields actual_2024
SEASON_YEAR = 2024   ->  yields actual_2023
SEASON_YEAR = 2023   ->  yields actual_2022
```

Three runs, one number changed each time, no new code. That produces roughly **10 minutes of
work for a 4-season, ~720-observation sample** of price-paid versus points-scored in this exact
league — enough to actually test who beats their draft slot, which round the surplus lives in,
and whether any of the analyst or ranker signals have ever predicted it.

**Caveat before running:** the script recomputes league scoring from raw components and checks
itself against ESPN's `appliedTotal`. The 12-component scoring map was fitted on the 2026
payload. If the check fails on an older season, the scoring settings changed that year — that
is information, not a bug, and the script will say so loudly rather than writing a bad file.

**What it will not fix:** the reframe from "breakout" to "outperforms ADP" is the right move
and it widens the target usefully, but the sample is still 12 managers in one league. Four
seasons of one league is enough to describe *this* market and not enough to claim a general
law. That distinction should survive into whatever the test concludes.
