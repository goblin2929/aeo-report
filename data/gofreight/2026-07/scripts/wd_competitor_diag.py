import urllib.request,urllib.parse,base64,json,sys,time,re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
AUTH = base64.b64encode(f"{os.environ['WORKDUO_PUBLIC_KEY']}:{os.environ['WORKDUO_SECRET_KEY']}".encode()).decode()
PID='cmhk59aw9001mlo33c3t8n3rj'
def api(path,params,att=6):
    for i in range(att):
        try:
            req=urllib.request.Request(f'https://api.workduo.ai/core/v1/{path}?'+urllib.parse.urlencode(params));req.add_header('Authorization',f'Basic {AUTH}')
            with urllib.request.urlopen(req,timeout=120) as r:return json.loads(r.read())
        except Exception as e:time.sleep(2*(i+1));last=str(e)
    raise RuntimeError(last)
qs=json.load(open('/tmp/wd_queries_all.json'));nb=[q['id'] for q in qs if q.get('topic') in ('MOFU','TOFU','BOFU')]
def bk(p):
    pl=(p or '').lower()
    if 'chatgpt' in pl or pl.startswith('openai'):return 'ChatGPT'
    if 'perplexity' in pl:return 'Perplexity'
    if 'google' in pl or 'ai-overview' in pl or 'gemini' in pl:return 'Google AI'
    return 'Other'
def fetch(qid):
    out=[];tok=None
    for _ in range(80):
        p={'projectId':PID,'queryId':qid,'dateRange':'custom','startDate':'2026-07-06','endDate':'2026-08-02','limit':100}
        if tok:p['pageToken']=tok
        try:res=api('responses',p)
        except:break
        out.extend(res.get('data',[]));tok=res.get('nextPageToken')
        if not tok:break
    return out
resps=[]
with ThreadPoolExecutor(max_workers=4) as ex:
    for rs in ex.map(fetch,nb): resps.extend(rs)
# Google AI only
gai=[r for r in resps if bk(r.get('platform',''))=='Google AI']
def ent_names(r):
    out=set()
    for e in (r.get('mentionedEntities') or []):
        n=(e.get('name') or '').lower().strip()
        if n: out.add(n)
    return out
# tally all entities to find competitors
tally=defaultdict(int)
for r in gai:
    for n in ent_names(r): tally[n]+=1
print("=== Top mentioned entities in Google AI (non-brand, Jul6-Aug2) ===",file=sys.stderr)
for n,c in sorted(tally.items(),key=lambda x:-x[1])[:18]: print(f"  {c:4d}  {n}",file=sys.stderr)
# weekly mention rate for gofreight (selfMentioned) + top competitors
def wk(d): return datetime.strptime(d,'%Y-%m-%d').strftime('%Y-W%V')
BRANDS={'GoFreight':None,'CargoWise':'cargowise','Magaya':'magaya','Descartes':'descartes','Logixboard':'logixboard','Freightos':'freightos','WiseTech':'wisetech'}
wtot=defaultdict(int)
wbrand=defaultdict(lambda:defaultdict(int))
for r in gai:
    w=wk(r.get('date','')); wtot[w]+=1
    names=ent_names(r)
    for b,key in BRANDS.items():
        hit = r.get('selfMentioned') if b=='GoFreight' else any(key in n for n in names)
        if hit: wbrand[b][w]+=1
weeks=sorted(wtot)
print("\n=== Google AI Overview weekly mention RATE (mentions / total responses) ===")
hdr="week      total  "+"".join(f"{b:>11s}" for b in BRANDS)
print(hdr)
for w in weeks:
    t=wtot[w]
    cells="".join(f"{(wbrand[b][w]/t*100):>10.1f}%" for b in BRANDS)
    print(f"{w}  {t:>5d}  {cells}")
