#!/usr/bin/env python3
r"""check_locals.py -- a local read before it is assigned, found without running the function (doc 448).

    py check_locals.py              scan the shipped scripts beside this file (the SCRIPTS list below)
    py check_locals.py a.py b.py    scan these files
    py check_locals.py --selftest   the defect that shipped on 29 Sept must fire; a correct function must not

WHY THIS EXISTS. On 29 Sept at 20:06 `wire.py` died in `main()` with UnboundLocalError: a call added at
doc 445 read `week` fourteen lines before the line that assigns it. The unit test had called the new
function directly and never walked `main()`, which needs ESPN and so is never run here (0.2: a test must
exercise the object production builds). No guard reads the ORDER of a function. This one does: for every
function in a file, every name that is local to it (assigned anywhere in its body) whose first READ comes
before its first WRITE in source order is reported, with both line numbers. Nested functions, lambdas and
comprehensions are their own scopes and are skipped (their reads run later, as closures). Names declared
global or nonlocal are skipped. Standard library only; the same on 3.11 and 3.12.

A hit is a defect or a loop-carried variable with no initial value, and the second is the first waiting to
happen. Exit 1 on any hit, 2 on a file that does not parse.
"""
import ast, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ['wire.py', 'sheet_engine.py', 'lineup.py', 'todo_page.py', 'make_online.py', 'lookahead_box.py',
           'spot.py', 'check_pages.py', 'check_page_logic.py', 'check_vintage.py', 'check_inputs.py',
           'check_citations.py', 'check_guards.py', 'check_kit.py', 'claim_order_log.py', 'make_commands.py',
           'check_page_rules.py', 'proj_due.py',
           os.path.join('research', 'build_inherit.py'), os.path.join('research', 'wk1', 'build_form.py'),
           os.path.join('research', 'wk1', 'build_lines.py'), os.path.join('research', 'wk1', 'build_depth_daily.py'),
           os.path.join('research', 'open_threads.py'), os.path.join('research', 'wk1', 'rookie_screen.py')]

SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp,
          ast.GeneratorExp, ast.ClassDef)


def _targets(node):
    """Names a statement binds in the CURRENT scope (not inside a nested scope)."""
    out = []
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            out.append((n.id, n.lineno))
    return out


def _walk_scope(body):
    """Yield (name, lineno, is_store) for the function body in source order, skipping nested scopes."""
    events = []

    def visit(node):
        if isinstance(node, SCOPES):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                events.append((node.name, node.lineno, True))       # the def binds its name here
                for d in node.decorator_list:
                    visit(d)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for d in node.args.defaults + node.args.kw_defaults:
                    if d is not None:
                        visit(d)
            if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                # the FIRST iterable of a comprehension is evaluated in the enclosing scope
                visit(node.generators[0].iter)
            return
        if isinstance(node, ast.Name):
            events.append((node.id, node.lineno, isinstance(node.ctx, (ast.Store, ast.Del))))
            return
        # evaluation order: for an assignment the value is read before the target is written
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
            if isinstance(node, ast.AugAssign):
                visit(node.value)
                events.append((node.target.id, node.lineno, False) if isinstance(node.target, ast.Name)
                              else (None, node.lineno, False))
                visit(node.target)
                return
            if getattr(node, 'value', None) is not None:
                visit(node.value)
            for t in ([node.target] if not isinstance(node, ast.Assign) else node.targets):
                visit(t)
            return
        if isinstance(node, (ast.For, ast.AsyncFor)):
            visit(node.iter); visit(node.target)
            for b in node.body + node.orelse:
                visit(b)
            return
        for child in ast.iter_child_nodes(node):
            visit(child)

    for stmt in body:
        visit(stmt)
    return [e for e in events if e[0] is not None]


