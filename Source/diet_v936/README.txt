diet_v936 -- the proposed v9.36 directive, the second diet (doc 447; batch six of the to-do list).
APPLIED 29 Sept 2026, 22:50 ET, on Matt's go (doc 452). The live files are v9.36; this folder is the record of the proposal
and its proof. One correction before it shipped: the directive header said thirty-five passages, the count is thirty-three.

what is here
  00_PROJECT_DIRECTIVE.md   the proposed v9.36: v9.35 with thirty-three story passages tagged v9.12 and earlier moved
                            out; two rule sentences corrected in WHERE THINGS LIVE (the proof standard is the word
                            multiset with the rewrites reversed; the findings count is 50); two short deletions listed
                            as rewrites (a stale to-do inside 0.5(a2), a v5.3 note in the section 9 table)
  DIRECTIVE_CHANGELOG.md    the proposed changelog: a v9.36 entry at the top, the thirty-three passages verbatim at the foot
  directive.diff            what changes in the directive, line by line (unified diff, v9.35 -> v9.36)
  changelog.diff            what is added to the changelog (additions only)
  diet_check.py             the proof, generalised at doc 447: every word of the base is in the proposal or in the moved
                            passages, the listed rewrites reversed; --selftest deletes a word and a passage and shows
                            the check fire. Standard library. Reads the base and new versions from proposed_meta.json.
  proposed_meta.json        the rewrites and the moved passages, read by diet_check.py

what stayed on purpose: every rule sentence; every canonical example beside a rule (Matt's quoted words, the one-line
cases such as MarShawn Lloyd and Spears against Mike Washington); the retraction table; the evidence lines a rule
rests on (the 44% / 21% take count, the 12-1-7 count of his mechanisms, the receiver composite's four cells).

to apply (Claude does this on your go): archive the two live files to _archive, copy the two proposed files over
them, push both to the store, run py check_citations.py and py check_inputs.py, then you paste.

the price: 87,461 bytes -> 79,906 (8.6% smaller); with v9.35 already applied, the every-turn read is down from
99,049 to 79,906 since this morning, 19.3%, about 4,800 tokens a turn on the bytes-over-four estimate this project
uses (24,800 -> 20,000). The changelog grows by 10,938 bytes and is read only when someone asks why a rule exists.
