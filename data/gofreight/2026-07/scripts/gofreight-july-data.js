const { google } = require('googleapis');
const { getAuthenticatedClient } = require('./auth');
const fs = require('fs');
const SITE = 'sc-domain:gofreight.com';
const JUL = { s: '2026-07-01', e: '2026-07-31' };
const JUN = { s: '2026-06-01', e: '2026-06-30' };
const PRIMARY = [{ filters: [{ dimension: 'page', operator: 'contains', expression: 'https://gofreight.com/' }] }];

async function fetchGSC(sc, s, e, dims, filter) {
  const all = []; let start = 0;
  while (true) {
    const body = { startDate: s, endDate: e, dimensions: dims, rowLimit: 25000, startRow: start };
    if (filter) body.dimensionFilterGroups = filter;
    const r = await sc.searchanalytics.query({ siteUrl: SITE, requestBody: body });
    const rows = r.data.rows || []; all.push(...rows);
    if (rows.length < 25000) break; start += 25000;
  }
  return all;
}
function agg(rows) { const m = new Map(); for (const r of rows) { const k = r.keys[0]; const e = m.get(k) || { clicks: 0, impressions: 0, posSum: 0 }; e.clicks += r.clicks; e.impressions += r.impressions; e.posSum += r.position * r.impressions; m.set(k, e); } for (const [, v] of m) v.avgPos = v.impressions ? v.posSum / v.impressions : 0; return m; }
function totals(rows) { let c = 0, i = 0, ps = 0; for (const r of rows) { c += r.clicks; i += r.impressions; ps += r.position * r.impressions; } return { clicks: c, impressions: i, avgPos: i ? ps / i : 0, ctr: i ? c / i * 100 : 0 }; }
function subfolder(url) { try { const u = new URL(url); const h = u.hostname; const p = u.pathname; if (h.startsWith('support.')) return 'Support'; if (h.startsWith('api.')) return 'API'; if (h.startsWith('archive.')) return 'Archive'; if (p === '/' || p === '') return 'Homepage'; if (p.startsWith('/blog')) return 'Blog'; if (p.startsWith('/glossary')) return 'Glossary'; if (p.startsWith('/solutions') || p.startsWith('/solution')) return 'Solutions'; if (p.startsWith('/pricing')) return 'Pricing'; if (p.startsWith('/product') || p.startsWith('/features')) return 'Product'; return 'Other'; } catch { return 'Other'; } }
function classifyQuery(q) { const s = q.toLowerCase(); if (s === 'gofreight' || s === 'go freight') return 'exact'; if (s.includes('gofreight') || s.includes('go freight')) return 'brandedRelated'; return 'nonBranded'; }
function weekMonday(d) { const x = new Date(d + 'T00:00:00Z'); const dow = x.getUTCDay(); x.setUTCDate(x.getUTCDate() + (dow === 0 ? -6 : 1 - dow)); return x.toISOString().slice(0, 10); }

(async () => {
  const auth = await getAuthenticatedClient(); const sc = google.searchconsole({ version: 'v1', auth });
  console.error('page/query pulls...');
  const julP = await fetchGSC(sc, JUL.s, JUL.e, ['page'], PRIMARY);
  const junP = await fetchGSC(sc, JUN.s, JUN.e, ['page'], PRIMARY);
  const julQ = agg(await fetchGSC(sc, JUL.s, JUL.e, ['query']));   // unfiltered for brand segments (matches prior methodology)
  const junQ = agg(await fetchGSC(sc, JUN.s, JUN.e, ['query']));
  const julPa = agg(julP), junPa = agg(junP);
  const julTot = totals(julP), junTot = totals(junP);

  const topPages = [...julPa.entries()].map(([k, v]) => ({ url: k, julClicks: v.clicks, julImpr: v.impressions, julPos: v.avgPos, junClicks: (junPa.get(k) || {}).clicks || 0, junImpr: (junPa.get(k) || {}).impressions || 0 })).sort((a, b) => b.julClicks - a.julClicks).slice(0, 30);

  const subAgg = (pm) => { const m = new Map(); for (const [url, v] of pm) { const sf = subfolder(url); const e = m.get(sf) || { clicks: 0, impressions: 0 }; e.clicks += v.clicks; e.impressions += v.impressions; m.set(sf, e); } return m; };
  const julS = subAgg(julPa), junS = subAgg(junPa);
  const subs = [...new Set([...julS.keys(), ...junS.keys()])].map(k => ({ name: k, julClicks: (julS.get(k) || {}).clicks || 0, junClicks: (junS.get(k) || {}).clicks || 0, julImpr: (julS.get(k) || {}).impressions || 0, junImpr: (junS.get(k) || {}).impressions || 0 })).sort((a, b) => b.julClicks - a.julClicks);

  const segAgg = (qm) => { const s = { exact: { c: 0, i: 0 }, brandedRelated: { c: 0, i: 0 }, nonBranded: { c: 0, i: 0 } }; for (const [q, v] of qm) { const c = classifyQuery(q); s[c].c += v.clicks; s[c].i += v.impressions; } return s; };
  const julSeg = segAgg(julQ), junSeg = segAgg(junQ);

  // weekly clicks + brand (includingRegex), Jan 5 through Aug 2
  console.error('weekly...');
  const REGEX = '(?i)go\\s*-?\\s*freight|gofright';
  const dTot = await fetchGSC(sc, '2026-01-01', '2026-08-02', ['date'], PRIMARY);
  const dBrand = await fetchGSC(sc, '2026-01-01', '2026-08-02', ['date'], [{ filters: [{ dimension: 'page', operator: 'contains', expression: 'https://gofreight.com/' }, { dimension: 'query', operator: 'includingRegex', expression: REGEX }] }]);
  const bByDate = new Map(dBrand.map(r => [r.keys[0], r.clicks]));
  const wk = {};
  for (const r of dTot) { const w = weekMonday(r.keys[0]); (wk[w] = wk[w] || { t: 0, b: 0 }).t += r.clicks; wk[w].b += (bByDate.get(r.keys[0]) || 0); }
  const weekly = Object.entries(wk).sort((a, b) => a[0].localeCompare(b[0])).map(([w, v]) => ({ week: w, total: v.t, nonBrand: v.t - v.b }));

  fs.writeFileSync('d:/tmp/gofreight-july-data.json', JSON.stringify({ julTot, junTot, julSeg, junSeg, subfolders: subs, topPages, weekly }, null, 2));
  console.error(`JUL: ${julTot.clicks} clicks, ${Math.round(julTot.impressions)} impr, pos ${julTot.avgPos.toFixed(2)}, CTR ${julTot.ctr.toFixed(3)}%`);
  console.error(`JUN: ${junTot.clicks} clicks, ${Math.round(junTot.impressions)} impr, pos ${junTot.avgPos.toFixed(2)}, CTR ${junTot.ctr.toFixed(3)}%`);
  console.error('Segments JUL:', JSON.stringify(julSeg), 'JUN:', JSON.stringify(junSeg));
  console.error('Subs:', JSON.stringify(subs));
  console.error('WROTE d:/tmp/gofreight-july-data.json');
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
