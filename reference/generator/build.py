#!/usr/bin/env python3
"""Builds the SpearPoint B2B SEO Dashboard (index.html) from the data/ JSON files."""
import json, html, os
from collections import Counter

D = 'data'
L = lambda f: json.load(open(os.path.join(D, f)))
trend = L('gsc_trend.json'); kw = L('keywords.json'); serps = L('serps.json')
comps = L('competitors.json'); gaps = L('gaps.json')
Q = L('gsc90_queries.json'); P = L('gsc90_pages.json'); ana = L('gsc90_analysis.json')
css = open('base.css.txt').read()
logo_h = open('logo1.txt').read().strip(); logo_f = open('logo2.txt').read().strip()
e = html.escape

GEN_DATE = 'November 16, 2026'
W = trend['windows']
def pct(a, b): return (a - b) / b * 100

# ---------------- extra CSS ----------------
css += """
/* ---- SEO dashboard additions ---- */
.report-nav { background:#fff; border-bottom:1px solid var(--line); }
.report-nav .wrap { display:flex; gap:6px; flex-wrap:wrap; padding-top:10px; padding-bottom:10px; }
.report-nav a, .report-nav span { font-size:12.5px; font-weight:700; padding:7px 14px; border-radius:100px; text-decoration:none; color:var(--blue); border:1.5px solid var(--line); }
.report-nav a:hover { border-color:var(--blue); background:var(--beige); }
.report-nav .on { background:var(--blue); color:#fff; border-color:var(--blue); }
.report-nav .soon { color:var(--muted1); border-style:dashed; }
.kpi-delta { font-size:12px; font-weight:700; margin-top:6px; }
.up { color:var(--green-dark); } .down { color:var(--red-dark); } .flat { color:var(--slate); }
.takeaways { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:16px; }
@media (max-width:860px) { .takeaways { grid-template-columns:1fr; } }
.take { background:var(--blue); color:#fff; border-radius:10px; padding:20px 22px; }
.take .t-k { font-size:11px; text-transform:uppercase; letter-spacing:.1em; color:var(--green); font-weight:800; margin-bottom:6px; }
.take.warn .t-k { color:#F7A797; }
.take h4 { font-size:16px; line-height:1.3; margin-bottom:8px; }
.take p { font-size:13px; color:#C7D2DA; margin:0; }
.pk-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
@media (max-width:980px) { .pk-grid { grid-template-columns:1fr 1fr; } }
@media (max-width:620px) { .pk-grid { grid-template-columns:1fr; } }
.pk-card { background:#fff; border:1px solid var(--line); border-radius:10px; padding:18px 18px 16px; display:flex; flex-direction:column; }
.pk-top { display:flex; justify-content:space-between; gap:8px; align-items:flex-start; }
.pk-kw { font-size:16px; font-weight:800; color:var(--blue); }
.pk-loc { font-size:11px; color:var(--slate); margin-top:2px; }
.pk-pos { text-align:right; }
.pk-pos .n { font-size:26px; font-weight:800; line-height:1; }
.pk-pos .l { font-size:9.5px; text-transform:uppercase; letter-spacing:.05em; color:var(--slate); font-weight:700; }
.pk-stats { display:flex; gap:14px; margin-top:12px; padding-top:10px; border-top:1px solid var(--line); font-size:12px; color:var(--slate); flex-wrap:wrap; }
.pk-stats b { color:var(--ink); }
.pk-serp { margin-top:10px; font-size:12px; color:var(--slate); }
.pk-serp ol { margin:4px 0 0; padding-left:18px; color:var(--ink); }
.pk-insight { margin-top:10px; font-size:12.5px; color:var(--ink); background:var(--beige); border-radius:8px; padding:10px 12px; }
.pk-insight b { color:var(--blue); }
.pk-alt { margin-top:auto; padding-top:10px; font-size:12px; color:var(--slate); }
.pk-alt span { display:inline-block; background:rgba(77,184,89,.14); color:var(--green-dark); font-weight:700; border-radius:100px; padding:2px 9px; margin:3px 4px 0 0; }
.pos-none { color:var(--red-dark); } .pos-mid { color:#C98A1A; } .pos-good { color:var(--green-dark); }
.cmp-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:14px; }
@media (max-width:980px) { .cmp-grid { grid-template-columns:repeat(3,1fr); } }
@media (max-width:620px) { .cmp-grid { grid-template-columns:1fr 1fr; } }
.metric-best { color:var(--green-dark) !important; }
.sc-grid { display:grid; gap:16px; }
.sc-grid.five { grid-template-columns:repeat(3,1fr); }
.sc-grid.four { grid-template-columns:repeat(2,1fr); }
@media (max-width:980px) { .sc-grid.five, .sc-grid.four { grid-template-columns:1fr 1fr; } }
@media (max-width:640px) { .sc-grid.five, .sc-grid.four { grid-template-columns:1fr; } }
.sc-card { background:#fff; border:1px solid var(--line); border-radius:10px; padding:18px 18px 16px; display:flex; flex-direction:column; gap:12px; }
.sc-card.is-client { border:2px solid var(--green); }
.sc-head { display:flex; justify-content:space-between; align-items:flex-start; gap:10px; }
.sc-score .n { font-size:34px; font-weight:800; color:var(--blue); line-height:1; }
.sc-score .d { font-size:13px; color:var(--slate); font-weight:700; }
.sc-bar { height:8px; background:#ECEBD9; border-radius:6px; overflow:hidden; }
.sc-bar div { height:100%; background:var(--blue); border-radius:6px; }
.sc-card.is-client .sc-bar div { background:var(--green); }
.sc-parts { display:flex; flex-direction:column; gap:6px; }
.sc-part { display:grid; grid-template-columns:150px 1fr 30px; gap:8px; align-items:center; font-size:12px; color:var(--slate); }
.sc-part i { font-style:normal; color:var(--muted1); font-size:10.5px; }
.sc-part b { text-align:right; color:var(--ink); font-variant-numeric:tabular-nums; }
.sc-track { height:6px; background:#ECEBD9; border-radius:4px; overflow:hidden; }
.sc-track div { height:100%; background:var(--muted3); border-radius:4px; }
.sc-sub { font-size:10.5px; text-transform:uppercase; letter-spacing:.06em; font-weight:800; color:var(--slate); margin-bottom:6px; }
.sc-kws { display:flex; flex-wrap:wrap; gap:5px; }
.sc-kws .sc-sub { width:100%; margin-bottom:0; }
.sc-kw { font-size:11px; background:#F3F2E6; color:var(--slate); border-radius:100px; padding:3px 9px; }
.sc-kw b { color:var(--muted3); }
.sc-kw.hit { background:rgba(77,184,89,.15); color:var(--green-dark); }
.sc-kw.hit b { color:var(--green-dark); }
.sc-mets { border-top:1px solid var(--line); padding-top:4px; }
.sc-note { font-size:12.5px; color:var(--ink); background:var(--beige); border-radius:8px; padding:10px 12px; }
.method-box { margin-top:14px; font-size:12.5px; color:var(--slate); background:#fff; border:1px dashed var(--line); border-radius:8px; padding:12px 16px; line-height:1.6; }
.method-box b { color:var(--ink); }
.kpi-grid.five { grid-template-columns:repeat(5,1fr); }
@media (max-width:1100px) { .kpi-grid.five { grid-template-columns:repeat(3,1fr); } }
@media (max-width:640px) { .kpi-grid.five { grid-template-columns:1fr 1fr; } }
.dt-chart svg { width:100%; height:auto; display:block; }
tr.row-client td { background:rgba(77,184,89,.10); }
.muted { color:var(--muted1); font-size:11px; }
.src-t { font-size:10.5px; color:var(--muted3); }
.pos-none-t { font-size:11.5px; color:var(--red-dark); font-weight:700; }
.pk-partial { margin-top:10px; font-size:12px; color:var(--slate); }
.pk-partial table { width:100%; border-collapse:collapse; margin-top:4px; }
.pk-partial td { padding:4px 0; border-top:1px solid #EEECDD; font-size:12px; color:var(--ink); vertical-align:top; }
.pk-partial td.r { text-align:right; font-weight:800; white-space:nowrap; padding-left:8px; }
.pk-partial td small { color:var(--muted3); font-size:10.5px; }
.pk-partial .none { color:var(--red-dark); font-weight:700; }
.pg-btns button.pg-on { background:var(--blue); color:#fff; border-color:var(--blue); }

.bar-list { display:flex; flex-direction:column; gap:10px; }
.bar-row { display:grid; grid-template-columns:150px 1fr 130px; gap:12px; align-items:center; font-size:13px; }
.bar-track { background:#ECEBD9; border-radius:6px; height:14px; overflow:hidden; }
.bar-fill { height:100%; border-radius:6px; }
.bar-val { text-align:right; font-variant-numeric:tabular-nums; color:var(--slate); font-size:12px; }
.mini h4 { font-size:13px; text-transform:uppercase; letter-spacing:.06em; color:var(--slate); margin-bottom:10px; }
.chart-legend { display:flex; gap:18px; font-size:12.5px; color:var(--slate); margin-top:10px; flex-wrap:wrap; }
.chart-legend i { display:inline-block; width:12px; height:12px; border-radius:3px; margin-right:6px; vertical-align:-1px; }
.cell-num { text-align:right; font-variant-numeric:tabular-nums; }
.pos-pill { font-weight:800; }
td.url { max-width:420px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.note-box { background:#fff; border-left:4px solid var(--red); border-radius:6px; padding:12px 16px; font-size:13px; color:var(--slate); margin-top:16px; }
.note-box b { color:var(--ink); }
.cell-topic-tag { white-space:nowrap; }
"""

