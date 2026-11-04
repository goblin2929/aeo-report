# -*- coding: utf-8 -*-
"""Assemble the September 2026 GoFreight report HTML from frag_oct.pkl."""
import json, pickle
fr = pickle.load(open('/Users/ekiriandra/tmp/sep/frag_oct.pkl','rb'))
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
PCD=json.load(open('/Users/ekiriandra/tmp/oct/gf-page-clicks-oct.json'))
GC='https://gofreight.com/glossary/garden-city-terminal-tracking'; SV='https://gofreight.com/glossary/savannah-terminal-tracking'
gc_n,gc_j=PCD[GC]['jun'],PCD[GC]['jul']; sv_n,sv_j=PCD[SV]['jun'],PCD[SV]['jul']
sav_n,sav_j=gc_n+sv_n,gc_j+sv_j
rest_n,rest_j=CL_N-sav_n,CL_J-sav_j; rest_p=(rest_j-rest_n)/rest_n*100
brand_n,brand_j=CL_N-NB_N,CL_J-NB_J; br_p=(brand_j-brand_n)/brand_n*100
last_wk=fr['clicks_tot'][-1]
_SB=json.load(open('/Users/ekiriandra/tmp/oct/gf_savannah_brand_split.json'))
_snb=lambda m:sum(v['clicks']-v['brand'] for v in _SB[m].values())
nbx_n,nbx_j=NB_N-_snb('sep'),NB_J-_snb('oct'); nbx_p=(nbx_j-nbx_n)/nbx_n*100
_CD=json.load(open('/Users/ekiriandra/tmp/oct/ga4_chatgpt_direct_daily.json'))['chatgpt_daily']
def _avg(a,b,n): return sum(v for k,v in _CD.items() if a<=k<=b)/n
cg_short=(_avg('20261001','20261007',7)-_avg('20261008','20261015',8))*8
cg_pre,cg_gap,cg_post=_avg('20260924','20261007',14),_avg('20261009','20261014',6),_avg('20261016','20261029',14)
_DR=json.load(open('/Users/ekiriandra/tmp/oct/ga4-ai-drop.json'))
gem_n=sum(x['jun'] for x in _DR['sources'] if 'gemini' in x['source']); gem_j=sum(x['jul'] for x in _DR['sources'] if 'gemini' in x['source'])
def dcls(v): return 'up' if v>0 else ('down' if v<0 else '')
def sgn(v): return f"{'+' if v>0 else ''}{round(v):,}"
SUB=fr['SUBS']
glo_n,glo_j=SUB['Glossary']; blog_n,blog_j=SUB['Blog']; sol_n,sol_j=SUB['Solutions']
glo_p=(glo_j-glo_n)/glo_n*100; blog_p=(blog_j-blog_n)/blog_n*100
home_n,home_j=SUB['Homepage']; home_p=(home_j-home_n)/home_n*100
_wk=list(zip(fr['week_labels'],fr['clicks_tot'])); peak_lbl,peak_wk=max(_wk,key=lambda x:x[1])
ais_peak=max(x for x in fr['ais'] if x!='null')
exec(open('/Users/ekiriandra/tmp/oct/aeo_text.py').read())
_MN={'08':'Aug','09':'Sep','10':'Oct'}
def wlab(w): return f"{_MN[w[5:7]]} {int(w[8:])}"
def jsarr(a): return '['+','.join('null' if x=='null' else f'{x}' for x in a)+']'
week_labels_js='['+','.join(f'"{x}"' for x in fr['week_labels'])+']'

GA=json.load(open('/Users/ekiriandra/tmp/oct/gsc_genai.json'))
_gm=GA['monthly']
def _gaicell(k): return _gm[k]
ga_s,ga_o=_gm['2026-09']['ai'],_gm['2026-10']['ai']; gt_s,gt_o=_gm['2026-09']['all'],_gm['2026-10']['all']
ga_p=(ga_o-ga_s)/ga_s*100; gn_s,gn_o=gt_s-ga_s,gt_o-ga_o; gn_p=(gn_o-gn_s)/gn_s*100; gt_p=(gt_o-gt_s)/gt_s*100
gsh_s,gsh_o=ga_s/gt_s*100,ga_o/gt_o*100; ga_share_of_growth=(ga_o-ga_s)/(gt_o-gt_s)*100
def _row(label,key,fmt):
    a,b,c=[fmt(_gm[k]) for k in ('2026-08','2026-09','2026-10')]
    return a,b,c
