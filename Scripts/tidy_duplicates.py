#!/usr/bin/env python3
r"""
tidy_duplicates.py -- move the Source\ runnable duplicates into 2026\_archive\.

Doc 78 chunk 2 found six runnable duplicates in Source\, a folder documented as
"documents, findings, data. Nothing runs here." They are still there because the
device bridge Claude works through has no delete tool. A script Claude WRITES,
which Matt RUNS, has no such limit -- so this is that script.

    py tidy_duplicates.py           # show what would move, change nothing
    py tidy_duplicates.py --move    # move them to _archive with a date suffix

It MOVES, never deletes. Everything is recoverable from 2026\_archive\.
Files whose bytes match the canonical copy are moved too -- a second copy of the
right file is still how the wrong file gets run one day.
"""
import argparse, datetime as dt, hashlib, os, shutil, sys

BASE   = r"G:\My Drive\_Fantasy\2026"
SOURCE = os.path.join(BASE, 'Source')
ARCH   = os.path.join(BASE, '_archive')
SCRIPTS= os.path.join(BASE, 'Scripts')
KIT    = os.path.join(SCRIPTS, 'live_draft')

# (name in Source\, where the canonical copy lives, why it is a hazard)
TARGETS = [
    ('check_kit.py',                SCRIPTS, 'a STALE copy of the stale-copy detector'),
    ('smoke_spine.py',              SCRIPTS, 'different bytes, same name'),
    ('code_rebuild_spine_v5.py',    SCRIPTS, 'second copy in a "nothing runs here" folder'),
    ('board_v8_fixed.csv',          KIT,     'THE board. Two copies is how the wrong one loads'),
    ('board_v7_kdst_separate.csv',  KIT,     'the pre-ESPN_ID version broke the D/ST filter once'),
    ('ESPN_prerank_with_ids.csv',   KIT,     'inert today (injector uses an absolute path) but the exact Aug-28 shape'),
    # naming-rule violations: one name, no version, history in _archive
    ('FABLE_TASKING_PROMPT_v3.txt', None,    'naming rule: version in the filename'),
    ('ERROR_PATTERNS_1.md',         None,    'naming rule: numbered duplicate'),
    ('test_check_kit.py',           None,    'a test file living beside canonical documents'),
]
TEXT = ('.py', '.csv', '.md', '.txt', '.bat', '.ps1')

def norm_read(p):
    b = open(p, 'rb').read()
    return b.replace(b'\r\n', b'\n') if p.lower().endswith(TEXT) else b

def fingerprint(p):
    b = norm_read(p)
    return len(b), hashlib.sha256(b).hexdigest()[:16]

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--move', action='store_true', help='actually move them')
    a = ap.parse_args(argv)

    if not os.path.isdir(SOURCE):
        print(f"  Source folder not found: {SOURCE}"); return 1
    found = []
    for name, canon_dir, why in TARGETS:
        src = os.path.join(SOURCE, name)
        if not os.path.exists(src):
            continue
        note = why
        if canon_dir:
            c = os.path.join(canon_dir, name)
            if os.path.exists(c):
                same = fingerprint(src) == fingerprint(c)
                note = f"{why}  [{'identical to' if same else 'DIFFERS from'} {os.path.relpath(c, BASE)}]"
            else:
                print(f"  !! REFUSING to touch {name}: no canonical copy at {c}")
                continue
        found.append((src, name, note))

    if not found:
        print("  Nothing to tidy -- Source\\ is clean."); return 0

    print(f"{'MOVING' if a.move else 'WOULD MOVE'} {len(found)} file(s) out of Source\\:\n")
    for src, name, note in found:
        print(f"   {name:32s} {note}")
    if not a.move:
        print("\n  Nothing changed. Re-run with --move to do it.")
        print("  Everything goes to _archive with a date suffix; nothing is deleted.")
        return 0

    os.makedirs(ARCH, exist_ok=True)
    stamp = f"{dt.datetime.now():%Y%m%d_%H%M}"
    print()
    moved = 0
    for src, name, _ in found:
        root, ext = os.path.splitext(name)
        dst = os.path.join(ARCH, f"{root}_FROM_SOURCE_{stamp}{ext}")
        try:
            shutil.move(src, dst); moved += 1
            print(f"   moved {name:32s} -> _archive\\{os.path.basename(dst)}")
        except Exception as e:
            print(f"   FAILED {name}: {e}")
    print(f"\n  {moved} of {len(found)} moved.")
    print("  Now run:  py check_kit.py    -- the STRAGGLER warning should be gone.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
