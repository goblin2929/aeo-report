const { google } = require('googleapis');
const { getAuthenticatedClient } = require('./auth');
const fs = require('fs');
const SITE='sc-domain:gofreight.com';
const PRIMARY=[{filters:[{dimension:'page',operator:'contains',expression:'https://gofreight.com/'}]}];
async function pull(sc,s,e){const all=[];let r=0;while(true){const res=await sc.searchanalytics.query({siteUrl:SITE,requestBody:{startDate:s,endDate:e,dimensions:['page'],rowLimit:25000,startRow:r,dimensionFilterGroups:PRIMARY}});const rows=res.data.rows||[];all.push(...rows);if(rows.length<25000)break;r+=25000;}return all;}
function norm(u){u=u.trim().split('#')[0].split('?')[0];if(u.endsWith('/')&&u.length>'https://gofreight.com/'.length)u=u.replace(/\/+$/,'');return u.toLowerCase();}
(async()=>{
  const auth=await getAuthenticatedClient();const sc=google.searchconsole({version:'v1',auth});
  const jun=await pull(sc,'2026-07-01','2026-07-31');const may=await pull(sc,'2026-06-01','2026-06-30');
  const m={};
  for(const r of jun){const k=norm(r.keys[0]);(m[k]=m[k]||{jul:0,jun:0}).jul+=r.clicks;}
  for(const r of may){const k=norm(r.keys[0]);(m[k]=m[k]||{jul:0,jun:0}).jun+=r.clicks;}
  fs.writeFileSync('d:/tmp/gf-page-clicks-july.json',JSON.stringify(m));
  console.error('pages:',Object.keys(m).length);
})().catch(e=>{console.error('ERR',e.message);process.exit(1);});
