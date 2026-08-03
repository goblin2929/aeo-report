/**
 * GA4 AI-referral drop analysis: June vs July 2026.
 * Which sources and which landing pages lost AI-referred sessions.
 */
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');
const PROPERTY = '373075091';
const CRED = path.join(__dirname, '..', 'input', 'credentials');
const profiles = JSON.parse(fs.readFileSync(path.join(CRED, 'gsc-profiles.json'), 'utf-8'));
const AI = /(chatgpt|chat\.openai|openai\.com|perplexity|gemini\.google|bard\.google|claude\.ai|anthropic|copilot|you\.com|poe\.com|deepseek|grok\.com|x\.ai|mistral|phind|searchgpt|edgeservices|aimode)/i;

async function run(analyticsdata, dims, s, e) {
  const r = await analyticsdata.properties.runReport({
    property: `properties/${PROPERTY}`,
    requestBody: { dateRanges: [{ startDate: s, endDate: e }], dimensions: dims.map(n => ({ name: n })), metrics: [{ name: 'sessions' }], limit: 100000 },
  });
  return r.data.rows || [];
}
(async () => {
  const p = profiles['novastacks'];
  const oa = new google.auth.OAuth2(p.client_id, p.client_secret, 'http://localhost:3000/oauth2callback');
  oa.setCredentials(JSON.parse(fs.readFileSync(path.join(CRED, 'ga4-google-tokens.json'), 'utf-8')));
  const ad = google.analyticsdata({ version: 'v1beta', auth: oa });
  const months = { jun: ['2026-06-01', '2026-06-30'], jul: ['2026-07-01', '2026-07-31'] };

  // Source-level
  const src = {};
  for (const [m, [s, e]] of Object.entries(months)) {
    for (const row of await run(ad, ['sessionSource'], s, e)) {
      const so = row.dimensionValues[0].value; const n = +row.metricValues[0].value;
      if (AI.test(so)) { src[so] = src[so] || { jun: 0, jul: 0 }; src[so][m] += n; }
    }
  }
  // Landing-page-level (AI sources only)
  const lp = {};
  for (const [m, [s, e]] of Object.entries(months)) {
    for (const row of await run(ad, ['landingPage', 'sessionSource'], s, e)) {
      const page = row.dimensionValues[0].value; const so = row.dimensionValues[1].value; const n = +row.metricValues[0].value;
      if (AI.test(so)) { lp[page] = lp[page] || { jun: 0, jul: 0 }; lp[page][m] += n; }
    }
  }
  const srcArr = Object.entries(src).map(([k, v]) => ({ source: k, ...v, delta: v.jul - v.jun })).sort((a, b) => a.delta - b.delta);
  const lpArr = Object.entries(lp).map(([k, v]) => ({ page: k, ...v, delta: v.jul - v.jun })).sort((a, b) => a.delta - b.delta);
  fs.writeFileSync('d:/tmp/ga4-ai-drop.json', JSON.stringify({ sources: srcArr, landingPages: lpArr }, null, 2));

  const T = (o) => `jun ${o.jun} jul ${o.jul} (${o.delta >= 0 ? '+' : ''}${o.delta})`;
  console.error('=== AI sessions by SOURCE (Jun vs Jul) ===');
  for (const s of srcArr) console.error(`  ${T(s).padEnd(28)} ${s.source}`);
  const junTot = srcArr.reduce((a, b) => a + b.jun, 0), julTot = srcArr.reduce((a, b) => a + b.jul, 0);
  console.error(`  TOTAL jun ${junTot} jul ${julTot} (${julTot - junTot})`);
  console.error('=== Biggest landing-page DROPS (Jun vs Jul) ===');
  for (const l of lpArr.filter(x => x.delta < 0).slice(0, 15)) console.error(`  ${T(l).padEnd(28)} ${l.page}`);
  console.error('=== Biggest landing-page GAINS ===');
  for (const l of [...lpArr].reverse().filter(x => x.delta > 0).slice(0, 8)) console.error(`  ${T(l).padEnd(28)} ${l.page}`);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
