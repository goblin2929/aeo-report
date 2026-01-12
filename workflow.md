# GoFreight AEO Report Workflow

## Overview
This document defines the complete workflow for generating monthly AEO performance reports for GoFreight.

---

## Report Sections (Required)

### 1. Header
- Title: "[Client] AEO Performance Report — [Month Year] Monthly Report"
- Subtitle: "Search Visibility & Traffic Analysis"
- Date range and "Prepared by Novastacks"

### 2. Executive Summary KPIs (4 cards)
| Metric | Source | Calculation |
|--------|--------|-------------|
| Total Clicks | GSC | Sum of daily clicks |
| Total Impressions | GSC | Sum of daily impressions |
| Average CTR | GSC | Total Clicks / Total Impressions × 100 |
| Average Position | GSC | Weighted average from daily data |

Each card shows:
- Current period value
- MoM change (% and absolute)
- Green = positive, Red = negative

### 3. Executive Summary Content
- **Month in Review** (blue callout box): Key narrative summary
- **Deliverables Shipped** (green boxes): Published content by category
- **Pending Publication** (yellow boxes): Approved but not live
- **KPI Outcome Analysis** (green status cards): What worked
- **Critical Issues** (red callout box): Problems requiring attention
- **Next Month Priorities** (dark background section): Focus areas

### 4. Query Segment Breakdown (MoM Variance)
Segment traffic into three groups:
| Segment | Definition |
|---------|------------|
| Exact Brand | query = "gofreight" exactly |
| Branded Related | query contains "gofreight", "go freight", "gofright" |
| Non-Branded | All other queries |

**Required table:**
```
| Segment | Click Δ | % of Change | Impr Δ | % of Change |
|---------|---------|-------------|--------|-------------|
| Exact "gofreight" | +X | X% | +X | X% |
| Branded Related | +X | X% | +X | X% |
| Non-Branded | +X | X% | +X | X% |
| TOTAL | +X | 100% | +X | 100% |
```

**Required visualization:**
- Segment cards showing current values and contribution %
- Contribution bars
- Segment pie chart

