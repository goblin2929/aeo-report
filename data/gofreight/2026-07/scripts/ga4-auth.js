/**
 * GA4 OAuth setup (Option B) — mirrors the GSC auth.js pattern.
 *
 * Reuses the `novastacks` OAuth client (client_id/secret from gsc-profiles.json)
 * but requests the Google Analytics read scope and saves to its OWN token file
 * (ga4-google-tokens.json) so it never clobbers the GSC token.
 *
 * One-time setup:
 *   node scripts/ga4-auth.js
 * Then authorize in the browser with a Google account that has at least
 * "Viewer" on GA4 property 373075091 (GoFreight).
 *
 * Requires: the Google Analytics Data API enabled in the OAuth client's
 * Cloud project, and http://localhost:3000/oauth2callback registered as a
 * redirect URI (already true for the novastacks client used by GSC).
 */
const { google } = require('googleapis');
const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const CREDENTIALS_DIR = path.join(__dirname, '..', 'input', 'credentials');
const PROFILES_PATH = path.join(CREDENTIALS_DIR, 'gsc-profiles.json');
const REDIRECT_URI = 'http://localhost:3000/oauth2callback';
const TOKEN_FILE = path.join(CREDENTIALS_DIR, 'ga4-google-tokens.json');
const SCOPES = ['https://www.googleapis.com/auth/analytics.readonly'];

// Reuse the novastacks OAuth client (already has localhost:3000 redirect registered)
const SOURCE_PROFILE = process.argv[2] || 'novastacks';

async function main() {
  const profiles = JSON.parse(fs.readFileSync(PROFILES_PATH, 'utf-8'));
  const p = profiles[SOURCE_PROFILE];
  if (!p || !p.client_id || !p.client_secret) {
    throw new Error(`Profile "${SOURCE_PROFILE}" missing client_id/client_secret in ${PROFILES_PATH}`);
  }
  const oauth2Client = new google.auth.OAuth2(p.client_id, p.client_secret, REDIRECT_URI);

  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent',
  });
  console.log('\n  GA4 authorization (property 373075091)');
  console.log('  Sign in with a Google account that has Viewer on the GoFreight GA4 property.');
  console.log('  If the browser does not open, visit:\n');
  console.log(`  ${authUrl}\n`);
  if (process.platform === 'win32') exec(`cmd.exe /c start "" "${authUrl}"`);
  else exec(`${process.platform === 'darwin' ? 'open' : 'xdg-open'} "${authUrl}"`);

  const code = await new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const parsed = url.parse(req.url, true);
      if (parsed.pathname === '/oauth2callback') {
        if (parsed.query.code) {
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end('<h2>GA4 authorization successful.</h2><p>You can close this tab.</p>');
          server.close();
          resolve(parsed.query.code);
        } else {
          res.writeHead(400); res.end('No code'); server.close();
          reject(new Error('No authorization code received'));
        }
      }
    });
    server.listen(3000, () => console.log('  Waiting for authorization on http://localhost:3000 ...'));
    setTimeout(() => { server.close(); reject(new Error('Timed out after 5 min')); }, 300000);
  });

  const { tokens } = await oauth2Client.getToken(code);
  fs.writeFileSync(TOKEN_FILE, JSON.stringify(tokens, null, 2));
  console.log(`\n  Tokens saved to ${TOKEN_FILE}`);
  console.log('  Now run: node scripts/ga4-ai-traffic.js');
}
main().catch((e) => { console.error('ERR', e.message); process.exit(1); });
