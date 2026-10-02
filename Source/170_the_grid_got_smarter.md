# 170 — The grid was a price list. Matt said so, and he was right.

**Date:** 2026-09-05 (Sat afternoon ET) · **Trigger:** Matt, on the first ADP grid: *"What i don't
love is the fact the board doesn't show the intelligence we have built. Josh Allen should NOT be
where he is now. NO chance he will be there and we established that already."*

He is right, it was a defect, and it is the same defect this project keeps finding in a new place:
**a shipped artifact quietly disagreeing with a measured finding, and nothing checking.**

---

## 1. THE COMPLAINT WAS EXACTLY CORRECT

v1 dealt players into cells in raw ADP order. That put **Josh Allen in Matt's pick-17 cell**, which
§4.2 measured at **survival ≈ 0.03** at q=0.90 and §4.15 uses as its headline example of why
dispersion alone is not a survival model (*"on Josh Allen it read 74% where the calibrated answer
was 3%"*). The page was making, in ink, the precise error the directive names.

I had written the caveat *on the page* — "Josh Allen sits in your pick-17 cell and the calibrated
chance is about 3%" — and thought that discharged it. **It does not.** A caveat explaining why the
picture is wrong is worse than a picture that is right: it costs the reader a translation step at
60 seconds a pick, and Matt's whole stated reason for wanting this format is *"so i don't need to
do mental math."* **Print the corrected number, not the number plus an apology.**

## 2. WHAT WAS APPLIED — two measured behaviours, nothing invented

Base coordinate is **`eff_pick`**, the keeper-depleted one (§2.1e), because that is the space
§4.12's noise and the opponent model were fitted in.

| adjustment | source | effect |
|---|---|---|
| **Snyder takes Allen at his turn** | §5 / §4.12, fitted q ≈ 0.90; 4-for-4 when available (2.21, 2.23, 2.21, then 1.01 overall in 2025); the 2024 miss was a two-pick snipe | Allen drawn at **9**, not 17 |
| **TE effective ADP +15 picks** | §4.12, fitted. Corroborated independently by §4.7: **zero** TEs inside the first 17 picks in 2024 or 2025, one TE before round 3 in 43 team-seasons, median first TE round 7 | 19 TEs slide 15 picks later |

**20 of 144 cells move.** That is the whole adjustment. No new model was built and none was needed
— both numbers were already in the directive, unused by any artifact.

**The TE shift turns out to be the more valuable of the two.** It moves **McBride 23 → 33** and
**Bowers 24 → 34**, i.e. from "gone before your pick 32" to "plausibly still there at 32." §4.3 says
those are the only two TEs carrying a premium and §7 lists both in the pick-32 tie — so three
independent parts of the project now agree on the page instead of contradicting each other on it.

**Where the §7 five land after adjustment: Lamar 24 · Kyren 26 · Hall 27 · McBride 33 · Bowers 34 ·
Judkins 35.** They straddle pick 32. §7's instruction — *"any of them, first one showing"* — is now
something you can see rather than something you have to remember.

## 3. WHAT WAS DELIBERATELY NOT DRAWN, AND THIS IS THE PART TO KEEP

The obvious way to make a grid "smart" is to colour each cell by how far our board rank sits from
the market's pick — *we like him more than they do*. **That is the single most tempting thing to
draw on this page and it is the one thing measured to be backwards.**

- §4.13 tested it as "the market is sleeping on him" against 324 player-seasons: **rho −0.079, the
  worst of three signals. Retired.**
- §4.22(b) re-measured it on a different market: **rho −0.173, p<0.001, n=409** — stronger, same
  wrong direction.
- The VALUE LADDER greys its own **BOARD** badge out and excludes it from the agreement count for
  exactly this reason, and says so in its key.

So no cell is coloured by board-vs-ADP, and the script says why in a comment at the top so the next
session does not "improve" it back in. `[TESTED — twice, two markets, both negative]`

## 4. THE FOUR MARKS, AND WHY THEY ARE RANKED

Matt asked for hot spots and traps. They exist, but they are **not of equal strength**, and a page
that draws them at equal weight is lying by layout. Ranked on the page, strongest first:

| mark | what it is | strength |
|---|---|---|
| **★** | the only names §7 ranks at pick 32 — dollars, 100 board states, N=2,000 paired drafts | **hardest number in the project.** Shown only in rounds 2–4 |
| **−$n** | same measurement's other half: CI-clear *behind* those five, by that many dollars | same test, same strength |
| **green bar** | on the VALUE LADDER for one of his picks | **a shortlist, not a ranking** — three tests found no link and the sign leans backwards |
| **AVOID / DISC** | the injury sweep's grade. 8 AVOID + 32 DISCOUNT inside the 144 cells | one sourced report each |

**Matt's pick-32 cell currently holds Davante Adams at −$14.** The page draws the trap *in his own
cell* with the five better answers in the cells around it. That is the single most useful thing on
the sheet and it exists only because §7's dollars were brought onto it.

## 5. THREE THINGS VERIFIED BY EXECUTION, NOT BY EYE

1. **The snake arithmetic asserts its own property**: every one of Matt's picks must land in
   column 8, and the 144 cells must cover picks 1–144 exactly once. **Negative control run first** —
   an off-by-one injected into the even-round formula produced
   `AssertionError: snake is wrong: pick 17 lands in column [7], not 8`. A guard that has never
   fired is not a guard (§0.2).
2. **The Chrome path was tested, not the wkhtmltopdf path.** My container has `wkhtmltopdf`; Matt's
   does not (§8/doc 146). `shutil.which` was stubbed to hide it so `to_pdf.find_renderer()` fell
   through to Chrome — the renderer that will actually run on his machine.
3. **The green value bar was checked against every position tint at 200 dpi**, because a dark-green
   bar on the light-green RB fill could have been invisible. It is not. Rendering a mark and
   *seeing* it are different claims.

## 6. TWO SMALLER FIXES FROM THE SAME MESSAGE

- **Matt's column is one continuous red strip**, not twelve outlined boxes. He asked for "the
  border, not the horizontal lines" — the per-cell outlines were drawing rungs that read as a
  second table nested inside the first.
- **Every cell now carries its overall pick number**, faint in grey, red in his column. He said the
  format helps because *"i don't need to do mental math"*; making him count cells to find pick 89
  was mental math.


## 7. VOR ON EVERY CELL — Matt asked, and it is the right number

*"Can the VOR number be included for each player? I think that helps the most, unless you
recommended another."*

**Yes, and I do not have a better one.** VOR (`proj_leaguepts − replacement[pos]`, §4.1) is what
the board sorts by, what §4.10's rollout maximises, and the only quantity on this project that is
comparable across positions by construction. Shipped: **top-left of every cell, in the position's
colour. Value on the left, price on the right.** Under the name, his rank inside his own position
(`RB2`, `TE1`) — free to compute and it reads faster than the raw number.

**Two things were added with it, and both are the reason it works rather than decoration:**

**(a) VOR greys out below replacement.** 72 of the 144 drawn cells are negative. §0.3 is explicit
that *"rank comparisons among below-replacement players are noise"* — so those numbers are printed
in grey and the eye skips them. The side effect is the most useful thing on the page: the colour
drains out of the grid somewhere in **round 5–6**, and that transition *is* replacement level drawn
across the whole board. Round medians run **+109 · +69 · +36 · +20 · +5 · −3 · −2 · −16 · −17 ·
−39 · −38 · −72.** Matt asked to *see the structure of the draft*; that is the structure.

**(b) A news-zeroed player is now unmistakable.** Josh Jacobs is on this grid — at **pick 52**,
because the grid draws where the *room* will spend picks and somebody will spend one on him. Before
VOR he was an ordinary-looking RB cell. He now reads **−169 against a round-5 median of +5**, with
a red **NEWS OUT** chip. The number alone gives him away; the chip says why.

**THE ONE RISK, AND IT IS NOT HYPOTHETICAL.** Putting VOR and the pick number side by side invites
exactly the inference this project has killed twice — *"big VOR, late pick, therefore bargain."*
Retired at **rho −0.079** (n=324, §4.13), re-measured **backwards at −0.17** (n=409, §4.22b).
So the legend says it in the plainest words available, immediately under the two numbers it is
about: **read VOR down a round to see where value falls off; do not hunt gaps with it.** Nothing is
coloured by the gap, and §3 of this doc is the note to the next session about why.

**Where the ladder and VOR disagree, both are drawn and neither wins.** Chris Rodriguez Jr. sits at
pick 133 with a green value-ladder bar and a grey **−99**. That is correct on both counts: at pick
133 every player is below replacement, so the ladder is doing its only job — which of the noise has
several independent sources pointing at it — while VOR says the whole region is noise. §4.13's
*"risk from round 9, never before"* is the reconciliation, and it needs both marks visible to be
readable.

## 8. AND THE LAYOUT WAS MEASURED, NOT EYEBALLED

Adding VOR pushed round 12 onto a second sheet, and a two-page grid defeats the point of a grid.
I guessed at the fix twice and was wrong twice, then measured: rendered the table alone and the
legend alone, and took the content extent out of each PDF with `pdftotext -bbox`. **Table 505pt,
legend 113pt, usable page 578pt — over by 40pt, about 7%.** That said exactly how much to take out
and from where. One page, content bottom at **567pt of 595 usable.**

Same lesson as §0.2's profile-do-not-reason, in a place nobody thinks of as a measurement.


## 9. BUY, THE ANALYST CASE, AND A SPLIT INTO TWO SHEETS

Matt: *"can we add the AVOID, buy and bull too?"* then, *"I remember you telling that the early
rounds stick to the board and the later rounds need a bit more decision making. Perhaps if it's
spread across two sheets that helps and the cells can be bigger."*

**AVOID was already there** (red chip, 8 of the 144 cells) — worth saying rather than silently
re-shipping it. `buy` and the bull/bear case are new, and the split is his idea and a good one.

**`bull` could not go on as written and should not have.** The prose runs to 400 characters against
a ~100px cell. But the data has a better field for this: **`lean`**, a ≤15-character verdict, and it
is populated on exactly the 34 players who have *both* a bull and a bear case written.
**`bear` never appears without `bull` — 34 and 0** — so a bull-with-no-lean means somebody wrote the
upside and nobody wrote the other side, which is itself worth a distinct mark. Shipped as five
glyphs: ▲▲ strongly bull · ▲ lean bull · ◆ genuinely split · ▼ lean bear · △ bull case only.

**THE MARK THAT NEEDED A WARNING IS ◆.** A "genuinely split" diamond reads as *interesting*. §4.13d
measured the opposite: the six-ranker panel is closer to **one opinion measured six times** (mean
pairwise r 0.81), and **disagreement, controlling for price, predicted finishing WORSE — −0.244,
p=0.0009.** The key says so directly under the glyphs. This is the third mark on this page that
needed its own measurement printed beside it to stop it being read backwards.

**The chips cost no height, because the layout was wrong before.** AVOID/DISC used to float with
`clear:right`, which stacked each chip on its own row — every marked cell was a line taller than it
needed to be. Line one is now a flex row: **VOR · chips · pick.** Adding BUY on top of AVOID/DISC/
NEWS OUT made the page *shorter*.

**The split is at round 9, and it is not an aesthetic choice.** §4.13: *"risk from round 9 (picks
104, 113, 128, 137). Never before."* A global upside tilt costs $22–41 of expected payout; a
round-9-and-later tilt is free. That is exactly Matt's "early rounds stick to the board, later
rounds need decision making," and it is measured, so the seam goes there.