# ---------------- KPI ----------------
def delta(cur, prev, better_low=False, unit='%'):
    d = pct(cur, prev)
    good = (d < 0) if better_low else (d > 0)
    cls = 'up' if good else 'down'
    arrow = '▲' if d > 0 else '▼'
    return f'<div class="kpi-delta {cls}">{arrow} {abs(d):.0f}% vs. prior 90 days</div>'

l90, p90, y90, l28, p28 = W['l90'], W['p90'], W['y90'], W['l28'], W['p28']
pos_gain = p90[3] - l90[3]; pos_yoy = y90[3] - l90[3]

sc = L('scores.json'); s2 = L('serps2.json')
PKW = ['b2b seo agency','denver seo company','aeo agency','ai search optimization agency','seo cro agency','conversion based seo']
PKL = {'b2b seo agency':'B2B SEO Agency','denver seo company':'Denver SEO Company','aeo agency':'AEO Agency','ai search optimization agency':'AI Search Optimization Agency','seo cro agency':'SEO + CRO Agency','conversion based seo':'Conversion Based SEO'}
kpis = f"""
<div class="kpi-grid five">
  <div class="kpi-card"><div class="kpi-label">Organic Clicks · 90 days</div><div class="kpi-value tab">{l90[1]:,}</div>
    {delta(l90[1], p90[1])}<div class="kpi-sub">Last 28 days: <b>{l28[1]}</b> clicks (<span class="up">▲ {pct(l28[1],p28[1]):.0f}%</span> vs. prior 28)</div></div>
  <div class="kpi-card"><div class="kpi-label">Impressions · 90 days</div><div class="kpi-value tab">{l90[2]/1000:.0f}K</div>
    {delta(l90[2], p90[2])}<div class="kpi-sub">Times SpearPoint appeared in Google results</div></div>
  <div class="kpi-card"><div class="kpi-label">Avg. Google Position</div><div class="kpi-value tab">{l90[3]}</div>
    <div class="kpi-delta up">▲ {pos_gain:.0f} spots vs. prior 90 days</div><div class="kpi-sub">▲ <b>{pos_yoy:.0f} spots</b> vs. same period last year ({y90[3]})</div></div>
  <div class="kpi-card"><div class="kpi-label">Domain Trust</div><div class="kpi-value tab">50<span style="font-size:16px;color:var(--slate);">/100</span></div>
    <div class="kpi-delta up">▲ 9 in 12 months (41 → 50)</div><div class="kpi-sub">Targeted competitors: <b>60&ndash;79</b></div></div>
  <div class="kpi-card"><div class="kpi-label">Priority Keywords on Page 1</div><div class="kpi-value tab">1<span style="font-size:16px;color:var(--slate);">/6</span></div>
    <div class="kpi-delta flat">“b2b seo agency” is next at #11</div><div class="kpi-sub">On page 1: “conversion based seo” at #4</div></div>
</div>
<div class="takeaways">
  <div class="take"><div class="t-k">What's working</div><h4>SpearPoint is showing up higher in Google than a year ago.</h4>
    <p>Average position improved from {y90[3]} to {l90[3]} year over year. The last 28 days brought {l28[1]} clicks, up {pct(l28[1],p28[1]):.0f}% on the 28 days before, and “b2b seo agency” sits on the edge of page 1 (#9&ndash;11 all week).</p></div>
  <div class="take warn"><div class="t-k">What's missing</div><h4>The AI Search and Denver keywords aren't ranking yet.</h4>
    <p>“aeo agency” (590/mo), “ai search optimization agency” (480/mo) are not in Google's top 100, and “denver seo company” is stuck on page 2 (#14). In the last 90 days, about a third of identifiable clicks (45 of 124) came from people already searching “SpearPoint” by name.</p></div>
  <div class="take"><div class="t-k">Fastest path to leads</div><h4>Retarget pages that already exist.</h4>
    <p>Push /b2b-seo from #11 onto page 1, point the AEO page at “aeo agency” and “ai search optimization agency,” and give Denver its own page. All three pages already exist.</p></div>
</div>"""

# ---------------- priority keyword cards ----------------
TRACK = {'b2b seo agency':(11,'SE Ranking daily tracker · US','#9&ndash;11 since Nov 13'),
         'seo cro agency':(56,'SE Ranking daily tracker · US','#56&ndash;69 since Nov 13'),
         'conversion based seo':(4,'SE Ranking daily tracker · US','#4 every day since Nov 13'),
         'denver seo company':(14,'SE Ranking keyword database · US','Denver: not in top 70')}
