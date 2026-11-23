#!/usr/bin/env python3
"""Builds the SpearPoint CRO + Website Dashboard (cro/index.html)."""
import json, html, os, re
e = html.escape
seo_html = open('site/index.html').read()
css = re.search(r'<style>(.*?)</style>', seo_html, re.S).group(1)
logo_h = open('logo1.txt').read().strip(); logo_f = open('logo2.txt').read().strip()
GA = json.load(open('data/ga4.json')) if os.path.exists('data/ga4.json') else None
LG = json.load(open('data/gsc90_landing_groups.json'))
GEN_DATE = 'November 16, 2026'

css += """
.report-nav a:hover { border-color:var(--blue); background:var(--beige); }
.flow { display:grid; grid-template-columns:repeat(5,1fr); gap:0; align-items:stretch; margin-top:8px; }
@media (max-width:980px) { .flow { grid-template-columns:1fr; } }
.flow-step { background:#fff; border:1px solid var(--line); border-radius:10px; padding:16px; position:relative; margin-right:22px; }
.flow-step:last-child { margin-right:0; }
.flow-step:not(:last-child)::after { content:'→'; position:absolute; right:-19px; top:42%; font-size:20px; color:var(--muted1); font-weight:800; }
@media (max-width:980px) { .flow-step { margin:0 0 22px; } .flow-step:not(:last-child)::after { content:'↓'; right:auto; left:50%; top:auto; bottom:-24px; } }
.flow-step .k { font-size:10.5px; text-transform:uppercase; letter-spacing:.08em; font-weight:800; color:var(--red); }
.flow-step h4 { font-size:15px; margin:4px 0 6px; color:var(--blue); }
.flow-step .big { font-size:26px; font-weight:800; color:var(--blue); line-height:1.1; }
.flow-step p { font-size:12.5px; color:var(--slate); margin:6px 0 0; }
.stuck { margin-top:10px; font-size:12px; color:var(--red-dark); background:rgba(241,115,92,.10); border-radius:6px; padding:8px 10px; }
.stuck b { color:var(--red-dark); }
.sev { display:inline-block; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:.06em; border-radius:100px; padding:2px 9px; }
.sev-high { background:rgba(241,115,92,.18); color:var(--red-dark); }
.sev-med { background:rgba(201,138,26,.16); color:#9A6A12; }
.sev-low { background:rgba(147,160,168,.2); color:var(--muted3); }
.score-cell { font-weight:800; text-align:center; border-radius:6px; }
.s1 { background:rgba(241,115,92,.28); } .s2 { background:rgba(241,115,92,.14); } .s3 { background:rgba(201,138,26,.14); } .s4 { background:rgba(77,184,89,.16); } .s5 { background:rgba(77,184,89,.32); }
.pending { border:2px dashed var(--line); border-radius:10px; padding:22px; text-align:center; color:var(--slate); background:#fff; }
.sub-h { font-size:16px; color:var(--blue); margin:0 0 12px; }
.pending b { color:var(--ink); display:block; font-size:15px; margin-bottom:4px; }
.cro-total { display:flex; gap:24px; align-items:center; flex-wrap:wrap; background:#fff; border:1px solid var(--line); border-radius:10px; padding:18px 22px; margin-bottom:16px; }
.cro-total .n { font-size:46px; font-weight:800; color:var(--blue); line-height:1; }
.cro-total .n span { font-size:16px; color:var(--slate); }
.cro-total p { margin:0; font-size:13.5px; color:var(--slate); max-width:760px; }
tr.sc-main td { border-bottom:none; padding-bottom:4px; }
tr.sc-note td { font-size:12.5px; color:var(--slate); padding-top:0; }
.score-cell { border-radius:0 !important; width:84px; }
td.note-c { font-size:12px; color:var(--slate); min-width:220px; }
"""

def section(cls, kicker, title, desc, body, id_=''):
    return f'''<section class="block {cls}"{f' id="{id_}"' if id_ else ''}><div class="wrap"><div class="section-head"><div class="kicker">{kicker}</div><h2>{title}</h2>{f'<p>{desc}</p>' if desc else ''}</div>{body}</div></section>'''

