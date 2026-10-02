diet_v935 -- the proposed v9.35 directive, batch four of the to-do list (doc 444; doc 435 batch D), extended by doc 445.
NOT APPLIED. The live files are unchanged. This folder is the proposal, for Matt to read and say go or no.

what is here
  00_PROJECT_DIRECTIVE.md   the proposed v9.35: v9.34 with thirty story passages moved out, three index rows rewritten
                            to carry no numbers (4.35, 4.36, 4.38), row 4.42 added (doc 445), one rule sentence changed
                            (claim order: FILLING, was BLOCKED)
  DIRECTIVE_CHANGELOG.md    the proposed changelog: a v9.35 entry at the top, the thirty passages verbatim at the foot
  directive.diff            what changes in the directive, line by line (unified diff, v9.34 -> v9.35)
  changelog.diff            what is added to the changelog (additions only)
  diet_check.py             the proof: every word of v9.34 is in v9.35 or in the moved passages, the listed rewrites
                            reversed; --selftest deletes a word and a passage and shows the check fire. Standard library.
  proposed_meta.json        the rewrites, the inserted row and the moved passages, read by diet_check.py

to apply (Claude does this on your go, doc 444 item 1): archive the two live files to _archive, copy the two
proposed files over them, push both to the store, run py check_citations.py and py research\audit_directive.py,
then you paste the new 00_PROJECT_DIRECTIVE.md into the project's custom instructions.

the price: 99,049 bytes -> 87,461 (11.7% smaller; 86,935 before doc 445 added the 4.42 row); the every-turn read
falls by about 2,900 tokens on the bytes-over-four estimate this project uses (24,800 -> 21,900). The changelog
grows by 17,650 bytes and is read only when someone asks why a rule exists.
