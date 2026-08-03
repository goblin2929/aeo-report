# -*- coding: utf-8 -*-
"""WorkDuo June+July occurrence-count citations + weekly non-brand visibility.
Keys: jun (June 2026) / jul (July 2026). Output d:/tmp/wd_july.json."""
import urllib.request, urllib.parse, base64, json, sys, re, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import os
AUTH = base64.b64encode(f"{os.environ['WORKDUO_PUBLIC_KEY']}:{os.environ['WORKDUO_SECRET_KEY']}".encode()).decode()
PID = 'cmhk59aw9001mlo33c3t8n3rj'

def api(path, params, attempts=6):
    url = f'https://api.workduo.ai/core/v1/{path}?' + urllib.parse.urlencode(params)
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url); req.add_header('Authorization', f'Basic {AUTH}')
            with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read()[:200].decode(errors='replace')
            if e.code == 400: raise RuntimeError(f'HTTP 400: {body}')
            last = f'HTTP {e.code}: {body}'
        except Exception as e: last = str(e)
        time.sleep(2*(i+1))
    raise RuntimeError(f'FAILED: {last}')

qs = json.load(open('/tmp/wd_queries_all.json'))
qmap = {q['id']: q.get('topic','?') for q in qs}
all_qids = list(qmap.keys())
nonbrand = set(q for q,t in qmap.items() if t in ('MOFU','TOFU','BOFU'))
print(f'{len(all_qids)} queries, {len(nonbrand)} non-brand', file=sys.stderr)

CHUNKS = [('2026-06-01','2026-06-30'),('2026-07-01','2026-07-31')]
MONTH = {'2026-06':'jun','2026-07':'jul'}

def fetch(args):
    qid,s,e = args; out=[]; tok=None
    for _ in range(300):
        p={'projectId':PID,'queryId':qid,'dateRange':'custom','startDate':s,'endDate':e,'limit':100}
        if tok: p['pageToken']=tok
        try: res=api('responses',p)
        except RuntimeError as ex: print(f'  giveup {qid[-6:]} {s}: {ex}',file=sys.stderr); break
        out.extend(res.get('data',[])); tok=res.get('nextPageToken')
        if not tok: break
    return qid,out

def bucket(p):
    pl=(p or '').lower()
    if 'chatgpt' in pl or pl.startswith('openai'): return 'ChatGPT'
    if 'perplexity' in pl: return 'Perplexity'
    if 'google' in pl or 'ai-overview' in pl or 'gemini' in pl: return 'Google AI'
    return 'Other'
def norm(u):
    u=u.strip().split('#')[0].split('?')[0]
    if u.endswith('/') and len(u)>len('https://gofreight.com/'): u=u.rstrip('/')
    return u.lower()
GF_RE=re.compile(r'https?://[^\s\'">\]\\]*gofreight\.com[^\s\'">\]\\]*',re.I)
CIT=['citations','sources','references','citedUrls','sourceUrls','citedSources','mentionedUrls']
def extract(resp):
    urls=[]; found=False
    for fld in CIT:
        v=resp.get(fld)
        if isinstance(v,list):
            found=True
            for it in v:
                if isinstance(it,str) and 'gofreight.com' in it.lower(): urls.append(it)
                elif isinstance(it,dict):
                    for k in ('url','link','href','source','uri'):
                        if isinstance(it.get(k),str) and 'gofreight.com' in it[k].lower(): urls.append(it[k]); break
        elif isinstance(v,str) and 'gofreight.com' in v.lower(): found=True; urls.append(v)
    if not found: urls=GF_RE.findall(json.dumps(resp))
    return [norm(u) for u in urls if 'gofreight.com' in u.lower()]

weekly=defaultdict(lambda: defaultdict(lambda:{'m':0,'t':0}))
monthly_vis=defaultdict(lambda:{'m':0,'t':0})
monthly_sov=defaultdict(lambda:{'s':0.0,'n':0})   # non-brand SOV
monthly_mentions=defaultdict(int)                  # all-query self-mentions
page_cit=defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
page_tot=defaultdict(lambda: defaultdict(int))
resp_counts=defaultdict(int)
for s,e in CHUNKS:
    tasks=[(q,s,e) for q in all_qids]; got=0
    with ThreadPoolExecutor(max_workers=4) as ex:
        for qid,resps in ex.map(fetch,tasks):
            got+=len(resps); nb=qid in nonbrand
            for r in resps:
                d=r.get('date',''); mo=d[:7]; pl=bucket(r.get('platform',''))
                if pl!='Other':
                    resp_counts[mo]+=1
                    if r.get('selfMentioned'): monthly_mentions[mo]+=1
                    if nb:
                        wk=datetime.strptime(d,'%Y-%m-%d').strftime('%Y-W%V')
                        weekly[wk][pl]['t']+=1; monthly_vis[mo]['t']+=1
                        try: monthly_sov[mo]['s']+=float(r.get('sov') or 0); monthly_sov[mo]['n']+=1
                        except (TypeError,ValueError): pass
                        if r.get('selfMentioned'): weekly[wk][pl]['m']+=1; monthly_vis[mo]['m']+=1
                if mo in MONTH:
                    ml=MONTH[mo]
                    for u in extract(r): page_cit[u][ml][pl]+=1; page_tot[u][ml]+=1
    print(f'  {s}: {got} responses',file=sys.stderr)