### 5. Subfolder Performance Analysis
Group pages by URL path prefix:
| Subfolder | URL Pattern |
|-----------|-------------|
| Homepage | gofreight.com/ (exact) |
| Blog | /blog/* |
| Glossary | /glossary/* |
| Solutions | /solutions/* |
| Pricing | /pricing/* |
| Customers | /customers/* |
| Get Demo | /get-demo/* |
| Archive | archive.gofreight.com/* |
| Support | support.gofreight.com/* |

**Required table columns:**
- Subfolder
- Prev Clicks / Current Clicks
- Click Δ (absolute + %)
- Prev Impr / Current Impr
- Impr Δ (absolute + %)
- Trend indicator

**Required summary rows:**
1. **SUBTOTAL** row (background: #D9EBD9, bold)
   - Sum all subfolder values
2. **% of Site Total** row (background: #E6E6E6, bold italic)
   - Each column = Subtotal / Site Total × 100

### 6. Conversion Performance by Subfolder (if GA4 data available)
| Column | Calculation |
|--------|-------------|
| Sessions | GA4 sessions by page path |
| Form Starts | GA4 form_start events |
| Form Submits | GA4 form_submit events |
| Form Start Rate | Form Starts / Sessions × 100 |
| Conversion Rate | Form Submits / Sessions × 100 |
| Form Completion Rate | Form Submits / Form Starts × 100 |

**Required:** Site Total row at bottom

### 7. Top Pages Performance (by Clicks)
Show top 10 pages by clicks with MoM comparison.

**Required columns:**
- # (rank)
- Page (URL with link)
- Current Clicks / Prev Clicks
- Δ Clicks (absolute + %)
- Current Impr / Prev Impr
- Δ Impr (absolute + %)

**Required summary rows:**
1. **SUBTOTAL (Top 10)** row (background: #D9EBD9, bold)
2. **% of Site Total** row (background: #E6E6E6, bold italic)

### 8. Impression Gainers Table
Show pages with highest impression growth (not necessarily in top 10 by clicks).
- Use green header (#22c55e)
- Include Content Type column (Education, Product, Brand, Terminal)

### 9. Top Keywords Performance
Show top 12 keywords by clicks with MoM comparison.

**Required columns:**
- # (rank)
- Keyword
- Current Clicks / Prev Clicks
- Δ (absolute change with color)
- Current Position
- Type (Brand / Education / Terminal / Product)
- Ranking URL (linked)

**Required summary rows:**
1. **Top 12 Subtotal** row (background: #f0f9ff, bold, border-top)
2. **% of Total (X clicks)** row (background: #e8f5e9, italic)

### 10. Core Keyword Tracking
Track priority commercial keywords from Ahrefs/SEMrush.

**Required columns:**
- Core Keyword
- Search Volume
- Prev Position / Current Position
- Δ Position (with trend arrow)
- Ranking URL

### 11. AEO Metrics (if Workduo data available)
| Metric | Source |
|--------|--------|
| Visibility % | Workduo screenshot |
| Share of Voice % | Workduo screenshot |
| Average Position | Workduo screenshot |
| Competitive Rank | Workduo screenshot |

### 12. Daily Performance Charts
- Daily Clicks line chart
- Daily Impressions line chart
- Use Chart.js with brand colors

---

## Data Collection Steps

### Step 1: GSC Data (Current Period)
```javascript
// 1. Site-level totals
mcp__google-search-console__get_performance_data({
  site_url: "sc-domain:gofreight.com",
  start_date: "[period_start]",
  end_date: "[period_end]",
  row_limit: 1000
})

// 2. Daily data
mcp__google-search-console__get_performance_data({
  site_url: "sc-domain:gofreight.com",
  start_date: "[period_start]",
  end_date: "[period_end]",
  dimensions: ["date"],
  row_limit: 1000
})

// 3. Page data
mcp__google-search-console__get_performance_data({
  site_url: "sc-domain:gofreight.com",
  start_date: "[period_start]",
  end_date: "[period_end]",
  dimensions: ["page"],
  row_limit: 1000
})

// 4. Query data
mcp__google-search-console__get_performance_data({
  site_url: "sc-domain:gofreight.com",
  start_date: "[period_start]",
  end_date: "[period_end]",
  dimensions: ["query"],
  row_limit: 1000
})
```

### Step 2: GSC Data (Comparison Period)
Run same 4 queries for previous period of equal length.

### Step 3: Calculate Query Segments
```javascript
// Segment classification
function classifyQuery(query) {
  const q = query.toLowerCase();
  if (q === 'gofreight') return 'exact_brand';
  if (q.includes('gofreight') || q.includes('go freight') || q.includes('gofright')) return 'branded_related';
  return 'non_branded';
}
```

### Step 4: Calculate Subfolder Metrics
```javascript
// Subfolder classification
function classifyPage(url) {
  if (url.includes('/blog')) return 'Blog';
  if (url.includes('/solutions')) return 'Solutions';
  if (url.includes('/customers')) return 'Customers';
  if (url.includes('/pricing')) return 'Pricing';
  if (url.includes('/get-demo')) return 'Get Demo';
  if (url.includes('/glossary')) return 'Glossary';
  if (url.includes('archive.gofreight.com')) return 'Archive';
  if (url.includes('support.gofreight.com')) return 'Support';
  return 'Other';
}
```

### Step 5: Content Tracker
```javascript
mcp__google-sheets__get_sheet_data({
  spreadsheet_id: "1D7MDm4_4HpuIfjUe2CBTYat2AoTWRFLK2XgGBI8gpUc",
  sheet: "Novastacks Content delivery Tracker",
  range: "A1:S50"
})
```
Filter by Status column:
- "Published" → Deliverables Shipped
- "Gofreight Approved yet to Publish" → Pending Publication

### Step 6: AEO Data
Ask user for Workduo screenshot path, read image to extract metrics.

---

## Table Styling Standards

### Data Tables
```css
.data-table th {
  background: #333333; /* medium-gray */
  color: white;
  padding: 12px 15px;
  text-align: left;
}

.data-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
}

.trend-up { color: #22c55e; font-weight: 600; }
.trend-down { color: #ef4444; font-weight: 600; }
```

### Summary Rows
```css
/* Subtotal row */
tr.subtotal {
  background: #D9EBD9;
  font-weight: bold;
}

/* % of Total row */
tr.percent-total {
  background: #E6E6E6;
  font-weight: bold;
  font-style: italic;
}
```

### Callout Boxes
```css
/* Blue - informational */
.callout-blue {
  background: linear-gradient(135deg, rgba(1, 170, 193, 0.1), rgba(1, 215, 244, 0.05));
  border-left: 4px solid #01aac1;
}

/* Green - success/positive */
.callout-green {
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
  border-left: 4px solid #22c55e;
}

/* Yellow - warning/pending */
.callout-yellow {
  background: linear-gradient(135deg, #fefce8, #fef3c7);
  border-left: 4px solid #eab308;
}

/* Red - critical/error */
.callout-red {
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
  border-left: 4px solid #ef4444;
}
```

---

## Validation Checklist

Before publishing, verify:

1. [ ] **Subfolder totals ≈ site total** (within 5%)
2. [ ] **% calculations use site total as denominator**
3. [ ] **All subtotal rows included in tables**
4. [ ] **Query segment breakdown adds to 100%**
5. [ ] **MoM changes calculated correctly** ((Current - Previous) / Previous × 100)
6. [ ] **Content status matches actual publication state**
7. [ ] **AEO data matches Workduo screenshot exactly**
8. [ ] **No fabricated/estimated data** - every metric has a source

---

## Output Files

- Report: `gofreight_[month]_[year]_report.html`
- GitHub Pages: Copy to `index.html`
- Data archive: Save raw data to `data/` folder