ga_rows=[]
for label,fn,pct in [('Impressions in generative AI features',lambda k:_gm[k]['ai'],True),('Impressions outside AI features',lambda k:_gm[k]['all']-_gm[k]['ai'],True),('All web impressions',lambda k:_gm[k]['all'],True)]:
    v=[fn(k) for k in ('2026-08','2026-09','2026-10')]; d=(v[2]-v[1])/v[1]*100
    ga_rows.append(f'<tr><td>{label}</td><td class="num">{f(v[0])}</td><td class="num">{f(v[1])}</td><td class="num">{f(v[2])}</td><td class="num {dcls(d)}">{d:+.1f}%</td></tr>')
_sh=[_gm[k]['ai']/_gm[k]['all']*100 for k in ('2026-08','2026-09','2026-10')]
ga_rows.append(f'<tr class="subtotal"><td>AI features share of impressions</td><td class="num">{_sh[0]:.1f}%</td><td class="num">{_sh[1]:.1f}%</td><td class="num">{_sh[2]:.1f}%</td><td class="num">{_sh[2]-_sh[1]:+.1f} pts</td></tr>')
ga_rows='\n'.join(ga_rows)
def _short(u):
    p=u.replace('https://gofreight.com','') or '/'
    return 'gofreight.com/ (homepage)' if p=='/' else (p if len(p)<=60 else p[:58]+'…')
