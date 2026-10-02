# 214 — The Boone file was already on the drive, and the QB fade is not a scoring artifact

**2026-09-07, ~15:30 ET. Draft T-4h30m.**
Matt uploaded a file he described as pulled from Yahoo at 10:42 AM today and asked for a heat map
with two columns: plus/minus against ADP and plus/minus against VOR. Mid-task he redirected to
"summary by player on the ones that matter and how i might consider on the board." No heat map was
built; this doc is the analysis behind the summary.

---

## 1. THE UPLOADED FILE IS THE AUGUST 4 FILE. IT IS NOT A SEPT 7 PULL.

```
md5  46b2b604dfd17206bd384d43b6025a25   (uploaded today)
md5  46b2b604dfd17206bd384d43b6025a25   G:\My Drive\_Fantasy\2026\Yahoo_Boone_Rankings_HalfPPR_2026-08-04.csv
```
Byte-identical. Its own filename carries `20260804`. `diff` is empty.

**A newer Boone list was already in `Source\` and neither of us reached for it:**
`Sept 1 Boone and Matt Rankings - Boone.csv` (7,648 bytes, saved 2026-09-01, md5 `5f47bfc4…`).
Same schema, 303 rows. **All analysis below uses the SEPT 1 list**, with Aug 4 as the movement
reference — which is what Matt originally asked the second file to be.

This is the §0.5(c)4 collision check catching a *read*, not a write: the folder listing would have
found the newer file before any of this ran.

## 2. BOONE BARELY MOVES. HE IS NOT A NEWS INSTRUMENT.

Aug 4 → Sept 1, on the 263 players matched to the board: **26 moved at all, and only three by more
than four slots** — Derrick Henry −5, Ashton Jeanty −5, Chris Godwin +6. Everything else is ±1–4
and most of it is cascade from those three.

**Independent proof the list predates the news cycle:** Boone has **Josh Jacobs at 109**. Our board
projects Jacobs at **0.0** — the Aug 30 Commissioner's Exempt List override in `news_overrides.csv`.
The Sept 1 list did not absorb an Aug 30 event.
**Use him for structural preference, never for what changed.**

## 3. A HYPOTHESIS THAT DIED — THE QB FADE IS NOT A SCORING ARTIFACT

Boone sits a median **44 ranks below the market at QB** and 33 below our board. The obvious
explanation is that he ranks for a 4-point passing TD default while §2 gives us **6**.

**Tested, and it is wrong.** Recomputed every QB at 4-pt passing TDs from stat id `4` in the
09-05 pull's `raw_stats`, then re-derived the QB12 replacement line on the same scale:

| | 6-pt TD | 4-pt TD |
|---|---|---|
| QB12 replacement | 341.6 | **286.7** (falls 54.9) |

The replacement line falls with the quarterbacks, so **VOR is nearly invariant**:
Allen rank 14 → 13 · Lamar 32 → 31 · Hurts 38 → 33 · Daniels 39 → 34 · Nix 54 → 51.
`[TESTED, n=all board QBs]` **Boone's QB fade is an opinion, not arithmetic.**

**The two exceptions are real and worth carrying:** the shift scales with projected passing TDs.
**Stafford (34.9 pass TD) moves 40 → 55** and **Burrow (32.9) moves 35 → 43**. Stafford is the most
6-point-TD-dependent name on this board — his VOR of +21.2 falls to **+6.3** in a 4-point league.
The edge is real *in this league*, and it rests on a single scoring rule.

## 4. WHERE HE ACTUALLY DISAGREES — IT IS POSITIONAL, NOT PLAYER-LEVEL

Median rank delta, players inside ADP 170. Positive = Boone ranks him HIGHER.

| pos | n | vs market ADP | vs our board |
|---|---|---|---|
| QB | 30 | **−44** | **−33** |
| RB | 54 | −1 | **0** |
| WR | 78 | −3 | **+4** |
| TE | 25 | **−33** | **−54** |

**RB and WR are dead flat against both.** That is the finding: Boone and our board agree on the two
positions that make up Matt's first eight picks, so he adds nothing structural there — every RB/WR
gap is a genuine individual call, and there are few of them. QB and TE are where he differs, and
§4.3 already says most of the TE tail is worthless, so his TE fade largely *agrees* with us.

**Note the one TE he does not fade: Bowers, 17th, +5 on the market and +6 on our board.** His TE
view is "Bowers, then a cliff" — a sharper version of §4.3.

## 5. THE PLAYER-LEVEL READS THAT MATTER

`VOR` is our board's. `vs market` = Boone rank minus ADP rank. `vs board` = Boone minus our VOR rank.

**Pick 17**
| player | VOR | Boone | vs market | vs board |
|---|---|---|---|---|
| Kenneth Walker III | +81.2 | 11 | **+12** | +2 |
| Chase Brown | +71.3 | 12 | +4 | +8 |
| Brock Bowers | +51.2 | 17 | +5 | +6 |
| Derrick Henry | +95.4 | 23 | −9 | **−14** |
| Trey McBride | +47.6 | 35 | −14 | −11 |

Boone independently backs Matt's stated "Walker over Henry," and it is one of only three players he
moved more than four slots since Aug 4 — Henry down, not up. §4.25 already measured that passing on
Henry at 8 costs **0.0**; this is a second, unrelated source landing the same way.

**Pick 32 — his ordering inside §7's five-name tie**
Bowers 17 · **Nabers 20** · Kyren 27 · Hall 28 · McBride 35 · Judkins 52 · Lamar 55.
§7 says take the engine's #1 and do not override. **This does not override it**; it is the 60-second
read among the five that §7 explicitly calls for. Boone's tie-internal order is Bowers first,
Judkins and Lamar last. He is +8 on Nabers, who is *not* in §7's tie — and §7 already measured that
the availability haircut is the one thing that moves Nabers (+$27 → +$3), so treat that as a wash.

**Picks 56 / 65 — two direct answers to questions Matt already asked**
| player | VOR | Boone | vs market | vs board |
|---|---|---|---|---|
| Luther Burden III | +4.8 | 40 | **+15** | **+18** |
| Courtland Sutton | +6.2 | 108 | **−48** | **−53** |
| Rome Odunze | +19.4 | 60 | −10 | −17 |
| Terry McLaurin | +16.6 | 57 | −12 | −11 |
| Christian Watson | −5.9 | 46 | **+22** | **+31** |

Matt asked about Burden and said Sutton "hasn't impressed"; Boone is the highest source on Burden
and buries Sutton. **But note Odunze**: doc 211 §2 established he is the best VOR at 56 (+19.4), and
Boone is *cooler* on him than either the market or us. Odunze is our call, not a consensus one.

**Round 9+ — his loudest names our board can still reach**
Godwin +35 · Stribling +34 · Croskey-Merritt +30 · Jayden Reed +26 · Josh Downs +26 ·
Jordan Mason +21 · Parker Washington +22.
Five of seven are WRs. §4.13's late-dart band is where a swing is free, so these are legitimate
round-9+ tiebreakers and nothing more.

**Disregard entirely:** Josh Jacobs (Boone 109, our board 0.0 projected — see §2) and MarShawn Lloyd
(Boone 62, our board rank 184; ESPN's own projection is 78.2 with no override, so this is a genuine
disagreement, but Lloyd is the §0.5(c)5 missing-row case and the board's number is the one built on
the current pull).

## 6. HOW TO USE HIM — ONE LINE

**Boone is a tiebreaker, never a source.** §4.13d already established that the analyst accuracy
tables cannot justify following a ranker *or* dismissing one. On the two positions Matt drafts first
he agrees with our board to within a rank, so there is nothing to arbitrate. **Consult him only
where the board is already inside its own coin-flip band** — pick 32's five names, the 56/65 WR
cluster, and the round-9+ darts.

## 7. JOIN PROVENANCE

Key: name + position + team, normalised (case, accents, punctuation, Jr/Sr/II/III stripped), team
aliases LA↔LAR, WAS↔WSH, JAC↔JAX — §3's rule, since neither Boone file carries `espn_id`.
**263 of 303 Boone rows matched** `board_v8_fixed.csv` (staged 15:19 ET, 41,549 bytes).
**The 40 unmatched are all accounted for and none is a defect:** 12 are exactly the twelve keepers
(Olave, Pickens, Javonte Williams, Rice, Flowers, Etienne, Loveland, McMillan, Skattebo, Stevenson,
Maye, Diggs — removed from the board per §2.1d, which is an independent confirmation of the keeper
list); 12 are D/ST and 11 are kickers, which the board names differently; 5 are deep RBs outside the
480 rows. **Zero silent drops.**

## 8. OPEN

- The heat map itself was not built — Matt redirected mid-task. The join is in the session
  scratchpad and can be rendered on request.
- `Yahoo_Top_300_as_of_817.csv` (six rankers including Harmon, per doc 06) is still missing from
  both `Source\` and `04_source_data\`. Doc 213 §5 carries this.
- Whether Boone's Sept-1 list is genuinely his newest is unverified; the Yahoo page Matt linked is
  not paywalled (he confirmed; my earlier agent's "gated" finding was wrong), so it is checkable
  from his browser — post-draft.
