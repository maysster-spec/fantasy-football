#!/usr/bin/env python3
r"""
make_shortcuts.py -- put a "FF2026 Draft" folder on the Desktop with one launcher per
scenario, plus a link to the command page.

    py make_shortcuts.py            # create/refresh the folder
    py make_shortcuts.py --remove   # take it away again

doc 94: COMMANDS.html cannot launch anything -- browsers will not run local programs from
a file:// page, and that restriction is a good one. So the page stays the reference and the
Desktop folder is the launcher. These are tiny forwarding .bat files, NOT Windows shortcuts:
no COM, no pywin32, nothing to install, and each one works no matter where it is double-clicked.
"""
import argparse, os, sys

SCRIPTS = r"G:\My Drive\_Fantasy\2026\Scripts"
PAGE    = r"G:\My Drive\_Fantasy\2026\COMMANDS.html"
FOLDER  = "FF2026 Draft"
INDEX   = "_what these are.txt"

# Numbered so Windows sorts them the way you use them: 00 = the page you read,
# 01-05 = things you run, 06+ = the documents. Two digits so the order holds
# everywhere, not just in Explorer's number-aware sort.
# (filename on the desktop, batch file in Scripts\, one plain-English line)
LAUNCHERS = [
    ("01 - Check everything.bat",  "weekend_check.bat",    "runs every pre-draft test and gives one answer"),
    ("02 - Saturday refresh.bat",  "sept5_after.bat",      "after the projections refresh: rebuild every printout"),
    ("03 - DRAFT NIGHT 655pm.bat", "draft_night.bat",      "the whole 7:00 PM sequence - it stops if anything is wrong"),
    ("04 - Fix ESPN sign-in.bat",  "cookie_jar.bat",       "when ESPN says you are not signed in"),
    ("05 - Refresh printouts.bat", "sync_desk_copies.bat", "put today's board, ladder, card, guide and how-to on your desk"),
]

# Documents live at the 2026 root with a DATE in the name, so match on a prefix and
# link to whichever is current. Re-run this after sync_desk_copies and it re-points.
#
# doc 146 -- WHY THIS LIST CHANGED. Two of the four links here pointed at documents that
# no longer exist: doc 116 retired FALLBACK_BOARD and INJURY_CONTEXT_SHEET as desk copies
# and sync_desk_copies.py now DELETES their dated copies from the root, so both links had
# been dead since Aug 31. Meanwhile the two documents built since -- the draft board itself
# and the value ladder -- had no link at all. A generated folder that quietly rots is worse
# than no folder, so the sweep below now removes anything this script no longer generates.
DOCS_DIR = r"G:\My Drive\_Fantasy\2026"
DOCS = [
    ("06 - Draft board.url",     "DRAFT_BOARD_",     "THE board - every player, one row each"),
    ("07 - Value ladder.url",    "VALUE_LADDER_",    "where the board, the analysts and the depth chart agree"),
    ("08 - Draft card.url",      "DRAFT_CARD_",      "the one-pager you read at the table"),
    ("09 - Override card.url",   "OVERRIDE_CARD_",   "the few players the board cannot show correctly"),
    ("10 - Draft day guide.url", "DRAFT_DAY_GUIDE_", "read once, before the night"),
    ("11 - How to read the board.url", "HOW_TO_READ_IT_",
     "what every column, badge and warning on the live board means"),
    # doc 174: the snake grid. It was added to sync_desk_copies.DOCS when it was built but
    # never here, which is doc 161's defect exactly -- a desk copy that re-dates every refresh
    # with no link pointing at it. `audit_desk.py` cross-checks these two lists for that reason.
    ("12 - Draft board grid.url", "ADP_GRID_",
     "where players are likely to go, 12 wide, keeper-adjusted - 2 sheets"),
    # doc 209: the SAME defect a third and fourth time, and the comment above it was already
    # written. BOARD_GRID (our order) and TIER_SHEET both ship, both are on the desk, and both
    # re-date on every refresh -- with nothing on the Desktop pointing at either. audit_desk.py
    # reports exactly this as a "note" and was never run because its own paths were wrong.
    ("13 - Our board grid.url", "BOARD_GRID_",
     "the same 12-wide grid in OUR order, not the market's - 2 sheets"),
    ("14 - Tier sheet.url", "TIER_SHEET_",
     "our ranking by tier, one column a position - how many are left before your next turn"),
]

# Anything matching this that we did not just write is a leftover from an older version of
# this list, and gets removed. Files you put in the folder yourself are left alone.
import re as _re
GENERATED = _re.compile(r'^\d{1,2} - .+\.(bat|url)$', _re.I)

