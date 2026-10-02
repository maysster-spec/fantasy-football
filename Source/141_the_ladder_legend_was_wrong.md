# 141 — Three things the value ladder said that were not true, and one test of Matt's

**2026-09-03 · Matt read the VALUE_LADDER legend carefully and it did not survive · T-4 days**

---

## The do-this list

1. **Nothing.** The rebuilt `VALUE_LADDER.pdf` is on your Drive, and `values.csv` is now stored
   next to its builder so the sheet can be rebuilt at all (it could not be, until today).
2. Read §2 below before pick 32 — your incumbent-vs-challenger read was tested and it is a NULL,
   which is itself the useful answer.

---

## 1. What the legend claimed, and what the code does

Matt asked what five things on the sheet meant. Three of the five answers were **not what the
legend said.** All three are legend defects, not code defects — the sheet computed the right
thing and described it wrongly, which is the harder kind to notice.

**(a) "BOARD — our VBD is well ahead of his price."** VBD is a POINT TOTAL (St. Brown is
+101.33). ADP is a PICK NUMBER. They are not comparable and the sheet was inviting exactly the
reading Matt gave it back ("his value is 32 but his ADP is 42"). The code is
`ev(): if r.board_rank < r.adp_pick - 12` — a **rank against a rank**, with a 12-slot threshold.
Now reads *"his rank on our VBD board is 12+ slots ahead of his ADP."*

**(b) "Ng = games played in 2025 (darker is worse)."** There is no shading on this sheet — every
caution renders in one orange. **The legend was describing the DRAFT_BOARD**, whose `12g` badge
*is* shaded in three tones (§4.22e). Matt: *"Looks like 10g of sugar at a glance."* Correct, and
the label was actively working against the finding it exists to carry, which is that **the number
is the warning, not the badge**: 10–12 games cost −16.9 points against projection, 1–6 games cost
−40.8. Now renders as **`played 10`**, and the legend carries the two numbers.

**(c) The columns had no headers at all.** Seven unlabelled columns, and Matt had to ask what
each one was. Header row added: `player · tm · pos · adp · still there · why he is on this sheet ·
caution · detail`.

**Also fixed:** `p` shown as `0.85` is now `85%`; `DISC` and `AVOID` are spelled out in the legend
(`DISC` = take him later than this rank, not here); team abbreviation added — it does not crowd
the row, the `detail` column had the slack, and it is needed to read `path opened by <teammate>`
at a glance.

## 1b. `still there` is not one number, it is two — and neither is safe

Matt asked where the ladder's `p` appears on the live board. It does not — they are **different
quantities computed different ways**, and putting them side by side would be a trap:

| | the ladder's **still there** | the live board's **still there?** |
|---|---|---|
| question | will he be there **when I arrive** at pick 32 | if I pass now, is he there at my **next turn** |
| method | closed form, `1 − Φ(pick; μ=eff_pick, σ=0.111·eff+5.40)` | 400 simulated runs over the players **actually left** |
| input | a static effective ADP | the live available pool at this pick |

Both are §4.12 dispersion with **no §5 opponent model**, and §4.15 measured what that costs: on
Josh Allen it reads **74%** where the calibrated answer is **3%**, because neither knows Snyder
takes Allen at his turn. **Both are ceilings. Neither checks the other.** The legend now says so.

## 1c. THE SHEET COULD NOT BE REBUILT — the real defect behind all of this

`values.py` reads a `rankers.csv` that exists in **no folder on Matt's machine**. It was a
container-local intermediate from the session that built the sheet, so `VALUE_LADDER.pdf` had
become unreproducible: no input, no rebuild, no correction. Same failure class as doc 139's
number collision — an artifact whose provenance is not on disk.

