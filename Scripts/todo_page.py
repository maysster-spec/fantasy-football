"""todo_page.py -- rebuild MY_TODO.html, and re-stamp the link on the week sheet.

Matt, 2026-09-17: "can't we do better than a text file, but you can still update it without me
running a python file since i don't need to scrape the info for you from espn." Exactly right --
the to-do list needs nothing from ESPN, so it must not be hostage to a pull. This script touches
NO network and NO ESPN session: it reads Source\\matt_todo.txt and writes Source\\MY_TODO.html,
then edits the two places on Source\\WEEK_SHEET.html that carry the open count.

ONE IMPLEMENTATION, NOT TWO. The page itself is built by sheet_engine.write_todo_page, the same
function py wire.py --html calls, so the two routes cannot drift (0.5(c)4 -- a second NAME for one
JOB is the same defect as a second file claiming one number).

    py todo_page.py            rebuild the page and re-stamp the sheet
    py todo_page.py --check    say what it WOULD do, write nothing
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'Source'))
sys.path.insert(0, HERE)
import sheet_engine                                        # noqa: E402

SHEET = os.path.join(SRC, 'WEEK_SHEET.html')
TEAM = 'The Poetry of Junkyard Juggers'


def restamp(path, n):
    """Re-point the week sheet's masthead link and box header at the current count.

    Returns (changed, why). It NEVER inserts the link into a sheet that does not have one: a
    sheet built before this existed is rebuilt by py wire.py --html, and silently editing a page
    whose shape I have not checked is how a false sentence ships (doc 303 section 6).
    """
    if not os.path.exists(path):
        return False, 'WEEK_SHEET.html is not there'
    s = open(path, encoding='utf-8').read()
    if 'MY_TODO.html' not in s:
        return False, ('this sheet predates the link -- run  py wire.py --html  once and it will '
                       'be built in')
    out = re.sub(r'(to-do list &mdash; )\d+( open</a>)', lambda m: m.group(1) + str(n) + m.group(2), s)
    out = re.sub(r'(yours this week &mdash; )\d+( open</h4>)', lambda m: m.group(1) + str(n) + m.group(2), out)
    out = re.sub(r'(and <strong>)\d+(</strong> more)',
                 lambda m: m.group(1) + str(max(0, n - 6)) + m.group(2), out)
    if out == s:
        return False, 'the sheet already says ' + str(n)
    # THE COUNT IS CHECKED AFTER THE WRITE, NOT ASSUMED (0.2: verify the artifact). A regex that
    # matched nothing returns unchanged text above; one that matched the wrong thing is caught here.
    if out.count('to-do list &mdash; %d open' % n) != 1:
        return False, 'the masthead link did not re-stamp cleanly -- sheet left untouched'
    open(path, 'w', encoding='utf-8').write(out)
    return True, 'sheet re-stamped to %d open' % n


def main(argv):
    check = '--check' in argv
    op, dn = sheet_engine.load_todo_all(SRC)
    print('  matt_todo.txt: %d open, %d done' % (len(op), len(dn)))
    if check:
        ok, why = (None, '')
        print('  --check: would write %s and re-stamp the sheet. Nothing written.'
              % os.path.join(SRC, sheet_engine.TODO_PAGE))
        return 0
    path, n = sheet_engine.write_todo_page(SRC, team_name=TEAM)
    if not path:
        print('  NOTHING WRITTEN -- Source\\matt_todo.txt is not there')
        return 1
    print('  written: %s  (%d open)' % (path, n))
    ok, why = restamp(SHEET, n)
    print(('  ' if ok else '  not re-stamped -- ') + why)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
