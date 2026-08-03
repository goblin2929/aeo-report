# GoFreight AEO Monthly Report — July 2026 · raw data & scripts

Backing data and reproducibility scripts for [`gofreight_july_2026_report.html`](../../../gofreight_july_2026_report.html)
(July 2026 vs June 2026). Generated 2026-08-03.

## `json/` — pulled datasets
| File | Source | Contents |
|---|---|---|
| `gofreight-july-data.json` | GSC (sc-domain:gofreight.com, main-domain filtered) | July vs June totals, query segments, subfolders, top-30 pages, weekly clicks |
| `gf-core-page-us-july.json` | GSC, country=usa, per target page | Core-keyword US position by target page (Jun vs Jul) |
| `gf-page-clicks-july.json` | GSC | Per-page July/June click map (for most-cited clicks) |
| `wd_july.json` | WorkDuo `/responses` (occurrence-count) | Per-page citations, subfolder rollup, totals, weekly + monthly non-brand visibility |
| `wd_w31.json` | WorkDuo | Final-week (Jul 27–Aug 2) engine visibility |
| `ga4_ai_traffic.json` | GA4 property 373075091 | Weekly + monthly AI-referral sessions |
| `ga4-ai-drop.json` | GA4 | AI-session Jun→Jul deltas by source and by landing page |
| `ga4-chatgpt-lp.json` | GA4 (ChatGPT sources only) | ChatGPT landing-page Jun→Jul deltas |

## `scripts/` — pull + build
- **GSC (Node):** `gofreight-july-data.js`, `gf-core-page-us-july.js`, `gf-page-clicks-july.js`, `gf-fms-check.js` — run via the audit repo's `auth.js` (OAuth profile `novastacks`).
- **GA4 (Node):** `ga4-auth.js` (one-time OAuth), `ga4-ai-traffic.js`, `ga4-ai-drop-analysis.js`, `ga4-chatgpt-lp.js`.
- **WorkDuo (Python):** `wd_july.py`, `wd_w31.py`, `wd_competitor_diag.py` (competitor-vs-GoFreight citation rates).
- **Report builders (Python):** `build_july_report.py` → `frag_july.pkl`, then `write_july_report.py` → the HTML.

## Credentials
No secrets are committed. The WorkDuo scripts load keys from the environment
(`WORKDUO_PUBLIC_KEY` / `WORKDUO_SECRET_KEY`); the GSC/GA4 scripts read the OAuth
profile / token files from the private audit repo (not included here). Set the
env vars before running the WorkDuo scripts.
