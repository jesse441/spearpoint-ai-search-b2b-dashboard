#!/usr/bin/env python3
"""Builds the 90-Day Plan tab (plan/index.html) from data/plan90.json (mirrors the
'SpearPoint 90 Day Plan Recommendations' tab in the Marketing SEO spreadsheet)."""
import json, re, os, html
e = html.escape
cro_html = open('cro/index.html').read()
css = re.search(r'<style>(.*?)</style>', cro_html, re.S).group(1)
logo_h = open('logo1.txt').read().strip(); logo_f = open('logo2.txt').read().strip()
D = json.load(open('data/plan90.json'))
GEN_DATE = 'November 20, 2026'
SHEET = 'https://docs.google.com/spreadsheets/d/1huXlSvLQXf5us0bMf_4HSW3bVIiLrMbGA5-5_tOTros/edit'
TABS = [('overview', 'Overview'), ('seo', 'SEO Dashboard'), ('ai', 'AI Search Dashboard'), ('cro', 'CRO + Website Dashboard'), ('plan', '90-Day Plan')]

def nav(on):
    out = []
    for k, t in TABS:
        if k == on: out.append(f'<span class="on" aria-current="page">{t}</span>')
        else: out.append(f'<a href="./#{k}" target="_top" onclick="if(window.parent!==window&&parent.showTab){{parent.showTab(\'{k}\');return false}}">{t}</a>')
    return '<nav class="report-nav"><div class="wrap">' + ''.join(out) + '</div></nav>'

css += """
.draft-banner { display:flex; gap:14px; align-items:center; background:#fff; border:1px solid var(--line); border-left:5px solid var(--green); border-radius:10px; padding:14px 18px; margin-bottom:18px; font-size:13.5px; color:var(--slate); }
.draft-banner b { color:var(--blue); }
.draft-banner .pill { background:rgba(77,184,89,.15); color:var(--green-dark); font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:.08em; padding:4px 10px; border-radius:100px; white-space:nowrap; }
.imp-meta { margin-top:10px; display:flex; flex-wrap:wrap; gap:6px 16px; font-size:12px; color:var(--muted3); }
.imp-meta b { color:var(--slate); font-weight:700; }
.flag-bucket { background:rgba(29,56,83,.09); color:var(--blue); }
.decision { display:inline-block; margin-left:8px; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:.05em; padding:3px 9px; border-radius:100px; background:rgba(201,138,26,.14); color:#9A6A12; }
.tbl-head { display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:12px; }
.tbl-head .count { font-size:12.5px; color:var(--slate); }
table.plan { width:100%; border-collapse:collapse; font-size:13px; }
table.plan td { padding:11px 13px; border-bottom:1px solid var(--line); vertical-align:top; }
table.plan td.id { font-weight:800; color:var(--red); white-space:nowrap; }
table.plan td.title { font-weight:700; color:var(--ink); min-width:220px; }
table.plan td.small { font-size:12px; color:var(--slate); }
table.plan th { cursor:default; }
.tech-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
@media (max-width:900px) { .tech-grid { grid-template-columns:1fr; } }
.tech-card { background:#fff; border:1px solid var(--line); border-radius:10px; padding:18px 20px; }
.tech-card .m { font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:.08em; color:var(--red); }
.tech-card h4 { margin:6px 0 8px; font-size:15px; color:var(--blue); }
.tech-card p { margin:0; font-size:13px; color:var(--slate); line-height:1.55; }
.tech-card .hrs { display:inline-block; margin-top:10px; font-size:11px; font-weight:800; background:var(--beige); border-radius:100px; padding:3px 10px; color:var(--blue); }
"""

def section(cls, kicker, title, desc, body, id_=''):
    return f'''<section class="block {cls}"{f' id="{id_}"' if id_ else ''}><div class="wrap"><div class="section-head"><div class="kicker">{kicker}</div><h2>{title}</h2>{f'<p>{desc}</p>' if desc else ''}</div>{body}</div></section>'''

MONTHS = ['Dec 2026', 'Jan 2027', 'Feb 2027']
def chips(tid, opts):
    return f'<div class="filter-chips" data-for="{tid}">' + ''.join(f'<button class="filter-btn{" active" if i == 0 else ""}" data-f="{e(o)}">{e(o)}</button>' for i, o in enumerate(opts)) + '</div>'
