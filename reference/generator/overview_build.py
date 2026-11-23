#!/usr/bin/env python3
"""Builds the client-facing Overview (title) page: overview/index.html."""
import json, re, os
cro_html = open('cro/index.html').read()
css = re.search(r'<style>(.*?)</style>', cro_html, re.S).group(1)
logo_h = open('logo1.txt').read().strip(); logo_f = open('logo2.txt').read().strip()
W = json.load(open('data/gsc_trend.json'))['windows']
l90, y90, l28, p28 = W['l90'], W['y90'], W['l28'], W['p28']
GEN_DATE = 'November 17, 2026'

def nav(on):
    items = [('overview', 'Overview'), ('seo', 'SEO Dashboard'), ('ai', 'AI Search Dashboard'), ('cro', 'CRO + Website Dashboard')]
    out = []
    for k, t in items:
        if k == on: out.append(f'<span class="on" aria-current="page">{t}</span>')
        else: out.append(f'<a href="./#{k}" target="_top" onclick="if(window.parent!==window&&parent.showTab){{parent.showTab(\'{k}\');return false}}">{t}</a>')
    return '<nav class="report-nav"><div class="wrap">' + ''.join(out) + '</div></nav>'

def go(k, label):
    return f'<a class="ov-btn" href="./#{k}" target="_top" onclick="if(window.parent!==window&&parent.showTab){{parent.showTab(\'{k}\');return false}}">{label} &rarr;</a>'

css += """
.ov-goal { background:#fff; border:1px solid var(--line); border-left:6px solid var(--green); border-radius:14px; padding:22px 28px; margin-bottom:22px; display:flex; gap:22px; align-items:flex-start; flex-wrap:wrap; }
.ov-goal .k { color:var(--green-dark); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:.1em; margin-bottom:6px; }
.ov-goal h3 { margin:0 0 8px; color:var(--blue); font-size:22px; line-height:1.3; }
.ov-goal p { margin:0; color:var(--slate); font-size:14px; line-height:1.6; max-width:900px; }
.ov-goal p b { color:var(--ink); }
.ov-hero { background:var(--blue); color:#fff; border-radius:14px; padding:30px 34px; display:flex; gap:28px; align-items:center; flex-wrap:wrap; }
.ov-hero h2 { color:#fff; margin:0 0 8px; font-size:24px; line-height:1.3; }
.ov-hero p { margin:0; color:rgba(255,255,255,.85); font-size:15px; line-height:1.6; max-width:760px; }
.ov-hero .k { color:var(--green); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:.1em; margin-bottom:8px; }
.ov-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-top:22px; }
@media (max-width:980px) { .ov-grid { grid-template-columns:1fr; } }
.ov-card { background:#fff; border:1px solid var(--line); border-radius:14px; padding:24px 24px 22px; display:flex; flex-direction:column; border-top:5px solid var(--green); }
.ov-card .tag { display:inline-block; align-self:flex-start; font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:.08em; color:var(--green-dark); background:rgba(77,184,89,.14); border-radius:100px; padding:4px 11px; }
.ov-card h3 { font-size:20px; color:var(--blue); margin:12px 0 4px; }
.ov-card .lead { font-size:14px; color:var(--slate); margin:0 0 16px; line-height:1.55; }
.ov-stats { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:16px; }
.ov-stat { background:var(--beige); border-radius:10px; padding:12px 14px; }
.ov-stat .n { font-size:26px; font-weight:800; color:var(--blue); line-height:1.1; }
.ov-stat .n small { font-size:13px; color:var(--slate); font-weight:700; }
.ov-stat .l { font-size:11.5px; color:var(--slate); margin-top:3px; line-height:1.35; }
.ov-wins { list-style:none; padding:0; margin:0 0 16px; }
.ov-wins li { position:relative; padding:0 0 9px 26px; font-size:13.5px; color:var(--ink); line-height:1.5; }
.ov-wins li::before { content:'✓'; position:absolute; left:0; top:0; width:18px; height:18px; border-radius:50%; background:var(--green); color:#fff; font-size:11px; font-weight:800; display:flex; align-items:center; justify-content:center; }
.ov-next { margin-top:auto; border-top:1px solid var(--line); padding-top:14px; font-size:13px; color:var(--slate); line-height:1.5; }
.ov-next b { color:var(--blue); }
.ov-btn { display:inline-block; margin-top:14px; background:var(--blue); color:#fff !important; text-decoration:none; font-weight:700; font-size:13px; padding:10px 16px; border-radius:100px; align-self:flex-start; }
.ov-btn:hover { background:var(--green-dark); }
.ov-steps { display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }
@media (max-width:980px) { .ov-steps { grid-template-columns:1fr; } }
.ov-step { background:#fff; border:1px solid var(--line); border-radius:12px; padding:20px 22px; }
.ov-step .d { display:inline-block; background:var(--blue); color:#fff; font-size:11px; font-weight:800; border-radius:100px; padding:4px 11px; letter-spacing:.04em; }
.ov-step h4 { margin:10px 0 6px; font-size:16px; color:var(--blue); }
.ov-step p { margin:0; font-size:13.5px; color:var(--slate); line-height:1.55; }
"""

