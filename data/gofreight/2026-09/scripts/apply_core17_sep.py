import json, re, shutil
from urllib.parse import urlparse
ALL=json.load(open('/Users/ekiriandra/tmp/sep/gf_core17_allpages.json'))
CANON=['freight forwarding software','freight management software','freight management system','freight management system software','best freight forwarding software','best freight management software','air freight forwarding software','global freight management system','ocean freight management software','sea freight management software','container freight management system']
EMERG=['freight forwarding crm','logistics crm software','best tms software','freight forwarder software','freight software','freight tracking software']
SITELINK={'/company','/pricing','/why-gofreight'}
LIST='https://gofreight.com/blog/best-freight-management-software'; HOME='https://gofreight.com/'
MINIMP=10
def path(u):
    p=urlparse(u).path.rstrip('/'); return p or '/'
def label(u):
    p=path(u)
    if p=='/': return 'gofreight.com/ (homepage)'
    return p if len(p)<=46 else p[:44]+'…'
def link(u): return f'<a href="{u}" target="_blank">{label(u)}</a>'
def best(kw,m):
    rows=[r for r in ALL[kw][m] if r['impr']>=MINIMP and path(r['url']) not in SITELINK]
    return min(rows,key=lambda r:r['pos']) if rows else None
def pos_of(kw,m,u):
    r=next((r for r in ALL[kw][m] if path(r['url'])==path(u)),None); return r
def ptype(u):
    p=path(u)
    if p=='/': return 'homepage'
    if p.startswith('/solutions'): return 'solution page'
    if p.startswith('/product'): return 'product page'
    if p.startswith('/glossary'): return 'glossary page'
    if 'best-' in p or 'software-guide' in p or 'comparison' in p: return 'listicle / guide'
    return 'blog'
def band(cp): return 'top 2' if cp<=2 else ('top 3' if cp<=3 else ('top 5' if cp<=5 else ('page 1' if cp<=10 else ('page 2' if cp<=20 else 'page 3+'))))
def main(kw,m):
    rows=[r for r in ALL[kw][m] if path(r['url']) not in SITELINK]
    return max(rows,key=lambda r:r['impr']) if rows else None
NICE={'homepage':'homepage','solution page':'solution page','product page':'product page','glossary page':'glossary page','listicle / guide':'listicle','blog':'blog post'}
def row(kw):
    a,s=main(kw,'aug'),main(kw,'sep'); ba,bs=best(kw,'aug'),best(kw,'sep')
    pa=f"{a['pos']:.1f}" if a else 'n/a'; ps=f"{s['pos']:.1f}" if s else 'n/a'
    dd=round(a['pos']-s['pos'],1) if (a and s) else None
    if dd is None: cls,dc,win='','n/a',False
    elif dd>0: cls,dc,win='up',f'+{dd:.1f} ▲',True
    elif dd==0: cls,dc,win='','±0.0 ●',True
    else: cls,dc,win='down',f'{dd:.1f} ▼',False
    swap = a and s and path(a['url'])!=path(s['url'])
    ta,ts=(NICE[ptype(a['url'])] if a else ''),(NICE[ptype(s['url'])] if s else '')
    if not s: summ='No US impressions in September'
    elif swap and ta!=ts: summ=f"{pa} → {ps}, shifted from {ta} to {ts}"
    elif swap: summ=f"{pa} → {ps}, shifted to a different {ts}"
    else: summ=f"{pa} → {ps} on the {ts}"
    bcell=(f"{ba['pos']:.1f} → {bs['pos']:.1f}" if (ba and bs) else 'n/a')
    btip=(f' title="August: {label(ba["url"])} · September: {label(bs["url"])}"' if (ba and bs) else '')
    return (f'<tr class="{"win-row" if win else ""}"><td><b>{kw}</b></td><td>{link(a["url"]) if a else "n/a"}</td><td class="num">{pa}</td>'
            f'<td>{link(s["url"]) if s else "n/a"}</td><td class="num">{ps}</td><td class="num {cls}">{dc}</td><td class="num"{btip}>{bcell}</td><td>{summ}</td></tr>'), (dd,kw,a,s,summ)
def hdr(first): return (f'<tr><th>{first}</th><th>Main page · August</th><th class="num">Aug avg pos (month)</th><th>Main page · September</th><th class="num">Sep avg pos (month)</th><th class="num">Δ Position</th><th class="num">Best position Aug → Sep</th><th>Summary</th></tr>')
def table(keys):
    rs=[row(k) for k in keys]; return '\n'.join(r[0] for r in rs),[r[1] for r in rs]
def lh(kw,m,u):
    r=pos_of(kw,m,u); return (f"{r['pos']:.1f}",f"{r['impr']:,}") if r else ('n/a','0')