# ---------------- CRO scorecard (manual audit, Nov 16 2026) ----------------
CRIT = ['ICP clarity', 'Messaging', 'Proof', 'Answers buyer questions', 'Clear CTA & next step', 'Low-friction conversion']
CRIT_S = ['ICP', 'Messaging', 'Proof', 'Buyer Qs', 'CTA', 'Friction']
PAGES = [
 ('Homepage', '/', 77, [2,4,4,3,4,3], 'Speaks to B2B, fitness and ecommerce in one hero, so B2B buyers have to self-select. Strong outcome message and results (5X trials, 2X trials).'),
 ('B2B SEO', '/b2b-seo', 8, [4,3,3,4,4,3], 'Clear B2B audience and a testimonial in the hero. The H1 (“Conversion Based B2B SEO”) is vague, and there is no linked B2B case study with numbers.'),
 ('Denver SEO', '/seo', 12, [4,4,4,5,4,3], 'Best page on the site: a local promise, an objection-led H2 (“Burned by an SEO agency before?”), proof, FAQ and FAQ schema. It has 3 H1 tags.'),
 ('AEO / AI Search', '/aeo-ai-search-services', 1, [3,4,4,4,4,3], 'H1 now fixed. Good proof (the ZenOne 5X case) and an FAQ. Who it is for (B2B, SaaS, local?) is not stated above the fold.'),
 ('Conversion-Based SEO', '/conversion-based-seo', 0, [3,4,4,2,4,3], 'Strong promise (“Built to Increase Leads and Sales”), but no FAQ to handle questions about SEO + CRO scope, timing or price.'),
 ('Pricing', '/pricing', 0, [3,4,3,2,4,3], 'Transparent $750&ndash;$2,000+/mo tiers, a strong trust signal. No FAQ on contracts, onboarding or results timeline. The CTA sends visitors back to the audit form.'),
 ('Free SEO Audit (form)', '/free-seo-audit', 0, [2,3,1,2,3,2], 'The main conversion page has no proof beside the form, 6 fields including a required budget and a long required textarea, and the consultation must be booked separately after submitting.'),
 ('Contact', '/contact', 2, [2,1,1,1,3,2], 'Opens with a spam warning (“we will report it as spam”) before the form. Phone is required. No proof and no booking option.'),
 ('Free Quote (GBP “Book”)', '/free-quote', 0, [3,3,3,1,4,3], 'Google Business Profile\'s booking button lands here. Clean form with Clutch badges, but the badges are from 2023 and “plans starting at $600/month” conflicts with the $750 Starter plan on /pricing.'),
 ('Top blog posts', '/blog/…', 107, [2,2,3,4,1,3], 'The traffic leaders (Shopify guide, gym keywords, B2B CTAs) answer questions well but have no audit CTA inside the article, only generic “Learn more” buttons.'),
]
def avg(s): return sum(s) / len(s)
rows = ''
for name, url, clicks, s, note in PAGES:
    sc = round(avg(s) * 20)
    rows += f'<tr class="sc-main"><td><b>{e(name)}</b> <span class="src-t">{e(url)}</span></td>' + ''.join(f'<td class="score-cell s{v}">{v}</td>' for v in s) + f'<td class="cell-num"><b style="font-size:16px">{sc}</b></td><td class="cell-num">{clicks}</td></tr><tr class="sc-note"><td colspan="9">{note}</td></tr>'
weights = [max(c, 3) for _, _, c, _, _ in PAGES]
site_score = round(sum(avg(s) * 20 * w for (_, _, _, s, _), w in zip(PAGES, weights)) / sum(weights))
crit_avg = [round(sum(p[3][i] for p in PAGES) / len(PAGES) * 20) for i in range(6)]
score_html = f'''<div class="cro-total"><div class="n">{site_score}<span>/100</span></div><p><b>Website CRO Score.</b> Ten key pages scored 1&ndash;5 on six CRO best practices, weighted by how much organic traffic each page receives. Strongest: <b>Messaging ({crit_avg[1]})</b> and <b>Clear CTA ({crit_avg[4]})</b>. Weakest: <b>ICP clarity ({crit_avg[0]})</b>, <b>Answers buyer questions ({crit_avg[3]})</b> and <b>Proof at the point of conversion</b>.</p></div>
<div class="table-wrap"><table><thead><tr><th>Page</th>{''.join(f'<th style="text-align:center">{c}</th>' for c in CRIT_S)}<th class="cell-num">Score</th><th class="cell-num">Clicks (90d)</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="method-box"><b>How pages are scored:</b> 1 = missing or works against conversion, 3 = present but generic, 5 = best practice. <b>ICP</b>: is it obvious who the page is for? <b>Messaging</b>: is the outcome specific and differentiated? <b>Proof</b>: are results, testimonials or logos near the decision point? <b>Buyer Qs</b>: does it answer price, process, timeline and fit (FAQ). <b>CTA</b>: one obvious next step. <b>Friction</b> (higher = less friction): short forms, instant booking, no extra steps. Page score = average &times; 20. Reviewed on the live site, Nov 16, 2026.</div>'''

