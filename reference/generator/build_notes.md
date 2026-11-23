# SpearPoint B2B Dashboard: build notes & monthly refresh

**Live report (one URL, 4 tabs):** https://spearpoint-dashboard-b2b.netlify.app/
Tabs: Overview (default) · SEO · AI Search · CRO + Website. Link to a tab with `#overview`, `#seo`, `#ai` or `#cro`.
Renamed Nov 17, 2026 from spearpoint-ai-search-b2b.netlify.app; the old URL no longer works.

First built: Nov 13, 2026. Revised Nov 16 (keywords, scoring, Domain Trust) and Nov 17 (CRO dashboard, GA4, Overview page, one-URL report, Denver keyword swap).

## How the report is built and deployed
- **Repo:** GitHub `jesse441/spearpoint-ai-search-b2b-dashboard`, branch `main`. Netlify project `spearpoint-dashboard-b2b` deploys automatically on every push to main.
- **Files:**
  - `index.html`: shell page with the tab switching. Each tab loads its dashboard in an auto-height iframe.
  - `overview.html`, `seo.html`, `ai-search.html`, `cro.html`: the four tabs. Each page's nav calls `parent.showTab()`.
  - The AI Search page's floating Vidyard video lives in `index.html` and shows only on the AI Search tab.
- **Generators (Claude workspace):** `build.py` (SEO), `cro_build.py` (CRO), `overview_build.py` (Overview), all in one Python generator folder. AI Search is edited directly in `ai-search.html`.
- **Unused Netlify sites:** `spearpoint-seo-b2b` and `spearpoint-cro-website-b2b` are leftovers and can be deleted.

## Priority keywords (updated Nov 17)
B2B SEO Agency · **Denver SEO Company** (replaced Denver SEO Agency on Nov 17, checked in Denver, CO) · aeo agency · ai search optimization agency · SEO + CRO Agency · Conversion Based SEO
- Denver SEO Company: #14 on /seo in SE Ranking's US database. GSC 90-day average #18.2 (2,214 impressions, 0 clicks). Not in the top 70 in the Nov 17 Denver live check, where Thrive Agency is #1. It is not in the rank tracker (no keyword slots free).

## Competitors
- **Targeted (monitor across all 3 reports):** Breaking B2B, TrioSEO, Flow Agency, Thrive Digital (thrivedigital.com).
- **Top 4 SERP competitors:** Thrive Agency (thriveagency.com, a different company from Thrive Digital), Coalition Technologies, 1Digital Agency, Optimist (yesoptimist.com). SpearPoint is shown alongside them for comparison.

## Scoring (0–100, same formulas every month)
**SEO Strength Score** (Targeted Competitors) does not include the priority keywords:
- 30% Domain Trust
- 25% keywords in the top 10 (log, 10,000 = 100)
- 25% organic traffic (log, 100,000/mo = 100)
- 20% referring domains (log, 10,000 = 100)

Nov 16 scores: Flow 65 · TrioSEO 60 · Breaking B2B 58 · Thrive Digital 54 · SpearPoint 49.

**SERP Competitiveness Score** (Top 4 SERP + SpearPoint):
- 35% priority-keyword points (top 3 = 100, 4–10 = 75, 11–20 = 40, 21–50 = 15, 51–100 = 5, none = 0, averaged over 6)
- 20% Domain Trust
- 15% each for top-10 keywords, traffic and referring domains

Nov 17 scores (after the Denver swap): Thrive Agency 78 · Coalition 68 · 1Digital 54 · Optimist 52 · SpearPoint 42.

## CRO + Website (Nov 17 baseline)
- **Website CRO Score: 59/100.** Ten pages were scored 1–5 on ICP, messaging, proof, buyer questions, CTA and friction, weighted by organic clicks.
  - Best page: /seo at 80. Worst pages: /contact at 33 and /free-seo-audit at 43.
- **GA4** (property "SpearPoint Marketing LLC" 351870281, stream "SpearPoint Website"; Aug 13 – Nov 10):
  - Traffic: 4,086 sessions, 3,435 users, 34.9% engagement rate. Organic Search had 577 sessions at 60.5% engagement.
  - Forms: 104 form_start events from 66 users, but only 2 form_submit events.
  - **0 key events.** generate_lead and Schedule are configured but have never fired, so fixing lead tracking is roadmap item #1.
  - Suspected bot or spam traffic: Direct (75% of sessions at 27% engagement) and /scholarship.
- **Journey stuck points:** blog posts get 43% of organic clicks but have no in-article CTA. Other issues:
  - The audit form has 6 fields, including a required budget and textarea, and booking is a separate step.
  - The site has no phone number or chat.
  - The /contact page opens with a spam warning.
  - /free-quote (the Google Business Profile booking page) shows "$600/mo", which conflicts with /pricing ($750), and has 2023 Clutch badges.

## Rank source
The SE Ranking daily tracker is the source of truth. Use live SERP checks only for keywords the tracker doesn't cover.

## Where else things live
- **SE Ranking project:** "SpearPoint Marketing LLC" (7259084). Engines: 1175311 (US) and 2944117 (Denver). The keyword and competitor limits are full.
- **Supabase** (on hold): `ai_search_snapshots` (rcrpcdorpyexpqvjmesu), `b2b_seo_*` tables.

## Monthly refresh SOP
1. Export GSC (16 months) and pull GA4 for the last 90 days: traffic acquisition, events and pages.
2. Pull SE Ranking tracker ranks, competitor overviews, backlinks and Domain Trust. Recompute both scores.
3. Re-check the CRO scorecard pages for changes.
4. Rebuild seo.html, cro.html and overview.html, copy them into the repo and push to main. Netlify redeploys automatically.
