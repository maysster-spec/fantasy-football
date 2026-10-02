# 159 — The screen had no key either, and the ---- lines have their own history

*Sept 3 evening Eastern. Matt, after the paper-board fixes: "do any similar artifacts need to be
cleaned/clarified on the live draft board?"*

---

## 1. THE AUDIT: WHAT THE SCREEN ENCODES vs WHAT IT EXPLAINED

Every selector in `live_draft.py`'s stylesheet that paints a colour, border or background, checked
against `COLGLOSS` — the "what do these columns mean?" panel. **The legend explained eight things.
The page encoded at least twelve.** Undocumented, in order of how much ink they use:

| encoded | was it in the key? |
|---|---|
| **the badges** — AVOID / OUT / IR / DISC / BYE / FADE / Q / MINE / BUY / CALLS / OPEN / DART / ok, plus BUY at three brightnesses | **no** |
| **the GONE column** — NOW, then −1 −2 −3, top three brightened | **no** |
| **the dashed TIER BREAK line** and its −n VBD label | **no** |
| **the RUN flag** in the headline | **no** |

**This is exactly the defect Matt found on paper, one artifact over.** The printed board carried a
badge key in its footer and the screen carried none — and doc 105 designed those badges to be the
tiebreaker for the half of the night where the board has no opinion. A tiebreaker you have to
decode is not a tiebreaker.

**Fixed by adding four entries to `COLGLOSS`.** That list feeds **both** the live legend **and**
`make_howto.py`, so screen and paper now come from one source and cannot drift on these. The
how-to page skips the badge entry because it already prints a fuller table of the same thing —
declared explicitly, and the script asserts the skipped keys still exist so a rename cannot silently
drop them.

**Verified by rendering:** 12 legend rows on the live page, 33 rows on the how-to, both from the
same source. No number, no ordering and no engine behaviour changed.

**Also checked, and clean:** the case-collision that broke the paper board's colour code (doc 158)
cannot happen here — `live_draft.py` emits a real `<!doctype html>`, so class matching is
case-sensitive. It does carry a `VBD`/`vbd` pair that *would* collide in quirks mode. **If anyone
ever removes that doctype, that is the same defect.**

---

## 2. YES — AND IT WAS THE LINES, TWICE (doc 139, then doc 147)

Matt remembered right, and the pun lands: the `----` lines *were* the display problem.

**Doc 139, the tier lines.** The number of dashed tier rules varied with the spread on screen, and
the number of player rows varied too — 10 on his turn, 8 while waiting. So the board changed height
**every refresh**, and everything below it slid up and down between polls, on a 60-second clock.
Fixed by pinning the *structure*, not a min-height: **exactly 12 player rows and exactly 3 tier
rows, always**, with the unused tier slots rendered as invisible spacers
(`tr.tier.gh div{border-top-color:transparent}`). Fixing the structure means the height is identical
by construction — no pixel estimate to get wrong.

**Doc 147, the same bug beside it.** Pinning the board left the GONE column free to grow from 0 to
18 names, so the page *still* changed height for the first two rounds, for the same reason and at
the same cost. Fixed at 8 rows, padded with `visibility:hidden`.

**Both re-verified tonight, after every change:** shape `[(12, 3)]` at all twelve of Matt's picks,
and the board's top edge at **199px** across five draft states and four viewport widths. That is
the guarantee §7 states — *if it ever renders a different count, something is wrong; say so rather
than explaining it.*

---

## 3. ONE MORE DEFECT, MINE, WORTH RECORDING

Inserting the four legend entries, my splice ate the closing `),` of the entry above it.
**`ast.parse` reported the file was fine** — `('a', 'b' 'c')` is valid Python, it just calls a
string — and the failure only appeared on `import`. **A syntax check is not a test.** The red-team
harness caught it because it imports the module and renders real pages; the syntax check would have
let it through to a commit.

---

## 4. AND THE KEY NOW PRINTS THE MARKS, NOT DESCRIPTIONS OF THEM

*Matt: "add color matching to the columns and definitions where it makes sense."*

The only honest way to print a key for a coloured mark is to print the mark. So
`make_howto.py` no longer describes the colours — it **parses `live_draft.py`'s stylesheet at
generation time**, resolves its `:root` variables, and renders every chip with the board's own
background, border and text colour. **18 colours reproduced, checked by searching the generated
page for each expected hex.** Change the board's palette and the page follows; a retyped hex is
how a key starts lying (docs 157, 158).

The page is white and the board is dark, so each chip sits on the board's own panel colour
`#171a21` rather than being tinted onto paper — what he sees on the sheet is what is on the screen.

Covered: all thirteen badges, `R`, `goes first`, the four position chips, the RUN flag, the
starter strip in its three states, and a new **"the colours in that column"** table showing what
`free` / `tie` / cheap / dear actually look like at `-0.9`, `-4.2`, `-13.7`.

**One defect in my own extractor, and it is a nice one.** `rule()` took the FIRST CSS block
matching a selector. The eleven badge classes share a font declaration —
`.ctxA,.ctxD,…,.ctxM{font:…}` — so for `.ctxM` the first match is that shared block, and the
lookup never reached `.ctxM{background:#6b4a08;…}` further down. **MINE rendered as a plain grey
chip and nothing said so.** Fixed by merging *every* matching block in source order, which is what
a browser does anyway. **Caught by searching the rendered page for each expected hex** — not by
looking at it, where a grey chip among coloured ones reads as a design choice.