CLUSTER=['freight management software','freight management system software','ocean freight management software','sea freight management software','freight management system']
def cluster_rows():
    out=[]
    for kw in CLUSTER:
        la,ia=lh(kw,'aug',LIST); ls,is_=lh(kw,'sep',LIST); ha,ja=lh(kw,'aug',HOME); hs,js=lh(kw,'sep',HOME)
        out.append(f'<tr><td><b>{kw}</b></td><td class="num">{la}</td><td class="num">{ls}</td><td class="num">{ha}</td><td class="num">{hs}</td><td class="num">{ia} / {is_}</td><td class="num">{ja} / {js}</td></tr>')
    return '\n'.join(out)
def build():
    ct,cm=table(CANON); et,em=table(EMERG)
    mv=cm+em
    ups=sorted([m for m in mv if m[0] is not None and m[0]>0.3],reverse=True)
    downs=sorted([m for m in mv if m[0] is not None and m[0]<-0.3])
    li=lambda t:''.join(f'<li><b>“{kw}”</b> {summ}</li>' for dd,kw,a,s,summ in t[:5])
    return f'''<section>
    <h2>Core Keyword Tracking: Commercial Cluster (US market, monthly average position, September vs August)</h2>
    <p class="note" style="margin-bottom:8px;"><b>Canonical panel</b>: the 11 commercial cluster terms, kept fixed month over month. For each keyword and month we take the <b>main GoFreight page</b> (the page with the most US impressions for that keyword) and its <b>monthly average position</b>, so when Google switches from one GoFreight page to another the shift is visible. <b>Best position</b> is the best monthly average across any GoFreight page with at least {MINIMP} US impressions (hover for the page). Sitelinks shown under the homepage (company, pricing, why GoFreight) are left out. All positions are monthly averages, lower = better.</p>
    <table class="t"><thead>{hdr('Core Keyword')}</thead><tbody>
      {ct}
    </tbody></table>
    <div class="two-col" style="margin-top:10px;">
      <div class="takeaway-box win"><b>✓ Improved (US, main page)</b><ul>{li(ups)}</ul></div>
      <div class="takeaway-box watch"><b>⚠ Watch (US, main page)</b><ul>{li(downs) or '<li>No material declines this month.</li>'}</ul></div>
    </div>
    <h3 style="margin-top:16px;">Freight management cluster: listicle vs homepage</h3>
    <table class="t"><thead><tr><th>Keyword</th><th class="num">Listicle · Aug</th><th class="num">Listicle · Sep</th><th class="num">Homepage · Aug</th><th class="num">Homepage · Sep</th><th class="num">Listicle impr Aug / Sep</th><th class="num">Homepage impr Aug / Sep</th></tr></thead><tbody>
      {cluster_rows()}
    </tbody></table>
    <p class="note">Monthly average US position of the <a href="{LIST}" target="_blank">Best Freight Management Software listicle</a> and the <a href="{HOME}" target="_blank">homepage</a> for the same keyword. Lower = better.</p>
    <div class="takeaway-box" style="margin-top:8px;"><b>Read (hypothesis): the search intent is shifting from listicles toward vendor pages.</b> In August Google answered these freight management queries mainly with the listicle; in September it showed the homepage instead, and the solution pages also climbed (for example /solutions/ocean-freight for “ocean freight management software”, 29.2 to 18.5 monthly average). For ocean and sea freight management software the shift is a net gain: <b>8.5 → 8.0</b> and <b>9.3 → 5.2</b>, shifted from listicle to homepage. For the broad terms it is a net loss: “freight management software” <b>3.1 → 12.2</b> and “freight management system software” <b>5.4 → 10.6</b>, also shifted from listicle to homepage. If the SERP keeps favouring vendor pages, the October solution and product page work is the lever, because those are the pages Google now wants to show for this cluster. The listicle is live and Google can still index it; we keep tracking both pages.</div>
    <h3 style="margin-top:16px;">Emerging Keywords (candidate terms: CRM / TMS / tracking)</h3>
    <table class="t"><thead>{hdr('Emerging Keyword')}</thead><tbody>
      {et}
    </tbody></table>
    <p class="note">Tracked alongside the canonical panel with the same main page and monthly average method.</p>
  </section>'''
def replace_section(fn, html):
    h=open(fn,encoding='utf-8').read()
    m=re.search(r'<section>\s*<h2>[^<]*Core Keyword Tracking.*?</section>', h, re.S)
    if not m: raise SystemExit('core section not found')
    open(fn,'w',encoding='utf-8').write(h[:m.start()]+html+h[m.end():]); print('updated',fn)
F='/Users/ekiriandra/seo-projects/aeo-report/gofreight_september_2026_report.html'
replace_section(F,build())
shutil.copy(F,'/Users/ekiriandra/seo-projects/novastacks/clients/gofreight/output/reports/gofreight_september_2026_report.html')
print('done')
