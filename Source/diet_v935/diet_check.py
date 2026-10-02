#!/usr/bin/env python3
r"""diet_check.py -- prove the v9.35 diet moved words and did not lose them (doc 444).

    py diet_check.py            reads ..\00_PROJECT_DIRECTIVE.md (v9.34, the live file) and the two files
                                beside this script (the proposed v9.35 directive and changelog)

THE CLAIM IT TESTS: every word of the v9.34 directive is in the v9.35 directive or in the changelog's
"CASE HISTORIES MOVED OUT AT v9.35" section, as a multiset, once the listed rewrites (the header
paragraph, the claim-order line, the three index rows and the added one, six markup repairs) are reversed. And the moved
section holds every passage exactly as it stood. Standard library only.
"""
import collections, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)                                   # Source\
LIVE = os.path.join(SRC, '00_PROJECT_DIRECTIVE.md')
NEW = os.path.join(HERE, '00_PROJECT_DIRECTIVE.md')
CHG = os.path.join(HERE, 'DIRECTIVE_CHANGELOG.md')
META = os.path.join(HERE, 'proposed_meta.json')

def words(t):
    return re.findall(r'\S+', t)

def main():
    for p in (LIVE, NEW, CHG, META):
        if not os.path.exists(p):
            sys.exit('missing: ' + p)
    before = open(LIVE, encoding='utf-8').read()
    after = open(NEW, encoding='utf-8').read()
    chg = open(CHG, encoding='utf-8').read()
    meta = json.load(open(META, encoding='utf-8'))
    if 'v9.34' not in before.split('\n', 1)[0]:
        sys.exit('the live directive is not v9.34; this check was written against v9.34')
    # 1. reverse the listed rewrites on the proposed text
    rev = after
    pairs = [(meta['hdr_new'], meta['hdr_old']), (meta['blk_new'], meta['blk_old']),
             (meta['row35_new'], meta['row35_old']), (meta['row36_new'], meta['row36_old'])]
    pairs += [(n, o) for o, n in meta['reps']]
    pairs += [('(v9.35)\n', '(v9.34)\n'), ('every entry v5.4 through v9.35,', 'every entry v5.4 through v9.34,')]
    pairs += [tuple(x) for x in meta.get('pairs', [])]          # doc 445: the 4.38 row and the findings count
    for ins in meta.get('inserts', []):                          # doc 445: the 4.42 row, an insertion
        if rev.count(ins + '\n') != 1:
            sys.exit('inserted row not found exactly once: %r' % ins[:60])
        rev = rev.replace(ins + '\n', '')
    for n, o in pairs:
        if rev.count(n) != 1:
            sys.exit('rewrite not found exactly once in the proposed directive: %r' % n[:60])
        rev = rev.replace(n, o)
    # 2. every moved passage sits verbatim in the changelog's new section
    sec = chg.split('# CASE HISTORIES MOVED OUT AT v9.35', 1)
    if len(sec) != 2:
        sys.exit('the changelog has no CASE HISTORIES MOVED OUT AT v9.35 section')
    sec = sec[1]
    bad = [lab for lab, txt in meta['moved'] if txt.strip() not in sec]
    if bad:
        sys.exit('moved passages missing from the changelog: ' + '; '.join(bad))
    # 3. the multiset
    got = collections.Counter(words(rev))
    for lab, txt in meta['moved']:
        got.update(words(txt))
    want = collections.Counter(words(before))
    lost = want - got
    gained = got - want
    n_moved = sum(len(words(t)) for _, t in meta['moved'])
    print('v9.34 directive: %d words; v9.35: %d words; moved: %d words in %d passages'
          % (sum(want.values()), len(words(after)), n_moved, len(meta['moved'])))
    if lost or gained:
        print('LOST from v9.34:', dict(list(lost.items())[:20]))
        print('GAINED in v9.35 outside the listed rewrites:', dict(list(gained.items())[:20]))
        return 1
    print('every word of v9.34 is in v9.35 or in the changelog section, and nothing was added outside the listed rewrites')
    return 0

def selftest():
    """Two negative controls: a word deleted from the proposed directive, and a moved passage deleted
    from the changelog. Both must fail. Run against copies in a temporary folder; nothing is written."""
    import shutil, tempfile, subprocess
    fails = 0
    for what in ('word', 'passage'):
        d = tempfile.mkdtemp()
        sub = os.path.join(d, 'diet_v935'); os.makedirs(sub)
        shutil.copy(LIVE, os.path.join(d, '00_PROJECT_DIRECTIVE.md'))
        for f in ('00_PROJECT_DIRECTIVE.md', 'DIRECTIVE_CHANGELOG.md', 'proposed_meta.json', 'diet_check.py'):
            shutil.copy(os.path.join(HERE, f), os.path.join(sub, f))
        if what == 'word':
            t = open(os.path.join(sub, '00_PROJECT_DIRECTIVE.md'), encoding='utf-8').read()
            t = t.replace('Every reply opens with a numbered do-this list', 'Every reply opens with a do-this list', 1)
            open(os.path.join(sub, '00_PROJECT_DIRECTIVE.md'), 'w', encoding='utf-8', newline='').write(t)
        else:
            m = json.load(open(os.path.join(sub, 'proposed_meta.json'), encoding='utf-8'))
            t = open(os.path.join(sub, 'DIRECTIVE_CHANGELOG.md'), encoding='utf-8').read()
            t = t.replace(m['moved'][3][1].strip(), '', 1)
            open(os.path.join(sub, 'DIRECTIVE_CHANGELOG.md'), 'w', encoding='utf-8', newline='').write(t)
        r = subprocess.run([sys.executable, os.path.join(sub, 'diet_check.py')], capture_output=True, text=True)
        ok = r.returncode != 0
        print('  %-4s a %s deleted -> exit %d (must be non-zero)' % ('ok' if ok else 'BAD', what, r.returncode))
        fails += 0 if ok else 1
        shutil.rmtree(d, ignore_errors=True)
    print('selftest: %s' % ('both controls fired' if not fails else '%d control(s) did not fire' % fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(selftest() if '--selftest' in sys.argv else main())
