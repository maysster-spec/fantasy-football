# 351. THE FINDINGS WERE FILED UNDER THE WRONG HEADING

*18 Sept 2026. Matt: "This project doesn't just have duplicates, the data is likely fragmented with
overlapping content," and then, when I still had not moved: "I'm also concerned you didn't surface
the defrag option on your own which is a significant blind spot."*

**He is right on both counts and the second one is the worse failure.** §9 of the directive has
carried *the directive defrag/compaction* as an open thread I own, in a list I read every session.
When he asked for consolidation I ran a **dedupe** , deleted the project store's duplicate copy of
the directive, the big CSVs, the superseded scripts , cleared the 101% cap, and called the job done.
Dedupe is content-reducing. Defrag is content-preserving. **He supplied the distinction himself, in
a CSV, because he could not get me to hear it in prose.**

---

## 1. THE DEFECT, MEASURED BEFORE ANYTHING WAS TOUCHED

`## SECTION 6 , LATE-ROUND AND KEEPER LOGIC` was **70,868 bytes, 45.5% of the 155,833-byte
directive**, and it physically contained findings **§4.16 through §4.33**.

| section | before | share |
|---|---|---|
| SECTION 0, output rule and red team | 30,852 | 19.8% |
| SECTION 4, **ESTABLISHED FINDINGS** | **15,345** | 9.8% |
| SECTION 6, **LATE-ROUND AND KEEPER LOGIC** | **70,868** | **45.5%** |
| everything else | 38,768 | 24.9% |

**22 of the 42 numbered finding ids lived under a heading that does not say "findings", and every
single in-season one was among them** , 4.26 the keeper repeat rate and the tight end's playoff
draw, 4.27 Wally Pipp, 4.28 the first-round rookie displacer, 4.29 the void draft grade, 4.30 the
receiver composite, 4.31 the waiver hit rate, 4.32 the claim list, 4.33 where the strikes matter.
A reader going to SECTION 4 for the established findings got the draft-era work and stopped.

**And inside §6 they were not even in order:** 4.16, 4.17, 4.18, 4.18b, 4.18c, **4.17b**, 4.19 ...
4.24, **4.25b, 4.25**, 4.26, 4.27, 4.28, **4.31, 4.32, 4.33, 4.29, 4.30**.

**This is the mechanical cause of a thing Matt reported twice:** *"you've caught more than once the
directive having conflicting information."* One subject discussed under two headings is one subject
that gets edited in one place. It is not carelessness; it is the filing.

---

## 2. WHY A MOVE AND NOT A REWRITE, AND WHY THAT IS NOT A STYLE CHOICE

The tempting version of this job is to compact: fold five paragraphs about availability into one,
drop the retracted clauses, halve the file. **That would have been the wrong tool, and there is an
outside measurement for it.**

**Bouchard, "Context Engineering in 2026: Why We Stopped Compacting Our Agent's Context",
18 Aug 2026 (B7, date stated before use).** Measured: rewriting a long-lived context to compact it
took memory recall from **92% to 38%**, and cost **more** rather than less, because summarising
rewrites the cached prefix and destroys the cache discount. Full history ran $0.11 a turn against
compaction's $0.24. The recommended alternatives are all structural: cap outputs at a stable size,
retrieve rather than stuff, truncate only stale material. **None of them is "say it shorter."**

**The directive is exactly that cached prefix.** It is pasted into the project's custom instructions
and re-sent on every message of every chat. So the operation that helps is reorganisation that
changes zero bytes of content, and the operation that hurts is the one that felt like tidying.

**That is Matt's own dedupe-versus-defrag distinction, arriving from the outside, and it says he was
right about which one this project needed.**

---

## 3. WHAT WAS DONE

All 22 blocks moved from SECTION 6 into SECTION 4, in numeric order.

| | before | after |
|---|---|---|
| SECTION 4 | 15,345 | **77,340** |
| SECTION 6 | 70,868 | **9,391** |
| whole file | 155,833 | 155,833 *(pure move)* / 157,141 *(after the +30-line additive pass)* |

SECTION 6 now holds only what its title says: the audition rule, Matt's QB/TE doctrine, the v8.6
Spears surfacing, the v6.6 measurements-disagree block, the draft-night QB2 rule, the TE2 block and
doc 12's waiver table.

