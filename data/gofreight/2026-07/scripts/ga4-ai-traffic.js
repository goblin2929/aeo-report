/**
 * GA4 AI-referral sessions pull for GoFreight (property 373075091), via the
 * OAuth token created by ga4-auth.js. Mirrors ga4_ai_traffic_pull.py's source
 * definition (sessionSource matching the AI_PAT regex), daily -> ISO weekly.
 *
 * Usage:  node scripts/ga4-ai-traffic.js [startDate] [endDate]
 *   defaults: 2026-01-01 .. today
 * Output: d:/tmp/ga4_ai_traffic.json  (weekly + monthly + by-source)
 */
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const PROPERTY = '373075091';
const CREDENTIALS_DIR = path.join(__dirname, '..', 'input', 'credentials');
const PROFILES_PATH = path.join(CREDENTIALS_DIR, 'gsc-profiles.json');
const TOKEN_FILE = path.join(CREDENTIALS_DIR, 'ga4-google-tokens.json');
const REDIRECT_URI = 'http://localhost:3000/oauth2callback';
const AI_PAT = /(chatgpt|chat\.openai|openai\.com|perplexity|gemini\.google|bard\.google|claude\.ai|anthropic|copilot|you\.com|poe\.com|deepseek|grok\.com|x\.ai|mistral|phind|searchgpt|edgeservices|aimode)/i;

const START = process.argv[2] || '2026-01-01';
const END = process.argv[3] || new Date().toISOString().slice(0, 10);

function isoWeekMonday(dateStr) {
  const d = new Date(dateStr + 'T00:00:00Z');
  const dow = d.getUTCDay();
  d.setUTCDate(d.getUTCDate() + (dow === 0 ? -6 : 1 - dow));
  return d.toISOString().slice(0, 10);
}

async function main() {
  if (!fs.existsSync(TOKEN_FILE)) throw new Error(`No GA4 token. Run: node scripts/ga4-auth.js`);
  const profiles = JSON.parse(fs.readFileSync(PROFILES_PATH, 'utf-8'));
  const p = profiles['novastacks'];
  const oauth2Client = new google.auth.OAuth2(p.client_id, p.client_secret, REDIRECT_URI);
  const tokens = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf-8'));
  oauth2Client.setCredentials(tokens);
  oauth2Client.on('tokens', (t) => fs.writeFileSync(TOKEN_FILE, JSON.stringify({ ...tokens, ...t }, null, 2)));

  const analyticsdata = google.analyticsdata({ version: 'v1beta', auth: oauth2Client });
  const resp = await analyticsdata.properties.runReport({
    property: `properties/${PROPERTY}`,
    requestBody: {
      dateRanges: [{ startDate: START, endDate: END }],
      dimensions: [{ name: 'date' }, { name: 'sessionSource' }],
      metrics: [{ name: 'sessions' }],
      limit: 250000,
    },
  });

  const daily = {}, bySource = {};
  for (const row of resp.data.rows || []) {
    const d = row.dimensionValues[0].value;
    const src = row.dimensionValues[1].value;
    const s = parseInt(row.metricValues[0].value, 10);
    if (AI_PAT.test(src)) {
      daily[d] = (daily[d] || 0) + s;
      bySource[src] = (bySource[src] || 0) + s;
    }
  }
  const weekly = {}, monthly = {};
  for (const [d, s] of Object.entries(daily)) {
    const iso = `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`;
    const wk = isoWeekMonday(iso);
    weekly[wk] = (weekly[wk] || 0) + s;
    const mo = `${d.slice(0, 4)}-${d.slice(4, 6)}`;
    monthly[mo] = (monthly[mo] || 0) + s;
  }
  const out = {
    meta: { property: PROPERTY, range: `${START}..${END}`,
      source: 'GA4 runReport date+sessionSource, sessions, AI_PAT filter' },
    weekly: Object.fromEntries(Object.entries(weekly).sort()),
    monthly: Object.fromEntries(Object.entries(monthly).sort()),
    by_source_total: Object.fromEntries(Object.entries(bySource).sort((a, b) => b[1] - a[1])),
  };
  fs.writeFileSync('d:/tmp/ga4_ai_traffic.json', JSON.stringify(out, null, 2));
  console.log('MONTHLY:', JSON.stringify(out.monthly));
  console.log('WEEKLY:', JSON.stringify(out.weekly));
  console.log('WROTE d:/tmp/ga4_ai_traffic.json');
}
main().catch((e) => { console.error('ERR', e.message); process.exit(1); });