ga_top='\n'.join(f'<tr><td><a href="{x["url"]}" target="_blank">{_short(x["url"])}</a></td><td class="num">{f(x["ai"])}</td><td class="num">{f(x["all"])}</td><td class="num">{x["ai"]/x["all"]*100:.0f}%</td></tr>' for x in GA['top_pages_3mo'][:8])
_CP=GA['compare_pages']; _PG=json.load(open('/Users/ekiriandra/tmp/oct/gf_pages_country_sep_oct.json'))
INC6=['https://gofreight.com/blog/education/buyer-pays-freight-costs-unraveling-fca-incoterms','https://gofreight.com/blog/industry-insights/mastering-fob-in-shipping-a-complete-guide.html','https://gofreight.com/glossary/fob-shipping-point-vs-fob-destination','https://gofreight.com/blog/education/understanding-exw-meaning-in-international-trade','https://gofreight.com/blog/education/understanding-ex-works-in-international-trade.html','https://gofreight.com/glossary/what-is-incoterms']
inc_s=sum(_CP[u]['sep'] for u in INC6); inc_o=sum(_CP[u]['oct'] for u in INC6)
cp_ts=sum(v['sep'] for v in _CP.values()); cp_to=sum(v['oct'] for v in _CP.values()); inc_share=(inc_o-inc_s)/(cp_to-cp_ts)*100
_US=GA['compare_countries']['United States']; us_s,us_o=_US['sep'],_US['oct']; us_p=(us_o-us_s)/us_s*100
_ris=sorted(_CP.items(),key=lambda x:-(x[1]['oct']-x[1]['sep']))[:10]
def _clk(u,m): return _PG[m]['pages'].get(u,[0])[0]
ga_rise='\n'.join(f'<tr><td><a href="{u}" target="_blank">{_short(u)}</a></td><td class="num">{f(v["sep"])}</td><td class="num">{f(v["oct"])}</td><td class="num up">+{f(v["oct"]-v["sep"])}</td><td class="num">{f(_clk(u,"sep"))} → {f(_clk(u,"oct"))}</td></tr>' for u,v in _ris)
_gw=GA['weekly']; ga_wl='['+','.join(f'"{wlab(w)}"' for w in _gw)+']'
ga_wai='['+','.join(str(v['ai']) for v in _gw.values())+']'; ga_wother='['+','.join(str(v['all']-v['ai']) for v in _gw.values())+']'
HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GoFreight AEO October 2026</title>
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
      <h1>AEO Monthly Report: October 2026</h1>
      <div style="font-size:11px; color:var(--slate-5); margin-top:2px;">October vs September 2026 monthly review · GoFreight ↔ Novastacks</div>
    </div>
    <div class="meta">
      <div><strong>November 3, 2026</strong></div>
      <div>Monthly tables: Oct 1 to 31 vs Sep 1 to 30 · Weekly trends: Jan 5 to Oct 26 (last full week)</div>
      <div>GSC filtered to gofreight.com (support / api / archive subdomains excluded)</div>
    </div>
  </header>

  <div class="hook">
    <strong>Headline:</strong> October clicks fell <strong>{d_tot_p:+.1f}% to {f(CL_J)}</strong>, and the change sits on two pages, and it is not a loss of ranking. Our two Savannah terminal tracking glossary pages <strong>kept a strong position (around 5 to 6)</strong>, but Google now shows the Georgia Ports Authority page and an AI Overview above them, so searchers get the answer before they reach our result and clicks fell from <strong>{f(sav_n)} to {f(sav_j)}</strong>. <strong>Every other page combined grew {rest_p:+.1f}% ({f(rest_n)} to {f(rest_j)})</strong>, with the Blog up <strong>{blog_p:+.1f}%</strong> on the Incoterm guides. Impressions rose <strong>{imp_p:+.1f}%</strong>, and about <strong>{ga_share_of_growth:.0f}% of the new impressions came from Google's generative AI features</strong> ({f(ga_s)} to {f(ga_o)}, {ga_p:+.1f}%), where searchers often read the answer without clicking, so CTR fell from {CTR_N:.2f}% to {CTR_J:.2f}%. {vis_hook} AI referred sessions eased to <strong>{f(AIS_J)} ({ais_p:+.1f}%)</strong>, partly because of a tracking gap: from 8 to 15 October a ChatGPT bug (confirmed by OpenAI) removed the source tag from its links, so analytics could not attribute those visits to ChatGPT, while Gemini almost doubled. All 30 October refreshes are live, the Solution and Product page rewrite is done, and the homepage climbed for the freight management keywords (“freight management software” 12.2 → 4.8).
  </div>

  <div class="kpi-row">
    <div class="kpi"><div class="label">Total Clicks · October</div><div class="val">{f(CL_J)}</div>
      <div class="delta {dcls(d_tot)}">{sgn(d_tot)} ({d_tot_p:+.1f}%) vs September</div>
      <div class="delta up" style="font-weight:600;">excl. Savannah pages {rest_p:+.1f}% ({f(rest_n)} to {f(rest_j)})</div></div>
    <div class="kpi"><div class="label">Non Brand Clicks · October</div><div class="val">{f(NB_J)}</div>
      <div class="delta {dcls(d_nb)}">{sgn(d_nb)} ({d_nb_p:+.1f}%) MoM · {nbsh_j:.1f}% of clicks</div>
      <div class="delta up" style="font-weight:600;">excl. Savannah pages {nbx_p:+.1f}% ({f(nbx_n)} to {f(nbx_j)})</div></div>
    <div class="kpi"><div class="label">AI Sessions · October (GA4)</div><div class="val">{f(AIS_J)}</div>
      <div class="delta {dcls(AIS_J-AIS_N)}">{ais_p:+.1f}% vs September {f(AIS_N)} · ChatGPT {f(fr['cg_jun'])} to {f(fr['cg_jul'])}</div></div>
    <div class="kpi"><div class="label">AI Visibility · October (WorkDuo)</div><div class="val">{VIS_J:.1f}%</div>
      <div class="delta {dcls(VIS_J-VIS_N)}">{VIS_J-VIS_N:+.1f} pts vs September · citations {cit_p:+.1f}% ({f(ac_n)} to {f(ac_j)})</div></div>
  </div>

  <div class="chart-row">
    <div class="chart-card">
      <h3>① Total Clicks vs Non Brand Clicks (Weekly)</h3>
      <div class="sub">GSC gofreight.com, date dimension · non brand = total minus brand regex queries</div>
      <div class="chart-canvas-wrap"><canvas id="chart1"></canvas></div>
      <div class="takeaway"><b>Read:</b> Weekly clicks fell from about 2,100 in September to <b>1,793 in the week of Oct 5</b>, when clicks on our Savannah terminal pages fell (the Georgia Ports Authority page and an AI Overview now show above them), then recovered every week to <b>{f(last_wk)} in the week of Oct 26</b>. Non brand clicks were <b>{f(NB_J)} ({d_nb_p:+.1f}% MoM)</b>, still <b>{nbsh_j:.1f}%</b> of all clicks. Impressions grew {imp_p:+.1f}%, mostly inside Google's AI features (see the Generative AI section), which earn fewer clicks per impression.</div>
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
      <div class="takeaway"><b>Read:</b> AI sessions were <b>{f(AIS_J)} in October ({ais_p:+.1f}%)</b>, the second highest month of 2026 after September. Recorded ChatGPT sessions fell {f(fr['cg_jun'])} to {f(fr['cg_jul'])}; about {f(cg_short)} of those sessions fall in the 8 to 15 Oct window when a ChatGPT bug removed the tracking tag from its links, while <b>Gemini rose {f(gem_n)} to {f(gem_j)}</b> (see the deep dive below).</div>
    </div>
  </div>

  <div class="two-col">
    <section>
      <h2>October: What Was Done</h2>
      <table class="t">
        <thead><tr><th>#</th><th>Initiative</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td colspan="3" style="background:var(--slate-1);font-weight:700;color:var(--teal-d);">Related SEO topics</td></tr>
          <tr><td class="num">1</td><td><b>October content batch: 30 of 30 refreshes published</b> (14 Oct: 15 pages, 19 Oct: 14 pages, 28 Oct: the 5 data analytics tools guide). The batch covers the commercial comparison pages (best freight management software, best TMS software, Descartes alternatives, GoFreight vs Descartes, CargoWise pricing), the terminal tracking glossary pages and the customs guides. Every URL was submitted to IndexNow on publish.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">2</td><td><b>Solution &amp; Product pages: H2 and FAQ optimization</b> across the 14 solution and product pages, with GoFreight's final comments applied.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">3</td><td><b>Site fixes delivered (14 Oct)</b>: restored the ocean freight transit times post (it held the CFR article by mistake), a CFR refresh for its own glossary page, the Catapult product name corrected on three Magaya and CargoWise comparison blogs, and the ITS terminal staging duplicate flagged for removal.</td><td><span class="focus-status done">DONE</span></td></tr>
          <tr><td class="num">4</td><td><b>Homepage redesign check (29 Oct)</b>: compared the new homepage with the old one for the core keywords. The new page drops the visible FAQ and most keyword copy; positions are checked again in mid November.</td><td><span class="focus-status done">DONE</span></td></tr>
        </tbody>
      </table>
      <div class="takeaway-box" style="margin-top:10px;"><b>Effect visible in the data:</b> Blog clicks {blog_p:+.1f}% ({f(blog_n)} to {f(blog_j)}), led by the Incoterm guides; pages outside the two Savannah terminal pages {rest_p:+.1f}% in clicks; homepage up for the freight management cluster (see Core Keyword Tracking).</div>
    </section>

    <section>
      <h2>November 2026: Next Action Items &amp; Priorities</h2>
      <ol class="prio-list">
        <li><b>[Content] Create the 2027 technology report</b>: target publication in mid December 2026.<span class="tag content">Content</span><span class="tag aeo">AEO</span></li>
        <li><b>[AEO] Outreach to the sources that name competitors but not GoFreight</b>: in Google AI Overview answers from 26 Oct to 4 Nov, several third party pages are cited next to CargoWise, Magaya or Descartes without GoFreight. The first 10 priority domains are listed with outreach emails ready, and GoFreight's G2 and GetApp profiles are the directories AI Overview now cites for customer portal questions.<span class="tag aeo">AEO</span></li>
        <li><b>[Content] Refresh the blogs that AI answers stopped citing</b>, mostly the Best TMS and Best NVOCC topics. In Google AI Overview (6 to 19 Oct vs 26 Oct to 4 Nov) <a href="https://gofreight.com/blog/nvocc-software-top-solutions" target="_blank">NVOCC software top solutions</a> went from 10 citations to 0 for the NVOCC TMS question, and the TMS questions on scaling, pricing and implementation cite GoFreight less. Seven pages are in the November plan (#17 to #23), including <a href="https://gofreight.com/blog/best-logistics-crm-software" target="_blank">best logistics CRM software</a>, <a href="https://gofreight.com/blog/tms-software-guide" target="_blank">TMS software guide</a> and <a href="https://gofreight.com/blog/transparent-freight-software-pricing" target="_blank">transparent freight software pricing</a>.<span class="tag content">Content</span><span class="tag aeo">AEO</span></li>
        <li><b>[Content] November batch</b>: 13 refreshes already delivered, the rest in production, including the product page specification tables moved from October.<span class="tag content">Content</span></li>
        <li><b>[Technical] Homepage after the redesign</b>: check the homepage keyword positions again (12 to 26 Nov) and align the FAQ markup with the visible page.<span class="tag technical">Technical</span></li>
      </ol>
      <div class="takeaway-box" style="margin-top:8px;"><b>Savannah terminal pages: visibility kept, clicks taken above us.</b> <a href="https://gofreight.com/glossary/garden-city-terminal-tracking" target="_blank">/glossary/garden-city-terminal-tracking</a> ({f(gc_n)} to {f(gc_j)} clicks) and <a href="https://gofreight.com/glossary/savannah-terminal-tracking" target="_blank">/glossary/savannah-terminal-tracking</a> ({f(sv_n)} to {f(sv_j)}) still rank around positions 5 to 6. What changed is the results page: the Georgia Ports Authority page and an AI Overview now appear before our result, and they answer the terminal question directly.</div>
    </section>
  </div>

  <section>
    <h2>Query Segment Breakdown (October vs September)</h2>
    <table class="t"><thead>
      <tr><th>Segment</th><th class="num">September Clicks</th><th class="num">October Clicks</th><th class="num">Click Δ</th><th class="num">Δ %</th><th class="num">September Impr</th><th class="num">October Impr</th><th class="num">Impr Δ</th></tr>
    </thead><tbody>
      {fr['seg']}
    </tbody></table>
    <div class="takeaway-box"><b>Read:</b> Non branded clicks fell <b>{d_nb_p:+.1f}% ({sgn(d_nb)})</b>, and the two Savannah terminal pages account for {f(sav_n-sav_j)} fewer clicks, more than the whole non brand decline. Those pages kept their position; the clicks went to the Georgia Ports Authority page and the AI Overview shown above them. Branded clicks eased {br_p:+.1f}% ({f(brand_n)} to {f(brand_j)}). Non branded is still <b>{nbsh_j:.1f}% of all clicks</b>. Brand rows are measured on the full property (query dimension); non brand is derived as total minus brand.</div>
  </section>

  <section>
    <h2>Google Generative AI Features: Where the New Impressions Came From</h2>
    <div class="two-col" style="align-items:start;">
      <div>
        <table class="t"><thead>
          <tr><th>Google Search Console (web)</th><th class="num">August</th><th class="num">September</th><th class="num">October</th><th class="num">Δ % Sep → Oct</th></tr>
        </thead><tbody>
          {ga_rows}
        </tbody></table>
        <p class="note">Google Search Console export, Performance filtered to generative AI features vs all web results, gofreight.com property, date basis (August = Aug 2 to 31, as exported). These totals are date based, so they sit slightly below the page based impression totals in the other tables.</p>
        <div class="takeaway-box"><b>Read:</b> Impressions in Google's generative AI features grew <b>{ga_p:+.1f}%</b> ({f(ga_s)} to {f(ga_o)}) and now make up <b>{gsh_o:.1f}%</b> of all GoFreight impressions, up from {gsh_s:.1f}% in September and {_sh[0]:.1f}% in August. Impressions outside the AI features grew only {gn_p:+.1f}%. So about <b>{ga_share_of_growth:.0f}% of October's new impressions</b> were GoFreight pages shown inside AI answers, where a searcher often reads the answer without clicking. This is the main reason CTR fell while GoFreight's content was shown more often.</div>
      </div>
      <div>
        <div class="chart-card" style="padding:10px 12px;">
          <h3>Weekly impressions: inside vs outside AI features</h3>
          <div class="sub">GSC export, weeks Aug 3 to Oct 26</div>
          <div class="chart-canvas-wrap" style="height:180px;"><canvas id="chart4"></canvas></div>
        </div>
      </div>
    </div>
    <h3 style="margin-top:14px;font-size:12.5px;">Rising pages: biggest gains in AI feature impressions, October vs September</h3>
    <table class="t"><thead>
      <tr><th>Page</th><th class="num">AI feature impr · September</th><th class="num">AI feature impr · October</th><th class="num">Δ</th><th class="num">Clicks Sep → Oct (all search)</th></tr>
    </thead><tbody>
      {ga_rise}
    </tbody></table>
    <p class="note">Page level figures from the Search Console comparison export (Oct 1 to 31 vs Sep 1 to 30, generative AI features); page totals run slightly above the date based totals in the table above. Clicks are from all Google web search for the same page.</p>
    <div class="takeaway-box win"><b>What the rising pages tell us:</b>
      <ul>
        <li><b>The Incoterm guides lead.</b> Six Incoterm pages (FCA, FOB, FOB shipping point vs destination, the two EXW guides and the Incoterms overview) went from {f(inc_s)} to {f(inc_o)} AI feature impressions, about <b>{inc_share:.0f}% of the growth</b>. Their clicks grew too (FCA 159 to 383, FOB 162 to 229, EXW 97 to 210), so being shown inside AI answers did not cost these pages traffic.</li>
        <li><b>October refreshes are picked up.</b> Pages refreshed in October rose inside the AI features: <a href="https://gofreight.com/blog/customs-clearance-timeline" target="_blank">customs clearance timeline</a> (4,559 to 12,159), <a href="https://gofreight.com/blog/general/what-is-freight-forwarding-and-how-does-it-work.html" target="_blank">what is freight forwarding</a> (5,027 to 8,646), <a href="https://gofreight.com/glossary/its-terminal-tracking" target="_blank">ITS terminal tracking</a> (1,559 to 4,567) and <a href="https://gofreight.com/blog/customs-duty-import-tax-guide" target="_blank">customs duty guide</a> (3,825 to 6,339).</li>
        <li><b>The homepage</b> also appeared more often in AI features (8,395 to 13,050).</li>
        <li><b>The US grew {us_p:+.1f}%</b> in AI feature impressions ({f(us_s)} to {f(us_o)}), so the growth is not only international.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Subfolder Performance (October vs September), with AI Citation Coverage</h2>
    <table class="t"><thead>
      <tr><th>Subfolder</th><th class="num">September Clicks</th><th class="num">October Clicks</th><th class="num">Click Δ</th><th class="num">Δ %</th><th class="num">September Impr</th><th class="num">October Impr</th><th class="num aeo">Pages Cited · September</th><th class="num aeo">Pages Cited · October</th></tr>
    </thead><tbody>
      {fr['sub']}
    </tbody></table>
    <p class="note">Totals reflect the primary gofreight.com property (support / api / archive subdomains excluded per the filter). <b>Pages Cited by AI</b> = distinct pages cited as a source by ChatGPT, Perplexity, or Google AI in WorkDuo-tracked responses that month, shown as <i>pages (total citations)</i>.</p>
    <div class="takeaway-box"><b>Read:</b> <b>Blog grew {blog_p:+.1f}%</b> ({f(blog_n)} to {f(blog_j)}) and is again the largest subfolder. The Incoterm guides led: <a href="https://gofreight.com/blog/education/buyer-pays-freight-costs-unraveling-fca-incoterms" target="_blank">FCA Incoterms</a> 159 to 383 clicks, <a href="https://gofreight.com/blog/industry-insights/mastering-fob-in-shipping-a-complete-guide.html" target="_blank">FOB in shipping</a> 162 to 229 and the two EXW guides 97 to 210. <b>Glossary fell {glo_p:+.1f}%</b> ({f(glo_n)} to {f(glo_j)}): the two Savannah terminal pages still rank around positions 5 to 6 but received {f(sav_n-sav_j)} fewer clicks because the Georgia Ports Authority page and an AI Overview now sit above them, while other terminal pages grew (<a href="https://gofreight.com/glossary/its-terminal-tracking" target="_blank">ITS</a> 201 to 243, <a href="https://gofreight.com/glossary/everport-terminal-tracking" target="_blank">Everport</a> 22 to 75). The homepage eased {home_p:+.1f}% ({f(home_n)} to {f(home_j)}), in line with lower branded clicks.</div>
  </section>

  <section>
    <h2>Top 30 Pages by Clicks (October vs September), with AI Citations per Page</h2>
    <table class="t"><thead>
      <tr><th>#</th><th>Page</th><th>NovaStacks Work</th><th class="num">September Clicks</th><th class="num">October Clicks</th><th class="num">Δ Clicks</th><th class="num">October Impr</th><th class="num aeo">AI Citations · September</th><th class="num aeo">AI Citations · October</th></tr>
    </thead><tbody>
      {fr['top30']}
    </tbody></table>
    <p class="note"><b>NovaStacks Work</b> flags each blog / glossary page from the content delivery tracker: <span style="background:#eafaf0;color:#15803d;padding:1px 5px;border-radius:4px;font-size:11px;font-weight:600">🆕 NS · Created</span> = a new NovaStacks article (month it went live), <span style="background:#e6f4f1;color:#0f766e;padding:1px 5px;border-radius:4px;font-size:11px;font-weight:600">🔄 NS · Updated</span> = an existing page NovaStacks last refreshed (latest update month; hover for the exact date). Pages with no flag are legacy GoFreight content NovaStacks has not touched. <b>AI Citations</b> = WorkDuo-tracked AI responses citing this page as a source in the month.</p>
  </section>

  <section>
    <h2>Top 15 Most Cited Pages by AI: A Different List Than the Click Winners</h2>
    <table class="t"><thead>
      <tr><th>#</th><th>Page</th><th>NovaStacks Work</th><th class="num aeo">AI Citations · September</th><th class="num aeo">AI Citations · October</th><th class="num">Δ</th><th class="num">October Clicks</th><th class="num">In Click Top 30?</th></tr>
    </thead><tbody>
      {fr['top15']}
    </tbody></table>
    <p class="note">The 15 pages with the most AI citations in October, ordered by the change vs September (biggest gainers first).</p>
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
    <h2>AI Traffic Deep Dive: a ChatGPT Tracking Gap, and Gemini Doubles</h2>
    <p class="note" style="margin-bottom:8px;">AI referred sessions went from {f(AIS_N)} (September) to {f(AIS_J)} (October), <b>{ais_p:+.1f}%</b>. This section shows <b>which engines and which pages</b> moved. The source table sums sessions per AI source, so its total can differ by a session or two from the monthly total.</p>
    <div class="two-col" style="align-items:start;">
      <div>
        <table class="t"><thead>
          <tr><th>AI Source</th><th class="num">September</th><th class="num">October</th><th class="num">Δ</th></tr>
        </thead><tbody>
          {fr['src']}
        </tbody></table>
        <div class="takeaway-box watch" style="margin-top:8px;"><b>ChatGPT: a tracking bug explains part of the decline.</b> From 8 to 15 October ChatGPT links went out without their <code>utm_source=chatgpt.com</code> tag and without referral data, so analytics could no longer attribute those visits to ChatGPT. OpenAI confirmed it was a known bug and the fix rolled out from 15 October (<a href="https://searchengineland.com/chatgpt-appears-to-drop-utm-tracking-making-ai-referral-traffic-harder-to-measure-496552" target="_blank">Search Engine Land, 20 Oct 2026</a>). GoFreight's GA4 dips in the same window: ChatGPT sessions averaged <b>{cg_pre:.1f} a day</b> from 24 Sep to 7 Oct, fell to <b>{cg_gap:.1f} a day</b> from 9 to 14 Oct, and came back to <b>{cg_post:.1f} a day</b> from 16 to 29 Oct. Against the early October rate, the bug window accounts for about <b>{f(cg_short)} sessions</b> of the {f(fr['cg_jun']-fr['cg_jul'])} fewer recorded ChatGPT sessions ({f(fr['cg_jun'])} to {f(fr['cg_jul'])}); after the fix ChatGPT sessions came back close to, but not fully at, the early October level.</div>
        <div class="takeaway-box win" style="margin-top:8px;"><b>Gemini doubled.</b> Gemini went from <b>{f(gem_n)} to {f(gem_j)}</b>, its best month of 2026, which offsets about half of the recorded ChatGPT decline.</div>
      </div>
      <div>
        <table class="t"><thead>
          <tr><th>ChatGPT landing pages that lost recorded sessions</th><th class="num">September</th><th class="num">October</th><th class="num">Δ</th></tr>
        </thead><tbody>
          {fr['lp_drop']}
        </tbody></table>
        <table class="t" style="margin-top:10px;"><thead>
          <tr><th>ChatGPT landing pages that gained sessions</th><th class="num">September</th><th class="num">October</th><th class="num">Δ</th></tr>
        </thead><tbody>
          {fr['lp_gain']}
        </tbody></table>
      </div>
    </div>
    {lp_read}
  </section>

  <section>
    <h2>AEO Metrics: Month over Month</h2>
    <table class="t"><thead>
      <tr><th>Metric</th><th class="num">September 2026</th><th class="num">October 2026</th><th class="num">Change</th><th>Source</th></tr>
    </thead><tbody>
      {fr['aeo']}
    </tbody></table>
    <p class="note">AI Platform Sessions from GA4 direct (property 373075091). AI Visibility (non brand) from the WorkDuo API. Pages Cited / Total Citations recounted from the WorkDuo API (occurrence count, 28 non brand + 11 branded prompt panel, project cmhk59aw9001mlo33c3t8n3rj).</p>
    {aeo_box}
  </section>

  <footer>
    Sources: GSC (sc-domain:gofreight.com, date-dim for totals; page-dim for page/subfolder; page filter = gofreight.com, subdomains excluded; US market core keywords filtered country=usa, main page per keyword) · WorkDuo project cmhk59aw9001mlo33c3t8n3rj (28 non-brand prompts for visibility; all prompt citations occurrence-recounted from /responses API) · GA4 property 373075091 (AI-referral sessions + source/landing-page analysis; ChatGPT tracking bug 8 to 15 Oct per Search Engine Land, 20 Oct 2026) · GSC Performance exports, generative AI features vs all web (downloaded 2026-11-03) · Generated 2026-11-03
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
]}}, options:{{responsive:true, maintainAspectRatio:false, plugins:{{legend:{{position:'bottom',labels:{{font:{{size:10}},boxWidth:10,padding:6}}}}, tooltip:{{callbacks:{{label:(c)=>`${{c.dataset.label}}: ${{c.parsed.y.toFixed(1)}}%`}}}}}}, scales:{{y:{{beginAtZero:true,max:50,ticks:{{font:{{size:10}},callback:(v)=>v+'%'}},grid:{{color:'#f1f5f9'}}}}, x:{{ticks:{{font:{{size:10}},maxRotation:0,autoSkip:true,maxTicksLimit:8}},grid:{{display:false}}}}}}}}}});

