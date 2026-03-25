---
name: Financial Data Extraction
description: Extract balance sheet, income statement, shares outstanding, organic growth, and GAAP reconciliation data from financial PDFs. Standardize via Tiger-Transformer and append structured output to the document markdown.
---

# Financial Data Extraction (Phase 2)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- If Tiger-Transformer is not running on localhost:8000 then ask the user to run `.\tools\start_transformer.bat`
- If a static file server is not running on localhost:8181 then ask the user to run `.\tools\start_file_server.bat`

**DO NOT EVER start servers without human user.**

## Overview

This skill extracts four financial components from the PDF and appends structured markdown tables to the document's `.md` file:

| Component | Requires Transformer | Dependency | Conditional |
| --- | --- | --- | --- |
| Balance Sheet | Yes (`/predict/balance-sheet`) | None | No |
| Income Statement + Shares | Yes (`/predict/income-statement`) | None | No |
| Organic Growth | No (LLM-only) | Income Statement (needs revenue) | No |
| GAAP Reconciliation | No (LLM-only) | None | `earnings_announcement` only |

### Output Script

After extracting raw data into a JSON file, run the centralized Python script:

```bash
python skills/financial_data_extraction/scripts/transform_and_append.py --json <extracted.json> --md <output.md>
```

The script handles:
- Tiger-Transformer API calls for balance sheet and income statement standardization
- Expense sign normalization (expenses → negative)
- Accumulated depreciation sign correction
- Organic growth calculation (simple YoY with organic growth override)
- Markdown table formatting and appending

The script is **idempotent** — re-running will skip sections that already exist in the output file.

See `resources/transformer_example.py` for a standalone template on querying the Transformer API directly.

---

## Step 1: Single-Pass PDF Read

Open the PDF in the browser **ONCE** and scroll through to extract ALL raw data needed for every component below. Collect it into a temporary JSON structure or your scratchpad. Close the browser. All subsequent steps run offline from this raw data.

**What to capture during the single pass:**

1. **Consolidated Balance Sheet** — all line items for the current period column
2. **Consolidated Income Statement** — all line items from revenue through net income for the current period, PLUS prior-year revenue from the comparative column
3. **Basic and Diluted Shares Outstanding** — usually at the bottom of the income statement
4. **Organic/Comparable Sales Growth** — from the management discussion or press release highlights
5. **GAAP Reconciliation Table** — from the supplemental tables (earnings announcements only)

---

## Step 2: Balance Sheet Extraction

### 2a. Locate and Verify

Find the **Consolidated Balance Sheet** (or "Consolidated Balance Sheets"):

- Column headers match `period_end_date` or `time_period`
- Is CONSOLIDATED (not subsidiary or segment)
- Contains both Assets AND Liabilities/Equity sections
- Is the full table (not a condensed summary from a press release header)

**ADR / dual-currency documents**: If the statement has BOTH a local currency column (e.g., RMB, TWD, EUR) AND a USD convenience translation column, **always use the local (functional) currency column**. Ignore the USD translation.

### 2b. Extract Line Items

Extract **every** line item for the **current period column** only. The extraction must be **complete** — do not skip or abbreviate any rows.

**JSON structure:**

```json
{
  "currency": "USD",
  "unit": "thousands",
  "line_items": [
    {"line_name": "Cash and cash equivalents", "line_value": 2243971, "line_category": "current_assets"},
    {"line_name": "Inventories", "line_value": 1323602, "line_category": "current_assets"},
    {"line_name": "Total current assets", "line_value": 4060577, "line_category": "current_assets"},
    {"line_name": "Property and equipment, net", "line_value": 1545811, "line_category": "noncurrent_assets"},
    {"line_name": "Accounts payable", "line_value": 348441, "line_category": "current_liabilities"},
    {"line_name": "Non-current lease liabilities", "line_value": 1154012, "line_category": "noncurrent_liabilities"},
    {"line_name": "Stockholders' equity", "line_value": 4232081, "line_category": "equity"}
  ]
}
```

**Extraction rules:**