PK = [
  dict(kw='b2b seo agency', vol=50, kd=13, gsc='28,297 impressions · avg. #62.9 · 2 clicks',
       insight='On the edge of page 1, at #9&ndash;11 every day this week. The <b>/b2b-seo</b> H1 reads “Conversion Based B2B SEO.” Putting “B2B SEO Agency” in the title and H1 is the clearest lever.',
       alts=[('b2b seo services',480),('b2b seo company',480),('b2b seo',260)]),
  dict(kw='denver seo company', vol=10, kd=24, gsc='2,214 impressions · avg. #18.2 · 0 clicks (90 days)',
       insight='Page 2 nationally: #14 on <b>/seo</b>, which was retitled “Denver SEO Company…” this week. A Denver-located check on Nov 17 didn\'t find SpearPoint in the top 70; Thrive Agency is #1 and list sites (Built In Colorado, Reddit, Clutch) fill page 1. Fixing the 3 H1 tags on /seo and adding Denver client proof is the fastest lift.',
       alts=[('denver seo',2900),('seo agency denver',590),('seo company colorado',110)]),
  dict(kw='aeo agency', vol=590, kd=16, gsc='No impressions for this query in 16 months',
       insight='The highest-volume priority keyword and one of the easiest (difficulty 16). Demand has more than doubled in a year. The AEO page\'s H1 has a typo (“AI SEARCH + AEO SERVICES SERVICES”) and doesn\'t use the word “agency.”',
       alts=[('answer engine optimization agency',260),('aeo agencies',90)]),
  dict(kw='ai search optimization agency', vol=480, kd=36, gsc='No impressions for this query in 16 months',
       insight='Demand jumped from about 10/mo a year ago to 480/mo. Half the top 10 are “best AI SEO agencies” lists (Percepture, Optimist, Thrive). Getting listed on those pages is as important as ranking SpearPoint\'s own page.',
       alts=[('ai seo agency',810),('generative engine optimization agency',480)]),
  dict(kw='seo cro agency', vol=None, kd=None, gsc='CRO topics: 23K impressions · 0 clicks',
       insight='Too niche for measurable search volume. <b>/conversion-based-seo</b> ranks around #56. Keep it as positioning, and target the CRO terms people actually search.',
       alts=[('conversion rate optimization services',150),('conversion rate optimization agency',70)]),
  dict(kw='conversion based seo', vol=0, kd=25, gsc='No impressions for this query in 16 months',
       insight='SpearPoint owns this phrase, at #4 every day this week. It has almost no search volume, so its value is brand proof: buyers who hear the term and Google it find SpearPoint.',
       alts=[('seo conversion rate optimization',170),('cro seo',110)]),
]
PARTIAL = {
 'b2b seo agency': [('b2b seo company',35,480,'/b2b-seo'),('b2b seo companies',39,480,'/b2b-seo'),('seo agency for b2b',37,90,'/b2b-seo'),('b2b seo firm',40,90,'/b2b-seo'),('b2b saas seo agency',23,170,'GSC avg')],
 'denver seo company': [('seo denver',14,140,'/seo · tracker'),('seo agency in denver',13,10,'/seo · Denver tracker'),('affordable denver seo company',15,90,'/seo'),('seo agency denver co',15,20,'/seo'),('denver colorado seo agency',16,20,'/seo'),('seo agency denver',21,590,'/seo · tracker')],
 'aeo agency': [('aeo content strategy',35,10,'AEO guide (blog)'),('aeo strategy',76,320,'AEO guide (blog)'),('what is aeo answer engine optimization',77,110,'AEO guide (blog)')],
 'ai search optimization agency': [('llmo vs seo',1,20,'LLMO vs SEO (blog)'),('llmo seo audit',6,0,'LLMO vs SEO (blog)'),('appear in chatgpt',35,0,'How to appear on ChatGPT (blog)'),('llmo seo services',45,0,'LLMO vs SEO (blog)'),('llmo',59,480,'LLMO vs SEO (blog)')],
 'seo cro agency': [('denver conversion rate optimization agency',17,10,'/conversion-rate-optimization'),('cro seo consultant',35,0,'/conversion-based-seo')],
 'conversion based seo': [('conversion focused seo agency',21,0,'/conversion-based-seo'),('cro seo consultant',35,0,'/conversion-based-seo')],
}
PARTIAL_NOTE = {
 'b2b seo agency': 'Coverage is broad but stuck on pages 3&ndash;4: about 30 “B2B SEO + agency/company/firm” variants rank #33&ndash;45, all on /b2b-seo.',
 'denver seo company': 'Strong partial coverage: about 90 Denver/Colorado SEO variants rank, many at #13&ndash;17 on /seo. The sister phrase “denver seo agency” only shows up at #99, through a blog post.',
 'aeo agency': 'No agency-intent coverage. Only informational AEO terms rank, all from the AEO blog guide. The /aeo-ai-search-services page ranks for none of them.',
 'ai search optimization agency': 'Ranks for LLMO and GEO <i>informational</i> terms through blog posts (“llmo vs seo” #1), but for no “AI search / AI SEO agency” terms.',
 'seo cro agency': 'Thin coverage: one Denver CRO term at #17 and “cro seo consultant” at #35. Service-intent CRO terms aren\'t ranking.',
 'conversion based seo': 'Besides the exact phrase at #4, /conversion-based-seo also ranks for “conversion focused seo agency” (#21) and “cro seo consultant” (#35).',
}
def poscls(p): return 'pos-none' if p is None else ('pos-good' if p <= 10 else 'pos-mid')
cards = []
for c in PK:
    s = s2[c['kw']]
    if c['kw'] in TRACK: sp, src, rng = TRACK[c['kw']]
    else:
        sp = s['spearpoint'][0][0] if s['spearpoint'] else None; src = f'SE Ranking live check · {s["location"]}'; rng = ''
    top = [o[1] for o in s['top10'] if 'thespearpoint' not in o[1]][:5]
    posn = f'#{sp}' if sp else '&mdash;'
    vol = 'n/a' if c['vol'] is None else f"{c['vol']:,}"
    kd = '&mdash;' if c['kd'] is None else c['kd']
    cards.append(f"""<div class="pk-card">
  <div class="pk-top"><div><div class="pk-kw">{e(PKL[c['kw']])}</div><div class="pk-loc">{src} · {"Nov 17" if c["kw"]=="denver seo company" else "Nov 16"}, 2026</div></div>
  <div class="pk-pos"><div class="n {poscls(sp)}">{posn}</div><div class="l">{'Not in top 100' if sp is None else 'SpearPoint rank'}</div></div></div>
  <div class="pk-stats"><span>Volume <b>{vol}{'' if vol=='n/a' else '/mo'}</b></span><span>Difficulty <b>{kd}</b></span>{f'<span>Range <b>{rng}</b></span>' if rng else ''}</div>
  <div class="pk-stats" style="border-top:none;margin-top:4px;padding-top:0;"><span>GSC: <b style="font-weight:600">{e(c['gsc'])}</b></span></div>
  <div class="pk-serp">Top results today:<ol>{''.join(f'<li>{e(d)}</li>' for d in top)}</ol></div>
  <div class="pk-insight">{c['insight']}</div>
  <div class="pk-partial"><div class="sc-sub">Partial keyword coverage (SpearPoint ranks for)</div>{PARTIAL_NOTE[c['kw']]}<table>{''.join(f'<tr><td>{e(k)}<br><small>{v:,}/mo · {e(u)}</small></td><td class="r {poscls(p)}">#{p}</td></tr>' for k,p,v,u in PARTIAL[c['kw']])}</table></div>
  <div class="pk-alt">Related keywords to target:<br>{''.join(f'<span>{e(a)} · {v:,}</span>' for a,v in c['alts'])}</div>
</div>""")
pk_html = '<div class="pk-grid">' + ''.join(cards) + '</div>'

# ---------------- scored competitor cards ----------------
order = ['SpearPoint Marketing','Breaking B2B','TrioSEO','Flow Agency','Thrive Digital']
colors = {'SpearPoint Marketing':'#4DB859','Breaking B2B':'#8FA6AE','TrioSEO':'#6E8AA6','Flow Agency':'#1D3853','Thrive Digital':'#C7CBB9'}
STRENGTH_PARTS = [('auth','Domain Trust',30),('top10','Top-10 keywords',25),('traffic','Organic traffic',25),('links','Referring domains',20)]
SERP_PARTS = [('kv','Priority keywords',35),('auth','Domain Trust',20),('top10','Top-10 keywords',15),('traffic','Organic traffic',15),('links','Referring domains',15)]
def pos_txt(p): return '&mdash;' if p is None else f'#{p}'
def score_card(rank, name, d, key, partdefs, client=False, note='', show_kw=False):
    parts = ''.join(f'<div class="sc-part"><span>{lab} <i>{w}%</i></span><div class="sc-track"><div style="width:{d["parts"][k]}%"></div></div><b>{d["parts"][k]}</b></div>' for k, lab, w in partdefs)
    pk = ''.join(f'<span class="sc-kw {"hit" if d["pos"][k] else ""}">{e(PKL[k])} <b>{pos_txt(d["pos"][k])}</b></span>' for k in PKW)
    mets = [('Domain Trust', d['dr']), ('Referring domains', format(d['refd'], ',')), ('Ranking keywords (US)', format(d['kw'], ',')),
            ('Keywords in top 10', format(d['t10x'], ',')), ('Est. monthly traffic', format(d['traffic'], ','))]
    mrows = ''.join(f'<div class="score-metric"><span>{a}</span><b>{b}</b></div>' for a, b in mets)
    v = d[key]
    return f"""<div class="sc-card{' is-client' if client else ''}">
  <div class="sc-head"><div><div class="score-rank">#{rank} · {e(d['domain'])}</div><div class="score-card-name">{e(name)}{' <span class="tag-client">Client</span>' if client else ''}</div></div>
  <div class="sc-score"><span class="n">{v:.0f}</span><span class="d">/100</span></div></div>
  <div class="sc-bar"><div style="width:{v}%"></div></div>
  <div class="sc-parts">{parts}</div>
  {f'<div class="sc-kws"><div class="sc-sub">Rank on the 6 priority keywords</div>{pk}</div>' if show_kw else ''}
  <div class="sc-mets">{mrows}</div>
  {f'<div class="sc-note">{note}</div>' if note else ''}
</div>"""
tg = sc['targeted']
rank_t = sorted(order, key=lambda b: -tg[b]['strength'])
cmp_html = '<div class="sc-grid five">' + ''.join(score_card(i+1, b, tg[b], 'strength', STRENGTH_PARTS, b.startswith('SpearPoint')) for i, b in enumerate(rank_t)) + '</div>'
SCORE_METHOD = ('<div class="method-box"><b>How the SEO Strength Score works (0&ndash;100).</b> It uses the same formula for every brand and every month, so the targeted competitors can be tracked the same way across the SEO, AI Search and CRO reports. It measures overall organic strength and does not include the priority keywords. '
  '<b>Domain Trust (30%)</b>: SE Ranking\'s 0&ndash;100 Domain Trust score. '
  '<b>Top-10 keywords (25%)</b>, <b>organic traffic (25%)</b> and <b>referring domains (20%)</b> use a log scale, so 10,000 top-10 keywords, 100,000 visits/mo or 10,000 referring domains = 100.</div>')
SERP_METHOD = ('<div class="method-box"><b>How the SERP Competitiveness Score works (0&ndash;100).</b> Unlike the SEO Strength Score above, this one includes the priority keywords, because it measures who is winning those specific searches. '
  '<b>Priority keywords (35%)</b>: rank on each of the 6 keywords (top 3 = 100 pts, 4&ndash;10 = 75, 11&ndash;20 = 40, 21&ndash;50 = 15, 51&ndash;100 = 5, not ranking = 0), averaged. '
  '<b>Domain Trust (20%)</b>, plus <b>top-10 keywords</b>, <b>organic traffic</b> and <b>referring domains</b> (15% each, same log scales).</div>')

