# 298 -- F2: the screen was pointed at the board, and the board is not the pool

**12 September 2026.** Catalog item F2. The three-signal receiver screen has only ever been run on
receivers the draft board rated. It is now run on the pool Matt can actually claim from, and it
finds one man neither page has ever shown.

---

## 1. The claim in its testable form, written before the run

> Running 4.30's three signals on every FREE receiver, rather than only on board rows, adds at
> least one man who clears 3 of 3 and who has never appeared on either page, and the men already
> tagged on the page still clear on the corrected population.

Both halves hold.

---

## 2. What was wrong with the old run

`research/build_pedigree.py` iterates the **draft board**. A free receiver the board never rated is
never screened, and doc 292 already showed 71 free skill players are off the board on any given
week. Two further defects the catalog names, both fixed here: it compared **receiving-only** points
against the 9.62 bar, so a receiver with carries scored low and could wrongly qualify; and it
dropped 4.30's own **4-game minimum**.

---

## 3. The run

**POPULATION -- restated, not inherited (0.6):** receivers FREE in Matt's league on the 11 Sept
20:14 pull, from `WIRE_20260911.csv` **and** `FREE_UNRANKED_20260911.csv` together, so on-board and
off-board alike: **129 free receivers, 109 on the board and 20 off it.** Of those, the ones drafted
into the NFL in **2024 or 2025** (years 2 and 3; a 2026 rookie has no 2025 line and belongs to
4.28's separate first-round screen), who played **4+ games in 2025** and averaged **under 9.62**
half-PPR a game on **full** scoring: **33 receivers.**
**THE THREE SIGNALS, 4.30's own cutoffs unchanged:** NFL rounds 1-3 · yards per target above 7.13 ·
targets a game above 3.20. `[TESTED]`

**FOUR CLEAR 3 OF 3:**

| receiver | tm | rostered | drafted | g | ppg | y/tgt | tgt/g | on the board? | ESPN today |
|---|---|---|---|---|---|---|---|---|---|
| Jalen McMillan | TB | 32.6% | 2024 r3 | 4 | 5.98 | 11.87 | 3.75 | yes | **doubtful** |
| Ricky Pearsall | SF | 2.8% | 2024 r1 | 9 | 7.84 | 9.96 | 5.89 | yes | **injured reserve** |
| **Jayden Higgins** | **HOU** | **3.4%** | **2025 r2** | **17** | **6.41** | **7.72** | **4.00** | **NO** | **injured reserve** |
| Pat Bryant | DEN | 1.9% | 2025 r3 | 13 | 4.56 | 7.71 | 3.77 | yes | active |

**THE FIND IS JAYDEN HIGGINS, AND HE CONFIRMS THE DEFECT EXACTLY.** He is a 2025 second-round pick
who played all seventeen games, and **he has never been on either page** because the board carries
no projection for him. Doc 248 scored him above all three cutoffs `[INHERITED]`; this is an
independent run, on a different population, with the scoring bar corrected, and it agrees.

**THE OTHER THREE REPLICATE THE PAGE.** McMillan, Pearsall and Bryant are exactly the three the
sheet already tags, arrived at from the free pool instead of the board and on full scoring rather
than receiving-only. Two runs, two populations, the same three names.

**THE JOIN WAS ASSERTED, NOT ASSUMED (3).** ESPN carries no nflverse id, so the key is normalised
name plus position. 43 of 129 free receivers have no NFL draft row; every one is an undrafted man
or a veteran outside the 2024-25 window. **Fuzzy-matched every one of the 43 against the 2024-25
drafted receivers: no near-match, so nothing young was silently dropped.** 35 of the pool's young
receivers joined; 33 survived the games and scoring filters.

---

## 4. AND THE HONEST HEADLINE IS THE ONE I DID NOT EXPECT

**Every one of the four is unusable this week.** McMillan is doubtful, Pearsall and Higgins are on
injured reserve, and Bryant is the man I am under instruction not to price. **The screen's entire
current output is men Matt cannot claim and start**, which is worth saying plainly rather than
presenting a list that reads like four opportunities.

**So no card was written for Higgins, and that is deliberate.** A card puts a man on the sheet; a
man on injured reserve belongs on a watch line, not on a page whose top section is called "the
move". He goes on the watch list when he comes off IR, and the thing that would catch him then is
the change below, not a hand-written card.

---

## 5. The change this earns, with its testable form

**NOT YET RUN, and it is a code change rather than a study:** point `build_pedigree.py` at the free
pool as well as the board, so `pedigree_2026.csv` carries every free receiver in 4.30's population
and the wire's screen tags stop depending on whether the board happened to rate a man. Its
falsifier is already written: the three names the page tags today must still be tagged after the
change, and Higgins must appear. Then a controls check in the C-series that plants a 3-of-3
receiver off the board and requires him on the page.

**Do not read the screen as a forecast (4.13d).** 3 of 3 is a 39.4% base rate on n=33 cells, and
4.30's own list of men who cleared it and fell -- Bateman, Burks, Toney, Rondale Moore, Terrace
Marshall -- is the calibration.

**Reproduce:** `Scripts\research\f2\screen_free_wr.py`, stdlib only, inputs named in its header.
