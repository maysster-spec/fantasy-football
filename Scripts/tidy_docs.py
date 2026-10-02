#!/usr/bin/env python3
r"""
tidy_docs.py -- move superseded reference documents out of Source\ and into _archive\.

    py tidy_docs.py            show what would move  (default, changes nothing)
    py tidy_docs.py --move     actually move them, with a date suffix
    py tidy_docs.py --root     ALSO tidy the 2026 root folder (doc 116)
    py tidy_docs.py --root --move

Doc 108. Five different files tried to orient a reader and three of them were stale enough to
mislead: two pinned the directive at v5.4 (it is v5.8) and said the draft kit was five files
(it is six). `00_START_HERE.md` replaces all of them.

NOTHING IS DELETED. Everything lands in 2026\_archive\ with a date suffix, exactly like
tidy_duplicates.py. If a file turns out to matter, it is still there.

--root (doc 116) applies the same idea to the 2026 folder itself. The root is a DESK, not a
filing cabinet: the only things that belong on it are what Matt opens on draft night. Raw
research outputs go to their source folder, finished analysis goes to Source\, and one-off
prompts and spreadsheet leftovers go to _archive. Dated desk copies are NOT touched here --
sync_desk_copies.py owns those and already sweeps the retired ones.
"""
import argparse, datetime as dt, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
ARCH = os.path.normpath(os.path.join(HERE, '..', '_archive'))

RETIRE = [
    # (filename, why)
    ('00_HANDOVER_READ_ME_FIRST.md', 'replaced by 00_START_HERE.md; pins v5.4 and "five files"'),
    ('00_CALENDAR_TO_DRAFT.md',      'replaced by 00_START_HERE.md + DRAFT_DAY_GUIDE; pins v5.4'),
    ('PROJECT-STATE.md',             'Aug 8 -- three weeks and ~60 findings out of date'),
    ('00_CLAUDE_WORKFLOW.md',        'Aug 18 -- superseded by the directive'),
    ('00_PROJECT_DIRECTIVE_v4.md',   'violates the naming rule; v5.8 is current'),
    ('NEW_CHAT_PROMPT.txt',          'session bootstrap, pre-dates the red-team sweep'),
    ('SCRATCHPAD_INIT.txt',          'session bootstrap, pre-dates the red-team sweep'),
    ('NEXT_PROMPT_scratchpad_finish.txt', 'one-off prompt, work completed'),
    ('GEMINI_FIX_BRIEF_espn_pull.md',     'the pull was fixed and verified Aug 28'),
    ('GEMINI_FIX_2_espn_pull.md',         'the pull was fixed and verified Aug 28'),
    ('GEMINI_REDTEAM_PACKAGE.md',         'that red team ran; docs 78-82 and 100 supersede it'),
    ('FABLE_TASKING_PROMPT.txt',          'task 1 complete (doc 92); task 2 is at the 2026 root'),
    ('GEMINI_sheets_and_calendar.txt',    'one-off prompt, work completed'),
    ('QC_ADDENDUM.md',                    'folded into the directive and ERROR_PATTERNS'),
]

# Never touch these, whatever else changes.
KEEP = {'00_START_HERE.md', '00_PROJECT_DIRECTIVE.md', 'DRAFT_DAY_GUIDE.md', 'ERROR_PATTERNS_1.md',
        '02_findings_ledger.md', '02b_LEDGER_CORRECTIONS_v5.md', 'INJURY_CONTEXT_SHEET.md',
        '01_league_and_managers.md', 'manager-profiles.md', '2026_League_Settings.txt'}


# --- doc 116: the 2026 root folder -------------------------------------------------------
# (filename, destination subfolder or '_archive', why)
ROOT_MOVES = [
    ('2026-nfl-injury-sweep.csv',        '10_Gemni', 'raw Gemini output; the repaired copy is Source\\sweep_20260831.csv'),
    ('Fantasy Football Gap Analysis.md', '10_Gemni', 'raw Gemini output'),
    ('Comprehensive Fantasy Analyst Call Scraping, Fact-Checking, and Custom League Draft Report.md',
                                          '10_Gemni', 'raw Gemini output, audited in doc 103'),
    ('favorite-analysts-calls-2026.csv', '10_Gemni', 'Gemini scrape; analyst_calls_joined.csv is what is read'),
    ('raw-analyst-calls-v2.csv',         '10_Gemni', 'Gemini scrape; analyst_calls_joined.csv is what is read'),
    ('94_picks_17_and_32.md',            'Source',   "Fable's picks-17/32 study, reviewed in doc 111"),
    ('Fable_results.txt',                'Source',   'Fable run log'),
    ('FABLE_TASKING_PROMPT_2_picks_17_32.txt', 'Source', 'that task is complete'),
    ('PODCAST_PROMPT.txt',               'Source',   'one-off prompt, work completed'),
    ('Untitled spreadsheet - Sheet1 (2).csv', '_archive', 'the delta table, pasted by hand; delta_gaps.py emits it'),
    ('Untitled spreadsheet.gsheet',      '_archive', 'Google Sheets stub for the file above'),
    ('~$ntasy Football To Do List.docx',  '_archive', 'Word lock file left behind by a crash'),
]
# Stays on the desk, whatever else happens.
ROOT_KEEP = {'COMMANDS.html', 'Fantasy Football To Do List.docx'}

