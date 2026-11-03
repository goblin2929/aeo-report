import sys, json
sys.path.insert(0,'scripts')
from gsc_client import GSC
SITE='sc-domain:gofreight.com'
KW=['freight forwarding crm','logistics crm software','best tms software','freight forwarder software','freight software','freight tracking software',
    'freight forwarding software','freight management software','freight management system','freight management system software','best freight forwarding software','best freight management software','air freight forwarding software','global freight management system','ocean freight management software','sea freight management software','container freight management system']
MONTHS=[('sep','2026-09-01','2026-09-30'),('oct','2026-10-01','2026-10-31')]
g=GSC('novastacks')
out={}
for kw in KW:
    out[kw]={}
    for lab,s,e in MONTHS:
        f=[{'filters':[{'dimension':'country','operator':'equals','expression':'usa'},{'dimension':'query','operator':'equals','expression':kw}]}]
        rows=g.query(SITE,s,e,dimensions=['page'],row_limit=1000,dimension_filter_groups=f)
        out[kw][lab]=sorted([{'url':r['keys'][0],'pos':round(r['position'],1),'impr':int(r['impressions']),'clicks':int(r['clicks'])} for r in rows],key=lambda x:-x['impr'])
json.dump(out,open('/Users/ekiriandra/tmp/oct/gf_core17_allpages.json','w'),indent=1)
for kw in KW:
    m=lambda l:(out[kw][l][0]['url'].replace('https://gofreight.com',''),out[kw][l][0]['pos'],out[kw][l][0]['impr']) if out[kw][l] else None
    print(f"{kw:36s} SEP {m('sep')}  OCT {m('oct')}")