- Extract values EXACTLY as shown — do NOT round, estimate, or calculate
- `line_name`: Shorten names, remove "net of..." notes
- `line_value`: Numeric only (no commas, no currency symbols). Use negative values where shown
- `line_category`: One of `current_assets`, `noncurrent_assets`, `current_liabilities`, `noncurrent_liabilities`, `equity`. Classify based on where the item appears in the balance sheet (items above "Total current assets" are `current_assets`, items below are `noncurrent_assets`, etc.)
- `currency`: Use the document's actual currency — do NOT assume or convert to USD
- `unit`: Only set if EXPLICITLY stated (e.g., "In thousands", "In millions"). Otherwise null
- Include ALL subtotals and totals (Total Current Assets, Total Assets, Total Liabilities, etc.)
- Include ALL individual line items within each section — do NOT summarize or aggregate
- Maintain exact document order

**Anti-hallucination rules:**

- ONLY extract values explicitly shown in the document
- Do NOT invent line items or values
- If a value is not visible, use null or omit
- Do NOT use external knowledge

### 2c. Completeness Assessment

After extraction, use your judgment to assess whether the balance sheet is complete. Consider these indicators:

| Indicator | What to Check |
| --- | --- |
| Section coverage | Are Assets, Liabilities, AND Equity all present with individual line items (not just totals)? |
| Accounting equation | Does Total Assets ≈ Total Liabilities + Equity? |
| Minimum detail | Current assets has at least Cash + 1 other item? Non-current has PP&E or equivalent? |
| Subtotal presence | Are Total Current Assets, Total Assets, Total Current Liabilities present? |
| Reasonable count | A typical balance sheet has 15–30 line items. Fewer than 8 suggests missing data. |

Rate your confidence:
- **High** — All indicators pass. Proceed.
- **Medium** — 1–2 minor gaps, but data is usable for downstream calculations. Proceed with a note.
- **Low** — Major sections missing or accounting equation fails significantly. Re-read the PDF before proceeding.

> ⚠️ A **Low** confidence extraction will produce nonsensical Invested Capital and ROIC calculations downstream. Do NOT proceed without re-extracting.

---

## Step 3: Income Statement Extraction

### 3a. Locate and Verify

Find the **Consolidated Statement of Income** (also called "Statement of Operations", "Statement of Earnings", or "Results of Operations"):

- Column headers match `period_end_date` or `time_period`
- Is CONSOLIDATED (not segment-level)
- Starts with Revenue and ends with Net Income (or similar)

**ADR / dual-currency documents**: Always use the local (functional) currency column.

### 3b. Extract Line Items

Extract **every** line item from revenue through net income for the **current period column**. The extraction must be **complete**.

> ⚠️ **IMPORTANT: Prior-Year Revenue**
> While extracting the current period, also look at the comparative column and extract the **prior-year revenue**. This single value is required for the Organic Growth component. You do not need the full prior-year column, just the top-line revenue.

**JSON structure:**

```json
{
  "currency": "USD",
  "unit": "thousands",
  "prior_revenue": 2771838,
  "line_items": [
    {"line_name": "Net revenue", "line_value": 3205103, "line_category": "income_statement"},
    {"line_name": "Costs of goods sold", "line_value": 1301678, "line_category": "income_statement"},
    {"line_name": "Gross profit", "line_value": 1903425, "line_category": "income_statement"},
    {"line_name": "Income from operations", "line_value": 913890, "line_category": "income_statement"},
    {"line_name": "Income before income tax expense", "line_value": 931720, "line_category": "income_statement"},
    {"line_name": "Income tax expense", "line_value": 262252, "line_category": "income_statement"},
    {"line_name": "Net income", "line_value": 669468, "line_category": "income_statement"}
  ],
  "basic_shares": 126.228,
  "diluted_shares": 126.584,
  "shares_unit": "millions"
}
```

**Extraction rules:**

- Extract values EXACTLY as shown — do NOT round, estimate, or calculate
- `line_name`: Shorten names, remove "net of..." notes
- `line_value`: Numeric only. Use negative values where shown in the document
- `line_category`: Always `"income_statement"` for all income statement items
- `currency`: Use the document's actual currency
- `unit`: Only set if EXPLICITLY stated. Otherwise null
- **CONTINUE below Net Income** to extract basic and diluted shares outstanding
- Include ALL subtotals: Revenue, Gross Profit, Operating Income, Net Income, etc.
- Include ALL intermediate items between Operating Income and Net Income (interest income, interest expense, equity method gains/losses, FX, other income/expense, etc.)
- Maintain exact document order

