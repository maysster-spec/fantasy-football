# 320 -- B2: the usage order names the inheritor better than the preseason chart, from week 3 on

**16 September 2026.** Catalog item B2, from `REDTEAM_TASKING_PROMPT.md` section B: *`depth_map.csv`
is a preseason depth chart, and doc 296 caught it naming a man who did not play.* Tested on five
seasons of lead-back absences, paired, against the official week-1 chart, the official chart of the
week itself, and three usage windows.

---

## 0. WHAT TO DO

1. **From the week-3 sheet on, order each backfield by carries plus targets this season, not by the
   preseason chart.** Usage names the man who actually inherits **72% of the time against the
   chart's 62%**, on the same 111 events, and the gap is not chance (p=0.04). In settled backfields,
   where the chart's number one is also the usage leader, it is **85% against 69%** (p=0.001).
2. **Keep the chart through this week.** With one game of usage (the week-2 events, n=8) usage
   and chart tie at 62.5%, and five of the thirteen live disagreements below rest on a backup with
   one to three touches. The switch pays from week 3.
3. **The official weekly depth chart is not the fix.** Nflverse publishes it and it names the
   inheritor 69%, below usage, and in settled backfields it loses to usage by ten points
   (p=0.02). The team's own chart lags the team's own usage.
4. **The stepping rule from doc 296 is worth eight to nine points on its own** and applies to both
   sources: without stepping past a man who is not playing, chart 54%, usage 63%.
5. **The code change is one function and it is mine.** `wire.py` `load_depth()` re-derives `depth`
   from `form_2026.csv`'s cumulative row once two completed weeks exist, and leaves the chart
   untouched before that. Written below, not shipped tonight because another session has
   `wire.py` open (doc 316 landed at 02:42). It fires on the first Tuesday it is in the tree.

---

## 1. THE CLAIM IN ITS TESTABLE FORM, WRITTEN BEFORE THE RUN

> **POPULATION:** every team-week 2021-2025, regular season weeks 2-14, where the running back who
> led his team in carries plus targets over the weeks played so far (the usage leader to date)
> played the previous week and has no line this week while his team plays. One event per absence
> spell, its first week only, because from the second week on the usage order already contains the
> inheritor's relief work and the comparison would be rigged.
> **OUTCOME:** the running back on that team with the most carries plus targets in the absence week.
> **PREDICTORS**, each naming one man before the week is played: the official week-1 depth chart
> (nflverse `depth_charts`; the 3 Sept snapshot for 2025), and the second back by carries plus
> targets to date. Both may step past a man with no line in the absence week, because the live code
> already steps past a man ESPN lists OUT (doc 296).
> **FALSIFIER, fixed first:** usage must name the inheritor at least 5 points more often than the
> chart on the same events, with McNemar p under 0.05, or the preseason chart stays.

**n = 114 events. 111 carry a week-1 chart** (CHI 2021, CIN 2022 and CIN 2024 had no running-back
rows on the nflverse chart that season and are excluded from the paired comparison, named here so
the count is auditable). Per season 32 / 25 / 20 / 21 / 16. The usage leader held a median 58% of
his team's backfield touches, and the inheritor took a median **68%** of them in the absence week,
so a hit is a hit on a real job.

**The test is paired (the same events under every arm) and the p is McNemar's exact test on the
discordant pairs, which is the only thing that can separate two predictors scored on one set.**

---

## 2. THE RESULT

| predictor of the inheritor | names him | without stepping |
|---|---|---|
| **week-1 official chart** | **62.2%** | 54.1% |
| **carries + targets to date** | **72.1%** | 63.1% |
| last three weeks only | 70.3% | 69.4% |
| last week only | 71.2% | 68.5% |
| the official chart of THAT week | 69.4% | 65.8% |

**Usage minus chart: +9.9 points. Chart right and usage wrong 7 times; usage right and chart wrong
18 times; McNemar p = 0.043.** `[TESTED, n=111, five seasons]` **The falsifier passes, at the edge:
the gain clears 5 by a distance and the p clears 0.05 by very little.** Two things say the direction
is real rather than a coin landing right: the three usage windows agree with each other to within
two points, and the settled-backfield cell below is far stronger than the average.

**The two sources name the same man 71% of the time.** In the 32 events where they disagree, usage
is right **56%**, the chart **22%**, and neither 22%. That is where the whole gain lives.

**WHERE IT WORKS AND WHERE IT DOES NOT (0.5a3: the subgroup, not the average):**

