#!/usr/bin/env python3
"""Re-pull the Ultherapy keyword universe for all five markets and deduplicate.

Why: the sheet's 'Keywords raw' tab held only 1,999 rows (AU + HK complete, SG 40% short,
TH and TW absent entirely), and the totals summed word-order permutations that DataForSEO
returns as separate rows carrying the SAME clustered volume — inflating the region by ~24%.

Dedup rule: fingerprint = lowercased, punctuation-stripped, token-SORTED phrase. Variants
sharing a fingerprint are one query; we keep the highest-volume spelling and record the rest.
STOP on any API failure — no partial totals presented as complete.
"""
import os, sys, json, base64, urllib.request, urllib.error, re, time, collections

EP = "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live"

MARKETS = {
 "SG": {"location_name":"Singapore","language_name":"English",
        "seeds":["ultherapy","ultherapy prime","hifu","skin tightening"]},
 "AU": {"location_name":"Australia","language_name":"English",
        "seeds":["ultherapy","ultherapy prime","hifu","skin tightening"]},
 "TH": {"location_name":"Thailand","language_name":"Thai",
        "seeds":["ultherapy","ultherapy prime","hifu","ยกกระชับผิว"]},
 "TW": {"location_name":"Taiwan","language_name":"Chinese (Traditional)",
        "seeds":["ultherapy","音波拉提","電波拉皮","拉提"]},
 "HK": {"location_name":"Hong Kong","language_name":"Chinese (Traditional)",
        "seeds":["ultherapy","超聲刀","hifu","緊膚"]},
}
LIMIT = 1000

def creds():
    u,p = os.environ.get("DATAFORSEO_USERNAME"), os.environ.get("DATAFORSEO_PASSWORD")
    if not (u and p):
        for line in open(os.path.expanduser("~/.novastacks-env")):
            line=line.strip()
            if line.startswith("DATAFORSEO_USERNAME="): u=line.split("=",1)[1].strip().strip('"\'')
            if line.startswith("DATAFORSEO_PASSWORD="): p=line.split("=",1)[1].strip().strip('"\'')
    if not (u and p): sys.exit("STOP: DataForSEO credentials not found.")
    return u,p

def post(payload, c, label, tries=4):
    body=json.dumps(payload).encode()
    for a in range(tries):
        r=urllib.request.Request(EP, data=body, method="POST")
        r.add_header("Content-Type","application/json")
        r.add_header("Authorization","Basic "+base64.b64encode(f"{c[0]}:{c[1]}".encode()).decode())
        try:
            with urllib.request.urlopen(r, timeout=180) as resp:
                d=json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504) and a<tries-1: time.sleep(5*(a+1)); continue
            sys.exit(f"STOP: HTTP {e.code} on {label}: {e.read().decode()[:250]}")
        except Exception as e:
            if a<tries-1: time.sleep(5*(a+1)); continue
            sys.exit(f"STOP: request failed on {label}: {e}")
        if d.get("status_code")!=20000: sys.exit(f"STOP: status {d.get('status_code')} {d.get('status_message')} on {label}")
        t=(d.get("tasks") or [{}])[0]
        if t.get("status_code")!=20000: sys.exit(f"STOP: task {t.get('status_code')} {t.get('status_message')} on {label}")
        return t
    sys.exit(f"STOP: retries exhausted on {label}")

def fingerprint(k):
    toks = re.findall(r"[a-z0-9]+|[^\x00-\x7f]", k.lower())
    return " ".join(sorted(toks))

def main():
    c=creds(); out={}
    for mk,cfg in MARKETS.items():
        seen={}
        for seed in cfg["seeds"]:
            payload=[{"keyword":seed,"location_name":cfg["location_name"],
                      "language_name":cfg["language_name"],"limit":LIMIT,
                      "include_serp_info":False,"exact_match":False}]
            t=post(payload,c,f"{mk}:{seed}")
            items=(t.get("result") or [{}])[0].get("items") or []
            for it in items:
                kw=it.get("keyword")
                ki=it.get("keyword_info") or {}
                vol=ki.get("search_volume")
                if not kw or not vol: continue
                if kw not in seen or vol>seen[kw]: seen[kw]=vol
            print(f"  {mk} seed '{seed}': {len(items)} items, running unique {len(seen)}",
                  file=sys.stderr, flush=True)
        out[mk]=seen
        print(f"{mk}: {len(seen)} raw keywords, raw volume {sum(seen.values()):,}", file=sys.stderr, flush=True)
    json.dump(out, open("keywords_raw.json","w",encoding="utf8"), ensure_ascii=False)

    # deduplicate
    summary={}
    dedup={}
    for mk,seen in out.items():
        groups=collections.defaultdict(list)
        for kw,v in seen.items(): groups[fingerprint(kw)].append((kw,v))
        rows=[]
        for fp,g in groups.items():
            g.sort(key=lambda x:(-x[1], len(x[0])))
            rep,vol=g[0]
            rows.append({"keyword":rep,"volume":vol,"variants":len(g),
                         "variant_list":"; ".join(k for k,_ in g[1:][:6])})
        rows.sort(key=lambda r:-r["volume"])
        dedup[mk]=rows
        summary[mk]={"raw_rows":len(seen),"raw_volume":sum(seen.values()),
                     "unique":len(rows),"dedup_volume":sum(r["volume"] for r in rows)}
    json.dump(dedup, open("keywords_dedup.json","w",encoding="utf8"), ensure_ascii=False)
    print("\nMKT   raw kw  raw vol   unique  dedup vol  inflation", file=sys.stderr)
    tr=td=0
    for mk in ["SG","TH","AU","TW","HK"]:
        s=summary[mk]; tr+=s["raw_volume"]; td+=s["dedup_volume"]
        print(f"{mk:4}{s['raw_rows']:>8,}{s['raw_volume']:>10,}{s['unique']:>9,}{s['dedup_volume']:>11,}"
              f"{(s['raw_volume']/s['dedup_volume']-1)*100:>10.0f}%", file=sys.stderr)
    print(f"ALL {'':>7}{tr:>10,}{'':>9}{td:>11,}{(tr/td-1)*100:>10.0f}%", file=sys.stderr)
    json.dump(summary, open("keywords_summary.json","w",encoding="utf8"))

if __name__=="__main__": main()
