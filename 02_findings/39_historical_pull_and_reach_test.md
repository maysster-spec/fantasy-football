# 39 — WHAT THE HISTORICAL PULL ACTUALLY RETURNED, AND THE REACH TEST
**Aug 23, 2026.** Three files uploaded: `espn_projections_{2022,2023,2024}_20260823.csv`.

---

## 1. WHAT CAME BACK — TWO GAPS CLOSED, THE ONE THAT MATTERED DID NOT

| column | 2022 | 2023 | 2024 |
|---|---|---|---|
| `proj_YYYY` | 675/700 | 699/700 | 699/700 |
| `espn_adp` | 700 | 699 | 700 |
| **`actual_YYYY-1`** | **0/700** | **0/700** | **0/700** |

**Preseason projections and historical ESPN ADP are now real.** `00_MANIFEST.md` lists both as
"genuinely missing, not misplaced" — that line is now wrong for 2022–2024 and should be edited.
Verified genuine: the 2022 file's cheapest ADPs are Cooper Kupp 5.5, McCaffrey 7.2, Ekeler 7.5,
Dalvin Cook 18.7, Najee Harris 22.2. That is a 2022 board, not a 2026 board wearing a 2022 label.
Uncensored ADP counts: 185 (2022), 250 (2023), 292 (2024).

**Actuals came back completely empty — all three years, every row.** Not a parsing bug. The
script asks for `seasonId = SEASON_YEAR - 1` with `statSourceId = 0`; querying the 2022 endpoint
returns only 2022 rows, so the prior-season request matches nothing and correctly writes null
rather than a wrong number. Confirmed independently: `raw_stats` recomputes to **exactly**
`proj_2022` under the 12-component league map (Kupp 255.3 = 255.3; Henry 250.0 = 250.0), and the
component values are projections — Kupp's row says 1363 receiving yards, which is his 2022
*forecast*, not the 812 he actually managed before the injury.

### The fix — one line, in `season_rows`'s caller

```python
# currently:
act = pick_one(season_rows(p, PRIOR,       0), f"actual {PRIOR}",       name, anomalies)
# should be, for a completed season:
act = pick_one(season_rows(p, SEASON_YEAR, 0), f"actual {SEASON_YEAR}", name, anomalies)
```

Then `SEASON_YEAR = 2023` yields **actual_2023** rather than an empty actual_2022, and the three
runs cover 2022/2023/2024 directly instead of off-by-one. **Not guaranteed to work** — ESPN may
not serve `statSourceId=0` on the `kona_player_info` view for closed seasons. If it comes back
empty again the endpoint does not carry actuals and the fallback is nflverse weekly data with
the league's 12-component scoring applied, which this project can already do.

**No re-pull needed to try it.** The script saves `espn_raw_YYYY_20260823.json` next to each CSV.
`py espn_pull_projections.py --raw espn_raw_2023_20260823.json` re-parses with no network. If the
actual rows are in that payload, the patched script will find them in seconds.

### 2022 is defective — do not use it

58 of 180 drafted players are absent from the 2022 file, and they are not fringe names:
**Jonathan Taylor, Justin Jefferson, Tyreek Hill, A.J. Brown, Alvin Kamara, DK Metcalf,
George Kittle** are all missing. Zero D/ST among the 58, so it is not a naming convention issue —
those players simply are not in the payload. 2023 misses 7, 2024 misses 0. Cause is unconfirmed;
the `sortDraftRanks` filter behaving differently for 2022 is the likeliest candidate. **Every
number below therefore uses 2023 and 2024 only.**

---

## 2. THE REACH TEST — [TESTED], AND IT CONTRADICTS THE PREMISE

For the record: I did not previously establish that Matt reaches late. Nothing in this session
or in the ledger says so. Rather than accept or deny it, here is the measurement.

**Identity had to be solved first.** Team names change every year, so attributing picks required
a chain: *a team's keeper in year Y was drafted by the same manager in year Y−1.* That resolves
all 12 managers across all four seasons — see `manager_identity_map.csv`. Matt's thread:

**Ekeler's Edge (2022) → Long Arm of the Lamar (2023) → Ja'Marracle Whip Juggernauts (2024) →
The Poetry of Junkyard Juggers (2025)**