| | n | chart | usage | weekly chart | usage minus chart |
|---|---|---|---|---|---|
| **the usage leader IS the chart's number one** (a settled backfield) | **80** | 68.8% | **85.0%** | 75.0% | **+16.2, p=0.001** |
| the usage leader is NOT the chart's number one | 31 | 45.2% | 38.7% | **54.8%** | −6.5, p=0.75 |

**When a fill-in is leading the backfield because the chart's starter is hurt, nobody predicts the
next man well, and the chart does slightly better than usage.** Of the seven events the chart got
and usage did not, three are the chart's own starter walking back in from an early injury (Jacobs
2021, Elijah Mitchell 2022, Moss 2023) and four are ordinary calls (Coleman NYJ 2021, Sermon SF
2021, Ingram ARI 2023, Demercado ARI 2025). The usage order cannot see a man who has not played
yet. That is a known limit, not a defect, and it is exactly why the live code's OUT-status step
exists.

**BY WEEK, because the live question is when to switch:**

| absence in | n | chart | usage |
|---|---|---|---|
| **week 2** (one game of usage) | **8** | **62.5%** | **62.5%** |
| weeks 3-4 | 18 | 61.1% | 77.8% |
| weeks 5-9 | 50 | 66.0% | 70.0% |
| weeks 10-14 | 37 | 57.1% | 74.3% |

**One week of usage is no better than the chart; two or more weeks are.** n=8 at week 2 cannot
resolve much, but it is the cell that matters this week and it says wait.

**BY SEASON:** usage minus chart +6.5 / +12.5 / +10.0 / +20.0 / **0.0** (2021 to 2025, n=31 / 24 /
20 / 20 / 16). Positive in four of five and flat in 2025, never negative. `[TESTED]`

**The disagreements read the way the numbers say.** Usage got Pacheco over McKinnon (KC 2022),
Allgeier over the chart's nobody (ATL 2022), Charbonnet over Dallas (SEA 2023), Ray Davis over Ty
Johnson (BUF 2024), Tracy over Gray (NYG 2024), Guerendo over Taylor (SF 2024), Gainwell over Kaleb
Johnson (PIT 2025). The chart got Jacobs over Drake (LV 2021), Sermon over Cannon (SF 2021),
Elijah Mitchell over McCaffrey-as-second (SF 2022), Ingram over Demercado (ARI 2023). All 32 rows,
by name, in `B2_disagreements.csv`; all 114 events in `B2_events.csv`.

---

## 3. THE LIVE FILE, AND WHY THIS WEEK IS THE ONE WEEK NOT TO ACT ON IT

`B2_live_2026_backfields.csv` puts `depth_map.csv`'s order beside the week-1 usage order for all 32
teams. **Thirteen backups differ and seven leads differ.** The thirteen:

| team | chart 1 | chart 2 | usage 1 (touches) | usage 2 (touches) |
|---|---|---|---|---|
| ARI | Jeremiyah Love | Tyler Allgeier | Tyler Allgeier (19) | Jeremiyah Love (15) |
| BUF | James Cook III | Ty Johnson | James Cook (17) | Frank Gore Jr. (1) |
| CLE | Quinshon Judkins | Dylan Sampson | Quinshon Judkins (14) | Raheim Sanders (4) |
| DAL | Javonte Williams | Jaydon Blue | Javonte Williams (17) | Emari Demercado (2) |
| DET | Jahmyr Gibbs | Isiah Pacheco | Jahmyr Gibbs (34) | Sione Vaki (3) |
| IND | Jonathan Taylor | DJ Giddens | Jonathan Taylor (23) | Seth McGowan (1) |
| KC | Kenneth Walker III | Emari Demercado | Kenneth Walker III (29) | Emmett Johnson (10) |
| MIA | De'Von Achane | Ollie Gordon II | De'Von Achane (16) | Jaylen Wright (1) |
| MIN | Aaron Jones Sr. | Jordan Mason | Jordan Mason (15) | Aaron Jones (13) |
| NE | TreVeyon Henderson | Reggie Gilliam | Rhamondre Stevenson (24) | Corey Kiner (6) |
| PHI | Saquon Barkley | Tank Bigsby | Saquon Barkley (17) | Will Shipley (3) |
| SEA | Zach Charbonnet | Jadarian Price | Jadarian Price (12) | George Holani (9) |
| **SF** | Christian McCaffrey | **Jordan James** | Christian McCaffrey (18) | **Kaelon Black (15)** |