# ---------------- Conversion path ----------------
tot = sum(v[0] for v in LG.values())
pct = lambda k: round(LG.get(k, [0])[0] / tot * 100)
flow_html = f'''<div class="flow">
 <div class="flow-step"><div class="k">1 · Search</div><h4>Google organic</h4><div class="big">{tot}</div><p>Organic clicks in the last 90 days (Search Console). About a third come from people searching “SpearPoint” by name.</p></div>
 <div class="flow-step"><div class="k">2 · Landing page</div><h4>Where they land</h4><p><b>Blog posts {pct("Blog posts")}%</b> · Homepage {pct("Homepage")}% · Service pages {pct("Service pages")}% · Pricing, audit, contact &amp; case studies {pct("Conversion & proof pages")}%</p>
  <div class="stuck"><b>Stuck point:</b> most visitors enter on blog posts, mainly ecommerce and fitness topics, not on B2B service pages.</div></div>
 <div class="flow-step"><div class="k">3 · Next click</div><h4>Find the offer</h4><p>Blog → “Learn more” → service page → “Get My Free Audit”. That is 3+ clicks before the form.</p>
  <div class="stuck"><b>Stuck point:</b> the top blog posts have no audit or booking CTA inside the article.</div></div>
 <div class="flow-step"><div class="k">4 · Conversion</div><h4>Free audit form</h4><p>6 fields: name, email, website, <b>required budget</b> and a <b>required long text box</b> (keywords, competitors, monthly leads).</p>
  <div class="stuck"><b>Stuck point:</b> high effort for a cold B2B visitor, with no proof or “what happens next” beside the form.</div></div>
 <div class="flow-step"><div class="k">5 · Sales call</div><h4>Book the consult</h4><p>“30 min SEO Consultation &ndash; Please Schedule After Submitting.” The booking link (HubSpot) only lives on /demo, linked from the footer.</p>
  <div class="stuck"><b>Stuck point:</b> a second step after the form, with no phone number or chat on the site.</div></div>
</div>'''

STUCK = [
 ('high','Leads are not being measured', 'GA4 recorded 0 key events and only 2 form_submit events in 90 days, against 104 form starts by 66 users. The generate_lead and Schedule key events are set up but have never received data, so conversion rate by page or channel is unknown.', 'GA4'),
 ('high','Search traffic lands on content, not offers', f'Blog posts take {pct("Blog posts")}% of organic clicks and B2B service pages only {pct("Service pages")}%. /b2b-seo had 8 clicks in 90 days. Pricing, audit, contact and case-study pages together had {LG.get("Conversion & proof pages",[0])[0]}.', 'Search Console, last 90 days'),
 ('high','Top blog posts have no conversion path', 'The Shopify guide (27 clicks) and gym keywords (15) posts have no in-article audit CTA, only “Learn more” buttons. GA4 shows the Shopify guide averaging 3s of engagement and the GEO guide 1s.', 'Page review'),
 ('high','The audit form asks too much, too early', 'Required: budget, website, and a long “About Your Business” box (top keywords, competitors, average monthly leads). The consultation must be scheduled separately after submitting.', '/free-seo-audit'),
 ('high','No instant way to talk to someone', 'No phone number on key pages, no chat, and the HubSpot meeting link appears only on /demo (footer link).', 'Site-wide'),
 ('med','No proof at the decision point', 'The audit page (about 250 words) has no testimonial, results or client logos near the form. The case studies exist (ZenOne 5X free trials) but aren\'t used there.', '/free-seo-audit'),
 ('med','The homepage serves three audiences at once', 'The hero targets “B2B, fitness, and ecommerce businesses.” B2B buyers, the campaign goal, have to self-select before they see relevant proof.', 'Homepage'),
 ('med','The contact page warns visitors before it welcomes them', 'The first lines are a spam warning (“we will report it as spam”). Phone is a required field.', '/contact'),
 ('med','The Google Business Profile booking page is out of date', 'GBP\'s “Book” button sends people to /free-quote (hundreds of Reserve-with-Google URLs in Search Console). The page shows Clutch 2023 badges and “starting at $600/month”, which conflicts with the $750 Starter plan on /pricing. GA4: 82 users, 0s average engagement and no form starts.', '/free-quote + GA4'),
 ('low','Heavy third-party scripts', '/b2b-seo loads 161 requests from 23 third-party hosts (HubSpot, Hotjar, Facebook, AdLytic, SearchAtlas and others), which slows mobile visitors.', 'Browser check'),
 ('low','Key buyer questions are unanswered on money pages', 'There is no FAQ on /pricing, /conversion-based-seo or /conversion-rate-optimization covering contracts, timeline to results, onboarding and who does the work.', 'Page review'),
]
stuck_rows = ''.join(f'<tr><td><span class="sev sev-{s}">{ {"high":"High","med":"Medium","low":"Low"}[s] }</span></td><td><b>{e(t)}</b></td><td class="note-c">{d}</td><td class="src-t">{e(src)}</td></tr>' for s, t, d, src in STUCK)
stuck_html = f'<div class="table-wrap"><table><thead><tr><th>Impact</th><th>Where visitors get stuck</th><th>Evidence</th><th>Source</th></tr></thead><tbody>{stuck_rows}</tbody></table></div>'

