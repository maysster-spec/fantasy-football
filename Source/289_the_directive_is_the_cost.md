# 289 — THE 83% IS THE DIRECTIVE, NOT THE RETRIEVAL NOTICE
### Matt asked whether the project's context load can be reduced. Yes. The lever is one file, and the retrieval notice is not the problem — it is the correct state.
*2026-09-11. Measurement + plan. Nothing executed yet; the mirror gap in §4 must close first.*

---

## 1. WHAT THE TWO THINGS ACTUALLY ARE

**(a) "Project knowledge has grown past what Claude can read all at once, so Claude searches it."**
This is **RAG**, and it is the state we want. The doc store holds **338 docs**. Loaded whole they
would be on the order of **half a million tokens** — several times any context window. Searching
them is the only viable mode, and there is no version of "reduce it" that gets all 338 back into
every chat. **Leave it alone.** What CAN be improved is *what search returns*, which is a relevance
problem, not a size problem (see §3(2)).

**(b) The 83%.** That is this chat's own context, and the retrieval notice is not what filled it.

## 2. THE MEASUREMENT

**`00_PROJECT_DIRECTIVE.md` is 155,691 bytes ≈ ~40,000 tokens, and it is loaded into EVERY message
of EVERY chat in this project.** On a 200k window that is **a fifth of the window spent before Matt
types a word** — and it is spent again on the next chat, and the one after.

**In THIS session it was loaded twice** — once at start and once when the session context was
re-read mid-conversation — so roughly **80,000 tokens of the 83% is the directive alone.** The rest
is my own doing: one `device_list_dir` of `Source\` dumped ~290 filenames with sizes and timestamps
in a single tool result.

**And v9.2 already proved the fix works.** The changelog trim moved 20,483 characters out of this
file on 2026-09-09 without changing one rule. **The file has since grown back past where it
started.** §4 now carries the evidence, the case studies, the method notes and the retracted text in
strikethrough — all of it valuable, none of it needed in the *instructions*.

## 3. THE THREE LEVERS, RANKED

**(1) TRIM THE DIRECTIVE — the only one that pays in every future chat.** Target ~155KB → ~50KB.
Method is the changelog precedent exactly: **every RULE and every LIVE NUMBER stays in the
directive; the narrative of how it was found, the case studies, the struck-through retracted text
and the method notes move to `Source\DIRECTIVE_EVIDENCE.md`** and into the doc store, where search
can reach them when they matter.
**THE RISK IS REAL AND IT IS THIS PROJECT'S #1 HISTORICAL ERROR:** summarising a finding is how a
number drifts. `audit_directive.py` and `check_plain.py` both exist and must be run against the
trimmed file before it ships. **This is a deliberate operation with verification, not a tidy-up.**

**(2) ARCHIVE THE DRAFT-ERA DOCS OUT OF THE DOC STORE.** Docs **1–222 are pre-draft**; the draft is
over. Removing them from the project store (they stay on the drive) leaves the in-season corpus,
which is what every search should be hitting. **This does not reduce the 40,000 tokens — it improves
what RAG returns.**
**BLOCKED ON A SAFETY CHECK, AND THIS IS A LIVE DATA-LOSS RISK: the two stores are not mirrors.**
The drive's `Source\` listing jumps **78 → 92** and **241 → 245**, so roughly **16 docs
(79–91, 242–244) appear to exist in the project store and NOT in `Source\`.** They may be in
`2026\_archive\` or another folder. **`[NOT YET RUN]` — testable form: list every project doc path,
list `Source\` and `2026\_archive\`, diff on the numeric prefix, and commit every project-only doc
to the drive BEFORE a single `project_delete` runs.** A blind cleanup here destroys the only copy.

**(3) END A CHAT WHEN ITS TOPIC ENDS.** The directive cost is per-chat and unavoidable; the
*conversation* cost is not. A long thread pays for its own history on every turn. **And a folder
listing is the single most expensive cheap-looking call available** — filter it or narrow the path.

## 4. SEQUENCING, AND WHY IT IS NOT A PUNT

**The audit chat (doc 288, `IN_SEASON_REDTEAM_HANDOFF.md`) opens first, and the directive trim waits
for its catalog.** Not because the trim would remove the auditor's evidence — the numbered docs are
the evidence and they are untouched — but because **§6(1) of the charter puts the directive's own
replacement-level numbers under audit**, and a compressed §4 written tonight would bake my current
reading of those numbers into the instructions the auditor reads. **Trim after the catalog says which
§4 paragraphs are wrong, so the trim and the corrections land in one pass instead of two.**

**Order:** audit catalog → mirror diff (2) → directive trim (1). **(3) is standing.**