Rather than reconstruct `rankers.csv` approximately and silently ship a *different* sheet, the
49 rows were read back out of the shipped PDF (`parse_ladder.py`), team joined on the board
spine with a zero-unmatched assert, and `values.csv` written to `Scripts\` where its builder
lives. **Round-trips exactly by construction: 49 players, 11 picks, same as shipped.**

---

## 2. MATT'S QUESTION, TESTED: is the incumbent worse off in an unsettled backfield?

> *"Am I wrong in thinking that the incumbent is in a worse position than the new guy in certain
> cases where there is an unsettled backfield? Kyren Williams made me think of this."*

§4.13c noticed 8 of 15 late RB booms were backs who **inherited** a backfield and tagged it
`[OBSERVED, not tested]` — *"unsettled backfield is not a coded variable and was not tested."*
Coding it now.

**BASELINE, POPULATION, SAMPLE SIZE.** Population: every team-season in the two usable ESPN
preseason pulls (2022 + 2024; 2023's `raw_stats` are empty for 98 of 103 QBs, §4.21). Top two RBs
per team by **preseason projection**; `gap = RB1proj − RB2proj`; **UNSETTLED if gap < 60** (§4.20's
own threshold). Within each pair the **incumbent is whoever the MARKET prices higher** — lower
preseason ADP from the sanctioned registry (§1.1), never historical `espn_adp`. Baseline: expected
VBD14 from price alone, `v_t` regressed on `log(adp)` across all RBs that season (2022 r=−0.592
n=60; 2024 r=−0.609 n=85); a player's **beat** is his residual. Unit of analysis is the
**team-season**, not the player — OL disruption, vacated share and the positional tilt have all
now been killed by the A5 clustering correction, so anything team-constant clusters first.
**n = 48 team-seasons with both backs priced and scored; 19 of them unsettled.**

| | n | incumbent beat | challenger beat | **incumbent − challenger** | p | bootstrap 95% CI |
|---|---|---|---|---|---|---|
| **UNSETTLED (gap < 60)** | 19 | +13.4 | +5.2 | **+8.2** | 0.604 | [−22.9, +38.1] |
| LEAD BACK (gap ≥ 60) | 29 | +1.3 | −2.8 | +4.1 | 0.816 | [−30.5, +37.8] |
| difference of differences | | | | +4.1 | 0.863 | |

**NULL. And the point estimate leans the OTHER way from the intuition** — the incumbent beat his
price by more, not less. **`[TESTED, n=19 team-seasons, UNDERPOWERED]`.** Do not read the +8.2 as
a finding either; the CI is 60 points wide.

**What is actually there is the VARIANCE, and it is enormous.** The 19 unsettled pairs, worst to
best for the incumbent:

```
2024 CAR  INC Jonathon Brooks    -80.2   CHL Rico Dowdle       +52.8   -133
2024 CIN  INC Zack Moss          -23.7   CHL Chase Brown       +86.9   -111
2024 DET  INC Jahmyr Gibbs       +40.4   CHL David Montgomery  +88.3    -48
2022 HOU  INC Devin Singletary   +31.3   CHL Dameon Pierce     +67.8    -37
...
2024 ARI  INC James Conner       +64.3   CHL Trey Benson       -41.1   +105
2024 MIN  INC Aaron Jones        +58.7   CHL Ty Chandler       -50.0   +109
2024 TEN  INC Tony Pollard       +59.5   CHL Tyjae Spears      -50.7   +110
```

Matt's story is real and it is in there twice — **Brooks/Dowdle and Moss/Chase Brown are exactly
"the incumbent was the wrong guy."** So are Pollard/Spears and Jones/Chandler, in the opposite
direction, at the same magnitude. **The spread is ±110 points around a mean of +8.**

**THIS IS §4.20's POINT, ARRIVED AT FROM THE OTHER SIDE.** The flag does not tell you who wins the
job. It tells you **the job is unresolved and worth 215 points to whoever gets it.** Kyren Williams
carries `contested job, worth 215 pts` on the ladder for that reason, and neither the sheet nor
this test has an opinion on whether he keeps it. Doc 110's open question — *"whether the winner of
an unsettled job is worth having remains untestable here"* — is still open, and this test does not
close it.

**Limits.** 19 team-seasons. "Incumbent" here means *the market's favourite*, which is not
identical to *last year's starter* — that is the closest proxy the sanctioned data supports, and a
different coding could move the number. Two seasons. Every caveat points the same way: **not
resolved, and not resolvable before Monday.**

---

## 3. Closing (§7)

**Top 3 assumptions → what would invalidate each**
1. *The rebuilt sheet is the shipped sheet plus fixes.* Verified by round-trip: 49 rows across the
   same 11 picks, every field parsed from the PDF, team joined with a zero-unmatched assert.
   Invalidated by a change to mkvalue's layout — `parse_ladder.py` asserts and dies rather than
   parsing a subset, which is how the first run caught itself losing page 2 (34 rows, not 49).
2. *ADP is a usable proxy for "incumbent".* If the intended contrast is the returning starter
   regardless of price, this measured something adjacent. Re-code from depth charts to settle it.
3. *gap < 60 on a preseason projection means the same thing in 2022, 2024 and 2026.* §4.20 set the
   threshold on the 2026 pull. All three are full-season projections, but the scale drifts.

**The missing input that would most improve this:** a coded incumbent/challenger label from depth
charts rather than from ADP, across 2021–2025. It would roughly double the usable pairs and remove
assumption 2 entirely. Not available before Sept 7.
