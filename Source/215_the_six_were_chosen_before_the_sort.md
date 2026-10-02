# 215 — The six were chosen before the sort: the D/ST fix, and the red team Matt asked for

**2026-09-07, 16:45 ET. Draft T−3h15m.** Matt: *"I'm hesitant about the red team action we could do
with changes we've made today. Do you not recommend."* **He was right and I was wrong to say
"nothing to run."** §0.5(d) lists "a milestone date arrives" as an unprompted trigger, and
`live_draft.py` was edited five times today. The sweep found a live defect in this afternoon's own
work, three hours before the draft.

---

## 0. ACTIONABLE

1. **`live_draft.py` is now 131,034 bytes / `385426fa851307c2`.** `check_kit.py` re-pinned. Both
   committed. **Run `py check_kit.py` before the mock.**
2. **The Jaguars D/ST could not appear on the tool at pick 152.** Fixed. That is the D/ST doc 212
   recommends, and Matt would never have seen it.
3. **Mike Washington Jr. is a legitimate late dart, but as a lottery ticket on Jeanty's ankle, not
   as a handcuff — unless Matt owns Jeanty.**
4. **His mock-draft command sequence has step 1 wrong** — the listener is `bridge_server.py`, not
   `live_draft.py --bridge`.

---

## 1. THE DEFECT: THE SIX WERE CHOSEN BY SEASON PROJECTION, THEN SORTED BY THE OPENING MONTH

This afternoon's edit added an opening-month rank to the streamer page (doc 213): `render_streamer`
sorts its rows by `_open4()` and paints an amber rank. **It sorts the six it is handed. It does not
choose them.**

`Engine.streamers()` returns `k.head(n)` with **`n=6`, ordered by ESPN's season projection.**

**The Jaguars are 22nd of 32 defenses by season projection (80.2) and 2nd by the opening month.**
So the amber ranking reordered six defenses that could never contain the one the recommendation
names. Measured at the realistic pick-152 state (the 8 defenses with an ADP before 152 removed):

```
OLD six shown:  CHI  LAC  CLE  GB  DET  KC        Jaguars present: False
NEW six shown:  JAX(2) CHI(4) TB(5) NO(7) LAC(8) CLE(9)
```

**This is §0.5(c)5 — the missing-row check — firing on an artifact I built four hours ago.** It is
the MarShawn Lloyd defect in a second place: the row that serves the decision was not on the page,
the row count was right, and no guard fired.

**And it is §4.8 restated.** *"D/ST draft value is not realizable... draft-day VBD for both is an
illusion."* The pool was being cut by exactly the number §4.8 says is an illusion, and only then
ordered by the thing doc 212 measured. **Cut last, not first.**

### The fix — two lines, engine untouched
- call site: `eng.streamers(pos, [...], n=32)` — ask for every available streamer.
- `render_streamer`: sort by opening rank, **then** `top[:SHOW_STREAMERS]` (6).

### Verified on the object production builds (§0.2, doc 80)
Real `Engine`, real `board_v7_kdst_separate.csv`, real HTML out: 20,925 bytes, six amber cells,
`Jaguars` on the page. **Negative control run and it reproduces the defect** — the shipped `n=6`
call returns `CHI LAC CLE GB DET KC` with no Jaguars at any depletion level.

### The kicker page moves too
At 161 the six become Santos (CHI, 4) · Reichard (MIN, 7) · Grupe (IND, 8) · Loop (BAL, 9) ·
Folk (ATL, 13) · McLaughlin (TB, 14) — ordered by the opening month, as doc 213 intends.

### One test of mine was wrong before it was right — recording it
My first coverage check resolved each row's team as `r.get('team_c') or r.get('team')` and passed
32/32. Production passes `t.get('team')`. **`Engine.streamers()` renames `team_c` → `team` in the
dict it returns, so production is correct** — but I had verified a different object than the one
that runs, which is the exact §0.2 failure, and I only caught it by reading the call chain.

