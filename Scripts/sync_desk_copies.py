#!/usr/bin/env python3
r"""
sync_desk_copies.py -- put the two documents Matt actually reads on the 2026 root folder,
dated, with exactly one of each.

WHY THIS IS PYTHON AND NOT A .BAT (doc 84):
The batch version used `if errorlevel 1 (...) else (echo OK guide -^> NAME)`. Inside a
parenthesised cmd block the `^>` escape does not hold: cmd read the `>` as a redirect and
wrote the echo text into a file literally named DRAFT_CARD_20260830.pdf -- 11 bytes, in
whatever directory the script was launched from. Two junk files masquerading as PDFs, and
the success message never printed. Batch conditionals cannot be tested from the machine
that writes them; Python can. So the logic lives here and the .bat is a three-line wrapper.

WHY THE ROOT COPIES CARRY A DATE AND THE Source\ ONES DO NOT:
  Source\  is canonical -- ONE name, no version, per the directive's naming rule.
  The root copies are dated snapshots for reading. The date is how you tell at a glance
  whether the thing on your desk is current. Old dated copies are removed, so only one
  of each ever sits there.
"""
import datetime as dt, glob, os, shutil, sys

SRC = r"G:\My Drive\_Fantasy\2026\Source"
DST = r"G:\My Drive\_Fantasy\2026"
# Dated at the root: the date is how you tell at a glance whether what is on your desk
# is current. Everything here is something Matt PRINTS or opens under time pressure.
DOCS = [
    ("guide   ", "DRAFT_DAY_GUIDE.pdf"),
    ("card    ", "DRAFT_CARD.pdf"),
    # doc 116: ONE board replaces five. FALLBACK_BOARD, LATE_RB_SHEET, AUDITION_WINDOW,
    # ANALYST_CALLS and INJURY_CONTEXT_SHEET all still BUILD into Source\ -- they are just no
    # longer desk copies, because flipping between five sheets at 60 seconds a pick was the
    # thing that made them useless. Their patterns stay in the cleanup list below so the old
    # dated copies at the root get swept away on the next run.
    ("board   ", "DRAFT_BOARD.pdf"),
    # doc 157: the page that explains the live board's columns, badges and strip. It is
    # GENERATED from live_draft.COLGLOSS by make_howto.py, so it cannot drift from the
    # screen the way the guide and the card did (docs 79, 82).
    ("how-to  ", "HOW_TO_READ_IT.pdf"),
    # doc 161.  `make_shortcuts.py` has linked `07 - Value ladder` and `09 - Override card` since
    # they were built, and neither was ever added HERE -- so their dated copies at the root were
    # frozen at whatever date they were last made by hand, while board / card / guide / how-to
    # re-dated on every refresh.  Not a dead link, which you would notice: a link that silently
    # opens an older document than the one beside it.  Found by cross-checking every prefix in
    # make_shortcuts.DOCS against this list, which is now a test (`audit_desk.py`).
    ("ladder  ", "VALUE_LADDER.pdf"),
    ("override", "OVERRIDE_CARD.pdf"),
    # doc 169: the 12-wide snake grid -- where players are likely to go, keeper-adjusted.
    # It builds its own PDF (make_gridboard imports to_pdf.render), so it can never be
    # stale against its page; the refusal below still checks.
    ("grid    ", "ADP_GRID.pdf"),
    # doc 203 (Matt): the same 12-wide snake filled in OUR order of value. Read beside
    # ADP_GRID, the two together show where the room is giving a player away.
    ("ourgrid ", "BOARD_GRID.pdf"),
    # doc 192: our ranking arranged BY TIER -- one column per position one row per tier.
    # The board is that ranking as a 180-row list and the grid is in PICK order so a
    # positional tier is scattered across it. This one answers "how many are left in this
    # tier before my next turn". It builds its own PDF through to_pdf.render.
    ("tiers   ", "TIER_SHEET.pdf"),
]
# Removed from the desk but still cleaned up at the root if an old dated copy is sitting there.
RETIRED = ["FALLBACK_BOARD.pdf", "AUDITION_WINDOW.pdf", "LATE_RB_SHEET.pdf",
           "ANALYST_CALLS.pdf", "INJURY_CONTEXT_SHEET.xlsx"]
# NOT dated: things you bookmark or leave open. A changing filename breaks a bookmark.
STABLE = [("commands", "COMMANDS.html")]

