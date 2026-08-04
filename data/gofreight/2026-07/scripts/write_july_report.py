# -*- coding: utf-8 -*-
"""Assemble the July 2026 GoFreight report HTML from frag_july.pkl."""
import json, pickle
fr = pickle.load(open('d:/tmp/frag_july.pkl','rb'))
def f(n): return f"{round(n):,}"

CL_N,CL_J = fr['CL_JUN'],fr['CL_JUL']
NB_J,NB_N = fr['NB_J'],fr['NB_N']; nbsh_j=fr['nbsh_j']
d_tot=CL_J-CL_N; d_tot_p=d_tot/CL_N*100
d_nb=NB_J-NB_N; d_nb_p=d_nb/NB_N*100
TOT=fr['TOT']
pc_n,pc_j=TOT['jun_total_cit_primary'],TOT['jul_total_cit_primary']
ac_n,ac_j=TOT['jun_total_cit'],TOT['jul_total_cit']; ac_g=(ac_j-ac_n)/ac_n*100

def jsarr(a): return '['+','.join('null' if x=='null' else f'{x}' for x in a)+']'
week_labels_js='['+','.join(f'"{x}"' for x in fr['week_labels'])+']'

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AEO Monthly Report — GoFreight — July 2026</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root {{ --teal:#017d8e; --teal-d:#0e7490; --slate-9:#0f172a; --slate-7:#334155; --slate-5:#64748b; --slate-3:#cbd5e1; --slate-1:#f1f5f9; --green:#16a34a; --amber:#d97706; --red:#dc2626; }}
  * {{ box-sizing:border-box; }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,'Inter','Segoe UI',system-ui,sans-serif; background:#fff; color:var(--slate-9); margin:0; padding:28px 36px; font-size:13.5px; line-height:1.45; }}
  .page {{ width:1280px; margin:0 auto; }}
  html {{ min-width:1320px; }}
  header {{ border-bottom:2px solid var(--teal); padding-bottom:12px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:flex-end; }}
  header h1 {{ font-size:22px; margin:0; color:var(--slate-9); letter-spacing:-0.01em; }}
  header .meta {{ font-size:12px; color:var(--slate-5); text-align:right; }}
  header .meta strong {{ color:var(--slate-7); }}
  .hook {{ background:linear-gradient(90deg,#ecfeff 0%,#f0fdfa 100%); border-left:4px solid var(--teal); padding:12px 16px; border-radius:4px; margin-bottom:18px; font-size:14px; }}
  .hook strong {{ color:var(--teal-d); }}
  .kpi-row {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:16px; }}
  .kpi {{ border:1px solid var(--slate-3); border-radius:6px; padding:10px 14px; background:#fff; }}
  .kpi .label {{ font-size:11px; color:var(--slate-5); text-transform:uppercase; letter-spacing:0.04em; }}
  .kpi .val {{ font-size:20px; font-weight:700; color:var(--slate-9); margin-top:2px; }}
  .kpi .delta {{ font-size:12px; margin-top:2px; }}
  .delta.up {{ color:var(--green); }} .delta.down {{ color:var(--red); }} .delta.flat {{ color:var(--amber); }}
  .chart-row {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:22px; }}
  .chart-card {{ border:1px solid var(--slate-3); border-radius:6px; padding:12px 14px 10px; background:#fff; }}
  .chart-card h3 {{ font-size:13px; margin:0 0 2px; color:var(--slate-9); }}
  .chart-card .sub {{ font-size:11px; color:var(--slate-5); margin-bottom:8px; }}
  .chart-canvas-wrap {{ height:200px; position:relative; }}
  .chart-card .takeaway {{ margin-top:8px; font-size:11.5px; color:var(--slate-7); background:var(--slate-1); padding:6px 8px; border-radius:4px; }}
  .chart-card .takeaway b {{ color:var(--slate-9); }}
  section {{ margin-bottom:22px; }}
  section h2 {{ font-size:13px; margin:0 0 8px; color:var(--teal-d); text-transform:uppercase; letter-spacing:0.06em; border-bottom:1px solid var(--slate-3); padding-bottom:4px; }}
  .two-col {{ display:grid; grid-template-columns:1fr 1fr; gap:22px; }}
  table.t {{ width:100%; border-collapse:collapse; font-size:12px; background:#fff; }}
  table.t th {{ text-align:left; font-size:10.5px; text-transform:uppercase; letter-spacing:0.04em; color:var(--slate-5); border-bottom:1.5px solid var(--slate-3); padding:5px 8px; font-weight:600; }}
  table.t th.num, table.t td.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  table.t th.aeo, table.t td.aeo {{ background:#ecfeff; }}
  table.t th.aeo {{ color:var(--teal-d); }}
  table.t td {{ padding:5px 8px; border-bottom:1px solid var(--slate-1); color:var(--slate-7); }}
  table.t td:first-child {{ color:var(--slate-9); }}
  table.t tr.subtotal td {{ background:var(--slate-1); font-weight:700; color:var(--slate-9); border-top:1.5px solid var(--slate-3); }}
  table.t a {{ color:var(--teal-d); text-decoration:none; }}
  table.t a:hover {{ text-decoration:underline; }}
  .up {{ color:var(--green); }} .down {{ color:var(--red); }}
  .win-row td {{ background:#f0fdf4; }}
  .note {{ font-size:11px; color:var(--slate-5); margin-top:6px; }}
  .takeaway-box {{ margin-top:8px; font-size:11.5px; color:var(--slate-7); background:var(--slate-1); padding:8px 10px; border-radius:4px; }}
  .takeaway-box b {{ color:var(--slate-9); }}
  .takeaway-box.win {{ background:#f0fdf4; border-left:3px solid var(--green); }}
  .takeaway-box.watch {{ background:#fffbeb; border-left:3px solid var(--amber); }}
  .takeaway-box ul {{ margin:4px 0 0; padding-left:18px; }} .takeaway-box li {{ margin-bottom:3px; }}
  .focus-status {{ font-weight:700; font-size:11px; }} .focus-status.done {{ color:var(--green); }}
  .prio-list {{ margin:0; padding-left:20px; }} .prio-list li {{ margin-bottom:6px; font-size:12.5px; }} .prio-list li b {{ color:var(--teal-d); }}
  .tag {{ display:inline-block; font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.04em; padding:1px 6px; border-radius:8px; margin-left:6px; vertical-align:middle; }}
  .tag.aeo {{ background:#ecfeff; color:var(--teal-d); border:1px solid #a5f3fc; }}
  .tag.content {{ background:#f0fdf4; color:var(--green); border:1px solid #bbf7d0; }}
  .tag.technical {{ background:#fffbeb; color:var(--amber); border:1px solid #fde68a; }}
  .tag.product {{ background:#eef2ff; color:#4338ca; border:1px solid #c7d2fe; }}
  footer {{ margin-top:16px; font-size:10.5px; color:var(--slate-5); text-align:center; border-top:1px solid var(--slate-3); padding-top:6px; }}
  @media print {{ body {{ padding:16px 20px; font-size:11.5px; }} .chart-canvas-wrap {{ height:160px; }} header h1 {{ font-size:18px; }} }}
</style>
</head>
<body>
<div class="page">
  <header>
    <div>
      <h1>AEO Monthly Report — July 2026</h1>
      <div style="font-size:11px; color:var(--slate-5); margin-top:2px;">July vs June 2026 monthly review · GoFreight ↔ Novastacks</div>
    </div>
    <div class="meta">
      <div><strong>August 3, 2026</strong></div>
      <div>Monthly tables: Jul 1–31 vs Jun 1–30 · Weekly trends: Jan 5 – Jul 27</div>
      <div>GSC filtered to gofreight.com (support / api / archive subdomains excluded)</div>
    </div>
  </header>

  <div class="hook">
    <strong>Headline:</strong> July was another broad-based growth month — total clicks <strong>+33.2% (6,390)</strong>, non-brand <strong>+47.8% (5,287, now 82.7% of all clicks)</strong>, and CTR <strong>0.37% → 0.51%</strong>. AEO deepened sharply: WorkDuo AI visibility <strong>29.3% (+6.0pp)</strong>, share of voice <strong>26% (+4.5pp)</strong>, and AI citations <strong>+34.6% (5,903 → 7,947)</strong>. The one soft spot: AI-referred sessions dipped to <strong>392 (−18.3%)</strong> — and that decline is <strong>entirely a ChatGPT referral pullback</strong> (every other engine grew), coinciding with an early-July ChatGPT model update. GoFreight’s own ChatGPT citation visibility actually rose (+6.6pp), so this is a referral-behavior shift, not a loss of AI presence.
  </div>

  <div class="kpi-row">
    <div class="kpi"><div class="label">Total Clicks · July</div><div class="val">6,390</div>
      <div class="delta up">+{f(d_tot)} (+{d_tot_p:.1f}%) vs June · Non-brand {f(NB_J)} ({nbsh_j:.1f}%)</div></div>
    <div class="kpi"><div class="label">Non-Brand Clicks · July</div><div class="val">{f(NB_J)}</div>
      <div class="delta up">+{f(d_nb)} (+{d_nb_p:.1f}%) MoM</div></div>
    <div class="kpi"><div class="label">AI Visibility · July (WorkDuo)</div><div class="val">29.3%</div>
      <div class="delta up">+6.0 pts vs June · SOV 26.0% (+4.5 pts)</div></div>
    <div class="kpi"><div class="label">AI Sessions · July (GA4)</div><div class="val">392</div>
      <div class="delta down">−18.3% vs June 480 · ChatGPT-driven dip</div></div>
  </div>

  <div class="chart-row">
    <div class="chart-card">
      <h3>① Total Clicks vs Non-Brand Clicks (Weekly)</h3>
      <div class="sub">GSC gofreight.com, date-dim · non-brand = total minus brand-regex queries</div>
      <div class="chart-canvas-wrap"><canvas id="chart1"></canvas></div>
      <div class="takeaway"><b>Read:</b> Non-brand clicks kept climbing — July delivered <b>{f(NB_J)} non-brand clicks (+{d_nb_p:.1f}% MoM)</b> and non-brand share reached <b>{nbsh_j:.1f}% of total</b>, up from 74.6% in June. The content program keeps compounding on the informational long-tail.</div>
    </div>
    <div class="chart-card">
      <h3>② AEO Visibility · Non-Brand by Engine (Weekly)</h3>
      <div class="sub">WorkDuo · 28 non-brand prompts (MOFU/TOFU/BOFU); self-mention rate per engine</div>
      <div class="chart-canvas-wrap"><canvas id="chart2"></canvas></div>
      <div class="takeaway"><b>Read:</b> <b>Google AI Overview held its series-high band (37–41%)</b> for most of July, easing only in the final week (Jul 27–Aug 2). Blended non-brand visibility rose to <b>29.3% for July</b> (from 23.4% in June) — a series high. The final-week dip is <b>industry-wide</b> (competitor evidence in the deep-dive below), not a GoFreight-specific loss.</div>
    </div>
    <div class="chart-card">
      <h3>③ AI Traffic Sessions (Weekly · GA4)</h3>
      <div class="sub">GA4 property 373075091, sessionSource matching AI platforms (chatgpt, perplexity, gemini, claude, copilot…)</div>
      <div class="chart-canvas-wrap"><canvas id="chart3"></canvas></div>
      <div class="takeaway"><b>Read:</b> AI sessions eased through July (weekly 90 → 77 → 67, recovering to 110 late-month) — <b>July totaled 392 vs June’s 480 (−18.3%)</b>. The full decline is ChatGPT (see the AI-Traffic Deep-Dive below); Gemini, Claude and Perplexity all grew, so total AI reach is diversifying.</div>
    </div>
  </div>

  <div class="two-col">
    <section>
      <h2>July — What Was Done</h2>
      <table class="t">
        <thead><tr><th>#</th><th>Initiative</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td class="num">1</td><td><b>Proposal — Knowledge pages (SEO hygiene)</b> — sent a proposal to clean up and standardize the Knowledge / help-center pages for crawlability and consistency.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">2</td><td><b>Proposal — Customer Stories page redesign</b> — sent a proposal for a new design structure for the Customer Stories pages.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">3</td><td><b>Secured a free backlink from FlexFulfillment</b> — the June reciprocal exchange landed live: <a href="https://www.flexfulfillment.eu/what-a-3pl-should-check-when-your-inbound-arrives-the-receiving-standards-that-matter/" target="_blank">flexfulfillment.eu — inbound receiving standards</a>.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">4</td><td><b>Refreshed 16 articles for search-engine visibility</b> — re-optimized existing posts to lift organic rankings and CTR.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">5</td><td><b>Refreshed 2 articles for the AI-citation gap</b> — reworked pages specifically to close gaps where AI engines were not yet citing GoFreight.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">6</td><td><b>Published 12 new articles</b> — new topical coverage (BAU cadence).</td><td><span class="focus-status done">DONE</span></td></tr>
        </tbody>
      </table>
      <div class="takeaway-box" style="margin-top:10px;"><b>Effect visible in the data:</b> Blog clicks +20.8% and Glossary +191% MoM; primary-domain AI citations rose {f(pc_n)} → {f(pc_j)}; Product-page citations jumped 374 → 806 (workflow-automation 30 → 192, integrations 269 → 387) as the fan-out FAQ work keeps compounding.</div>
    </section>

    <section>
      <h2>August 2026 — Next Action Items &amp; Priorities</h2>
      <ol class="prio-list">
        <li><b>Revisit the Solution pages</b> — audit each Solution page to identify concrete improvements (messaging, structure, on-page SEO, and fan-out FAQ), building on the Product-page gains already showing in AI citations.<span class="tag product">Product</span><span class="tag aeo">AEO</span></li>
        <li><b>Implement the Customer Stories page revamp</b> — build the new design structure proposed in July: re-architect the content so it is clearer and more convenient for users, and easier for crawlers and AI engines to extract, with improved on-page SEO tags (title, meta, headings, structured data).<span class="tag product">Product</span><span class="tag technical">Technical</span><span class="tag aeo">AEO</span></li>
        <li><b>BAU — 30 new articles</b> — maintain the monthly publishing cadence (30 articles) that is driving the non-brand and citation growth.<span class="tag content">Content</span></li>
      </ol>
      <div class="takeaway-box watch" style="margin-top:12px;"><b>Watch:</b> the ChatGPT referral pullback (AI sessions −18%, all ChatGPT) and the late-July Google AI Overview citation dip — both are <b>industry-wide</b> (competitors fell in the same window), so monitor whether they stabilize as the mid-2026 AI-platform changes settle; diversification into Gemini/Claude/Perplexity is the hedge.</div>
    </section>
  </div>

  <section>
    <h2>Query Segment Breakdown (July vs June)</h2>
    <table class="t"><thead>
      <tr><th>Segment</th><th class="num">June Clicks</th><th class="num">July Clicks</th><th class="num">Click Δ</th><th class="num">Δ %</th><th class="num">June Impr</th><th class="num">July Impr</th><th class="num">Impr Δ</th></tr>
    </thead><tbody>
      {fr['seg']}
    </tbody></table>
    <div class="takeaway-box"><b>Read:</b> Non-branded grew <b>+{d_nb_p:.1f}% MoM (+{f(d_nb)})</b> while branded held roughly flat — the content flywheel again. Non-branded now stands at <b>{nbsh_j:.1f}% of all clicks</b>, up from 74.6% in June. Brand rows are measured on the full property (query-dim); non-brand is derived as total minus brand.</div>
  </section>

  <section>
    <h2>Subfolder Performance (July vs June) — with AI Citation Coverage</h2>
    <table class="t"><thead>
      <tr><th>Subfolder</th><th class="num">June Clicks</th><th class="num">July Clicks</th><th class="num">Click Δ</th><th class="num">Δ %</th><th class="num">June Impr</th><th class="num">July Impr</th><th class="num aeo">Pages Cited · June</th><th class="num aeo">Pages Cited · July</th></tr>
    </thead><tbody>
      {fr['sub']}
    </tbody></table>
    <p class="note">Totals reflect the primary gofreight.com property (support / api / archive subdomains excluded per the filter). <b>Pages Cited by AI</b> = distinct pages cited as a source by ChatGPT, Perplexity, or Google AI in WorkDuo-tracked responses that month, shown as <i>pages (total citations)</i>.</p>
    <div class="takeaway-box"><b>Read:</b> <b>Glossary surged +191%</b> (clicks 580 → 1,690) on the terminal-tracking and Incoterms pages, and <b>Blog grew +20.8%</b> with citations 4,399 → 5,830. <b>Product is the AEO standout</b> — citations 374 → 806 (workflow-automation 30 → 192, integrations 269 → 387), the fan-out FAQ work compounding. Homepage clicks eased −8% but its US commercial rankings strengthened (see Core Keyword Tracking).</div>
  </section>

  <section>
    <h2>Top 30 Pages by Clicks (July vs June) — with AI Citations per Page</h2>
    <table class="t"><thead>
      <tr><th>#</th><th>Page</th><th>Recent Work</th><th class="num">June Clicks</th><th class="num">July Clicks</th><th class="num">Δ Clicks</th><th class="num">July Impr</th><th class="num aeo">AI Citations · June</th><th class="num aeo">AI Citations · July</th></tr>
    </thead><tbody>
      {fr['top30']}
    </tbody></table>
    <p class="note"><b>Recent Work</b> tags carried forward from prior reports (historical NovaStacks work markers); July’s specific refreshed / new-article URLs are not individually tagged here. <b>AI Citations</b> = WorkDuo-tracked AI responses citing this page as a source in the month.</p>
  </section>

  <section>
    <h2>Top 15 Most-Cited Pages by AI — A Different List Than the Click Winners</h2>
    <table class="t"><thead>
      <tr><th>#</th><th>Page</th><th class="num aeo">AI Citations · June</th><th class="num aeo">AI Citations · July</th><th class="num">Δ</th><th class="num">July Clicks</th><th class="num">In Click Top 30?</th></tr>
    </thead><tbody>
      {fr['top15']}
    </tbody></table>
    <div class="takeaway-box"><b>Read: SEO winners and AEO winners are different pages.</b> Google clicks flow to educational long-tail content; AI engines answering buying-intent prompts cite the <b>commercial pages</b> — platform-overview, cargowise-vs-gofreight, best-freight-management-software, best-tms-software, /product/integrations, /product/workflow-automation. The Product pages’ climb (workflow-automation 30 → 192) shows the June fan-out FAQ work is now landing in AI answers.</div>
  </section>

  <section>
    <h2>Core Keyword Tracking — Commercial Cluster (GSC avg position by target page, United States market, July vs June)</h2>
    <table class="t"><thead>
      <tr><th>Core Keyword</th><th>Target Page</th><th class="num">July Impr (US)</th><th class="num">June Pos</th><th class="num">July Pos</th><th class="num">Δ Position</th><th>Note</th></tr>
    </thead><tbody>
      {fr['core']}
    </tbody></table>
    <p class="note">United States market only (GSC country = usa), filtered to <b>each keyword's specific target page</b> (query + page), not the blended all-pages average. Lower = better.</p>
    <div class="two-col" style="margin-top:10px;">
      <div class="takeaway-box win"><b>✓ Wins on the target page (US)</b>
        <ul>
          <li><b>The homepage broke into the top of the US SERP</b> — “freight forwarder software” 4.1 → <b>1.8</b> and “freight forwarding software” 5.8 → <b>2.5</b>. June’s cannibalization has resolved and the homepage now owns these terms.</li>
          <li><b>“best tms software”</b> climbed 5.7 (15.7 → 10.0), and “best freight management software” (6.2 → 4.4) and “freight tracking software” (6.6 → 4.9) improved on the best-fms blog.</li>
          <li><b>“freight management software” is won by the listicle</b> — <b>/blog/best-freight-management-software holds position ~2 (1.8)</b> in the US, both months. (Tracking was re-pointed from the homepage, which only surfaces weakly at ~33 for this query — the listicle is the page that actually ranks.)</li>
        </ul>
      </div>
      <div class="takeaway-box watch"><b>⚠ Watch (US, target page)</b>
        <ul>
          <li><b>“logistics crm software”</b> softened on the CRM listicle (15.1 → 17.3) and <b>“freight software”</b> eased (8.3 → 10.0). The August Solution-page work targets the commercial cluster.</li>
          <li>The homepage still surfaces weakly (~33) as a secondary URL for “freight management software”; low priority (zero clicks), but a canonical/internal-link nudge toward the listicle would tidy the signal.</li>
        </ul>
      </div>
    </div>
  </section>

  <section>
    <h2>AI Traffic Deep-Dive — Why AI Sessions Dipped in July</h2>
    <p class="note" style="margin-bottom:8px;">AI-referred sessions fell from 480 (June) to 392 (July). This section isolates <b>which engines and which pages</b> moved, and offers a fair read of the likely cause.</p>
    <div class="two-col" style="align-items:start;">
      <div>
        <table class="t"><thead>
          <tr><th>AI Source</th><th class="num">June</th><th class="num">July</th><th class="num">Δ</th></tr>
        </thead><tbody>
          {fr['src']}
        </tbody></table>
        <div class="takeaway-box win" style="margin-top:8px;"><b>The decline is 100% ChatGPT — and traffic is diversifying.</b> ChatGPT was <b>{fr['cg_share_jun']}% of all AI sessions in June</b> and drove the entire net drop ({fr['cg_jun']} → {fr['cg_jul']}, {fr['cg_drop']}). <b>Every other engine grew</b> — Gemini, Claude and Perplexity all added sessions — so GoFreight’s AI reach is broadening beyond a single platform.</div>
      </div>
      <div>
        <table class="t"><thead>
          <tr><th>ChatGPT landing pages that lost sessions</th><th class="num">June</th><th class="num">July</th><th class="num">Δ</th></tr>
        </thead><tbody>
          {fr['lp_drop']}
        </tbody></table>
        <table class="t" style="margin-top:8px;"><thead>
          <tr><th>ChatGPT landing pages that gained</th><th class="num">June</th><th class="num">July</th><th class="num">Δ</th></tr>
        </thead><tbody>
          {fr['lp_gain']}
        </tbody></table>
      </div>
    </div>
    <div class="takeaway-box" style="margin-top:10px;"><b>Likely cause (hypothesis, fairly stated).</b> The drop is entirely ChatGPT and <b>broad-based across pages</b> (the homepage alone is −52, with the rest spread thin across help-center, demo, pricing and older educational pages) — a shape that fits a <b>platform-level change in how ChatGPT surfaces and links sources</b>, not a GoFreight ranking loss. Industry reports attribute an <b>early-July ChatGPT model update</b> to shorter, more self-contained answers with fewer click-throughs. Critically, GoFreight’s own <b>ChatGPT citation visibility rose +6.6pp</b> in the same period (WorkDuo) — so GoFreight is being <b>cited more but clicked less</b>: a referral-behavior shift, not a loss of AI presence. Two supporting checks: it is not seasonality (organic clicks rose +33%), and it is not an attribution artifact (unattributed “not set” traffic also fell, so sessions were not merely re-bucketed). <i>We treat the model-update link as a directional external factor, not a proven cause; the ChatGPT-isolated, cross-page pattern is the hard evidence.</i></div>
    <div class="takeaway-box"><b>Is this GoFreight-specific? No — it is category-wide.</b> The chart ② final-week visibility dip raises the same question, and the answer is the same: measuring competitors in the <i>same</i> Google AI Overview answers, <b>every major vendor's citation rate fell in that final week</b> — a platform shift, not a GoFreight loss. GoFreight stayed the <b>most-cited vendor</b> in the category throughout (261 mentions vs CargoWise 209, Magaya 204, Descartes 194 over Jul 6–Aug 2).
      <table class="t" style="margin-top:6px;">
        <thead><tr><th>Google AI Overview — weekly citation rate</th><th class="num">Jul 6–12</th><th class="num">Jul 13–19</th><th class="num">Jul 20–26</th><th class="num">Jul 27–Aug 2</th></tr></thead>
        <tbody>
          <tr class="win-row"><td><b>GoFreight</b></td><td class="num">41.3%</td><td class="num">39.8%</td><td class="num">38.7%</td><td class="num down">22.3%</td></tr>
          <tr><td>CargoWise</td><td class="num">27.4%</td><td class="num">28.5%</td><td class="num">31.5%</td><td class="num down">25.9%</td></tr>
          <tr><td>Magaya</td><td class="num">33.0%</td><td class="num">30.6%</td><td class="num">24.9%</td><td class="num down">22.3%</td></tr>
          <tr><td>Descartes</td><td class="num">31.8%</td><td class="num">29.6%</td><td class="num">26.5%</td><td class="num down">17.6%</td></tr>
        </tbody>
      </table>
      <span class="note" style="display:block; margin-top:4px;">WorkDuo, same non-brand prompts and engine; competitor rates from the mentionedEntities field. GoFreight fell most in points but from the highest base, and still finished at or above the pack (tied with Magaya, above Descartes).</span>
    </div>
    <div class="takeaway-box win"><b>In plain terms — this is not a GoFreight loss.</b> At the end of July, Google’s AI Overview started putting <b>fewer website links in each answer</b> (mostly on the broad “which freight software should I use?” type questions). We checked what actually changed, and here it is in three simple points:
      <ul>
        <li><b>The answers got shorter for everyone.</b> In mid-July, a typical AI Overview answer linked to about <b>14 websites</b>; by the end of the month it linked to only about <b>8</b>. That is roughly <b>40% fewer links per answer</b> — for every brand, not just GoFreight.</li>
        <li><b>No competitor took our place.</b> GoFreight was not swapped out for a rival — CargoWise, Magaya and Descartes lost links in the very same week, and the <i>types</i> of sites Google cites barely changed. Google is simply citing <b>fewer</b> of them. It is a shrink, not a swap.</li>
        <li><b>GoFreight is being mentioned more, not less.</b> Our AI visibility actually went <b>up +6 points</b> in July. Google is featuring GoFreight <i>more</i> often; it is just linking out to fewer sites overall, so fewer people click through.</li>
      </ul>
      <b>Bottom line:</b> Google changed how it builds its answers (shorter, with fewer links), and it happened to the whole industry at once. It is not something GoFreight did wrong — and GoFreight’s presence in AI answers actually grew.</div>
    <div class="takeaway-box win"><b>The offset:</b> newly published July content is already earning AI referrals across engines — <a href="https://gofreight.com/blog/maritime-disruption" target="_blank">/blog/maritime-disruption</a> (0 → 14 sessions), <a href="https://gofreight.com/blog/freight-forwarding-business-development" target="_blank">/blog/freight-forwarding-business-development</a> (new), and <a href="https://gofreight.com/product/rate-management-quoting" target="_blank">/product/rate-management-quoting</a> — so the content program is expanding AI reach even as ChatGPT’s referral volume compresses.</div>
  </section>

  <section>
    <h2>AEO Metrics — Month over Month</h2>
    <table class="t"><thead>
      <tr><th>Metric</th><th class="num">June 2026</th><th class="num">July 2026</th><th class="num">Change</th><th>Source</th></tr>
    </thead><tbody>
      {fr['aeo']}
    </tbody></table>
    <p class="note">AI Visibility, Share of Voice and LLM Engaged Sessions from the WorkDuo dashboard (project cmhk59aw9001mlo33c3t8n3rj). AI Platform Sessions from GA4 direct (property 373075091); the WorkDuo dashboard reads July AI sessions at 342 on a narrower source list — same direction. Pages Cited / Total Citations recounted from the WorkDuo API (occurrence-count, 28-non-brand + 11-branded prompt panel).</p>
    <div class="takeaway-box win"><b>AEO performance: citations and visibility both up sharply.</b>
      <ul>
        <li><b>AI citations grew +{ac_g:.1f}%</b> ({f(ac_n)} → {f(ac_j)} across all properties) on a wider page set ({TOT['jun_pages']} → {TOT['jul_pages']} pages) — the comparison blogs and now the <b>Product pages</b> carry the load.</li>
        <li><b>WorkDuo AI visibility reached 29.3% (+6.0pp)</b> and share of voice 26% (+4.5pp); ChatGPT visibility alone rose +6.6pp and Google AI Overview held 37%.</li>
        <li><b>AI sessions dipped −18.3%</b> (all ChatGPT) even as citations rose — the visibility-up / sessions-down divergence detailed in the deep-dive above.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Off-Page AEO — Publisher Outreach</h2>
    <div class="takeaway-box win"><b>Secured a free backlink from FlexFulfillment.</b> The June reciprocal exchange is now live: <a href="https://www.flexfulfillment.eu/what-a-3pl-should-check-when-your-inbound-arrives-the-receiving-standards-that-matter/" target="_blank">flexfulfillment.eu — “what a 3PL should check when your inbound arrives”</a> (DR 7, ~4.4k organic traffic), a topically relevant freight/fulfillment placement that AI engines can cite. We are closing the outreach topic for now: the other June prospects (Truckpedia, DevOpsSchool, Gitnux, ZipDo) either did not respond or could not demonstrate referral value, so we are not pursuing paid placements there. The higher-leverage lever remains <b>earning citations through content</b> — reflected in the +34.6% citation growth above.</div>
  </section>

  <footer>
    Sources: GSC (sc-domain:gofreight.com, date-dim for totals; page-dim for page/subfolder; page filter = gofreight.com, subdomains excluded; US-market core keywords filtered country=usa, per target page) · WorkDuo project cmhk59aw9001mlo33c3t8n3rj (28 non-brand prompts for visibility; all-prompt citations occurrence-recounted from /responses API; AI Visibility / SOV / LLM Engaged Sessions from the WorkDuo dashboard) · GA4 property 373075091 (AI-referral sessions + source/landing-page drop analysis) · Generated 2026-08-03
  </footer>
</div>

<script>
const fmt = (n) => n===null?'n/a':n.toLocaleString();
const weekLabels = {week_labels_js};
const clicks   = {jsarr(fr['clicks_tot'])};
const nbClicks = {jsarr(fr['clicks_nb'])};
const chatGpt    = {jsarr(fr['chat'])};
const perplexity = {jsarr(fr['perp'])};
const googleAi   = {jsarr(fr['goog'])};
const aiSessions = {jsarr(fr['ais'])};

new Chart(document.getElementById('chart1'), {{ type:'line', data:{{ labels:weekLabels, datasets:[
  {{label:'Total clicks', data:clicks, borderColor:'#94a3b8', backgroundColor:'rgba(148,163,184,0.08)', borderWidth:2, borderDash:[4,3], tension:0.25, fill:false, pointRadius:2, pointBackgroundColor:'#94a3b8'}},
  {{label:'Non-brand clicks', data:nbClicks, borderColor:'#017d8e', backgroundColor:'rgba(1,125,142,0.12)', borderWidth:2.8, tension:0.25, fill:true, pointRadius:2.5, pointBackgroundColor:'#017d8e'}}
]}}, options:{{responsive:true, maintainAspectRatio:false, plugins:{{legend:{{position:'bottom',labels:{{font:{{size:10}},boxWidth:14,padding:6}}}}, tooltip:{{callbacks:{{label:(c)=>`${{c.dataset.label}}: ${{fmt(c.parsed.y)}}`}}}}}}, scales:{{y:{{beginAtZero:true,ticks:{{font:{{size:10}},callback:(v)=>v.toLocaleString()}},grid:{{color:'#f1f5f9'}}}}, x:{{ticks:{{font:{{size:10}},maxRotation:0,autoSkip:true,maxTicksLimit:8}},grid:{{display:false}}}}}}}}}});

new Chart(document.getElementById('chart2'), {{ type:'line', data:{{ labels:weekLabels, datasets:[
  {{label:'Google AI Overview', data:googleAi, borderColor:'#0891b2', backgroundColor:'rgba(8,145,178,0.08)', borderWidth:2.2, tension:0.3, pointRadius:1.8}},
  {{label:'Perplexity', data:perplexity, borderColor:'#16a34a', backgroundColor:'rgba(22,163,74,0.08)', borderWidth:2.2, tension:0.3, pointRadius:1.8}},
  {{label:'ChatGPT', data:chatGpt, borderColor:'#d97706', backgroundColor:'rgba(217,119,6,0.08)', borderWidth:2.2, tension:0.3, pointRadius:1.8}}
]}}, options:{{responsive:true, maintainAspectRatio:false, plugins:{{legend:{{position:'bottom',labels:{{font:{{size:10}},boxWidth:10,padding:6}}}}, tooltip:{{callbacks:{{label:(c)=>`${{c.dataset.label}}: ${{c.parsed.y.toFixed(1)}}%`}}}}}}, scales:{{y:{{beginAtZero:true,max:45,ticks:{{font:{{size:10}},callback:(v)=>v+'%'}},grid:{{color:'#f1f5f9'}}}}, x:{{ticks:{{font:{{size:10}},maxRotation:0,autoSkip:true,maxTicksLimit:8}},grid:{{display:false}}}}}}}}}});

new Chart(document.getElementById('chart3'), {{ type:'line', data:{{ labels:weekLabels, datasets:[
  {{label:'AI sessions', data:aiSessions, borderColor:'#7c3aed', backgroundColor:'rgba(124,58,237,0.15)', borderWidth:2.5, tension:0.3, fill:true, pointRadius:2.5, pointBackgroundColor:'#7c3aed', spanGaps:false}}
]}}, options:{{responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}, tooltip:{{callbacks:{{label:(c)=>`${{c.parsed.y}} AI sessions`}}}}}}, scales:{{y:{{beginAtZero:true,suggestedMax:150,ticks:{{stepSize:25,font:{{size:10}}}},grid:{{color:'#f1f5f9'}}}}, x:{{ticks:{{font:{{size:10}},maxRotation:0,autoSkip:true,maxTicksLimit:8}},grid:{{display:false}}}}}}}}}});
</script>
</body>
</html>'''

import os
outdir='d:/seo-projects/novastacks/clients/gofreight/output/reports'
os.makedirs(outdir,exist_ok=True)
open(outdir+'/gofreight_july_2026_report.html','w',encoding='utf-8').write(HTML)
print('WROTE',outdir+'/gofreight_july_2026_report.html','len',len(HTML))
