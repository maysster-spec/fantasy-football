# 158 — Quirks mode ate the colour code, and the key never mentioned colour at all

*Sept 3 evening Eastern. Matt: "same with the gold lines pictured… I couldn't easily figure out
the rhyme or reason."*

---

## 1. THERE WAS NO RHYME OR REASON TO FIND

The coloured rule under a row means **"last player in that position's tier"**, and it is supposed
to be colour-coded by position: RB green `#12734f`, WR blue `#15628f`, TE gold `#9a6212`,
QB purple `#6b3fa0`.

**Every line on the page was rendering gold.** Measured off the rendered pixels rather than read
off the CSS — seven full-width rules sampled on page 1, all `rgb(154,98,18)` = `#9a6212` = the
tight-end colour, under running backs and receivers alike.

**Cause: these pages carry no `<!doctype html>`, so the browser renders them in QUIRKS MODE, and
in quirks mode CSS class selectors match CASE-INSENSITIVELY.** The tier-end class was `te`, so it
also matched the *position* class `TE`. `tr.te.TE td` is the last of the four position rules, so it
won on every row and painted the TE colour everywhere.

**Proved by execution, both directions.** Same HTML re-rendered with a doctype prepended:
the same seven rules came back `(18,115,79)` and `(21,98,143)` — RB green and WR blue, correct
per position. That is the diagnosis and its control in one test.

---

## 2. THE FIX, AND WHY NOT THE OBVIOUS ONE

**Renamed the class `te` → `tend`.** It cannot collide with any position code.

**Adding the doctype would also have worked and was the wrong call three days out.** A doctype
flips the whole document from quirks to standards mode — box model, table sizing, line height,
and therefore where the page breaks fall — on a document that is about to be printed and used at a
table. The rename changes one selector and nothing else.

**Verified after:** the same seven rules now read **4 RB green, 3 WR blue**, matching the positions
of the players above them.

**Checked for the general form of the bug across every generator** — any two classes on one page
differing only by case. `mkvalue.py`, `make_fallback.py` and `make_howto.py`: none.
`live_draft.py` has `VBD`/`vbd`, but it emits a real `<!doctype html>` and so is in standards mode
where the match is case-sensitive; it renders correctly and is left alone. **If anyone ever removes
that doctype, that pair becomes the same defect.**

---

## 3. THE REAL COMPLAINT WAS THE KEY, AND IT WAS RIGHT

Matt could not find the shading or the lines documented **because they were not documented**. The
key at the foot of every page explained the badges and the commentary lean, and said nothing at all
about row colour or the coloured rules — the two things that cover the most pixels on the page.

The key now carries both:

> **row shading** — pink = AVOID · gold = a real DISC · white = neither
> **coloured line under a row** = last player in that position's tier (RB WR TE QB);
> the grey **TIER n** divider is the overall tier

**This is the second time in one evening that a legend and a rendering disagreed** (doc 157: a gold
row above a legend that said "not a discount"). The pattern is the same both times — the mark got
built, the key did not get updated, and the reader is left inferring a rule that was never true.
**A visual encoding that is not in the key is not a feature, it is noise with a backstory.**