# ---------------- GA4 (traffic, engagement, conversions) ----------------
def ga_pending(what):
    return f'<div class="pending"><b>Waiting for GA4 access</b>{what} will fill in from SpearPoint\'s GA4 property (stream G-DWZ02L21VS) once it is reachable in Chrome.</div>'
R4 = json.load(open('data/ga4_raw.json'))
T = R4['totals']
fs, fu = R4['events']['form_start']; sb_, su = R4['events']['form_submit']
kpis = f"""<div class="kpi-grid five">
  <div class="kpi-card"><div class="kpi-label">Sessions · 90 days</div><div class="kpi-value tab">{T["sessions"]:,}</div><div class="kpi-sub">{T["users"]:,} users · Organic Search 577</div></div>
  <div class="kpi-card"><div class="kpi-label">Engagement rate</div><div class="kpi-value tab">{T["eng_rate"]:.1f}%</div><div class="kpi-sub">Organic Search: 60.5% · Direct: 27.1%</div></div>
  <div class="kpi-card"><div class="kpi-label">Form starts</div><div class="kpi-value tab">{fs}</div><div class="kpi-sub">{fu} users ({fu/T["users"]*100:.1f}% of users) started a form</div></div>
  <div class="kpi-card"><div class="kpi-label">Key events (conversions)</div><div class="kpi-value tab" style="color:var(--red)">0</div><div class="kpi-sub">Leads aren't being recorded in GA4: only {sb_} form_submit events in 90 days</div></div>
  <div class="kpi-card"><div class="kpi-label">Website CRO Score</div><div class="kpi-value tab">{site_score}<span style="font-size:16px;color:var(--slate);">/100</span></div><div class="kpi-sub">From the page-by-page audit below</div></div>
</div>"""
ch_rows = ''.join(f'<tr><td><b>{e(c)}</b></td><td class="cell-num">{s_:,}</td><td class="cell-num">{round(s_/T["sessions"]*100,1)}%</td><td class="cell-num">{en:,}</td><td class="cell-num">{er}%</td><td class="cell-num">{t}</td><td class="cell-num">0</td></tr>' for c,s_,en,er,t in R4['channels'])
pg_rows = ''.join(f'<tr><td>{e(p)}</td><td class="cell-num">{v:,}</td><td class="cell-num">{u:,}</td><td class="cell-num">{t}</td><td class="cell-num"><b>{f}</b></td></tr>' for p,v,u,t,f in R4['pages'] if v)
funnel = f"""<div class="flow" style="grid-template-columns:repeat(4,1fr)">
 <div class="flow-step"><div class="k">Users</div><h4>Visited the site</h4><div class="big">{T["users"]:,}</div><p>{T["sessions"]:,} sessions, 35% of them engaged.</p></div>
 <div class="flow-step"><div class="k">Intent</div><h4>Viewed audit, contact or pricing</h4><div class="big">263</div><p>Users on /free-seo-audit (108), /contact (124) and /pricing (31). Some may have visited more than one.</p></div>
 <div class="flow-step"><div class="k">Started</div><h4>Started a form</h4><div class="big">{fu}</div><p>{fs} form starts. Most were on /contact (41) and /free-seo-audit (21). About half came from India, Pakistan and Morocco, so some are probably spam.</p></div>
 <div class="flow-step"><div class="k">Recorded lead</div><h4>Key event in GA4</h4><div class="big" style="color:var(--red)">0</div><p>Only {sb_} form_submit events. The generate_lead and Schedule key events exist but have received no data.</p><div class="stuck"><b>Tracking gap:</b> real leads (from HubSpot or email) aren't reaching GA4, so conversion rate can't be measured yet.</div></div>
</div>"""
traffic_html = f"""<h3 class="sub-h">Lead funnel (GA4, {R4["range"]})</h3>{funnel}
<h3 class="sub-h" style="margin-top:28px">Sessions &amp; engagement by channel</h3>
<div class="table-wrap"><table><thead><tr><th>Channel</th><th class="cell-num">Sessions</th><th class="cell-num">Share</th><th class="cell-num">Engaged sessions</th><th class="cell-num">Engagement rate</th><th class="cell-num">Avg. engagement / session</th><th class="cell-num">Key events</th></tr></thead><tbody>{ch_rows}</tbody></table></div>
<div class="note-box"><b>What this means:</b> Direct makes up 75% of sessions but only 27% of them are engaged. Combined with high-view, low-engagement pages like /scholarship (637 views, 5s), this points to bot or spam traffic diluting the averages. <b>Organic Search is the quality channel:</b> 60.5% engagement and 40s per session, which is why getting those visitors to a lead is the priority.</div>
<h3 class="sub-h" style="margin-top:28px">Top pages: engagement &amp; form starts</h3>
<div class="table-wrap"><table><thead><tr><th>Page</th><th class="cell-num">Views</th><th class="cell-num">Active users</th><th class="cell-num">Avg. engagement / user</th><th class="cell-num">Form starts</th></tr></thead><tbody>{pg_rows}</tbody></table></div>
<div class="note-box"><b>Read-outs:</b> the Shopify guide (111 views, <b>3s</b>) and the GEO guide (91 views, <b>1s</b>) lose visitors almost immediately. /free-quote (the Google Business Profile booking page) has 82 users, <b>0s</b> engagement and no form starts. /case-study (1m 03s), /ai-search-dashboard (2m 15s) and /b2b-seo/saas (1m 06s) hold attention best, so they should link straight to booking.</div>"""
takeaways = f'''<div class="takeaways">
  <div class="take"><div class="t-k">What's working</div><h4>The message and pricing build trust.</h4><p>Outcome-led headlines (“More business, not just better reports”), real results (5X free trials, 2X trials) and transparent $750&ndash;$2,000+/mo pricing are above average for SEO agencies.</p></div>
  <div class="take warn"><div class="t-k">Where visitors get stuck</div><h4>The path from search to a conversation is long.</h4><p>66 users started a form in 90 days, but GA4 recorded 0 leads. Organic visitors mostly land on blog posts with no direct CTA. The free audit needs a 6-field form plus a separate scheduling step, with no proof beside it.</p></div>
  <div class="take"><div class="t-k">Biggest lever</div><h4>Track leads, then shorten the path.</h4><p>Fix GA4 lead tracking first so every change can be measured. Then add in-article CTAs, a 3-field audit form with booking built in, and proof next to every form.</p></div>
</div>'''