# doc 165 wave 5 -- RESTORED. doc 146 built a guard here that REFUSES to put a PDF on the
# desk when it is older than the .html page it was made from; that is the defect doc 146
# found (DRAFT_BOARD.pdf was Sept 1 while its page was current, and this script copied it
# with an OK and a byte count). On Sept 3 I edited a STALE MIRROR of this file and committed
# it over the newer one -- 6,767 bytes became 5,674 -- and the guard went with it. doc 162
# recorded the byte drop as "unresolved"; THIS is what was lost, found by grepping for the
# guard the directive says exists. SS0.2: an exit code is not a result, and neither is a
# byte count.
#
# TOLERANCE, and why it is not zero: the pages and their PDFs are written seconds apart by
# the same run, and VALUE_LADDER's PDF is currently 429 MILLISECONDS older than its page --
# write ordering, not staleness. A zero-tolerance guard would refuse it every time and be
# switched off within a day. STALE_SECS catches the failure that actually happened (a PDF
# from a previous DAY) and ignores same-run ordering.
STALE_SECS = 60


def page_for(src, name):
    """The .html this PDF is built from, if this project builds one. DRAFT_CARD and
    DRAFT_DAY_GUIDE come from Scripts\\card.html and guide.html and are deliberately outside
    to_pdf.py (doc 146), so they have no page here and are not checked."""
    root, ext = os.path.splitext(name)
    if ext.lower() != '.pdf':
        return None
    p = os.path.join(src, root + '.html')
    return p if os.path.exists(p) else None



def main(src=SRC, dst=DST, docs=DOCS, stable=STABLE):
    stamp = f"{dt.datetime.now():%Y%m%d}"
    print("Clearing previous desk copies...")
    removed = 0
    pats = [f"{os.path.splitext(n)[0]}_*{os.path.splitext(n)[1]}"
            for n in [d[1] for d in docs] + RETIRED]
    for pat in pats + ["Copy of DRAFT_DAY_GUIDE.pdf", "Copy of DRAFT_CARD.pdf"]:
        for f in glob.glob(os.path.join(dst, pat)):
            try:
                os.remove(f); removed += 1
            except OSError as e:
                print(f"   could not remove {os.path.basename(f)}: {e}")
    print(f"   {removed} old copy(ies) removed")

    print("Copying current versions...")
    failed = []
    for label, name in docs:
        s = os.path.join(src, name)
        page = page_for(src, name)
        if page and os.path.exists(s):
            behind = os.path.getmtime(page) - os.path.getmtime(s)
            if behind > STALE_SECS:
                failed.append(f"{name} is {behind/60:.0f} min older than {os.path.basename(page)}"
                              f" -- the page was rebuilt and the PDF was not. Run: py to_pdf.py")
                print(f"   REFUSED {label}  {name} is {behind/60:.0f} min behind its page."
                      f"  Run  py to_pdf.py  and re-run this.")
                continue
        # was f"{name[:-4]}_{stamp}.pdf" -- hardcoded .pdf and stripped 4 chars, which turned
        # INJURY_CONTEXT_SHEET.xlsx into INJURY_CONTEXT_SHEET._20260830.pdf. Caught by the test.
        root, ext = os.path.splitext(name)
        d = os.path.join(dst, f"{root}_{stamp}{ext}")
        try:
            shutil.copy2(s, d)
            n = os.path.getsize(d)
            # An 11-byte "PDF" is what the old batch bug produced. Refuse to call that a pass.
            if n < 1024:   # an 11-byte "PDF" is what the old batch bug produced
                failed.append(f"{name} copied but is only {n} bytes -- that is not a PDF")
                print(f"   FAILED  {label}  {os.path.basename(d)} is {n} bytes")
            else:
                print(f"   OK      {label}  {os.path.basename(d)}   {n:,} bytes")
        except Exception as e:
            failed.append(f"{name}: {e}")
            print(f"   FAILED  {label}  {e}")

    for label, name in stable:
        s_, d_ = os.path.join(src, name), os.path.join(dst, name)
        try:
            shutil.copy2(s_, d_)
            n = os.path.getsize(d_)
            print(f"   OK      {label}  {name}   {n:,} bytes   (undated - bookmark it)")
        except Exception as e:
            failed.append(f"{name}: {e}")
            print(f"   FAILED  {label}  {e}")

    print()
    if failed:
        print("  *** AT LEAST ONE COPY FAILED ***")
        for f in failed: print("     ", f)
        print("  A REFUSED line means the PDF is behind its page: run  py to_pdf.py  and")
        print("  re-run this. Any other failure usually means the file is open in a viewer.")
        return 1
    print(f"  Desk copies refreshed. {len(docs)+len(stable)} files confirmed above, with sizes.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
