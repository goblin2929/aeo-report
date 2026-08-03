const { google } = require('googleapis');
const { getAuthenticatedClient } = require('./auth');
const SITE='sc-domain:gofreight.com';
async function pull(sc,kw,s,e){
  const filter=[{filters:[{dimension:'country',operator:'equals',expression:'usa'},{dimension:'query',operator:'equals',expression:kw}]}];
  const r=await sc.searchanalytics.query({siteUrl:SITE,requestBody:{startDate:s,endDate:e,dimensions:['page'],rowLimit:1000,dimensionFilterGroups:filter}});
  return (r.data.rows||[]).map(x=>({url:x.keys[0],pos:+x.position.toFixed(1),impr:x.impressions,clicks:x.clicks})).sort((a,b)=>a.pos-b.pos);
}
(async()=>{
  const auth=await getAuthenticatedClient();const sc=google.searchconsole({version:'v1',auth});
  for(const [label,s,e] of [['JULY','2026-07-01','2026-07-31'],['JUNE','2026-06-01','2026-06-30']]){
    console.error(`\n=== "freight management software" (US) — ${label} — pages ranking ===`);
    for(const r of await pull(sc,'freight management software',s,e)) console.error(`  pos ${String(r.pos).padStart(5)}  impr ${String(r.impr).padStart(5)}  clicks ${r.clicks}  ${r.url}`);
  }
})().catch(e=>{console.error('ERR',e.message);process.exit(1);});
