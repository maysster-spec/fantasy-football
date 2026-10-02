# 26 — WHAT ACTUALLY SEPARATED THE 2025 FIELD, AND MATT'S DOMAIN KNOWLEDGE (PERSISTED)
**Aug 23, 2026.** Written so the next session does not lose it again.

---

# PART A — THE FINDING

## Counting breakouts is the wrong metric. Aggregate surplus is the right one.

Tested in your league, 2025, all 12 teams, on **position-adjusted** value.
`surplus = (actual points − actual replacement at his position) − (preseason projection − preseason replacement)`
i.e. **how much a player beat the price you paid, in startable value.**

| | statistic |
|---|---|
| playoff vs non-playoff, **counting** breakouts | 1.50 vs 1.00, t=+0.81, **p=0.438 — nothing** |
| seed vs **total roster surplus** | Spearman **−0.783, p=0.003** |
| total surplus vs points-for | **+0.833** |

**Only two rosters finished the year with positive total surplus. They finished 1st and 2nd.**

| seed | manager | breakouts | total surplus |
|---|---|---|---|
| 1 | Lobsinger | 3 | **+240.8** |
| 2 | R Taylor | 2 | **+219.7** |
| 3 | **Matt** | **3** | **−110.8** |
| 4 | Snyder | 1 | −135.8 |
| 5 | Grenier | 0 | −234.5 |
| 6 | Rychlicki | 0 | −14.3 |
| 7–12 | — | 0–2 | −112 to −384 |

**You tied for the most breakouts in the league and still finished with negative surplus.**
Bhayshul Tuten (+120), Pickens (+92), Charbonnet (+91) were three of the fifteen biggest hits in
the draft — and the rest of your roster gave it all back. You made the playoffs on 11 wins with
the **6th-most points**. That is schedule luck, not roster construction.

**This reframes the objective.** The target is not *"hit on a breakout."* One hit is noise —
Brown/Collins had two and finished 9th. The target is **maximise expected surplus over draft
cost across all fourteen picks.** A breakout is one way to generate surplus. Not overpaying at
picks 4 through 9 is another, and it is the one you are losing on.

*Honesty about the metric:* surplus and points-for share the `actual` term, so part of that
+0.833 is definitional. What is **not** definitional is the ordering — a roster can post high
points-for by paying full price for players who merely met expectations. The top two did not do
that. They beat their prices.

## Where surplus came from

Breakouts skewed **RB: 8 of 15, from 34% of the drafted pool.** WR 5, QB 2, TE 0.
**Zero tight ends generated top-decile surplus in 2025.** Consistent with doc 24's finding that
TE analyst accuracy does not persist — nobody can price the position, including the market.

## A correction I made mid-analysis, logged

My first pass ranked all positions together on raw points. In a 6-point-passing-TD league every
starting QB outscores every running back, so "breakout" collapsed into "drafted a quarterback
late" — **9 of the top 14 were QBs.** A scoring-format artifact, not a finding. Redone
position-adjusted, QBs are 2 of 15. `ERROR_PATTERNS`: filter to the population that matters,
and never rank across incomparable groups.

---

# PART B — MATT'S DOMAIN KNOWLEDGE (the thing that keeps getting lost)

These are **his inputs**, recorded verbatim in substance. They are not model findings. Tagged so
a future session treats them as evidence with a track record — his instinct has been right
against the model at least four documented times (`ERROR_PATTERNS` F4).

### B1 · Ranker skill is position-specific `[CONFIRMED BY TEST, doc 24]`
He said it first. Measured: RB accuracy persists (+0.48/+0.36/+0.27), WR weaker, **QB negative
three years running, TE zero.** RB and QB skill are uncorrelated (rho +0.008).
**Never treat "most accurate analyst" as a single thing.**

### B2 · The accuracy contest rewards conservatism `[CONFIRMED BY TEST, doc 23]`
Being 10% tidier on ordinary players is worth **2.80×** as much accuracy score as perfect
foresight on every breakout. Breakouts are 3.4% of total rank error.

### B3 · Breakout-callers self-select OUT of FantasyPros `[HYPOTHESIS — his, untested]`
His mechanism: analysts who take real ranking risk avoid the contest because a handful of bold
calls scores badly across the full board, and a poor public score damages a brand they monetise
through subscriptions. They would rather sell their own content than be scored on someone
else's metric.
**Partial corroboration already in hand:** Zachariason, Siegele, McFarland, Silva, Gretch,
Hartitz and Thorman are absent from all four accuracy tables; Draft Sharks and The Action
Network publish accuracy history but **do not syndicate current rankings to FantasyPros**
(found 2026-08-23). Absence is real. The *motive* is untested.
**How to test:** take 8–10 analysts spanning the FantasyPros accuracy range, pull each one's
individual ranking, and measure mean |their rank − ADP|. If the top of the leaderboard hugs ADP
harder than the bottom, the mechanism is real. **Falsifier:** no relationship between boldness
and accuracy rank.

### B4 · The real decision rule analysts use `[his observation]`
*"Would I really want to draft that player in that spot?"* — when the answer is no, they
override their own model. **The board should surface that question, not hide it.** This is why
the EDGE column works for him and a single blended number does not.

### B5 · His breakout examples, in his stated order of impact
Bijan Robinson · Puka Nacua · Christian McCaffrey · Jaxon Smith-Njigba · Chris Olave ·
Trey McBride · Brock Purdy · Chase Brown · Drake Maye · George Pickens · Derrick Henry ·
Jonathan Taylor · Michael Wilson.
*Note for whoever tests this:* the list spans several seasons, not one. Each name must be
matched to **its own** breakout year before anything is computed against it.

### B6 · Cost constraint `[standing]`
Claude Pro tokens are the scarce resource. Any workstream that another model can do should go to
that model. Claude's job is the parts that need the project's data on disk and the integrity
harness. **Never spend Claude tokens on open-ended web research another model does for free.**

### B7 · Rankers he wants investigated for breakout skill `[his gut — treat as a prior worth testing]`
Justin Boone (specifically the years he was NOT in the FantasyPros contest) · Chris Raybon ·
Dwain McFarland · JJ Zachariason · Rob Waziak · the Fantasy Footballers staff.
*Already known:* Raybon is **RB #3 multi-year** on measured accuracy — the only one of these
with a confirmed quantitative record, and it is a good one. Boone's 2025 draft accuracy was
**#114/212**. Waziak won 2022 outright (#1/247) and is **#24 in 2025**.
