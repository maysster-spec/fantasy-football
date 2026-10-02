# 223 — The weekly waiver process, and the pool priced on our own board

**2026-09-08 (draft +1).** Matt: *"we need to design a weekly waivers process"* · *"anyone on the
waiver who may be of consideration now?"* · *"we need to apply those projections"* · *"does Nacua
have a decent backup? was that player already scooped up if so"*

**Shipped:** `Source\THE_WEEKLY_WIRE.html` (the routine, the drop ladder, the pool) ·
`Scripts\wire.py` (new) · `Scripts\set_cookies.py` (patched).

---

## 1. THE COLLISION CHECK PAID FOR ITSELF — §0.2's folder-listing rule

**I was about to write `waivers.py`. It already exists** (3,065 bytes, Aug 2026) and pulls
HISTORICAL transactions into `waiver_report_<year>.csv` — the file every waiver finding in this
project is built on. Different job, same obvious name. **The new one is `wire.py`.** One name, one
job, and `00_HOW_TO_RUN_IT.md` gets both.

**And the second half of the same rule:** `set_cookies.py` exists because four scripts each carried
a copy of the cookies and one of them silently drifted (doc 86). `wire.py` is a fifth. **It was
added to `set_cookies.py`'s `FILES` list in the same commit, and the guard was RUN, not assumed** —
both regexes match `wire.py` exactly once each, and the rewritten file still parses. §0.2: a guard
that has never been executed is not a guard.

## 2. WHAT `wire.py` DOES, AND WHAT IT IS NOT

ESPN's free-agent page sorts by **percent owned** — the market's opinion. `wire.py` pulls the real
pool (`kona_player_info`, `filterStatus ∈ {FREEAGENT, WAIVERS}`, limit 400), joins it to
`board_v8_fixed.csv` and `player_context.csv` **on `espn_id`** (§3's identity rule), and re-sorts on
our own value with the job flag, the job's worth, the back signals and the news grade attached.
Writes `Source\WIRE_<date>.csv`.

**Tested to the seam and no further.** The local half was run against the objects production builds:
480 board rows priced, 265 context rows, flags correct on five spot-checked names. **The ESPN half
is untested and only Matt can test it** (§0.4 item 1) — `py wire.py --check` proves the cookies
before anything else runs. Two failure modes are explicit rather than silent: a 401 says "run
`set_cookies.py`", and **an empty pool exits with an error rather than printing an empty sheet** —
§0.2, an exit code is not a result.

**And it names what it could not price.** Our board is 480 rows; ESPN's universe is larger, so a
genuinely deep name has no value on it. The sheet prints those by name rather than dropping them —
§0.5(c)5, the missing-row check, on the one artifact where the missing row is the whole point.

## 3. THE PROCESS, AND WHERE EACH RULE COMES FROM

| the rule on the page | what it rests on |
|---|---|
| Tuesday pull, Tuesday-night claims | Waiver Period 2 Days, `2026_League_Settings.txt` line 125 |
| Priority costs nothing, never hoard it | line 126, *Waiver Order: Reset Each Week to Inverse Order of Standings* — not FAAB |
| Always claim, never wait for free agency | doc 205 §1: claim +1.18 ppg over the man dropped (p=0.0016, n=443); free-agent add +0.52 (p=0.29) |
| No rush in September | doc 205 §0.2: wk 1–3 22.1% vs wk 10–14 23.1%, p=0.83 |
| Chase QB and TE, be strict on WR | §4.19: his own adds hit QB 35.7% (n=14), RB 20.5% (n=39), **WR 12.5% (n=24)** vs league 20.1% |
| The wire cannot fix an RB hole | §4.19: four of five RBs he adds never give a startable stretch |
| Buy the job, not the name | §4.20 / doc 141: incumbent − challenger +8.2, p=0.604 — null, and the point estimate leans the other way |

**The drop ladder is the piece doc 205 §3 said the scheme needed and could not have before the
roster existed.** A waiver pickup can never be kept (§2.1a), and rounds 1–4 were never keepable
either — so the entire 2027 cost of a drop sits on the eight players drafted at 56 through 161:

- **free to drop:** Browns D/ST (152), Pineiro (161) — K and D/ST become keepers 0% of the time
- **near-free:** Shough (137), Washington Jr (128), Worthy (113), Spears (104) — rounds 9–12 become
  keepers 8.3% of the time and §4.18b measured what those keeps return at ≈ 0
- **costly:** Dobbins (89), Dowdle (80), LaPorta (65), Hurts (56) — rounds 5–8, **15.1%**, the
  audition window §6 narrowed to exactly this seam

## 4. NACUA'S BACKUP — HE ALREADY OWNS IT, AND IT WAS NEVER ON THE WIRE

Every Rams skill player, checked against the 180 rostered names:

| player | value | who has him |
|---|---|---|
| Puka Nacua | +131.3 | **Matt** |
| Kyren Williams | +46.8 | Window is Always Open |
| **Davante Adams** | **+35.0** | **Matt** |
| Matthew Stafford | +21.2 | Window is Always Open |
| Blake Corum | −17.6 | ChatCTE |
| Terrance Ferguson (TE) | −27.5 | free |

**After Adams the room ends.** On the 09-03 pull the next Rams receiver is **Tutu Atwell at 26.0
projected points for the season**, then Whittington 18.0 and Mumpfield 16.1 — none of them rostered
by anyone, and none of them worth a bench spot. **There is no handcuff to scoop because there is
nothing behind Adams to scoop.** If Nacua misses time the targets go to a player Matt already owns,
which is the quiet upside of the pick-41 card that read "genuinely split."

## 5. THE POOL, THE MORNING AFTER — AND THE ANSWER IS "NOT YET"

339 of the 480 board rows are unrostered. **Best available by value, by position:** RB Samaje
Perine −77.5 · TE T.J. Hockenson −20.9 · WR Tank Dell −38.4 (carries AVOID — on IR designated to
return, four games minimum) · QB Daniel Jones −35.5.

**No running back on the wire is inside 77 points of a startable one, which is doc 12's table
stated as a fact about today rather than a rate.** The names worth watching are the ones whose JOB
could open — Brian Robinson Jr. behind the 315-point Atlanta job, Kaelon Black behind San
Francisco's 302, Ty Johnson behind Buffalo's 262 — and no job has moved, because no games have been
played. **Nothing here is worth a claim before Week 1.**

**CAVEAT ON THIS LIST, stated because it will be wrong within a week:** it is the undrafted pool
computed from the draft results, not a live pull. It is correct as of the morning of 2026-09-08 and
goes stale on the first transaction anyone makes. **`wire.py` is what replaces it.**

## 6. OPEN

- `wire.py`'s ESPN half is **untested against a live session** — the one thing on this only Matt can run.
- The exact hour ESPN processes claims in this league is **not in the settings file**, which gives
  the period (2 days) and the order rule and nothing else. Worth confirming once from the league page.
- §4.19's paradox is still open: he is **1.05 weeks earlier** to the player than the field at RB and
  it does not convert. Doc 205 ruled out the drop side. Whether it is the wrong names or too early
  on the right ones is untested.
