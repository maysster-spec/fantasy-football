# 369. THE COMMANDS PAGE HAD ELEVEN CSS RULES THAT NEVER APPLIED, AND TWO LINKS THAT RESOLVED INTO THE WRONG FOLDER

*19 September 2026, early hours ET. Batch 1 of the page red team Matt asked for on 18/19 September.
Everything below was measured on the files as committed and verified by hash after the commit, not by
the commit result (SECTION 9 rule 1). Doc 368 is the previous number; 369 reserved by listing the folder
first. Matt's instruction for this work: "Redesign from ground up if it makes sense to do so. A redesign
will need to be done properly though and in batches so i can hit next."*

---

## 0. WHAT TO DO

1. **Matt: run `.\ff.bat`.** It is on your list. Nothing on this page is visible until it runs, because
   every fix here is in the GENERATORS, not in the generated pages.
2. **A live defect, and it is the reason the commands page looks wrong: eleven CSS rules ship as
   literal `{{ }}` and have never once applied.** Its tables, its batch boxes, its step lists and its
   monospace sizing have been unstyled since the page was first generated. Fixed. Section 2.
3. **Both broken commands links had one cause and it was not a bad choice, it was a relative path.**
   A link written `COMMANDS.html` on a page that lives in `Source\` resolves to `Source\COMMANDS.html`.
   Fixed in both places to `../COMMANDS.html`. Section 1.
4. **The copy button is back**, on all ten commands, and it copies over `file://` where the modern
   clipboard call is refused without saying so. Section 3.
5. **Jump links exist now**, on all three pages, and they stick to the top of the window rather than
   scrolling away. Section 4.
6. **Cross-page links open in a new tab and the to-do page has a way back.** Both halves of the fix
   Matt offered, because they solve different halves of the problem. Section 4.
7. **BATCH 2 AND BATCH 3 ARE NOT DONE AND ARE DESCRIBED IN SECTION 6**, so the next session starts
   there rather than re-deciding it.

---

## 1. THE TWO DEAD LINKS: ONE CAUSE

`WEEK_SHEET.html` and `MY_TODO.html` both live in `Source\`. Both linked to `COMMANDS.html` with no
path, which the browser resolves against the page's own folder:

```
Source\WEEK_SHEET.html  +  href="COMMANDS.html"   ->  Source\COMMANDS.html    the dead stub
Source\MY_TODO.html     +  href="COMMANDS.html"   ->  Source\COMMANDS.html    the dead stub
                                                       the live page is at  2026\COMMANDS.html
