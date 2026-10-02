# 213 — Matt's kicker mechanism is right, and it still cannot be drafted on

**2026-09-07, 15:05 ET, T−5h.** Three of his questions, answered with measurements, plus one
change shipped to the live board.

---

## 1 — HIS KICKER MECHANISM IS CORRECT, AND IT IS THE STRONGEST RELATIONSHIP IN THE STUDY

Matt: *"other signals may include where a team's offense commonly stalls within Field Goal range
because they can't sustain drives, which gives the kicker more opportunities."*

**POPULATION: 2,683 team-games, 2021–2025 regular season, nflverse play-by-play joined to kicker
points scored under this league's own rules.** A drive counts as "reached field-goal range" when
it got inside the opponent's 40. `[TESTED]`

| what | correlation with that week's kicker points |
|---|---|
| **share of FG-range drives that ended in a kick — HIS SIGNAL** | **+0.700** |
| number of FG-range drives | +0.189 |
| **the game's total points — his other guess** | **+0.155** |

**He is right, and by a distance.** Stalling in range is nearly the whole story of a kicker week.

**And his second guess is also right, just small.** Kicker points by how high-scoring the game was:

| game total | kicker points |
|---|---|
| under 35 | 7.12 |
| 35–42 | 7.75 |
| 42–49 | 8.06 |
| 49–56 | 8.32 |
| 56+ | 9.04 |

**A shootout is worth about two points to a kicker over a defensive struggle.** Real, and a fifth
of what stalling is worth.

---

## 2 — AND NEITHER CAN BE DRAFTED ON, FOR ONE REASON: THE INPUT DOES NOT REPEAT

Both numbers above are HINDSIGHT — they describe the game after it happened. The draft-day
question is whether a team's *tendency* carries from one season to the next.

| what | year-to-year persistence (n=128 transitions) |
|---|---|
| stall rate in FG range | **r = +0.200** |
| FG-range drives per game | **r = +0.052 — nothing** |
| kicker points per game | r = +0.259 |

**The mechanism is real and the predictor is not.** A team that stalled inside the 40 all of 2025
has barely more than a coin flip's tendency to do it again, and how OFTEN a team reaches field-goal
range does not carry over at all.

**This is §4.21's shape a third time — *unpriced* and *predictable* are different claims.** The
best single input available is the kicker's own team points per game, which persists at +0.259,
and that is exactly what the projection in doc 212 already uses. **There is no better kicker
signal to add. The question was worth asking and the answer closes it.**

---

## 3 — THE WAIVER RULES, FACT-CHECKED, AND HIS D/ST ARGUMENT IS STRONGER THAN HE PUT IT

Checked against ESPN's own support pages, not inferred.

| his belief | verdict |
|---|---|
| "each week has two waiver rounds" | **WRONG as stated, right in effect.** ESPN processes waivers **daily**, 3–5am ET, on a 1-day period. The NFL calendar concentrates them into two that matter: **Wednesday** (Sunday's drops) and **Thursday** (Monday-night's) |
| "winning a claim drops me for the next one" | **RIGHT.** A successful claim sends you to the **bottom** of the order immediately |
| "the order resets weekly to inverse standings" | **RIGHT, and it is a named setting** — ESPN's **"Reset Each Week"**, Monday 3:00am ET. His league has it |

**So his D/ST point is not just correct, it is bigger than he claimed.** Burning the claim on a
defence in Wednesday's run does not only cost him the second run — **it puts him at the bottom for
the whole rest of the week**, including Thursday's, which is where a Monday-night breakout back
first appears. One defence claim can cost the one running back he actually wanted, and §4.19
measured that an RB hole is the one the wire cannot patch for him.

**That is the argument for drafting the opening MONTH at 152 rather than the opener** — it is not
about points, it is about never having to spend the claim.

---

## 4 — SHIPPED: THE LIVE BOARD'S D/ST AND KICKER PAGES NOW RANK BY THE OPENING MONTH

Matt asked for a bright number beside the name because he cannot read this decision off VOR.
`render_streamer` — the page that draws at picks **152 and 161 only** — now:
- **orders by the first-four-weeks projection instead of the season projection**, so the headline
  name at the top of the page IS the answer;
