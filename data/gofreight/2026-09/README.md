# GoFreight AEO Monthly Report: September 2026 · raw data and scripts

Backing data for [`gofreight_september_2026_report.html`](../../../gofreight_september_2026_report.html) (September 2026 vs August 2026). Generated 2026-10-06.

## Key convention
All builder inputs use `jun` = **August (prior)** and `jul` = **September (current)**; `gf_core17_sep.json` uses explicit `augPos` / `sepPos`.

## `json/`
| File | Source | Contents |
|---|---|---|
| `gofreight-sep-data.json` | GSC (sc-domain:gofreight.com, main domain filter) | Totals, query segments, subfolders, top 30 pages, weekly clicks (Jan 5 to Sep 28; report charts stop at Sep 21, the last full week) |
| `gf-page-clicks-sep.json` | GSC | Per page clicks, Aug and Sep |
| `gf_core17_allpages.json` | GSC, country = usa | 17 keyword core panel: every GoFreight page ranking per keyword, Aug and Sep (report: main page = most US impressions, monthly average position; best position = best monthly average across pages with 10+ US impressions; sitelinks excluded) |
| `gf_core17_sep.json` / `gf-core-page-us-sep.json` | GSC, country = usa | Earlier fixed target page pull (kept for reference) |
| `wd_sep.json` | WorkDuo `/responses` (occurrence count) | Citations per page, totals, weekly + monthly non brand visibility (Jul 1 to Oct 4) |
| `ga4_ai_traffic.json`, `ga4-ai-drop.json`, `ga4-chatgpt-lp.json` | GA4 property 373075091 | AI referral sessions: weekly, monthly, by source, by landing page |
| `gf_tracker_flags.json` | Content Delivery Tracker | NovaStacks Created / Updated flag per URL |

## `scripts/`
Pulls: `gofreight_sep_data.py`, `gf_page_clicks_sep.py`, `gf_core17_sep.py`, `wd_sep.py`, `ga4_sep.py` (run from `audit/seo-audit-testing/`). Build: `build_sep_report.py` → `write_sep_report.py` (uses `aeo_text.py`) → `apply_core17_sep.py` → `postfix.py` (house style: dashes and compound hyphens).

## Credentials
None committed. WorkDuo keys load from `WORKDUO_PUBLIC_KEY` / `WORKDUO_SECRET_KEY`; GSC / GA4 tokens from `input/credentials/` in the private audit repo.
