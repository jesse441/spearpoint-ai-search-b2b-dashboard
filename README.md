# Client Performance Dashboard: build kit

This branch (`builder-kit`) holds everything Claude needs to rebuild the SpearPoint dashboard for a new client.
It is not deployed: Netlify only publishes `main`. The master SOP is the Claude Doc
"Client Performance Dashboard: Master SOP" (https://claude.ai/artifact/RNQVDaCUhRf8N8GFRFDyuL).

## Get it in a new session

```bash
git clone --branch builder-kit --single-branch https://github.com/jesse441/spearpoint-ai-search-b2b-dashboard.git kit
```

## What's here

| Path | What it is |
| --- | --- |
| `reference/site/` | The finished SpearPoint report: `index.html` (tab shell), `overview.html`, `seo.html`, `ai-search.html`, `cro.html`. Copy the look, layout and wording style from these. |
| `reference/generator/build.py` | SEO dashboard generator. Reads `data/*.json`, writes `site/index.html` (= `seo.html`). |
| `reference/generator/cro_build.py` | CRO + Website generator. Reuses the CSS from `site/index.html`, writes `cro/index.html` (= `cro.html`). |
| `reference/generator/overview_build.py` | Overview generator. Reuses CSS from `cro/index.html`, writes `overview/index.html` (= `overview.html`). |
| `reference/generator/plan_build.py` | Optional 90-day plan preview page (not deployed; the plan lives on the client spreadsheet). |
| `reference/generator/parse_serp.py` | Turns SE Ranking SERP results into `serps2.json` (top-10 counts per domain). |
| `reference/generator/base.css.txt`, `logo1.txt`, `logo2.txt` | Shared CSS and the header / footer logos as data URIs. Replace the logos with the client's. |
| `reference/generator/data/` | SpearPoint's data files, as a format reference for each pull (see below). |
| `reference/generator/build_notes.md` | SpearPoint's build notes: the template for each client's notes. |
| `apps-script/swap_rows.gs` | The "90 Day Plan Swap Rows" Apps Script for the plan tab (simple `onEdit` trigger). |

`ai-search.html` has no generator: it was built by hand. For a new client, copy it and replace its data blocks and text.

## Build order

```
data/*.json ──> build.py ──> site/index.html ──> cro_build.py ──> cro/index.html ──> overview_build.py ──> overview/index.html
                                                   reference/site/ai-search.html (copy + edit by hand)
```

Copy outputs into the client repo as `seo.html`, `cro.html`, `overview.html`, `ai-search.html`, plus `index.html` from `reference/site/`.

## Data files (one per pull)

| File | Source | Shape |
| --- | --- | --- |
| `gsc_trend.json` | GSC, 16 months + comparison windows | `{monthly, windows, devices, total16}` |
| `gsc90_queries.json`, `gsc90_pages.json` | GSC, last 90 days | `[[key, clicks, impressions, position], …]` |
| `gsc16_queries.json`, `gsc16_pages.json` | GSC, 16 months | same |
| `gsc90_analysis.json` | Derived: topic buckets + striking-distance queries | `{cats, striking}` |
| `gsc90_landing_groups.json` | Derived: landing page buckets for the CRO path | `{Homepage, Blog posts, Service pages, Conversion & proof pages, Other}` |
| `keywords.json`, `keywords_ranked.json` | SE Ranking keyword research + client rank | rows |
| `gaps.json` | SE Ranking domain-keywords comparison | rows |
| `competitors.json` | SE Ranking domain overview per brand | `{brand: {...}}` |
| `domain_trust.json` | SE Ranking Domain Trust history + referring-domain quality | `{months, series, …}` |
| `serps2.json` | SE Ranking SERP top 100 for the 6 priority keywords | `{keyword: [...]}` |
| `scores.json` | Computed SEO Strength + SERP Competitiveness | `{targeted, serp}` |
| `ga4_raw.json` | GA4, last 90 days | `{range, totals, channels, pages, events, key_events_configured}` |
| `plan90.json` | 90-day plan rows (P, R, T, B, G, A) | used for the spreadsheet tab |

## Adapting for a client

1. Copy `reference/generator/` to a working folder. Replace `data/` with the client's pulls in the same shapes.
2. Search each generator for SpearPoint-specific text (brand names, competitor names, priority keywords, takeaway copy, roadmap items) and rewrite it from the client's data. Never leave SpearPoint wording behind: `grep -ri "spearpoint\|breaking b2b\|trioseo\|denver" .` must come back empty except for intended matches.
3. Swap the logos, brand colors and font in `base.css.txt` / `logo*.txt`.
4. Run the generators in order, copy outputs into the client repo, push to `main`.
