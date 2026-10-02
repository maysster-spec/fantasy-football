# 48 — STAGED RED TEAM: PROTOCOL AND FAILURE CATALOG
**Aug 25, 2026.** Throughline: **bug-fix and enhancement of the projected stat line** — the number
every downstream decision rests on. Method chosen after researching current guidance; sources at
the end. Matt's framing was right in structure; two things below deliberately depart from it.

---

## THE PROTOCOL — TOP RECOMMENDATION, ONE OPTION

**Slice by FAILURE MODE, not by file or by document. Run each slice as an isolated adversarial
subagent. Reconcile against the catalog at the end.**

### Why this shape, and where it departs from Matt's sketch

**Departure 1 — chunk by mechanism, not by artifact.** The K/D-ST defect appeared in **seven
separate files**. Had the review been chunked per-file, each chunk would have seen one instance,
judged it locally reasonable, and passed it. The divide-and-conquer literature calls this **task
noise**: chunking backfires precisely when the information needed to see a defect is spread across
chunks. Slicing by failure mode keeps every instance of one mechanism inside one chunk.

**Departure 2 — I must not check my own work.** Current adversarial-review guidance is explicit
that models show self-preference and that **leniency is worst exactly where the work is wrong** —
the model that made the error is the one most likely to rationalise it. This session wrote the
pipeline, so this session is disqualified as its own checker. Each chunk therefore runs as a
**fresh subagent**: read-only, no knowledge of why the code looks the way it does, given only the
catalog rows for its slice and pre-committed pass/fail criteria.

**Kept from Matt's sketch, because it is correct:** catalog first (this is FMEA — enumerate
failure modes before inspecting), and a final coverage reconciliation. That last step handles what
the literature calls **aggregator noise** — error introduced when merging chunk results. Every
catalog row must carry a verdict from exactly one chunk; a row with no verdict is a coverage hole,
not a pass.

### Chunk sizing
6–12 catalog rows sharing one mechanism. Small enough for a focused pass, large enough that a
cross-cutting defect cannot hide between rows.

### Per-chunk contract
Input: catalog rows + file paths + pre-committed criteria. Output per row: **CONFIRMED DEFECT /
CLEAN / CANNOT VERIFY**, each with a number or a quoted line. "Looks fine" is not a verdict.
**Any fix is followed by a smoke test and a re-run of that chunk only** — never a silent patch.

### Order — by expected yield, not by pipeline order
Scoring conversion runs first because it is the least-examined and highest-leverage stage: if the
scoring map is wrong, **every** projected point total is wrong and every finding in docs 21–47
inherits the error.

---

## THE FAILURE CATALOG

### CHUNK 1 — SCORING CONVERSION (runs first)
| id | constraint to validate |
|---|---|
| S1 | The `SCORING` map reproduces this league's settings exactly: pass 0.04/yd, **6/pass TD**, −2 INT, rush/rec 0.1/yd, 6/TD, **0.5/reception**, −2 fumble lost |
| S2 | **2-point conversions** (stat 62) are scored. Open item: "204 points sit on the board unexamined" |
| S3 | Return TDs (101/102) are scored, and are not double-counted against rush/rec TDs |
| S4 | No league scoring component is MISSING from the map entirely (bonuses, first downs, sacks-taken) |
| S5 | Reconstructed points match ESPN's own `appliedTotal` within tolerance for QB/RB/WR/TE |
| S6 | The reconstruction check cannot pass vacuously on an empty stat row (the 2023 failure) |
| S7 | K and D/ST points are NOT computed from the offensive map (0% of their stats appear in it) |
| S8 | The same scoring map is applied identically to ESPN and to FantasyPros stat lines |
| S9 | Half-PPR is applied at 0.5, not 1.0 or 0 — verify against a known player's published total |
| S10 | Negative components (INT, fumble) carry the right sign |

### CHUNK 2 — SOURCE ACQUISITION
| id | constraint |
|---|---|
| A1 | Every pull filters on `seasonId` (the `top_400` defect) |
| A2 | `statSourceId` 0=actual / 1=projection never transposed |
| A3 | Hollow projection rows (only stat 210) become NULL, never 0.0 |
| A4 | ESPN ADP censoring at ~169.4 is respected — never rank inside the sentinel blob |
| A5 | Capture date present on every derived file |
| A6 | Row coverage: 700 expected; short pulls flagged |
| A7 | `--raw` cannot be applied to multiple seasons |
| A8 | Prior-year columns are null in raw mode and say so |

### CHUNK 3 — REPLACEMENT AND VBD
| id | constraint |
|---|---|
| V1 | Starter counts match the league: 1QB 2RB 2WR 1TE 1FLEX — is RB30/WR30 right given a FLEX? |
| V2 | Replacement pools exclude nulls, zeros and synthetic rows |
| V3 | K/D-ST carry no cross-position VBD |
| V4 | FLEX is priced somewhere — RB30/WR30 assumes it, but is that the right baseline? |
| V5 | Replacement recomputed per source, never borrowed across sources |
| V6 | VBD is never compared across positions using raw points (the +82-pick error) |
| V7 | Bye weeks do not enter VBD (they are a roster constraint, not a value one) |

### CHUNK 4 — IDENTITY AND JOINS
| id | constraint |
|---|---|
| J1 | Joins key on `espn_id`, never on name, wherever an id exists |
| J2 | Every join asserts its match count and fails on a drop |
| J3 | The keeper join asserts — the Etienne recurrence |
| J4 | D/ST naming handled ("Texans D/ST" vs "Houston Texans") |
| J5 | Alias table covers Jr./Sr./II/III and initials |
| J6 | No duplicate `espn_id` survives any merge |

### CHUNK 5 — BOARD ASSEMBLY
| id | constraint |
|---|---|
| B1 | All 12 keepers removed before pick 1 |
| B2 | `eff_pick` = adp_pick − keepers ahead |
| B3 | Synthetic rows never ranked |
| B4 | Injury flags surfaced, never silently scored |
| B5 | Week-14 Pickens clashes flagged |
| B6 | Ordering is deterministic and reproducible |

### CHUNK 6 — EXPORT AND INJECTION
| id | constraint |
|---|---|
| E1 | `ESPN_ID` column exact, int, no nulls, no dupes |
| E2 | Row order is the ranking |
| E3 | K/D-ST last |
| E4 | Keepers excluded |
| E5 | Player count sane vs the injector's expectations |

### CHUNK 7 — THE HARNESS ITSELF (meta)
| id | constraint |
|---|---|
| H1 | Every guard fires on the historical defect that motivated it |
| H2 | No threshold passes a known past failure (the D/ST-20 hole) |
| H3 | Failure branches print; `anomalies` is never write-only |
| H4 | Counters distinguish "present" from "non-zero" |
| H5 | `code_audit_v1.py` points at the v5 spine, not the stale one |

---

## RECONCILIATION (final step)
Every row above must carry exactly one verdict. Rows with none are coverage holes. Any CONFIRMED
DEFECT gets a fix, a smoke test, and a re-run of its own chunk — then the reconciliation repeats.

## SOURCES
- [When Does Divide and Conquer Work for Long Context LLM? A Noise Decomposition Framework](https://arxiv.org/abs/2506.16411) — task/model/aggregator noise; chunking backfires on cross-chunk dependencies
- [Adversarial Code Review: Why the Maker Shouldn't Grade the Checker](https://www.augmentcode.com/guides/adversarial-code-review) — fresh context, read-only tools, different model, pre-committed criteria, separate agent instance
- [Failure mode and effects analysis](https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis) — enumerate failure modes before inspection