# ---------------- Recommendations ----------------
R = [
 ('Days 1&ndash;30', 'Quick Wins &mdash; Remove Friction', 'Fix lead tracking first, then the forms and CTAs. All of it can ship this month without new pages.', [
  ('Fix GA4 lead tracking (do this first)', 'Fire generate_lead on the thank-you or confirmation step of the audit, quote and contact forms (Squarespace form blocks don’t send a reliable form_submit). Fire Schedule when a HubSpot meeting is booked, using HubSpot’s meeting-booked message event. Add phone and email click events, then confirm in GA4 DebugView. Without this, conversion rate can’t be measured.', 'Measurement'),
  ('Cut the audit form to 3 fields and book the call on the thank-you page', 'Keep name, work email and website. Move budget and “about your business” to an optional second step, or ask them on the call. Embed the HubSpot meeting calendar on the thank-you page so the consult is booked in the same session instead of “please schedule after submitting.”', 'Form completion'),
  ('Add proof beside every form', 'Put the ZenOne “5X free trials” result, one B2B testimonial (e.g. Zen Supplies: “we now have leads coming from SEO”) and client logos next to the /free-seo-audit, /free-quote and /contact forms. Add a 3-step “what happens next” with turnaround time.', 'Trust at decision'),
  ('Put a contextual CTA inside the top blog posts', 'Add an in-article CTA box after the intro and at the end of the 10 most-visited posts, matched to topic: B2B posts → “Free B2B SEO &amp; AI Search Audit”, Shopify → ecommerce audit, gym posts → fitness audit. These posts receive more organic clicks than all service pages combined.', 'Blog → lead'),
  ('Rewrite the contact page opening', 'Lead with “Talk to a B2B SEO specialist. We reply within 1 business day,” add the booking link and phone, make phone optional, and move the anti-spam note below the form (or handle spam with reCAPTCHA, which is already installed).', 'Contact conversion'),
  ('Fix the Google Business Profile booking page', 'Update /free-quote: match pricing to /pricing ($750 Starter, not $600), refresh the Clutch badges, add a testimonial, and add the HubSpot booking calendar, since GBP\'s “Book” button sends local searchers straight here.', 'Local leads'),
 ]),
 ('Days 31&ndash;60', 'Tests &mdash; Sharpen ICP &amp; Messaging', 'A/B tests and page edits that make B2B buyers feel the site is for them.', [
  ('Test a B2B-first homepage hero', 'Variant: “SEO &amp; AI Search for B2B companies that need pipeline, not just traffic,” with B2B logos and the ZenOne result. Move fitness and ecommerce to an “Other industries we serve” row. Measure audit-form starts and engaged sessions.', 'ICP clarity'),
  ('Add a second, lower-commitment offer', 'Offer the “AI Search Visibility Snapshot” (the dashboard SpearPoint already builds) as an email-only download or instant report for visitors not ready for a call. Use it as a soft CTA on blog posts and the AI Search page.', 'Lead volume'),
  ('Add FAQs to the money pages', 'Add 6&ndash;8 FAQs plus FAQ schema to /pricing, /conversion-based-seo and /conversion-rate-optimization: contract length, time to results, who does the work, what is included, how AI Search is measured, and how SpearPoint differs from other agencies.', 'Objection handling'),
  ('Sticky “Book a call” on mobile', 'Add a slim sticky bar on mobile service pages and blog posts with “Free audit” and “Book a 15-min call.” Test it against the current header button.', 'Mobile conversion'),
  ('Clean up page structure', 'Use one H1 on /seo (it has 3) and a B2B SEO Agency H1 on /b2b-seo, and link each service page to its best case study with numbers.', 'Clarity + SEO'),
 ]),
 ('Days 61&ndash;90', 'Build &mdash; Measure Every Lead', 'Assets and filters that turn this into a monthly CRO program.', [
  ('Filter bot traffic and connect HubSpot', 'Add a GA4 filter or segment for suspected spam (e.g. /scholarship hits and low-engagement Direct traffic from Singapore and China) so conversion rate uses real visitors. Match HubSpot contacts to their original source, so organic and AI Search leads can be reported here.', 'Measurement'),
  ('Build B2B case study pages', 'Turn the B2B wins into indexable case studies with numbers, timeline and process, and link them from /b2b-seo, the AEO page and the audit form.', 'Proof'),
  ('Trim third-party scripts', 'Audit the 23 third-party hosts on service pages. Remove unused tools (e.g. duplicate analytics or SEO scripts), delay Hotjar and Facebook until interaction, and recheck mobile Core Web Vitals.', 'Speed'),
  ('Run Hotjar recordings on the audit funnel', 'Hotjar is already installed. Review 50+ sessions on /free-seo-audit and the top blog posts to see where visitors stop scrolling or abandon the form, then feed that into the next tests.', 'Insight'),
  ('Monthly CRO review in this dashboard', 'Track conversion rate by landing page, form start → submit rate and meetings booked each month, alongside the SEO and AI Search dashboards.', 'Accountability'),
 ]),
]
n = 0; road = []
for badge, title, sub, items in R:
    cards = []
    for h, p, tag in items:
        n += 1
        cards.append(f'<div class="imp-card"><div class="imp-num">{n:02d}</div><div class="imp-body"><span class="imp-flag flag-existing">{tag}</span><h4>{h}</h4><p>{p}</p></div></div>')
    road.append(f'<div class="phase"><div class="phase-head"><span class="phase-badge">{badge}</span><h3>{title}</h3></div><p class="phase-sub">{sub}</p><div class="imp-grid">{"".join(cards)}</div></div>')