```

Both now read `../COMMANDS.html`. Verified in the rebuilt to-do page: two occurrences of
`../COMMANDS.html`, zero of the bare form.

**AND THE STUB THEY LANDED ON WAS A DEAD END, WHICH IS THE PART THAT DESERVED THE COMPLAINT.** It
printed the live path as *text* and offered no link at all, so the only way out was to read a Windows
path off the screen and retype it. Matt: *"The redirect page doesn't have a hyperlink the the new
commands page."* Correct. It is now a signpost with the live page as the primary link, the pre-draft
console as **archived draft commands** (his words, and the file is real:
`_archive\COMMANDS_Source_20260918_predraft.html`), and the other four pages under it.

**No auto-redirect.** A page that moves under you is worse than one that asks, and the stub exists for
an old bookmark, which is exactly the case where being told what happened is the point.

---

## 2. THE DEFECT NOBODY HAD FOUND: CSS SHIPPED AS LITERAL BRACES

`make_commands.py` builds its page from a plain string finished with `.replace('{css}', ...)`. It was
once an f-string, where `{{` is how you write a literal brace. **When it stopped being an f-string the
doubled braces stayed**, and a plain string does not un-double anything. So the generated page carried:

```
table.g{{border-collapse:collapse;width:100%;margin:0 0 10px}}
```

A browser cannot parse that. **Eleven rules, all of them dead**, measured on the shipped page:
`table.g`, its `th`/`td`, its `thead th`, `tr.lead td`, `td.cmd`, `code`, `.why`, `.batbox`,
`.batbox h4`, `ol.steps`, `ol.steps li`. That is every rule the page defines for itself. What survived
was only the shared stylesheet, which knows nothing about this page's tables.

**Measured before and after, on the rebuilt page: 11 occurrences of `{{`, then 0.**

**WHY NO GUARD CAUGHT IT.** `check_plain.py` reads prose. `check_kit.py` checks names, sizes and
hashes. Nothing in this project has ever parsed a generated page and asked whether its own CSS is
valid, so a page could be visibly broken while every check passed. That is §0.2's exit-code rule in a
place nobody had looked: the builder reported success and wrote a file, and the file was wrong.
**NOT YET RUN, and it belongs in batch 2: a check that greps every generated page for `{{`, `}}` and
an unsubstituted `{token}`, and fails loudly.** The testable form is written and it is cheap.

---

## 3. THE COPY BUTTON, AND WHY IT IS NOT ONE LINE

Matt: *"once i finally find the commands page, the copy button was removed, lol."* It is back on all
ten rows.

**IT DOES NOT USE `navigator.clipboard` FIRST, ON PURPOSE.** These pages are opened over `file://`.
The async clipboard API is refused there in some browser builds and the promise simply never resolves,
which would give a button that looks like it worked and did not. That is the exit-code defect wearing a
different hat. So the handler builds a hidden textarea and calls `document.execCommand('copy')`, which
works over `file://`, falls back to the modern API only if that throws, and says **copy failed** rather
than flashing **copied** when neither worked.

---

## 4. NAVIGATION: WHAT CHANGED ON ALL THREE PAGES

**The page bar moved out from above the title.** Matt: *"the hyperlinks on the week sheet are too high
on the page."* They sat between the kicker line and the `<h1>`, so the first thing on the page was a row
of links and the second was what the page is. The bar is now under the standfirst, labelled *other
pages*, and it carries all four pages rather than one or two.

**A sticky section nav.** Matt: *"if any sheet needs jump to links, it's the damn Week Sheet. It's
insufferably long."* It is 76 KB of rendered page with **no `id` attribute anywhere in it**, so there
was nothing to jump to even if a link had existed. Ten anchors now exist and the bar that points at them
stays pinned to the top of the window while you scroll:

```
0 what to do · seat list · 1 free bodies · drop costs · 2 the bar · 3 the bet ·
the cards · 4 who else is short · 5 your roster · 6 rules · top
```

The sub-section anchors are deliberate. **The seat list, the drop costs and the cards are the three
things on that page that get read on their own**, and none of them is a numbered section, so a nav of
only the seven numbered sections would have missed all three.

The to-do page gets the same treatment, its old loose jump row promoted into the same sticky bar with
the commands section added. The commands page gets one too. **That is the consistency Matt asked for,
and it went the direction he said: the to-do page's look won.**

**BOTH HALVES OF THE BACK-LINK FIX, because they are not the same fix.** Cross-page links open in a new
tab, so the sheet you came from still exists. And the to-do page opens with a bar whose first item is
**&larr; the week sheet**, for the case where you arrived some other way. A new tab alone would not have
helped a page opened from a bookmark; a back link alone would still have destroyed the sheet.

**Scroll-margin.** A jumped-to heading would otherwise land underneath the sticky bar. Every `h2` and
`h3` now reserves 56 px for it. This is the sort of thing that is invisible when right and infuriating
when missing.

---

## 5. HOW THIS WAS TESTED, INCLUDING WHAT WAS NOT

**Built for real, not reasoned about:**
- `sheet_engine.write_todo_page` was called against the actual `matt_todo.txt` and produced an
  87 KB page: 44 open items, the count guard passing, 2 links to `../COMMANDS.html`, 0 bare ones,
  7 `target="_blank"`, the sticky nav and the top anchor present.
- `make_commands.py` was run in a mirrored tree with the five real batch files, producing a
  24 KB page: `{{` gone, 10 copy buttons, 4 new-tab page links, the nav present.
- `py_compile` with `-W error::SyntaxWarning` on both, which is doc 144's Python 3.12 trap. Clean.

**NOT built, and this is the honest gap: `WEEK_SHEET.html` itself.** Its renderer needs a live ESPN
pull, which is Matt's to run, so the sheet could not be produced here. The edit was proved a different
way instead: **the multiset of `{...}` substitutions in the module is unchanged except for one new
name, `backbar`, which is defined and which the to-do page build exercised.** Everything else added to
the week sheet is literal HTML with no braces in it. A rendering failure would have to come from a name
that does not exist, and no new name was introduced. **It still wants one real run to be certain, which
is why item 1 is run `ff.bat`.**

**A note on the false alarm in that check, kept because it looks like a defect and is not.** The
placeholder scan also flagged `margin:0 14px 0 0`, `padding:5px 0` and `scroll-margin-top:56px`. Those
are CSS declarations inside `CSS`, which is a plain string, so their braces are literal. The to-do page
building successfully is the proof: had those braces been interpolated, it would have raised instead of
writing a page. Section 2's defect is the same trap in the opposite direction, in a different file.

---

## 6. BATCH 2 AND BATCH 3, NOT DONE, SO THE NEXT SESSION DOES NOT RE-DECIDE THEM

Matt asked for this in batches he can advance, and asked for the important material at first reach.
Batch 1 was navigation and the two broken pages, because those are defects. **What is left is design,
and design changes what he reads first, so it should not be bundled with bug fixes.**

**BATCH 2, the guard and the ordering.**
- **NOT YET RUN:** the generated-page linter from section 2, `{{`, `}}` and unsubstituted `{token}`,
  wired into `ff.bat` next to `check_plain.py`. Cheap, and it is the check whose absence let a visibly
  broken page ship for as long as the page has existed.
- The week sheet opens with a 64-character-wide standfirst explaining what a free player is worth.
  **That is the method, not the answer.** The answer is section 0. Proposal: the standfirst shrinks to
  one line and the explanation moves to where the arithmetic is worked, which is already its own box.
- The empty-slot line (`week 5 D/ST, week 6 TE, week 8 K, week 10 QB`) is a calendar of holes buried in
  a paragraph of prose. It is four dates and it should look like four dates.

**BATCH 3, the long tail.**
- Section 1 prints six free bodies at each of six positions, 36 rows of 14 columns, above the bar that
  explains what the numbers mean. Most weeks he needs one position. Proposal: collapse to the position
  that is actually short this week, with the rest behind a control.
- The cards section is the longest thing on the page and is read least often.
- Print and PDF: the sticky bar is already neutralised for print, but nothing else has been looked at.

**AND ONE THING THAT IS NOT MINE TO DECIDE.** Matt asked to reimagine the content as a human would, and
as an analyst who wants people to read it. The strongest version of that is a real front page: what to
do, what changed since the last build, and what it costs, with everything else one click down. That is a
bigger change than a batch and it should be his call, not a surprise on a Sunday morning.
