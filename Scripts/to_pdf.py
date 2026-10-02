#!/usr/bin/env python3
r"""
to_pdf.py -- turn the freshly built HTML pages into the PDFs you print.

    py to_pdf.py           rebuild every printout whose PDF is older than its page
    py to_pdf.py --check   just tell me which printouts are out of date
    py to_pdf.py --all     rebuild all of them even if they look current

WHY THIS EXISTS (doc 146, and it is a live defect, not a tidy-up).
Every builder in this project -- make_board, make_fallback, mkvalue, mkoverride, make_sheets --
writes an .html page and then shells out to `wkhtmltopdf` to turn it into the PDF that actually
gets printed. **wkhtmltopdf is not installed on this machine.** Proof, from the Sept 3 console:

    py make_fallback.py
    wkhtmltopdf not on PATH. Wrote ...\Source\FALLBACK_BOARD.html -- open it and print to PDF.

    py mkvalue.py
    TypeError: expected str, bytes or os.PathLike object, not NoneType     <-- exe was None

So on this machine every rebuild silently updates the PAGE and leaves the PDF where it was.
DRAFT_BOARD.pdf was Sept 1 while DRAFT_BOARD.html was current, and `sync_desk_copies.py`
cheerfully copied the Sept 1 PDF to the desk and printed "OK" with a byte count. That is doc
109's failure -- the paper cannot follow the board -- rebuilt as an automatic process.

THE FIX NEEDS NO INSTALL. Chrome (and Edge, which is on every Windows box) will print a local
page to PDF from the command line. This script tries wkhtmltopdf first in case it ever does get
installed, then Chrome, then Edge. If none of the three is found it says so in one line and names
the pages to print by hand -- it never pretends it succeeded.

WHAT IT WILL AND WILL NOT TOUCH. Only the four printouts named in PAGES below -- the ones a
script rebuilds when the board changes. Two things are deliberately excluded, each for its own
reason, and both reasons are written next to the list.
"""
import argparse, glob, os, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))

# (PDF name in Source\,  the page it is made from,  what it is in plain words)
# Most pages sit next to their PDF in Source\. The card and the guide are the two exceptions --
# they are written by hand in Scripts\ -- so their source page is named explicitly rather than
# assumed, which is how DRAFT_CARD.pdf came to be older than card.html and nobody noticed.
PAGES = [
    ('DRAFT_BOARD',      'Source/DRAFT_BOARD.html',    'the board you draft from -- one row per player'),
    ('VALUE_LADDER',     'Source/VALUE_LADDER.html',   'where the board, the analysts and the depth chart agree'),
    ('FALLBACK_BOARD',   'Source/FALLBACK_BOARD.html', 'the paper backup, if the live tool dies'),
    ('OVERRIDE_CARD',    'Source/OVERRIDE_CARD.html',  'the few players the board cannot show correctly'),
    # doc 163: HOW_TO_READ_IT was on the DESK (sync_desk_copies DOCS) and in NEITHER rebuild
    # path -- not here, and make_howto.py was never called by sept5_after.bat.  So editing
    # live_draft.COLGLOSS changed the board and left the page explaining it frozen, with no
    # guard firing: sync's 'PDF older than its page' check cannot catch a page that was never
    # rebuilt either.  Doc 146's defect in a fifth place.  Both halves are fixed together.
    ('HOW_TO_READ_IT',   'Source/HOW_TO_READ_IT.html', 'how to read the live board -- generated FROM live_draft.COLGLOSS'),
]
# DELIBERATELY NOT IN THAT LIST: DRAFT_CARD and DRAFT_DAY_GUIDE.
# They ARE built from Scripts\card.html and Scripts\guide.html -- verified, not assumed: every
# one of the 364 distinct words in DRAFT_CARD.pdf appears in card.html. But card.html declares
# `@page{size:Letter landscape}` while the PDF on the desk is PORTRAIT, because whoever built it
# ran wkhtmltopdf without -O Landscape. Chrome honours the CSS, so rebuilding the card here would
# silently turn the two-page portrait card Matt has already read into a landscape one, four days
# out, for no gain: nothing in the Saturday refresh changes their content.
# If the card ever does need rebuilding, that is a decision, not a side effect of this script.

CHROME_CANDIDATES = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    os.path.join(os.environ.get('LOCALAPPDATA', ''), r'Google\Chrome\Application\chrome.exe'),
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
]


def find_renderer():
    """(kind, path) for the first thing that can make a PDF, or (None, None)."""
    exe = shutil.which('wkhtmltopdf')
    if exe:
        return 'wkhtmltopdf', exe
    for name in ('chrome', 'google-chrome', 'chromium', 'msedge'):
        exe = shutil.which(name)
        if exe:
            return 'chrome', exe
    for p in CHROME_CANDIDATES:
        if p and os.path.exists(p):
            return 'chrome', p
    return None, None


ZOOM = 0.78     # see the note in render() -- measured against wkhtmltopdf, not chosen


