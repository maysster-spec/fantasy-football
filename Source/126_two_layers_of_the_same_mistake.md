# 126 — ESPN says the mock league is DELETED. And the prerank was telling you to reach.

**Date:** 2026-09-01. Two findings, both from artifacts rather than reasoning.

---

## 1. THE MOCK QUESTION IS CLOSED. ESPN SAYS IT IN WORDS.

`feed_evidence\20260901_070737_pollfail_934208921_2026_err.json`:

```json
{"messages":["This League has been deleted."],
 "details":[{"shortMessage":"This League has been deleted.",
             "type":"LEAGUE_NOT_FOUND_DELETED"}]}
```

**That is the 404, in ESPN's own words, and it was never about cookies or authorisation.**

**Four mock rooms, four identical stories.** Every `firstok` snapshot is **exactly 78,745 bytes** —
`910821995`, `629362362`, `1449026878`, `934208921`. Byte-identical payloads from four different
leagues, each followed by a `pollfail` a few minutes later. In every one:

- `status.createdAsLeagueType: 21985` — each room is a **clone of the real league**
- `teamsJoined: 1` — only Matt ever joined
- `pickOrder: [13,11,7,12,4,6,5,9,3,1,2,10]` — identical every time
- **1 real pick, always the same one:** playerId 4426354 (Pickens) at overall 176, `reservedForKeeper`
- `drafted: false`, `inProgress: true`, and **it never changed**

**CONCLUSION, now evidence-backed: `lm-api-reads` serves a mock room's OPENING STATE and never the
live picks, then returns LEAGUE_NOT_FOUND_DELETED once the room closes.** The tool cannot follow an
ESPN mock. Not a bug to fix — an endpoint that does not carry the data.

**Doc 119 guessed "the room was torn down" and was right in substance with no evidence for it.
That is still the E8 error.** A right guess and a finding are different objects; this is the finding.

### The risk this leaves open, and it is the important one

**Nothing has ever verified that `lm-api-reads` carries picks DURING a live draft** — not for a mock,
and not for the real league. Docs 58 and 84 read *completed* drafts; `--replay 2025` reads history.
The live path is untested and the mock cannot test it.

**The experiment that CAN: create a throwaway ESPN league — a real one, not a mock — with autopick
bots, start its draft, and point the tool at it.** A real league has a persistent id and exercises
exactly the path Sept 7 uses. It is the only remaining way to find out before the night itself.

---

## 2. THE PRERANK WAS TELLING HIM TO REACH — measured

Matt: *"Stafford and Warren were listed on the ESPN board as best player available. Makes me wonder
about our preranking."* **He was right, and this is the second-worst defect found this week.**

ESPN's draft room reads YOUR custom rankings for "best available". The shipped prerank is a
**pure VBD sort, monotone, with no roster or market logic at all:**

| prerank | player | pos | VBD | **ADP** |
|---|---|---|---|---|
| 36 | Tyler Warren | TE | 28.1 | 51.4 |
| **40** | **Matthew Stafford** | **QB** | **21.2** | **86.1** |
| 41 | Bucky Irving | RB | 20.0 | 55.6 |

**Stafford was listed forty-six places ahead of where the market takes him.** Following that list
pays pick 40 for a player available at 86 and loses whoever was on the board in between — which is
exactly what Matt did and exactly what he noticed.

**The VBD is not wrong. A value ranking is not a draft order.** §4.4 measures this board at
**QB +15.7 and TE +18.0 against consensus by construction**, so a naked VBD sort front-loads those
two positions — the two positions he was being offered all night.

**`make_prerank.py`** applies one rule: *a player may not be listed more than `slack` slots ahead of
his own ADP* (default 8). If he will still be there later, taking him now costs you the player you
could have had — the live board's own `cost vs #1` idea, applied statically.

**ADP is used as a PRICE, never as an opinion.** §4.13 retired ADP-minus-projection as a predictive
signal (rho −0.079, worst of three). VBD still decides who is better; ADP only stops you paying
early for it.

**Effect, top 120: 51 players move 6+ slots.** Stafford **40 → 63**. Burrow 35 → 41. Purdy 57 → 79.
Mahomes 64 → 81. Bo Nix 54 → 70. Rising to meet them: McConkey 45 → 38, Waddle 50 → 42, Pitts
60 → 50, Marvin Harrison 74 → 60. **The top 24 becomes 13 RB / 8 WR / 2 TE / 1 QB** — a draft board
rather than a value table. The elite tier barely moves, because elite players are priced near
their value.

**Two guards in the builder**, both from this week's lessons: it carries the **64 K and D/ST rows**
the board has never contained (a 480-row list would let ESPN autodraft a kicker of its own choosing),
and it **refuses to write a list shorter than the shipped one.**

**It is audit-only by default and it changes NOTHING in the draft room until the prerank is
re-injected** — which is Matt's lane (§0.4: anything that writes to ESPN).

---

## 3. THE LATE-ROUND UPSIDE LIST HE ASKED FOR

*"I kept getting veterans with low ceiling in the later rounds and not players who could trend up."*
Picks 104–137, gated to the real-ADP region (§4.14), ranked by open job + analyst lean + BUY:

| goes at | player | pos | why |
|---|---|---|---|
| 99 | Kenny Gainwell | RB TB | OPEN behind Bucky Irving, **job worth 189** — the biggest job on this list |
| 100 | Jonathon Brooks | RB CAR | OPEN behind Hubbard, BUY, 2nd-round capital · DISCOUNT (two ACLs) |
| 118 | Rachaad White | RB WAS | OPEN behind Croskey-Merritt, BUY · DISCOUNT (hamstring) |
| 120 | RJ Harvey | RB DEN | OPEN behind Dobbins — **and Dobbins is the AVOID on this board** |
| **127** | **Jordan Mason** | **RB MIN** | **OPEN behind a 31-year-old Aaron Jones · BUY · LEAN BULL** — the only name carrying all four |
| 140 | Tyjae Spears | RB TEN | OPEN behind Tony Pollard (foot sprain) |
| 151 | Tyler Allgeier | RB ARI | behind Jeremiyah Love, **job worth 246** — and Love has a high ankle sprain |
| 115 / 125 | Xavier Worthy · Makai Lemon | WR | the two late WRs with a bull lean |

**Jordan Mason at 127 is the cleanest shape on the board**: unsettled backfield, a job worth 153,
both analyst panels ahead of ADP, and the only late name with a bull lean on top. **Tyler Allgeier
at 151 is the biggest job** — 246 points — and the man ahead of him is hurt right now.

**Against KC Concepcion (goes at 133, no job, no lean, WR5-ish) that is not a close comparison.**

## ASSUMPTIONS

1. **`slack = 8` is a judgement, not a measurement.** Nothing here measures the right number; it is
   set to be visibly conservative. `--slack N` changes it and the audit shows the effect.
2. **ESPN's draft room really does use the injected prerank for "best available."** Consistent with
   what Matt saw; not independently verified.
3. **A throwaway real league would exercise the live path.** Believed, untested — that is the test.
