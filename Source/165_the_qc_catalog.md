# 165 — The pre-draft QC catalog, and Ladder A run

**2026-09-04.** Six ladders, thirty checks, highest level first. Batch = one ladder. This doc is
the checklist; each wave appends its result here. **Ladder A is run below. A6 is the one item in
it that needs a live web sweep and is held for wave 2.**

Legend: **PASS** · **FIX** (defect found and repaired) · **OPEN** (found, not repaired) ·
**HELD** (not yet run) · **SKIP** (a directive says do not re-derive).

---

## THE CATALOG

### LADDER A — DATA. *Does the board describe reality?*
| # | check | state |
|---|---|---|
| A1 | keeper set: predicted vs ESPN's live `keeperPlayerIds`; eligibility, one-per-team | **FIX** (doc 164) |
| A2 | ADP vintage: every consumer of a projections pull agrees on which one | **PASS** after doc 164 |
| A3 | board reconciles to §2 scoring | **SKIP** — §4.23(c) says do not re-audit |
| A4 | `games_2025.csv` covers every board row; badge bands correct | **OPEN** |
| A5 | `player_context.csv` currency: how old is the news, how much is unclassified | **OPEN** |
| A6 | live news sweep Sept 3 → Sept 7 against the drafted range | **PASS with 4 updates** (wave 2) |

