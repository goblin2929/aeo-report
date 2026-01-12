# Monthly Report Data Collection Checklist

## Report Period: _____________ (e.g., December 2024)

---

## Step 1: Google Search Console Data

### 1.1 Site-Level Metrics (Current Month)
- [ ] Query GSC for report month
- [ ] Record values below:

| Metric | Value |
|--------|-------|
| Total Clicks | |
| Total Impressions | |
| Average CTR | |
| Average Position | |

### 1.2 Site-Level Metrics (Previous Month - for MoM)
- [ ] Query GSC for previous month
- [ ] Record values below:

| Metric | Value |
|--------|-------|
| Total Clicks | |
| Total Impressions | |
| Average CTR | |
| Average Position | |

### 1.3 Calculated MoM Changes
| Metric | Current | Previous | Change % |
|--------|---------|----------|----------|
| Clicks | | | |
| Impressions | | | |
| CTR | | | |
| Position | | | |

### 1.4 Subfolder Performance
Run query with `dimensions: ["page"]`, then group by subfolder prefix:

| Subfolder | Dec Clicks | Nov Clicks | Change | Dec Impr | Nov Impr | Change |
|-----------|------------|------------|--------|----------|----------|--------|
| /blog | | | | | | |
| /solutions | | | | | | |
| /customers | | | | | | |
| /pricing | | | | | | |
| /get-demo | | | | | | |
| **SUBTOTAL** | | | | | | |
| **% of Site Total** | | | | | | |

**Validation:** Subtotal should roughly match site total (minus homepage/other pages)

### 1.5 Top 10 Pages
- [ ] Export top pages by clicks
- [ ] Save to `data/gsc_top_pages_{month}.csv`

### 1.6 Top 10 Keywords
- [ ] Export top keywords by clicks
- [ ] Run additional query with `dimensions: ["query", "page"]` to get ranking URLs
- [ ] Save to `data/gsc_top_keywords_{month}.csv`

---

## Step 2: Google Analytics 4 Data

### 2.1 Sessions by Page Path
- [ ] Query GA4 for sessions by pagePath
- [ ] Group by subfolder

### 2.2 Form Events by Page
- [ ] Query GA4 for `form_start` events
- [ ] Query GA4 for `form_submit` events
- [ ] Query GA4 for `get_demo_form_submit_hero_success` events

### 2.3 Conversion Metrics Table
| Subfolder | Sessions | Form Starts | Form Submits | Start Rate | Conv Rate | Completion Rate |
|-----------|----------|-------------|--------------|------------|-----------|-----------------|
| /pricing | | | | | | |
| /get-demo | | | | | | |
| /solutions | | | | | | |
| /blog | | | | | | |
| / (Homepage) | | | | | | |
| /customers | | | | | | |
| **TOTAL** | | | | | | |

**Formulas:**
- Start Rate = Form Starts ÷ Sessions × 100
- Conv Rate = Form Submits ÷ Sessions × 100
- Completion Rate = Form Submits ÷ Form Starts × 100

---

## Step 3: Workduo AEO Data

### 3.1 Export Screenshot
- [ ] Log into Workduo dashboard
- [ ] Go to project: `cmhk59aw9001mlo33c3t8n3rj`
- [ ] Screenshot "AI Search Brand Visibility" table
- [ ] Save to `data/workduo_aeo_{month}.jpg`

### 3.2 Record Values
| Brand | Visibility % | Share of Voice % | Avg Position |
|-------|--------------|------------------|--------------|
| CargoWise | | | |
| Magaya Supply Chain | | | |
| Descartes | | | |
| Shipthis | | | |
| **GoFreight** | | | |

---

## Step 4: Content Tracker Data

### 4.1 Query Google Sheet
- [ ] Pull data from Novastacks Content Delivery Tracker
- [ ] Filter by report month

### 4.2 Categorize Content
| Category | Count | Status | Items |
|----------|-------|--------|-------|
| Customer Story Pages | | Published | |
| CargoWise Articles | | Published | |
| Blog Content | | Published | |
| Blog Content | | Pending | |
| Other | | | |

**Validation:** Verify "Published" items are actually live by checking URLs

---

## Step 5: Pre-Publish Validation

- [ ] Sum of subfolder clicks ≈ site total clicks
- [ ] % of total uses SITE TOTAL as denominator
- [ ] All "Deliverables Shipped" have Status = "Published" in tracker
- [ ] AEO metrics match Workduo screenshot exactly
- [ ] MoM calculations are correct (Current - Previous) ÷ Previous × 100
- [ ] No placeholder or estimated data remains

---

## Step 6: Report Generation

- [ ] Update HTML report with collected data
- [ ] Copy to index.html for GitHub Pages
- [ ] Commit with descriptive message
- [ ] Push to GitHub
- [ ] Verify live at GitHub Pages URL

---

## Data Archive

Save all raw data to `data/` folder:
```
data/
├── gsc_site_metrics_{month}.json
├── gsc_top_pages_{month}.csv
├── gsc_top_keywords_{month}.csv
├── ga4_sessions_{month}.json
├── ga4_events_{month}.json
├── workduo_aeo_{month}.jpg
└── content_tracker_{month}.csv
```

---

**Report completed by:** _______________
**Date:** _______________
**Review completed by:** _______________