**Five of the thirteen (BUF, DAL, DET, IND, MIA) rest on a backup with one to three touches**, which
is the week-2 cell's warning in a table. **Three are real and already known: SF is doc 296's case
and the OUT rule already names Black; KC's Emmett Johnson (10 touches) and NE's Corey Kiner are the
ones the chart cannot see.** After week 2 posts, the usage column is two games deep and this table
is the one to read.

---

## 4. THE CODE CHANGE, WRITTEN AND NOT SHIPPED (0.4)

`wire.py` reads `depth` from `depth_map.csv` in `load_depth()`, and both `next_man_up()` and
`in_doubt()` sort on it. The change is contained to `load_depth()`: after the rows are read, if
`form_2026.csv` holds two or more completed weeks, re-rank `depth` within each team by the
cumulative `touches` row, keeping every man without a line BELOW every man with one at his chart
depth plus 10 (the fullback offset already in `depth_map.py`). `ahead` becomes the new depth-1 man.
Before two completed weeks, nothing changes, so the week-2 sheet is untouched and the week-3 sheet
switches by itself.

```python
def usage_depth(rows, form, completed_weeks, min_weeks=2):
    """Re-rank depth within team by cumulative carries+targets once the season has
    enough games to trust (doc 320: two or more completed weeks). Chart order otherwise."""
    if completed_weeks < min_weeks:
        return rows
    by_tm = {}
    for r in rows:
        by_tm.setdefault(r['tm'], []).append(r)
    for tm, rs in by_tm.items():
        def touches(r):
            f = form.get((norm_name(r['player']), 'RB', team_key(tm)))
            return float(f['touches']) if f and f.get('touches') else -1.0
        seen = [r for r in rs if touches(r) >= 0]
        seen.sort(key=lambda r: (-touches(r), r['depth']))
        for i, r in enumerate(seen, 1):
            r['depth'] = i
        for r in rs:
            if touches(r) < 0:
                r['depth'] += 10
        lead = seen[0]['player'] if seen else ''
        for r in rs:
            r['ahead'] = lead if r['depth'] > 1 else ''
    return rows
```

**Its two controls, to be run before it is pinned (0.2):** plant a form file with two completed
weeks where a depth-3 man leads his team in touches and assert `next_man_up()` names him; plant
one completed week and assert the chart order is unchanged. `load_form()` must also return the
count of completed weeks, which it can read from the week values it already iterates. This goes
in `redteam_controls.py` as C18 and C19, and `check_kit.py` is re-pinned with it.

---

## 5. WHAT THIS DOES NOT LICENSE

- **It does not say who inherits when the chart's starter is the one returning.** In that cell the
  chart is a little better and nothing is good; the OUT-status step is what handles it live.
- **It is a running-back result.** Doc 244 already found the receiver room is not one job, so a
  receiver version of this would be a different event and is not run.
- **The 2025 chart is a snapshot on 3 Sept, not a week-1 chart**, because nflverse changed the
  depth-chart format that season; 2021-2024 use the week-1 REG chart. Both are the last thing a
  reader could have seen before the opener, which is what `2026_NFL_Depth_Charts_All_Teams.csv`
  (6 Aug) also is.
- **"No line" is the absence definition on both sides.** A back who dressed and took no touches has
  no nflverse row and reads as absent; for a lead back that is an injury-in-the-first-series
  event and is vanishingly rare, but it is a definition, not a fact about injury reports.

## 6. OPEN

- **NOT YET RUN:** the `load_depth()` change above with its two controls, once `wire.py` is not
  under edit by two sessions.
- **NOT YET RUN:** whether the inheritor's SHARE (median 68%) is itself predicted better by
  usage than by the chart, which is the seat lane's relief-rate question from the other side
  (doc 318 measured the rate as flat across lead-back quality; this would ask whether the ORDER
  carries it).
- **OPEN:** the 2021 season carries 32 of the 114 events and the chart's own hit rate there is
  the lowest of the five; nothing here explains why and the nflverse 2021 chart may simply be
  noisier.

**Reproduce:** `Scripts\research\b2\b2_depth_order.py`, pandas only; inputs
`stats_player_week_2021-2025.csv`, `depth_charts_2021-2025.csv` and `games.csv` from nflverse
(the first four weekly files are in `Scripts\research\_nflverse_cache\`, the rest are named in the
script header). Outputs `B2_events.csv`, `B2_disagreements.csv`, `B2_summary.json`,
`B2_live_2026_backfields.csv`, log `run_b2_20260916.txt`.
