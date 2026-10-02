# 399 — The seat dies when the designation goes, not when he plays. And the curve we published reproduces under nothing.

*23 Sept 2026. Doc 397 batch D1, worked in the order Matt set. Directive v9.21 → v9.22. `ir_seat_validity.py` is new
and reproduces doc 391's headline before it measures anything. Ledger row 174. Doc 391 corrected at source.*

---

## 1. WHY THIS RAN

Batch A struck a line in §2 that said the 19.5% downgrade-to-Questionable cell was *"the quiet failure, seat gone and
nothing gained."* v9.19 had already killed that: ESPN's football help says an update **"from OUT or IR to QUESTIONABLE
or DOUBTFUL"** leaves the roster **"NOT invalid."** He keeps the seat.

**Striking it exposed the larger problem.** If a Questionable downgrade does not end the seat, then *nothing* in doc
391's seat-life table was measuring when the seat ends. It was measuring **when the man takes a snap**, which is a
different event, and the whole *"median seat dies between two and three weeks"* rested on it.

**Direction was not predicted, and I said so before the run** (§0.5(a2)). Two mechanisms push opposite ways: a
Questionable downgrade **keeps** a seat the old measure killed, and **38.2%** of Out players carry no designation at
all in w+1 — that group loses the seat immediately, and the old measure counted most of them as still holding it.

---

## 2. THE REPRODUCTION CHECK CAME FIRST, AND IT PASSED EXACTLY

§0.2 and §5.5: build the real object, not an equivalent one. Before measuring anything new the script rebuilds doc
391's population and prints its rates:

| | this run | doc 391 |
|---|---|---|
| population n | **1,431** | 1,431 |
| plays a snap in w+1 | **29.6%** | 29.6% |
| still Out | **38.9%** | 38.9% |
| downgraded to Questionable | **19.5%** | 19.5% |
| Doubtful | **3.4%** | 3.4% |
| no designation at all | **38.2%** | 38.2% |

**To the decimal, on all six.** The script, the filter and the population are sound — which matters, because it
localises everything below to the curve rather than to the data.

---

## 3. THE FINDING: THE TWO ERRORS RUN IN OPPOSITE DIRECTIONS

Seat **valid** = designation in {Out, Doubtful, Questionable}, or no designation but dark for three further weeks,
which reads as NFL injured reserve and which ESPN's slot accepts. Seat **invalid** = no designation and he played, or
no designation and he plays again later.

| | w+1 | w+2 | w+3 | w+4 | w+5 |
|---|---|---|---|---|---|
| **seat still VALID (the event that matters)** | **75.5%** | **51.2%** | **35.2%** | **26.4%** | **22.2%** |
| still not playing (what we measured) | 70.4% | 52.7% | 41.9% | 35.6% | 31.5% |

**Week one, the seat is SAFER than published** — the most common upgrade keeps it. **Week three on, it is SHORTER** —
losing the designation without playing kills a seat the old measure counted as alive. The gap reaches **9 points by
w+5**.

**THE CONCLUSION SURVIVES.** The valid curve crosses 50% between w+2 and w+3: **the median seat still dies between two
and three weeks.** Matt's play does not change. The number behind it does, and so does the shape of the risk.

---

## 4. THE PUBLISHED CURVE IS RETRACTED, NOT PATCHED. IT REPRODUCES UNDER NOTHING.

Doc 391 published the curve on **n=1,035** — a population the directive then inherited without the n, which is §0.6's
failure mode exactly. Six definitions were tried against it:

