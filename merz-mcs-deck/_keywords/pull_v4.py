# -*- coding: utf-8 -*-
"""v4 universe — the definition Tina set:
   IN : Merz brand terms, generic modality terms (HIFU / ultrasound lifting / skin tightening),
        and face-lift SYMPTOM queries (sagging, jowls, double chin, wrinkles, laxity).
   OUT: queries whose only product reference is a COMPETITOR (Thermage, Ultraformer, Sofwave,
        鳳凰電波, 海芙音波, 熱瑪吉 ...). A comparison that names Ultherapy stays in.
   Seeds are structurally IDENTICAL across all five markets — brand, brand, generic HIFU,
   market ultrasound-lifting term, market tightening term, market sagging term — so the
   markets are comparable to each other. That symmetry is the point.
"""
import sys, json, collections
sys.path.insert(0,'.')
import pull_keywords as P

SEEDS = {
 "SG": ("Singapore","English",
        ["ultherapy","ultherapy prime","hifu","ultrasound skin lifting","skin tightening treatment","sagging skin treatment"]),
 "AU": ("Australia","English",
        ["ultherapy","ultherapy prime","hifu","ultrasound skin lifting","skin tightening treatment","sagging skin treatment"]),
 "TH": ("Thailand","Thai",
        ["ultherapy","ultherapy prime","hifu","ยกกระชับผิวหน้า","กระชับผิว","ผิวหย่อนคล้อย"]),
 "TW": ("Taiwan","Chinese (Traditional)",
        ["ultherapy","ultherapy prime","hifu","音波拉提","臉部緊緻","臉部鬆弛"]),
 "HK": ("Hong Kong","Chinese (Traditional)",
        ["ultherapy","ultherapy prime","hifu","超聲刀","面部緊緻","面部鬆弛"]),
}

MERZ = ['ultherapy','ulthera','merz','超聲刀','音波拉提']   # market names for Merz's own modality
COMPET = ['thermage','ultraformer','sofwave','oligio','emface','morpheus','profhilo','tixel',
          'medicube','鳳凰電波','鳳凰','海芙','熱瑪吉','酷塑','鈴鐺針']
GENERIC = ['hifu','mfu','mmfu','ultrasound','radio frequency','skin tightening','tightening',
           'face lift','facelift','facial lift','lifting','lift','firming','collagen',
           '拉提','拉皮','緊膚','緊緻','緊實','膠原','醫美','ยกกระชับ','กระชับ','ร้อยไหม']
SYMPTOM = ['sagging','laxity','jowl','double chin','turkey neck','wrinkle','fine lines','droopy',
           'eyelid','brow','nasolabial','marionette','anti aging','anti-aging','aging',
           '鬆弛','下垂','法令紋','雙下巴','皺紋','抗老','輪廓','眼皮','頸紋','木偶紋',
           'หย่อนคล้อย','เหนียง','ริ้วรอย','ใต้คาง','คิ้ว']
BLOCK = ['提拉米蘇','提拉米苏','皮拉提斯','普拉提','布加拉提','拉提斯','pilates','tiramisu',
         'bugatti','咖啡','蛋糕','千層']

def classify(k):
    lo=k.lower()
    if any(b in lo or b in k for b in BLOCK): return None
    has_merz  = any(m in lo or m in k for m in MERZ)
    has_comp  = any(c in lo or c in k for c in COMPET)
    has_gen   = any(g in lo or g in k for g in GENERIC)
    has_symp  = any(s in lo or s in k for s in SYMPTOM)
    # competitor-only query -> out
    if has_comp and not has_merz: return None
    if has_merz or has_gen or has_symp: return True
    return None

def main():
    c=P.creds(); out={}; summ={}
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
        filt={k:v for k,v in seen.items() if classify(k)}
        g=collections.defaultdict(list)
        for kw,v in filt.items(): g[P.fingerprint(kw)].append((kw,v))
        rows=[]
        for fpk,grp in g.items():
            grp.sort(key=lambda x:(-x[1],len(x[0])))
            rows.append({"keyword":grp[0][0],"volume":grp[0][1],"variants":len(grp),
                         "variant_list":"; ".join(k for k,_ in grp[1:][:6])})
        rows.sort(key=lambda r:-r["volume"])
        out[mk]=rows
        summ[mk]={"pulled":len(seen),"pulled_vol":sum(seen.values()),"kept":len(filt),
                  "uniq":len(rows),"dedup_vol":sum(r["volume"] for r in rows)}
        print(f"{mk}: pulled {len(seen)}/{sum(seen.values()):,} -> kept {len(filt)} -> "
              f"dedup {len(rows)}/{sum(r['volume'] for r in rows):,}", flush=True)
    json.dump(out, open("keywords_v4.json","w",encoding="utf8"), ensure_ascii=False)
    json.dump(summ, open("summary_v4.json","w"), indent=1)
    print("\nDONE", flush=True)

if __name__=="__main__": main()