**Anti-hallucination rules:**

- ONLY extract values explicitly shown in the document
- Do NOT invent line items or values
- If a value is not visible, use null or omit
- Do NOT use external knowledge

### 3c. Shares Outstanding

Extract basic and diluted shares outstanding from the bottom of the income statement. Capture their unit separately — it may differ from the statement unit (e.g., shares in thousands while revenue in millions). If only one type found, set the other to null. Validate that diluted ≥ basic.

### 3d. Completeness Assessment

After extraction, assess whether the income statement is complete:

| Indicator | What to Check |
| --- | --- |
| Revenue present | Does a revenue/net revenue line exist at the top? |
| Flow completeness | Does the statement flow logically: Revenue → Gross Profit → Operating Income → Pre-Tax Income → Tax → Net Income? |
| Tax line present | Is Income Tax Expense/Benefit captured? (Critical for NOPAT calculation) |
| Operating income present | Is there an Operating Income / Income from Operations line? (Critical for EBITA) |
| Shares captured | Are basic AND diluted share counts present with units? |
| Prior-year revenue | Was the comparative column's revenue captured? (Critical for Organic Growth) |
| Reasonable count | A typical income statement has 8–20 line items. Fewer than 5 suggests missing data. |

Rate your confidence:
- **High** — All indicators pass. The full flow from revenue to net income is captured with all intermediate items.
- **Medium** — Minor omissions (e.g., some intermediate items between operating income and net income are missing), but all 5 critical anchors (Revenue, Operating Income, Pre-Tax Income, Tax, Net Income) are present.
- **Low** — One or more critical anchors are missing. Re-read the PDF before proceeding.

> ⚠️ Missing the tax line prevents NOPAT calculation. Missing operating income prevents EBITA calculation. These are the most common causes of downstream failures.

---

## Step 4: Organic Growth Extraction

**Depends on:** Income Statement (needs current and prior-year revenue).

### 4a. Extract Organic Growth Percentage

Search the document for an explicitly stated **organic growth** or **constant-currency growth** percentage.

**What to look for:**

- "organic growth" / "organic revenue growth"
- "constant currency growth" / "constant currency revenue growth"
- "currency-neutral growth"
- "comparable sales growth" / "comparable store sales"

**Rules:**

- Extract the RAW percentage as a float (e.g., 12.0 for 12%, -2.3 for -2.3%)
- Only extract if EXPLICITLY labeled as organic or constant-currency growth
- Do NOT extract simple reported revenue growth in this step
- If not found, set to null — the script will calculate simple growth as fallback

### 4b. JSON Structure

```json
{
  "current_revenue": 3205103,
  "prior_revenue": 2771838,
  "unit": "thousands",
  "organic_growth": 12.0
}
```

Set `organic_growth` to `null` if not explicitly reported — the script will automatically calculate simple YoY revenue growth as the fallback.

> ⚠️ **VALIDATION**: If both organic growth and simple growth are available, they should be within ±5 percentage points. If the gap exceeds 10pp, flag for user review.

---

## Step 5: GAAP Reconciliation Extraction (Conditional)

**Only run for `earnings_announcement` document types.** Skip entirely for 10-Q, 10-K, etc.

### 5a. Locate the Reconciliation Table

Find the **GAAP to non-GAAP operating income** or **EBITDA reconciliation** table. Usually found in the supplemental tables at the end of earnings press releases.

**What to look for:**

- Tables titled "Reconciliation of GAAP to Non-GAAP" or similar
- Tables showing adjustments from GAAP operating income to adjusted/non-GAAP operating income or EBITDA

**What to AVOID:**

- Net income reconciliation tables (wrong table)
- Margin reconciliation tables
- EPS reconciliation tables
- Segment-level reconciliations (need consolidated)

### 5b. Extract Line Items

