# 72 — CORRECTIONS TO THE SCRATCH-PAD OPS BRIEF

**Aug 28, 2026.** Read this beside `draft_night_and_mock_ops_brief.md`.
The brief is good work and its citations are its value — these are the five places it
went stale or wrong. **Fold both into the DRAFT_DAY_GUIDE, then retire both files.**

---

## 1. §7 ITEM 1 IS CLOSED. The injector points at `Scripts\live_draft\`.

The brief was right that a mismatch existed, and right about which failure mode it was.
Settled by device read on Aug 28:

| copy | bytes | CSV_FILENAME points at |
|---|---|---|
| `...\2026\Scripts\espn_draft_injector_Gemini.py` | **4,660** | `Scripts\live_draft\` ✓ |
| `C:\Users\wmatt\OneDrive\Fantasy\Scripts\...` | **4,660** | `Scripts\live_draft\` ✓ |
| project store `claude/espn_draft_injector_Gemini.py` | ~~4,616~~ | ~~`Source\live_draft\`~~ — **was stale, now corrected** |

The brief's hypothesis — "the project-store copy is stale relative to what Matt runs" — was
the correct one. Weekend Test 1 exercises the file everyone believes it does.

## 2. §7 ITEM 3 / THE DOC CONFLICT: `Source\live_draft\` NO LONGER EXISTS.

It was verified byte-for-byte against `Scripts\live_draft\` and then **trashed on Aug 28**.
`00_HANDOVER_READ_ME_FIRST.md` has been corrected. **`00_CALENDAR_TO_DRAFT.md` and
`00_HOW_TO_RUN_IT.md` still describe it and must be reconciled in one batched edit.**

The kit is five files in **`G:\My Drive\_Fantasy\2026\Scripts\live_draft\`**.

## 3. THE PULL SCRIPT'S BARE COMMAND IS NO LONGER DANGEROUS.

The brief says: *"flags are mandatory. Bare command defaults to `[2022,2023,2024]`."*
**That describes the pre-patch script.** The current one carries:

```python
DRAFT_SEASON    = 2026
DEFAULT_SEASONS = [DRAFT_SEASON]
```

plus a `confirm_seasons()` guard that refuses a completed season unless a human types
`historical` or passes `--yes`. The flags are now belt-and-braces, not load-bearing.
Keep recommending them; stop calling them mandatory, and mention the guard so nobody
"fixes" it back.

## 4. THE SEPT 5 NEWS TASK WRITES DOC 66, NOT 64.

The brief says `claude/64_sep5_news_pass.md`. Doc 64 already exists and is
`64_aug28_pull_and_freeze_verdict.md`. The scheduled task writes **`claude/66_sep5_news_pass.md`**
(doc 65 §5.5). A guide sending Matt to doc 64 on Sept 5 sends him to the freeze verdict.

## 5. NEVER VERIFY A FILE FROM A BYTE COUNT IN PROSE — INCLUDING THIS DOC'S.

`Espn_pull_projections.py` changed **three times on Aug 28 alone**: 13,037 → 14,992 → 15,194.
Any number written in any document is a snapshot with a half-life measured in hours.
`py check_kit.py` from `...\2026\Scripts\` is the only authority. This is the project's
single most repeated failure and it has now bitten inside one working day.

---

## WHAT THE BRIEF GOT RIGHT AND SHOULD SURVIVE INTO THE GUIDE

- The reconciled date-ordered action list (§1).
- Both mock modes with corrected syntax, and the honest limits of a public mock (§2) —
  especially that it has no keeper depletion, which is this league's defining feature.
- The five engine output columns and what each means (§3).
- **"The tool is advisory only — it never clicks or types anything into ESPN."** That belongs
  near the top of the guide.
- The override-is-free point: just pick who you want in ESPN's room; the next poll re-plans.
- Test 1/2/3 pass-fail detail (§5), including the 512 silent failure and the
  `(0 flagged keeper)` stop condition.
- Team ID = 9 unconfirmed (§4) — still open, still Matt's.

## ONE THING TO ADD THAT THE BRIEF DOES NOT COVER

**There is no offline fallback.** If `live_draft.py` dies at pick 41, nothing on paper tells
Matt who to take. The FALLBACK_BOARD artifact — top ~180 of `board_v8_fixed.csv` by vbd,
printed — closes that, and it costs one print job.