| population | n | w+1 | w+2 | w+3 | w+4 | w+5 |
|---|---|---|---|---|---|---|
| all Out-weeks, team plays w+1 | 1,431 | 70.4 | 52.7 | 41.9 | 35.6 | 31.5 |
| all Out-weeks, byes kept | 1,657 | 74.4 | 56.0 | 45.4 | 39.2 | 35.0 |
| first Out per player-season, team plays w+1 | 779 | 72.5 | 54.6 | 42.2 | 34.4 | 29.3 |
| first Out per player-season, byes kept | 885 | 75.8 | 56.8 | 45.3 | 37.6 | 32.4 |
| episodes (gap > 2), team plays w+1 | 899 | 72.3 | 54.7 | 42.9 | 35.8 | 31.3 |
| episodes (gap > 2), byes kept | 1,040 | 76.1 | 57.7 | 46.9 | 40.0 | 35.2 |
| **published** | **1,035** | **73.8** | **53.8** | **40.8** | **31.2** | **23.8** |

**None matches.** The nearest by n is 1,040 against 1,035 and it runs **4 to 11 points high in the tail**. Every
variant decays more slowly than the published one, which is the signature of a shrinking denominator somewhere in the
original, but **that is a guess and it is not asserted** — the supportable statement is that the curve cannot be
reproduced and therefore cannot be quoted (§3). The six variants ship inside the script so the retraction is
re-checkable rather than taken on my word.

---

## 5. NEW, AND NO FILE IN THIS PROJECT HELD IT

**PARKING AN OUT MAN LEAVES THE ROSTER INVALID — AND THE LINEUP FROZEN — THE FOLLOWING SUNDAY 24.5% OF THE TIME.**
351 of 1,431: **257 played**, and **94 were cleared without playing**, which is the case no one would think to watch
for.

**About one parked man in four.** That is the price of §2's Sunday-morning roster check, and until now it was an
instruction with no number attached.

---

## 6. AND THE POSITION ORDERING INVERTS

| | seat invalid at w+1 | ~~plays w+1 (old measure)~~ |
|---|---|---|
| **RB** (n=296) | **20.3%** — safest seat | 26.7% |
| **QB** (n=156) | **22.4%** | 19.2% — *"holds longest"* |
| **TE** (n=309) | **24.9%** | 31.4% |
| **WR** (n=636) | **26.1%** — riskiest seat | 33.0% |

**A parked QB was the SAFEST park on the old measure and is the second RISKIEST on this one.** A quarterback ruled out
loses his designation without playing more often than any other position — he is on the sideline in a cap, healthy
enough to dress. The old line drew an inference from this about §6's streaming doctrine (*"the opposite of what the
roster wants, since QB is the position §6 says to stream"*); **that inference is withdrawn.** The half that survives
is that **a parked receiver is the riskiest seat.**

---

## 7. WHAT IS STILL OPEN

- **[NOT ESTABLISHED] The NFL-IR arm is a proxy.** nflverse drops a player from the weekly report when he leaves the
  53, so *no designation* conflates cleared-and-healthy with on-IR-and-gone; the script separates them by looking
  three weeks forward. **ESPN's own `injuryStatus` settles it directly**, and `STATUS_LOG.csv` (doc 393) starts
  recording it on the next `ff.bat` run. Re-run this then.
- **[OPEN], mine:** §4.23a is cited in `DIRECTIVE_FINDINGS.md` with no index row and no body (carried from batch A).
- **Batch B is next**: the header accretion Matt noticed unprompted, with B3's outside read.

---

## 8. PROVENANCE

Five files archived to `2026\_archive\` before being overwritten, committed from a fresh container path with
`expectedMtimeMs`, then staged back and compared by CRLF-normalised sha256 — **content, never the commit result**
(§9 rules 1 and 2). Every edit asserted its occurrence count before applying (§9 rule 6). **Doc 391 is corrected at
source with a banner and its curve struck in place** (§9 rule 5), because the retraction has to reach the doc that
minted the number, not only the files that cite it.

`Scripts\research\ir\ir_seat_validity.py` carries its pre-registered form in the docstring, asserts that the REG
filter drops no season (doc 391's own defect, which silently discarded four of five seasons), joins on
`gsis_id → pfr_id` and never on a name (§3), and prints the reproduction check and all six failed variants on every
run.
