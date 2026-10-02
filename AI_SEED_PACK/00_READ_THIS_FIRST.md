# League context for any AI research run — 2026

**Feed this whole folder into a NEW notebook. Do not reuse an old one: stale sources are how the
last run put Jaylen Waddle in Miami and Rico Dowdle in Dallas.**

## The three files

| file | what it is | how to use it |
|---|---|---|
| `board_top200.csv` | the actual draft board for THIS league | **the only source of truth for teams, rounds and value** |
| `keepers_UNDRAFTABLE.csv` | the 12 predicted keepers | **never recommend anyone on this list** — they are not in the draft |
| this file | scoring, picks, rules | context |

## Hard rules for the model

1. **Only recommend players that appear in `board_top200.csv`.** If a player is not in it, say so
   rather than guessing a round for him.
2. **Use the `goes_at_in_THIS_league` column, never national ADP.** This is a keeper league; 12
   players are off the board before pick 1, so public ADP is systematically wrong here. The
   `national_adp` column is included only so you can see the difference.
3. **Never recommend a name from `keepers_UNDRAFTABLE.csv`.** Do not recommend fading them either
   — they cannot be drafted, so the call is meaningless.
4. **Team comes from the `team` column.** If a source says a different team, the source is stale;
   say so and use the column.
5. **Cite a date for every claim.** Anything you cannot date, mark as undated.
6. **If you disagree with the board, say so explicitly and show the reasoning.** Do not silently
   substitute your own number.

## The league

- 12 teams, ESPN, snake, 14 rounds of real picks (the keeper is charged to round 15).
- Start **1 QB · 2 RB · 2 WR · 1 TE · 1 FLEX (RB/WR/TE) · 1 D/ST · 1 K**. Bench 6, IR 3.
- Scoring: **0.5 PPR**, **6-point passing TDs**, 0.04/passing yard, 0.1/rush-rec yard, −2 INT,
  −2 fumble lost, 2-point conversions 2 pts.
- Manager picks from **slot 8**: **8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137, 152, 161.**
  Pick 152 is D/ST, pick 161 is K. **Pick 137 is the last flexible selection.**
- Keeper held: **George Pickens, WR, bye 14.**
- Keeper rule: must have been drafted round 5+ the previous season AND rostered all season.
  Free-agent and trade acquisitions are ineligible. One per team, cannot repeat consecutively.

## Things already settled — do not re-litigate

- **Pick 8: best player available, not a quarterback.** Measured; closed.
- **Position deadlines:** past pick 65 every remaining WR projects below a startable starter;
  QB, RB and TE last until pick 89.
- **Only two tight ends carry a premium** (Bowers, McBride), then a long flat tail.
- **D/ST and K are streamed** — never before picks 152 and 161.
- **Take risk only from pick 104 on.** Tilting earlier costs $22–41 of expected payout.

## What is genuinely useful from a research run

Names to read about, with a dated reason and a source. Depth-chart changes, injuries, role
changes, camp reports. **Not** rounds, not teams, not projections — those are in the CSV.