def desktop():
    for c in (os.path.join(os.path.expanduser("~"), "Desktop"),
              os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")):
        if os.path.isdir(c):
            return c
    return None

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--remove', action='store_true')
    ap.add_argument('--desktop', help='override the Desktop path (used by the tests)')
    ap.add_argument('--scripts', default=SCRIPTS)
    ap.add_argument('--docs', default=DOCS_DIR)
    ap.add_argument('--page', default=PAGE)
    a = ap.parse_args(argv)

    dt = a.desktop or desktop()
    if not dt:
        print("  Could not find your Desktop folder. Pass --desktop \"C:\\path\\to\\Desktop\"")
        return 1
    out = os.path.join(dt, FOLDER)

    if a.remove:
        if not os.path.isdir(out):
            print(f"  Nothing to remove -- {out} does not exist."); return 0
        # Only remove what this script generates. Anything you put in the folder yourself
        # stays, and the folder is left behind if it still holds any of it.
        for f in os.listdir(out):
            if GENERATED.match(f) or f == INDEX:
                os.remove(os.path.join(out, f))
        left = os.listdir(out)
        if left:
            print(f"  Removed the launchers. {len(left)} of your own file(s) left in {out}.")
            return 0
        os.rmdir(out)
        print(f"  Removed {out}"); return 0

    os.makedirs(out, exist_ok=True)
    made, wrote = 0, set()
    for name, target, why in LAUNCHERS:
        src = os.path.join(a.scripts, target)
        if not os.path.exists(src):
            print(f"  SKIPPED {name:30s} -- {target} not found in Scripts\\")
            continue
        body = (
            "@echo off\r\n"
            f"REM  {why}\r\n"
            f"REM  Generated by make_shortcuts.py -- edits belong in {target}, not here.\r\n"
            f'call "{src}"\r\n'
        )
        with open(os.path.join(out, name), "w", newline="") as f:
            f.write(body)
        made += 1; wrote.add(name)
        print(f"  {name:30s} -> {target}")

    def urlfile(name, target, label):
        with open(os.path.join(out, name), "w", newline="") as f:
            f.write("[InternetShortcut]\r\nURL=file:///" + target.replace("\\", "/") + "\r\n")
        wrote.add(name)
        print(f"  {name:30s} -> {label}")

    urlfile("00 - Command page.url", a.page, "COMMANDS.html")
    made += 1

    # newest file matching each prefix -- the dated printouts change name every rebuild
    docs = a.docs
    for name, prefix, why in DOCS:
        try:
            hits = [f for f in os.listdir(docs) if f.startswith(prefix)]
        except OSError:
            hits = []
        if not hits:
            print(f"  SKIPPED {name:30s} -- nothing starting {prefix} in the 2026 folder")
            continue
        newest = max(hits, key=lambda f: os.path.getmtime(os.path.join(docs, f)))
        urlfile(name, os.path.join(docs, newest), newest)
        made += 1

    # Sweep anything this script used to generate and no longer does, so the folder cannot
    # accumulate two numbering schemes or a link to a document that has been retired.
    swept = []
    for f in sorted(os.listdir(out)):
        if f in wrote or f == INDEX:
            continue
        if GENERATED.match(f):
            try:
                os.remove(os.path.join(out, f)); swept.append(f)
            except OSError:
                pass
    for f in swept:
        print(f"  removed (no longer generated)  {f}")

    # One plain-text index, so "which of these do I click" is answerable without opening any
    # of them. Written last so it can list exactly what is really there.
    lines = ["FF2026 Draft -- what each of these is", "=" * 44, "",
             "00 - Command page        every command, grouped by when you need it",
             "                         START HERE if you are not sure.", ""]
    for name, _t, why in LAUNCHERS:
        if name in wrote:
            lines.append(f"{name[:-4]:<26} {why}")
    lines += ["", "The numbered documents are the current printouts. They carry a date in",
              "the file they point at; re-run  py make_shortcuts.py  after refreshing the",
              "printouts and these links re-point to the new ones.", ""]
    for name, _p, why in DOCS:
        if name in wrote:
            lines.append(f"{name[:-4]:<26} {why}")
    with open(os.path.join(out, INDEX), "w", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n  {made} launcher(s) in:  {out}")
    print(f"  {INDEX} lists what each one is, in plain English.")
    print("  Pin that folder to your taskbar or leave it on the Desktop.")
    print("  Re-run after sync_desk_copies.bat -- the document links re-point to the new dates.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
