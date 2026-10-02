# 114 — "Your analysts" is a coverage list, not a quality ranking; and the 20 positions we hold without an argument

**Date:** 2026-08-31, late.

---

## 1. I FRAMED KATZ WRONG AND MATT CAUGHT IT

I wrote that Jason Katz "is not one of your analysts," which reads as a demotion. It is not one,
and the directive already says why: **§4.13d — you cannot use the FantasyPros accuracy contest to
justify following an analyst, and you cannot use it to dismiss one either.** The panel is one
opinion measured six times (mean pairwise r **0.81**), the contest is structurally blind to
breakout skill (being 10% tidier on ordinary players scores **2.80×** as much as perfect foresight
on every breakout), and disagreement among rankers predicts finishing **worse** (−0.244, p=0.0009).

**So the eight names — Fantasy Footballers, Boone, Harmon, FantasyLife, Zachariason, Gretch,
Raybon, Waziak — describe WHICH SHOWS WE SCRAPED. They are a coverage decision, and the only
evidence about them is that we have no evidence.** A player absent from the corpus is a hole in our
scraping, not a verdict on him, and an outside voice with a better argument is a better argument.

Corrected on the live board's hover for both Swift and Monangai, and written into the new
GEMINI_DELTA_TAKES prompt as an explicit instruction: *"that is a list of who I happen to read,
NOT a quality ranking... if a stronger case is made by somebody I have never heard of, give me
that one and name them."*

**The directive needed no change — my phrasing did.** Worth recording because it is a soft version
of the same failure §4.13d exists to prevent.

---

## 2. DEEP RESEARCH, NOT A GROUNDED NOTEBOOK — and it matters here specifically

Matt asked which one to run. **The injury sweep needs live web search, so Deep Research is the
right tool.** A notebook grounded only in attached sources cannot see news it was not handed, and
will report on it with the same confidence either way. **That is precisely the failure this sweep
was written to fix** — Monangai's Aug-17 knee was not contradicted anywhere, it was simply absent.

He is running both to compare, which is fine, so `GEMINI_INJURY_SWEEP.txt` now opens by branching:
Deep Research gets "start fresh, attach nothing"; a grounded notebook is told to **declare that in
one line before anything else, treat every HEALTHY row as UNKNOWN, and leave the CHANGED SINCE
AUGUST 30 section empty rather than guess.** A comparison is only useful if the weaker tool is
made to admit what it cannot see.

---

## 3. WHERE WE DISAGREE WITH THE MARKET AND CANNOT SAY WHY — `delta_gaps.py`

Matt: *"do we need more analyst takes on the player deltas?"* Yes, and this narrows it from
"scrape everything again" to twenty names.

**FIRST, WHAT THIS IS NOT.** §4.13 **retired** ADP-rank-minus-projection-rank as a predictive
signal: tested on 324 player-seasons it was the **worst of the three** tried, rho **−0.079**, and
its coldest quintile broke out at **3.1%** against a base rate near 11%. **A big delta is not a
good pick and this list is not a shopping list.** It answers a different question: where are we
taking a position against the market with no human explanation on file for it? That is worth ten
minutes of reading before the draft, not a pick during it.

**THE DELTA HAS TO BE RESIDUALISED OR IT IS AN ARTIFACT.** Raw, the mean delta by position is
**QB +4.5 · TE +7.6 · RB +1.4 · WR −5.6** — which is just §4.4's measured board bias (QB +15.7,
TE +18.0 against ECR) showing up again. The raw top of the list was nine QBs and TEs and not one
of them was a real disagreement. Demeaning within position × ADP band removes it, the same
correction the analyst residual already uses.

**Result: 142 players inside reach, 57 with any analyst call, and these 20 gaps.**

| we rate him above the market | goes at | | the market rates him above us | goes at |
|---|---|---|---|---|
| Kyle Monangai (RB CHI) | 114 | | Travis Hunter (WR JAX) | 108 |
| Brock Purdy (QB SF) | 95 | | Kyler Murray (QB MIN) | 131 |
| Alec Pierce (WR IND) | 94 | | RJ Harvey (RB DEN) | 120 |
| **Tank Dell (WR HOU)** | 146 | | Kenny Gainwell (RB TB) | 99 |
| Jared Goff (QB DET) | 124 | | Woody Marks (RB HOU) | 138 |
| Jacory Croskey-Merritt (RB WAS) | 122 | | Isaiah Likely (TE NYG) | 113 |
| Kenyon Sadiq (TE NYJ) | 143 | | Jaxson Dart (QB NYG) | 69 |
| Matthew Golden (WR GB) | 96 | | Trevor Lawrence (QB JAX) | 84 |
| Joe Burrow (QB CIN) | 47 | | Marvin Harrison Jr. (WR ARI) | 71 |
| Patrick Mahomes (QB KC) | 96 | | Chris Godwin Jr. (WR TB) | 121 |

**Read the left column carefully, because Tank Dell is on it.** Our board rates him well above the
market and our own injury sheet has him at **2 expected games** (doc 98, where I recommended him
and had to retract). **"We rate him above the market" very often means our projection is stale,
not that we found something.** The market had the injury priced and we did not. That is the single
most useful thing this list does: it surfaces where our own data is behind, and the same mechanism
put Monangai at the top of the same column.

`py delta_gaps.py` prints it; `--prompt` writes `Source\GEMINI_DELTA_TAKES.txt`, which asks for the
bull case, the bear case, which way the weight of commentary leans, and one sourced verbatim quote
per side with NONE FOUND permitted — the fabricated-quote problem from doc 103 written into the ask.

---

## ASSUMPTIONS

1. **The corpus's 57-of-142 coverage is a scraping artifact**, so a gap means "not scraped," not
   "nobody has spoken." *Killed by:* the sweep coming back with nothing on several of the twenty.
2. **Position × band demeaning removes the whole artifact.** It removes the measured part; a
   residual bias inside a band would survive. Unresolved and probably small.
3. **A delta with no commentary is worth reading about.** Untested — it is a triage heuristic, not
   a finding, and §4.13 is explicit that the delta itself predicts nothing.