pos_gain = round(y90[3] - l90[3])
click_up = round((l28[1] - p28[1]) / p28[1] * 100)

hero = f'''<div class="ov-hero"><div>
  <div class="k">The big picture</div>
  <h2>SpearPoint is gaining ground in Google and showing up in AI answers. Now the focus is turning that visibility into more B2B leads.</h2>
  <p>This report brings together three views of SpearPoint's online growth: how it ranks in Google (SEO), how often AI tools like ChatGPT and Google's AI Overviews mention it (AI Search), and how well the website turns visitors into conversations (CRO + Website).</p>
</div></div>'''

cards = f'''<div class="ov-grid">
 <div class="ov-card">
  <span class="tag">Trending up</span>
  <h3>SEO</h3>
  <p class="lead">SpearPoint is ranking higher in Google than it was a year ago, and search clicks are climbing.</p>
  <div class="ov-stats">
   <div class="ov-stat"><div class="n">+{click_up}%</div><div class="l">Google clicks, last 28 days vs. the 28 days before</div></div>
   <div class="ov-stat"><div class="n">{pos_gain} <small>spots</small></div><div class="l">Higher average Google position than last year</div></div>
  </div>
  <ul class="ov-wins">
   <li><b>#4 for “conversion based seo”</b>, SpearPoint's signature service</li>
   <li><b>#11 for “b2b seo agency”</b>, one step from page 1</li>
   <li>Domain Trust grew from <b>41 to 50</b> in 12 months</li>
  </ul>
  <div class="ov-next"><b>Next:</b> push the B2B and Denver service pages onto page 1 of Google.</div>
  {go('seo', 'View SEO dashboard')}
 </div>
 <div class="ov-card">
  <span class="tag">Competitive</span>
  <h3>AI Search</h3>
  <p class="lead">AI tools are already citing SpearPoint's content, and it holds its own against larger agencies.</p>
  <div class="ov-stats">
   <div class="ov-stat"><div class="n">64.5<small>/100</small></div><div class="l">AI Search Score, ahead of Breaking B2B and Thrive Digital</div></div>
   <div class="ov-stat"><div class="n">72</div><div class="l">Times AI answers linked to SpearPoint</div></div>
  </div>
  <ul class="ov-wins">
   <li>Cited in <b>11 of 16 topics</b>, tied for the most of any brand</li>
   <li><b>797 websites</b> appear alongside SpearPoint in AI answers</li>
   <li>Brand reputation score of <b>99/100</b></li>
  </ul>
  <div class="ov-next"><b>Next:</b> get SpearPoint named more often, not just linked, in AI answers about B2B SEO.</div>
  {go('ai', 'View AI Search dashboard')}
 </div>
 <div class="ov-card">
  <span class="tag">Ready to grow</span>
  <h3>CRO + Website</h3>
  <p class="lead">Search visitors are highly engaged. A few simple changes can turn more of them into leads.</p>
  <div class="ov-stats">
   <div class="ov-stat"><div class="n">60%</div><div class="l">Engagement rate from Google visitors, the site's best traffic</div></div>
   <div class="ov-stat"><div class="n">66</div><div class="l">People started a contact or audit form in 90 days</div></div>
  </div>
  <ul class="ov-wins">
   <li>Clear, results-focused messaging and <b>real client results</b></li>
   <li><b>Transparent pricing</b>, a strong trust signal for buyers</li>
   <li>The Denver SEO page scores <b>80/100</b> on CRO best practices</li>
  </ul>
  <div class="ov-next"><b>Next:</b> track every lead, shorten the audit form and add “book a call” options.</div>
  {go('cro', 'View CRO + Website dashboard')}
 </div>
</div>'''