sp_ = sc['targeted']['SpearPoint Marketing']; se = dict(sc['serp']); se['SpearPoint Marketing'] = sp_
SERP_NOTES = {
 'Thrive Agency': 'Ranks #1&ndash;5 for three priority keywords with dedicated service pages, including #1 for “denver seo company” (/denver-seo-company), plus AI SEO and CRO. <b>Not the same company</b> as the targeted competitor Thrive Digital.',
 'Coalition Technologies': 'Ranks #3 for “ai search optimization agency” and #6 for “seo cro agency” with focused pages (/ai-seo-company, /cro-agency), backed by 4,264 referring domains.',
 '1Digital Agency': 'Ranks for two priority keywords (#18 “seo cro agency”, #37 “aeo agency”). Its Denver city page ranks for “denver seo agency” but isn\'t in the top 70 for “denver seo company.”',
 'Optimist': 'The closest model for SpearPoint: a B2B-focused AI Search + SEO agency, far smaller than Thrive or Coalition (316 est. visits/mo). It wins AEO terms with “Best AEO agencies” and “Best AI SEO agencies” list pages (#4&ndash;5).',
 'SpearPoint Marketing': 'SpearPoint ranks for four priority keywords (#4, #11, #14, #56), more than any of the four SERP competitors. The gap is in where it ranks: only one is in the top 10, and Domain Trust (50) is the lowest of the five.',
}
rank_s = sorted(se, key=lambda b: -se[b]['score'])
serp_html = '<div class="sc-grid five">' + ''.join(score_card(i+1, b, se[b], 'score', SERP_PARTS, b.startswith('SpearPoint'), note=SERP_NOTES[b], show_kw=True) for i, b in enumerate(rank_s)) + '</div>'
serp_html += '<div class="note-box"><b>What this means:</b> these four were chosen because they show up most often in Google\'s top 10 across the 6 priority-keyword searches (directories, forums and software vendors excluded). They outscore SpearPoint mainly on Domain Trust and size, not on B2B focus. Optimist shows a B2B specialist can win “aeo agency” and “ai search optimization agency” with list-style pages and links, without Thrive-level scale.</div>' + SERP_METHOD


# ---------------- Domain Trust section ----------------
DT = L('domain_trust.json')
def dt_chart():
    W,H,pL,pR,pT,pB=1100,320,40,140,16,30
    ms=DT['months']; n=len(ms); x=lambda i:pL+i*(W-pL-pR)/(n-1); lo,hi=30,90; y=lambda v:pT+(hi-v)/(hi-lo)*(H-pT-pB)
    g=f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Domain Trust over 12 months">'
    for v in range(30,91,10):
        g+=f'<line x1="{pL}" x2="{W-pR}" y1="{y(v)}" y2="{y(v)}" stroke="#E6E5D5"/><text x="{pL-6}" y="{y(v)+4}" font-size="10" fill="#5C6B77" text-anchor="end">{v}</text>'
    for i,m in enumerate(ms):
        if i%2==0: g+=f'<text x="{x(i)}" y="{H-8}" font-size="10" fill="#5C6B77" text-anchor="middle">{["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(m[5:])-1]} {m[2:4]}</text>'
    labels=[]
    for b,vals in DT['series'].items():
        c=colors[b]; w=3.5 if b.startswith('SpearPoint') else 2
        g+=f'<polyline points="{" ".join(f"{x(i)},{y(v)}" for i,v in enumerate(vals))}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>'
        g+=f'<circle cx="{x(n-1)}" cy="{y(vals[-1])}" r="4" fill="{c}"><title>{b}: {vals[-1]}</title></circle>'
        labels.append([y(vals[-1]),b,vals[-1],c])
    labels.sort(); last=-99
    for ly,b,v,c in labels:
        ly=max(ly,last+13); last=ly
        g+=f'<text x="{W-pR+8}" y="{ly+4}" font-size="11" fill="{c if c!="#C7CBB9" else "#8A8E7C"}" font-weight="700">{v} {e(b.replace(" Marketing",""))}</text>'
    return g+'</svg>'
q=DT['quality']
dt_rows=''
for b in sorted(order,key=lambda b:-DT['series'][b][-1]):
    v=DT['series'][b]; qq=q[b]; cl=' class="row-client"' if b.startswith('SpearPoint') else ''
    dt_rows+=f'<tr{cl}><td><b>{e(b)}</b></td><td class="cell-num"><b>{v[-1]}</b></td><td class="cell-num up">+{v[-1]-v[0]}</td><td class="cell-num">{qq["total"]:,}</td><td class="cell-num">{qq["hi"]:,} <span class="muted">({qq["hi"]/qq["total"]*100:.0f}%)</span></td><td class="cell-num">{qq["low"]/qq["total"]*100:.0f}%</td></tr>'
bk=DT['sp_buckets']; bmax=max(c for _,c in bk)
bucket_rows=''.join(f'<div class="bar-row"><span><b>{e(l)}</b></span><div class="bar-track"><div class="bar-fill" style="width:{c/bmax*100:.1f}%;background:{"#F1735C" if i==0 else "#4DB859" if i>=3 else "#93A0A8"}"></div></div><span class="bar-val">{c} domains</span></div>' for i,(l,c) in enumerate(bk))
nl=DT['newlost']; nmax=max(nl['gained'])
nl_rows=''.join(f'<div class="bar-row"><span><b>{m}</b></span><div class="bar-track"><div class="bar-fill" style="width:{g/nmax*100:.1f}%;background:#1D3853"></div></div><span class="bar-val">+{g} new · −{lo} lost</span></div>' for m,g,lo in zip(nl['months'],nl['gained'],nl['lost']))
sp_hist=DT['series']['SpearPoint Marketing']
dt_html=f"""<div class="split-col mini"><h4>Domain Trust, last 12 months</h4><div class="dt-chart">{dt_chart()}</div>
<p class="progress-note">SpearPoint (thick green line) went from 34 in Aug 2025 to {sp_hist[-1]} today. Over the last 12 months every brand in the set gained Domain Trust: Flow Agency +20, TrioSEO +14, Breaking B2B +11, SpearPoint +9, Thrive Digital +7. SpearPoint is climbing, but not fast enough to close the gap on its own.</p></div>
<div class="split-col mini" style="margin-top:20px;"><h4>Link quality behind the score</h4>
<div class="table-wrap"><table><thead><tr><th>Brand</th><th class="cell-num">Domain Trust</th><th class="cell-num">12-mo change</th><th class="cell-num">Referring domains</th><th class="cell-num">From DT 50+ sites</th><th class="cell-num">From DT 0&ndash;9 sites</th></tr></thead><tbody>{dt_rows}</tbody></table></div>
<p class="progress-note">Links from high-trust sites (Domain Trust 50+) move the score most. SpearPoint has 64 of them, about a third of what Flow Agency (198) and TrioSEO (222) have.</p></div>
<div class="split-two" style="margin-top:20px;">
<div class="split-col mini"><h4>SpearPoint's referring domains by their Domain Trust</h4><div class="bar-list">{bucket_rows}</div>
<p class="progress-note">68% of SpearPoint's referring domains have a Domain Trust under 10, the highest share in the competitive set (53&ndash;63% for the others).</p></div>
<div class="split-col mini"><h4>New vs. lost referring domains</h4><div class="bar-list">{nl_rows}</div>
<p class="progress-note">Most of the 283 new referring domains in October and November look like the spam wave noted in the roadmap: 265 sites linking with the same “Premium SEO Link Building Experts&hellip;” anchor. They inflate the referring-domain count without adding trust. Reviewing them for a disavow file is roadmap item 11.</p></div>
</div>
<div class="note-box"><b>What this means:</b> Domain Trust is SpearPoint's biggest gap. It is 10&ndash;29 points behind every targeted competitor and 25&ndash;39 behind the top SERP competitors. It is likely a big part of why pages like /b2b-seo stall at #9&ndash;11 instead of reaching the top 5. Closing it means earning links from real, high-trust sites (B2B publications, Denver/Colorado business sources, podcasts and partner pages), not adding more links. About 4&ndash;6 a month would roughly double SpearPoint's DT 50+ link count within a year.</div>"""