# --- doc 169: THE NAMED LIST ABOVE WENT STALE IN SIX DAYS ---------------------------------
# Every entry in ROOT_MOVES now prints "gone" -- they were all moved on Aug 30 and the root
# refilled with thirteen NEW files nobody listed. A hardcoded list cannot tidy a folder that
# keeps changing; it only tidies the folder it was written for. So the named list stays (it is
# history, and it is harmless), and everything it does not name goes through RULES.
#
# TWO THINGS THIS WILL NOT DO, both on purpose:
#   1. It never touches a DATED desk copy (DRAFT_BOARD_20260905.pdf and friends).
#      sync_desk_copies.py owns those and sweeps the retired ones itself. Two owners for one
#      file is how a draft-night artifact goes missing.
#   2. It never moves a file no rule recognises. It PRINTS it as UNCLASSIFIED and leaves it.
#      A tidier that guesses is worse than a cluttered desk.
import re

DATED = re.compile(r'^(?P<stem>.+?)_20\d{6}(_\d{4})?\.(pdf|html|csv|xlsx|docx)$', re.I)

# A dated file at the root is only safe if something actually SWEEPS it. Rather than keep a
# second copy of that list here -- two lists that drift is the defect this project keeps
# paying for -- read the stems straight out of sync_desk_copies.py, which is the owner.
# Found by checking: RESEARCH_PLAN_20260901.pdf is in NEITHER of its lists, so nothing has
# swept it since Sept 1 and a blanket "dated files are owned" rule would have told you a lie.
_FALLBACK_OWNED = {'DRAFT_DAY_GUIDE', 'DRAFT_CARD', 'DRAFT_BOARD', 'HOW_TO_READ_IT',
                   'VALUE_LADDER', 'OVERRIDE_CARD', 'FALLBACK_BOARD', 'AUDITION_WINDOW',
                   'LATE_RB_SHEET', 'ANALYST_CALLS', 'INJURY_CONTEXT_SHEET'}


def desk_owned():
    """Stems sync_desk_copies.py dates at the root, or sweeps when retired."""
    f = os.path.join(HERE, 'sync_desk_copies.py')
    try:
        src = open(f, encoding='utf-8').read()
        body = src[src.index('DOCS = ['):src.index('STABLE')]
        found = set(re.findall(r'["\']([A-Za-z0-9_]+)\.(?:pdf|xlsx|html)["\']', body))
        if found:
            return found
    except Exception as e:
        print(f"  !! could not read sync_desk_copies.py ({e}) -- using the built-in list")
    return _FALLBACK_OWNED

# (regex, destination, why) -- FIRST match wins, so order matters.
ROOT_RULES = [
    (r'^~\$',                        '_archive', 'Office lock file left by a crash'),
    (r'^~WRL.*\.tmp$',               '_archive', 'Word crash temp file'),
    (r'\.(tmp|log|bak)$',            '_archive', 'temp / log leftover'),
    (r'\.gsheet$',                   '_archive', 'Google Sheets stub -- holds no data'),
    (r'output|powershell|console|errors\.txt$',
                                     '_archive', 'console dump -- the finding it produced is in a numbered doc'),
    (r'^(NEXT_)?PROMPT|PROMPT.*\.txt$|^FABLE_TASKING_PROMPT',
                                     '_archive', 'one-off tasking prompt, work completed'),
    (r'^transcript-',                '10_Gemni', 'raw research transcript'),
    (r'Research\.md$|Analysis\.md$|^Comprehensive |Gemini|Gemni',
                                     '10_Gemni', 'raw deep-research output -- the audited copy lives in Source'),
    (r'\.csv$',                      'Source',   'data belongs in the filing cabinet, not on the desk'),
    (r'\.md$',                       'Source',   'finished analysis belongs in Source'),
    (r'\.pdf$',                      '_archive', 'undated PDF on the desk -- Source holds the master'),
]


OWNED = {x.upper() for x in desk_owned()}


def classify(name):
    """Return (dest, why) or (None, reason-it-was-left-alone)."""
    if name in ROOT_KEEP:
        return None, 'on the KEEP list'
    m = DATED.match(name)
    if m and m.group('stem').upper() in OWNED:
        return None, 'dated desk copy -- sync_desk_copies.py owns it'
    if m:
        return '_archive', 'dated copy that NO script sweeps -- orphaned at the root'
    for pat, dest, why in ROOT_RULES:
        if re.search(pat, name, re.I):
            return dest, why
    return None, 'UNCLASSIFIED'