steps = '''<div class="ov-steps">
 <div class="ov-step"><span class="d">DAYS 1&ndash;30</span><h4>Quick wins</h4><p>Track every form and booked call, shorten the free audit form, add “book a call” buttons, and sharpen the B2B and Denver pages for Google.</p></div>
 <div class="ov-step"><span class="d">DAYS 31&ndash;60</span><h4>Build visibility</h4><p>Publish content that answers B2B buyers' questions, get SpearPoint listed on “best agency” pages, and test a B2B-focused homepage.</p></div>
 <div class="ov-step"><span class="d">DAYS 61&ndash;90</span><h4>Prove the results</h4><p>Add B2B case studies, connect leads back to SEO and AI Search, and review progress in these dashboards every month.</p></div>
</div>'''

def section(cls, kicker, title, desc, body):
    return f'<section class="block {cls}"><div class="wrap"><div class="section-head"><div class="kicker">{kicker}</div><h2>{title}</h2>{f"<p>{desc}</p>" if desc else ""}</div>{body}</div></section>'

goal = ('<div class="ov-goal"><div><div class="k">Primary Goal</div>'
        '<h3>More leads from B2B companies searching for SEO and AI Search services.</h3>'
        '<p><b>Who we want to reach:</b> B2B business owners and marketers (about $1M to $10M in annual revenue) in consulting, manufacturing, service businesses and SaaS or tech, who need customers beyond referrals and paid ads. '
        'Every number in this report, and every task in the 90-day plan, is judged by whether it moves SpearPoint closer to this goal.</p></div></div>')

body = (section('alt', 'Summary', 'Where SpearPoint Stands Today', '', goal + hero + cards)
        + section('', 'What Happens Next', 'The 90-Day Plan at a Glance', 'The detailed roadmap is in each dashboard. Here is the short version.', steps))

page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="robots" content="noindex">
<title>Overview &mdash; SpearPoint Marketing B2B Performance Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="report-header"><div class="header-inner"><img src="{logo_h}" alt="SpearPoint Marketing"><div class="header-meta">Generated {GEN_DATE}<br>Site: thespearpoint.com</div></div>
<div class="eyebrow-row"><div class="eyebrow">B2B Performance Report</div><h1 class="report-title">SpearPoint Marketing B2B Performance Report</h1>
<p class="report-sub">A simple summary of SEO, AI Search and website performance, with the plan for the next 90 days. Use the tabs or the buttons below to see each full dashboard.</p></div></header>
{nav('overview')}
{body}
<footer><div class="wrap"><img src="{logo_f}" alt="SpearPoint Marketing"><p>Sources: Google Search Console, SE Ranking, GA4 and a live review of thespearpoint.com. SEO and website figures cover the last 90 days (Aug 13 &ndash; Nov 10, 2026) unless noted; AI Search figures are from SE Ranking's AI Search tracking (October 2026). Prepared by SpearPoint Marketing.</p></div></footer>
</body></html>"""
os.makedirs('overview', exist_ok=True)
open('overview/index.html', 'w').write(page)
print('wrote overview/index.html', len(page), click_up, pos_gain)
