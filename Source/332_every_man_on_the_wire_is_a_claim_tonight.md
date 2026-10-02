# 332. Every man on the wire is a claim tonight, and the biggest job is the wrong chip

*17 Sept 2026, 02:00 UTC. Matt ran the wire at 9:23pm ET, could not find Kaelon Black on the sheet,
and asked whether to run it again and which next-man-up back is worth a chip instead. The run
worked. Black is on the sheet but not where he reads. And his instinct about not landing Black is
correct on his own measured record.*

---

## 1. WHAT CHANGED

1. **The run printed. Nothing to re-run.** `WIRE_20260916.csv` is 33,564 bytes, written 21:23 ET,
   and the new `avail` column is filled on all 281 rows.
2. **ALL 281 AVAILABLE PLAYERS READ `WAIVERS`. There is not one free agent tonight.** The weekly
   period is running, so every add costs a claim until Thursday morning processing. The "if the
   button says Add" branch is dead this week, for everybody.
3. **Black IS on the sheet, in the handcuff table and as a card. He is not in "Priority pickups,
   in order", which is the list Matt reads.** Ledger rows 29 and 42, exactly as C22c predicted.
4. **THE PRIORITY LIST HAS NO RUNNING BACK IN IT AT ALL.** 1 Schultz, 2 Malik Washington,
   3 Devaughn Vele. That is the August-projection sort, and it is why the question had to be asked
   in a chat instead of answered on the page.
5. **`THE_WEEKLY_WIRE.html` is still from 15 September.** It only rebuilds with `--html`, and its
   waiver-order sentence is doc 311's hard-coded string, so it is not evidence of his position.
6. **RECOMMENDATION: Chris Brooks (GB).** Not Black.

---

## 2. WHY NOT BLACK, IN HIS OWN NUMBERS

Matt: *"if you see the waiver order I'm not going to get him."* **His read is right, and the wire
page already carries the measurement that proves it, from his own two seasons:**

> *"You lose five of every six players another team also wants. Over the last two seasons you
> chased 63 players somebody else claimed the same week and got 10 of them. On the players nobody
> else claimed, you got 56%."*

**Black is the most contested profile on the board: 44.2% rostered elsewhere, 15 carries and
targets in week 1, which is doc 314's 15-plus band at 2.27 filers and 56% contested.** One claim
spent there is a one-in-six shot by his own record. **The same claim spent on a man nobody is
filing on is better than even money.**

**I do NOT know his waiver position.** The only sentence on file is the hard-coded "near the back
of the line" that doc 311 flagged as wrong, on a page two days stale. `py wire.py --html` fetches
the real `waiverRank` from ESPN and prints it. Until then the honest statement is: **unknown, and
the contest level is the part that decides this anyway.**

---

## 3. THE UNROSTERED NEXT-MAN-UP BACKS, WITH THE MAN AHEAD PRICED

**POPULATION: every `next_man` in `Source\inherit_2026.csv` not on any of the twelve rosters in
`LEAGUE_ROSTERS.csv`, joined to `WIRE_20260916.csv` for week-1 workload and ownership. n=15.
The contest band is doc 314's, keyed on last-completed-game carries plus targets.**

| back | tm | job | man ahead | his 2025 games | week 1 | owned | contested |
|---|---|---|---|---|---|---|---|
| Brian Robinson Jr. | ATL | **315** | Bijan Robinson | **17** | 25% snaps, 9 opp | 24.2% | 29% |
| Kaelon Black | SF | **302** | McCaffrey, **questionable now** | 17 | 43% snaps, 15 opp | **44.2%** | **56%** |
| DJ Giddens | IND | 291 | Jonathan Taylor | **17** | no snaps | 0.3% | 14% |
| Ty Johnson | BUF | 262 | James Cook III | 17 | no snaps | 1.6% | 14% |
| Tank Bigsby | PHI | 252 | Saquon Barkley | 16 | 11% snaps | 16.5% | 14% |
| **Chris Brooks** | **GB** | **241** | **Josh Jacobs, OUT indefinitely** | 15 | **56% snaps, 8 opp** | **15.5%** | **29%** |
| Samaje Perine | CIN | 239 | Chase Brown | 17 | 28% snaps, 8 opp | 11.2% | 29% |
| **Keaton Mitchell** | **LAC** | **236** | **Omarion Hampton** | **9** | 31% snaps, 4 opp | 19.6% | **14%** |
| Dylan Sampson | CLE | 211 | Quinshon Judkins *(Matt's own)* | 14 | none | 15.0% | 14% |
| **Tyrone Tracy Jr.** | **NYG** | 205 | **Cam Skattebo** | **8** | 3% snaps | **4.5%** | **14%** |

**READ THE `man ahead` COLUMN, NOT THE `job` COLUMN. That is doc 240's rule and it inverts the
top of this table.** The two biggest jobs, 315 and 291, sit behind men who played all seventeen
games last season. **That is the Spears profile exactly: a large job whose holder never misses.**

---

## 4. THE RECOMMENDATION, AND THE HONEST COUNTER ON EACH

**1. CHRIS BROOKS (GB).** The only man on this table whose job is **already open rather than
waiting on an injury**: Jacobs has been on the Commissioner's Exempt List since 30 Aug 2026,
indefinitely. Brooks took **56% of the snaps** in week 1, the highest share of any unrostered back
here. At 15.5% owned in the 29% band, this is the kind of claim Matt wins at better than even
money. **COUNTER, and it is real: he splits with MarShawn Lloyd, who is rostered by DUCK and
out-carried him 13 to 7 in week 1. Brooks gets a SHARE of 241, not the whole of it.** Also worth
knowing: **Jacobs is still rostered**, so that owner can claim Brooks himself at any time.

**2. KEATON MITCHELL (LAC).** The fragility signal that actually measures in this project is games
missed, not age or reputation, and **Omarion Hampton played 9 of 17 in 2025**. Mitchell is already
on 31% of snaps. 19.6% owned, 14% contested band, so he lands. **COUNTER: Hampton is rostered by
POT and healthy right now, so this is a seat, not a job.**

**3. TYRONE TRACY JR. (NYG), the cheapest ticket.** **4.5% owned, nobody in this league is filing
on him**, and Cam Skattebo played 8 of 17 last season. **COUNTER, and it is why he is third: 3% of
the snaps in week 1. He is not taking work, so he is a pure bet on Skattebo missing time.**

**DO NOT CHASE: Brian Robinson Jr. or DJ Giddens.** Jobs of 315 and 291, and both holders played
all seventeen. The number that makes them look good is the one doc 240 says to ignore.

---

## 5. OPEN

- **Ledger rows 29 and 42.** The priority list still ranks on an August projection, so no running
  back appears in it and this recommendation had to be made in a chat. C22c watches it. `[OPEN]`
- **His real waiver position is unknown.** `py wire.py --html` fetches it; the sentence currently
  on the page is doc 311's hard-coded one. `[OPEN]`
- **`inherit_2026.csv` is from 14 September** and its ownership figures are stale against tonight's
  wire (Black reads 15.4% there and 44.2% on the wire). The job and the man ahead are current; the
  ownership is not. `[OPEN]`
- Carried: JOB 3, JOB 4, the section 4.25b wording, the draft-capital column, catalog B4.
