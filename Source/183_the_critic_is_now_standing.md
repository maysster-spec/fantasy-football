# 183 — The critic is now a standing job, and three controls had gone stale

**2026-09-05, night (T−2).** Matt: *"add as standard that I need a critic, and someone to red team
my assumptions... don't let my prior directives compete with better outcomes, always challenge me.
I much rather be proven wrong and get us right."* And: *"I do find myself asking for your red team
work and I have to prompt you for it. is there anything you could do to bake routine check after
certain milestones?"*

Checked what already exists before adding anything, because he explicitly asked me not to duplicate.

---

## 1. What already existed, and what genuinely did not

**Already in §0.2, and being followed:** an exit code is not a result · the folder-listing rule
before writing a new file (collision) · a diagnosis is a claim, test it before writing the fix · a
guard that has never been executed is not a guard · test the object PRODUCTION builds · profile,
do not reason. **His memory that we defined controls for "thinking a job is done when it isn't" is
correct — that is §0.2's doc-146 block, and it is intact.**

**Genuinely missing, and now added as §0.5:**
- **No standing instruction to challenge HIM.** The directive is thorough about testing *my* claims
  and says almost nothing about testing his. `ERROR_PATTERNS` **F4** — *"his instinct has a track
  record, treat it as evidence"* — arguably tilts the other way, and §6 until today literally said
  *"do not argue him out of it."*
- **No stated red-team METHOD.** Catalog-first, batching and the closing overview have been ad hoc
  in every session, including this one.
- **No MISSING-file check.** §0.2 catches a thing that should not exist. Nothing catches a thing
  that should exist and does not — which is precisely how **MarShawn Lloyd sat at rank 184 against
  a 180-row printed cut with no guard firing.** Matt found it, not the machinery.
- **No milestone triggers at all.** Nothing in the project says "after X, run Y without being asked."

## 2. §0.5, in five parts

**(a) What to challenge.** The bar is *would being wrong here change a pick, a file, or a number
someone acts on?* If no, let it go — he has said other models cost him time over trivia and it is
the fastest way to make the challenge worthless. **And doc 181 says where to aim: a price or a
process he calls wrong is EVIDENCE; a causal mechanism he proposes is a HYPOTHESIS.**

**(b) A preference of his that a measurement contradicts gets SURFACED at the moment it binds** —
not obeyed silently, not overridden silently.

**(c) The method, his words:** catalog first · batch, sized to finish · overview at the end of each
batch · **collision check** before writing any file · **missing-row check** after any build that
produces paper.

**(d) Six milestone triggers that fire unprompted**, each naming what runs — board rewrite,
directive edit, research batch close, artifact rebuild, milestone date, and any claim of completion.

**(e) Name the dropped threads at the end of every session that produced more than one doc.** Not
"some things remain." The names.

## 3. THE OPEN THREADS, BY NAME — the first run of §0.5(e)

**Waiting on Matt (his machine, §0.4 items 1–2):**
1. `py apply_research.py --findings ..\Source\redteam_sept5.csv --write` — **38 verified facts, not
   yet on the cards.**
2. Rebuild the paper (`make_board` → `mkvalue` → `to_pdf` → `sync_desk_copies`), then `py check_kit.py`.
3. `py make_shortcuts.py` — the **12 - Draft board grid** desktop link still does not exist.
4. `py fetch_keepers.py --dry` — **now the ONLY untested item in §8** (see §4).

**Open questions, no owner:**
5. **The pick-8 margin.** 7.8 and ~20 disagree, both single-state (doc 182).
6. **Does ESPN's IR slot accept reserve/PUP?** Decides whether Charbonnet is a free stash.
7. **Wan'Dale Robinson's ESPN QUESTIONABLE** has no source behind it — check the app Sunday.
8. **Carolina's lead back.** Genuinely unsettled; will stay that way past the draft.
9. **32 AVOID/DISCOUNT rows** between his picks, still on their Aug-31 stamp. Post-draft.

**Housekeeping, low risk, still real:**
10. **Two live doc-number collisions in `Source\`** — `150_pick17_in_dollars.md` /
    `150_the_board_does_have_a_builder.md`, and `94_picks_17_and_32.md` /
    `94_picks_17_and_32_2322.md`. The rule that forbids these is in §0.2 and the files predate it.
11. `redteam_batch2.csv` is superseded by `redteam_sept5.csv`.
12. `after_pull.bat` is a stub and can be deleted.
13. **`ERROR_PATTERNS` F4 should be split** into pricing/process instinct (evidence) versus
    mechanism hypothesis (hypothesis). Post-draft.
14. **`_lineup` has no absence model** and `refresh_proj.py` is quarantined. Both explicitly post-draft.

## 4. Three controls had gone stale. Two are fixed tonight.

**(i) §8 claimed the live-feed replay was untested. It PASSED on Sept 4** — doc 163, 08:51 EDT,
180 rows fetched with 12 flagged keeper, 181 renders, no traceback, guard silent. **The entry sat
there for two days saying otherwise.** Corrected: `fetch_keepers.py --dry` is the only one left.
This is the exact failure §0.5(d)'s last row now guards.

**(ii) Sunday's 9:00 AM sweep was armed against a brief written before four red-team batches.** It
would have told a fresh session to start numbering at 169 (183 is used), to re-research Love,
Egbuka, Jeanty, Kittle, Henderson, LaPorta and Judkins (all done Sept 5), to treat Kittle's sources
as unresolved (resolved — the card's "age 38, out right now" was wrong on both counts), to chase
Kyler Murray as the QB2 answer (it is Bo Nix), and to quote pick 8's retracted 20-point margin.
**Rewritten.** It now carries the settled states, the three corrected grades, B7's date rule, doc
166's two-source rule, an explicit "do not touch the board or the cards at T−1", and a scope of
**six names, then stop.**

**(iii) `audit_directive.py`'s expectations were hand-copied constants** — fixed earlier tonight
(doc 180). It now parses §4.14's numbers out of the directive. **51 ok, 0 FAIL after all of
today's edits.**

## 5. Standing

`[SHIPPED]` — §0.5 added; §8's stale claim corrected; the Sunday brief rewritten; `audit_directive`
still green.
`[NOT DUPLICATED]` — checked §0.2 first; the exit-code and collision controls already existed and
were left alone. §0.5 cites them rather than restating them.
`[OPEN]` — everything in §3, by name.
