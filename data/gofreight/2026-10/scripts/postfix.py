import re,sys
for fn in ['/Users/ekiriandra/seo-projects/aeo-report/gofreight_september_2026_report.html','/Users/ekiriandra/seo-projects/novastacks/clients/gofreight/output/reports/gofreight_september_2026_report.html']:
    h=open(fn,encoding='utf-8').read()
    head,rest=h.split('<body>',1); body,tail=rest.split('<script>',1)
    R=[('>—<','>no<'),('<td class="num">—</td>','<td class="num"></td>'),
       ('Core Keyword Tracking — Commercial Cluster','Core Keyword Tracking: Commercial Cluster'),
       ('AEO Metrics — Month over Month','AEO Metrics: Month over Month'),
       ('Canonical static panel</b> — the full commercial-cluster set','Canonical static panel</b>: the full commercial cluster set'),
       ('(candidate terms — CRM / TMS / tracking)','(candidate terms: CRM / TMS / tracking)'),
       ('freight-management / forwarding-software cluster','freight management / forwarding software cluster'),
       ('best-ranking','best ranking'),
       (' — ',', '),('non-brand','non brand'),('Non-branded','Non branded'),('WorkDuo-tracked','WorkDuo tracked'),('query-dim','query dimension'),
       ('Non-brand','Non brand'),('self-mention','self mention'),('date-dim','date dimension'),('page-dim','page dimension'),('occurrence-recounted','occurrence recounted'),('AI-referral','AI referral'),('source/landing-page','source / landing page'),('country=usa','country = usa')]
    for a,b in R: body=body.replace(a,b)
    # td placeholder em dash in Top15 "In Click Top 30?" column
    body=body.replace('style="color:var(--slate-5)">no<','style="color:var(--slate-5)">no<')
    open(fn,'w',encoding='utf-8').write(head+'<body>'+body+'<script>'+tail)
    txt=re.sub(r'<[^>]+>',' ',re.sub(r'<style>.*?</style>','',body,flags=re.S))
    left=[txt[max(0,m.start()-40):m.end()+30] for m in re.finditer('[—–]',txt)]
    print(fn.split('/')[-3], 'dashes left:',len(left)); [print('  ',repr(x)) for x in left[:8]]
    print('  hyphen tokens (non-URL-ish):',sorted(set(t for t in re.findall(r'\b[A-Za-z]+-[A-Za-z]+\b',txt) if t.lower() in {'real-time','cloud-based','non-brand','top-line','month-over-month','buying-intent','single-question','cross-page','high-value'})))
