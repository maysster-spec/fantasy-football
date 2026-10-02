# 398 — The handover was three versions stale, and the changelog had no entry for any of them

*23 Sept 2026. Doc 397 batch A, worked in the order Matt set. Directive v9.20 → v9.21, `00_START_HERE.md`
version 11 → 12, `DIRECTIVE_CHANGELOG.md` gains four entries. All three verified on the drive by content hash.
Ledger row 173.*

---

## 1. WHAT THIS BATCH WAS

Matt, 23 Sept: *"worth a review and a red team. We have updated 10x since the last fable run."* The catalog
shipped first on its own (doc 397, §0.5(c)1) so he could see the shape and re-order it. He did not re-order it:
*"work the suggested order."* Batch A is the one the catalog called the batch a fresh chat pays for — **the
resident set disagreeing with itself.** Five items, all CONFIRMED, all fixed. Two were worse than the catalog
said and one is new.

**None of this is a measurement.** Batch A is a consistency pass over files this project wrote in the last
twenty-four hours. The only number it touches is one it removes.

---

## 2. A2 — THE HANDOVER WAS THREE VERSIONS STALE. THIS IS THE ONE THAT MATTERED.

`00_START_HERE.md` was last written 22 Sept 20:00 and carried **zero occurrences** of `SSPD`, `"NOT invalid"`
or `"Questionable or Doubtful"` — the three strings that carry everything v9.19 established. Section 2 still
told a fresh session:

| what the handover said | status since v9.19, sixteen hours earlier |
|---|---|
| *"ruled Out then upgraded in-week ... flips any day, Monday included, and nothing on a schedule protects you"* | **WRONG.** An upgrade to Questionable or Doubtful is explicitly SAFE and it is the most common upgrade there is |
| *"19.5% are downgraded to Questionable, seat gone, nothing gained, and that is the most common way it fails"* | **WRONG.** The roster stays valid and he keeps the seat |
| *"Safe at any placement day: NFL injured reserve, suspension/PUP/NFI"* | **WRONG for suspension** — *"Suspended players (SSPD) are NOT eligible for IR on FFL."* PUP and NFI are not addressed by that page either way, so NOT ESTABLISHED |
| *"Still BLOCKED: which ESPN designations this league accepts"* | **CLOSED** at doc 394 |

**This is the file a new chat reads first.** For sixteen hours the handover was the worst-informed file in the
project, and every one of those four had been retracted in the directive sitting beside it. Section 2 is
rewritten from the sourced rules, the four wrong versions struck in place so the reversal is legible rather than
silently absent, and the drop rule (884 for 884) and the claim-ordering rule are carried across from docs 393
and 396, neither of which had ever reached this file either.

**Its own version stamp said *"the directive is v9.13"*** while the file had been edited eight versions later.
Bumped to 12, with the rule written into the stamp: bump it in the same commit as any edit.

---

## 3. A1 — §2 CARRIED THE DEAD READING ELEVEN LINES BELOW THE CORRECTION THAT KILLS IT

v9.19 struck the quiet-failure reading in §2's corrections list (line 669) and left it asserted in §2's
seat-life paragraph (line 686). Same section, same file, eleven lines apart. A reader reaching the table got the
retracted version.

**§9 rule 5 says a retraction must reach the SOURCE doc. This is its sibling and it is a harder miss: a
retraction must reach the whole of the file it is written in.** When the correction is right there, the eye
reports the file as corrected.

Struck at the second site, pointing at the first — and the strike is what exposed D1 below, so it is not
cosmetic.

---

## 4. A4 — THE CHANGELOG HAD NO ENTRY FOR v9.18, v9.19 OR v9.20

The catalog called this a stale pointer. It is not. **Three versions had no history at all.**

`DIRECTIVE_CHANGELOG.md`'s own preamble states the rule: *"any edit to the directive bumps its header line in
the same commit"* and *"a new entry goes at the TOP of this file."* **Broken three times in one day, by me,
while the directive's header grew four nested bracket blocks carrying the same material in a register nobody
can search** — which is batch B and is exactly what Matt noticed unprompted.

The three entries are written from `AUDIT_LEDGER.md` rows 170, 171 and 172, which recorded every one of them
correctly at the time. **The record was kept and the history was not.** That is §0.5(f) in its own words: the
ledger is the RECORD, it is not the FIX. Nothing was reconstructed from memory; where the ledger quotes Matt,
the entry quotes the ledger.