new Chart(document.getElementById('chart3'), {{ type:'line', data:{{ labels:weekLabels, datasets:[
  {{label:'AI sessions', data:aiSessions, borderColor:'#7c3aed', backgroundColor:'rgba(124,58,237,0.15)', borderWidth:2.5, tension:0.3, fill:true, pointRadius:2.5, pointBackgroundColor:'#7c3aed', spanGaps:false}}
]}}, options:{{responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}, tooltip:{{callbacks:{{label:(c)=>`${{c.parsed.y}} AI sessions`}}}}}}, scales:{{y:{{beginAtZero:true,suggestedMax:150,ticks:{{stepSize:25,font:{{size:10}}}},grid:{{color:'#f1f5f9'}}}}, x:{{ticks:{{font:{{size:10}},maxRotation:0,autoSkip:true,maxTicksLimit:8}},grid:{{display:false}}}}}}}}}});
new Chart(document.getElementById('chart4'), {{ type:'bar', data:{{ labels:{ga_wl}, datasets:[
  {{label:'Inside AI features', data:{ga_wai}, backgroundColor:'#017d8e', stack:'s'}},
  {{label:'Outside AI features', data:{ga_wother}, backgroundColor:'#cbd5e1', stack:'s'}}
]}}, options:{{responsive:true, maintainAspectRatio:false, plugins:{{legend:{{position:'bottom',labels:{{font:{{size:10}},boxWidth:10,padding:6}}}}, tooltip:{{callbacks:{{label:(c)=>`${{c.dataset.label}}: ${{c.parsed.y.toLocaleString()}}`}}}}}}, scales:{{y:{{stacked:true,beginAtZero:true,ticks:{{font:{{size:10}},callback:(v)=>(v/1000)+'k'}},grid:{{color:'#f1f5f9'}}}}, x:{{stacked:true,ticks:{{font:{{size:10}},maxRotation:0,autoSkip:true,maxTicksLimit:7}},grid:{{display:false}}}}}}}}}});
</script>
</body>
</html>'''

import os
outdir='/Users/ekiriandra/seo-projects/novastacks/clients/gofreight/output/reports'
os.makedirs(outdir,exist_ok=True)
open(outdir+'/gofreight_october_2026_report.html','w',encoding='utf-8').write(HTML)
print('WROTE',outdir+'/gofreight_october_2026_report.html','len',len(HTML))
