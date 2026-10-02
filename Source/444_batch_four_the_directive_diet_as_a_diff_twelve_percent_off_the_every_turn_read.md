# 444. BATCH FOUR: THE DIRECTIVE DIET AS A DIFF, 12% OFF THE EVERY-TURN READ, EVERY WORD ACCOUNTED FOR, AND NOT APPLIED

*29 Sept 2026, evening. Claude (Cowork), batch four of "complete the to do list... in batches to ensure fidelity", which is
doc 435's batch D ("propose the cut as a diff for Matt, not an applied edit; price the paste: tokens per turn before and
after"). 444 reserved by listing `Source\` at 19:30 ET. No em dashes.*

> **Extended the same evening by doc 445:** the proposal now also rewrites the 4.38 index row (its numbers are in the
> findings file) and adds row 4.42; the price is 99,049 to 87,461 bytes, 11.7%, about 2,900 tokens a turn. The
> figures below (86,935; 12.2%; two rows) are as first written. The folder and its README carry the current ones.

---

## 0. WHAT TO DO

1. **Matt: read `Source\diet_v935\directive.diff` (378 lines) and say go or no.** On go I archive the two live files, copy
   the proposal over them, push the store, run the citation and directive audits, and you paste v9.35. Nothing is applied
   tonight: the audit prompt asked for a diff, not an edit, and the directive is the one file every session reads.
2. **The price: 99,049 bytes to 86,935, 12.2% smaller, about 3,000 tokens a turn off every turn of every chat**
   (24,800 to 21,700 on the bytes-over-four estimate this project has used since doc 367; a tokenizer was not reachable
   from here, so the figure is an estimate and labelled one). Doc 435 sized the cut at about 16 KB and 4,000 tokens; the
   measured cut is 12 KB, because the §2 passages that carry the standing waiver and IR instructions stayed.
3. **What moved: thirty passages, 11.1 KB, tagged v9.13 to v9.32, verbatim, to a new section at the foot of
   `DIRECTIVE_CHANGELOG.md`, each labelled with the rule it belongs to.** §2 gives up fifteen (5.3 KB: the v9.15 preamble,
   your quoted mechanic, the retracted Sunday rule and its story, the misreading story, your words on the sourcing, the
   "what this corrects" list, the seat-curve narrative and the three retracted numbers the DO-NOT-QUOTE table already
   carries, the degenerate claim-order statistic, the 6.1%, a dated roster count, your kicker question); §0.5 gives up
   seven (3.2 KB: the em-dash case, the 4.36 narrative and its tone example, the Worthy case, the streaming-QB case, the
   six-days-stale story and the tracker's explanation); §9 gives up seven (2.4 KB: the doc 417, doc 392 and 134-edit
   stories, the header's history and its outside citations, "the part that is mine"); §1.1 gives up the struck registry
   sentence. Every rule sentence stayed where it was.
4. **Two index rows are rewritten, not moved: 4.35 and 4.36 carried 38 numbers between them in an index that says of
   itself "the index carries no numbers on purpose".** Every one of those numbers is in `DIRECTIVE_FINDINGS.md` (checked by
   script; the one miss, 395, is a doc number in the docs column). The old rows sit verbatim in the changelog.
5. **One rule sentence changes, and it is the only one: §2's claim-order line reads FILLING since doc 442 instead of
   BLOCKED**, because `claim_order_log.py --pair` records the input the BLOCKED line named. That is why the proposal is a
   version (v9.35) and not a tidy.
6. **The proof runs on your machine: `py Source\diet_v935\diet_check.py`.** Every word of v9.34 is in v9.35 or in the moved
   passages once the listed rewrites are reversed (17,088 words before; 14,992 in v9.35 plus 1,911 moved, the difference
   being the rewritten header, rows and one line, all listed in `proposed_meta.json`). `--selftest` deletes one word from
   the proposal and one passage from the changelog and shows the check fire on each.
7. **Nothing to run.** The proposal is on the drive; the live files are untouched; `claude_todo.txt` closes batch D and
   `matt_todo.txt` carries the decision.

---

## 1. THE RULE OF THE CUT

RULE is a sentence a session must obey; STORY is how it was found. Doc 435 classified nine blocks; this doc cut at the
sentence, not the block, because in this file the two are interleaved inside paragraphs (the (e) mirror rule sits between
the six-days-stale story and your quoted question). Where a passage carried both, the rule sentence stayed and the story
moved; where a story sentence was the only concrete example of its rule (the Spears block, (a2)'s record of your calls,
the doc 291 seat cases), it was left alone, because that is what the outside read below says an example is for. The
DO-NOT-QUOTE table is untouched: a retraction is actionable (0.1) and stays resident; what moved is the account of how
each retraction was found, which the table's right column does not need.

Cutting inside a paragraph means the line multiset (doc 367's proof) no longer applies; the proof here is the word
multiset with the rewrites reversed, which is stricter about content and silent about line breaks. Six markup repairs were
needed where a cut left a bold span open, a bracket orphaned, a full stop missing or a leading space behind; each is a
listed rewrite and each is reversed by the check.

## 2. THE OUTSIDE READ (0.5(c)6)

Anthropic, *Effective context engineering for AI agents*, published 29 Sep 2025, read as page text: the aim is "the
smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome"; "context rot: as the
number of tokens in the context window increases, the model's ability to accurately recall information from that context
decreases"; the right altitude for a system prompt sits between "hardcoding complex, brittle logic" and "vague, high-level
guidance"; and on examples, "for an LLM, examples are the 'pictures' worth a thousand words", with "a set of diverse,
canonical examples" preferred to "a laundry list of edge cases".

Where we agree: the cut is that guidance applied, and §9 rule 7 already cites the same page. Where we differ on purpose:
the directive keeps one canonical case beside most rules (your own words, quoted), because the case is what makes the rule
concrete for a reader who was not there; the diet moves the narrative of the finding, not the example. Where we differ by
accident, and it is out of this batch's scope: the v9.12-and-earlier material was never classified this way, and SECTION 0
is still 38 KB of an 87 KB file (41.5 KB of 99 KB before). A second batch on the older blocks would be the same operation with the same proof.

## 3. WHAT IS IN THE FOLDER

`Source\diet_v935\`: the proposed `00_PROJECT_DIRECTIVE.md` and `DIRECTIVE_CHANGELOG.md`, `directive.diff` (135 lines
removed, 31 added), `changelog.diff` (additions only, 224 lines), `diet_check.py` with `--selftest`, `proposed_meta.json`,
and a README saying how it is applied. The changelog grows from 96,782 to 114,073 bytes and is read only on demand.

## 4. OPEN, BY NAME

- **Matt's:** go or no on v9.35 (`matt_todo.txt`); the two claim-order runs each week; the routes purchase; the ESPN D/ST
  box score.
- **NOT YET RUN:** a second diet batch on the v9.12-and-earlier blocks, same operation, same proof, if the first is
  accepted; the practice report's Out as `next_man_up()`'s trigger; the rise on an eight-week horizon (4.38); the 4.34
  column from week 10; the trim of the other three pages (doc 439); the Wednesday and 6 October runs (doc 439).
- **BLOCKED on Matt:** the prior Opus research chat.