def tidy_root(move):
    root = os.path.normpath(os.path.join(HERE, '..'))
    stamp = f"{dt.datetime.now():%Y%m%d}"
    print("\n" + "=" * 74)
    print("  TIDY THE 2026 ROOT" + ("" if move else "   (dry run -- nothing moves)"))
    print("=" * 74)
    print("  The root is a desk. Dated desk copies stay; sync_desk_copies.py owns those.\n")
    n = 0
    for name, dest_dir, why in ROOT_MOVES:
        if name in ROOT_KEEP:
            print(f"  !! {name} is on the KEEP list -- skipped"); continue
        p = os.path.join(root, name)
        if not os.path.exists(p):
            print(f"  gone      {name}"); continue
        target_dir = ARCH if dest_dir == '_archive' else os.path.join(root, dest_dir)
        base, ext = os.path.splitext(name)
        dest = os.path.join(target_dir, (f"{base}_{stamp}{ext}" if dest_dir == '_archive' else name))
        print(f"  {'MOVING' if move else 'would move'}  {name}\n            -> {dest_dir}\\   ({why})")
        if move:
            os.makedirs(target_dir, exist_ok=True)
            if os.path.exists(dest):
                dest = dest.replace(ext, f"_{dt.datetime.now():%H%M}{ext}")
            shutil.move(p, dest)
        n += 1
    # --- doc 169: the rules pass, over everything the named list did not cover ------------
    named = {x[0] for x in ROOT_MOVES}
    unknown, kept = [], []
    print("\n  --- by rule (everything the list above does not name) ---")
    for entry in sorted(os.listdir(root)):
        full = os.path.join(root, entry)
        if os.path.isdir(full) or entry in named:
            continue
        dest_dir, why = classify(entry)
        if dest_dir is None:
            (unknown if why == 'UNCLASSIFIED' else kept).append((entry, why))
            continue
        target_dir = ARCH if dest_dir == '_archive' else os.path.join(root, dest_dir)
        base, ext = os.path.splitext(entry)
        dest = os.path.join(target_dir,
                            (f"{base}_{stamp}{ext}" if dest_dir == '_archive' else entry))
        print(f"  {'MOVING' if move else 'would move'}  {entry}\n            -> {dest_dir}\\   ({why})")
        if move:
            os.makedirs(target_dir, exist_ok=True)
            if os.path.exists(dest):
                dest = dest.replace(ext, f"_{dt.datetime.now():%H%M}{ext}")
            shutil.move(full, dest)
        n += 1

    print(f"\n  {n} file(s) {'moved' if move else 'would move'}. NOTHING WAS DELETED.")
    if kept:
        print("\n  STAYING ON THE DESK:")
        for e, why in kept:
            print(f"    {e:<44} {why}")
    if unknown:
        print("\n  !! UNCLASSIFIED -- left alone on purpose. Add a rule or move them by hand:")
        for e, _ in unknown:
            print(f"    {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--move', action='store_true')
    ap.add_argument('--root', action='store_true', help='also tidy the 2026 root folder')
    a = ap.parse_args()
    if not os.path.isdir(SRC): sys.exit(f"  no Source folder at {SRC}")
    stamp = f"{dt.datetime.now():%Y%m%d}"
    n = 0
    print("=" * 74)
    print("  RETIRE SUPERSEDED REFERENCE DOCS" + ("" if a.move else "   (dry run -- nothing moves)"))
    print("=" * 74)
    for name, why in RETIRE:
        if name in KEEP:
            print(f"  !! {name} is on the KEEP list -- skipped"); continue
        p = os.path.join(SRC, name)
        if not os.path.exists(p):
            print(f"  gone      {name}"); continue
        root, ext = os.path.splitext(name)
        dest = os.path.join(ARCH, f"{root}_RETIRED_{stamp}{ext}")
        print(f"  {'MOVING' if a.move else 'would move'}  {name}\n            {why}")
        if a.move:
            os.makedirs(ARCH, exist_ok=True)
            if os.path.exists(dest): dest = dest.replace(ext, f"_{dt.datetime.now():%H%M}{ext}")
            shutil.move(p, dest)
        n += 1
    print(f"\n  {n} file(s) {'moved to' if a.move else 'would move to'} {ARCH}")
    if not a.move and n:
        print("  Nothing was deleted and nothing will be. Re-run with --move to do it.")
    print("  Everything still in Source\\ is either current or is a numbered finding doc,")
    print("  and numbered docs are history on purpose -- the higher number wins.")
    if a.root:
        tidy_root(a.move)


if __name__ == '__main__':
    main()
