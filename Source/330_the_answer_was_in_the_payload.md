# 330. The answer was in the payload

*17 Sept 2026, 00:50 UTC. Matt: "how do you not know what players are available? Last i checked
you should have access to all that information... Are you doubting the information you have?"
He is right, it was not doubt, and it was worse than doubt: the pull already asked ESPN for the
answer and the parser threw it away. Fixed, controlled, 65 of 65.*

---

## 1. WHAT CHANGED

1. **`wire.py` line 1327 already asks ESPN for `filterStatus: ["FREEAGENT", "WAIVERS"]`.** ESPN
   returns which one each man is, **on the pool entry**. The parser read `injuryStatus` off the
   nested `player` object and never looked at the entry. **The Add-or-Claim answer has been in
   every payload since the wire was written.**
2. **Fixed.** New `avail` column on `WIRE_*.csv` and on `FREE_UNRANKED_*.csv`, and the row now
   leads with **ADD, costs no priority** or **CLAIM, costs your priority**.
3. **Never defaulted.** If ESPN serves nothing, the run says so and no row invents either word.
4. **C22 and C22c added to `redteam_controls.py`, and the negative control fires.** 65 of 65,
   run against the real tree, not a fixture.
5. **AND THE RUN FOUND A SECOND THING I DID NOT GO LOOKING FOR, recorded as C22c: the file knows
   and the page still does not show Kaelon Black at all.** Ledger rows 29 and 42, still open.
6. **`check_kit.py` re-pinned:** `wire.py` 109,601 bytes, `188edb934ba446b8`.

---

## 2. THE DEFECT, EXACTLY

```python
xf = {"players": {"filterStatus": {"value": ["FREEAGENT", "WAIVERS"]}, ...
```
Then, 139 lines later:
```python
for entry in pool:
    p = entry.get('player') or {}
    status[pid] = (p.get('injuryStatus') or 'ACTIVE').upper()
```
**`entry['status']` is where ESPN puts FREEAGENT or WAIVERS. `entry['player']['injuryStatus']` is
whether he is hurt. The wire read the second and never the first**, so the page said "check the
button" on every row, and on 16 Sept I said it to Matt in a reply as well.

**This is section 0.4 in its most expensive form: I asked him to do something the payload had
already done.** It is not that the data was doubtful. It is that a field we pay for on every run
was discarded at the parse.

---

## 3. THE FIX, AND WHY IT REFUSES TO GUESS

The row now carries the raw ESPN token in `avail`, and the page carries the instruction:

| ESPN token | what the row says |
|---|---|
| `FREEAGENT` | **ADD, costs no priority** |
| `WAIVERS` | **CLAIM, costs your priority** |
| absent | nothing, and the run raises a LOAD PROBLEM naming it |

**Absence is never read as FREEAGENT.** Section 3's rule against defaulting a mandatory field: a
wrong Add is a claim he did not need to spend and a wrong Claim is a man he could have had
tonight, so a silent guess is worse here than a blank. The word goes at the FRONT of the flag
string because it changes the ORDER of the list (section 4.32: only the first clearing claim
spends real priority).

---

## 4. THE CONTROLS, AND THE TWO WRONG OBJECTS THEY CAUGHT IN ME

**C22, five checks, both arms.** The mock now plants ESPN's availability on the pool entry, which
it never carried before.
- **Negative control first (doc 59's rule): with nothing served, the run must SAY it cannot tell.**
  It does, and no row invents a word.
- Positive: planted `FREEAGENT` and `WAIVERS` reach the page in the right words, the console
  counts them, and the CSV carries both tokens.

**The control was wrong twice before it was right, and both were the same error I keep making.**
1. It asserted the wording on **Kaelon Black**, who is not rendered on that page at all.
2. It then used **Brenton Strange**, who renders only in the playoff tight-end table, which prints
   a schedule and no flags.
**Correct assertions about the wrong object, section 0.5(a2), in a control this time.** Running it
is what found both; reading it would not have.

---

## 5. C22c: THE GAP THIS DOES NOT FIX, RECORDED SO NOBODY READS THE PASS AS THOUGH IT DID

**Kaelon Black is the most-raced back on the live wire and the page cannot say one word about him,
because it never prints him.** The priority list ranks on ESPN's AUGUST projection, where he is
**minus 112.1**, and the row cap drops him before any flag is read. Adding an availability column
does nothing about that.

C22c asserts it as a KNOWN GAP: the file carries his availability, and the page does not render
him. **If that check ever fails, the page has started showing him and ledger rows 29 and 42 can
close.** A control that asserts a defect still exists is the only kind that notices when it stops.

`[OPEN]` and it is the same defect as doc 326's: the board's own sort is blind to the in-season
workload, so the man with 15 opportunities sits below men with none.

---

## 6. OPEN

- **Ledger rows 29 and 42**, the August projection ranking the in-season list. C22c now watches it.
- **The page renders flags in some tables and not others**, so a row's availability shows in the
  pool table and not in the playoff tables. Cosmetic today, and named here so it is not rediscovered.
- Carried from docs 326 and 329: JOB 3, JOB 4, the section 4.25b wording, the draft-capital column,
  the chart-versus-usage tell, catalog B4.
