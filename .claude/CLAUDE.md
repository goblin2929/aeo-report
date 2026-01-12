# GoFreight AEO Report Project

## Client
GoFreight - Freight forwarding software

## Data Sources

### Google Search Console
- Site URL: `sc-domain:gofreight.com`
- Domains: gofreight.com, archive.gofreight.com
- MCP Tool: `mcp__google-search-console__get_performance_data`

### Google Analytics 4
- Property ID: `373075091`
- Quota Project: `seo-agency-478605`
- Auth: `gcloud auth application-default print-access-token`

### Content Tracker (Google Sheet)
- Spreadsheet ID: `1D7MDm4_4HpuIfjUe2CBTYat2AoTWRFLK2XgGBI8gpUc`
- Sheet Name: `Novastacks Content delivery Tracker`
- MCP Tool: `mcp__google-sheets__get_sheet_data`

### Workduo AEO
- Project ID: `cmhk59aw9001mlo33c3t8n3rj`
- Access: Manual screenshot (API auth unreliable)
- Screenshot location: User's Desktop

## Subfolders to Analyze
| Path | Name |
|------|------|
| /blog | Blog |
| /solutions | Solutions |
| /customers | Customers |
| /pricing | Pricing |
| /get-demo | Get Demo |

## Competitors to Track
1. CargoWise
2. Magaya Supply Chain
3. Descartes Forwarder Enterprise
4. Shipthis

---

## Report Generation Workflow

When asked to generate a report for any period:

### Step 1: Collect GSC Data
```
mcp__google-search-console__get_performance_data
- site_url: "sc-domain:gofreight.com"
- start_date: [period start]
- end_date: [period end]
- row_limit: 1000
```
Run 4 queries:
1. No dimensions → site-level totals
2. dimensions: ["page"] → subfolder analysis
3. dimensions: ["query"] → top keywords
4. dimensions: ["query", "page"] → keyword ranking URLs

Also run for comparison period (previous period of same length).

### Step 2: Collect GA4 Data
Query GA4 API for:
- Sessions by pagePath
- Form start events (eventName = "form_start")
- Form submit events (eventName = "form_submit")

### Step 3: Collect Content Tracker Data
```
mcp__google-sheets__get_sheet_data
- spreadsheet_id: "1D7MDm4_4HpuIfjUe2CBTYat2AoTWRFLK2XgGBI8gpUc"
- sheet: "Novastacks Content delivery Tracker"
- range: "A1:S50"
```
Filter by Status column:
- "Published" → Deliverables Shipped
- "Gofreight Approved yet to Publish" → Pending Publication

### Step 4: Get AEO Data
Ask user for Workduo screenshot location, then read image to extract:
- Visibility %
- Share of Voice %
- Average Position
- Competitive Rank

### Step 5: Calculate Metrics
- MoM Change: (Current - Previous) ÷ Previous × 100
- % of Total: Subfolder ÷ Site Total × 100
- Form Start Rate: Form Starts ÷ Sessions × 100
- Conversion Rate: Form Submits ÷ Sessions × 100
- Completion Rate: Form Submits ÷ Form Starts × 100

### Step 6: Generate HTML Report
- Use Novastacks brand styling (from global CLAUDE.md)
- Save as `gofreight_[start_date]_to_[end_date]_report.html`
- Do NOT overwrite index.html (each report gets its own URL)

### Step 7: User Validation (REQUIRED)
Present report to user for review before publishing. User must verify:
- All metrics match source data
- Content status is accurate
- No missing sections or tables

### Step 8: Publish to GitHub (AFTER USER APPROVAL ONLY)
Only after user explicitly confirms accuracy:
```bash
git add gofreight_[date_range]_report.html
git commit -m "Add [date range] AEO report"
git push origin main
```

**File Naming** (include full date range):
- `gofreight_jan_1_10_2026_report.html` → Jan 1-10, 2026
- `gofreight_jan_11_20_2026_report.html` → Jan 11-20, 2026
- `gofreight_dec_2025_report.html` → Full month December 2025

**IMPORTANT**: Never push without explicit user validation.

---

## Validation Rules (MUST CHECK)

1. **Subfolder totals**: Sum of subfolder clicks ≈ site total clicks
2. **% calculations**: Always use SITE TOTAL as denominator
3. **Content status**: Verify "Published" items are actually live
4. **AEO data**: Must match Workduo screenshot exactly
5. **No fabricated data**: Every metric traced to actual source

## Common Mistakes to Avoid

- Don't mark content as "shipped" if status is "Approved yet to Publish"
- Don't invert AEO position (lower = better, 1.5 beats 3.1)
- Don't mix archive.gofreight.com with main site data
- Don't estimate or fabricate AEO metrics

---

## Output Files
- Report: `gofreight_{period}_report.html`
- GitHub Pages: `index.html`
- Data archive: `data/` folder
