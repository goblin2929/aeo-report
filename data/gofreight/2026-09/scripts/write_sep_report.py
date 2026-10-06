# -*- coding: utf-8 -*-
"""Assemble the September 2026 GoFreight report HTML from frag_sep.pkl."""
import json, pickle
fr = pickle.load(open('/Users/ekiriandra/tmp/sep/frag_sep.pkl','rb'))
def f(n): return f"{round(n):,}"

CL_N,CL_J = fr['CL_JUN'],fr['CL_JUL']
NB_J,NB_N = fr['NB_J'],fr['NB_N']; nbsh_j=fr['nbsh_j']
d_tot=CL_J-CL_N; d_tot_p=d_tot/CL_N*100
d_nb=NB_J-NB_N; d_nb_p=d_nb/NB_N*100
TOT=fr['TOT']
pc_n,pc_j=TOT['jun_total_cit_primary'],TOT['jul_total_cit_primary']
ac_n,ac_j=TOT['jun_total_cit'],TOT['jul_total_cit']; ac_g=(ac_j-ac_n)/ac_n*100

AIS_N,AIS_J=fr['AIS_JUN'],fr['AIS_JUL']; ais_p=(AIS_J-AIS_N)/AIS_N*100
VIS_N,VIS_J=fr['VIS_JUN'],fr['VIS_JUL']
POS_N,POS_J=fr['POS_JUN'],fr['POS_JUL']; CTR_N,CTR_J=fr['CTR_JUN'],fr['CTR_JUL']
nbsh_n=fr['nbsh_n']; imp_p=(fr['IM_JUL']-fr['IM_JUN'])/fr['IM_JUN']*100
cit_p=ac_g
def dcls(v): return 'up' if v>0 else ('down' if v<0 else '')
def sgn(v): return f"{'+' if v>0 else ''}{round(v):,}"
SUB=fr['SUBS']
glo_n,glo_j=SUB['Glossary']; blog_n,blog_j=SUB['Blog']; sol_n,sol_j=SUB['Solutions']
glo_p=(glo_j-glo_n)/glo_n*100; blog_p=(blog_j-blog_n)/blog_n*100
_wk=list(zip(fr['week_labels'],fr['clicks_tot'])); peak_lbl,peak_wk=max(_wk,key=lambda x:x[1])
ais_peak=max(x for x in fr['ais'] if x!='null')
exec(open('/Users/ekiriandra/tmp/sep/aeo_text.py').read())
def jsarr(a): return '['+','.join('null' if x=='null' else f'{x}' for x in a)+']'
week_labels_js='['+','.join(f'"{x}"' for x in fr['week_labels'])+']'

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GoFreight AEO September 2026</title>
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
  .focus-status {{ font-weight:700; font-size:11px; }} .focus-status.done {{ color:var(--green); }} .focus-status.progress {{ color:var(--amber); }}
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
      <h1>AEO Monthly Report: September 2026</h1>
      <div style="font-size:11px; color:var(--slate-5); margin-top:2px;">September vs August 2026 monthly review · GoFreight ↔ Novastacks</div>
    </div>
    <div class="meta">
      <div><strong>October 6, 2026</strong></div>
      <div>Monthly tables: Sep 1 to 30 vs Aug 1 to 31 · Weekly trends: Jan 5 to Sep 21 (last full week)</div>
      <div>GSC filtered to gofreight.com (support / api / archive subdomains excluded)</div>
    </div>
  </header>

  <div class="hook">
    <strong>Headline:</strong> September was GoFreight's best organic month of 2026 so far. Total clicks grew <strong>{d_tot_p:+.1f}% to {f(CL_J)}</strong>, non brand clicks grew <strong>{d_nb_p:+.1f}% to {f(NB_J)}</strong> (now <strong>{nbsh_j:.1f}%</strong> of all clicks), and average position improved from <strong>{POS_N} to {POS_J}</strong> while CTR rose from <strong>{CTR_N:.2f}% to {CTR_J:.2f}%</strong>. AI referred sessions kept climbing, <strong>{f(AIS_N)} to {f(AIS_J)} ({ais_p:+.1f}%)</strong>, led by ChatGPT. {vis_hook} One item to watch: the Best Freight Management Software listicle lost its top 5 Google position on 5 to 6 September (see Core Keyword Tracking).
  </div>

  <div class="kpi-row">
    <div class="kpi"><div class="label">Total Clicks · September</div><div class="val">{f(CL_J)}</div>
      <div class="delta {dcls(d_tot)}">{sgn(d_tot)} ({d_tot_p:+.1f}%) vs August · position {POS_N} to {POS_J}</div></div>
    <div class="kpi"><div class="label">Non Brand Clicks · September</div><div class="val">{f(NB_J)}</div>
      <div class="delta {dcls(d_nb)}">{sgn(d_nb)} ({d_nb_p:+.1f}%) MoM · {nbsh_j:.1f}% of clicks</div></div>
    <div class="kpi"><div class="label">AI Sessions · September (GA4)</div><div class="val">{f(AIS_J)}</div>
      <div class="delta {dcls(AIS_J-AIS_N)}">{ais_p:+.1f}% vs August {f(AIS_N)} · ChatGPT {f(fr['cg_jun'])} to {f(fr['cg_jul'])}</div></div>
    <div class="kpi"><div class="label">AI Visibility · September (WorkDuo)</div><div class="val">{VIS_J:.1f}%</div>
      <div class="delta {dcls(VIS_J-VIS_N)}">{VIS_J-VIS_N:+.1f} pts vs August · citations {cit_p:+.1f}% ({f(ac_n)} to {f(ac_j)})</div></div>
  </div>

  <div class="chart-row">
    <div class="chart-card">
      <h3>① Total Clicks vs Non Brand Clicks (Weekly)</h3>
      <div class="sub">GSC gofreight.com, date dimension · non brand = total minus brand regex queries</div>
      <div class="chart-canvas-wrap"><canvas id="chart1"></canvas></div>
      <div class="takeaway"><b>Read:</b> Weekly clicks passed 2,000 for the first time in September and peaked at <b>{f(peak_wk)} in the week of {peak_lbl}</b>. Non brand clicks reached <b>{f(NB_J)} ({d_nb_p:+.1f}% MoM)</b> and <b>{nbsh_j:.1f}%</b> of all clicks, up from {nbsh_n:.1f}% in August. Impressions were flat ({imp_p:+.1f}%), so the growth came from better positions and a higher CTR on the same demand.</div>
    </div>
    <div class="chart-card">
      <h3>② AEO Visibility · Non Brand by Engine (Weekly)</h3>
      <div class="sub">WorkDuo · 28 non brand prompts (MOFU/TOFU/BOFU); self mention rate per engine</div>
      <div class="chart-canvas-wrap"><canvas id="chart2"></canvas></div>
      <div class="takeaway"><b>Read:</b> {vis_read}</div>
    </div>
    <div class="chart-card">
      <h3>③ AI Traffic Sessions (Weekly · GA4)</h3>
      <div class="sub">GA4 property 373075091, sessionSource matching AI platforms (chatgpt, perplexity, gemini, claude, copilot)</div>
      <div class="chart-canvas-wrap"><canvas id="chart3"></canvas></div>
      <div class="takeaway"><b>Read:</b> AI sessions reached <b>{f(AIS_J)} in September ({ais_p:+.1f}%)</b>, a new monthly high, with the best week at <b>{f(ais_peak)}</b>. <b>ChatGPT added {sgn(fr['cg_jul']-fr['cg_jun'])} sessions ({f(fr['cg_jun'])} to {f(fr['cg_jul'])})</b> and Perplexity and Copilot grew, while Gemini and Claude sent fewer visits (see the deep dive below).</div>
    </div>
  </div>

  <div class="two-col">
    <section>
      <h2>September: What Was Done</h2>
      <table class="t">
        <thead><tr><th>#</th><th>Initiative</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td colspan="3" style="background:var(--slate-1);font-weight:700;color:var(--teal-d);">Related SEO topics</td></tr>
          <tr><td class="num">1</td><td><b>Improving the Solution &amp; Product pages</b>: GoFreight Solutions &amp; Product Pages: H2 and FAQ Rewrite (31 Aug 2026) across the 14 live solution and product pages. The new copy is still being verified before it goes live.</td><td><span class="focus-status progress">IN PROGRESS</span></td></tr>
          <tr><td class="num">2</td><td><b>Implemented IndexNow for GoFreight</b>: the key file is live at gofreight.com, and new or updated URLs from the content delivery tracker are submitted to Bing and other IndexNow engines on publish (first batch of 16 URLs accepted on 14 Sep). Impact: TBA.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td colspan="3" style="background:var(--slate-1);font-weight:700;color:var(--teal-d);">Related SEM topics</td></tr>
          <tr><td class="num">3</td><td><b>Built three new SEM landing pages in HubSpot.</b></td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">4</td><td><b>SEM landing page optimisation</b>: new versions for all three campaigns.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">5</td><td><b>Audited the Google Ads conversion actions</b> with RevOps (Bruce).</td><td><span class="focus-status done">DONE</span></td></tr>
        </tbody>
      </table>
      <div class="takeaway-box" style="margin-top:10px;"><b>Effect visible in the data:</b> Glossary clicks {glo_p:+.1f}% and Blog {blog_p:+.1f}% MoM; Solutions pages {f(sol_n)} to {f(sol_j)} clicks; non brand share climbed {nbsh_n:.1f}% to {nbsh_j:.1f}%; AI referred sessions {ais_p:+.1f}% ({f(AIS_N)} to {f(AIS_J)}).</div>
    </section>

    <section>
      <h2>October 2026: Next Action Items &amp; Priorities</h2>
      <ol class="prio-list">
        <li><b>[SEO] Implement the new content for the Solution &amp; Product pages</b>: publish the approved H2 and FAQ rewrite across the 14 solution and product pages once verification is complete.<span class="tag product">Product</span><span class="tag aeo">AEO</span></li>
      </ol>
      <div class="takeaway-box" style="margin-top:12px;"><b>Why this matters for AI visibility:</b> for software selection prompts, AI assistants lean on a vendor's own solution pages. In the last 30 days, ChatGPT used a GoFreight page as a source in 159 answers without naming GoFreight, while it named Descartes 40 times and CargoWise 32 times in those same answers. Most of Descartes' citations land on its /solutions/ pages; most of GoFreight's land on blog posts. Stronger solution and product pages give assistants a GoFreight claim they can repeat.</div>
      <div class="takeaway-box watch" style="margin-top:8px;"><b>Watch:</b> the <a href="https://gofreight.com/blog/best-freight-management-software" target="_blank">Best Freight Management Software</a> listicle lost its top 5 position for “freight management software” on 5 to 6 September: its average US position went from 3.1 in August to 15.8 in September, and Google now ranks the homepage for that group of keywords instead. The page is live and Google can still index it; the cause is still open and we are tracking it.</div>
    </section>
  </div>

  <section>
    <h2>Query Segment Breakdown (September vs August)</h2>
    <table class="t"><thead>
      <tr><th>Segment</th><th class="num">August Clicks</th><th class="num">September Clicks</th><th class="num">Click Δ</th><th class="num">Δ %</th><th class="num">August Impr</th><th class="num">September Impr</th><th class="num">Impr Δ</th></tr>
    </thead><tbody>
      {fr['seg']}
    </tbody></table>
    <div class="takeaway-box"><b>Read:</b> Non-branded grew <b>+{d_nb_p:.1f}% MoM (+{f(d_nb)})</b> while branded held roughly flat — so the content program keeps doing the work. Non branded now stands at <b>{nbsh_j:.1f}% of all clicks</b>, up from {nbsh_n:.1f}% in August. Brand rows are measured on the full property (query-dim); non-brand is derived as total minus brand.</div>
  </section>

  <section>
    <h2>Subfolder Performance (September vs August), with AI Citation Coverage</h2>
    <table class="t"><thead>
      <tr><th>Subfolder</th><th class="num">August Clicks</th><th class="num">September Clicks</th><th class="num">Click Δ</th><th class="num">Δ %</th><th class="num">August Impr</th><th class="num">September Impr</th><th class="num aeo">Pages Cited · August</th><th class="num aeo">Pages Cited · September</th></tr>
    </thead><tbody>
      {fr['sub']}
    </tbody></table>
    <p class="note">Totals reflect the primary gofreight.com property (support / api / archive subdomains excluded per the filter). <b>Pages Cited by AI</b> = distinct pages cited as a source by ChatGPT, Perplexity, or Google AI in WorkDuo-tracked responses that month, shown as <i>pages (total citations)</i>.</p>
    <div class="takeaway-box"><b>Read:</b> <b>Glossary grew {glo_p:+.1f}%</b> (clicks {f(glo_n)} to {f(glo_j)}) and is now the largest subfolder by clicks, ahead of Blog ({blog_p:+.1f}%, {f(blog_n)} to {f(blog_j)}). Last month's terminal tracking finding held: <a href="https://gofreight.com/glossary/garden-city-terminal-tracking" target="_blank">/glossary/garden-city-terminal-tracking</a> grew again to 1,594 clicks, and /glossary/what-is-incoterms almost doubled (343 to 676). Solutions pages doubled on a small base ({f(sol_n)} to {f(sol_j)}); Product was flat and Pricing eased on a small base (46 to 39).</div>
  </section>

  <section>
    <h2>Top 30 Pages by Clicks (September vs August), with AI Citations per Page</h2>
    <table class="t"><thead>
      <tr><th>#</th><th>Page</th><th>NovaStacks Work</th><th class="num">August Clicks</th><th class="num">September Clicks</th><th class="num">Δ Clicks</th><th class="num">September Impr</th><th class="num aeo">AI Citations · August</th><th class="num aeo">AI Citations · September</th></tr>
    </thead><tbody>
      {fr['top30']}
    </tbody></table>
    <p class="note"><b>NovaStacks Work</b> flags each blog / glossary page from the content-delivery tracker: <span style="background:#eafaf0;color:#15803d;padding:1px 5px;border-radius:4px;font-size:11px;font-weight:600">🆕 NS · Created</span> = a new NovaStacks article (month it went live), <span style="background:#e6f4f1;color:#0f766e;padding:1px 5px;border-radius:4px;font-size:11px;font-weight:600">🔄 NS · Updated</span> = an existing page NovaStacks last refreshed (latest update month; hover for the exact date). Pages with no flag are legacy GoFreight content NovaStacks has not touched. <b>AI Citations</b> = WorkDuo-tracked AI responses citing this page as a source in the month.</p>
  </section>

  <section>
    <h2>Top 15 Most Cited Pages by AI: A Different List Than the Click Winners</h2>
    <table class="t"><thead>
      <tr><th>#</th><th>Page</th><th>NovaStacks Work</th><th class="num aeo">AI Citations · August</th><th class="num aeo">AI Citations · September</th><th class="num">Δ</th><th class="num">September Clicks</th><th class="num">In Click Top 30?</th></tr>
    </thead><tbody>
      {fr['top15']}
    </tbody></table>
    {top15_read}
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
    <h2>AI Traffic Deep Dive: ChatGPT Drives a New High</h2>
    <p class="note" style="margin-bottom:8px;">AI referred sessions rose from {f(AIS_N)} (August) to {f(AIS_J)} (September), <b>{ais_p:+.1f}%</b>. This section isolates <b>which engines and which pages</b> moved. The source table sums sessions per AI source, so its total can differ by a session or two from the monthly total.</p>
    <div class="two-col" style="align-items:start;">
      <div>
        <table class="t"><thead>
          <tr><th>AI Source</th><th class="num">August</th><th class="num">September</th><th class="num">Δ</th></tr>
        </thead><tbody>
          {fr['src']}
        </tbody></table>
        <div class="takeaway-box win" style="margin-top:8px;"><b>ChatGPT carried the month.</b> ChatGPT sessions grew <b>{f(fr['cg_jun'])} to {f(fr['cg_jul'])} ({sgn(fr['cg_drop'])})</b> and now make up <b>{fr['cg_share_jul']}%</b> of AI referred sessions, up from {fr['cg_share_jun']}%. Perplexity and Copilot also grew. Gemini and Claude sent fewer visits than in August, so the net gain is smaller than the ChatGPT gain alone.</div>
      </div>
      <div>
        <table class="t"><thead>
          <tr><th>ChatGPT landing pages that gained sessions</th><th class="num">August</th><th class="num">September</th><th class="num">Δ</th></tr>
        </thead><tbody>
          {fr['lp_gain']}
        </tbody></table>
      </div>
    </div>
    <div class="takeaway-box" style="margin-top:10px;"><b>Where the new AI visits land:</b> beyond the homepage, ChatGPT sent new visits to commercial and product pages such as <a href="https://gofreight.com/blog/best-tms-software" target="_blank">/blog/best-tms-software</a> and <a href="https://gofreight.com/product/shipment-tracking-operations" target="_blank">/product/shipment-tracking-operations</a>, plus glossary pages such as <a href="https://gofreight.com/glossary/ocean-carrier-alliances" target="_blank">/glossary/ocean-carrier-alliances</a>. A product page earning AI referrals supports the October focus on the solution and product pages.</div>
  </section>

  <section>
    <h2>AEO Metrics — Month over Month</h2>
    <table class="t"><thead>
      <tr><th>Metric</th><th class="num">August 2026</th><th class="num">September 2026</th><th class="num">Change</th><th>Source</th></tr>
    </thead><tbody>
      {fr['aeo']}
    </tbody></table>
    <p class="note">AI Platform Sessions from GA4 direct (property 373075091). AI Visibility (non brand) from the WorkDuo API. Pages Cited / Total Citations recounted from the WorkDuo API (occurrence count, 28 non brand + 11 branded prompt panel, project cmhk59aw9001mlo33c3t8n3rj).</p>
    {aeo_box}
  </section>

  <footer>
    Sources: GSC (sc-domain:gofreight.com, date-dim for totals; page-dim for page/subfolder; page filter = gofreight.com, subdomains excluded; US market core keywords filtered country=usa, per target page) · WorkDuo project cmhk59aw9001mlo33c3t8n3rj (28 non-brand prompts for visibility; all prompt citations occurrence-recounted from /responses API) · GA4 property 373075091 (AI-referral sessions + source/landing-page analysis) · Generated 2026-10-06
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
  {{label:'Non brand clicks', data:nbClicks, borderColor:'#017d8e', backgroundColor:'rgba(1,125,142,0.12)', borderWidth:2.8, tension:0.25, fill:true, pointRadius:2.5, pointBackgroundColor:'#017d8e'}}
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
outdir='/Users/ekiriandra/seo-projects/novastacks/clients/gofreight/output/reports'
os.makedirs(outdir,exist_ok=True)
open(outdir+'/gofreight_september_2026_report.html','w',encoding='utf-8').write(HTML)
print('WROTE',outdir+'/gofreight_september_2026_report.html','len',len(HTML))