Independently confirmed at the 2025 end: `backtest_2025_actual.csv` lists Matt's picks as 11 and
14 (Nabers, Chase Brown); the 2025 draft has both at Poetry of Junkyard Juggers. Two paths, same
answer.

**Metric.** Reach = ADP − actual pick. Positive = taken *earlier* than the national market.
Keepers excluded (not selections). Censored ADP excluded. Because reach against national ADP is
mechanically inflated in a keeper league — twelve players are off the board before pick 1, so
everyone's picks run "ahead" of national ADP by a margin that grows through the draft — the only
readable number is **relative to what the other eleven managers did in that same round, that same
year.** n = 313 picks.

| | league median reach | **JUG relative to same round** |
|---|---|---|
| rounds 1–4 | +10.5 (n=84) | **−5.7** (n=7) |
| rounds 5–9 | +46.2 (n=114) | **−24.7** (n=9) |
| **rounds 10–15** | +13.9 (n=115) | **+0.1** (n=10) |

**Matt does not reach late. Rounds 10–15 come in at +0.1 — dead on the league median.**
Across the 24 manager-seasons in the sample he ranks 2nd of 24 in 2024 (+7.1) and 16th of 24 in
2023 (−3.5). The spread across all managers runs −44.7 to +7.7, so both of his seasons sit inside
ordinary variation and point in opposite directions. There is no late-round reaching tendency in
this data.

**Where he does deviate is rounds 5–9, at −24.7 — the opposite direction.** He takes middle-round
players roughly 25 picks *later* than his league-mates do. That is value-waiting, not reaching.
It is also the round band the directive calls the keeper-audition window (rounds 5–9), so it is
worth knowing that his habit there is patience.

**Caveats, stated rather than buried.** n=9 and n=10 for the JUG bands — **UNDERPOWERED**, and a
single pick moves the median. The 2023 middle-round number is dragged hard by one pick:
Sam LaPorta at 133 against an ADP of 63.6, i.e. 70 picks *later* than market, which was the best
value pick in the sample and is doing most of the work in that −24.7. Strip it and the middle-round
effect largely dissolves. **The defensible conclusion is the negative one — no late-reach tendency
exists in the data — not the positive one that he is systematically patient at 5–9.**

One data caution: ESPN's `averageDraftPosition` for a closed season may be a full-season average
rather than a strictly preseason snapshot. The top-of-board sanity check passed for 2022, but
LaPorta at 63.6 is aggressive for a 2023 preseason rookie TE and is the kind of value that would
appear if the average absorbed in-season drafts. Flagged, not resolved.

---

## 3. THE ANALYST-SCORING PIPELINE — RIGHT IDEA, WRONG SIZE

Correcting an overbroad claim from the last round. Saying "the analyst files did not help" lumped
together two files built for two purposes, and the historical half was always meant to be scored.
That was the right design and the objection was not that the files were useless.

But scoring them still cannot happen, for two reasons rather than one:

1. **No actuals** — section 1 above.
2. **The historical corpus is 19 calls on 18 distinct players.** Ten from "Top 10 Must Have
   Sleepers For 2024", five from "Must Own Sleepers – 2024", four from the Fantasy Footballers
   episode dated 2025-08-19. `27_model_offload_plan.md` sized this pipeline at "maybe 200 rows."
   At 19, even with perfect outcome data, a per-analyst hit rate would be a handful of calls per
   analyst against a base rate — **UNDERPOWERED past the point of being worth computing.**

**To make it work, the corpus has to grow, not the outcome data alone.** That means going back to
Gemini Notebook with August 2023 and August 2024 episodes from the same curated analysts — the
same extraction prompt, pointed at older episodes. The 2026 sources are saturated (last batch
mostly removed confidence); the *historical* side is where sources are missing. Roughly 5 analysts
× 2 years × 2 episodes would get to a scoreable sample.

---

## 4. BYPRODUCT: FOUR YEARS OF OPPONENT DATA INSTEAD OF TWO

`manager_identity_map.csv` maps every team name to a manager across 2022–2025. Section 4.12 flags
the RB/WR pace gaps as `[HYPOTHESIS]` specifically because they "rest on 2 drafts." They no longer
have to. Eleven of twelve managers trace cleanly back to 2022; Fleming (NickCannonFanClub) only
appears from 2024, so he is a genuine 2-season sample and should stay flagged as one.
