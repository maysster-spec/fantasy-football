#!/usr/bin/env python3
r"""
make_sheets.py -- rebuild the three paper companion sheets from current data.

    py make_sheets.py

    AUDITION_WINDOW.pdf   picks 56 / 65 / 80 / 89 -- the keeper-audition window
    LATE_RB_SHEET.pdf     picks 104 / 113 / 128 / 137 -- direct backups
    ANALYST_CALLS.pdf     every player with a podcast call, inside reach

Doc 109. These three were built by hand in a chat, which is exactly the failure FALLBACK_BOARD
had: when the board changed, the paper could not follow. `refresh_adp.py` moves every `goes at`
on all three, so they need a builder. Run this after ANY board change.

Reads: live_draft\board_v8_fixed.csv, depth_map.csv, live_draft\player_context.csv,
       analyst_calls_joined.csv (optional).  Writes into ..\Source\.
"""
import html, os, shutil, subprocess, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, 'live_draft')
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
SKILL = [8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137]

CSS = """@page{margin:0}
body{font:10.4pt/1.28 "Segoe UI",Arial,sans-serif;color:#15181d;margin:0;padding:6mm 7mm}
h1{font-size:16.5pt;margin:0 0 2pt;color:#8f1d1d}
.sub{font-size:9.2pt;color:#5c646f;margin:0 0 7pt}
table{border-collapse:collapse;width:100%;font-size:9.4pt}
th{background:#eceff3;border-bottom:1.5px solid #99a;text-align:left;padding:3pt 4pt;font-size:8.5pt}
td{padding:2.6pt 4pt;border-bottom:1px solid #e6e8ec;vertical-align:top}
tr:nth-child(even) td{background:#f8f9fb}
.n{text-align:right;white-space:nowrap}.p{font-weight:700;white-space:nowrap}
.tk{color:#12734f;font-weight:700;white-space:nowrap}.wv{color:#8a929e}
.st{background:#e7f4ec;color:#12734f;font-weight:700;font-size:8pt;padding:1pt 4pt;border-radius:3px}
.bk{color:#8a929e;font-size:8.6pt}
.buy{background:#e7f4ec;color:#12734f;font-weight:700;font-size:8pt;padding:1pt 4pt;border-radius:3px}
.av{background:#fbecea;color:#a11f1a;font-weight:700;font-size:8pt;padding:1pt 4pt;border-radius:3px}
.q{font-size:8.8pt;color:#25292f;font-style:italic}
.jc{color:#b3261e;font-weight:700;font-size:8.4pt}
.jt{color:#9a6212;font-weight:700;font-size:8.4pt}
.jg{color:#12734f;font-weight:700;font-size:8.4pt}
.k{background:#fbf6e8;border-left:3px solid #d8a127;padding:5pt 8pt;margin:0 0 7pt;font-size:9.5pt}"""


def when(e):
    c = [p for p in SKILL if p <= float(e) + 0.5]
    if not c: return ('gone by 8', 'wv')
    if float(e) > SKILL[-1] + 12: return ('waiver', 'wv')
    return (f'take at {c[-1]}', 'tk')


def load():
    b = pd.read_csv(os.path.join(KIT, 'board_v8_fixed.csv'))
    d = pd.read_csv(os.path.join(HERE, 'depth_map.csv'))
    c = pd.read_csv(os.path.join(KIT, 'player_context.csv'))
    g = os.path.join(HERE, 'analyst_calls_joined.csv')
    calls = pd.read_csv(g) if os.path.exists(g) else pd.DataFrame(columns=['player'])
    m = b.merge(d[['espn_id', 'depth', 'ahead', 'job', 'job_gap', 'job_ceil', 'dart_shape']], on='espn_id', how='left') \
         .merge(c[['ESPN_ID', 'grade', 'buy', 'calls_up', 'calls_down', 'who']],
                left_on='espn_id', right_on='ESPN_ID', how='left')
    if 'quote' in calls.columns:
        m = m.merge(calls[['player', 'quote']], on='player', how='left')
    else:
        m['quote'] = None
    return m


def page(title, sub, keybox, head, rows, out):
    doc = ('<!doctype html><html><head><meta charset="utf-8"><title>' + title + '</title><style>'
           + CSS + '</style></head><body><h1>' + title + '</h1><div class="sub">' + sub + '</div>'
           + ('<div class="k">' + keybox + '</div>' if keybox else '')
           + '<table><tr>' + head + '</tr>' + rows + '</table></body></html>')
    hp = os.path.join(SRC, '_sheet_tmp.html')
    open(hp, 'w', encoding='utf-8').write(doc)
    exe = shutil.which('wkhtmltopdf')
    if not exe:
        print(f"  wkhtmltopdf not on PATH -- wrote {hp}; print it to PDF by hand.")
        return False
    r = subprocess.run([exe, '--enable-local-file-access', '--quiet', '-s', 'Letter',
                        '-T', '0', '-B', '0', '-L', '0', '-R', '0', hp, out],
                       capture_output=True, text=True)
    os.remove(hp)
    if r.returncode or not os.path.exists(out) or os.path.getsize(out) < 4000:
        print(f"  !! {os.path.basename(out)} FAILED to build; the old one was not replaced.")
        return False
    print(f"  wrote {out}  ({os.path.getsize(out):,} bytes)")
    return True