def render(kind, exe, html, pdf):
    """Returns None on success, else a one-line reason."""
    tmp = None
    if kind == 'wkhtmltopdf':
        cmd = [exe, '--enable-local-file-access', '--quiet', '-s', 'Letter', html, pdf]
    else:
        # A separate profile directory matters: without it Chrome hands the job to the copy of
        # itself Matt already has open and returns instantly having written nothing.
        prof = tempfile.mkdtemp(prefix='ff2026_pdf_')
        # ZOOM: every page in this project was laid out against wkhtmltopdf, which assumes a
        # 1024px-wide page. Chrome maps 1 CSS pixel to 1/96 inch, so the same page comes out
        # bigger and runs onto more sheets -- the draft board went from 7 pages to 12, a 70%
        # increase in paper for the document Matt reads at the table. MEASURED, not guessed:
        # sweeping the zoom against wkhtmltopdf's own output, 0.78 reproduces its page count
        # EXACTLY on all three pages that exist today -- board 7=7, ladder 3=3, backup 2=2.
        # (816/1024 = 0.797, so the constant is the page-width ratio, not a fudge.)
        # The scale is injected into a COPY beside the original, so the original is untouched
        # and any relative link in it still resolves.
        tmp = os.path.join(os.path.dirname(os.path.abspath(html)),
                           '~topdf_' + os.path.basename(html))
        with open(html, encoding='utf-8', errors='replace') as f:
            body = f.read()
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(body + '\n<style>html{zoom:%s}</style>\n' % ZOOM)
        url = 'file:///' + os.path.abspath(tmp).replace('\\', '/')
        cmd = [exe, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
               f'--user-data-dir={prof}', f'--print-to-pdf={pdf}', url]
        if os.name != 'nt':
            # Linux-as-root (the test container) refuses to start without this. Windows does
            # not need it, and it is deliberately NOT passed there.
            cmd.insert(1, '--no-sandbox')
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return 'the renderer did not finish inside three minutes'
    except Exception as e:
        return str(e)
    finally:
        if tmp:
            try:
                os.remove(tmp)
            except OSError:
                pass
    if not os.path.exists(pdf):
        tail = (r.stderr or r.stdout or '').strip().splitlines()
        return (tail[-1] if tail else 'no PDF was produced and nothing was said about why')
    # An 11-byte "PDF" is what a shell-redirect accident produces (doc 84). Refuse to call it done.
    if os.path.getsize(pdf) < 4096:
        return f'wrote only {os.path.getsize(pdf)} bytes -- that is not a PDF'
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='report only, change nothing')
    ap.add_argument('--all', action='store_true', help='rebuild even the ones that look current')
    ap.add_argument('--src', default=SRC)
    a = ap.parse_args(argv)

    root = os.path.normpath(os.path.join(HERE, '..'))
    todo, missing, current = [], [], []
    for base, page, why in PAGES:
        html = os.path.normpath(os.path.join(root, page))
        pdf = os.path.join(a.src, base + '.pdf')
        if not os.path.exists(html):
            missing.append((base, page))
            continue
        if a.all or not os.path.exists(pdf) or os.path.getmtime(pdf) < os.path.getmtime(html) - 1:
            todo.append((base, why, html, pdf))
        else:
            current.append((base, why))

    print()
    print('  PRINTOUTS')
    for base, why in current:
        print(f'    up to date   {base:<16} {why}')
    for base, why, _h, p in todo:
        age = 'never built' if not os.path.exists(p) else \
              f'PDF is {(os.path.getmtime(_h) - os.path.getmtime(p)) / 3600:.1f} h older than the page'
        print(f'    OUT OF DATE  {base:<16} {age}')
    for base, page in missing:
        print(f'    no page      {base:<16} ({page} is not there -- nothing to make it from)')

    if not todo:
        print('\n  Nothing to rebuild. Every printout matches the page it came from.')
        return 0
    if a.check:
        print(f'\n  {len(todo)} printout(s) out of date. Run  py to_pdf.py  to rebuild them.')
        return 0

    kind, exe = find_renderer()
    if not exe:
        print('\n  *** No PDF maker found on this machine. ***')
        print('  Not wkhtmltopdf, not Chrome, not Edge. Nothing was changed.')
        print('  Open each page below in your browser and press Ctrl+P -> Save as PDF,')
        print('  saving over the file of the same name:')
        for base, _w, h, _p in todo:
            print('     ', h)
        print('  Then run  py to_pdf.py --check  again to confirm they are current.')
        return 1

    print(f'\n  Making PDFs with: {os.path.basename(exe)}')
    failed = []
    for base, why, html, pdf in todo:
        t0 = time.time()
        err = render(kind, exe, html, pdf)
        if err:
            failed.append((base, html))
            print(f'    FAILED   {base:<16} {err}')
        else:
            print(f'    rebuilt  {base:<16} {os.path.getsize(pdf):,} bytes '
                  f'({time.time() - t0:.1f}s)')

    print()
    if failed:
        print('  *** AT LEAST ONE PRINTOUT DID NOT REBUILD ***')
        print('  The old PDF is still sitting there, which means it is now WRONG.')
        print('  Open the page and print it by hand rather than trusting the old file:')
        for base, h in failed:
            print('     ', h)
        return 1
    print(f'  {len(todo)} printout(s) rebuilt. Now run  py sync_desk_copies.py  to put them')
    print('  on your desk, then re-run  py make_shortcuts.py  so the Desktop links re-point.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
