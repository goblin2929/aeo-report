# Which prompts/topics drove the late-July Google AI Overview visibility drop?
import urllib.request,urllib.parse,base64,json,sys,os,time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
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
qmeta={q['id']:{'topic':q.get('topic','?'),'text':(q.get('query') or '')} for q in qs}
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
# distinct google-family platforms
plats=defaultdict(int)
for r in resps:
    p=(r.get('platform') or '').lower()
    if 'google' in p or 'gemini' in p or 'ai-overview' in p: plats[p]+=1
print("=== google-family platform values (Jul13-Aug2) ===",file=sys.stderr)
for p,c in sorted(plats.items(),key=lambda x:-x[1]): print(f"  {c:5d}  {p}",file=sys.stderr)

def is_aio(r): return 'ai-overview' in (r.get('platform') or '').lower()
BEFORE=('2026-07-13','2026-07-26'); AFTER=('2026-07-27','2026-08-02')
def bucket(d): return 'before' if BEFORE[0]<=d<=BEFORE[1] else ('after' if AFTER[0]<=d<=AFTER[1] else None)
# per query AI-Overview only
q=defaultdict(lambda:{'before':{'m':0,'t':0},'after':{'m':0,'t':0}})
topic=defaultdict(lambda:{'before':{'m':0,'t':0},'after':{'m':0,'t':0}})
for r in resps:
    if not is_aio(r): continue
    b=bucket(r.get('date','')); 
    if not b: continue
    qid=r.get('queryId',''); tp=qmeta.get(qid,{}).get('topic','?')
    q[qid][b]['t']+=1; topic[tp][b]['t']+=1
    if r.get('selfMentioned'):
        q[qid][b]['m']+=1; topic[tp][b]['m']+=1
def rate(d): return d['m']/d['t']*100 if d['t'] else None
print("\n=== Google AI OVERVIEW visibility by TOPIC (before Jul13-26 vs after Jul27-Aug2) ===")
for tp in ['TOFU','MOFU','BOFU']:
    b,a=topic[tp]['before'],topic[tp]['after']
    rb=rate(b); ra=rate(a)
    d = (ra-rb) if (rb is not None and ra is not None) else None
    print(f"  {tp:5s}  before {b['m']}/{b['t']} ({rb:.1f}%)  ->  after {a['m']}/{a['t']} ({ra:.1f}%)   Δ {d:+.1f}pp")
rows=[]
for qid,dd in q.items():
    rb=rate(dd['before']); ra=rate(dd['after'])
    if rb is None or ra is None: continue
    rows.append((ra-rb, rb, ra, dd, qmeta[qid]['topic'], qmeta[qid]['text']))
rows.sort(key=lambda x:x[0])
print("\n=== Biggest AI-Overview visibility DROPS by prompt ===")
print(f"{'Δpp':>6} {'before':>8} {'after':>8}  topic  prompt")
for d,rb,ra,dd,tp,txt in rows[:14]:
    print(f"{d:>6.0f} {dd['before']['m']}/{dd['before']['t']:>3}={rb:>4.0f}% {dd['after']['m']}/{dd['after']['t']:>3}={ra:>4.0f}%  {tp:5s}  {txt[:72]}")
print("\n=== Prompts that HELD / rose ===")
for d,rb,ra,dd,tp,txt in [x for x in rows if x[0]>=0][:6]:
    print(f"{d:>6.0f} {rb:>4.0f}%->{ra:>4.0f}%  {tp:5s}  {txt[:72]}")