### What else was swept, and held
`py_compile -W error::SyntaxWarning` (the 3.12 escape trap, §0.4) · `OPEN4` 32/32 both positions,
ranks contiguous, no duplicates · `_open4` negative controls: `LA/LAR`, `WAS/WSH`, `JAC/JAX` all
alias correctly, and `'ZZZ'`, `None`, `''` and a non-streamer position all return `None` rather
than raising · `_board_out()` resolves and is writable · `detect_shape` short-circuit.

---

## 2. MIKE WASHINGTON JR. — Matt asked, and one of his numbers does not source

**`[SOURCED]` — every date stated before use, per `ERROR_PATTERNS` B7.**
Arkansas (via Buffalo and New Mexico State), **4th round**, **6'2", 228 lb**, **4.33 forty — the
fastest back in the rookie class**; 1,070 college yards at 6.4 ypc; self-described *"downhill
runner. Punishing back"* (Review-Journal, **Aug 11 2026**). Preseason **7.9 ypc over two games**
with two 30-plus runs and PFF's top rookie-RB grade in preseason week 1; 8 carries for 49 yards
against SF in week 3 (Yahoo, **Aug 31 2026**). Kubiak split a backfield in Seattle, and the
expectation is *"complementary, downhill packages, not a pure backup who only plays in
emergencies"* (Raider Ramble, **Sep 7 2026**).

**Jeanty: lower-ankle sprain, DNP the Wednesday before the opener; Kubiak answered "Yes" to whether
he plays Week 1 at Miami on Sep 13** (Bleacher Report, **Sep 2 2026**). Our board already carries
Jeanty as QUESTIONABLE.

**THE ONE NUMBER THAT DOES NOT SOURCE — §0.5(a).** Matt: *"He's expected to get 30% of the share as
it is?"* **No source found gives a share figure.** ESPN's own projections put Washington at 61.0
against Jeanty's 248.2 — **20% of the pair**, not 30%. The *direction* of his read is supported by
two independent outlets; the number is his own and runs about a third high.

**AND THE BOARD DISAGREES WITH THE FRAME.** §4.20's flag is computed from the RB1−RB2 projection
gap: Jeanty − Washington = **187.2**, which is **LEAD BACK (≥150)**, not UNSETTLED. **Las Vegas is
not an open job.** Washington's value is entirely contingent on Jeanty missing time.

**WHAT THAT CONTINGENCY IS WORTH — doc 207, and it is large.** A team's next man scores **12.0**
half-PPR points in weeks the lead back is out against **6.1** when he plays. **Inheriting a
backfield roughly doubles a back**, and 8 of the 15 late ratio-booms in §4.13c were backs who
inherited one. Washington's ADP of **162.8** sits inside §4.13's 121–180 band (17% ratio-breakout
rate) and inside §4.20's `adp_pick < 168` dart gate.

**THE DISTINCTION THAT DECIDES IT:**
- **If Matt takes Jeanty at 17**, Washington at 137 is insurance on his own first-round back, on a
  team whose starter has a live ankle. That is the strongest version of the bet.
- **If Matt does not own Jeanty**, Washington is a speculative dart on another manager's injury.
  Still legitimate under §4.13 — round 9+ is where a swing is free — but it is one dart among the
  3–4 §6 allows, competing with Croskey-Merritt, Jordan Mason and Jonah Coleman.
- **Both share Jeanty's week-13 bye**, which already holds Taylor, Henry, Hall, Bowers and Warren
  (§4.11b). Worth at most 1.2 points (§4.11) — noted, not decisive.

---

## 3. HOW CLOSE IS CLOSE ENOUGH FOR A POSITIVE SIGNAL — Matt asked for a number

He asked whether there is a VOR cushion above which the positive marks should be ignored. **There
is, and it falls out of sizes already measured.** All figures are points.

| the thing | measured size | where |
|---|---|---|
| the board's own uncertainty from the replacement line alone | **±1.5** | §4.1b |
| a bye collision, worst case on this board | **1.2** | §4.11 |
| one RB composite signal (target share · 13+ games · NFL rounds 1–3) | **+12.2 per signal, p=0.0008** | doc 191 |
| receiver snap share | **+0.79 per point of share, p<0.0001** | doc 197 |
| the `12g` availability warning | **−19.4, p=0.00004** | §4.22 / doc 203 |

