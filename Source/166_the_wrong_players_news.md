# 166 — Nacua was carrying another player's legal trouble, and the late-round sheet

**2026-09-05.** Matt read the Nacua note on the board, googled it, and found it belonged to
Jordan Addison. He was right. That, plus Stribling, the late-round sheet, and whether more
research is worth doing.

---

## 1. THE DEFECT: one player's off-field news on another player's card

**What the board said about Puka Nacua:**
> `NEWS 09-03: Groin injury; returned to practice on Sunday, August 24.`
> **`Potential NFL discipline/suspension pending league review for off-field issues.`**

**Nacua has no such matter.** The pending-discipline story is **Jordan Addison's** — a DUI arrest
that the NFL resolved with a **three-game suspension in August 2025**, served last season. So the
sentence was wrong twice over: **wrong player, and stale by a year.**

**Where it came from — the source, not the join.** `gemini_findings.csv` carries it in Nacua's own
`health` field, with two URLs. The second is
`complex.com/bets/.../is-puka-nacua-suspended-nfl-week-1` — **an aggregator page whose title is a
question.** A page asking "is X suspended?" is not a report that X is suspended, and the research
pass turned the question into a finding. `apply_research.py` then copied it faithfully onto the
card. **The pipeline did its job; the input was wrong and nothing checked it.**

**SCOPE — checked, and it is one row.** All 23 findings were re-read against a
legal/discipline/arrest/suspension pattern. **Nacua's is the only one.** Every other finding is a
depth-chart line or an injury note of the ordinary kind — the sort a roster page supports.

**FIXED in both places:** the sentence and the aggregator URL removed from `gemini_findings.csv`
(so a re-run of `apply_research.py` cannot put it back), and removed from the shipping
`player_context.csv` with an assert that **exactly one row and one field changed** and the row
count and columns did not. Old file archived, `check_kit` re-pinned.

**What Nacua's card says now, and it is corroborated twice:** groin, returned to practice Aug 24,
expected ready for the opener. McVay has described it as psoas soreness with a normal return.

**THE RULE THIS EARNS — for every future research pass:**
> **A legal, disciplinary or suspension claim needs two independent primary reports, and a
> headline that is a QUESTION is not one of them.** Injury and depth-chart notes can ride on a
> single beat-writer source; a claim about a man's conduct cannot.

---

## 2. DE'ZHAUN STRIBLING (WR, SF) — **yes, at 128 or 137. Do not reach.**

**What the board already has on him** — he is not an undiscovered name, he is a flagged one:

| | |
|---|---|
| price | **adp 138.9**, eff_pick **126.9** — live at your **128** and **137** |
| projection | 109.0 pts, vbd −54.6 (below replacement, like everything at that price) |
| badges | **BUY · DART · R (rookie) · DISC** |
| the BUY | **residual +14.5** after removing position and band effects — **6 of 6 rankers ahead of ADP**, 2 calling him a target. Justin Boone among them |
| the DART | direct **WR2** on the 2026 depth chart |
| the DISC | 08-31: hamstring **and shoulder**, "medium confidence", exp 16 games |
| bye | 8 — no clash with Pickens (14) |

**The hamstring is old news, and that matters.** Hamstring *tightness* in early August; **he was
back at practice Aug 6** and his preseason debut drew notice. He does **not** appear on the Sept-3
league injury tracker at all. The 08-31 card note is the most pessimistic reading of him available.

**The part that makes the case, and it is on the board rather than in the buzz:**
**Ricky Pearsall is out for the season** (PCL surgery) and sits at **0.0 projected points**. The SF
receiver room on your board is now **Evans (adp 84) · Stribling (139) · Deebo (143)** and then
nothing above 31 points. **The "job away" a DART badge normally waits for has already happened.**

**Two honest cautions:**
1. **"6 of 6 ahead" is worth less than it sounds in this band** — doc 35 measured that unanimity in
   ADP 100–170 is the *default* state, 40% of the band, because ADP is censored there. What rescues
   this one is that the badge is the **residualised** version, so the censoring is already removed.
2. **§4.22(c)'s availability penalty is a WR effect.** A rookie WR with a soft-tissue flag is
   exactly the profile that underperforms its price. At pick 128 that costs nothing; at 104 it would.

**Verdict: take him at 128 or 137 if he is there, and let the engine's #1 beat him if it wants to.
Do not move him up to 113.** Your read of Shanahan is not something this project can test — §4.13d
is explicit that no ceiling metric exists here — but the price is nearly free and the depth chart
in front of him is genuinely thin.

---

## 3. THE LATE-ROUND SHEET, REBUILT ON TODAY'S BOARD

Gate: `adp_pick < 168` (§4.14). Everything here is below replacement — that is what "late" means.
**`OPEN JOB n` = the depth chart is unresolved and the job is worth n points to whoever wins it.**

### PICK 89 — the last turn a startable QB or TE exists
| player | pos | eff | signals |
|---|---|---|---|
| **Rico Dowdle** | RB | 84 | OPEN JOB 174 |
| **Kenny Gainwell** | RB | 89 | DART · OPEN JOB 189 — *but Gemini has him as a clear top-two back with Irving, so this is a committee, not a vacancy* |
| Jonathon Brooks | RB | 93 | BUY · DART · OPEN JOB 161 · DISC (soreness, questionable wk 1) |
| Chuba Hubbard | RB | 96 | BUY · OPEN JOB 161 · DISC (hamstring, "ahead of schedule") |

