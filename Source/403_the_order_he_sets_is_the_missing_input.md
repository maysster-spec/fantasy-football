# 403 — The order he sets is the missing input, and it has to be captured before the run

*23 Sept 2026. Unblocks the item doc 401 left open. `claim_order_log.py` is new. Ledger row 178.
Nothing in the Sunday path changed.*

---

## 1. WHAT WAS BLOCKED

Doc 401 retracted the claim-order gradient and named the blocker: **every claim in a waiver run carries one identical
timestamp**, so `waiver_report_*.csv` cannot express within-run order, and *"prior wins that run"* was never a
quantity the data could say. The missing input is **the order Matt set**, paired with which claim won.

**That pairing has to be captured before the run.** Afterwards the order is gone: the report shows outcomes and one
shared timestamp, and nothing recovers the priority he dragged them into.

---

## 2. THE PREMISE WAS TESTED FIRST, WHICH IS THE POINT

§0.5(a5) exists because on 22 Sept a standing instruction shipped resting on an untested centre, with four real but
adjacent measurements stacked around it. So before writing anything:

**Testable form:** *if ESPN's API exposes pending waiver claims together with their priority order, the logger costs
Matt nothing; if not, it cannot be built without asking him to record the order by hand.*

**What was checked, and it is not the same as assumed:**
- `wire.py` requests exactly three views: `mTeam`, `kona_player_info`, `mRoster`. **None carries pending
  transactions.** So this is not doc 395's case, where four fields were in a payload already being fetched and
  thrown away. The data is genuinely not in hand.
- `wire.py` imports cleanly: its only top-level non-definition statement is the docstring and `__main__` is guarded,
  so the probe **reuses its session config instead of copying cookies into a second file.** One place to rotate
  credentials, not two.

**The live question is still open**, because answering it means an authenticated read against Matt's ESPN session,
and §0.4 puts that on his side of the line. It is a five-second command, not a research task.

---

## 3. WHAT SHIPPED, AND WHY IT IS NOT IN `ff.bat` YET

`claim_order_log.py` is **a probe first and a logger second**, because the schema is unknown:

1. asks for `mPendingTransactions` and `mTransactions2`
2. **prints the key names of a pending item**, so the schema is learned from the payload rather than guessed
3. appends anything it can see to `Source\CLAIM_ORDER_LOG.csv`, **append-only, no state comparison, so there is no
   silent-skip path** (the shape STATUS_LOG.csv uses, doc 393)

It does not touch `wire.py`, writes no page, and **nothing in the Sunday path reads its output.** If it is wrong it
costs one CSV, not a lineup. It stays out of `ff.bat` until it has run live once, because `ff.bat` builds Sunday's
pages and doc 144 is three scripts that worked in my container and died on his machine.

**If no order field is present it says so and logs the list order as `seen_order`, explicitly marked NOT
ESTABLISHED** as a reflection of his dragged priority. A list that happens to arrive in an order is not an order
field.

---

## 4. THE NEGATIVE CONTROLS FOUND A DEFECT IN MY OWN SCRIPT

Three controls, run before shipping (§0.2: a guard that has never been executed is not a guard):

| control | expected | result |
|---|---|---|
| ESPN unreachable | fail loudly, write nothing | **caught a real bug, see below** |
| reachable, nothing pending | say so, write nothing, exit 0 | OK |
| two of mine pending plus one of another team's | log mine only, order preserved, detect the order field | OK |

**Control 1 failed in the way that matters.** The first cut printed *"No pending waiver claims visible. That is a
legitimate result, not a failure"* and **returned 0** when it had reached nothing at all. That is doc 146's
exit-code trap exactly, and the script's own docstring claimed the opposite behaviour.

**It also would not have been caught by the assert as first written**, which only checked that no file was created.
The artifact here *is* the exit code, so the control now asserts it. Fixed: reaching no view returns 2 and says it
cannot tell *"no claims pending"* from *"could not ask"*.

---

## 5. A NEAR MISS WORTH RECORDING

`check_citations.py` was committed into `Scripts\` earlier today **without checking how `check_kit.py` treats a file
it does not know about.** If that folder were an exact set, every kit check from then on would have reported EXTRA
and incremented the failure count, which is the cry-wolf failure doc 402 had just been written about.

It is fine: `Scripts\` is `exact=False`; only `live_draft` and `espn_bridge` are exact sets. **But that is luck, not
method.** The rule that belongs next to doc 146's folder-listing rule: **before adding a file to a checked tree,
read how the checker treats an unlisted file.**

Neither new script is pinned in the manifest yet, deliberately: pin once they have run live and stopped changing.
**[OPEN], mine.**

---

## 6. WHAT MATT DOES, AND IT IS ONE LINE

**After placing Sunday's claims, before they process, run `py claim_order_log.py`.** That is the whole window.
Placement is Sunday night and processing is Tuesday morning, so any time in between works.

Once it has run live and the schema is known, it folds into `ff.bat` and he never runs it again.

---

## 7. STILL OPEN

- the live probe, above
- pinning both new scripts in `check_kit.py`'s manifest
- **D3**, whether `own_chg` predicts contention in this league: unblocked as of this morning, needs weeks
- **batch E**: ledger rows 162, 163, 165; the doc 383 registry batch; §4.33's TE playoff draw; `Auto Reactivate: No`;
  the position-cap and keeper-eligibility interactions with IR
