r"""check_inputs.py -- WHAT DO WE HAVE THAT NOTHING USES?

[doc 433] Matt, 25 Sept, after six defects in one evening that he found and no guard did:
"how should i have confidence now that the all values are in use that need to be, and that the
correct signals, and all the signals are measured"

His question splits into three and only the first is mechanical. This script answers that one.

  1. ARE THE INPUTS USED?      mechanical. This script. It found the red zone files unread.
  2. ARE THE SIGNALS CORRECT?  partly. Findings not cited in any script are listed, but a citation
                               is not an implementation and a null is CORRECTLY unwired, so this
                               half needs a human read of the list it prints.
  3. ARE ALL SIGNALS MEASURED? NOT ANSWERABLE. You cannot enumerate what nobody thought of. The
                               only instrument is 0.5(c)6's outside check and a human spot-checking
                               one player, which is how all six of tonight's defects were found.

Run it from Scripts\. No network, no ESPN. Prints, and exits 1 if a NAMED decision input is unread.
    py check_inputs.py --selftest   the negative controls for the display-only list, touch nothing
"""
import os, sys, csv, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'Source')

# Files whose columns are supposed to reach a DECISION. A file here that nothing reads is a defect,
# not a curiosity: it means we measured something and then did not use it.
# redzone_te_2025.csv left this list on 29 Sept (doc 441, finding 4.41): it is in DISPLAY_ONLY below.
DECISION_INPUTS = ['form_2026.csv', 'MY_ROSTER.csv', 'inherit_2026.csv', 'LEAGUE_ROSTERS.csv']
# The engine that actually builds THE CALL. A signal that never appears HERE never moves a pick,
# even when another script reads the file (wire.py reads the red zone and the sheet never saw it).
DECIDER = 'sheet_engine.py'

# A file can reach the decision WITHOUT the decider naming it, when another script turns it into a
# derived object that IS passed in. That is legitimate and this check cannot see it, so each one is
# acknowledged here BY NAME with its route. An empty reason is not allowed: if nobody can say how it
# reaches a pick, it does not, and it belongs in the defect list.
INDIRECT = {
    'LEAGUE_ROSTERS.csv': 'wire.py turns it into the free pool, and the free pool IS passed to the sheet',
}

# A file that is READ and PRINTED but, by a MEASUREMENT, must NOT reach the decision. This is the
# opposite of INDIRECT: the decider not touching it is the correct state, and the decider starting
# to touch it would be the defect (a null got wired). Each entry names the finding that measured it,
# so the exemption cannot outlive its reason: when the finding is retracted, this row goes with it.
# Two things are still checked for a file here, and either one failing is a real defect:
#   * something must still READ it (a display column nobody renders is a dead file, retire it);
#   * the decider must NOT touch it (the finding says nothing sorts on it).
DISPLAY_ONLY = {
    'redzone_te_2025.csv': ('doc 441, finding 4.41: red-zone usage is already inside expected points '
                            '(zero net of the two-game expected and snap share), so it is DISPLAY ONLY and '
                            'nothing sorts on it. It is last season\'s file with no 2026 builder; wire.py '
                            'prints it beside the tight ends and that is the whole of its job'),
}


def _touched(fn, read, allcols, dec):
    """Does the DECIDER touch this file: its stem, or a column that belongs to this file alone?
    A GENERIC COLUMN IS NOT EVIDENCE. `espn_id`, `player` and `name` appear in every file and in
    every script, so asking "does the decider mention any column of this file" passes for a file
    nothing reads. The first cut of this check did exactly that and let redzone_te_2025.csv through
    while sheet_engine.py has never contained the words "red zone". Evidence is the FILENAME, or a
    column that belongs to this file alone."""
    stem = os.path.splitext(fn)[0]
    uniq = [c for c in read if sum(1 for o in allcols.values() if c in o) == 1]
    return (stem.lower() in dec.lower()
            or any(re.search(r"['\"]" + re.escape(c) + r"['\"]", dec) for c in uniq))


def index_ids():
    """Every finding id in the directive's SECTION 4 index table (rows starting "| **4."), in order.
    Falls back to 4.1..4.37 if the directive is not beside this script's Source."""
    src = os.path.join(SRC, '00_PROJECT_DIRECTIVE.md')
    try:
        txt = open(src, encoding='utf-8').read()
    except OSError:
        return ['4.%d' % n for n in range(1, 38)]
    ids = re.findall(r'^\| \*\*(4\.\d+[a-z]?)\*\* \|', txt, re.M)
    return ids or ['4.%d' % n for n in range(1, 38)]


# Scripts that PRINT every column of every file by design and so are not evidence that a column is
# used: spot.py (the spot-check card) names columns in order to show them, never to decide on them.
# Counting it would let a column pass this check because a card can display it.
NOT_A_CONSUMER = {'spot.py'}


def load_code():
    out = {}
    for root, dirs, fs in os.walk(os.path.join(ROOT, 'Scripts')):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in fs:
            if f in NOT_A_CONSUMER:
                continue
            if f.endswith(('.py', '.bat')):
                p = os.path.join(root, f)
                try:
                    out[p] = open(p, encoding='utf-8', errors='replace').read()
                except OSError:
                    pass
    return out


def header(p):
    with open(p, encoding='utf-8-sig', errors='replace') as fh:
        rows = csv.reader(fh)
        h = next(rows, [])
        if os.path.basename(p).startswith('RedZone'):   # two header rows
            h = next(rows, [])
    return [c.strip() for c in h if c.strip()]


