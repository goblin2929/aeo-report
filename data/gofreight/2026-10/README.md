# GoFreight AEO Monthly Report: October 2026 · raw data and scripts

Backing data for [`gofreight_october_2026_report.html`](../../../gofreight_october_2026_report.html) (October 2026 vs September 2026). Generated 2026-11-03.

## Key convention
Builder inputs use `jun` = **September (prior)** and `jul` = **October (current)**; `gf_core17_allpages.json` uses explicit `sep` / `oct`.

## `json/`
| File | Source | Contents |
|---|---|---|
| `gofreight-oct-data.json` | GSC (sc-domain:gofreight.com, main domain filter) | Totals, query segments, subfolders, top 30 pages, weekly clicks (Jan 5 to Oct 26) |
| `gf-page-clicks-oct.json`, `gf_pages_country_sep_oct.json` | GSC | Per page clicks; per page clicks / impressions / position and per country, Sep and Oct |
| `gf_core17_allpages.json` | GSC, country = usa | 17 keyword core panel, every GoFreight page per keyword (www host rows excluded in the build) |
| `wd_oct.json` | WorkDuo `/responses` (occurrence count) | Citations per page, totals, weekly + monthly non brand visibility (Aug 1 to Nov 1) |
| `ga4_ai_traffic.json`, `ga4-ai-drop.json`, `ga4-chatgpt-lp.json`, `ga4_chatgpt_direct_daily.json` | GA4 property 373075091 | AI referral sessions weekly, monthly, by source, by landing page; daily ChatGPT for the 8 to 15 Oct tracking bug check |
| `gsc_genai.json`, `gsc-exports/` | GSC UI exports (2026-11-03) | Generative AI features vs all web impressions (date basis), Oct vs Sep per page / country |
| `gf_tracker_flags.json` | Content Delivery Tracker | NovaStacks Created / Updated flag per URL |

## `scripts/`
Pulls: `gofreight_oct_data.py`, `gf_page_clicks_oct.py`, `gf_core17_oct.py`, `wd_oct.py`, `ga4_oct.py` (run from `audit/seo-audit-testing/`). Build: `run_oct.sh` (`build_oct_report.py` → `write_oct_report.py` with `aeo_text.py` → `apply_core17_oct.py` → `postfix_oct.py`).

## Credentials
None committed. WorkDuo keys load from `WORKDUO_PUBLIC_KEY` / `WORKDUO_SECRET_KEY`; GSC / GA4 tokens from `input/credentials/` in the private audit repo.
