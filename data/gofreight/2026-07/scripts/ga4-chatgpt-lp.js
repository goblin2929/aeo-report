/** ChatGPT-only landing-page sessions, June vs July 2026. */
const { google } = require('googleapis');
const fs = require('fs'); const path = require('path');
const PROPERTY = '373075091';
const CRED = path.join(__dirname, '..', 'input', 'credentials');
const profiles = JSON.parse(fs.readFileSync(path.join(CRED, 'gsc-profiles.json'), 'utf-8'));
const CHATGPT = /(chatgpt|chat\.openai|openai\.com)/i;
async function run(ad, s, e) {
  const r = await ad.properties.runReport({ property: `properties/${PROPERTY}`, requestBody: { dateRanges: [{ startDate: s, endDate: e }], dimensions: [{ name: 'landingPage' }, { name: 'sessionSource' }], metrics: [{ name: 'sessions' }], limit: 100000 } });
  return r.data.rows || [];
}
(async () => {
  const p = profiles['novastacks'];
  const oa = new google.auth.OAuth2(p.client_id, p.client_secret, 'http://localhost:3000/oauth2callback');
  oa.setCredentials(JSON.parse(fs.readFileSync(path.join(CRED, 'ga4-google-tokens.json'), 'utf-8')));
  const ad = google.analyticsdata({ version: 'v1beta', auth: oa });
  const lp = {};
  for (const [m, [s, e]] of Object.entries({ jun: ['2026-06-01', '2026-06-30'], jul: ['2026-07-01', '2026-07-31'] })) {
    for (const row of await run(ad, s, e)) {
      const page = row.dimensionValues[0].value, src = row.dimensionValues[1].value, n = +row.metricValues[0].value;
      if (CHATGPT.test(src)) { lp[page] = lp[page] || { jun: 0, jul: 0 }; lp[page][m] += n; }
    }
  }
  const arr = Object.entries(lp).map(([k, v]) => ({ page: k, ...v, delta: v.jul - v.jun })).sort((a, b) => a.delta - b.delta);
  fs.writeFileSync('d:/tmp/ga4-chatgpt-lp.json', JSON.stringify(arr, null, 2));
  const jn = arr.reduce((a, b) => a + b.jun, 0), jl = arr.reduce((a, b) => a + b.jul, 0);
  console.error(`ChatGPT sessions by landing page — TOTAL jun ${jn} jul ${jl} (${jl - jn})`);
  console.error('=== biggest ChatGPT DROPS ===');
  for (const l of arr.filter(x => x.delta < 0).slice(0, 15)) console.error(`  jun ${String(l.jun).padStart(3)} jul ${String(l.jul).padStart(3)} (${l.delta})  ${l.page}`);
  console.error('=== ChatGPT GAINS ===');
  for (const l of [...arr].reverse().filter(x => x.delta > 0).slice(0, 6)) console.error(`  jun ${String(l.jun).padStart(3)} jul ${String(l.jul).padStart(3)} (+${l.delta})  ${l.page}`);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
