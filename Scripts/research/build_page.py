import json, html
d = json.load(open('sheet.json'))
E = lambda s: html.escape(str(s))
W = list(range(1, 15))
POS = ['QB','RB','WR','TE','D/ST','K']
bar = d['bar']
cands = {c['name']: c for c in d['cands']}
hdr = ''.join(f'<th scope="col">{w}</th>' for w in W)

# --- 1. the bar grid ---------------------------------------------------------------------------
brows = []
for p in POS:
    cells = []
    for w in W:
        v = bar[p][str(w)]
        cls = 'hole' if v == 0 else ''
        txt = 'empty' if v == 0 else f'{v:.1f}'
        cells.append(f'<td class="c {cls}">{txt}</td>')
    brows.append(f'<tr><th scope="row">{E(p)}</th>{"".join(cells)}</tr>')
bargrid = (f'<div class="scroll"><table class="g"><caption class="sr">The rate a new player must beat, '
           f'by position and week.</caption><thead><tr><th class="corner" scope="col">position</th>{hdr}'
           f'</tr></thead><tbody>{"".join(brows)}</tbody></table></div>')

# --- 2. candidate arithmetic -------------------------------------------------------------------
GROUPS = [
 ('Fills a week that is currently empty',
  'The bar is zero those weeks, so his whole rate counts. Nothing else on the wire is worth this much.',
  ['Brenton Strange','Pat Freiermuth','Dalton Schultz','Gunnar Helm',
   'Chris Boswell','Trey Smack','Will Reichard']),
 ('Beats nobody today &mdash; the injury and bye bench',
  'Every cell is zero because your own man is above the bar every week. That is the answer, not a gap in the sheet.',
  ['Brian Robinson Jr.','Samaje Perine','Tre Tucker','Jerry Jeudy','Tank Dell','Daniel Jones']),
 ('On waivers, so adding one costs a claim',
  'Everything else on this page is a free agent: the green plus, no claim, no priority spent.',
  ['Baker Mayfield','Tyjae Spears']),
]
WHEN = {'Brenton Strange':'week 5','Pat Freiermuth':'week 5','Dalton Schultz':'week 5','Gunnar Helm':'week 5',
        'Chris Boswell':'week 7','Trey Smack':'week 7','Will Reichard':'week 7',
        'Brian Robinson Jr.':'on the news','Samaje Perine':'on the news','Tre Tucker':'on the news',
        'Jerry Jeudy':'on the news','Tank Dell':'now, to IR','Daniel Jones':'only if Hurts goes',
        'Baker Mayfield':'never','Tyjae Spears':'never'}
NOTE = {'Brenton Strange':'LaPorta&rsquo;s week 6 is your only empty tight-end week',
        'Pat Freiermuth':'same job, bye in week 9 instead of 7',
        'Dalton Schultz':'all 17 games last year',
        'Gunnar Helm':'5.8% rostered &mdash; nobody is looking',
        'Chris Boswell':'Pineiro&rsquo;s bye is week 8',
        'Trey Smack':'a tenth better, but his bye is week 11, your worst week',
        'Will Reichard':'his bye is week 6, which stacks on LaPorta&rsquo;s',
        'Brian Robinson Jr.':'a lead-back job worth 315, unowned &mdash; best RB body on the wire',
        'Samaje Perine':'contested job worth 239',
        'Tre Tucker':'took the room off Davante Adams last year',
        'Jerry Jeudy':'Cleveland &mdash; the same offence as your defence',
        'Tank Dell':'carries the IR tag, so he takes an IR slot and not a bench spot',
        'Daniel Jones':'0.05 a game behind Shough, who already holds the spot',
        'Baker Mayfield':'clears Saturday. You start Hurts.',
        'Tyjae Spears':'clears Friday. You just dropped him and it cost nothing.'}

def crow(n):
    c = cands.get(n)
    if not c: return ''
    cells = []
    for w in W:
        v = c['calc'][str(w)]
        if v == 'bye': cells.append('<td class="c bye">bye</td>')
        elif v == 0:   cells.append('<td class="c zero">0</td>')
        else:          cells.append(f'<td class="c ok">+{v:.1f}</td>')
    g25 = f' <span class="warnpill">{c["g25"]} games in 2025</span>' if (c.get('g25') and c['g25'] < 13) else ''
    ow = f'{c["owned"]:.1f}%' if c.get('owned') is not None else '&mdash;'
    tcls = 'tot pos' if c['calc_total'] > 0.05 else 'tot'
    return (f'<tr><th scope="row"><span class="pl">{E(n)}</span>'
            f'<span class="meta">{E(c["pos"])} &middot; {E(c["tm"])} &middot; bye {int(float(c["bye"]))}'
            f' &middot; {ow} rostered</span></th>'
            f'<td class="rate">{c["market_wk"]:.1f}</td>{"".join(cells)}'
            f'<td class="{tcls}">{"+" if c["calc_total"]>0.05 else ""}{c["calc_total"]:.1f}</td>'
            f'<td class="when">{E(WHEN.get(n,""))}</td></tr>'
            f'<tr class="noterow"><td colspan="18" class="note">{NOTE.get(n,"")}{g25}</td></tr>')