### LADDER B — THE BOARD OBJECT. *Is the artifact internally consistent?*
| # | check | state |
|---|---|---|
| B1 | `board_v8_fixed` ∪ `board_v7_kdst_separate` ∪ prerank: one universe, no overlap, no dupes | **PASS** |
| B2 | `espn_id` integrity: nulls, duplicates, trailing-space names (doc 58's class) | **PASS** |
| B3 | replacement levels and `vbd` recomputed from the spine, independently of `board_audit` | **PASS** |
| B4 | §2.1(c) table vs the board's own `gone_ahead` column, on the current freeze | **PASS** |
| B5 | every badge traces to a live column AND is explained in the key | **OPEN — 1 finding** |

### LADDER C — THE ENGINE. *Does it decide correctly?*
| # | check | state |
|---|---|---|
| C1 | `CAPS = {'QB':2,'TE':2}` holds across N engine-driven drafts | **PASS** |
| C2 | fixed shape — 12 player rows, 3 tier rows, every state | **PASS** (doc 163, at 14 gone-rows) |
| C3 | seed sweep at every one of Matt's picks **on the current board** — margins and stability | **PASS + 1 correction** |
| C4 | rollout vs constrained-VBD fallback still ordered the same way | **PASS** |
| C5 | `_lineup` pure-Python vs numpy bit-identity (`bench_lineup.py`) | **PASS** |
| C6 | roster-panel / starter-strip arithmetic against a hand-checked roster | **PASS** |
| C7 | **NEW** — does any SHIPPED harness use a naive ADP filler that §5 forbids? | **YES — measured, NULL** |

### LADDER D — THE NIGHT PATH. *Will it actually run?*
| # | check | state |
|---|---|---|
| D1 | `check_kit.py` file tree, after today's eight writes | **PASS — 55/55, verified myself** |
| D2 | `draft_night.bat` traced step by step: what each step writes, what is reversible | **PASS + 1 note** |
| D3 | `keeper_swap → board_audit → injector → verify_prerank` chain, executed where possible | **FIX** (doc 164, first two links) |
| D4 | bridge: 6-hour staleness guard, BACKWARDS guard, atomic write, extension freshness | **PASS — all four** |
| D5 | failure modes: ESPN 401 at 7pm · bridge dies mid-draft · clock expires · power cut | **PASS** |
| D6 | **which scripts leave a durable record and which vanish into a console window** | **FIX — one edit covered all five** |

### LADDER E — THE PAPER. *Does the desk match the screen?*
| # | check | state |
|---|---|---|
| E1 | Desktop links → dated files → source pages, all current and all pointing forward | **PASS — all 7** |
| E2 | HOW_TO_READ_IT generated from the board's own legend and stylesheet | **FIX** (doc 163) |
| E3 | DRAFT_BOARD / FALLBACK / VALUE_LADDER / OVERRIDE current after the Sept-5 refresh | **FIX — the guard was GONE** |
| E4 | DRAFT_CARD and DRAFT_DAY_GUIDE — excluded from `to_pdf`; is their content still true? | **FIX — the card was inverted** |

### LADDER F — THE DIRECTIVE AND THE RECORD.
| # | check | state |
|---|---|---|
| F1 | `audit_directive.py` re-run against the shipping files | **PASS 51/51, after fixing the audit** |
| F2 | numbers this session changed: §2.1(c) provisional, §4.9's K-keeper exclusion | **OPEN — for the directive** |
| F3 | doc-number collisions in `Source\` | **OPEN — 2 found** |
| F4 | `ERROR_PATTERNS.md` — do this session's defects belong to existing patterns or new ones? | **FIX — new pattern C3** |

---

## LADDER A — RESULT

### A1 · keeper set — **FIX, and the model's miss was worse than doc 164 said**
Seven of twelve have selected. Six match the prediction. The seventh does not, and the eligibility
file explains why in one line. Window is Always Open's **entire** eligible pool:

| player | pos | 2025 rd | proj | VBD |
|---|---|---|---|---|
| Quentin Johnston | WR | 10 | 138.4 | **−30.1** |
| **Brandon Aubrey** | **K** | 13 | **171.6** | *(no K replacement level → blank)* |
| Stefon Diggs | — | 6 | **no projection** | — |
| Joe Mixon | — | 5 | **no projection** | — |

**Every skill option is below replacement or unprojected.** §4.9's "exclude K and D/ST from keeper
prediction entirely" therefore forced the pick onto **a player with no projection at all**, ADP 165.
Doc 164 called the model "blind by instruction"; that was too kind. **§4.9 is a rule about draft
value that was applied to a keeper decision, where the cost is fixed at round 15 and the only
question is who is worth more.** Matt said as much in chat and the correction never reached
`predicted_keepers_v5.csv`.

All twelve (7 actual + 5 predicted) verified against `keeper_eligibility_VERIFIED.csv`: all
present, all drafted round 5+, exactly one per team. **A1 otherwise passes.**

**The five still open, with their own best alternative:**

| team | predicted | VBD | next best | verdict |
|---|---|---|---|---|
| NickCannonFanClub (Fleming) | Javonte Williams | **+72.1** | Kyle Pitts +7.1 | safest call in the league |
| We Got This Sh!t (allen) | Drake Maye | +30.8 | DJ Moore +7.7 | safe |
| Bloodied Castaways (Kam) | Zay Flowers | +29.6 | Deebo −24.4 | safe |
| Kunning Stunts (Rychlicki) | Colston Loveland | +28.2 | Bo Nix +5.9 | safe |
| **Sentinel Sea Stallions (Ray)** | Rhamondre Stevenson | **+3.6** | **Aaron Jones −2.8** | **6.4 points apart, both near replacement — a coin flip** |

### A2 · ADP vintage — **PASS, after doc 164**
`depth_map.py` and `board_audit.py` already read `adp_vintage.txt` with an 08-23 fallback.
`keeper_swap.py` was the only consumer still hardcoding 08-23; doc 164 brought it into line, and
the split it uses (market from the stamp, projections from 08-23) is the same split `board_audit`
already used. No other script reads a fixed pull for the market.

### A4 · `games_2025.csv` coverage — **OPEN, and the live half is the keepers**
- 479 rows, no duplicate ids. **One board row has no `g25`: Josh Williams (RB, TB), rank 434,
  adp 169.95** — deep inside §4.14's sentinel, harmless. `make_board.py` left-merges and reads a
  missing value as 0, so he simply gets no badge; **`mark_rookies.py` asserts and would refuse to
  run.** It is not in `sept5_after.bat`, so nothing on the Sept-5 path breaks.
- **The real gap: the file was built FROM the board, so it contains none of the twelve keepers.**
  Every one of them is absent. So **any player who returns to the board at the 7:00 PM lock
  arrives with no availability badge, silently.** Today that is Diggs (below replacement, so it
  costs nothing). But five teams have not chosen: if Fleming keeps Kyle Pitts, **Javonte Williams
  returns at roughly RB-top-40 with the `12g` badge that §4.22(c) exists to show simply absent.**
- Drafted range today: 36 `12g` badges, 11 rookies. Worst band inside 161: **Nabers 4g (adp 35),
  Kyler Murray 5g (137), Jayden Reed 5g (140)**.

### A5 · `player_context.csv` currency — **OPEN**
265 rows. Grades NEUTRAL 103 · DISCOUNT 32 · AVOID 9. **22 rows carry a dated news line and every
one of them is stamped 09-03** — nothing since. **76 rows still say "no injury news found."** By
Monday the newest fact on any player card is four days old, over the weekend that decides
week-1 statuses. That is what A6 is for.

### A6 · live news sweep — **HELD for wave 2.**


---

## WAVE 2 — LADDER B, plus A6

### B1 · one universe — **PASS, exactly**
`board_v8_fixed` **480** + `board_v7_kdst_separate` **64** = **544** = the prerank, to the row.
Overlap between board and streamer sheet: **0**. Board players absent from the prerank: **0**.
Streamers absent: **0**. Prerank ids on neither sheet: **0**. Negative D/ST ids: **32**, as designed.
That 544 is also the number ESPN read back in doc 155 — two independent routes to the same total.

### B2 · identity — **PASS**
No null ids, no duplicate ids, on any of the three files. **No name carries stray or doubled
whitespace** (doc 58's defect, which made the #1 player undraftable). 54 of 480 names carry a
suffix, period, apostrophe or hyphen — 11%, matching §3's stated 10%. **Zero rows collide under
`norm()`**, so even the name-join fallback would not merge two players today.

### B3 · replacement and VBD — **PASS, and exactly**
Re-derived independently from the 08-23 pull: QB **341.6029** · RB **168.5889** · WR **163.5396** ·
TE **140.2949**, against §4.1's quoted 341.603 / 168.589 / 163.540 / 140.295 — agreeing to
**4 decimal places**, which is doc 101's rounding and nothing else. Recomputing every row's
`vbd = proj − replacement[pos]` reproduces the board's column with **max |difference| 0.000000
across all 480 rows**, and `rank` is strictly the VBD rank.
*(Terminology, per Matt: the quantity in that column is **VOR** — points over the replacement
starter. **VBD** is the method built on it. The column label stays as it is; the map has to be
stable three days out.)*

### B4 · §2.1(c) — **PASS**
Re-solved as a fixed point from the twelve published keeper ADPs: **identical on all fourteen rows**
to v7.1's table. The board's own per-player `gone_ahead` equals `count(keeper ADP < adp_pick)` on
**0 mismatched rows**, and `eff_pick = adp_pick − gone_ahead` holds on every row.

### B5 · badges — **PASS on the key, OPEN on one asymmetry**
Every label the live board actually draws — MINE · AVOID · OUT · IR · DISC · BYE · FADE · Q/D ·
BUY · CALLS · OPEN · DART · ok · R · tie · free · RUN — **is explained in the twelve-entry key.**
(`LEAD BACK`, `YOUR TAKE`, `DISCOUNT` and `NEUTRAL` appear in the source but only inside the
tooltip or as tested values, never as drawn labels. A first pass flagged them and was wrong; the
probe was the defect, not the board — the doc 159 lesson, again.)

**THE FINDING: the `12g` availability badge is on the PAPER board only. The live board has no
games-played mark at all** — `badges()` reads `player_context` and ESPN's injury flag and nothing
else. doc 105 caps the screen at two marks per row **on purpose**, so this may be a deliberate
trade rather than an omission — **but it is not neutral, because of what the tooltip says
instead:**

| player | adp | 2025 games | what the LIVE board tells you |
|---|---|---|---|
| Terry McLaurin | 61.1 | **10** | `no injury news found \| exp 17 gm \| [low confidence]` |
| Rome Odunze | 64.9 | **12** | `no injury news found \| exp 17 gm \| [low confidence]` |
| Marvin Harrison Jr. | 78.8 | **12** | `no injury news found \| exp 17 gm \| [low confidence]` |
| Garrett Wilson | 37.2 | **7** | `no injury news found \| exp 17 gm \| [low confidence]` |
| Drake London | 20.3 | **12** | `no injury news found \| exp 17 gm \| [low confidence]` |
| Jayden Reed | 139.7 | **5** | `no injury news found \| exp 17 gm \| [low confidence]` |

**`exp 17 gm` on a player who played seven.** §4.22(c) measured that a WR who missed time averages
**9.1** games the next season against 12.7, and beats his projection by **−16.2 points** (WR −25.4)
— and those exact three names, McLaurin, Odunze and Harrison Jr., are the "LIVE ROWS THIS CHANGES"
list in §4.22 itself. The screen carries the opposite claim, sourced from the analyst sweep's
expected-games column, at low confidence. 27 of the 36 badged players do have games language
somewhere in the tooltip; these do not.
**Surfaced, not fixed.** doc 105's two-mark cap is a stated design decision and this is a
board-appearance call, so it goes to Matt rather than being silently applied. The cheapest option
that respects the cap is to put the games count into `player_context.why`, which the tooltip
already renders, instead of adding a third badge.

### A6 · live news sweep — **PASS: the board already knew almost all of it**
Swept the week-1 injury reports and the camp tracker against the drafted range. Eighteen names
checked. **The board already carries every one**, mostly stamped 08-31 from the injury sweep with
four upgraded to 09-03. Nothing found is missing from the board, and the board's *direction* is
right on all four names below — each already carries DISCOUNT or AVOID. What is newer is the
**degree**:

| player | adp | board says (dated) | newer, 09-03 |
|---|---|---|---|
| **Jeremiyah Love** | **26.1** | DISCOUNT · left high ankle sprain (08-31) | **head coach: "50-50" for Week 1** — four outlets |
| Emeka Egbuka | 44.9 | DISCOUNT · turf toe (08-18) | sidelined Tuesday, "becoming concerning" |
| TreVeyon Henderson | 77.8 | DISCOUNT · ankle/foot (08-31) | **has not practiced since Aug 24** |
| George Kittle | 73.7 | **AVOID** · Achilles (08-31) | trending the *other* way — made the Australia trip, Schefter reports no setbacks; **but one outlet still has him likely out. CONFLICTING — do not resolve it, carry both.** |

**Nothing applied.** Every source found is itself dated 09-03, so a refresh today would buy one
day; the weekend practice reports are what change week-1 statuses, and §8 already schedules the
news search for the Sept-5 pass. Applying half a refresh now would make the cards look current
when they are not.

**Live consequence worth carrying to Monday:** Love is adp 26.1 and was the engine's #1 at pick 32
in the state rendered on 09-04. He already carries DISCOUNT, so the board is cautioning — but
"50-50 for Week 1" from the head coach is a harder fact than the badge implies, and pick 32 is
§7's genuine tie.


---

## WAVE 3 — LADDER C, THE ENGINE

### THE FIRST RUN WAS WRONG, AND THE HARNESS WAS THE DEFECT

The sweep's first pass reported **pick 8: McCaffrey 9/20, Nacua 7/20, five distinct winners** —
a flat contradiction of §4.2, which the directive calls CLOSED. Before writing that down I asked
why (§0.2: a diagnosis is a claim). It was not the engine and it was not the 09-03 ADP refresh —
McCaffrey moved **+0.53 picks**, St. Brown **+0.07**.

**It was my filler.** I generated opponent states by sorting on `eff_pick + noise` and taking the
first N — the same shape `shoot.py` uses. **§5 forbids exactly that:** *"Simulated opponents must
draft from a cheat sheet, not blindly down ADP: take the best VBD among the ~22 nearest the top of
their noisy board."* Under straight ADP, **McCaffrey — the 3rd-best VBD on the board — survives to
pick 8 in 12 of 20 states**, because his ADP is 7.72. No opponent drafting off value leaves him
there. Rerun with the §5 rule, same 20 seeds:

| opponent model | St. Brown available | winner at pick 8 |
|---|---|---|
| straight noisy ADP (`shoot.py`'s shape) | 14/20 | **McCaffrey 9 · Nacua 7 · Taylor 2 · Chase 1** |
| **§5 cheat sheet, window 22** | 20/20 | **Amon-Ra St. Brown 20/20** |

**§4.2 is confirmed, not contradicted. Pick 8 stays closed.** And this is §4.15's lesson in a new
place: *dispersion alone is not an opponent model.* Everything below is the §5-compliant rerun.

### C3 · seed sweep, 20 §5 states, production `Engine`, `rollout_inner=60`

| pick | modal #1 | share | distinct | median margin | IQR | states under 1.0 |
|---|---|---|---|---|---|---|
| 8 | **Amon-Ra St. Brown** | **20/20** | 1 | 8.90 | — | 0 |
| 17 | **Jeremiyah Love** | **20/20** | 1 | **0.60** | — | **17** |
| 32 | **Lamar Jackson** | 18/20 | 3 | **3.60** | — | 0 |
| 41 | Bhayshul Tuten | 17/20 | 3 | 5.20 | 0.3–5.2 | 7 |
| 56 | Rico Dowdle | 14/20 | 6 | **0.40** | 0.3–0.4 | **18** |
| 65 | DK Metcalf | 6/20 | 8 | 0.60 | 0.3–1.0 | 14 |
| 80 | Bo Nix | 4/20 | 13 | 0.20 | 0.2–0.4 | 18 |
| 89 | Mark Andrews | 4/20 | 11 | 0.35 | 0.1–0.9 | 15 |
| 104 | Kyle Monangai | 5/20 | 11 | 0.10 | 0.0–0.3 | 20 |
| 113 | Jacory Croskey-Merritt | 3/20 | 13 | 0.00 | — | 20 |
| 128 | Kenyon Sadiq | 6/20 | 8 | 0.00 | — | 20 |
| 137 | Khalil Shakir | 5/20 | 8 | 0.00 | — | 20 |

**HONEST LIMIT OF THIS SWEEP, stated up front:** at picks 8 and 17 the margin is *identical across
all twenty seeds*, which means my §5 filler produces **one state**, not twenty — with a 22-wide
window and only 7 or 16 picks to make, it simply takes the top of the VBD list every time. **So
picks 8 and 17 here are doc 139's seed-stability test, not doc 140's state-variety test.** They do
not add to §4.2 beyond replicating it on the current board. Variety appears from pick 32 on, and
that is where this sweep carries new information.

**Two results worth having:**

1. **Pick 32 lands on Lamar Jackson 18/20 at a median margin of 3.60.** §7's tie list is
   *Bowers · McBride · Kyren Williams · Judkins · Lamar*, and doc 140's median across 100 states
   was **3.65**. A different generator, twenty states instead of a hundred, and the margin agrees
   to **0.05**. §7's instruction — take the engine's #1 at 32, do not override it — is reinforced.
2. **PICK 56'S NUMBER WAS WRONG AND IS NOW CORRECTED.** v6.7 flagged doc 139's *"10/10 at margin
   2.77"* as SINGLE-STATE and never re-checked. Re-checked: **six distinct winners, median margin
   0.40, and 18 of 20 states under 1.0.** Pick 56 is a coin flip, not a clear call — the same
   correction v6.7 made to pick 32's 0.15, running the other way. **Do not carry 2.77.**

From pick 65 on the median margin is under a point and the winner is unstable by construction —
which is what §4.13's "risk from round 9" and §7's "cost spread collapses" already describe.

### C1 · CAPS — **PASS, 20 of 20**
No violation of any cap in any draft. **QB is exactly 2 and TE is exactly 2 in all twenty**, which
is Matt's §6 doctrine holding and the §4.18 draft-night rule resolving toward QB2 every time.
Roster shapes: 8× (5RB 3WR), 7× (4RB 4WR), 5× (6RB 2WR) — RB-heavy, matching §4.10's
"RB-RB-RB in 64–65%".

### C4 · rollout vs constrained VBD — **PASS: they are genuinely different rules**
Identical on **136 of 240** picks (57%). The divergences cluster at picks **17, 41, 56, 65** —
almost every one of them the rollout **passing on Matthew Stafford (QB, VBD 21.2)** to take an
RB or TE with lower VBD. That is lookahead doing its job: the QB tier is flat (§4.15's 11.8-point
plateau) so Stafford keeps, while the RB does not. If these two rules agreed 95% of the time the
rollout would not be worth the compute; at 57% it is clearly doing something, and what it does is
what §4.10 measured it doing.
*(This is the divergence rate, NOT §4.10's paired race — that needs the `code_ruletest_*` harness
and was not re-run.)*

### C5 · `_lineup` equivalence — **PASS, exactly**
`py bench_lineup.py`: **18,728 production calls, 0 mismatches, EXACT AGREEMENT**, and the on-clock
render is 6.7–9.9× faster with `same order: True` at every pick.

### C6 · starter strip — **PASS, six hand-checked cases through production `step()`**
Empty roster · 1QB/3RB/2WR/1TE · QB at the cap · 6 RB at the league cap · a second TE filling FLEX ·
and the FORCED branch with two turns left and two starters missing. All six render exactly the
expected strip, including the `+n` extras and the `full` markers.


---

## WAVE 4 — LADDER D, THE NIGHT PATH (plus C7)

### D1 · the file tree — **PASS, 55 of 55, checked from my side**
Staged every file `check_kit.py` pins — 42 in `Scripts\`, 9 in `Scripts\live_draft\`, the
5-file `espn_bridge\` extension — off Matt's machine and hashed them against the MANIFEST after
this session's nine writes: **55 entries, 55 OK, 0 mismatches, 0 unchecked.** The extension files
are among them, so doc 139's "a stale `hook.js` fails SILENTLY" case is covered.

### D2 · `draft_night.bat` traced — **PASS, and only ONE step is not reversible**

| step | what it does | writes | reversible |
|---|---|---|---|
| 1 | `check_kit.py` | — | read-only |
| 2 | `fetch_keepers.py --dry` → `--write` | `actual_keepers.csv` | yes, archived |
| 2b | `notepad actual_keepers.csv` (hand fallback) | that file | yes |
| 3 | `keeper_swap.py --check` → `--write` (**defaults Y**) | `board_v8_fixed.csv`, prerank, **and now `board_v7_kdst_separate.csv`** | yes, all archived first |
| 4 | `board_audit.py` | — | read-only **GATE** |
| 5 | `espn_draft_injector_Gemini.py` | **ESPN's stored prerank** | **the only outward write** — doc 155 measured the POST as REPLACE, so re-running is safe |
| 6 | `verify_prerank.py` | — | read-only |
| 7a–c | `bridge_server.py` → extension → `live_draft.py --bridge` | `bridge_picks.json`, `bridge_raw.jsonl`, `live_board.html`, `feed_evidence\` | yes |

**The note:** step 3 now rewrites the streamer sheet too (doc 164), so **two** hashes go stale
after the swap, not one. `check_kit.py`'s comment said "the BOARD hash" singular; corrected, so a
post-7pm run of `01 - Check everything` does not read as a new failure.

### D4 · bridge guards — **PASS, all four, executed**
- **6-hour staleness** — doc 163: refuses the 41-hour-old file, accepts it re-stamped.
- **LOST PICKS** — and my first test was wrong, not the guard. I called `_bridge_picks()`; the
  check lives one level up in `fetch_picks()`. **Third time this session my test was the defect**
  (the B5 badge probe, the wave-3 filler, this). Redone against the production path:

| feed goes | board sees | |
|---|---|---|
| 120 → 150 | 150 | grows normally |
| 150 → **90** | **150 held**, warning printed | correct |
| 100 → **100 with 20 different players** | **100 held**, warning printed | **doc 148 finding 1** — the subtle one that once handed Gibbs and Bijan back as available at pick 120 |

- **Atomic write** — `bridge_server.py` writes a sibling `.tmp` and `os.replace()`s it.
- **Extension freshness** — all 5 files hash-verified in D1.

### D5 · failure modes — **PASS**
- **ESPN 401 at 7pm:** `weekend_check.py` gates on `cookie_jar.py --check` and *skips* the two
  ESPN steps rather than failing them four separate ways; `04 - Fix ESPN sign-in` is the fix.
- **Bridge dies or is restarted mid-draft:** the LOST PICKS guard holds the last complete set.
- **Nothing read yet / extension not loaded:** this is doc 148's "most likely startup failure
  there is." The board does **not** render a plausible pick-1 page — it renders a waiting page
  that says *"No picks have been read yet. Nothing on this page is a recommendation,"* and doc 149
  finding 7 extended the same latch to mid-draft.
- **Clock expires:** ESPN autodrafts from the injected prerank, which doc 155 measured as holding
  **zero K or D/ST inside the top 250** — so it takes a skill player off Matt's own VBD order.

### D6 · logging — **one edit covered all five**
Inventory of what each script leaves behind: **only `live_draft.py` writes a log at all**
(`feed_evidence\*.json`). `check_kit`, `board_audit`, `verify_prerank`, `sept5_check`,
`sync_desk_copies`, `make_shortcuts` and `rehearsal` produce a **verdict and nothing on disk** —
which is precisely why Matt has had to copy and paste every result today.
**The fix is one line, because `weekend_check.py` already runs five of them** — board_audit,
check_kit, cookie_jar, verify_prerank and fetch_keepers. `weekend_check.bat` now tees to
`Scripts\weekend_check_log.txt`, so one double-click of `01 - Check everything` leaves a record of
all five. **Deliberately NOT applied to `draft_night.bat` or `sept5_after.bat`** — both stop and
ask questions Matt has to read and answer, and a redirect would hide the prompt.

### C7 · the engine's OWN survival model — **the exposure is measured, and it is nearly nil**
`code_live_engine.py` computes "who will be gone before my next turn" in **three** places as
`adp_opp + N(0, 0.111·adp_opp + 5.40)`, `argsort`, take the first `gap−1` — the exact shape §5
forbids for simulated opponents and §4.15 calls "not a survival model". doc 142 §4a had already
noted it for QBs. After wave 3, where that same shape wrecked my own state generator, the obvious
worry was that it wrecks the engine too.

**Measured, not reasoned.** Built a sandbox copy of the production engine with all three `gone`
computations replaced by the §5 cheat sheet, ran **both engines on identical board states**,
12 states × 12 picks:

**Same recommendation on 142 of 144 picks (99%).** The only two differences are both at **pick
104**, between players at **−11.9 vs −17.6** and **−5.3 vs −17.9** VBD — below replacement, inside
§4.13's "risk from round 9" band where §7 already says the cost spread has collapsed. **Picks 8
through 89 and 113 through 137 are identical in every state.**

**So: flag it, change nothing.** The survival model only feeds the *lookahead* term, and at the top
of the board the "adds now" term dominates it. This also bounds doc 142 §4a's QB soft spot from a
second direction. **Caveat, stated plainly: 12 states, and the cheat sheet is another model, not
ground truth. The finding is "swapping one plausible opponent model for another moves 2 of 144
picks", NOT "the survival model is right."** Post-draft work, per §4.18c's rule about not
re-aiming the objective days before the draft.


---

## WAVE 5 — LADDERS E AND F. THE CATALOG IS CLOSED.

### E4 · THE CARD TOLD HIM THE OPPOSITE OF THE CURRENT RULE — **FIXED**
`DRAFT_CARD.pdf` was last built **Aug 31** and doc 146 deliberately excluded it from `to_pdf.py`
(rebuilding would have rotated it to landscape), so it has been frozen while the directive went
v6.5 → v7.1. What it says at picks 104 and 113, verbatim:

> *"Second QB is the one live call. Worth +5 to +11 this season; **the RB you'd skip is worth
> about +8 as next year's keeper. Near enough a wash — so take the better player. QB only if it's
> Goff-or-better and no real RB is sitting there.**"*

That is the **struck-through v5.7 rule**. §4.18's current rule inverts it: *"At 104 or 113, if a
QB of Goff's tier or better is on the board, TAKE THE QB2."* The +8 keeper option the card is
still pricing was **measured at ≈ +0.7** (doc 138). **The card and the directive give opposite
instructions at the same two picks**, and the card is what he reads at the table.

**Fixed:** that paragraph rewritten to the current rule, flagged as a flip so the change is
visible, and — per §6 — **surfacing the conflict with his own doctrine rather than resolving it
for him.** One second stale line went with it: *"Under 1.5, it's a toss-up and your gut is free"*
predates §7 v6.7's "take the engine's #1 at 32, do not override it"; it now says take row 1 and
that a read breaks ties only *among* rows already at the top.
**Rebuilt with wkhtmltopdf, no landscape flag — still PORTRAIT, still 2 pages**, layout verified
by rendering it. Old card and page archived; `08 - Draft card.url` re-pointed to the 09-04 copy.
doc 146's worry was a silent rotation; this is neither silent nor rotated.

### E3 · THE GUARD DOC 146 BUILT WAS GONE, AND I AM THE ONE WHO DELETED IT — **RESTORED**
v6.9 says *"`sync_desk_copies.py` now **refuses** any PDF older than the page it came from."*
**It does not. There is no mtime comparison in the file at all.** On Sept 3 I edited a stale
mirror of it and committed that over the newer one — 6,767 bytes became 5,674 — and doc 162
recorded the byte drop as *"unresolved: could not determine what was lost."* **This is what was
lost.** Found by grepping for a guard the directive claims exists, which is the check doc 162
should have run.

Restored, with negative controls run first: a **day-old** PDF is REFUSED and names the fix
(`py to_pdf.py`); a PDF **429 ms** older than its page — which is what `VALUE_LADDER` looks like
right now, from same-run write ordering — passes. `STALE_SECS = 60` is the difference, and the
reason is written next to it: a zero-tolerance guard would refuse the ladder on every run and be
switched off inside a day. `DRAFT_CARD` and `DRAFT_DAY_GUIDE` have no `Source\*.html` page and
are skipped rather than refused. Re-pinned.

### E1 · the desk — **PASS, all seven**
Every `.url` resolves to a file that exists at the 2026 root: board, ladder, card (now 09-04),
override, guide, how-to (09-04), and the undated COMMANDS.html. doc 161's "a link that silently
opens an older document than the one beside it" does not recur.

### F1 · `audit_directive.py` — **51 ok, 0 FAIL, after fixing the audit itself**
It first reported **50 ok, 1 FAIL** — and both problems were the auditor's:
- **It was hardcoded to my container** (`KIT='/home/claude/work/final'`, `SRC='/mnt/user-data/...'`).
  §0.4 v6.8's exact failure, in a script the directive tells Matt to run. Now resolved against its
  own location, and **verified by running it from a relocated tree.**
- **The one FAIL counted directory entries, not kit members** — it saw 14 files in
  `Scripts\live_draft\` against the directive's 9, but 5 of those are runtime output
  (`bridge_picks.json`, `bridge_raw.jsonl`, `adp_vintage.txt`, `DRAFT_ROOM_RECON.txt`,
  `replay_log.txt`). Now counts the nine pinned members and names any that are missing.

With that, **every load-bearing number in the directive reconciles to the shipping files**,
including all 28 rows of §2.1(c) and §4.14's 327/153 sentinel counts.

### F3 · doc numbers — **two collisions, both real**
- **doc 150 is claimed by TWO DIFFERENT DOCUMENTS** — `150_pick17_in_dollars.md` and
  `150_the_board_does_have_a_builder.md`, written 2h49m apart on the same evening. This is doc
  139's "two agents wrote a doc 138 the same night" repeating, and §0.2's folder-listing rule not
  being followed.
- **doc 94 is claimed twice**, `94_picks_17_and_32.md` and `94_picks_17_and_32_2322.md`, same size
  — a duplicate save.
**Not renamed.** I can write files to Matt's Drive but cannot delete, so renaming would leave a
third copy and make it worse. Post-draft cleanup, with `tidy_docs.py`. **And `doc 150_pick17` is
not referenced anywhere in the directive — §7 has entries for picks 8, 32 and 56 and none for 17**,
which is the more useful half of this finding.

### F4 · `ERROR_PATTERNS.md` — **new pattern C3**
Three times in this session my *test* was the defect, not the thing tested — and all three
produced a **false alarm**, not a false pass. doc 80's existing rule covers the false-pass
direction only. Added **C3 · The probe was wrong, not the object — and it raised a FALSE ALARM**,
with all three instances and the rule that matters: *when a check contradicts a finding the
project has already CLOSED, the prior is that the check is wrong.*

### F2 · what the DIRECTIVE still needs — **OPEN, and it is the only thing left**
Two edits, neither safe to make until the keepers are final:
1. **§2.1(c)** — provisional re-solve in doc 164: a kicker keeper does not deplete the skill pool,
   so picks 104–161 each lose one keeper ahead. **Five teams have not chosen; re-solve at the lock.**
2. **§4.9** — *"Exclude K and D/ST from keeper prediction entirely"* is a rule about DRAFT value
   that was applied to a KEEPER decision, where cost is fixed at round 15. It pushed the prediction
   onto a player with no projection at all. Needs a carve-out: exclude them from ADP-based keeper
   prediction, **not** from the question of who a team is better off keeping.

---

## THE CATALOG, CLOSED

**30 checks + C7. Every one is now PASS, FIX, SKIP or a named OPEN — nothing is HELD.**

| ladder | pass | fixed | open | skip |
|---|---|---|---|---|
| A — data | 2 | 1 | 2 | 1 |
| B — the board object | 4 | 0 | 1 | 0 |
| C — the engine | 6 | 0 | 0 | 0 |
| D — the night path | 5 | 1 | 0 | 0 |
| E — the paper | 2 | 2 | 0 | 0 |
| F — the record | 1 | 1 | 2 | 0 |

**The four OPEN items, all deliberate:** A4 (`games_2025.csv` holds no keepers, so anyone who
returns at the lock arrives with no availability badge), A5 (every card is stamped 09-03 — the
Sept-5 news pass is scheduled), B5 (the live board has no games-played mark and the tooltip says
`exp 17 gm` for players who played 7 — a doc 105 two-badge-cap decision that is Matt's), and F2
above. **Nothing OPEN is a code defect; all four are decisions or scheduled work.**
