# 113 — Your brother's list against slot 8, and the injury sweep that should have caught Monangai

**Date:** 2026-08-31, evening.

---

## 1. HIS LIST, SORTED BY WHETHER YOU CAN ACTUALLY GET THEM

Method: the player's `eff_pick` (his ADP in the keeper-depleted coordinate, §2.1e) against the
§4.12 noise `sd = 0.111 × ADP + 5.40`. **"wait until" is the LATEST of your fourteen picks at
which he is still there — the safe column is P ≥ 0.85, the coin column is P ≥ 0.50.**

**This is dispersion only, and §4.15 is explicit that dispersion alone runs OPTIMISTIC** — it has
no opponent model in it. For this question that is the safe direction: it keeps a player on your
research list rather than cutting him wrongly. Treat every number as a ceiling.

### Cannot happen — do not spend a minute
| player | why |
|---|---|
| **Chris Olave** | **KEEPER — Taylor's. Not in the draft at all.** |
| **Colston Loveland** | **KEEPER — Rychlicki's. Not in the draft at all.** |
| Jahmyr Gibbs | eff 1.4. P(there at 8) = 0.12 |
| Ja'Marr Chase | eff 4.2. P = 0.26 |

### Live at pick 8, gone by 17 — these are your actual pick-8 menu
| player | pos | eff | P at 8 |
|---|---|---|---|
| Jaxon Smith-Njigba | WR SEA | 5.9 | 0.37 |
| James Cook III | RB BUF | 11.4 | 0.69 |
| De'Von Achane | RB MIA | 12.0 | 0.73 |

### Reachable at 17 — and this is where his round-2 list lands
| player | pos | eff | safe until | coin until |
|---|---|---|---|---|
| Chase Brown | RB CIN | 19.6 | 8 | **17** |
| Ashton Jeanty | RB LV | 19.8 | 8 | **17** |
| Kenneth Walker III | RB KC | 23.6 | 8 | **17** |
| Malik Nabers | WR NYG | 31.3 | **17** | 17 |

### Reachable at 32 or 41 — most of his rounds 3–5
| player | pos | eff | safe until | coin until |
|---|---|---|---|---|
| DeVonta Smith | WR PHI | 35.0 | 17 | **32** |
| Emeka Egbuka | WR TB | 37.7 | 17 | **32** |
| Ladd McConkey | WR LAC | 38.5 | 17 | **32** |
| Tyler Warren | TE IND | 41.4 | 17 | **41** |
| Quinshon Judkins | RB CLE | 42.5 | 17 | **41** |
| Jaylen Waddle | WR DEN | 44.3 | 32 | **41** |
| DJ Moore | WR BUF | 52.6 | 32 | **41** |

### Reachable at 56 — his round 6
| player | pos | eff | safe | coin |
|---|---|---|---|---|
| Bhayshul Tuten | RB JAX | 58.0 | 41 | **56** |
| Jadarian Price | RB SEA | 62.8 | 41 | **56** |
| Harold Fannin Jr. | TE CLE | 63.2 | 41 | **56** |

### Reachable at 80–89 — his round 7 and his QBs
| player | pos | eff | safe | coin |
|---|---|---|---|---|
| Parker Washington | WR JAX | 81.3 | 65 | **80** |
| Caleb Williams | QB CHI | 81.5 | 65 | **80** |
| Christian Watson | WR GB | 81.8 | 65 | **80** |
| Trevor Lawrence | QB JAX | 83.9 | 65 | **80** |
| Justin Herbert | QB LAC | 86.4 | 65 | **80** |
| **Jonathon Brooks** | RB CAR | 99.6 | **80** | **89** |

### Reachable at 104+ — the darts
| player | pos | eff | safe | coin |
|---|---|---|---|---|
| De'Zhaun Stribling | WR SF | 133.4 | 104 | 128 |
| Jalen Coker | WR CAR | 145.4 | 113 | 137 |
| Jonah Coleman | RB DEN | 157.4 | 128 | 152 |
| Cyrus Allen | WR KC | 157.6 | 128 | 152 |

**§4.14 caveat on the last block: past roughly pick 120 two thirds of the board sits inside ESPN's
undrafted sentinel and the ordering there is fabricated. Stribling, Coker, Coleman and Allen have
no real market price — "available at 128" means nothing more than "nobody has a price on him."**

### The three worth flagging
- **His QB trio is a real convergence with our own work.** Caleb / Lawrence / Herbert all sit at
  eff 81–86, i.e. **your pick 80 or 89**. §4.14 says there is no correct target pick for QB —
  one cliff at Allen, then a flat plateau — and those three are on the plateau at the exact turn
  where the board tends to offer nothing else. That is a fit, not a coincidence.
- **Jonathon Brooks is a full round later than his brother's list implies.** Round 6 in his league;
  here he is a **pick-89 coin flip and safe at 80**, which is earlier than your 104/113 dart
  window. If you want him you are paying a real pick, not a dart.
