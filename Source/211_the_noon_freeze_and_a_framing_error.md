# 211 — the noon freeze, an injury sweep, and a framing error that was mine

**2026-09-07, 13:30 ET, T−6.5h.** The final ADP freeze ran at 12:59. This is the §0.5(d)
milestone pass, a draft-day injury sweep, and a correction to something I put in front of Matt
two messages ago that he then reasoned from.

---

## 1 — §2.1(c) IS UNCHANGED ON THE NEW FREEZE

Read straight off the rebuilt `board_v8_fixed.csv`, not re-derived (doc 144 / §8):

| pick | keepers ahead | directive says | |
|---|---|---|---|
| 8 · 17 | 0 | 0 | holds |
| 32 | 4 | 4 | holds |
| 41 · 56 · 65 | 10 | 10 | holds |
| 80 · 89 | 11 | 11 | holds |
| 104 → 161 | 12 | 12 | holds |

**Twelve of twelve rows hold. Nothing to re-publish.**

**AND I NEARLY SHIPPED A WRONG ONE.** My first pass reconstructed the twelve keeper ADPs from
where `gone_ahead` steps up in the board. That recovers the **boundary** — the ADP of the first
row past the keeper — not the keeper's own ADP, so it pushed every keeper later and produced
"pick 32: 4 → 0 keepers, the directive is stale." It was wrong, and it was wrong in the
flattering direction (it said Matt was *shallower* than published). Caught by reading the
shipping column instead of re-deriving it, which is the rule §8 already carries. `ERROR_PATTERNS`:
**a reconstruction is not a reading.**

Every printout rebuilt and its PDF is newer than its page: DRAFT_BOARD, FALLBACK_BOARD,
OVERRIDE_CARD, VALUE_LADDER, ADP_GRID, BOARD_GRID, HOW_TO_READ_IT, TIER_SHEET — all stamped
12:59:38–12:59:53.

---

## 2 — THE FRAMING ERROR, AND IT MATTERS BECAUSE HE ACTED ON IT

I gave Matt a table headed "where the RB-vs-WR question actually lives" and listed, per turn, the
pairs **within 4.5 VOR of each other**. At pick 56 that printed *"Henderson 9.3 vs Sutton 6.2."*

He read it as the choice at 56 and replied *"I don't like either Henderson or Sutton in that
round."*

**The arithmetic was right and the object was wrong — §0.5(a2), the same shape as docs 191/195/196.**
That table answered *where are the near-ties*, and I let it be read as *who is the pick*. The best
player in that window is neither of them:

| pick 56, eff-pick window | |
|---|---|
| **Rome Odunze WR +19.4** (eff 57.2) | **three times Sutton, four times Burden** |
| Jadarian Price RB +11.9 (eff 55.7) | |
| TreVeyon Henderson RB +9.3 (eff 66.8) | not really a 56 name |
| Courtland Sutton WR +6.2 (eff 70.8) | |
| Luther Burden III WR +4.8 (eff 64.5) | |

**Matt's instinct was right and my table was the reason he had to have it.** Never hand him a
filtered list without the unfiltered one beside it.

---

## 3 — HIS THREE READS, AGAINST THE BOARD'S OWN SIGNALS

**(a) Henderson — his conclusion is right, his mechanism is not the live one.** He said the
pass-blocking issue caps the snaps. The board's objection is more immediate and it got worse
today: **has not practiced since Aug 24, DNP on the official report, Stevenson listed ahead of
him**, and a Sept 7 piece has him possibly missing Week 1 with Stevenson the starter regardless.
Graded DISCOUNT. `[SOURCED: RotoWire / NFL.com / Last Word, 2026-09-06 and 09-07]`

**(b) Sutton — the one measured thing points AGAINST his vacuum story.** Matt's claim: 2025
targets were inflated by a thin room and will regress. **Snap share 2025 is 85%, top quartile,
and it moved +0 from 2024** — the role was already that big the year before, so it is a stable
role rather than a one-year vacuum. In-20 targets 17, **in-10 targets 7**, which §4.5 measured as
the persistent kind (r=+0.59). **The real knock is not the one he named: age 30.9 against doc 202's
WR-only age slope (rho −0.175, p=0.045, n=132) — a slope, not a cliff.**
*Not measured: his target-share change 2024→2025. The snap number is a proxy for role, not for
targets, and I am not going to claim it settles his question.*

**(c) Burden — six measured reads against him, one analyst read for him.** From his own card:
zero inside-10 targets · **10.1% target share with Odunze on the field against 21% without** ·
40% snap share, bottom quartile · 12% air-yard share · vacated targets go to new arrivals ·
one archetype signal. Against that: BUY, residual +12.3, six of six panels ahead of ADP.
**§4.13d measured that the analyst panel cannot pick breakouts, so the one signal for him is the
one this project has already retired.** And the suppressor is the player the board wants at 56.

---

## 4 — DRAFT-DAY INJURY SWEEP, SEPT 6–7 ONLY

Our file was stamped 09-05/09-06. Everything below is newer than that.

| player | what, and when | why it matters |
|---|---|---|
| **Christian McCaffrey** | **did not take part in drills before SF's first full Melbourne practice, Sept 7; Shanahan gave no detail** | a **pick-8** name |
| **Puka Nacua** | groin/psoas, Sept 6, **expected to play** Thursday | a **pick-8** name |
| TreVeyon Henderson | still no practice, now two weeks; DNP, Sept 6 and 7 | confirms §3(a) |
| Emeka Egbuka | returned to practice (toe), Sept 7 | §7's −$20 list |
| **Falcons name Tua Tagovailoa the Week 1 starter; Penix inactive**, Sept 7 | | **touches Bijan Robinson and Drake London** |
| Jonathon Brooks | soreness, worked to the side Sept 7 | pick-80 dart |
| Kittle · Mike Evans | back in drills Sept 7 | — |
| Odunze · Burden · Price · Sutton | **nothing new since Sept 3–5** | our file is current on them |

**The next real wave is Wednesday Sept 9 — the first official Week 1 injury reports — which is
after the draft.** Tonight's information is as complete as it is going to get.

---

## 5 — WHAT THIS DOES TO DOC 200'S PICK-8 RULE: NOTHING, PLUS ONE SENTENCE

Doc 200 says take the highest VOR on the board at 8, and names Gibbs · McCaffrey · Bijan · Nacua ·
J. Taylor · Chase · JSN · St. Brown. **Two of those eight picked up a fresh flag today.**

The rule stands. McCaffrey is **+134.9** against St. Brown's **+101.3** — a 33.6-point cushion,
and a no-detail absence from one walkthrough is not worth 33 points. Neither man is ruled out;
both resolve on Wednesday.

**But doc 200 carried an unstated assumption and it is worth writing down: it treated a slip to
pick 8 as random.** Tonight there are two names with a public reason to slip.
**If one of the eight falls to you, that is still the pick — but glance at whether the room is
reacting to this news rather than making a mistake.** The cushion is big enough that it does not
change the answer; it changes how surprised you should be.
