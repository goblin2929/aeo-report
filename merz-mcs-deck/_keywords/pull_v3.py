# -*- coding: utf-8 -*-
"""v3 universe: non-surgical lifting category INCLUDING competitor product names.
Symmetric seed structure per market: Merz brand + generic modality + competitor products,
in that market's own language. Deduplicated by token-sorted fingerprint; noise filtered."""
import sys, json, collections, re
sys.path.insert(0, '.')
import pull_keywords as P

SEEDS = {
 "SG": ("Singapore","English",
        ["ultherapy","ultherapy prime","hifu","thermage","ultraformer","sofwave","skin tightening treatment"]),
 "AU": ("Australia","English",
        ["ultherapy","ultherapy prime","hifu","thermage","ultraformer","sofwave","skin tightening treatment"]),
 "TH": ("Thailand","Thai",
        ["ultherapy","ultherapy prime","hifu","thermage","ultraformer","ยกกระชับผิวหน้า","ร้อยไหม"]),
 "TW": ("Taiwan","Chinese (Traditional)",
        ["ultherapy","音波拉提","電波拉皮","海芙音波","鳳凰電波","埋線拉提","hifu"]),
 "HK": ("Hong Kong","Chinese (Traditional)",
        ["ultherapy","超聲刀","美版超聲刀","hifu","熱瑪吉","ultraformer","thermage"]),
}

BRANDPROD = ['ultherapy','ulthera','merz','thermage','ultraformer','sofwave','oligio','emface',
             'medicube','超聲刀','音波','電波','鳳凰','海芙','熱瑪吉','埋線','hifu','mfu','mmfu']
TREAT_EN = ['skin tightening','tightening','face lift','facelift','facial lift','lifting','lift',
            'collagen','jowl','double chin','brow','neck','nasolabial','ultrasound','radio frequency',
            'sagging','laxity','anti aging','anti-aging','wrinkle','firming']
TREAT_CJK = ['拉提','拉皮','緊膚','緊緻','下垂','鬆弛','輪廓','法令紋','雙下巴','膠原','抗老','皺紋','緊實','醫美']
TREAT_TH = ['ยกกระชับ','หน้า','ผิว','ร้อยไหม','เหนียง','ริ้วรอย','คอลลาเจน']
BLOCK = ['提拉米蘇','提拉米苏','皮拉提斯','普拉提','布加拉提','拉提斯','pilates','tiramisu','bugatti',
         '咖啡','蛋糕','千層','ตีรามิสุ']

def keep(k):
    lo = k.lower()
    if any(b in lo or b in k for b in BLOCK): return False
    if any(b in lo or b in k for b in BRANDPROD): return True
    if any(t in lo for t in TREAT_EN): return True
    if any(t in k for t in TREAT_CJK): return True
    if any(t in k for t in TREAT_TH): return True
    return False

def main():
    c = P.creds(); out={}; summ={}
    for mk,(loc,lang,seeds) in SEEDS.items():
        seen={}
        for s in seeds:
            t=P.post([{"keyword":s,"location_name":loc,"language_name":lang,"limit":1000,
                       "include_serp_info":False,"exact_match":False}], c, f"{mk}:{s}")
            items=(t.get("result") or [{}])[0].get("items") or []
            for it in items:
                kw=it.get("keyword"); v=(it.get("keyword_info") or {}).get("search_volume")
                if kw and v and (kw not in seen or v>seen[kw]): seen[kw]=v
            print(f"  {mk} '{s}': {len(items)} items, unique {len(seen)}", flush=True)
        filt={k:v for k,v in seen.items() if keep(k)}
        g=collections.defaultdict(list)
        for kw,v in filt.items(): g[P.fingerprint(kw)].append((kw,v))
        rows=[]
        for fpk,grp in g.items():
            grp.sort(key=lambda x:(-x[1], len(x[0])))
            rows.append({"keyword":grp[0][0],"volume":grp[0][1],"variants":len(grp),
                         "variant_list":"; ".join(k for k,_ in grp[1:][:6])})
        rows.sort(key=lambda r:-r["volume"])
        out[mk]=rows
        summ[mk]={"pulled":len(seen),"pulled_vol":sum(seen.values()),
                  "kept":len(filt),"kept_vol":sum(filt.values()),
                  "uniq":len(rows),"dedup_vol":sum(r["volume"] for r in rows)}
        print(f"{mk}: pulled {len(seen)} / {sum(seen.values()):,} -> filtered {len(filt)} -> "
              f"dedup {len(rows)} / {sum(r['volume'] for r in rows):,}", flush=True)
    json.dump(out, open("keywords_v3.json","w",encoding="utf8"), ensure_ascii=False)
    json.dump(summ, open("summary_v3.json","w"), indent=1)
    print("\nDONE", flush=True)

if __name__=="__main__": main()