- **Tyler Warren at 41 collides with the §4.3 finding.** Only Bowers (+51.2) and McBride (+47.6)
  carry a TE premium; Warren is +28.1 and then a long flat tail. He is takeable at 41 — whether he
  should be is a different question and §6's doctrine says no.

---

## 2. NEITHER SWIFT NOR MONANGAI IS IN THE ANALYST CORPUS AT ALL

Matt asked whether we already had write-ups. **We do not. Zero rows for either, in both
`favorite-analysts-calls-2026.csv` and `raw-analyst-calls-v2.csv` (78 joined rows total).**
Swift's only mark is quantitative — the panel residual **+8.6**, meaning both panels rank him ahead
of ADP after removing position and band effects. That is not a written take, it is arithmetic.

**What exists outside the corpus, found today, and it cuts against Matt's take on both:**
- **Swift IS in a contract year** — free agent in 2027, Bears projected around $13M of 2027 cap
  space. Matt's on-the-fly catch is correct. `[SOURCED: SI/OnSI, Aug 2026]`
- **Jason Katz (PFN, Aug 29):** *"Swift... not only firmly holds the primary gig, but he is also
  the far better play at price. Monangai remains an elite handcuff and can be a viable flex in
  times of need."* `[SOURCED]`
- **That Aug-29 piece does not mention Monangai's Aug-17 knee.** A fantasy outlook published
  twelve days after the MRI, silent on it. Which is the whole argument for section 3.

**Katz is not one of Matt's analysts** (Footballers, Boone, Harmon, FantasyLife, Zachariason,
Gretch, Raybon, Waziak), so he does not move `calls_up`. Both quotes are on the live board's hover
as sourced notes with that caveat attached.

**On the contract-year theory itself:** it is plausible and it is `[HYPOTHESIS]` here. Nothing in
this project codes contract status, so it cannot be tested against anything we hold, and the public
research on contract-year effects in the NFL is mixed. Do not let it carry weight it has not earned.

---

## 3. THE SWEEP — the approach, and why the importer matters more than the prompt

Matt's instinct to send a fresh sweep is right, and the reason is measurable: **of the 143 players
inside eff_pick 155, only 17 carry an injury grade.** 126 have nothing at all. The sheet was never
comprehensive; Monangai is just where that showed.

`Source\GEMINI_INJURY_SWEEP.txt` is the prompt. Three things in it are there because of specific
failures in this project:
1. **"Start a brand-new notebook with no sources attached"** — the Aug-31 report returned
   wrong-season analyst quotes because an old notebook's sources were still checked (doc 103).
2. **"Return a CSV, one row per player, and a HEALTHY row still counts"** — silence is the failure
   mode. A player quietly absent from the output is worse than one wrongly marked healthy.
3. **"Every non-healthy status needs a date and a URL; do not editorialise about credibility"** —
   the Mahomes episode, where a report called a real injury possibly fabricated (doc 83).

It also asks for **current status and injury *history* separately**, and for a closing list titled
CHANGED SINCE AUGUST 30, which is the only part that needs acting on.

**`Scripts\import_injury_sweep.py` loads the answer back.** It audits by default and writes nothing:
it refuses a row whose status has no source URL, refuses an unknown grade, refuses a name that does
not resolve to exactly one board row — and then **prints which shortlist players the sweep never
mentioned**, which is the check that would have caught Monangai. It writes only `grade` and `why`
and asserts that `mine`, `dart`, `buy` and the analyst-call columns did not move. **It will not
zero a player who is out for the season** — it prints the `news_overrides.csv` line instead,
because removing a player from the board should stay a deliberate act. All four guards verified by
execution against a deliberately broken sweep file.

---

## 4. THE HOVER — there is no trade-off to make

Matt: *"I'm conflicted if the hot take hover should be my note or an analyst. I'm biased and may
not even be accurate."*

**It is already both, and his note does not displace anything.** The tooltip is assembled in this
order and every part that exists is shown:

> `ESPN: QUESTIONABLE | YOUR TAKE: better blocker by far, earns snaps; Swift is 27... | AGREEING:
> ROLE: direct backup in an UNSETTLED backfield — the job is worth 196 pts to whoever wins it |
> Jason Katz (PFN, Aug 29): "Monangai remains an elite handcuff..."`

The gold **MINE** badge marks that a take exists; the hover carries the take *and* the evidence
next to it. **The bias he is worried about is handled by putting his own words where he can see
them beside the sourced ones, not by hiding either.** No change needed.

---

## ASSUMPTIONS

1. **Availability is dispersion-only and therefore optimistic** (§4.15 measured it 25× wrong on a
   player with a known taker). Safe direction for a research triage; wrong tool for a pick decision.
2. **His brother's league is not this one** — different size, scoring and keeper rules, so his round
   numbers are his own. Only the player identities transfer.
3. **The corpus is complete as a record of what was scraped**, so "zero rows for Swift" means the
   scrape missed him, not that no analyst has spoken. The sweep is the fix for that too.