# ---------------- impressions by theme ----------------
cats = ana['cats']; tot_i = sum(v[1] for v in cats.values())
cat_colors = {'Other SEO topics':'#B7C2C7','B2B & industries':'#4DB859','Fitness':'#93A0A8','Ecommerce':'#6F818A','Denver / Colorado':'#1D3853','AI Search / AEO':'#2F7A3B','Conversion / CRO':'#F1735C','Brand':'#D8D5C2'}
mx = max(v[1] for v in cats.values())
theme_rows = ''.join(
    f'<div class="bar-row"><span><b>{e(k)}</b></span><div class="bar-track"><div class="bar-fill" style="width:{v[1]/mx*100:.1f}%;background:{cat_colors.get(k,"#999")}"></div></div><span class="bar-val">{(f'{v[1]/1000:,.0f}K' if v[1]>=1000 else f'{v[1]:,}')} · {v[0]} click{'' if v[0]==1 else 's'}</span></div>'
    for k, v in sorted(cats.items(), key=lambda x: -x[1][1]))

# ---------------- top queries & pages ----------------
nonbrand = [r for r in Q if 'spearpoint' not in r[0]]
top_q = sorted(nonbrand, key=lambda r: (-r[1], -r[2]))[:10]
top_p = sorted(P, key=lambda r: (-r[1], -r[2]))[:10]
short = lambda u: u.replace('https://www.thespearpoint.com', '') or '/'
tq = ''.join(f'<tr><td>{e(r[0])}</td><td class="cell-num">{r[1]}</td><td class="cell-num">{r[2]:,}</td><td class="cell-num">{r[3]}</td></tr>' for r in top_q)
tp = ''.join(f'<tr><td class="url">{e(short(r[0]))}</td><td class="cell-num">{r[1]}</td><td class="cell-num">{r[2]:,}</td><td class="cell-num">{r[3]}</td></tr>' for r in top_p)
brand_clicks = sum(r[1] for r in Q if 'spearpoint' in r[0]); q_clicks = sum(r[1] for r in Q)

# striking distance
sd = ''.join(f'<tr><td>{e(r[0].replace(chr(10)," "))}</td><td class="cell-num">{r[2]:,}</td><td class="cell-num pos-pill">{r[3]}</td><td class="cell-num">{r[1]}</td></tr>' for r in [x for x in ana['striking'] if '\n' not in x[0] and '?' not in x[0] and 'example' not in x[0]][:12])

# ---------------- roadmap ----------------
R = [
 ('Days 1&ndash;30', 'Quick Wins &mdash; Retarget Pages That Already Exist', 'Edits to live pages only: titles, H1s, FAQs and internal links. No new pages, so Google can re-rank them within weeks.', [
  ('existing','Fix and retarget the AEO / AI Search service page','The H1 on /aeo-ai-search-services reads “AI SEARCH + AEO SERVICES SERVICES,” and the page earned only 543 impressions in 16 months. Fix the typo and retitle it “AEO Agency &amp; AI Search Optimization Agency” to match two priority keywords that aren\'t in the top 100 today: “aeo agency” (590/mo, KD 16) and “ai search optimization agency” (480/mo, KD 36). Add an FAQ block and a short “why an agency” section, since Google\'s top results for both are agency pages and agency lists.'),
  ('existing','Push /b2b-seo onto page 1 for “B2B SEO Agency”','/b2b-seo has bounced between #9 and #11 for “b2b seo agency” all week, right at the edge of page 1. Its H1 says “Conversion Based B2B SEO.” Lead the title and H1 with “B2B SEO Agency,” move the conversion message into the subhead, and add internal links from the B2B blog posts. Related terms “b2b seo services” and “b2b seo company” (480/mo each, KD 10&ndash;18) come along with it.'),
  ('existing','Give Denver its own focused page','Denver content lives on /seo, which also ranks nationally for “seo company” (48K impressions at #46), so it pulls in two directions. Move the Denver content to a /denver-seo-company URL (redirect /seo), keep the new “Denver SEO Company” title, use a single H1, and fix the H2 typo “SEO what Wins Denver.” SpearPoint is #14 for “denver seo company” and close variants already rank (“seo denver” #14, “seo agency denver” #21), and “denver seo” carries 2,900 searches a month.'),
  ('existing','Turn the free audit into a Denver SEO audit landing page','Google already shows SpearPoint at #9&ndash;11 for “denver seo audit” (2,389 impressions over 16 months), “seo audit service denver” and “denver website seo audit service,” but none have produced a click. A dedicated audit page with a form puts the offer in front of people searching for it.'),
  ('existing','Use the #4 “Conversion Based SEO” ranking as proof, and add FAQs','SpearPoint has held #4 for “conversion based seo” every day this week. The phrase has almost no search volume, so its value is as a brand signature. Add FAQs and schema to /conversion-based-seo and /conversion-rate-optimization (neither has one) to lift “seo cro agency” from about #56. Use the phrase in sales emails and decks so buyers who Google it find SpearPoint.'),
 ]),
 ('Days 31&ndash;60', 'Close the Competitor Keyword Gaps', 'New and expanded pages for keywords where Breaking B2B, TrioSEO and Flow Agency rank and SpearPoint does not. These are the gaps closest to a buying decision.', [
  ('existing','Expand /b2b-seo/saas into a full SaaS SEO services page','Breaking B2B ranks #1 for “saas seo services” (390/mo), “best saas seo agencies” (320) and “seo agencies for saas” (260). SpearPoint\'s /b2b-seo/saas page has 6K impressions at #27, and the homepage claims a 5X free-trial result for a B2B SaaS client. Lead with that proof.'),
  ('new','Build an LLM SEO / GEO agency page','Breaking B2B ranks #1&ndash;2 for “llm seo agency” (140) and “llm seo services” (170), and Flow Agency ranks #12. Related terms: “ai seo agency” (810/mo, KD 24) and “llm seo” (360). SpearPoint already has GEO/LLMO blog posts ranking #15&ndash;19 that can link to the new page.'),
  ('existing','Strengthen the industry pages buyers already find','Professional services and cybersecurity are already in striking distance: “seo for professional services firms” (#19.8, 7.1K impressions), “cyber security seo services” (#14.7) and “cybersecurity seo agency” (#20). Expand /cybersecurity-seo and the professional-services post into service pages with case studies and a clear audit CTA. TrioSEO\'s “seo for tech companies” page (260/mo, KD 8) shows the format works.'),
  ('existing','Publish a “How to choose a B2B SEO agency” comparison guide','“best b2b seo agency” costs $29.68 per click in ads, a sign of strong buyer intent. TrioSEO ranks for “how to choose seo company” (140/mo). SpearPoint has a “how to hire the best B2B SEO agency” post with 4 referring domains. Refresh it into a checklist plus comparison page that ends with the free audit.'),
  ('new','Launch a B2B case study hub','Breaking B2B and TrioSEO rank #1 for “saas seo case study” (90/mo), and Breaking B2B ranks #29 for “b2b seo case study” (70/mo, $20.63 CPC). SpearPoint\'s results (5X free trials, record ecommerce sales) sit on the homepage. Give each one an indexable page with numbers, timeline and process.'),
 ]),
 ('Days 61&ndash;90', 'Build Authority &amp; Turn Traffic Into Leads', 'Investments that raise every page at once: authority, link equity and conversion paths.', [
  ('new','Audit and disavow spam backlinks','265 of SpearPoint\'s 426 referring domains link with the same spam anchor (“Premium SEO Link Building Experts&hellip;”), plus a “darksidelinks” Telegram pattern. Every competitor has a similar footprint, so this looks like a negative-SEO network rather than anything SpearPoint did. Review it and submit a disavow file so the real link profile counts.'),
  ('new','Close the authority gap with digital PR','SpearPoint\'s Domain Trust is 50 vs. 60&ndash;79 for the targeted competitors, and only 64 of its referring domains have a Domain Trust of 50+ (Flow Agency: 198). TrioSEO has 904 referring domains, Flow Agency 762 and Breaking B2B 532. Aim for 4&ndash;6 earned links a month from B2B publications, Denver/Colorado sources (Built In Colorado and Clutch Denver both rank for “seo denver”) and guest podcasts.'),
  ('existing','Route high-traffic blog posts to service pages','In the last 90 days, ecommerce and fitness content drove about 105K impressions, more than B2B topics (72K). Add B2B CTAs and internal links from the top B2B posts (CTAs for B2B websites: 78 clicks; B2B case studies on websites: 17K impressions) to /b2b-seo, the AEO page and the audit page.'),
  ('new','Add a retainer and pricing explainer','TrioSEO ranks #1 for “seo retainers” (110/mo) and #8 for “seo monthly retainer” (70/mo). SpearPoint\'s /pricing page already sits at avg. position 5.7, so adding retainer language and FAQs there is a low-effort way to capture buyers comparing costs.'),
  ('new','Connect rankings to leads (sets up the CRO dashboard)','The 6 priority keywords are now tracked daily in SE Ranking, and monthly snapshots go to Supabase. Next, connect GA4 form fills to organic landing pages so this report can show leads by page, the bridge to the CRO + Website dashboard.'),
 ]),
]
n = 0; road = []
for badge, title, sub, items in R:
    cards_ = []
    for kind, h, p in items:
        n += 1
        flag = '<span class="imp-flag flag-existing">Existing page &mdash; retarget</span>' if kind == 'existing' else '<span class="imp-flag flag-new">New build</span>'
        cards_.append(f'<div class="imp-card"><div class="imp-num">{n:02d}</div><div class="imp-body">{flag}<h4>{h}</h4><p>{p}</p></div></div>')
    road.append(f'<div class="phase"><div class="phase-head"><span class="phase-badge">{badge}</span><h3>{title}</h3></div><p class="phase-sub">{sub}</p><div class="imp-grid">{"".join(cards_)}</div></div>')
