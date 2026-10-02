# 270 — The bar is the whole calculation

2026-09-10. Matt: *"the goal is more transparency for me so i can understand how the pieces and
values fit together so i can more easily do the calculations like you are doing. I can't put all
that into memory."*

That is the right complaint and it names a real defect in how this project has been reporting. Docs
268 and 269 handed him **verdicts** — +8.07, +10.20, +1.53 — with the method in prose underneath.
A verdict he cannot reproduce is a verdict he has to trust, and §0.1's whole point is that he should
not have to.

**The fix is one grid.** Everything I compute reduces to a single hidden variable, and once it is on
paper he can do any of it himself.

---

## The bar

For each position and week, **the points-per-week a new player must beat to change the starting
nine.** Solved by bisection against the same best-legal-nine used everywhere in this project.

| position | wk 1–5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|
| QB | 26.2 | 26.2 | 26.2 | 26.2 | 26.2 | **21.9** | 26.2 | 26.2 | 26.2 | 26.2 |
| RB | 14.2 | 14.2 | 14.2 | 14.2 | 14.2 | 14.2 | **11.7** | 14.2 | **12.4** | **12.4** |
| WR | 14.2 | 14.2 | 14.2 | 14.2 | 14.2 | 14.2 | **10.4** | 14.2 | 14.2 | **12.4** |
| TE | 10.7 | **0.0** | 10.7 | 10.7 | 10.7 | 10.7 | 10.7 | 10.7 | 10.7 | 10.7 |
| D/ST | 7.4 | 7.4 | 7.4 | 7.4 | 7.4 | 7.4 | **0.0** | 7.4 | 7.4 | 7.4 |
| K | 11.1 | 11.1 | 11.1 | **0.0** | 11.1 | 11.1 | 11.1 | 11.1 | 11.1 | 11.1 |

**The rule, complete:** a free player is worth `sum over weeks of max(0, his rate − the bar)`,
skipping his own bye. Nothing else. A zero in the grid is an empty slot, so his whole rate counts.

**Verified against the engine rather than asserted.** Hand-applying the grid reproduces the
production best-legal-nine to within **0.04 points** on every candidate tested — Strange +8.10
against +8.07, Boswell +10.20 against +10.20, Freiermuth +7.60 against +7.59. `[TESTED]` The grid is
not a simplification of the model; on this roster it *is* the model.

**And it explains every zero doc 268 reported without explaining.** Every free skill player measured
+0.00 because his rate sits under 14.2, not because the sheet was broken. That sentence was in doc
268; the number that makes it obvious was not.

---

## The transaction question, and a defect it exposed

Matt: *"are you getting transactions with these pulls?"*

**For 2022–2025, yes.** `waivers.py` reads ESPN's `mTransactions2` view week by week and writes
`waiver_report_<year>.csv` and `trade_report_<year>.csv`. Those ran last night: 25 trade rows in
2025 alone.

**For the season being played, no — and that was a hardcoded tuple.**

```
SEASONS = (2022, 2023, 2024, 2025)
```

**The live season was never in it.** So nothing on the drive could answer *who dropped whom this
week*, which is the one transaction question an in-season sheet actually needs — and it is the
question behind "note waiver status post waiver period." He asked whether it was covered; it was not.

**Fixed, and derived rather than hardcoded** so it cannot go stale again:

```
def _current_season(today=None):
    d = today or dt.date.today()
    return d.year if d.month >= 3 else d.year - 1
SEASONS = tuple(range(2022, LIVE_SEASON + 1))
```

Plus `py waivers.py --live` for the in-season run, which pulls this season only. Verified across a
March boundary: 2026-09-10 → 2026, 2027-01-15 → 2026, 2027-03-01 → 2027.

---

## FA is not WA, and it changes the cost side

From his own free-agent screen: **only Spears (clears Friday) and Mayfield (Saturday)** carry a
waiver period. Boswell, the Chiefs, Daniel Jones, McMillan, Tucker, Jeudy are all **FA** — the green
plus adds them immediately, **no claim and no priority spent**.

**This qualifies §4.32's cost side.** *"The resource is one turn at his real priority, twice a week"*
applies only inside a waiver period. §4.31's week-1 result is untouched, because that is about the
player's outcome and not his price — but the reason to ration is gone for anything marked FA.
**Do not treat an FA add as though it spends something.**

---

## What shipped

**`Source\WEEK_SHEET.html`**, also published as an artifact — six sections, in the §0.1 printed
register (no doc numbers, no p-values, no section marks on the page):

1. **The bar**, with a worked example that spells out one number end to end.
2. **Every candidate, week by week** — his rate, fourteen cells showing the gain in each week he
   actually plays, and the season total on the right. Grouped by what the row is *for*: fills an
   empty week · beats nobody today · costs a claim.
3. **Potential**, kept in its own table and explicitly **not** added to the market column — the
   distribution already contains everything the projection does, so summing them double counts. That
   was Matt's question 5 and the answer is that no "potential +2" column exists, because the two are
   two estimates of one quantity.
4. **Marrying the defence** — Cleveland and Chicago week by week with the opponent and which one to
   start, plus every free partner's gain over three windows, and when the second body is worth a spot.
5. **His fourteen**, so the bars have a visible source.
6. **Four rules** — FA vs WA, week 1, holes are different, one spot covers all three.

**`Scripts\waivers.py`** — the live season, plus `--live`. **`Scripts\check_kit.py`** — re-pinned.
**`Scripts\research\bars.py`** — builds the grid and checks it against the engine.

---

## Why the defence pairing gets a section rather than a line

Matt asked when marrying two defences makes sense. Three answers, all measured:

- **Not before week 9.** The pair returns about **+0.7 a week** and costs a bench spot every week.
  Until week 9 that spot is worth more as the tight end and kicker his byes need — +8 and +10.
- **From week 9 yes**, and for a reason that is behavioural rather than statistical: managers who
  stream drop good defences on bad matchups, so the partner gets cheaper exactly when he is wanted.
  Cleveland alone scores 5.02 a week over weeks 9–14; with the best free partner, 6.19.
- **Choosing the pair is the entire product.** The median free partner is worth about two points
  less than the best over six weeks, and against the best *single* defence in the league a randomly
  chosen pair is worth **less than nothing** (doc 267). Two bodies buy nothing; two calendars do.
- **The playoff partner is a different name.** Chicago is the worst free partner in weeks 15–17
  (+0.0) and Indianapolis the best (+2.1). Swap in week 14.

Cleveland's bye is week 11 and Chicago's is week 10, and Chicago is also the best free defence in
week 11 — the week his slot is currently empty. The calendars interlock without being made to.

---

## Open, with inputs named

- **Not yet run:** the absence model. The bar grid prices byes only. Every number on the sheet moves
  when a starter is out, and the sheet says so in words but cannot say it in points.
- **Not yet run:** re-running `waivers.py --live` now that 2026 is in the pull — nobody has seen this
  season's transaction rows yet, including the other eleven managers' adds and drops.
- **Open:** the trade reports exist and have not been read.
