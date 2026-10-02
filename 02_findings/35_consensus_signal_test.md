# 35 — TESTING THE "EVERYONE IS AHEAD OF ADP" SIGNAL
**Aug 23, 2026.** Matt's hypothesis, in his words: *"If all are going ahead of ADP on a
player I suspect that's a good indicator/signal."* Tested rather than assumed, per Section 0.

---

## THE TEST

**Metric.** For each player, the gap between ESPN's ADP rank and each of six independent
rankers' ranks (Boone, Smyth, Harmon, Pianowski, Winks, Norris — already columns in
`board_edges_v6.csv`). Positive gap = that ranker likes him more than ESPN's market does.
"Unanimous ahead" = all six positive.

**Population.** 144 board players who have an **uncensored** ESPN ADP and all six ranker
columns present. Censored players are excluded because ADP carries no ordering information
past pick ~169.4 — 492 of 700 players share a 1.56-pick blob there, so a "gap" against that
number is meaningless.

**Position adjustment.** 4.4 already establishes that the field and ESPN disagree
*systematically by position*, so a raw gap is partly a positional artifact, not a read on
the player. Measured on this population:

| pos | median ranker-vs-ESPN gap |
|---|---|
| RB | **+7.2 picks** |
| WR | +5.8 |
| QB | −3.0 |
| TE | **−14.0** |

Every number below is reported both raw and adjusted (`adj` = raw minus that position's own
median), so what's left is player-specific disagreement rather than the known positional tilt.

---

## RESULT — the hypothesis is right, but only in the top ~50

**[TESTED]** Base rate of "all six rankers ahead of ESPN ADP," by ADP band (n=144):

| ADP band | unanimous | rate | median mean-gap |
|---|---|---|---|
| 1–50 | 4 / 35 | **11.4%** | −0.2 |
| 50–100 | 10 / 37 | 27.0% | −2.7 |
| 100–140 | 15 / 37 | 40.5% | +7.7 |
| 140–170 | 14 / 35 | 40.0% | +20.0 |
| **all** | **43 / 144** | **29.9%** | |

**The rate rises monotonically with ADP.** That is mechanical, not insight: as ADP approaches
the censoring threshold it compresses, so nearly everyone deep looks "ahead of ADP." At ADP
140–170 the median player is +20 picks ahead of ESPN — being ahead there is the *default
state*, not a signal. Taking unanimity at face value across the whole board would have
produced a shortlist of 43 players, 29 of them deep flyers with negative VBD, and would have
felt like a discovery.

**Inside the top 50 it flips.** There ADP is well-measured and the market is efficient, so the
median gap is ≈0 and unanimity is genuinely uncommon — 4 players out of 35.

### The four, top-50 ADP, all six rankers ahead

| player | pos | ADP | VBD | adj gap | 2026 podcast calls |
|---|---|---|---|---|---|
| **Chase Brown** | RB | 24.0 | +71.3 | +0.3 | **4 target / 0 downgrade** |
| Nico Collins | WR | 27.7 | +42.1 | −2.1 | none |
| Omarion Hampton | RB | 27.8 | +67.3 | +1.7 | **0 target / 1 downgrade** (Winks) |
| DeVonta Smith | WR | 39.5 | +30.4 | +3.8 | none |

**Chase Brown is the only player in the pool where both independent signals point the same
way** — six-for-six ahead of ADP *and* four separate analysts calling him a target with no
dissent. He is already 21st on the board by VBD, so this is confirmation of a rank he has
earned, not an argument to reach.

**Omarion Hampton is the informative disagreement.** Ranker consensus is ahead of ADP, but
Hayden Winks is explicitly out ("extremely boom bust… really struggled in pass protection").
Two signals, opposite directions, on a player sitting at board rank 22 near Matt's pick-17
and pick-32 windows. Coin flip — do not resolve it by picking the signal you prefer.

---

## THE OTHER DIRECTION — downgrades landing inside the current top 60

Adding Winks, Norris, Boone, Ciely, Eisenberg, Harris, Patterson, Zachariason and Cupps to
the corpus (180 calls, up from 126) is what made this visible. It mostly *removed* confidence
rather than adding it — several "converging targets" from the first pass are now contested.

| board VBD rank | player | calls | who is out |
|---|---|---|---|
| 43 | **Bucky Irving** | 0T / **3D** | Levitan, Patterson, Daigle |
| 7 | Jaxon Smith-Njigba | 3T / 1D | Winks |
| 10 | James Cook III | 0T / 1D | Winks |
| 11 | De'Von Achane | 0T / 1D | Patterson |
| 22 | Omarion Hampton | 0T / 1D | Winks |
| 27 | Kyren Williams | 0T / 1D | Daigle |
| 31 | Malik Nabers | 0T / 1D | Patterson (ACL recovery) |
| 33 | Davante Adams | 0T / 1D | Levitan |
| 50 | DJ Moore | 1T / 1D | Harmon |
| 51 | Jadarian Price | 1T / 1D | Daigle |
| 54 | Sam LaPorta | 1T / 1D | Mahserejian |

**Bucky Irving is the loudest single result in the new data**: three independent analysts
call him overpriced, none defend him. He sits at board rank 43 on VBD alone. This is not
enough to move him — one projection set says he is worth that — but it is the clearest
"the room disagrees with my board" flag on the sheet.

Also flipped by the new sources: **Rico Dowdle** was 4-of-12 unanimous last pass, now 4T/1D
(Winks: "78th overall feels pretty rich… fragile"). **JSN** likewise now contested.

---

## WHAT THIS DOES AND DOES NOT LICENSE

- **Does:** treat unanimity as meaningful only inside roughly the top 50 ADP, position-adjusted.
  Below that it is close to free and should not be read as consensus.
- **Does:** treat 2+ independent downgrades with zero targets as a real fade flag.
- **Does not:** establish that either signal *predicts 2026 outcomes*. It cannot — 2026 results
  do not exist. **This is an agreement measurement, not a demonstrated edge.** Per Section 0,
  "uncorrelated with the projection" and "predicts outcomes" are different claims and this
  document only supports the weaker one. Everything here is annotation on the board, never a
  rank driver.
- **Falsifier, and how to actually earn the stronger claim:** the corpus contains dated 2024
  and 2025 calls. Scoring those against actuals already in the project would convert this from
  agreement to measured hit rate. It is currently blocked on 2024 player-level actuals, which
  the project does not have (see `00_MANIFEST.md`, "what is not here"). The four calls dated
  2025-08-19 are scoreable against `actual_2025` but n=4 is **UNDERPOWERED**, not evidence.

## DATA NOTE

180 analyst calls, superset of the earlier 126 (zero rows lost). Counting is by **distinct
analyst**, not distinct show — an analyst appearing on two podcasts is one opinion, which the
earlier "N of 12 sources" labels inflated. **This supersedes the "Ranked Summaries" sheet of
`analystbreakoutcalls.xlsx`**, which counted by show and did not position-adjust; that
workbook has been moved to `_archive` to stop the weaker count being used by mistake, and
`04_source_data/raw_analyst_calls_2026.csv` is the source of truth. Transcription noise is
present and material ("Davian Wicks", "Cam Scaboo", "Amarian Hampton", "Jaylen Coker"); 30
name aliases were mapped by hand. Episode dates are absent by design — see `34`, they are not
recoverable from transcripts.