def classify(url):
    if 'support.gofreight.com' in url: return 'Support'
    if 'archive.gofreight.com' in url: return 'Archive'
    if 'api.gofreight.com' in url: return 'API'
    path=url
    for pre in ['https://gofreight.com','http://gofreight.com','https://www.gofreight.com']:
        if url.startswith(pre): path=url[len(pre):]; break
    if path in ('','/'): return 'Homepage'
    path=path.rstrip('/')
    if path.startswith('/blog'): return 'Blog'
    if path.startswith('/glossary'): return 'Glossary'
    if path.startswith('/pricing'): return 'Pricing'
    if path.startswith('/product'): return 'Product'
    if path.startswith('/solution'): return 'Solutions'
    for sp in ['/freight-forwarding-software','/freight-management-software','/freight-management-system','/air-freight-software','/ocean-freight-software','/customs-management','/warehouse-management']:
        if path==sp or path.startswith(sp+'/'): return 'Solutions'
    return 'Other'

pages=[]
for url in page_tot:
    pages.append({'url':url,'subfolder':classify(url),'jul':page_tot[url].get('jul',0),'jun':page_tot[url].get('jun',0),
        'jul_plat':dict(page_cit[url].get('jul',{})),'jun_plat':dict(page_cit[url].get('jun',{}))})
pages.sort(key=lambda x:x['jul'],reverse=True)
BUCK=['Homepage','Blog','Glossary','Solutions','Product','Pricing','Support','API','Archive','Other']
rollup={}
for b in BUCK:
    ps=[p for p in pages if p['subfolder']==b]
    rollup[b]={'jul_pages':len([p for p in ps if p['jul']>0]),'jun_pages':len([p for p in ps if p['jun']>0]),
        'jul_cit':sum(p['jul'] for p in ps),'jun_cit':sum(p['jun'] for p in ps)}
prim=[p for p in pages if p['subfolder'] not in ('Support','API','Archive')]
totals={'jul_total_cit':sum(p['jul'] for p in pages),'jun_total_cit':sum(p['jun'] for p in pages),
    'jul_pages':len([p for p in pages if p['jul']>0]),'jun_pages':len([p for p in pages if p['jun']>0]),
    'jul_total_cit_primary':sum(p['jul'] for p in prim),'jun_total_cit_primary':sum(p['jun'] for p in prim),
    'jul_pages_primary':len([p for p in prim if p['jul']>0]),'jun_pages_primary':len([p for p in prim if p['jun']>0])}
wk_out={}
for w in sorted(weekly):
    wk_out[w]={pl:(round(weekly[w][pl]['m']/weekly[w][pl]['t']*100,1) if weekly[w][pl]['t'] else 0) for pl in ['ChatGPT','Perplexity','Google AI']}
mv={m:(round(v['m']/v['t']*100,1) if v['t'] else 0) for m,v in sorted(monthly_vis.items())}
msov={m:(round(v['s']/v['n']*100,1) if v['n'] else 0) for m,v in sorted(monthly_sov.items())}
out={'weekly_visibility':wk_out,'monthly_visibility_nonbrand':mv,'monthly_sov_nonbrand':msov,
    'monthly_brand_mentions':dict(sorted(monthly_mentions.items())),
    'monthly_response_counts':dict(sorted(resp_counts.items())),
    'pages':pages,'subfolder_rollup':rollup,'totals':totals}
json.dump(out,open('d:/tmp/wd_july.json','w'),indent=2)
print('monthly vis:',mv,file=sys.stderr)
print('totals:',json.dumps(totals),file=sys.stderr)
print('top15:',file=sys.stderr)
for p in pages[:15]: print(f'  jul {p["jul"]:4d} jun {p["jun"]:4d} {p["subfolder"]:9s} {p["url"]}',file=sys.stderr)
print('WROTE d:/tmp/wd_july.json',file=sys.stderr)