road_html = '<div class="roadmap">' + ''.join(road) + '</div>'

body = [
 section('alt', 'Snapshot', 'KPI Summary', 'Traffic, engagement and conversions from GA4 (last 90 days) plus the Website CRO Score from a page-by-page audit of thespearpoint.com.', kpis + takeaways),
 section('', 'User Journey', 'Conversion Path: Search → Landing Page → Conversion', 'How an organic visitor gets from Google to a sales conversation today, and the points where they are likely to drop off. Landing-page shares come from Search Console (last 90 days, Aug 13 &ndash; Nov 10, 2026).', flow_html),
 section('alt', 'Friction Points', 'Where Visitors May Be Getting Stuck', 'Ranked by likely impact on B2B lead volume.', stuck_html),
 section('', 'Traffic &amp; Engagement', 'Traffic, Engagement &amp; Conversions (GA4)', 'GA4, last 90 days (Aug 13 &ndash; Nov 10, 2026): the lead funnel, sessions and engagement by channel, and engagement and form starts by page.', traffic_html),
 section('alt', 'CRO Best Practices', 'Page-by-Page CRO Scorecard', 'Each key page scored against six CRO best practices: ICP, messaging, proof, answering buyer questions, a clear CTA and next step, and low-friction conversion.', score_html),
 section('roadmap-beige', 'Action Plan', 'How to Get More Conversions: 90-Day CRO Roadmap', 'Sixteen recommendations, sequenced so lead tracking and the fastest friction fixes ship first, then the messaging tests, then the tracking and proof that make CRO a monthly habit.', road_html),
]
method = ('Sources: live review of thespearpoint.com pages, forms and scripts in Chrome (Nov 16, 2026); Google Search Console landing pages for the www.thespearpoint.com property (last 90 days, client data); '
  'GA4 property SpearPoint Marketing LLC (stream SpearPoint Website), Aug 13 – Nov 10, 2026. Page scores are SpearPoint\'s CRO audit judgments using the rubric shown. Prepared by SpearPoint Marketing.')