- prints an **amber rank 1–32** in the first column, plus the Week-1 opponent and the four-week
  number beside the old season figure;
- says in plain English that the amber number is the ordering and the season column is not.

A team missing from the table keeps the old ordering and sorts last. **Blast radius is two picks:
nothing else in the file calls this function, and the printed `DST_K_WEEK1.md` is the fallback.**
Exercised after editing on a five-row list including a deliberately unknown team — order came out
Jaguars, Bears, Broncos, Jets, unknown; headline "Jaguars D/ST"; kicker page ordered Fairbairn
ahead of Little.

**And one thing fixed while I was in there:** that page carried the literal string **"§4.8"** in
its explanation. `check_plain.py` never caught it because it only scans the four PRINTED pages,
not the live board. Replaced with plain English. **`check_plain` should be pointed at
`live_board.html` too — post-draft.**

`live_draft.py` → **130474 / `5de72e4c71516ced`**, `check_kit.py` re-pinned.

---

## 5 — BOONE AND HARMON: I ANSWERED THE WRONG QUESTION, AND MATT CAUGHT IT IN ONE LINE

**Written first as "both paywalled, I read neither." Matt: *"how did you fill this csv file if this
is true?"* He is right, and the answer is on the drive.**

`Source\Boone_Rankings_HalfPPR_2026-08-04.csv` — 300 rows, header `#, Player, Boone 08/05`, names
formatted `Jahmyr Gibbs DET - RB`. **That is a FantasyPros export, not a Yahoo page.** FantasyPros
carries Boone as one of its contributing experts, and doc 25 records exactly how it was taken:
*"Pulled live from your FantasyPros account via the browser."* An earlier session drove his own
logged-in browser and read the rankings out of his account.

**So the question was never "is the Yahoo article readable."** It was "can I get Boone's and
Harmon's current rankings," and the answer is **yes, the same way this project already did it
twice** — Claude in Chrome against his own session. **I sent an agent at Yahoo and Reception
Perception, got a correct answer about those two sites, and reported it as though it settled the
question.** §0.5(a2), on my own work this time: right answer, wrong object.

**And the file I pointed at is not even the current one.** Doc 06 records
`Yahoo_Top_300_as_of_817.csv`, captured **Aug 17**, six rankers — **Boone, Smyth, Harmon,
Pianowski, Winks, Norris** — and says in its own header: *"Supersedes the Aug 4 Boone file as the
Boone source."* **The project has read Harmon too.** That file is not in `Source\` or
`04_source_data\` today; where it went is an open thread.

**What this does NOT change tonight.** §4.4's divergence numbers are a *sanity check against
outside opinion*, not a runtime input — §8 says so explicitly and says never to put them on his
required list. Doc 50 measured Boone's rankings against outcomes and they lost to ESPN's own
projection in all three testable years (pooled rho 0.341 vs 0.647) and lost to simply following
ADP. **A fresher Boone column would move no pick tonight.** It is worth doing for provenance, and
it is worth doing AFTER the draft.

Links, for the record (all Yahoo pages gated behind Fantasy Ultra; Reception Perception
subscriber-only):
- Boone half-PPR top 300, Sep 4 — `sports.yahoo.com/fantasy/article/fantasy-football-rankings-justin-boone-players-2026-155300702.html`
- Boone full-PPR top 300 — `.../2026-fantasy-football-full-ppr-rankings-justin-boones-top-300-players-155359326.html`
- Harmon half-PPR hub, Aug 26 — `.../2026-fantasy-football-rankings-matt-harmon-190019730.html`
- Harmon tiers cheat sheet, Aug 24 — `receptionperception.com/matt-harmons-2026-fantasy-football-ranking-tiers-cheatsheet/`
- **The one that actually worked before: `fantasypros.com/nfl/rankings/half-point-ppr-cheatsheets.php`, through his own logged-in browser.**

**OPEN THREAD: `Yahoo_Top_300_as_of_817.csv` is referenced by doc 06 as the current six-ranker
source and is not in either data folder.** §4.4's provenance rests on it. Post-draft.
