# 37 — RUNBOOK: AUG 23 → SEPT 7
**Answering "what else?"** Draft is Mon Sept 7, 8:00 PM. Keeper lock 7:00 PM. 15 days out.

Ordered by value per unit of Matt's time. Items marked **[Matt]** need him; the rest are mine.

---

## THIS WEEK

**1. [Matt] Rotate the ESPN cookie. Today.** `Espn_league_scoredraft_2021_2024.py` carries a
live `espn_s2` in plaintext at line 8, and it has now been in two chats. Log out of ESPN
Fantasy and back in — that invalidates it. Use `espn_pull_draft_history.py` from now on; it
reads credentials from environment variables so the file itself is safe to share and sync.

**2. [Matt] Enter the pre-rank in ESPN — top 120 only, not all 316.** `prerank_top120_v2.txt`
is in paste order. Past ~140 the board is ordered by projection because ADP is censored, and
the last flexible pick is 137 (effective ~149), so the tail is drag-and-drop labor with no
decision attached to it. Budget one sitting.

**3. Mock drafts — yes, but for two specific purposes, not for survival odds.** A public mock
does **not** reproduce this league: it has no keeper depletion (all twelve keepers are in the
pool, which is the single biggest structural feature of the real draft), and the opponents are
strangers rather than twelve managers with four years of modeled tendencies. Survival numbers
from a public mock will be wrong for this league in a knowable direction — too pessimistic
early, since the real board is ~10 players thinner by pick 32.

What mocks genuinely buy:
  - **ADP drift.** If the top 8 keeps coming back different from `board_edges_v6.csv`'s ADP
    (captured Aug 20), the board is stale and needs a re-pull sooner than Sept 5.
  - **Rehearsing pick 8 under a clock.** 4.2 says pick 8 is the *only* realistic Josh Allen
    window, and the edge sits inside a 7% band. That decision should not be made cold at 60
    seconds. Run it enough times that it is reflex.

**[Matt] What to log, per mock** — paste it back and I will score it against the model:
```
slot, who was gone at 8 / 17 / 32 / 41, what I took, what I wish I took
```
Four or five mocks is plenty. Ten adds nothing.

**4. Build the live board (tier 1).** Spec is in `32`. Say the word and I build it here rather
than handing it to Gemini — it is a small job and this session already has the data.

---

## DATED, NON-NEGOTIABLE

| when | what | who |
|---|---|---|
| **~Aug 25** | NFL final roster cuts land — rebuild board | me |
| **Sept 5 (T-48h)** | re-pull projections + ADP (carries live injury flags), news sweep on the shortlist | me |
| **Sept 7, 7:00 PM** | **keeper lock — swap predicted keepers for actual, rebuild depleted board** | me |
| **Sept 7, 8:00 PM** | draft | Matt |

The 7:00 PM rebuild is the one that cannot slip. The whole board is built on *predicted*
keepers; twelve names are held out of it (listed in `36`). If a prediction misses, that player
is invisible on draft night until the board is rebuilt.

---

## OPEN THREADS, RANKED BY WHAT THEY WOULD ACTUALLY CHANGE

**1. The objective function. Still the biggest unresolved question in the project.** The board
maximizes expected week 1–14 starting-lineup points. First place is 44% of the pot and the
2025 holdout showed the greedy-value rule beating the human average on the mean while
compressing outcome variance to 76 against humans' 202 — and losing to exactly the three
best-rated managers. If median-maximizing is not championship-maximizing, the board is
optimizing the wrong thing and no amount of ranking precision fixes it. This is queued for
Gemini 3.1 Pro Deep Think in `27` §3 and is worth doing before Sept 7.

**2. Keeper predictions drive everything downstream.** The effective-ADP table — a full round
of value at pick 41 — is computed from *which* keepers leave the board. Ten of twelve sit at
ADP 21–45. If two or three predictions are wrong, the pick-32-to-41 attrition math moves. Worth
one more pass before Sept 5.

**3. Scoring the analyst corpus against 2024/2025 actuals.** Would convert `35`'s agreement
measurement into a measured hit rate. Blocked on 2024 player-level actuals, which the project
does not have. Listed here so it stays visible rather than being quietly dropped.

## NOT WORTH DOING

- More analyst sources. The 180-call corpus is past the point of new information; the last
  batch mostly *removed* confidence rather than adding it, which is what a saturated sample
  looks like.
- Rebuilding the grid before the shared live-state layer exists. `33` covers why.
- Perfecting ranks below ~140. They are projection-ordered noise and no pick depends on them.
