const { google } = require('googleapis');
const { getAuthenticatedClient } = require('./auth');
const fs = require('fs');
const SITE='sc-domain:gofreight.com';
// keyword -> target match: {slug} where '' means homepage (path '/')
const MAP = [
  ['freight forwarding crm','best-logistics-crm-software'],
  ['logistics crm software','best-logistics-crm-software'],
  ['best tms software','best-tms-software'],
  ['freight management system','best-freight-management-software'],
  ['freight management software',''],
  ['freight forwarding software',''],
  ['freight forwarder software',''],
  ['best freight management software','best-freight-management-software'],
  ['freight software','best-freight-management-software'],
  ['freight tracking software','best-freight-management-software'],
];
async function pull(sc,kw,s,e){
  const filter=[{filters:[
    {dimension:'country',operator:'equals',expression:'usa'},
    {dimension:'query',operator:'equals',expression:kw},
  ]}];
  const res=await sc.searchanalytics.query({siteUrl:SITE,requestBody:{startDate:s,endDate:e,dimensions:['page'],rowLimit:1000,dimensionFilterGroups:filter}});
  return res.data.rows||[];
}
function matchRow(rows,slug){
  for(const r of rows){
    const u=new URL(r.keys[0]); const p=u.pathname;
    if(slug===''){ if(p==='/'&&u.hostname==='gofreight.com') return r; }
    else if(p.includes('/blog/'+slug)) return r;
  }
  return null;
}
(async()=>{
  const auth=await getAuthenticatedClient();const sc=google.searchconsole({version:'v1',auth});
  const out={};
  for(const [kw,slug] of MAP){
    const jr=await pull(sc,kw,'2026-07-01','2026-07-31');
    const mr=await pull(sc,kw,'2026-06-01','2026-06-30');
    const j=matchRow(jr,slug), m=matchRow(mr,slug);
    out[kw]={slug, target: slug===''?'https://gofreight.com/':('https://gofreight.com/blog/'+slug),
      julPos:j?+j.position.toFixed(1):null, junPos_:m?+m.position.toFixed(1):null,
      julImpr:j?j.impressions:0, junImpr_:m?m.impressions:0,
      julClicks:j?j.clicks:0, junClicks_:m?m.clicks:0};
    console.error(`${kw} -> ${slug||'homepage'}: May ${out[kw].junPos_} -> Jun ${out[kw].julPos} (US impr Jun ${out[kw].julImpr})`);
  }
  fs.writeFileSync('d:/tmp/gf-core-page-us-july.json',JSON.stringify(out,null,2));
  console.error('WROTE d:/tmp/gf-core-page-us-july.json');
})().catch(e=>{console.error('ERR',e.message);process.exit(1);});