def check_function(fn):
    declared = set()
    for n in ast.walk(fn):
        if isinstance(n, (ast.Global, ast.Nonlocal)):
            declared.update(n.names)
    params = {a.arg for a in fn.args.args + fn.args.kwonlyargs + fn.args.posonlyargs}
    if fn.args.vararg:
        params.add(fn.args.vararg.arg)
    if fn.args.kwarg:
        params.add(fn.args.kwarg.arg)
    events = _walk_scope(fn.body)
    # binds that are not Name nodes: an import, an except-as, a with-as. They take effect at their
    # own line, so they are merged into the event stream by line and treated as stores.
    extra = []
    for n in ast.walk(fn):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                extra.append(((a.asname or a.name).split('.')[0], n.lineno, True))
        if isinstance(n, ast.ExceptHandler) and n.name:
            extra.append((n.name, n.lineno, True))
        if isinstance(n, ast.withitem) and isinstance(n.optional_vars, ast.Name):
            extra.append((n.optional_vars.id, n.optional_vars.lineno, True))
    # ORDER IS EVALUATION ORDER, NOT LINE ORDER: a walrus in the test of a conditional expression runs
    # before the body that reads it even when the body sits on an earlier line. The extra binds are
    # slotted in by line, which is exact for them (each is a statement head).
    seq = list(events)
    for e in extra:
        pos = next((i for i, ev in enumerate(seq) if ev[1] > e[1]), len(seq))
        seq.insert(pos, e)
    locals_ = {name for name, _, is_store in seq if is_store}
    first_store, first_read = {}, {}
    for idx, (name, line, is_store) in enumerate(seq):
        if name in params or name in declared or name not in locals_:
            continue
        if is_store:
            first_store.setdefault(name, (idx, line))
        else:
            first_read.setdefault(name, (idx, line))
    hits = []
    for name, (ridx, rline) in first_read.items():
        sidx, sline = first_store[name]
        if ridx < sidx:
            hits.append((name, rline, sline))
    return hits


def check_file(path):
    src = open(path, encoding='utf-8').read()
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError as exc:
        return None, exc
    out = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for name, r, w in check_function(n):
                out.append((n.name, name, r, w))
    return out, None


SELFTEST_BAD = '''
def main():
    data = {'scoringPeriodId': 4}
    rosters = None
    depth = [1, 2]
    log(depth, week)                       # read on this line ...
    week = data.get('scoringPeriodId') or 0   # ... assigned on this one
    return week
'''
SELFTEST_GOOD = '''
import os
def main(argv=None):
    data = {'scoringPeriodId': 4}
    week = data.get('scoringPeriodId') or 0
    rows = [w for w in range(week)]
    total = 0
    for r in rows:
        total += r
    f = lambda x: x + total
    def inner():
        return week
    try:
        v = int('3')
    except ValueError as exc:
        v = 0
    with open(os.devnull) as fh:
        text = fh.read()
    return f(v), inner(), text, [r for r in rows if r > total]
'''


def selftest():
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as d:
        pb = os.path.join(d, 'bad.py'); open(pb, 'w').write(SELFTEST_BAD)
        pg = os.path.join(d, 'good.py'); open(pg, 'w').write(SELFTEST_GOOD)
        hits, _ = check_file(pb)
        fired = any(h[1] == 'week' for h in hits)
        print('  %-4s the 29 Sept defect (week read before it is assigned) fires: %s' % ('ok' if fired else 'BAD', hits))
        ok &= fired
        hits, _ = check_file(pg)
        quiet = not hits
        print('  %-4s a correct function with a loop, a lambda, a nested def, a try, a with and comprehensions '
              'stays quiet: %s' % ('ok' if quiet else 'BAD', hits))
        ok &= quiet
    print('selftest: %s' % ('both controls behaved' if ok else 'FAILED'))
    return 0 if ok else 1


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if '--selftest' in argv:
        return selftest()
    files = argv or [os.path.join(HERE, s) for s in SCRIPTS]
    bad = 0; parsed = 0
    for f in files:
        if not os.path.exists(f):
            print('  missing   %s' % f); continue
        hits, err = check_file(f)
        if err:
            print('  NO PARSE  %s: %s' % (f, err)); bad = 2; continue
        parsed += 1
        for fn, name, r, w in hits:
            print('  HIT       %s: %s() reads `%s` on line %d, first assigned on line %d' % (os.path.relpath(f, HERE), fn, name, r, w))
            bad = bad or 1
    print('check_locals: %d file(s) parsed, %s' % (parsed, 'no local is read before it is assigned' if not bad else 'FAIL'))
    return bad


if __name__ == '__main__':
    sys.exit(main())