road_html = '<div class="roadmap">' + ''.join(road) + '</div>'

# ---------------- embedded data for JS tables ----------------
data = dict(
  monthly=[m for m in trend['monthly'] if m[0] not in ('2025-07','2026-11')],
  kw=L('keywords_ranked.json'), gaps=gaps, queries=Q, pages=[[short(r[0])] + r[1:] for r in P],
)
data_json = json.dumps(data, separators=(',', ':')).replace('</', '<\\/')

legend = ''.join(f'<div class="legend-item"><span class="swatch" style="background:{colors[b]}"></span>{e(b)}{" (client)" if b.startswith("SpearPoint") else ""}</div>' for b in order)

def section(cls, kicker, title, desc, body, id_=''):
    return f'''<section class="block {cls}"{f' id="{id_}"' if id_ else ''}><div class="wrap"><div class="section-head"><div class="kicker">{kicker}</div><h2>{title}</h2>{f'<p>{desc}</p>' if desc else ''}</div>{body}</div></section>'''

def tbl(id_, controls=''):
    return f'''<div class="table-controls"><input class="search-box" id="{id_}Search" placeholder="Search…">{controls}</div>
<div class="table-wrap"><table id="{id_}Table"><thead></thead><tbody></tbody></table></div>
<div class="pagination" id="{id_}Pager"></div>'''

theme_chips = '<div class="filter-chips"><span class="filter-group-label">Theme</span>' + ''.join(
    f'<button class="filter-btn{" active" if t=="All" else ""}" data-f="{t}">{t}</button>' for t in ['All','B2B SEO','Denver SEO','AI Search / AEO','Conversion SEO / CRO']) + '</div>'
gap_chips = '<div class="filter-chips"><span class="filter-group-label">Competitor</span>' + ''.join(
    f'<button class="filter-btn{" active" if t=="All" else ""}" data-f="{t}">{t}</button>' for t in ['All','Breaking B2B','TrioSEO','Flow Agency']) + '</div>'

body = []
body.append(section('', 'Snapshot', 'KPI Summary', f'Google Search Console, last 90 days ({ "Aug 13" } &ndash; Nov 10, 2026) vs. the 90 days before. Priority-keyword ranks from SE Ranking on Nov 16, 2026.', kpis))
body.append(section('alt', 'Trend', 'Progress Over Time', 'Last 12 months of organic clicks and impressions from Google Search Console, loaded from SpearPoint\'s Supabase snapshot history. New months are added at each monthly refresh.',
  '<div class="progress-card"><div id="trendChart"></div><div class="chart-legend"><span><i style="background:#4DB859"></i>Clicks (left axis)</span><span><i style="background:#1D3853;height:3px;"></i>Impressions (right axis)</span></div><div class="progress-note" id="trendNote"></div></div>'))
body.append(section('', 'Competitive Landscape', 'SpearPoint vs. the Targeted Competitors',
  'The four agencies SpearPoint monitors across the SEO, AI Search and CRO reports, ranked by SEO Strength Score (overall organic strength, not including the priority keywords). Organic data is US-only from SE Ranking. Priority-keyword ranks were checked Nov 16, 2026.',
  cmp_html + '<div class="note-box"><b>What this means:</b> SpearPoint trails all four on Domain Trust (50 vs. 60&ndash;79) and on organic size, which puts it last on SEO Strength. Its edge is focus: it is the only one of the five ranking for any of the 6 priority keywords (see the next section). Flow Agency leads the group on size: 2,115 ranking keywords and 330 in the top 10.</div>' + SCORE_METHOD))
body.append(section('alt score-blue', 'Client Priority', 'Where SpearPoint Ranks for the 6 Priority Keywords',
  'SpearPoint\'s position for each priority keyword, who outranks it, the related keywords SpearPoint already ranks for (partial coverage), and related keywords with more search demand. Main ranks come from SE Ranking\'s daily tracker, or a live Google check where the keyword isn\'t tracked. Partial coverage comes from SE Ranking\'s keyword database for thespearpoint.com (US). Volumes are US monthly averages.', pk_html))
body.append(section('', 'SERP Competitors', 'Top 4 SERP Competitors vs. SpearPoint',
  'The agencies Google actually ranks for SpearPoint\'s priority keywords, with SpearPoint included for comparison. Scored on SERP Competitiveness, which includes the priority keywords.', serp_html))
body.append(section('alt', 'Domain Trust', 'Domain Trust: SpearPoint vs. the Competition',
  'Domain Trust is SE Ranking\'s 0&ndash;100 score for how authoritative a website is, based on the number and quality of sites linking to it. Higher Domain Trust makes every page easier to rank. Data from SE Ranking Backlinks, Nov 16, 2026.', dt_html))
body.append(section('', 'Google Search Console', 'Top Performing Queries &amp; Pages',
  f'Client data from SpearPoint\'s own Google Search Console account (www.thespearpoint.com), last 90 days (Aug 13 &ndash; Nov 10, 2026), the same window as the KPI Summary. Brand searches (“spearpoint marketing”) account for {brand_clicks} of {q_clicks} clicks on identifiable queries, so they are removed from the query list below to show which topics bring new visitors.',
  f'''<div class="split-two">
<div class="split-col mini"><h4>Top non-brand queries</h4><div class="table-wrap"><table><thead><tr><th>Query</th><th class="cell-num">Clicks</th><th class="cell-num">Impr.</th><th class="cell-num">Pos.</th></tr></thead><tbody>{tq}</tbody></table></div></div>
<div class="split-col mini"><h4>Top pages</h4><div class="table-wrap"><table><thead><tr><th>Page</th><th class="cell-num">Clicks</th><th class="cell-num">Impr.</th><th class="cell-num">Pos.</th></tr></thead><tbody>{tp}</tbody></table></div></div>
</div>
<div class="split-two" style="margin-top:20px;">
<div class="split-col mini"><h4>Where impressions come from (by topic)</h4><div class="bar-list">{theme_rows}</div>
<p class="progress-note">Ecommerce and fitness content still drives a large share of impressions. B2B, AI Search and Denver topics are the ones tied to this campaign's lead goal.</p></div>
<div class="split-col mini"><h4>Striking distance: B2B queries at positions 4&ndash;20</h4><div class="table-wrap"><table><thead><tr><th>Query</th><th class="cell-num">Impr.</th><th class="cell-num">Pos.</th><th class="cell-num">Clicks</th></tr></thead><tbody>{sd}</tbody></table></div>
<p class="progress-note">These already rank close to page 1. Small on-page improvements here tend to produce clicks fastest.</p></div>
</div>'''))
body.append(section('alt', 'What Changed This Month', 'Priority Keyword Movement',
  'Rank changes for the priority keywords between monthly snapshots in Supabase.',
  '<div class="locked-card" id="changesLocked"><strong>Not yet available</strong>Baseline captured on November 16, 2026. This section activates after the December snapshot, once two months of ranks exist to compare.</div><div id="changesBody" class="hidden"></div>'))
body.append(section('', 'Full Detail', 'Keyword Research',
  'The 6 client-requested keywords (★) plus related variants from SE Ranking (US). Difficulty runs 0&ndash;100; CPC is the average Google Ads cost per click, a proxy for commercial value. <b>SpearPoint rank</b> shows where thespearpoint.com ranks today: from SE Ranking\'s daily tracker where the keyword is tracked, otherwise SE Ranking\'s keyword database (monthly US snapshot), otherwise SpearPoint\'s own Search Console average position for the last 90 days. 17 of the 37 keywords rank in the top 100; only 1 (“conversion based seo”, #4) is on page 1.',
  tbl('kw', theme_chips)))