groups = ''
for title, sub, names in GROUPS:
    groups += (f'<h3>{title}</h3><p class="sub2">{sub}</p><div class="scroll">'
               f'<table class="g cand"><thead><tr><th class="corner" scope="col">player</th>'
               f'<th scope="col" class="rate">pts<br>a wk</th>{hdr}'
               f'<th scope="col" class="tot">season</th><th scope="col" class="when">when</th></tr></thead>'
               f'<tbody>{"".join(crow(n) for n in names)}</tbody></table></div>')

# --- 3. potential ------------------------------------------------------------------------------
POT = ['Omar Cooper Jr.','Ricky Pearsall','Pat Bryant','Jalen McMillan']
NFL = {'Omar Cooper Jr.':'NFL round 1, pick 30 &middot; rookie',
       'Ricky Pearsall':'NFL round 1, pick 31 &middot; year 3',
       'Pat Bryant':'NFL round 3, pick 74 &middot; year 2',
       'Jalen McMillan':'NFL round 3, pick 92 &middot; year 3'}
prows = ''
for n in POT:
    c = cands[n]
    g25 = f'<span class="warnpill">{c["g25"]} games in 2025</span>' if (c.get('g25') and c['g25'] < 13) else ''
    prows += (f'<tr><th scope="row"><span class="pl">{E(n)}</span>'
              f'<span class="meta">{NFL[n]} &middot; bye {int(float(c["bye"]))} &middot; {c["owned"]:.1f}% rostered</span></th>'
              f'<td class="num">{c["market_wk"]:.1f}</td><td class="num zero">0.0</td>'
              f'<td class="num tot pos">+{c["pot_gain"]:.2f}</td>'
              f'<td class="num">+{c["pot_p90"]:.1f}</td>'
              f'<td class="num">{c["pot_hit"]*100:.0f}%</td>'
              f'<td class="note">{g25}</td></tr>')

# --- 4. defence marriage -----------------------------------------------------------------------
DW = list(range(2, 18))
dhdr = ''.join(f'<th scope="col">{w}</th>' for w in DW)
def strip(team, other, label):
    cells = []
    for w in DW:
        a = d['dst'][team].get(str(w)); b = d['dst'][other].get(str(w))
        if a is None:
            cells.append('<td class="c bye">bye</td>'); continue
        start = (b is None) or (a >= b)
        opp = d['dst']['opp'][team].get(str(w)) or ''
        cells.append(f'<td class="c {"ok" if start else "zero"}">'
                     f'<span class="nm">{E(opp)}</span><span class="vl">{a:.1f}</span></td>')
    return f'<tr><th scope="row">{E(label)}</th>{"".join(cells)}</tr>'
best = []
for w in DW:
    a = d['dst']['CLE'].get(str(w)); b = d['dst']['CHI'].get(str(w))
    v = max([x for x in (a, b) if x is not None] or [0])
    best.append(f'<td class="c tot">{v:.1f}</td>')
ptot = ''.join(
  f'<tr><th scope="row">{E(t)}</th><td class="num">+{d["dst_gain"][t]["w2_14"]:.1f}</td>'
  f'<td class="num">+{d["dst_gain"][t]["w9_14"]:.1f}</td>'
  f'<td class="num">+{d["dst_gain"][t]["w15_17"]:.1f}</td></tr>'
  for t in sorted(d['partners'], key=lambda x: -d['dst_gain'][x]['w2_14']))

# --- 5. roster ---------------------------------------------------------------------------------
starters = {'Jalen Hurts','Ashton Jeanty','Quinshon Judkins','Puka Nacua','George Pickens',
            'Sam LaPorta','Davante Adams','Browns D/ST','Eddy Pineiro'}
rrows = ''
for p in sorted(d['roster'], key=lambda x: (POS.index(x['pos']), -x['wk'])):
    g25 = f'<span class="warnpill">{p["g25"]} games in 2025</span>' if (p.get('g25') and p['g25'] < 13) else ''
    rrows += (f'<tr><th scope="row"><span class="pl">{E(p["name"])}</span>'
              f'<span class="meta">{E(p["pos"])} &middot; {E(p["tm"])}</span></th>'
              f'<td class="num">{p["wk"]:.1f}</td><td class="num">{p["bye"]}</td>'
              f'<td class="when">{"starts" if p["name"] in starters else "bench"}</td>'
              f'<td class="note">{g25}</td></tr>')

open('/home/claude/out/parts.json','w').write(json.dumps(dict(
    bargrid=bargrid, groups=groups, prows=prows, dhdr=dhdr,
    cle=strip('CLE','CHI','Cleveland'), chi=strip('CHI','CLE','Chicago'),
    best=''.join(best), ptot=ptot, rrows=rrows, base=d['base'])))
print("ok")