page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="robots" content="noindex">
<title>CRO + Website &mdash; SpearPoint Marketing</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="report-header"><div class="header-inner"><img src="{logo_h}" alt="SpearPoint Marketing"><div class="header-meta">Generated {GEN_DATE}<br>Site: thespearpoint.com</div></div>
<div class="eyebrow-row"><div class="eyebrow">CRO + Website Report</div><h1 class="report-title">SpearPoint Marketing CRO + Website Dashboard - B2B</h1>
<p class="report-sub">How well thespearpoint.com turns search visitors into B2B leads: traffic and engagement, conversions, the user journey from search to conversion, a CRO best-practice scorecard, and a 90-day plan to raise conversion rate. Sources: GA4 · Google Search Console · live site review.</p></div></header>
<nav class="report-nav"><div class="wrap"><a href="./#overview" target="_top" onclick="if(window.parent!==window&&parent.showTab){{parent.showTab('overview');return false}}">Overview</a><a href="./#seo" target="_top" onclick="if(window.parent!==window&&parent.showTab){{parent.showTab('seo');return false}}">SEO Dashboard</a><a href="./#ai" target="_top" onclick="if(window.parent!==window&&parent.showTab){{parent.showTab('ai');return false}}">AI Search Dashboard</a><span class="on" aria-current="page">CRO + Website Dashboard</span></div></nav>
{''.join(body)}
<footer><div class="wrap"><img src="{logo_f}" alt="SpearPoint Marketing"><p>{e(method)}</p></div></footer>
</body></html>"""
os.makedirs('cro', exist_ok=True)
open('cro/index.html', 'w').write(page)
print('wrote cro/index.html', len(page), 'site score', site_score, crit_avg)
