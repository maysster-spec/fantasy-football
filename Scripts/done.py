"""done.py -- tick an item off the to-do list and rebuild the page, in one command.

MATT, 2026-09-18: "update something in the command files/bat files to update the to do list?
You tell me."

THE PROBLEM IT SOLVES. `matt_todo.txt` is the source and `MY_TODO.html` is generated from it, so
the page is never wrong about the file. But MATT HAD NO WAY TO TICK ANYTHING. He would do the
thing, and the item sat open until I noticed and edited the file for him -- which is why five
items he had already finished were still showing as open on 18 September. A list that only one of
us can close is a list that drifts from reality in one direction, always.

    done ff.bat                       tick the one open item matching that text
    done "PASTE THE DIRECTIVE"        quotes when the text has spaces
    done --list                       every open item, numbered
    done --check ff.bat               say what it would tick, change nothing
    done --undo ff.bat                put a ticked item back to open

IT REFUSES RATHER THAN GUESSES. The text must match EXACTLY ONE open item. Zero matches or two
matches and it prints the candidates and writes nothing -- ticking the wrong line silently is
worse than not ticking at all, and the whole point of the file is that it is trustworthy.

It archives the file before writing, then calls todo_page.main(), the SAME code path `ff.bat`
uses, so the page and the sheet's count are rebuilt by one implementation and cannot drift.

Standard library only. Paths resolve against this file, never the shell's cwd.
"""
import datetime as dt
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
SRC = os.path.join(ROOT, 'Source')
ARCH = os.path.join(ROOT, '_archive')
TODO = os.path.join(SRC, 'matt_todo.txt')


def items(lines, mark):
    """Every line that opens an item with `mark`, as (index, title). The title is the line up to
    its first `#`, which is where the note starts."""
    out = []
    for i, ln in enumerate(lines):
        if ln.startswith(mark):
            title = ln[3:].split('#', 1)[0].strip()
            out.append((i, title or ln[3:].strip()))
    return out


def find(lines, phrase, mark):
    """Exactly one, or nothing. Case-insensitive substring against the whole line, so a doc
    number or a script name in the note still finds it."""
    p = phrase.lower()
    hits = [(i, t) for i, t in items(lines, mark) if p in lines[i].lower()]
    return hits


def main(argv):
    if not os.path.exists(TODO):
        print('  NOTHING TO DO: %s is not there' % TODO)
        return 1
    check = '--check' in argv
    undo = '--undo' in argv
    args = [a for a in argv if not a.startswith('--')]
    lines = open(TODO, encoding='utf-8').read().split('\n')
    mark = '[x]' if undo else '[ ]'
    new = '[ ]' if undo else '[x]'

    if '--list' in argv or not args:
        op = items(lines, '[ ]')
        print('  %d open:' % len(op))
        for n, (i, t) in enumerate(op, 1):
            print('   %2d. %s' % (n, t[:96]))
        if not args:
            print('\n  Tick one with:  done "<some words from it>"')
        return 0

    phrase = ' '.join(args)
    hits = find(lines, phrase, mark)
    if not hits:
        print('  NOTHING MATCHED %r among the %s items. Nothing written.' % (phrase, 'ticked' if undo else 'open'))
        print('  Run  done --list  to see them.')
        return 1
    if len(hits) > 1:
        # REFUSE, AND SHOW THE AMBIGUITY. Picking the first match would be a silent wrong answer.
        print('  %r MATCHES %d ITEMS, so nothing was written. Be more specific:' % (phrase, len(hits)))
        for i, t in hits:
            print('    - %s' % t[:96])
        return 1

    i, title = hits[0]
    if check:
        print('  --check: would %s -- %s\n  Nothing written.'
              % ('re-open' if undo else 'tick', title[:96]))
        return 0

    os.makedirs(ARCH, exist_ok=True)
    stamp = dt.datetime.now().strftime('%Y%m%d_%H%M')
    shutil.copy2(TODO, os.path.join(ARCH, 'matt_todo_%s.txt' % stamp))

    note = '' if undo else '   # DONE %s' % dt.date.today().strftime('%d %b %Y')
    lines[i] = new + lines[i][3:] + note
    open(TODO, 'w', encoding='utf-8').write('\n'.join(lines))

    # VERIFY THE ARTIFACT, NOT THE WRITE (0.2): read it back and count.
    back = open(TODO, encoding='utf-8').read().split('\n')
    if not back[i].startswith(new):
        print('  *** THE LINE DID NOT CHANGE ON DISK. Nothing else was done.')
        return 1
    print('  %s: %s' % ('re-opened' if undo else 'ticked', title[:96]))
    print('  %d open now.' % len(items(back, '[ ]')))

    sys.path.insert(0, HERE)
    import todo_page                                                       # noqa: E402
    return todo_page.main([])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