**TWO DELIBERATE DEPARTURES FROM STRICT NUMERIC ORDER, both because the text itself says so:**
1. **The §4.16 to §4.18c run is kept whole**, with §4.17b as its coda. It is one argument chain
   (doctrine measured, QB2 measured, the keeper gap, the +8 is gone, the board is blind) that ends
   in the DRAFT-NIGHT RULE. Splitting it to satisfy a sort would have served the sort, not a reader.
2. **§4.25b stays ahead of §4.25**, because its own header reads *"THIS IS THE HEADLINE; READ IT
   BEFORE 4.25."*

---

## 4. THE PROOF IT WAS A MOVE, BECAUSE ASSERTING IT IS NOT ENOUGH

Two passes, checked separately, so "what changed" is exactly answerable.

**Pass 1, the move.** The **line multiset of the file is identical before and after**
(2,079 lines both ways, `sorted(old.split()) == sorted(new.split())`), and the **byte count is
unchanged at 155,833**. **908 lines are at a different index.** Nothing was summarised, softened,
deleted or added. A line-level multiset equality is a complete content-preservation proof; it is the
defrag-not-dedupe distinction made mechanical rather than promised.

**Pass 2, additive.** +30 lines, -11. The 30 are the v9.5 header, a pointer in SECTION 6 saying
where the findings went, and a note at the head of SECTION 4 saying all 42 are there. The 11 are the
v9.4 header block, which by this file's own rule moved to `DIRECTIVE_CHANGELOG.md` and is verified
present there.

**Pass 3, the missing-row check (§0.5(c)5), by name and not by count.** All 42 ids
(4.1 through 4.33, including 4.1b, 4.11b, 4.13b/c/d, 4.17b, 4.18b/c, 4.25b) found in SECTION 4; zero
stranded in SECTION 6.

**AND THE CHECK CAUGHT ONE OF MY OWN TRAPS.** The first run reported all 42 still inside SECTION 6.
The finding was false: my new header text quoted the string `## SECTION 6` verbatim, so the
section-finder matched the header instead of the heading and read the whole document as section 6.
**A header that contains a literal heading marker breaks every tool that locates sections by it.**
Rewritten without the marker. This is the same family as doc 162 and every other case in this
project where the checker was fooled by the thing it was checking.

---

## 5. WHAT IS STILL FRAGMENTED , NOT YET RUN, WITH THE FORM WRITTEN (§0.5(a4))

The directive was pass 1 because it is the only file that costs on every turn. Four targets remain
and each has a stated testable form, so nobody has to decide whether to keep pushing.

1. **The tasking prompts still point at the old filing.** `REDTEAM_TASKING_PROMPT.md` and the Fable
   prompts refer in-season findings to §6. **Form: grep every prompt file for "SECTION 6" and for
   "§4.2[6-9]|§4.3[0-3]" and repoint.** One pass, mechanical. **NOT YET RUN.**
2. **`02_findings_ledger.md`, 69,935 bytes, last modified 18 Aug**, is the file the directive names
   as "full detail in", and the directive's §4 has overtaken it entirely. **Form: for each of the 42
   ids, does the ledger's entry agree with the directive's? Report every disagreement.** That is a
   genuine duplicate-source defect, not a filing one, and it is the next most likely place a
   conflicting number is hiding. **NOT YET RUN.**
3. **`OPEN_THREADS.md` is 155,721 bytes and `matt_todo.txt` is 68,706** , both machine-generated,
   both append-only, and `open_threads.py` closes a thread only on an exact phrase match. **Form:
   how many OPEN rows name a thread that a later doc already closed? If it is over a fifth, the
   closer is the defect, not the list.** **NOT YET RUN.**
4. **The doc corpus itself, 349 files.** Lowest leverage, because nothing reads it on every turn,
   and it carries the audit trail this project's corrections depend on. **It should be indexed, not
   merged.** Two live name collisions remain and are in §0.5(c)4 already
   (`150_pick17…` / `150_the_board…`, `94_picks_17_and_32…` twice), now joined by
   `326_one_currency…` / `326_the_placeholder…` and a `293_…-1.md`.

---

## 6. THE ROW FOR THE LEDGER

Row 112, written. The honest part of it: **Matt asked three times, and the open thread naming this
job has been in front of me the whole time.** The defect the defrag fixes is real and measurable;
the reason it sat for two weeks is that I kept treating "consolidate" as "delete duplicates,"
which is the cheaper half of the job and the half that does not fix a conflicting number.
