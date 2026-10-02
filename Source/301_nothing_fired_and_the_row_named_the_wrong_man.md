# 301 — Nothing fired, and the row named the wrong man

**Sunday 13 Sept 2026, the 11:40am ET window. Week 1.**

## 1. The answer first

**Nothing fired. No claim, no drop, no priority spent.**

- **No player on `MY_ROSTER.csv` is on any inactive list** I could reach. All 15 checked by name.
- **No 1:00pm starter on a `free=yes` row of `inherit_2026.csv` was ruled out.** The 1pm teams
  holding a watched job — ATL (Bijan), IND (J. Taylor), TEN (Pollard), NYJ (Hall), CLE (Judkins),
  CIN (Chase Brown), BUF (Cook) — none reported out.
- **The one vacant backfield is Green Bay, and it is two weeks old.** Josh Jacobs went on the
  **Commissioner's Exempt List on 30–31 Aug 2026, indefinitely**
  `[SOURCED: ESPN, FOX Sports, NFL.com, packersnews.com, 30–31 Aug 2026]`. That is not a speed
  play — the market has had a fortnight. GB@MIN kicks at **4:25pm ET**
  `[SOURCED: CBS Sports 2026 Week 1 schedule]`.

**And the standing caveat kills it anyway.** His RB room is five deep — Jeanty, Judkins, Dobbins,
Dowdle, Washington Jr. A back who sits behind nobody of his is worth almost nothing to him. The
exception in the brief — a back behind one of **his own** starters — did not trigger today.

---

## 2. The defect: the GB row named the third-string back

`inherit_2026.csv` carried GB as `live_tag = out`, `next_man = Chris Brooks`, `free = yes`,
`owned_pct = 10.3`.

**The `live_tag` was updated when Jacobs went out. `next_man` never was.**

Today's Packers backfield `[SOURCED: Bolavip, 13 Sep 2026; corroborated by Sports Illustrated's
"Lloyd or Kaleb Johnson" Week 1 piece]`:

| order | player | in our league |
|---|---|---|
| 1 | **MarShawn Lloyd** | **ROSTERED** — absent from `WIRE_20260913.csv` and `FREE_UNRANKED_20260913.csv` |
| 2 | Chris Brooks | free, 11.3% owned, value **−138.5** |
| 3 | Kaleb Johnson | free, 6.2% owned — **but the wire file still has him on PIT** |

Emanuel Wilson, the 2025 backup, is no longer on the roster.

**So the row was surfacing a third-string back on a 152-point job as an opportunity** — the second
smallest backfield on the whole table, below Tennessee's 171, which is the number doc 240 used to
price the Spears hold at about **−5**. This is §4.20's *buy the job, never the name* and doc 296's
*the man who inherits must be playing*, failing on the one row that was actually live.

**CORRECTED, archived first.** GB now reads `next_man = MarShawn Lloyd`, `free = rostered`, with
the dated reason in `why`. `next_man_id` is left **empty rather than invented** (§3). One row
changed; header and row count identical (33 rows, 15 columns, verified). Old copy at
`2026\_archive\inherit_2026_20260913_1205.csv`.

**NOT YET RUN, and it is on `matt_todo.txt`:** `wire.py` and `check_kit.py` have not been re-run
against the corrected file — there is no shell on Matt's machine this session, only stage/commit.

**[OPEN] Is Kaleb Johnson a Packer?** Two outlets say Green Bay traded for him on 30 Aug; Matt's
own ESPN-derived `WIRE_20260913.csv` still lists him **PIT**, flagged *"unsettled job, worth 174"*.
If the trade is real that job number is the wrong backfield. One look at his ESPN page settles it.

---

## 3. The sources were not usable, and that is the finding to carry

**Every public inactive feed I reached today is serving 2024–25 rosters.** This is `ERROR_PATTERNS`
B7 territory and it nearly produced a confident wrong answer.

| source | what it published today | why it is unusable |
|---|---|---|
| fantasypros.com/nfl/players/inactives.php | listed **Aaron Donald** inactive for LAR | Donald retired in 2024 |
| sundayguardianlive.com 1pm tracker (upd. 13 Sep 2026) | *"Jaguars: Travis Etienne fully active"*, *"Saints RB Alvin Kamara inactive"* | Matt's own `inherit_2026.csv` has **Etienne as the NO starter and Kamara as his backup** |
| same | *"Steelers QB Russell Wilson inactive"*, *"Jets Aaron Rodgers active"*, *"Falcons QB Kirk Cousins active"* | all 2024–25 facts |
| nfl.com/inactives | *"Please check back soon"* | nothing published |
| Yahoo live blog vs FantasyPros | Tua on **MIA** vs Tua on **ATL** | flatly contradict each other |

**So the 1pm inactive list is reported here as UNVERIFIED, not as clean.** What survived
cross-checking is narrow and is what section 1 rests on: Jacobs (four outlets, dated), the GB depth
order (two outlets, dated), the kickoff times (CBS), and Matt's own files.

**THE RULE THIS EARNS:** *the Sunday window depends on a feed this project has never audited.* Doc
228's lesson was that an inherited population goes unexamined; this is the same shape one level out
— an inherited **source**. Before next Sunday, the 11:40 run needs at least one feed whose 2026
rosters have been checked against `inherit_2026.csv`, or it will keep being unable to answer the
only question it exists to answer.

---

## 4. What was verified, and what was not

**VERIFIED:** all 15 roster names against every list reached · the 14 `free=yes` rows against the
1pm slate · Lloyd's absence from both of today's free-pool files · the corrected CSV's shape ·
kickoff times for GB, CLE, CIN, BUF, MIA, PHI, LAC, KC.

**NOT VERIFIED:** the official 1pm inactive list (no trustworthy feed) · Kaleb Johnson's team ·
Lloyd's `espn_id` · any downstream guard on the corrected file.

**Also noted, and it argues the same way:** the Kaelon Black claim is already filed and settles
Thursday. There was a second reason not to spend anything today.

**And the calendar is against a claim regardless.** §4.31: a **week-1** add returns a season asset
**9.4%** of the time against week 2's **34.6%** (n=718, Fisher p=0.010) — the worst week of the
year. The scope note in doc 253 does not rescue it, because that exemption is for filling an
**empty** starting slot, and his lineup is full.