### PICKS 104 / 113 — the QB2 window, and the best "job away" story on the board
| player | pos | eff | signals |
|---|---|---|---|
| **RJ Harvey** | RB | 113 | **BUY · DART · OPEN JOB 164** — and **J.K. Dobbins ahead of him is AVOID and was reported Sept 2 as possibly headed to IR.** The cleanest vacancy on the sheet |
| Rachaad White | RB | 113 | BUY · DART · OPEN JOB 151 · DISC |
| Blake Corum | RB | 114 | BUY · DART |
| Aaron Jones Sr. | RB | 102 | OPEN JOB 154 — co-RB1 with Mason on the initial depth chart |
| Chris Godwin Jr. | WR | 110 | BUY (9 games in 2025 — read the badge number) |
| Dalton Kincaid | TE | 119 | BUY · DISC |
| *Kyle Monangai* | RB | 112 | DART · OPEN JOB **195** — the biggest open job here, **but AVOID**: hyperextended knee, week-to-week, wk 1 in serious question |

### PICK 128 — where Stribling lives
| player | pos | eff | signals |
|---|---|---|---|
| **De'Zhaun Stribling** | WR | 127 | **BUY · DART · R · DISC** — see §2 |
| **Jordan Mason** | RB | 127 | BUY · OPEN JOB 154 — co-RB1 with Aaron Jones |
| Jacory Croskey-Merritt | RB | 124 | BUY · OPEN JOB 151 · DISC (groin, Aug 25) |
| Josh Downs | WR | 125 | BUY · DISC |
| Jayden Reed | WR | 128 | BUY — **5 games in 2025, the darkest badge band** |
| Kyler Murray | QB | 125 | BUY — the QB2 candidate if you go that way at 113 |

### PICK 137 — the last flexible pick
| player | pos | eff | signals |
|---|---|---|---|
| **Tyler Allgeier** | RB | 151 | **BUY · DART**, job worth **244** — the biggest on the sheet |
| KC Concepcion | WR | 135 | BUY · R |
| Tyjae Spears | RB | 134 | DART · OPEN JOB 171 |
| Romeo Doubs | WR | 136 | BUY |
| Jalen Coker | WR | 142 | BUY |

### THREE CORRECTIONS TO THE LIST I GAVE YOU EARLIER
1. **Allgeier is a HANDCUFF, not an open job.** `depth_map` has ARI as **LEAD BACK** — the gap is
   ≥150, so Jeremiyah Love is clearly the guy and Allgeier only pays if Love misses time. That is
   still interesting this week (**Love is "50-50" for Week 1** per his head coach) but it is a
   different bet from Mason's or Harvey's, and I called it the wrong thing.
2. **Xavier Worthy and Makai Lemon carry NO signals on the current board** — no BUY, no dart, no
   job flag. I described them as "late WRs with a bull lean." That is not what the shipped context
   says today. Drop them.
3. **RJ Harvey has improved since that list** — the man ahead of him may be going on IR.

---

## 4. IS MORE RESEARCH WORTH IT? **Mostly no. One kind is.**

**Stop reading opinions.** Four separate measurements in this project say the analyst layer cannot
tell you what you want from it: the accuracy contest is structurally blind to breakout skill
(2.80× weight on ordinary players); the six-ranker panel is one opinion measured six times
(pairwise r 0.81); unanimity in ADP 100–170 is the default state, not a signal; and disagreement,
controlling for ADP, predicts finishing **worse** (−0.244, p=0.0009). §4.13's three draft-day
signals were all null, and §4.22(b) found that when the market and the projection disagree, **the
market is the one that is right.** More opinion changes no pick.

**Keep exactly one channel open: availability, this weekend.** Prior-season games played is the
one injury signal this project could measure and confirm (−16.2 points, p=0.025), and **Week-1
statuses are set on Friday, Saturday and Sunday** — after every source now on your cards. Scope it
to the ~25 names above plus your first four turns. That is a 20-minute job, not a project.

**And the five unresolved keepers** — `py fetch_keepers.py --dry` any time; it needs no lock.

---

## 5. WHY THE GEMINI BATCH DIED, AND HOW TO RE-RUN IT

61–62 names in one pass is past where these runs hold together, and the failure mode is not a
clean error — it is a truncated or drifting answer, which is how §1's contamination got in.

**Ask for less, in three batches, keyed to your turns:**
- **Batch A (~12):** your live names at picks 8–56.
- **Batch B (~12):** picks 65–113.
- **Batch C (~12):** picks 128–137 — the sheet in §3.

**And change the output contract.** Not prose. **One line per player: the fact, one URL, one date.**
Then add the rule §1 earned:

> For injury and depth-chart items, one beat-writer or team source is enough. **For any claim about
> discipline, suspension, arrest or legal status, give TWO independent primary reports — and a
> headline phrased as a question does not count as either.** If you cannot find two, say
> "unverified" and stop.
