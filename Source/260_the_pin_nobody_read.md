# 260 — The trade vocabulary is unknown, and the guard that should have said so was pinned to the wrong file

**Date:** 2026-09-09
**Trigger:** Matt, after running `py waivers.py`: *"the trades I thought showed on the transaction
report. I think there was one last year, dunno."*

---

## 1. WHAT HE RAN, AND WHAT IT PRODUCED

`py waivers.py` executed on his machine at **2026-09-09 21:19 UTC**. `waiver_report_2025.csv` went
**55,054 → 59,093 bytes**. It works.

**It wrote no `trade_report_*.csv` for any of the four seasons**, because `write()` returns 0 on an
empty list and never creates the file. The script's own §0.2 guard fired correctly:

> *"ZERO TRADES ACROSS EVERY SEASON. That is either true of this league or the feed does not carry
> them. Do not read it as 'nobody trades' until it is checked against one trade you remember
> happening."*

**Matt is the check the guard asked for, and he answered it: he remembers one.**

## 2. THE POPULATION QUESTION COMES FIRST (§0.6 rule 4)

*A conclusion that contradicts his direct experience is a population question first.* The 2025 report
holds **572 rows** and its `Type` column contains exactly two values:

| Type | rows |
|---|---|
| WAIVER | 432 |
| FREEAGENT | 140 |

**That is the filter's output, not the feed's vocabulary.** The report cannot tell us what ESPN calls
a trade, because the report is defined as the two types that are not trades. **We have never seen the
list of transaction types this feed returns.**

## 3. THE DIAGNOSIS IS A CLAIM AND IT IS NOT BEING SHIPPED AS A FIX (§0.2)

The likely cause is visible in the source — `waivers.py` matched **`ty == 'TRADE'` exactly**, in two
places, and ESPN's transaction enum plausibly uses `TRADE_ACCEPT` / `TRADE_PROPOSAL` / `TRADE_UPHELD`.
**Plausible is not measured, and the container cannot reach ESPN (403) to settle it.**

So the patch does **both**, and one run settles it either way:

1. **A census of every `type` string the feed returns**, printed before the zero-trade guard, with the
   ones now captured marked. If the vocabulary is `TRADE_ACCEPT`, the census says so by name. If the
   feed genuinely carries no trade of any spelling, the census says *that*, and the answer becomes
   "wrong view" rather than "wrong constant".
2. **Both matches widened to `ty.startswith('TRADE')`**, so a captured variant lands in
   `trade_report_<year>.csv` on the same run rather than requiring a second.

Shipped: `Scripts\waivers.py` **6,437 → 7,182 bytes**, `py_compile` clean, stdlib + `requests` only
(§0.4 environment rule). Old copy archived to `2026\_archive\waivers_20260909.py`.

## 4. THE REAL FINDING: A PIN THAT HAD NEVER BEEN RIGHT

`check_kit.py`'s manifest carried:

```
'waivers.py': (2997, '634dc1215d8b05e5'),
```

**2,997 is the byte count of `espn_api_python_script_historical_trans.py`, the line above it.** It was
copied by hand and was never this file's size. `waivers.py` was **6,437 bytes** before today, so
`check_kit.py` has been reporting a mismatch on it since the 09-08 rewrite — **and nobody read the
line.**

**This is §0.2's "a guard that has never been executed is not a guard" in its quieter form: a guard
that fires into a report no one reads.** The exit code was fine. The artifact said otherwise.
Re-pinned to `(7182, '7c41551bdbd83271')` with the reason in a comment above it.

## 5. STATUS UNDER §0.5(a4)

- **The trade record** — **NOT YET RUN.** Input named and now in place: one `py waivers.py` on his
  machine, which prints the vocabulary whatever the answer is.
- **Whether the trade sits in a different ESPN view** — **BLOCKED** until the census comes back. If
  the census shows no `TRADE*` string at any scoring period, the next input is `mTransactions2`
  without a `scoringPeriodId`, or the `mSettings`/`mTeam` transaction counters, both reachable only
  from his session.
- **§4.33's closing line stands unchanged:** *every trade claim in this project is unmeasured until
  `py waivers.py` runs.* It has now run once and produced a **null we do not trust**, which is not
  the same as a measurement.
