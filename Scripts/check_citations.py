"""
check_citations.py -- does every finding this project CITES actually exist?

Doc 402, directive v9.25.  Directive 0.5(c)5 is the missing-ROW check: section 0.2
catches a thing that should not exist, and nothing caught a thing that SHOULD
exist and does not.  This is that check for the finding graph.

WHAT IT DOES.  Reads the SECTION 4 index out of 00_PROJECT_DIRECTIVE.md, which is
the authority for which finding ids exist, then greps every canonical file for
every section-4.x citation and reports the ones with no index row.

WHY IT EXISTS.  Two dangling citations were live and both wasted real time:
  section 4.23a  in DIRECTIVE_FINDINGS.md and DIRECTIVE_CHANGELOG.md
                 -> a typo for 4.23(a), "positional calibration"
  section 4.22e  in DIRECTIVE_DRAFT_BOOK.md
                 -> no (e) exists; 4.22 has (a), (b), (c).  The availability
                    haircut and the surfaced-not-scored decision are 4.22(c).
The first one was read as a MISSING FINDING during a reconcile and sent a session
looking for a body that was never absent.  The second sat in the draft book
unnoticed through ten directive versions.

NEGATIVE CONTROL.  --selftest injects both dead citations into a copy of the text
and asserts the checker reports exactly them.  A guard that has never been shown
to fire is not a guard (directive 0.2).

[doc 435] AND "doc N" CITATIONS, WHICH IT NEVER COVERED.  Eight numbers were cited in shipped
files with no document behind them (413, 414, 424, 426, 429, 430, 433, 434), and this checker
could not see any of them because it only read section-4 ids.  It now also reads every
"doc N" / "docs N, M" in the canonical files, the two to-do files, and every .py/.bat in
Scripts\ (top level and research\), and reports the numbers with no N_*.md in Source\.
Numbers below 200 are the pre-draft docs, which live on the drive only (some in _archive\),
so they are checked only when a file is found and never reported missing.

EXIT.  0 clean, 1 if any citation has no index row or no doc file.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('FF_SRC') or os.path.normpath(os.path.join(HERE, '..', 'Source'))
DIRECTIVE = '00_PROJECT_DIRECTIVE.md'
FILES = [DIRECTIVE, 'DIRECTIVE_FINDINGS.md', 'DIRECTIVE_DRAFT_BOOK.md',
         'DIRECTIVE_CHANGELOG.md', '00_START_HERE.md', 'METHOD_TRAPS.md']
CITE = re.compile(r'§(4\.\d+[a-z]?)')
DOC_CITE = re.compile(r'\b[Dd]ocs?\s+(\d{1,3}(?:\s*(?:,|and|/|to|through)\s*\d{1,3})*)')
DOC_MIN = 200          # the season's docs; 1 to 199 are pre-draft and partly archived
TODO_FILES = ['claude_todo.txt', 'matt_todo.txt']
SCRIPTS = os.environ.get('FF_SCRIPTS') or os.path.normpath(os.path.join(SRC, '..', 'Scripts'))


def index_ids(directive_text):
    m = re.search(r'\| id \| what it establishes.*?\n(?=\n*---\n)', directive_text, re.S)
    if not m:
        raise SystemExit("could not find the SECTION 4 index table in " + DIRECTIVE)
    ids = set(re.findall(r'^\|\s*\*\*(4\.\d+\w*)\*\*', m.group(0), re.M))
    if len(ids) < 20:
        raise SystemExit(f"only {len(ids)} finding ids parsed from the index -- refusing to run")
    return ids


BACKTICK = re.compile(r'`[^`\n]*`')


def strip_named(t):
    """Blank out backticked spans.

    A backticked id is being NAMED as a string -- `section 4.23a` in a retraction
    notice -- not cited.  Without this the checker flags its own changelog entry
    and the directive header every time a dead id is documented, which is doc
    376's cry-wolf failure: a guard that fires on correct text gets ignored.
    """
    return BACKTICK.sub(lambda m: ' ' * len(m.group(0)), t)


def scan(texts, valid):
    bad = {}
    for name, t in texts.items():
        for cid in CITE.findall(strip_named(t)):
            if cid not in valid:
                bad.setdefault(cid, {}).setdefault(name, 0)
                bad[cid][name] += 1
    return bad


def doc_numbers(src):
    """Every N with an N_*.md in Source (and in _archive, one level down, if present)."""
    nums = set()
    dirs = [src]
    arch = os.path.normpath(os.path.join(src, '..', '_archive'))
    if os.path.isdir(arch):
        dirs.append(arch)
        for d in os.listdir(arch):
            if os.path.isdir(os.path.join(arch, d)):
                dirs.append(os.path.join(arch, d))
    for d in dirs:
        try:
            for fn in os.listdir(d):
                m = re.match(r'(\d{1,3})_.*\.md$', fn)
                if m:
                    nums.add(int(m.group(1)))
        except OSError:
            pass
    return nums


def scan_docs(texts, have):
    bad = {}
    for name, t in texts.items():
        for span in DOC_CITE.findall(strip_named(t)):
            for n in re.findall(r'\d{1,3}', span):
                n = int(n)
                if n == 999 and '__p3__' not in name:
                    continue            # the selftest's own sentinel, quoted in this file and the changelog
                if n < DOC_MIN and n not in have:
                    continue            # pre-draft, drive-only: not this checker's job
                if n not in have:
                    bad.setdefault(n, {}).setdefault(name, 0)
                    bad[n][name] += 1
    return bad


def load_scripts():
    texts = {}
    for d in (SCRIPTS, os.path.join(SCRIPTS, 'research')):
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.lower().endswith(('.py', '.bat')):
                p = os.path.join(d, fn)
                try:
                    texts[os.path.relpath(p, SCRIPTS)] = open(p, encoding='utf-8', errors='replace').read()
                except OSError:
                    pass
    return texts


def load():
    texts = {}
    for f in FILES + TODO_FILES:
        p = os.path.join(SRC, f)
        if os.path.exists(p):
            texts[f] = open(p, encoding='utf-8', errors='replace').read()
    if DIRECTIVE not in texts:
        raise SystemExit(f"missing {os.path.join(SRC, DIRECTIVE)}")
    return texts


def report(bad, valid):
    if not bad:
        print("CITATIONS OK -- every section-4 citation resolves to an index row.")
        return 0
    print(f"DANGLING CITATIONS: {len(bad)}")
    for cid, where in sorted(bad.items()):
        near = sorted(v for v in valid if v.startswith(cid[:4].rstrip('.')))
        print(f"  section {cid}  in {', '.join(f'{k} x{v}' for k, v in where.items())}")
        print(f"      no index row. nearest real id(s): {near or 'none'}")
    print("\nA citation is not a finding. Fix the citation, or write the finding and index it.")
    return 1


def report_docs(bad, nfiles):
    if not bad:
        print(f"DOC CITATIONS OK -- every 'doc N' (N >= {DOC_MIN}) in {nfiles} files has a file in Source.")
        return 0
    print(f"DANGLING DOC NUMBERS: {len(bad)}")
    for n, where in sorted(bad.items()):
        print(f"  doc {n}  cited in {', '.join(f'{k} x{v}' for k, v in where.items())}")
        print(f"      no {n}_*.md in Source. Write the doc, or strike the citation.")
    return 1


def main():
    texts = load()
    valid = index_ids(texts[DIRECTIVE])
    have = doc_numbers(SRC)
    alltexts = dict(texts)
    alltexts.update(load_scripts())

    if '--selftest' in sys.argv:
        print(f"--- NEGATIVE CONTROL: {len(valid)} valid ids ---")
        fake, real = '4.99z', sorted(valid)[0]
        probe = dict(texts)
        probe['__probe__'] = f"a citation to \u00a7{fake} and one to \u00a7{real}\n"
        bad = scan(probe, valid)
        assert fake in bad and '__probe__' in bad[fake], \
            f"checker FAILED to flag the injected dead id \u00a7{fake}"
        assert real not in bad, f"checker wrongly flagged the valid id \u00a7{real}"
        probe2 = dict(texts)
        probe2['__probe2__'] = f"a retraction naming `\u00a7{fake}` in backticks\n"
        bad2 = scan(probe2, valid)
        assert '__probe2__' not in bad2.get(fake, {}), \
            f"checker flagged a BACKTICKED \u00a7{fake}, which is a name, not a citation"
        print(f"  injected dead \u00a7{fake}    bare        -> flagged      OK")
        print(f"  injected live \u00a7{real}   bare        -> not flagged  OK")
        print(f"  injected dead \u00a7{fake}    backticked  -> not flagged  OK")
        print("SELFTEST PASSED: fires on a bare dead id; silent on a live one and on a named one.\n")
        # [doc 435] the doc-number half: a dead number fires, a live one and a backticked one do not
        live_doc = max(have)
        probe3 = {'__p3__': f"see doc 999 and doc {live_doc}, and a name `doc 999` in backticks\n"}
        bad3 = scan_docs(probe3, have)
        assert 999 in bad3 and bad3[999]['__p3__'] == 1, "checker FAILED to flag the injected doc 999 exactly once"
        assert live_doc not in bad3, f"checker wrongly flagged the live doc {live_doc}"
        print(f"  injected dead doc 999   bare        -> flagged      OK")
        print(f"  injected live doc {live_doc}   bare        -> not flagged  OK")
        print(f"  injected dead doc 999   backticked  -> not flagged  OK")
        print("SELFTEST PASSED: fires on a bare dead doc number; silent on a live one and on a named one.\n")

    print(f"--- {len(valid)} finding ids in the index, scanning {len(texts)} files ---")
    rc = report(scan(texts, valid), valid)
    print(f"--- {len(have)} doc files on disk, scanning {len(alltexts)} files for 'doc N' ---")
    rc2 = report_docs(scan_docs(alltexts, have), len(alltexts))
    return rc or rc2


if __name__ == '__main__':
    sys.exit(main())