def tag(r):
    if isinstance(r.grade, str) and r.grade == 'AVOID': return '<span class="av">AVOID</span> '
    if r.buy == 1: return '<span class="buy">BUY</span> '
    return ''


def main():
    m = load()
    RATE = {'RB': .191, 'WR': .107, 'QB': .250, 'TE': .143}
    KEEPV = {p: float(m[m.pos == p].sort_values('vbd', ascending=False).vbd.values[9])
             for p in ('RB', 'WR', 'QB', 'TE')}
    ok = 0

    # ---- 1. audition window
    w = m[(m.eff_pick >= 52) & (m.eff_pick <= 100) & (m.pos.isin(['RB', 'WR', 'TE']))].sort_values('eff_pick')
    rows = ''
    for _, r in w.iterrows():
        mv, cls = when(r.eff_pick)
        role = ('<span class="st">STARTER</span>' if r.depth == 1 else
                ('<span class="bk">behind ' + html.escape(str(r.ahead)) + '</span>'
                 if isinstance(r.ahead, str) and r.ahead else ''))
        q = html.escape(str(r.quote))[:100] if isinstance(r.quote, str) else ''
        who = html.escape(str(r.who))[:34] if isinstance(r.who, str) and r.who else ''
        note = ('&ldquo;' + q + '&rdquo; <span class="bk">' + who + '</span>') if q else ''
        rows += ('<tr><td class="p">' + tag(r) + html.escape(r.player) + '</td>'
                 f'<td class="n">{r.pos} {r.team_c}</td><td class="n">{int(r.bye)}</td>'
                 f'<td class="n">{r.proj_leaguepts:.0f}</td><td class="n">{r.vbd:+.0f}</td>'
                 f'<td class="{cls}">{mv}</td>'
                 f'<td class="n"><b>{RATE[r.pos]*KEEPV[r.pos]:+.1f}</b></td>'
                 '<td>' + role + '</td><td class="q">' + note + '</td></tr>')
    ok += page('THE KEEPER-AUDITION WINDOW &mdash; picks 56, 65, 80, 89',
        'Every RB/WR/TE the board expects in this range. <b>2027</b> is what the pick is worth as next '
        'year&rsquo;s keeper: how often that position gets kept, times what a keeper there is worth. '
        '<b>STARTER</b> = he is RB1/WR1 on his own depth chart &mdash; the FLEX floor.',
        '<b>Measured on four drafts, 2021&ndash;24 (n=474):</b> rounds <b>5&ndash;6 12.2%</b> become next '
        'year&rsquo;s keeper, rounds <b>7&ndash;8 17.7%</b>, rounds 9&ndash;12 only 8.3%, rounds 13&ndash;15 '
        '1.5%. Rounds 1&ndash;4 are 0% &mdash; ineligible. Expected 2027 value here: <b>RB +15.2 &middot; '
        'WR +4.2 &middot; QB +0.6 &middot; TE 0.0.</b>',
        '<th>player</th><th>pos</th><th class="n">bye</th><th class="n">proj</th><th class="n">VBD</th>'
        '<th>your move</th><th class="n">2027</th><th>his job</th><th>analyst note</th>',
        rows, os.path.join(SRC, 'AUDITION_WINDOW.pdf'))

    # ---- 2. late RB sheet
    # proj 0 rows are empty bodies ESPN carries but does not forecast -- they filled a page
    # with names that can never be a dart.
    l = m[(m.eff_pick >= 90) & (m.eff_pick <= 175) & (m.pos == 'RB') & (m.depth >= 2)
          & (m.proj_leaguepts > 20)].sort_values('eff_pick')
    rows = ''
    for _, r in l.iterrows():
        mv, cls = when(r.eff_pick)
        q = html.escape(str(r.quote))[:110] if isinstance(r.quote, str) else ''
        who = html.escape(str(r.who))[:34] if isinstance(r.who, str) and r.who else ''
        note = ('&ldquo;' + q + '&rdquo; <span class="bk">' + who + '</span>') if q else ''
        job = str(r.job) if isinstance(r.job, str) else ''
        jcls = {'UNSETTLED': 'jg', 'contested': 'jt', 'LEAD BACK': 'jc'}.get(job, '')
        jtxt = (f'<span class="{jcls}">{job}</span>'
                f'<span class="bk"> gap {int(r.job_gap)} &middot; job worth {int(r.job_ceil)}</span>') if job else ''
        rows += ('<tr><td class="p">' + tag(r) + html.escape(r.player) + '</td>'
                 f'<td class="n">{r.team_c}</td>'
                 '<td class="bk">' + html.escape(str(r.ahead) if isinstance(r.ahead, str) else '') + '</td>'
                 '<td>' + jtxt + '</td>'
                 f'<td class="n">{int(r.bye)}</td><td class="n">{r.proj_leaguepts:.0f}</td>'
                 f'<td class="{cls}">{mv}</td>'
                 '<td class="q">' + note + '</td></tr>')
    ok += page('LATE RB SHEET &mdash; picks 104 / 113 / 128 / 137',
        '<b>Behind</b> is the man he would have to replace. <b>The job</b> is how far apart ESPN projects the top two backs on that team, computed on the SOURCE pull so keepers still count. <span class="jg">UNSETTLED</span> under 60 &mdash; ESPN does not know who wins it, which is exactly the backfield worth a dart. <span class="jt">contested</span> 60&ndash;150. <span class="jc">LEAD BACK</span> over 150 &mdash; the starter owns it, so this is a pure handcuff that only pays on an injury. <b>Job worth</b> is what ESPN projects for the man holding it, i.e. roughly what the winner inherits. The team RB pie barely varies (317&ndash;355 across the league), so the gap, not the pie, is the whole signal.',
        '<b>From pick 104 only, and only on a near-tie.</b> 80% of picks in this range finish below '
        'replacement and none in three years became a league-winner. Lottery tickets on a job, not a plan '
        'for one &mdash; take 3 or 4. A hit is also a <b>+80 to +95 keeper</b> for 2027.',
        '<th>player</th><th class="n">tm</th><th>behind</th><th>the job</th><th class="n">bye</th>'
        '<th class="n">proj</th><th>your move</th><th>analyst note</th>',
        rows, os.path.join(SRC, 'LATE_RB_SHEET.pdf'))

    # ---- 3. analyst calls
    a = m[(m.eff_pick >= 90) & (m.eff_pick <= 175) &
          ((m.calls_up.fillna(0) > 0) | (m.calls_down.fillna(0) > 0) | (m.buy.fillna(0) == 1))].sort_values('eff_pick')
    rows = ''
    for _, r in a.iterrows():
        mv, cls = when(r.eff_pick)
        up, dn = int(r.calls_up or 0), int(r.calls_down or 0)
        dirn = (f'<span style="color:#12734f;font-weight:700">{up}&uarr;</span>' if up else '') + \
               (f' <span style="color:#b3261e;font-weight:700">{dn}&darr;</span>' if dn else '')
        q = html.escape(str(r.quote))[:150] if isinstance(r.quote, str) else ''
        who = html.escape(str(r.who)) if isinstance(r.who, str) and r.who else '<i>unattributed</i>'
        rows += ('<tr><td class="p">' + tag(r) + html.escape(r.player) + '</td>'
                 f'<td class="n">{r.pos} {r.team_c}</td><td class="n">{int(r.bye)}</td>'
                 f'<td class="{cls}">{mv}</td><td class="n">{dirn}</td>'
                 '<td class="q">' + (('&ldquo;' + q + '&rdquo;<br><span class="bk">' + who + '</span>') if q else '') + '</td></tr>')
    ok += page('ANALYST CALLS &mdash; only players you can actually reach',
        'De-duplicated and joined to the board. <b>&uarr;</b> target calls, <b>&darr;</b> downgrades. '
        '<b>BUY</b> = our own two panels are also ahead of ADP. Quotes verbatim, typos and all.',
        '<b>Read the provenance first.</b> Of 222 raw rows, <b>42 were the same call counted twice</b>, '
        '<b>189 carry no date at all</b>, 8 of the 33 dated ones are from <b>2025</b>, 36 are unattributed, '
        'and 11 names were mis-transcribed from audio. <b>A reading list &mdash; not evidence.</b>',
        '<th>player</th><th>pos</th><th class="n">bye</th><th>your move</th><th class="n">calls</th>'
        '<th>what they said</th>',
        rows, os.path.join(SRC, 'ANALYST_CALLS.pdf'))

    print(f"\n  {ok} of 3 sheets rebuilt.")
    if ok < 3: sys.exit(1)
    print("  Now  py sync_desk_copies.py  to put dated copies at the root.")


if __name__ == '__main__':
    main()