body.append(section('alt', 'Full Detail', 'Competitor Keyword Gaps',
  'Keywords where a targeted competitor ranks in Google\'s top 100 and SpearPoint does not, filtered from SE Ranking\'s gap report to service-relevant terms (branded and off-topic keywords removed).',
  tbl('gap', gap_chips)))
body.append(section('', 'Full Detail', 'All Search Console Queries (Top 1,000)', 'Client data from SpearPoint\'s own Google Search Console account (www.thespearpoint.com). Last 90 days (Aug 13 &ndash; Nov 10, 2026). Click any column header to sort.', tbl('q')))
body.append(section('alt', 'Full Detail', f'All Search Console Pages ({len(P)})', 'Client data from SpearPoint\'s own Google Search Console account (www.thespearpoint.com). Last 90 days (Aug 13 &ndash; Nov 10, 2026). Click any column header to sort.', tbl('p')))
body.append(section('roadmap-beige', 'Action Plan', 'Where SpearPoint Can Improve: 90-Day Roadmap',
  'Fifteen data-backed moves sequenced for lead generation: retarget existing pages first (fastest to move), then close the competitor keyword gaps, then build the authority and conversion paths that lift everything.', road_html))

method = ('Sources: Google Search Console (www.thespearpoint.com property; daily data through Nov 10, 2026, exported Nov 13, 2026); '
  'SE Ranking keyword metrics, live Google SERP checks (US; Denver, CO for “seo denver”), domain overviews, keyword-gap comparisons and Backlinks Summary, Domain Trust history and referring-domain trust distribution. '
  'Search Console reports up to 1,000 queries per export, and very rare queries are hidden for privacy, so query-level clicks add up to less than total clicks. '
  'Competitor traffic figures are SE Ranking estimates, not actual analytics. Monthly snapshots are stored in Supabase (b2b_seo_* tables). Prepared by SpearPoint Marketing.')