```json
{
  "reconciliation_type": "Operating Income",
  "unit": "thousands",
  "line_items": [
    {"line_name": "Income from operations", "line_value": 913890, "line_category": "gaap_item", "is_operating": "Yes"},
    {"line_name": "Stock-based compensation", "line_value": 200000, "line_category": "Recurring", "is_operating": "Yes"},
    {"line_name": "Amortization of intangibles", "line_value": 118000, "line_category": "Recurring", "is_operating": "No"},
    {"line_name": "Adjusted income from operations", "line_value": 1231890, "line_category": "adjusted_item", "is_operating": "Yes"}
  ]
}
```

**Line category classification:**

| Category | Description | Examples |
| --- | --- | --- |
| `gaap_item` | The base GAAP figure (first line) | "GAAP operating income" |
| `Recurring` | Normal, occurs every period | Depreciation, amortization, stock-based compensation |
| `One-Time` | Unusual or infrequent | Restructuring, impairment, acquisition costs, legal settlements |
| `adjusted_item` | The final adjusted non-GAAP figure | "Non-GAAP operating income", "Adjusted EBITDA" |

**Extraction rules:**

- Extract values EXACTLY as shown
- The first item is usually the GAAP starting figure (`gaap_item`)
- The last item is usually the non-GAAP ending figure (`adjusted_item`)
- All items in between are adjustments (`Recurring` or `One-Time`)

### 5c. Operating Classification

For each adjustment, classify as operating or non-operating:

| Classification | Examples |
| --- | --- |
| **Operating** | Stock-based compensation, depreciation (internal), other operating expenses |
| **Non-Operating** | Amortization of acquired intangibles, acquisition costs, restructuring/impairment, litigation, interest adjustments, tax adjustments, gain/loss on divestitures, FX |

**Common mistakes to avoid:**

- ❌ "Amortization of intangibles" is **NOT operating** — it relates to acquired intangibles (purchase accounting)
- ❌ "Acquisition-related expenses" are **NOT operating** — they are M&A costs
- ❌ "Restructuring and impairment charges" are **NOT operating** — they are one-time/unusual
- ✅ "Stock-based compensation" IS operating — it is a recurring cost of employment
- ✅ "Depreciation" IS operating — it relates to internally-owned assets

### 5d. Validate

Verify: GAAP base + sum of adjustments ≈ Non-GAAP total (tolerance ≤ 1). If validation fails, re-read the table. If it still fails, save anyway and report the error.

If no reconciliation table is found in an earnings announcement, note "GAAP Reconciliation: Not found" and move on.

---

## Step 6: Assemble JSON and Run Script

  Combine all extracted data into a single JSON file with top-level keys: `balance_sheet`, `income_statement`, `organic_growth`, `gaap_reconciliation`. Save to a temporary file (e.g., `tmp/TICKER_extracted.json`).
  
  > ⚠️ **IMPORTANT**: The script `transform_and_append.py` may crash with an `AttributeError` if `gaap_reconciliation` is set to `null` or `None`. If no reconciliation is found, provide an empty object with an empty list for `line_items`:
  > ```json
  > "gaap_reconciliation": {
  >   "reconciliation_type": "Operating Income",
  >   "unit": "thousands",
  >   "line_items": []
  > }
  > ```


Run the centralized script:

```bash
python skills/financial_data_extraction/scripts/transform_and_append.py --json tmp/TICKER_extracted.json --md processing_data/TICKER_DOCTYPE_DATE_temp.md
```

The script will:

1. Call the Tiger-Transformer for balance sheet and income statement standardization
2. Normalize expense signs (expenses → negative)
3. Fix accumulated depreciation signs
4. Calculate organic growth (simple YoY with organic override)
5. Format and append all sections as structured markdown tables
6. Skip any sections that already exist in the output (idempotent)

---

## Error Handling

- PDF cannot be opened in browser → Inform user, skip
- Balance sheet or income statement not found → Inform user, skip
- Transformer server not running → Inform user (run `.\tools\start_transformer.bat`)
- Validation fails → Save data anyway, report errors in markdown
- GAAP reconciliation not found (earnings announcement) → Note in output, continue
- Document is not an earnings announcement → Skip GAAP reconciliation entirely

## Reference

Based on `tiger-cafe\app\app_agents\` extractors:
- `balance_sheet_extractor.py`
- `income_statement_extractor.py`
- `organic_growth_extractor.py`
- `gaap_reconciliation_extractor.py`