| | rounds | cell | what it says |
|---|---|---|---|
| **Sheet 1** | 1–8 | 76px | **the board decides.** Pick 8 closed; at 32 take the engine's #1 rather than override it. Read a round's shape, spot a run — do not pick off it |
| **Sheet 2** | 9–12 | 136px | **you decide.** Everything here is below replacement, which is *why* the ordering stops helping. Carries §4.20's job flag and **what the job is worth**, the analysts' lean spelled out, and DART / ROOKIE |

§4.20's line is printed at the top of sheet 2 because it is the whole point of the extra room:
**buy the job, never the name** — measured on 19 unsettled backfields, the flag has no opinion on
who wins, and neither should the reader.

**Each sheet carries the full key.** A printed pair where page 2 explains page 1's marks is one
sheet, badly stapled.

## 10. AND THE HEIGHT IS NOW NAME-INDEPENDENT, WHICH IT WAS NOT

The name box is locked to two lines. Before that, a long surname wrapped, that one cell grew, and
round 12 landed on a second sheet — **and the 7:00 PM keeper swap changes twelve names on this
board**, so the layout would have been decided by whoever the twelve keepers turned out to be.

Locking it introduced a *silent* failure in its place: a name too long now clips instead of
wrapping. So the script measures every drawn name against the fit (17 characters at 10.8px in a
~97px cell) and **prints a warning naming the player**. The widest surname on the whole 480-row
board is `Westbrook-Ikhine` at 16, so it should never fire.
**Negative control run:** an 18-character surname produces
`!! NAME MAY CLIP: "Featherstonehaughs" (18 chars > 17)`. A 17-character one correctly does not.

Headroom after all of it: page 1 ends at **536pt**, page 2 at **501pt**, against 595 usable.

---

**Files:** `Scripts\make_gridboard.py` (11,819 → 17,9xx) · `Source\ADP_GRID.html` / `.pdf`
(two landscape pages: rounds 1-8, then 9-12). `sync_desk_copies.py` already owns `ADP_GRID.pdf`, and `tidy_docs.py` derives
its protected list from that file, so the dated desk copy is protected automatically.

**Open:** the grid is a *placement* estimate, not a survival model. It now carries two calibrated
corrections; it still has no opponent model. §4.15 stands — the live board's simulated
`still there?` remains the only survival number, and it too runs optimistic.