def table(tid, heads, rows, keys, filt_opts):
    body = ''.join(f'<tr data-k="{e(k)}">' + ''.join(r) + '</tr>' for r, k in zip(rows, keys))
    return (f'<div class="tbl-head">{chips(tid, filt_opts)}<span class="count" id="{tid}-count"></span></div>'
            f'<div class="table-wrap"><table class="plan" id="{tid}"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in heads) + f'</tr></thead><tbody>{body}</tbody></table></div>')
td = lambda v, c='': f'<td class="{c}">{e(v)}</td>'

P, R, T, B, G, A = (D[k] for k in 'PRTBGA')
n_dec = sum(1 for p in P if p[2] == 'Dec 2026')

# ---- Snapshot
kpis = f'''<div class="draft-banner"><span class="pill">Draft</span><div><b>Recommendations for Erika's review.</b> Erika makes the final call on each task in the <a href="{SHEET}" target="_blank" rel="noopener">SpearPoint 90 Day Plan Recommendations</a> tab of the marketing spreadsheet. Approved tasks will be marked here once she's decided.</div></div>
<div class="kpi-grid five">
  <div class="kpi-card"><div class="kpi-label">Priority tasks</div><div class="kpi-value tab">{len(P)}</div><div class="kpi-sub">{n_dec} start in December</div></div>
  <div class="kpi-card"><div class="kpi-label">Page refinements</div><div class="kpi-value tab">{len(R)}</div><div class="kpi-sub">6 pages a month: SEO, AI Search and CRO</div></div>
  <div class="kpi-card"><div class="kpi-label">Blog posts</div><div class="kpi-value tab">{len(B)}</div><div class="kpi-sub">4 a month, mostly B2B and AI Search</div></div>
  <div class="kpi-card"><div class="kpi-label">Guest posts</div><div class="kpi-value tab">{len(G)}</div><div class="kpi-sub">6 a month for link building</div></div>
  <div class="kpi-card"><div class="kpi-label">Technical SEO</div><div class="kpi-value tab">1<span style="font-size:16px;color:var(--slate);"> hr/mo</span></div><div class="kpi-sub">Tracking, headings, schema, speed</div></div>
</div>
<div class="takeaways">
  <div class="take"><div class="t-k">December</div><h4>Fix and measure.</h4><p>Get every lead tracked in GA4, then remove friction where visitors already convert: the audit form, contact page, booking page and blog CTAs. Push /b2b-seo onto page 1.</p></div>
  <div class="take"><div class="t-k">January</div><h4>Sharpen and position.</h4><p>Focus the Denver, SaaS and AEO pages, retarget existing posts at the client's priority AI prompts, and test a B2B-first homepage.</p></div>
  <div class="take"><div class="t-k">February</div><h4>Build and prove.</h4><p>Publish B2B case studies, strengthen the industry pages, add schema and speed fixes, and keep 6 guest posts a month building authority.</p></div>
</div>'''

# ---- Priority tasks by phase
phases = [('Dec 2026', 'December', 'Do First: Fix and Measure', 'Tracking and conversion fixes on the pages that already get traffic.'),
          ('Jan 2027', 'January', 'Next: Sharpen and Position', 'Page-1 pushes and AI Search positioning on the core service pages.'),
          ('Feb 2027', 'February', 'Build: Prove and Grow Authority', 'Case studies, industry pages and technical work that compound over time.'),
          ('Ongoing', 'Ongoing', 'Every Month', 'Work that runs through all 90 days.')]
road = []
for key, badge, title, sub in phases:
    cards = []
    for p in [p for p in P if p[2] == key]:
        pid, pri, mon, bucket, task, why, page, src, eff, owner = p
        cards.append(f'<div class="imp-card"><div class="imp-num">{pid}</div><div class="imp-body"><span class="imp-flag flag-bucket">{e(bucket)}</span><span class="decision">Pending Erika</span><h4>{e(task)}</h4><p>{e(why)}</p>'
                     f'<div class="imp-meta"><span><b>Page:</b> {e(page)}</span><span><b>From:</b> {e(src)}</span><span><b>Effort:</b> {e(eff)}</span><span><b>Owner:</b> {e(owner)}</span></div></div></div>')
    road.append(f'<div class="phase"><div class="phase-head"><span class="phase-badge">{badge}</span><h3>{title}</h3></div><p class="phase-sub">{sub}</p><div class="imp-grid">{"".join(cards)}</div></div>')
road_html = '<div class="roadmap">' + ''.join(road) + '</div>'

# ---- Tables
r_tbl = table('tR', ['ID', 'Month', 'Page', 'SEO change', 'AI Search change', 'CRO change', 'Target keyword / prompt'],
              [[td(r[0], 'id'), td(r[1], 'small'), td(r[2], 'title'), td(r[3]), td(r[4] or '—'), td(r[5]), td(r[6], 'small')] for r in R],
              [r[1] for r in R], ['All'] + MONTHS)
tech = '<div class="tech-grid">' + ''.join(f'<div class="tech-card"><div class="m">{e(t[1])}</div><h4>{e(t[2])}</h4><p>{e(t[3])}</p><span class="hrs">1 hr</span></div>' for t in T) + '</div>'
b_tbl = table('tB', ['ID', 'Month', 'Working title', 'Lane', 'Primary keyword (US/mo)', 'AI Search prompt', 'Pillar page', 'Author'],
              [[td(b[0], 'id'), td(b[1], 'small'), td(b[7], 'title'), td(b[2]), td(b[5], 'small'), td(b[6], 'small'), td(b[4], 'small'), td(b[3], 'small')] for b in B],
              [b[1] for b in B], ['All'] + MONTHS)
g_tbl = table('tG', ['ID', 'Month', 'Working title', 'Publication type (prospect)', 'Links to', 'Anchor text'],
              [[td(g[0], 'id'), td(g[1], 'small'), td(g[5], 'title'), td(g[4]), td(g[2], 'small'), td(g[3], 'small')] for g in G],
              [g[1] for g in G], ['All'] + MONTHS)
buckets = ['All', 'Page Refinement', 'Blogging', 'Link Building', 'AEO and AI Search', 'Website CRO']
a_tbl = table('tA', ['ID', 'Area', 'Alternative', 'Why consider it', 'Page / URL', 'Effort', 'Could replace'],
              [[td(a[0], 'id'), td(a[1], 'small'), td(a[2], 'title'), td(a[3]), td(a[4], 'small'), td(a[5], 'small'), td(a[6], 'small')] for a in A],
              [a[1] for a in A], buckets)

js = """<script>
document.querySelectorAll('.filter-chips').forEach(function(box){
  var t=document.getElementById(box.dataset.for), cnt=document.getElementById(box.dataset.for+'-count');
  function apply(f){var n=0;t.querySelectorAll('tbody tr').forEach(function(tr){var on=(f==='All'||tr.dataset.k===f);tr.style.display=on?'':'none';if(on)n++;});cnt.textContent='Showing '+n+' of '+t.querySelectorAll('tbody tr').length;}
  box.querySelectorAll('button').forEach(function(b){b.onclick=function(){box.querySelectorAll('button').forEach(function(x){x.classList.remove('active')});b.classList.add('active');apply(b.dataset.f);};});
  apply('All');
});
</script>"""

body = [
 section('alt', 'Snapshot', '90-Day Plan at a Glance', 'Dec 1, 2026 to Feb 28, 2027. The SEO, AI Search and CRO + Website roadmaps merged into one prioritized plan that fits the monthly tasks in SpearPoint\'s plan.', kpis),
 section('', 'Priority Tasks', 'What to Do First, Next and Last', f'{len(P)} tasks ranked by impact on B2B leads. Each one shows the evidence behind it and which dashboard recommendation it comes from.', road_html),
 section('alt', 'Page Refinement', 'Page Refinement: 6 Pages a Month', 'Each page gets its SEO, AI Search and CRO changes in one pass.', r_tbl),
 section('', 'Technical SEO', 'Monthly Technical SEO Optimization (1 hr/month)', '', tech),
 section('alt', 'Blogging', 'Blog Content Calendar: 4 Posts a Month', 'New topics only. Each post targets a keyword or an AI Search prompt and links to a pillar page. November\'s posts are already on the Blog Calendar tab.', b_tbl),
 section('', 'Link Building', 'Guest Post Calendar: 6 a Month', 'Each month\'s guest posts link to the pages being refined that month. Publication types are listed; the prospect list is built when the month starts.', g_tbl),
 section('roadmap-beige', 'Options for Erika', 'Alternatives: Swap Any of These In', 'Twenty more options for Erika to swap in for any task above. The "Could replace" column shows where each one fits.', a_tbl),
]
method = ('Sources: SEO, AI Search and CRO + Website dashboards in this report; the Plan, Blog Calendar and Guest Post tabs of the SpearPoint marketing spreadsheet; '
          'a live check of thespearpoint.com on Nov 20, 2026. Prepared by SpearPoint Marketing as a draft for review.')
page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="robots" content="noindex">
<title>90-Day Plan &mdash; SpearPoint Marketing</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="report-header"><div class="header-inner"><img src="{logo_h}" alt="SpearPoint Marketing"><div class="header-meta">Generated {GEN_DATE}<br>Site: thespearpoint.com</div></div>
<div class="eyebrow-row"><div class="eyebrow">90-Day Plan &middot; Draft for Review</div><h1 class="report-title">SpearPoint Marketing 90-Day Plan - B2B</h1>
<p class="report-sub">One prioritized plan for December through February, built from the SEO, AI Search and CRO + Website dashboards: priority tasks, 6 page refinements, 4 blog posts and 6 guest posts a month, plus alternatives to choose from.</p></div></header>
{nav('plan')}
{''.join(body)}
<footer><div class="wrap"><img src="{logo_f}" alt="SpearPoint Marketing"><p>{e(method)}</p></div></footer>
{js}
</body></html>"""
os.makedirs('plan', exist_ok=True)
open('plan/index.html', 'w').write(page)
print('wrote plan/index.html', len(page))