JS = r"""
const D = JSON.parse(document.getElementById('dashData').textContent);
const SUPABASE_URL = 'https://rcrpcdorpyexpqvjmesu.supabase.co';
const SUPABASE_KEY = 'sb_publishable_B-pCYNN_GPP6Ew_27ChI3w_OJas9-Vq';
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = n => n == null ? '—' : Number(n).toLocaleString('en-US');
async function sb(table, query) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/${table}?${query}`, { headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}` } });
  if (!r.ok) throw new Error(table + ' ' + r.status);
  return r.json();
}

// ---------- Trend chart ----------
function drawTrend(rows, source) {
  const W = 980, H = 320, pL = 46, pR = 64, pT = 18, pB = 36, pw = W - pL - pR, ph = H - pT - pB;
  const n = rows.length, bw = pw / n * 0.56;
  const maxC = Math.ceil(Math.max(...rows.map(r => r.c)) / 40) * 40;
  const maxI = Math.ceil(Math.max(...rows.map(r => r.i)) / 100000) * 100000;
  const x = i => pL + (i + 0.5) * pw / n;
  const yc = v => pT + ph - v / maxC * ph, yi = v => pT + ph - v / maxI * ph;
  const posMin = 20, posMax = 70, yp = v => pT + (v - posMin) / (posMax - posMin) * ph;
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Monthly organic clicks and impressions">`;
  for (let k = 0; k <= 4; k++) {
    const v = maxC * k / 4, gy = yc(v);
    s += `<line x1="${pL}" x2="${W - pR}" y1="${gy}" y2="${gy}" stroke="#E6E5D5"/>`;
    s += `<text x="${pL - 8}" y="${gy + 4}" font-size="10.5" fill="#5C6B77" text-anchor="end">${Math.round(v)}</text>`;
    s += `<text x="${W - pR + 8}" y="${gy + 4}" font-size="10.5" fill="#5C6B77">${Math.round(maxI * k / 4 / 1000)}K</text>`;
  }
  rows.forEach((r, i) => {
    s += `<rect x="${x(i) - bw / 2}" y="${yc(r.c)}" width="${bw}" height="${pT + ph - yc(r.c)}" rx="3" fill="#4DB859"><title>${r.m}: ${r.c} clicks</title></rect>`;
    s += `<text x="${x(i)}" y="${yc(r.c) - 5}" font-size="10" fill="#2F7A3B" text-anchor="middle" font-weight="700">${r.c}</text>`;
    const d = new Date(r.m + '-01T00:00:00Z');
    s += `<text x="${x(i)}" y="${H - 14}" font-size="10.5" fill="#5C6B77" text-anchor="middle">${d.toLocaleDateString('en-US', { month: 'short', timeZone: 'UTC' })}</text>`;
    if (d.getUTCMonth() === 0 || i === 0) s += `<text x="${x(i)}" y="${H - 2}" font-size="9.5" fill="#93A0A8" text-anchor="middle">${d.getUTCFullYear()}</text>`;
  });
  s += `<polyline points="${rows.map((r, i) => `${x(i)},${yi(r.i)}`).join(' ')}" fill="none" stroke="#1D3853" stroke-width="2.5" stroke-linejoin="round"/>`;
  rows.forEach((r, i) => s += `<circle cx="${x(i)}" cy="${yi(r.i)}" r="3.5" fill="#1D3853"><title>${r.m}: ${fmt(r.i)} impressions</title></circle>`);
  s += `</svg>`;
  document.getElementById('trendChart').innerHTML = s;
  document.getElementById('trendNote').textContent = `Last ${rows.length} full months (${source}). Hover any bar or point for exact values. November 2026 is a partial month and is excluded.`;
}
const fallbackTrend = D.monthly.slice(-12).map(m => ({ m: m[0], c: m[2], i: m[3], p: m[4] }));
drawTrend(fallbackTrend, 'Google Search Console');
sb('b2b_seo_snapshots', 'select=period_start,period_end,gsc_clicks,gsc_impressions,gsc_avg_position&notes=like.GSC%20monthly*&order=period_start.asc')
  .then(rows => { if (rows.length >= 2) drawTrend(rows.slice(-12).map(r => ({ m: r.period_start.slice(0, 7), c: r.gsc_clicks, i: r.gsc_impressions, p: Number(r.gsc_avg_position) })), 'Supabase snapshot history'); })
  .catch(() => {});

// ---------- What changed ----------
sb('b2b_seo_keyword_snapshots', 'select=snapshot_date,keyword,location,spearpoint_position,volume&is_priority=eq.true&order=snapshot_date.desc')
  .then(rows => {
    const dates = [...new Set(rows.map(r => r.snapshot_date))].sort().reverse();
    if (dates.length < 2) return;
    const [cur, prev] = dates, key = r => r.keyword + '|' + r.location;
    const P = Object.fromEntries(rows.filter(r => r.snapshot_date === prev).map(r => [key(r), r]));
    const items = rows.filter(r => r.snapshot_date === cur).map(r => {
      const a = P[key(r)]?.spearpoint_position, b = r.spearpoint_position;
      const delta = (a ?? 101) - (b ?? 101);
      return { r, a, b, delta };
    });
    const gain = items.filter(x => x.delta > 0), loss = items.filter(x => x.delta < 0);
    const row = x => `<div class="change-row"><span class="cr-prompt">${esc(x.r.keyword)}<span class="cr-topic">${esc(x.r.location)}</span></span><span class="cr-vol">${x.a ? '#' + x.a : '—'} → ${x.b ? '#' + x.b : '—'}</span></div>`;
    document.getElementById('changesBody').innerHTML = `<div class="changes-summary"><div class="changes-stat cs-gain"><div class="cs-num">${gain.length}</div><div class="cs-label">Keywords improved</div></div><div class="changes-stat cs-loss"><div class="cs-num">${loss.length}</div><div class="cs-label">Keywords declined</div></div><div class="changes-stat"><div class="cs-num">${items.filter(x => x.b && x.b <= 10).length}</div><div class="cs-label">On page 1 now</div></div></div>
      <div class="changes-cols"><div class="changes-col gain"><h4>Improved since ${prev}</h4>${gain.map(row).join('') || '<div class="changes-empty">No gains this month.</div>'}</div><div class="changes-col loss"><h4>Declined since ${prev}</h4>${loss.map(row).join('') || '<div class="changes-empty">No declines this month.</div>'}</div></div>`;
    document.getElementById('changesLocked').classList.add('hidden');
    document.getElementById('changesBody').classList.remove('hidden');
  }).catch(() => {});

// ---------- Generic table ----------
function pageNums(cur, pages) {
  const lo = Math.max(1, Math.min(cur - 2, pages - 4)), hi = Math.min(pages, lo + 4);
  let h = '';
  for (let i = lo; i <= hi; i++) h += `<button data-p="${i}" class="${i === cur ? 'pg-on' : ''}">${i}</button>`;
  return h;
}
function makeTable(id, cols, rows, opts = {}) {
  const st = { q: '', f: 'All', sort: opts.sort ?? null, asc: false, page: 1, per: opts.per || 25 };
  const table = document.getElementById(id + 'Table');
  table.querySelector('thead').innerHTML = '<tr>' + cols.map((c, i) => `<th data-i="${i}" class="${c.num ? 'cell-num' : ''}">${c.h}</th>`).join('') + '</tr>';
  function render() {
    let r = rows.filter(x => (!st.q || cols.some(c => String(c.v(x)).toLowerCase().includes(st.q))) && (st.f === 'All' || opts.filter(x, st.f)));
    if (st.sort != null) { const c = cols[st.sort]; r = [...r].sort((a, b) => { const A = c.s ? c.s(a) : c.v(a), B = c.s ? c.s(b) : c.v(b); return (A > B ? 1 : A < B ? -1 : 0) * (st.asc ? 1 : -1); }); }
    const pages = Math.max(1, Math.ceil(r.length / st.per)); st.page = Math.min(st.page, pages);
    const view = r.slice((st.page - 1) * st.per, st.page * st.per);
    table.querySelector('tbody').innerHTML = view.map(x => '<tr>' + cols.map(c => `<td class="${c.num ? 'cell-num' : ''} ${c.cls || ''}">${c.r ? c.r(x) : esc(c.v(x))}</td>`).join('') + '</tr>').join('') || `<tr><td colspan="${cols.length}" style="text-align:center;color:#5C6B77;padding:20px;">No matches</td></tr>`;
    document.getElementById(id + 'Pager').innerHTML = `<span>Showing <b>${fmt(r.length)}</b> rows</span>` + (pages > 1 ? `<span>Page <b>${st.page}</b> of <b>${pages}</b></span><div class="pg-btns"><button data-p="1" ${st.page === 1 ? 'disabled' : ''}>First</button><button data-p="${st.page - 1}" ${st.page === 1 ? 'disabled' : ''}>Prev</button>${pageNums(st.page, pages)}<button data-p="${st.page + 1}" ${st.page === pages ? 'disabled' : ''}>Next</button><button data-p="${pages}" ${st.page === pages ? 'disabled' : ''}>Last</button></div>` : '');
    document.querySelectorAll('#' + id + 'Pager button').forEach(b => b.onclick = () => { st.page = +b.dataset.p; render(); });
  }
  document.getElementById(id + 'Search').oninput = ev => { st.q = ev.target.value.toLowerCase(); st.page = 1; render(); };
  table.querySelectorAll('th').forEach(th => th.onclick = () => { const i = +th.dataset.i; st.asc = st.sort === i ? !st.asc : !!cols[i].asc; st.sort = i; render(); });
  const chips = table.closest('.wrap').querySelectorAll('.filter-btn');
  chips.forEach(b => b.onclick = () => { chips.forEach(c => c.classList.remove('active')); b.classList.add('active'); st.f = b.dataset.f; st.page = 1; render(); });
  render();
}
const pos = p => p == null ? '—' : `<span class="pos-pill ${p <= 10 ? 'pos-good' : p <= 20 ? 'pos-mid' : ''}">${p}</span>`;
makeTable('kw', [
  { h: 'Keyword', v: x => x[0], r: x => (x[6] ? '★ ' : '') + (x[6] ? '<b>' + esc(x[0]) + '</b>' : esc(x[0])), asc: true },
  { h: 'Theme', v: x => x[5], r: x => `<span class="cell-topic-tag">${esc(x[5])}</span>`, asc: true },
  { h: 'Volume', v: x => x[1] ?? -1, r: x => x[1] == null ? 'n/a' : fmt(x[1]), num: true },
  { h: 'Difficulty', v: x => x[3] ?? -1, r: x => x[3] ?? '—', num: true, asc: true },
  { h: 'CPC', v: x => x[2] ?? -1, r: x => x[2] == null ? '—' : '$' + Number(x[2]).toFixed(2), num: true },
  { h: 'Intent', v: x => x[4], r: x => esc((x[4]||'').split(',').map(c => ({I:'Informational',C:'Commercial',L:'Local',N:'Navigational',T:'Transactional'}[c]||c)).join(', ')) },
  { h: 'SpearPoint rank', v: x => x[7] ?? 999, r: x => x[7] ? pos(x[7]) : '<span class="pos-none-t">Not ranking</span>', num: true, asc: true },
  { h: 'Ranking page &middot; source', v: x => x[9], r: x => `${x[8] ? '<b>' + esc(x[8]) + '</b><br>' : ''}<span class="src-t">${esc(x[9])}</span>` }
], D.kw, { sort: 2, filter: (x, f) => x[5].startsWith(f.split(' ')[0]) , per: 10 });
makeTable('gap', [
  { h: 'Keyword', v: x => x[0], asc: true },
  { h: 'Volume', v: x => x[1], r: x => fmt(x[1]), num: true },
  { h: 'Difficulty', v: x => x[2], num: true, asc: true },
  { h: 'CPC', v: x => x[3], r: x => x[3] ? '$' + x[3].toFixed(2) : '—', num: true },
  { h: 'Competitor', v: x => x[4] },
  { h: 'Their rank', v: x => x[5], r: x => pos(x[5]), num: true, asc: true },
  { h: 'Their page', v: x => x[6], cls: 'url' },
  { h: 'Theme', v: x => x[7], r: x => `<span class="cell-topic-tag">${esc(x[7])}</span>` },
  { h: 'Build', v: x => x[8] }
], D.gaps, { sort: 1, filter: (x, f) => x[4].includes(f), per: 10 });
makeTable('q', [
  { h: 'Query', v: x => x[0], asc: true },
  { h: 'Clicks', v: x => x[1], num: true },
  { h: 'Impressions', v: x => x[2], r: x => fmt(x[2]), num: true },
  { h: 'CTR', v: x => x[2] ? x[1] / x[2] : 0, r: x => (x[2] ? (x[1] / x[2] * 100).toFixed(2) : '0.00') + '%', num: true },
  { h: 'Avg. position', v: x => x[3], r: x => pos(x[3]), num: true, asc: true }
], D.queries, { sort: 1 });
makeTable('p', [
  { h: 'Page', v: x => x[0], cls: 'url', asc: true },
  { h: 'Clicks', v: x => x[1], num: true },
  { h: 'Impressions', v: x => x[2], r: x => fmt(x[2]), num: true },
  { h: 'CTR', v: x => x[2] ? x[1] / x[2] : 0, r: x => (x[2] ? (x[1] / x[2] * 100).toFixed(2) : '0.00') + '%', num: true },
  { h: 'Avg. position', v: x => x[3], r: x => pos(x[3]), num: true, asc: true }
], D.pages, { sort: 1 });
"""

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>SEO Performance &mdash; SpearPoint Marketing vs. B2B SEO Competitors</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<header class="report-header">
  <div class="header-inner">
    <img src="{logo_h}" alt="SpearPoint Marketing">
    <div class="header-meta">Generated {GEN_DATE}<br>Region: United States &middot; Denver, CO</div>
  </div>
  <div class="eyebrow-row">
    <div class="eyebrow">SEO Performance Report</div>
    <h1 class="report-title">SpearPoint Marketing SEO Dashboard - B2B</h1>
    <p class="report-sub">Organic search performance for thespearpoint.com, tracked against Breaking B2B, TrioSEO, Flow Agency and Thrive Digital. Campaign goal: more leads from B2B companies searching for SEO and AI Search services. Sources: Google Search Console &middot; SE Ranking.</p>
    <div class="legend-row">{legend}</div>
  </div>
</header>
<nav class="report-nav"><div class="wrap"><a href="./#overview" target="_top" onclick="if(window.parent!==window&&parent.showTab){{parent.showTab('overview');return false}}">Overview</a><span class="on" aria-current="page">SEO Dashboard</span><a href="./#ai" target="_top" onclick="if(window.parent!==window&&parent.showTab){{parent.showTab('ai');return false}}">AI Search Dashboard</a><a href="./#cro" target="_top" onclick="if(window.parent!==window&&parent.showTab){{parent.showTab('cro');return false}}">CRO + Website Dashboard</a></div></nav>
{''.join(body)}
<footer><div class="wrap"><img src="{logo_f}" alt="SpearPoint Marketing"><p>{e(method)}</p></div></footer>
<script type="application/json" id="dashData">{data_json}</script>
<script>{JS}</script>
</body>
</html>"""
os.makedirs('site', exist_ok=True)
open('site/index.html', 'w').write(page)
print('wrote site/index.html', len(page))
