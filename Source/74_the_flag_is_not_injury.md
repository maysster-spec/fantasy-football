# 74 — THE "QUESTIONABLE" FLAG IS NOT AN INJURY DESIGNATION

**Aug 29, 2026. SUPERSEDES doc 73 §A2–A3.** Measured from `espn_raw_2026_20260820.json`.

---

## 1. THE FINDING

ESPN's player object carries **two** injury fields. The board uses the wrong one.

| field | what it is |
|---|---|
| `injured` | a **boolean**. ESPN's actual "this player is hurt" flag |
| `injuryStatus` | a one-word label. **This is what `flag` on the board comes from** |

Across the **top 180 of the board** (everything Matt can realistically draft):

| | count |
|---|---|
| `injured == True` | **3** — Alec Pierce, George Kittle, Zach Charbonnet (all `OUT`) |
| tagged `QUESTIONABLE` but `injured == False` | **33** |

**Every QUESTIONABLE player in the draftable range is marked NOT INJURED by ESPN's own boolean.**
Nacua, McCaffrey, Breece Hall, Jeremiyah Love, Malik Nabers — all `QUESTIONABLE`, all
`injured = False`.

**The red tag on the board is a roster-status marker, not a health designation.** It is worse
than uninformative: it would make Matt hesitate on five of his best targets for no reason.

## 2. WHAT THIS RETRACTS

Doc 73 §A2 measured that flagged players project **above** their ADP peers (RB +6.6, TE +8.4,
WR +24.1) and read it as *"the market discounts injury, ESPN's projection doesn't."*

**The measurement stands; the interpretation does not.** If the tag is not injury, the residual is
not an injury discount. It is some other property of the tagged population — plausibly that these
are wider-outcome players — and it is **unexplained**. Do not carry "the board overvalues injured
players" forward. Only three players in range are injured at all.

Doc 73 §A1 (the flag is display-only, never enters `vbd` or the rollout) and §A4 (historical flag
data is contaminated, untestable) are **unaffected and still correct**.

## 3. THE FIELD THAT ACTUALLY HELPS IS ALREADY IN THE PULL AND IS BEING THROWN AWAY

`seasonOutlook` — a paragraph of ESPN analyst text — is present on **177 of the top 180**.
It carries exactly the narrative Matt asked for and assumed did not exist:

> **Malik Nabers** — *"on the comeback trail after a torn ACL limited him to only four
> appearances last season…"*

`Espn_pull_projections.py` **does not capture it** (`grep seasonOutlook` → 0 hits). It is fetched
from ESPN on every pull and discarded before the CSV is written.

**RECOMMENDATION — the highest-value small change left before Sept 7.**
Add `"seasonOutlook": p.get("seasonOutlook")` to the row dict in `parse()`, carry it onto the
board, and render it as a hover tooltip on the player name in `live_board.html`. At the pick Matt
then reads *"torn ACL, four appearances"* instead of a meaningless red word.

Cost: one line in the pull, one column on the board, one `title=` attribute in the HTML.
**This is not a modeling change** — nothing enters `vbd`. It is putting information Matt already
owns in front of him at the moment he needs it.

## 4. WHAT THE BOARD SHOULD SHOW INSTEAD OF `QUESTIONABLE`

Drive the red tag off `injured == True`, not off `injuryStatus`. That turns 36 red tags in the
top 180 into **3** — and those three are real.

---

## 5. THE REMAINING GAP IS REAL, AND IT IS NARROWER THAN IT FEELS

Matt's worry was that he has not followed injury news. Measured: **3 players in his top 180 are
injured.** The preparation gap is not 36 players wide. It is 3, plus whatever changes between now
and Sept 7 — which is what the Sept 5 news sweep exists to catch.

What genuinely cannot be read off any ESPN field is the *class* of injury risk Matt described:
lingering high-ankle sprains, hamstring re-injury rates, post-ACL first-year ceilings. That is a
knowledge problem, not a data problem, and it is worth **one** research pass — see §6.

## 6. THE RESEARCH TASK WORTH OUTSOURCING (Gemini Deep Research or equivalent)

Two deliverables, both small, both reusable every season:

**(a) An injury-class reference card — one page, general, not player-specific.** For each of
roughly eight common injury classes: typical missed time, whether performance on return is
impaired and for how long, and documented re-injury rate. Matt's own examples are the spec:
hamstring strain re-injury 30–38%, high-ankle sprain lingering all season (Pollard, Ekeler 2023),
soft-tissue recurrence (Samuel, Evans), post-ACL year-one ceiling suppression (Barkley 2021).
This converts a word on a screen into a decision under a 60-second clock.

**(b) A one-line dossier for the ~15 players in the top 180 whose `seasonOutlook` mentions an
injury.** Injury type, current status, expected availability, re-injury history. Fifteen lines,
not a report.

**Do NOT ask for player rankings or draft advice from that pass.** The board handles value. What
is being bought is injury *context* the board cannot carry.

## 7. THE OPPORTUNITY MATT NAMED IS REAL AND ALREADY IN THE RULES

His instinct — a rookie RB whose price is depressed by an early-season injury, who returns as a
backup and inherits RB1 work — is exactly §4.13's finding. Breakout rate is **17.0%** at ADP
121–180 against 2.1–6.2% at 25–84, and the rule is: **take that risk from round 9 (picks 104, 113,
128, 137), never before.** An injured rookie RB behind a starter is a textbook instance. It needs
no new mechanism, only the discipline to keep it late.