**THE ASYMMETRY IS THE ANSWER, AND IT IS THE OPPOSITE OF WHAT HE EXPECTED.** The strongest thing
this project measures is a **negative** — availability at −19 — and it is bigger than any positive.
**So the AVOID marks override more ground than the positive marks promote.** He was already braced
for the avoid tags; those are the ones that deserve it.

**The working thresholds:**
- **Under ~2 points apart — a coin flip.** The board genuinely cannot separate them. Take the
  positive mark every time, and at pick 32 read the mark, not the number (§7: the five-name policy
  spread is $2.7).
- **2 to 8 points — the signal is live and roughly its own size.** Prefer the green 3/3 back or the
  high-snap-share receiver.
- **8 to 12 points — only the RB 3/3 green mark is big enough to reach**, and only if the trailing
  player carries no `12g` warning. A single signal is worth about twelve points and that is the
  ceiling on what it can pay for.
- **Over 12 points — take the higher VOR.** No positive indicator in this project measures that
  large.
- **A `12g` warning is worth about 19 points against a player, so it can flip a gap up to that
  size** — but §4.25b/doc 204 qualifies it: near-noise on an established veteran (McLaurin, Godwin,
  Kelce, Kittle), a real warning on a young one (Reed, Odunze).

**Two cautions.** The composite carries R² ≈ 0.05, so the point estimate is well measured and the
scatter around it is enormous — treat twelve as a ceiling, not an entitlement. And §0.5(a3):
**signals substitute, they do not compound.** 3/3 is not three times one signal; the count is a
reliability instrument.

**AND HIS LATE-ROUND POINT IS CORRECT AND ALREADY DOCTRINE.** §4.13: from round 9, break near-ties
toward the wider bet; before round 9, never. §4.13b is the reason — in ADP 121–180 only **20.5%** of
players deliver a startable season at all, so a two- or three-point VOR gap down there is measuring
almost nothing. **From pick 104 on, the signal beats the margin. Before it, the margin wins.**

---

## 4. THE MOCK SEQUENCE — his step 1 is wrong

He proposed `py live_draft.py --bridge` as the listener. **That is the board, not the listener.**

```
window 1:   py bridge_server.py
Chrome:     open the practice draft room, extension loaded
window 2:   py live_draft.py --bridge --mock --url "<room URL in quotes>"
```

`--url` is needed because ESPN mints a new leagueId for every practice room (doc 210).
**CLOSE BOTH WINDOWS WHEN THE MOCK ENDS.** Doc 210: four practice rooms fed one `bridge_picks.json`
and `bridge_server.py` dedupes first-write-wins, so a listener left running merges this evening's
real picks into the practice file.

---

## 5. OPEN THREADS

- **`n=6` may be cutting other pages the same way.** Only `streamers()` was audited. Any other
  `head(n)` that precedes a re-sort has this shape. Post-draft.
- Pick 56's single-state margin (`ERROR_PATTERNS` A19) — still the last unfixed instance.
- The pick-8 margin disagreement, 7.8 against 19.96 — still open.
- `Yahoo_Top_300_as_of_817.csv` still missing from `Source\` and `04_source_data\`.
- Doc-number collisions: two 150s, two 94s, two 193s.
- Age × situation change (his Randy Moss case) — post-draft, needs the 2023 and 2025 pulls.

*Sources: [Review-Journal, Aug 11 2026](https://www.reviewjournal.com/sports/raiders/raiders-rookie-rb-mike-washington-jr-brings-power-speed-tenacity-3862274/) · [Yahoo Sports, Aug 31 2026](https://sports.yahoo.com/articles/raiders-rookie-rb-mike-washington-210716798.html) · [Bleacher Report, Sep 2 2026](https://bleacherreport.com/articles/25495665-ashton-jeantys-injury-status-revealed-raiders-hc-ahead-week-1-vs-dolphins) · [Raider Ramble, Sep 7 2026](https://raiderramble.com/2026/09/06/mike-washington-jr-is-forcing-the-raiders-to-rethink-their-backfield/)*
