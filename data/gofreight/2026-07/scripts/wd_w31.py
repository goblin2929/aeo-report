import urllib.request,urllib.parse,base64,json,sys,time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
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
    for _ in range(50):
        p={'projectId':PID,'queryId':qid,'dateRange':'custom','startDate':'2026-07-27','endDate':'2026-08-02','limit':100}
        if tok:p['pageToken']=tok
        try:res=api('responses',p)
        except:break
        out.extend(res.get('data',[]));tok=res.get('nextPageToken')
        if not tok:break
    return out
agg=defaultdict(lambda:{'m':0,'t':0})
with ThreadPoolExecutor(max_workers=4) as ex:
    for rs in ex.map(fetch,nb):
        for r in rs:
            pl=bk(r.get('platform',''))
            if pl=='Other':continue
            agg[pl]['t']+=1
            if r.get('selfMentioned'):agg[pl]['m']+=1
out={pl:(round(agg[pl]['m']/agg[pl]['t']*100,1) if agg[pl]['t'] else 0) for pl in ['ChatGPT','Perplexity','Google AI']}
json.dump(out,open('d:/tmp/wd_w31.json','w'));print("W31:",out,file=sys.stderr)
