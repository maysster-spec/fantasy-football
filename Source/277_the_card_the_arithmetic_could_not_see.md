# 277 — The card the arithmetic could not see

Matt, 2026-09-10, quoting Monday's own shortlist back at me:

> *"The claim to make: Ricky Pearsall (SF). First-round pick and 3-of-3 on the receiver screen — the
> only free player with both. Same row's counterweight: 9 games last year."*

He was right about the signal, right about the counterweight, and the counterweight is the whole
story. **Pearsall is out for the 2026 season.** Finding that took one search, and the reason nobody
had done it is the second thing in this doc.

---

## 1. The recommendation is dead, and it died of the thing on its own row

**`[SOURCED: CBS Sports and ESPN, 1 August 2026]`** Pearsall is having season-ending surgery on the
PCL he injured in week 4 of 2025. Recovery is six to twelve months. He is on season-ending injured
reserve and will not play a down this year.

**The nine games were that knee.** The signal and the counterweight on that row were never two
facts; they were one injury seen from two sides, and the screen could only see the side that
flattered him — 53 targets, 5.9 a game, 10.3 yards a target, all of it compiled before the injury
and all of it inflating the very rates the screen keys on.

**And there is no consolation stash here.** A free-agency acquisition can never be a keeper in this
league (§2.1a), so a player who cannot help in 2026 cannot help in 2027 either. **The verdict is
DO NOT CLAIM**, and it is on the page in red.

---

## 2. The defect: he was never on the sheet at all

Doc 276 shipped the potential section yesterday. It listed three screened receivers. **The wire file
it read carries four**, and the one it dropped was the only player with both signals.

**The mechanism, reproduced before it was reported (§0.2):** ESPN publishes no projection for a
player on injured reserve — `proj_2026` is an empty string. `sheet_engine.rates()` skips any row
whose projection is at or below zero, because a zero would silently price a real player at nothing.
Correct rule, and it swallowed Pearsall with no error, no count, no line.

**This is §0.5(c)5 exactly** — the guard that exists because MarShawn Lloyd was rank 184 against a
180-row printed cut and simply was not on the paper. *"After any build that produces a printed or
rendered artifact, verify that the rows which must be on it ARE on it — by name, against the
decision they serve, not by row count."* The rule was written down and the new section did not have
it.

**FIXED, and the fix is a name and not a count.** `load_screened()` reads every screened row from the
newest wire file, independent of the pricing, and the page now prints a box naming anybody the
pricing dropped and why. Verified by rendering: the box names Pearsall.

**Worth stating plainly, because it is the general form:** the arithmetic liked Pearsall more than
any other name on the wire, and the arithmetic could not see a knee. That is not an argument for
less arithmetic. It is the argument for the section this doc adds.

---

## 3. The cards — dated news, the signal, and both cases

**`Source\cards_2026.csv`** is a new committed static input, in the same class as
`news_overrides.csv` and `sheet_constants.json`: written by hand, never computed, read by
`sheet_engine.py` and rendered under the bet section. Six cards, each carrying the signal, the
current status, dated news lines, a case for, a case against, and a one-line verdict.

**THE SCREEN LANE**

| player | verdict | the news that decides it |
|---|---|---|
| **Ricky Pearsall** (WR SF) | **DO NOT CLAIM** | season-ending PCL surgery `[CBS/ESPN, 1 Aug 2026]` |
| **Pat Bryant** (WR DEN, 1.9% owned) | the best live screen on the wire | week-1 depth chart has him third behind Sutton and Waddle, with Mims promoted ahead of him; Payton praises his hands, SI's Chad Jensen predicts a break-out as the number three who "will see the field often" `[Heavy, 9 Sep 2026]` |
| **Omar Cooper Jr.** (WR NYJ, 5.2%) | the cheapest lottery ticket | **WR4** — "leapfrogged on the depth chart by Isaiah Williams" `[Yahoo citing ESPN's Rich Cimini, 15 Aug 2026]` |
| **Jalen McMillan** (WR TB, 33.9%) | the same screen on a thinner base | left knee in camp, Bowles "expects him ready for week 1"; **four games in 2025**, so all three of his rates come off four games `[Sports Illustrated, 30 Aug 2026]` |

**THE SEAT LANE** *(and this is where the news changed a row)*

| player | verdict | the news that decides it |
|---|---|---|
| **Jordan James** (RB SF, 2.2%) | the seat is real, the man is not settled | Shanahan named the backup running back one of only two "murky" roles going into week 1 — James against rookie **Kaelon Black**, who "drew praise from both coaches and Brock Purdy throughout camp." *"Don't know yet… it's truly fluid."* `[NBC Sports Bay Area, 31 Aug 2026]` |
| **Brian Robinson Jr.** (RB ATL, 27.2%) | the one seat that already plays | steps into the Tyler Allgeier role behind Bijan — a defined complementary job, not a pure handcuff `[Atlanta Falcons / Yahoo, 2026 preseason]` |

**THE ONE THAT MOVED A ROW.** Doc 276's seat table ranks by what the job pays, and McCaffrey's job
is the second biggest on it. Shanahan's own words say **two men are in line for that seat**, and our
own two sources already disagreed about which — the published depth chart said Jordan James, ESPN's
projection order said Kaelon Black (doc 275). **Buying a contested seat is buying half a seat**, and
nothing in the ranking could express that. The card can.

---

## 4. What this changes about the section, stated as a rule

Doc 276 said the decision was **one comparison** — what the ticket is worth against what the spot
costs. That is still true of the *arithmetic*, and it is no longer the whole decision.

> **A number on this page prices a role. It cannot see a knee, a coach's sentence, or a rookie who
> passed somebody in August.** The screen ranks; the card decides. Where they disagree, the card
> wins, because everything the arithmetic knows is already in the screen and the card is the only
> place anything else can enter.

That is not a retreat from measurement. Every card names its outlet and its date (`ERROR_PATTERNS`
B7), the two cases are written to be argued with, and the verdict line is short enough to be wrong
in public.

---

## 5. Shipped

| file | what |
|---|---|
| `Source\cards_2026.csv` | **new.** Six cards. Hand-written, dated, never computed |
| `Scripts\sheet_engine.py` | `load_screened()` (the missing-row guard), `load_cards()`, the card block and its stylesheet |
| `Scripts\check_kit.py` | `sheet_engine.py` re-pinned |

**Negative controls run:** no `cards_2026.csv` → the section says the news half is missing, not
empty · no `WIRE_*.csv` → the guard reports it rather than claiming nothing was dropped · the guard
itself was verified against the live defect and it names Pearsall.

**NOT YET RUN, input named:** nothing on this page refreshes the news. A card is only as current as
the session that wrote it, and `cards_2026.csv` carries no staleness date of its own. The fix is a
`built` field plus a line on the page when it is more than a week behind the wire file — queued, not
built.
