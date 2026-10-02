# 190 — M7 tested (null), and everything from docs 185–189 in one page

**2026-09-06 (T−1).**

## 1. M7 — after-contact / efficiency. NULL. §4.6 should be downgraded.

§4.6 has said since the beginning that after-contact ability is *"the only thing underweighted by
ESPN — tiebreaker, not thesis."* It had never been given a payoff test. It has one now.

**BASELINE: half-PPR points wks 1–14 of year t+1, regressed on log(§1.1 preseason ADP) within
season. BEAT = residual. n=699, sd(beat)=45.1, 2022–2025, player-clustered SE.**

| position | measure | result |
|---|---|---|
| RB (n=211, 95 players) | yards per carry | +1.02, **p=0.877** |
| RB | EPA per carry | +14.4, **p=0.735** |
| WR/TE (n=390, 174 players) | **YAC per reception** | −0.62, **p=0.589** |
| WR/TE | yards per target | −1.16, **p=0.325** |
| WR/TE | EPA per target | −5.44, **p=0.496** |
| WR/TE | aDOT | −0.35, **p=0.556** |

**Seven measures, two positions, nothing under p=0.30, and five of six point the wrong way.**
`[TESTED — NULL]` §4.6's clause should read *"no measured prior-year efficiency signal survives a
payoff test"* rather than *"underweighted."*

**Two side results from the same regressions:**
1. **Doc 188 holds again at RB:** prior target share **+153.8, p=0.035** with efficiency controls in.
2. **AND DOC 188 IS AN RB-ONLY FINDING.** On pass-catchers, prior target share is **+9.4, p=0.788** —
   flatly null. That makes sense and it needs saying: for a receiver, target share *is* the
   position, so the market prices it; for a back it is a second dimension and the market misses it.
   **Doc 188 was measured on RBs and must be quoted as an RB finding only.**
3. **Availability replicates a third time:** prior games played, pass-catchers, **+1.70, p=0.041**.

## 2. THE WHOLE ARC, docs 185–190

| tested | verdict |
|---|---|
| **RB prior-year target share** | **LIVE. Top quartile beats price +11.6, bottom −15.6. Gap +27, p=0.011. Survives every control.** |
| red-zone role without the TDs (§4.5, ours) | already established; used to surface Sutton and Warren |
| teammate dependence | real in-season (+3.0pp share, p<0.0001), **null as a predictor** (p=0.699) |
| age cliff | **null**, four positions |
| prior workload / "370-carry curse" | **null**, and subsumed by target share |
| NFL draft capital, RB | **not established** — one season carries it |
| NFL draft capital, WR | **null** |
| year-2 receiving-role growth | **null** (+0.01 tgt/g, p=0.953, 37 of 71) |
| after-contact / YAC / EPA efficiency | **null** (this doc) |
| "new QB" flag | built and killed — 3 fires, 1 false |

**One live signal out of ten. It is an RB-only signal and it is worth about 27 points of spread.**

## 3. SHIPPED TONIGHT

- **42 live RB cards now carry their 2025 target-share band** (`player_context.csv`, TOP / mid /
  BOTTOM against the 2021–25 panel quartiles, 4.6% and 10.8%). Chosen over a board-builder change
  deliberately: the `why` column already renders on the board and the player cards, so this needs
  **no new column, no builder edit and no re-render risk** at T−1.
- `check_kit.py` re-pinned: **`player_context.csv` 89,505 / `613bdadd2c5105fa`**.
- Earlier today: Wan'Dale Robinson's QUESTIONABLE traced to a CBS projection feed and marked
  unsupported; Henderson escalated (no practice since Aug 24); `sept5_after.bat` grew the missing
  `make_gridboard.py` step; `replay_log.txt` added to check_kit's runtime allowlist.

## 4. NAMES THAT MOVED, ALL SESSION

| player | direction | why |
|---|---|---|
| **Bhayshul Tuten** (adp 61) | **DOWN** | 2.9% target share — bottom quartile at a round-5 price |
| **TreVeyon Henderson** (77) | **DOWN** | no practice in 12 days; his "pass-catching back" flag was ESPN's projection, not a role |
| **Luther Burden** (75) | **DOWN** | 1 archetype signal; 0 inside-10 targets; 10.1% share with Odunze on the field |
| **Blake Corum** (126) · **Croskey-Merritt** (136) | **DOWN** | 2.4% / 3.0% target share — I had named both as best darts |
| **Kenny Gainwell** (100) | **UP** | 16.3% share, highest of any back after pick 90; same Tampa job as Irving at 57 |
| **Courtland Sutton** (81) | **UP** | 17 inside-20 targets, 7 inside-10, **zero TDs** |
| **Tyler Warren** (52) | **UP** | 11 inside-10 targets on 2 TDs, year-2 TE, 1st-round capital |

## 5. OPEN THREADS, BY NAME (§0.5e)

Pick-56's single-state margin (`ERROR_PATTERNS` A19, §7) · the pick-8 margin disagreement (doc 182) ·
whether ESPN's IR slot accepts reserve/PUP, which decides Charbonnet · Carolina's lead back ·
two doc-number collisions in `Source\` (two 150s, two 94s) · `after_pull.bat` is a deletable stub ·
`ERROR_PATTERNS` F4 should be split post-draft · **§4.6 and §6's archetype A5 both need their
wording corrected post-draft** (this doc and doc 188) · a per-pair version of the teammate test.
