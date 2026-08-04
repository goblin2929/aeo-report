# What domains does Google AI Overview cite, before vs after the late-July shift?
import urllib.request,urllib.parse,base64,json,sys,os,time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
AUTH=base64.b64encode(f"{os.environ.get('WORKDUO_PUBLIC_KEY','pk-wd-beb48021-d4ec-455a-8d7d-1e4f5a16406d')}:{os.environ.get('WORKDUO_SECRET_KEY','sk-wd-f0d47824-6d81-452d-8472-79725d7861fa')}".encode()).decode()
PID='cmhk59aw9001mlo33c3t8n3rj'
def api(path,params,att=6):
    for i in range(att):
        try:
            req=urllib.request.Request(f'https://api.workduo.ai/core/v1/{path}?'+urllib.parse.urlencode(params));req.add_header('Authorization',f'Basic {AUTH}')
            with urllib.request.urlopen(req,timeout=120) as r:return json.loads(r.read())
        except Exception as e:time.sleep(2*(i+1));last=str(e)
    raise RuntimeError(last)
qs=json.load(open('/tmp/wd_queries_all.json'))
nb=[q['id'] for q in qs if q.get('topic') in ('MOFU','TOFU','BOFU')]
def fetch(qid):
    out=[];tok=None
    for _ in range(80):
        p={'projectId':PID,'queryId':qid,'dateRange':'custom','startDate':'2026-07-13','endDate':'2026-08-02','limit':100}
        if tok:p['pageToken']=tok
        try:res=api('responses',p)
        except:break
        out.extend(res.get('data',[]));tok=res.get('nextPageToken')
        if not tok:break
    return out
resps=[]
with ThreadPoolExecutor(max_workers=4) as ex:
    for rs in ex.map(fetch,nb): resps.extend(rs)
aio=[r for r in resps if 'ai-overview' in (r.get('platform') or '').lower()]
def period(d):
    if '2026-07-13'<=d<='2026-07-26': return 'before'
    if '2026-07-27'<=d<='2026-08-02': return 'after'
    return None
def dom(u):
    try: d=urlparse(u).netloc.lower()
    except: return None
    return d[4:] if d.startswith('www.') else d
def cites(r):
    out=[]
    for c in (r.get('citations') or []):
        u=c.get('url') if isinstance(c,dict) else (c if isinstance(c,str) else None)
        if u: 
            d=dom(u)
            if d: out.append(d)
    return out
resp_ct=defaultdict(int); cit_ct=defaultdict(int)
dom_cit=defaultdict(lambda:defaultdict(int))      # domain -> period -> citation occurrences
dom_resp=defaultdict(lambda:defaultdict(int))     # domain -> period -> responses citing
for r in aio:
    per=period(r.get('date','')); 
    if not per: continue
    resp_ct[per]+=1
    cs=cites(r); cit_ct[per]+=len(cs)
    for d in cs: dom_cit[d][per]+=1
    for d in set(cs): dom_resp[d][per]+=1
print("=== AI Overview answer 'shape' (non-brand prompts) ===")
for per in ['before','after']:
    rc=resp_ct[per]; cc=cit_ct[per]
    print(f"  {per:6s}: {rc} responses, {cc} citations, avg {cc/rc:.2f} citations/answer")
VENDOR={'gofreight.com','cargowise.com','magaya.com','descartes.com','logixboard.com','freightos.com','wisetechglobal.com','shipthis.com','gocomet.com','neurored.com'}
def cat(d):
    if d in VENDOR: return 'VENDOR'
    if any(x in d for x in ('g2.com','capterra','softwareadvice','getapp','trustradius','gartner','sourceforge','saasworthy','goodfirms','crozdesk','softwaresuggest','financesonline','selecthub','techimply','slashdot')): return 'DIRECTORY'
    return 'OTHER/EDITORIAL'
# category shares
cat_cit=defaultdict(lambda:defaultdict(int))
for d,per in dom_cit.items():
    for p,c in per.items(): cat_cit[cat(d)][p]+=c
print("\n=== Citation share by source type ===")
for c in ['VENDOR','DIRECTORY','OTHER/EDITORIAL']:
    b=cat_cit[c]['before']; a=cat_cit[c]['after']
    sb=b/cit_ct['before']*100 if cit_ct['before'] else 0; sa=a/cit_ct['after']*100 if cit_ct['after'] else 0
    print(f"  {c:16s} before {b:4d} ({sb:4.1f}%)  ->  after {a:4d} ({sa:4.1f}%)   Δshare {sa-sb:+.1f}pp")
# domains: sort by after count; flag NEW
alldoms=set(dom_cit)
rows=[(d,dom_cit[d]['before'],dom_cit[d]['after']) for d in alldoms]
print("\n=== Top domains cited AFTER (Jul27-Aug2), with before + status ===")
print(f"{'after':>6}{'before':>7}  {'cat':16s} domain")
for d,b,a in sorted(rows,key=lambda x:-x[2])[:22]:
    status='NEW' if b==0 and a>0 else ('rose' if a>b else ('fell' if a<b else 'flat'))
    print(f"{a:>6}{b:>7}  {cat(d):16s} {d}  [{status}]")
print("\n=== Domains that FELL the most (before -> after) ===")
for d,b,a in sorted(rows,key=lambda x:(x[2]-x[1]))[:12]:
    print(f"  {b:>4} -> {a:>4}  ({a-b:+d})  {cat(d):16s} {d}")
print("\n=== NEW domains appearing only AFTER (>=2 cites) ===")
for d,b,a in sorted([x for x in rows if x[1]==0 and x[2]>=2],key=lambda x:-x[2]):
    print(f"  {a:>3} cites  {cat(d):16s} {d}")