def audit(code, quiet=False):
    """The per-file check on one set of scripts. Returns the defect list, so the selftest can run it
    on a mutated set of scripts and assert that it fires (0.2: a guard never executed is not a guard)."""
    say = (lambda *a: None) if quiet else print
    blob = '\n'.join(code.values())
    dec = next((c for p, c in code.items() if os.path.basename(p) == DECIDER), '')
    if not dec:
        sys.exit(f'FAILED: {DECIDER} not found. This check is meaningless without it.')
    bad = []
    names = sorted(set(DECISION_INPUTS) | set(DISPLAY_ONLY)
                   | {f for f in os.listdir(SRC) if f.lower().startswith('redzone')})
    allcols = {n: header(os.path.join(SRC, n)) for n in names if os.path.exists(os.path.join(SRC, n))}
    say(f"{'file':<30}{'cols read':>10}   unread")
    for fn in names:
        p = os.path.join(SRC, fn)
        if not os.path.exists(p):
            say(f'{fn:<30}{"ABSENT":>10}')
            continue
        h = header(p)
        read = [c for c in h if re.search(r"['\"]" + re.escape(c) + r"['\"]", blob)]
        un = [c for c in h if c not in read]
        say(f'{fn:<30}{len(read):>4}/{len(h):<5}   {", ".join(un[:8]) if un else "-"}')
        if fn in DECISION_INPUTS and not read:
            bad.append(f'{fn}: nothing in any script reads a single column')
        touched = _touched(fn, read, allcols, dec)
        if fn in DISPLAY_ONLY:
            # the exemption is checked, not trusted: it must still be read, and the decider must
            # still be clear of it, or the finding it rests on is being contradicted by the code
            if not read:
                bad.append(f'{fn}: display only, and nothing reads it any more, so it is a dead file: '
                           f'retire it or restore the display')
            elif touched:
                bad.append(f'{fn}: display only ({DISPLAY_ONLY[fn].split(":")[0]} says nothing sorts on it), '
                           f'but {DECIDER} touches it now. Either the finding is superseded, so move this '
                           f'file to DECISION_INPUTS with the new doc, or a null got wired')
            else:
                say(f'{"":<30}{"":>10}   display only, by measurement: {DISPLAY_ONLY[fn]}')
            continue
        if read and not touched:
            if fn in INDIRECT:
                say(f'{"":<30}{"":>10}   reaches the decision indirectly: {INDIRECT[fn]}')
            else:
                bad.append(f'{fn}: read somewhere, but {DECIDER} never touches it, so no pick moves')
    return bad, blob


def selftest():
    """Negative controls for DISPLAY_ONLY, on the real Source and a synthetic pair of scripts.
    Nothing is written."""
    print('--- NEGATIVE CONTROLS (0.2: a guard never executed is not a guard) ---')
    fn = 'redzone_te_2025.csv'
    if not os.path.exists(os.path.join(SRC, fn)):
        sys.exit(f'selftest needs Source\\{fn} beside this script')
    cols = header(os.path.join(SRC, fn))
    lit = ', '.join(f"'{c}'" for c in cols)
    dec_path = os.path.join(HERE, DECIDER)
    # 1. the real code passes for this file (the case the exemption exists for)
    bad, _ = audit(load_code(), quiet=True)
    assert not any(b.startswith(fn) for b in bad), f'control 1 FAILED: the real code flags {fn}: {bad}'
    print(f'  1. real scripts           -> {fn} passes as display only           OK')
    # 2. the decider starts touching the display-only file: must fire (a null got wired)
    code = {dec_path: f"x = {lit}\nrz = 'redzone_te_2025'\n", os.path.join(HERE, 'wire.py'): f'y = {lit}\n'}
    bad, _ = audit(code, quiet=True)
    assert any(b.startswith(fn) and 'touches it now' in b for b in bad), f'control 2 FAILED: {bad}'
    print(f'  2. decider touches it     -> fires: "{[b for b in bad if b.startswith(fn)][0][:60]}..."  OK')
    # 3. nothing reads the display-only file any more: must fire (a dead file)
    code = {dec_path: "x = 1\n", os.path.join(HERE, 'wire.py'): "y = 1\n"}
    bad, _ = audit(code, quiet=True)
    assert any(b.startswith(fn) and 'dead file' in b for b in bad), f'control 3 FAILED: {bad}'
    print(f'  3. nothing reads it       -> fires: "{[b for b in bad if b.startswith(fn)][0][:60]}..."  OK')
    # 4. a display-only entry with no reason is not allowed
    assert all(v.strip() for v in DISPLAY_ONLY.values()), 'control 4 FAILED: a DISPLAY_ONLY entry has no reason'
    print('  4. every DISPLAY_ONLY row -> carries its reason                       OK')
    print('\nSELFTEST PASSED. Nothing was written.\n')
    return 0


def main():
    code = load_code()
    print(f'scanned {len(code)} scripts\n')
    bad, blob = audit(code)

    print('\nfindings never cited in any script (a citation is NOT an implementation, and a')
    print('measured NULL is correctly unwired -- read this list, do not act on it blind):')
    # doc 440: the ids come from the directive's SECTION 4 index (4.1 to whatever is newest, lettered
    # ones included), never a hand-typed list that stops at 4.36; and the pattern carries a LEFT
    # boundary, because 4.4 used to pass on "14.4" and 4.7 on "+14.7" (two false negatives).
    ids = index_ids()
    miss = [i for i in ids if not re.search(r'(?<![\d.])[§S]?' + re.escape(i) + r'(?![\d])', blob)]
    print('  ' + (', '.join(miss) if miss else 'none'))

    if bad:
        print('\n*** ' + str(len(bad)) + ' INPUT DEFECT(S):')
        for b in bad:
            print('   ' + b)
        sys.exit(1)
    print('\nevery decision input reaches the decider.')


if __name__ == '__main__':
    sys.exit(selftest() if '--selftest' in sys.argv else main())