Pointer: *"v5.4 through v9.14"* → *"v5.4 through v9.21"*, now true.

---

## 5. A3 — THE FINDINGS COUNT, AND A DEFECT OF MINE CAUGHT BEFORE IT WAS PUBLISHED

Stated **42** in the WHERE THINGS LIVE block and **43** in SECTION 4, against **45** index rows. Both now say 45.

**In the same pass a reconcile flagged eight index ids as having no body in `DIRECTIVE_FINDINGS.md`.** That
would have been a serious missing-row finding. **It was my regex.** The findings head as `4.15`, not `§4.15`,
and the pattern required the section mark. Checked before it went anywhere (§0.2: reproduce the failure first);
**all 45 have bodies.**

One real dangling reference survives and is **[OPEN], mine**: `§4.23a` is cited inside the findings file and
has no index row and no body.

---

## 6. A5 — NEW, NOT IN THE CATALOG: A NUMBER NOBODY HAD EVER SOURCED, LOAD-BEARING FOR A PROTECTED CATEGORY

§0.4 lists the four things that stop and ask every time. The first reads: **a waiver claim spends one of two
runs that week.** The handover said it twice, and one of those two sites **flagged it itself**: *"The run
count, two a week, is Matt's own and has NOT been checked against ESPN."* Flagged, and never run down.

**It is wrong.** `2026_League_Settings.txt`, read in full:

```
- Player Acquisition System: Waivers
- Season Acquisition Limit: No Limit
- Waiver Period: 2 Days
- Waiver Order: Reset Each Week to Inverse Order of Standings
```

**There is no run-count line at all**, and no acquisition limit. ESPN's own page, already quoted in doc 396 and
never carried back into the rules, says waivers are *"typically processed daily around 3:00 AM ET."*

**So there is no two-run week.** A claim matures at D+2 and processes at the next daily run — which is what
§2's D+2 table has said since v9.15. **The two statements were in the same file and disagreed**, and the D+2
table was the one with a source.

**What a winning claim actually spends is his waiver PRIORITY for the rest of that week.** ESPN: the winner
*"will move to the end of the waiver order"*, mid-run. The settings: the order resets weekly. That is scarcer
than a run, not looser, **so §0.4's protection is unchanged and better founded than it was.** The reason
changed; the rule did not.

---

## 7. WHAT THIS OPENS

- **D1, next, and the handover already carries a do-not-quote marker on it.** The seat-life numbers count
  *"takes a snap in w+1"* as the seat dying. By the rules sourced at v9.19 **the seat does not die on a
  Questionable downgrade**, and it may not die on him playing either — the slot's occupancy is decided by the
  designation, not by snaps. If that is right the measured event is the wrong one and **the seat lasts longer
  than §2 says**, in the conservative direction. *"The median seat dies between two and three weeks"* is not to
  be quoted until it is re-run.
- **§4.23a**, cited and bodiless.
- **Batch B**, the header accretion Matt noticed on his own (*"i don't recall seeing system directive structured
  this way"*), with B3's outside read on published practice for changelog placement and preamble length.

---

## 8. PROVENANCE

Three files archived to `2026\_archive\` with a `_20260923_0752` suffix before anything was overwritten,
committed from a fresh container path, `expectedMtimeMs` passed on all three, **then staged back and compared by
CRLF-normalised sha256 — content, never the commit result** (§9 rules 1 and 2):

| file | bytes | sha256[:16] |
|---|---|---|
| `00_PROJECT_DIRECTIVE.md` | 82,719 | `13b53531f1fee823` |
| `00_START_HERE.md` | 27,485 | `7a845f68c698fbb8` |
| `DIRECTIVE_CHANGELOG.md` | 63,644 | `f580396bb83fdab7` |

All three mirrored to the project store. `DIRECTIVE_CHANGELOG.md` was re-staged immediately before editing and
confirmed byte-identical to the copy the edit was built from (§9 rule 3); no other session had touched it.

Every edit asserted its own occurrence count before applying and the residuals were counted after (§9 rule 6):
`two runs` 0 live, `42 findings` 0, `43 findings` 0, quiet-failure assertion gone, `SSPD` present in the
handover for the first time.
