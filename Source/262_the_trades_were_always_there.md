# 262 — The trades were always there, and the lane is not what §4.33 said

**Date:** 2026-09-09
**Trigger:** Matt: *"the trades I thought showed on the transaction report. I think there was one
last year, dunno."* He was right, and his memory was the only instrument that could catch it.

---

## 1. THE CAUSE, CONFIRMED — THE STRING WAS NEVER `TRADE`

Doc 260 shipped a type census rather than a guessed constant. One run settled it. **ESPN's
transaction vocabulary for a trade has five members and not one of them is a bare `TRADE`:**

| type | rows, 2022–2025 | carries an item list |
|---|---|---|
| `TRADE_PROPOSAL` | 45 | **45 of 45** |
| `TRADE_DECLINE` | 18 | 1 |
| `TRADE_VETO` | 16 | 0 |
| `TRADE_ACCEPT` | 14 | 7 |
| `TRADE_UPHOLD` | 7 | 0 |

**100 rows, four seasons, and `ty == 'TRADE'` discarded 100% of them.** `[TESTED]` The four
`trade_report_<year>.csv` files now exist for the first time in this project.

**Only `TRADE_PROPOSAL` carries the goods.** The other four are bare events pointing at a proposal —
which is why the accept/decline rows look empty and are not defective.

## 2. THE MEASUREMENT

**POPULATION — state it every time: every transaction of any `TRADE_*` type in this league's ESPN
feed, seasons 2022–2025, all scoring periods 1–18. n=100. Nothing is excluded.** The proposer is the
`Team` field on a `TRADE_PROPOSAL`; the counterparties are the team names inside its item list.

| season | proposed | completed | declined | veto | uphold | close rate |
|---|---|---|---|---|---|---|
| 2022 | 5 | 1 | 3 | 4 | 0 | 20% |
| 2023 | 13 | 6 | 5 | 10 | 3 | 46% |
| 2024 | 12 | 3 | 5 | 1 | 4 | 25% |
| 2025 | 15 | 4 | 5 | 1 | 0 | 27% |
| **all** | **45** | **14** | **18** | **16** | **7** | **31%** |

**11.2 proposals a season. 3.5 completed.** `[TESTED, n=45 proposals]`

## 3. §2 SURVIVES AND §4.33 DOES NOT

**§2's "3 league-wide per season observed" was recorded as a BEHAVIOURAL read with no source.
It reproduces almost exactly: 3.5.** That number is now measured, and it stands.

**§4.33's sentence built on it does not.** It says:

> *"AND THE TRADE LANE IS NEARLY CLOSED HERE... So the levers needing no counterparty — holes, the
> defence, and the job change nobody has priced — are the whole of it."*

**That is §0.6 rule 4 in a new place, and it is mine.** The count was of *completed* trades; the
conclusion was about whether *trying* is worth anything. Different populations. **Eleven proposals a
season is an active lane with a hard close** — the constraint is conversion, not appetite, and those
are different problems with different answers. "Nobody trades" and "nobody says yes" are not the
same sentence, and I wrote the first from evidence for the second.

## 4. HIS OWN RECORD, AND IT CUTS BOTH WAYS

Matt: *"trades are not frequent in my league, and when I get offers they are most often unbalanced
significantly in their favor."*

**CONFIRMED, and more sharply than he put it. Every offer he has ever received came from ONE
manager: `ChatCTE` — 4 of 4.** Two of them landed in week 10 of 2025 and he declined both on the
same day. §5 describes that manager as *"Hyperactive, volatile"* and doc 242 retracted his last-place
grade. **His read of the offers he gets is a read of one hyperactive counterparty, and it is
accurate.**

**AND IT CORRECTS HIM ON THE OTHER HALF: he is the most active PROPOSER in the league.**

| | proposed | received |
|---|---|---|
| **Matt (Juggers)** | **9 — most in the league** | 4 |
| next most active | 7 | 0 |

**He proposes more than twice as often as he is approached, and more often than anyone else.** The
self-image is a man fielding bad offers; the record is a man doing the asking. On his own file:
2 declines and **1 accept, 2025 week 12** — the trade he remembered.

## 5. TWO DEFECTS IN MY OWN SCRIPT, ONE FIXED

- **`TeamB` was empty on all 100 rows and nothing said so.** It read `memberId` — a member GUID —
  against a dict keyed by TEAM id, so it missed every time and wrote `''`. **FIXED:** the
  counterparty is already in the item list, since every leg is `[FROM -> TO]`. `waivers.py`
  7,182 → 7,843 bytes, re-pinned in `check_kit.py`. This is §3's identity rule — the join key was
  wrong and the failure was a silent empty string, not an error.
- **Player IDs are not resolved to names** — the rows read `TRADE Player ID 4038941`. ESPN's
  per-week `players` block does not carry traded players. **NOT YET RUN, input named:** the
  `espn_projections_<season>_*.csv` files already in `Source\` carry `espn_id` → name for 2022–2024;
  2025 has no such pull, so that season needs `kona_player_info`. Until then the WHO is measured and
  the WHAT is not.

## 6. OPEN, NAMED (§0.5a4)

- **What `TRADE_VETO` means is NOT established.** 16 of them, 10 in 2023 alone, against 7
  `TRADE_UPHOLD`. It is either one team's veto VOTE or a successful kill, and the two readings give
  opposite pictures of how this league polices trades. **BLOCKED** on nothing — it needs the row
  timestamps read against the accepts, which is one pass over files now on disk. Queued.
- **The per-manager table CANNOT be mapped to §5's slots yet.** Most names in it — `Olave Garden`,
  `Ekeler's Edge`, `Sentinel Sea Stallions`, `Moore Chubb for u to Love` — are historical and are not
  in the 2026 table. **§8.5's rule is absolute here: never match a manager by team name.** Matt's own
  row is safe because his name is stable and distinctive; every other row needs
  `manager_identity_map.csv` before it is quoted. **Do not attribute the "7 proposals, 0 received"
  row to a current manager.**
- **What a completed trade was WORTH is still unmeasured.** 14 accepts is the population; scoring
  them needs the player names from §5's first bullet.
