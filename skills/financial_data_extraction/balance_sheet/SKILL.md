---
name: Balance Sheet Extraction
description: Extract balance sheet line items from a financial PDF, standardize names via Tiger-Transformer, and validate calculations.
---

# Balance Sheet Extraction (Sub-Skill 2a)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- Tiger-Transformer server running at `http://localhost:8000`

## Step-by-Step Instructions

### Step 1: Read the PDF and Classification Metadata

1. Read the classification `.md` file to get: `ticker`, `document_type`, `time_period`, `period_end_date`
2. Read the PDF directly using multimodal capabilities (do NOT use text extraction libraries)

### Step 2: Locate and Verify the Balance Sheet Section

1. In the PDF, find the **Consolidated Balance Sheet** (or "Consolidated Balance Sheets")
2. Verify it is the CORRECT section — it should:
   - Have column headers matching the `period_end_date` or `time_period`
   - Be a CONSOLIDATED statement (not a subsidiary or segment)
   - Contain both Assets AND Liabilities/Equity sections
   - Not be a condensed summary table from a press release header — look for the full table
3. **ADR / dual-currency documents**: If the statement has BOTH a local currency column (e.g., RMB, TWD, EUR) AND a USD convenience translation column, **always use the local (functional) currency column**. Ignore the USD translation.
4. If the correct section cannot be found, inform the user

### Step 3: Extract Line Items

Extract every line item from the balance sheet table for the **current period column only** (the column matching `period_end_date`).

**Output JSON structure:**
```json
{
    "currency": "RMB",
    "unit": "millions",
    "time_period": "Q1 2025",
    "period_end_date": "2025-02-28",
    "line_items": [
        {
            "line_name": "Cash and cash equivalents",
            "line_value": 7509,
            "line_category": "current_assets"
        }
    ]
}
```

**Extraction rules:**
- Extract values EXACTLY as shown — do NOT round, estimate, or calculate
- `line_name`: Shorten names, remove "net of..." notes
- `line_value`: Numeric only (no commas, no currency symbols). Use negative values where shown
- `line_category`: One of: `current_assets`, `noncurrent_assets`, `current_liabilities`, `noncurrent_liabilities`, `stockholders_equity`
- `unit`: Only set if EXPLICITLY stated (e.g., "In millions"). Otherwise null
- `currency`: Use the document's actual currency — do NOT assume or convert to USD. Common values: USD, EUR, GBP, JPY, CAD, RMB, CHF, AUD, KRW, INR, SEK, etc.
- Include ALL subtotals and totals (Total Current Assets, Total Assets, Total Liabilities, etc.)
- Maintain the exact order from the document

**Anti-hallucination rules:**
- ONLY extract values explicitly shown in the document
- Do NOT invent line items or values
- If a value is not visible, use null
- Do NOT use external knowledge

### Step 4: Validate Section Categories

Check that all `line_category` values are valid. If any are missing or invalid, fix them using this fallback logic:

1. Inherit from the previous item
2. Inherit from the next item
3. Infer from the line name (e.g., "equity" → `stockholders_equity`)
4. Last resort: use `current_assets`

### Step 5: Standardize via Tiger-Transformer

Send **ALL line items together in a single batch request** to the Tiger-Transformer server.

> ⚠️ **CRITICAL: Send ALL items at once, not one at a time.** The model uses a sliding context window that looks at the 2 items before and 2 items after each line to classify it. Sending items individually (or in small groups) strips this context and causes misclassifications. Always send the complete list in document order.

**How it works internally:** For each item, the server constructs:
```
[prev_2_name] [prev_1_name] [line_category] [line_name] [next_1_name] [next_2_name]
```
Items at the edges use `<START>` / `<END>` sentinel tokens.

**Request:** `POST http://localhost:8000/predict/balance-sheet`
```json
{
    "items": [
        {"line_name": "Cash and cash equivalents", "line_category": "current_assets", "line_order": 0},
        {"line_name": "Short-term investments", "line_category": "current_assets", "line_order": 1},
        {"line_name": "Trade receivables", "line_category": "current_assets", "line_order": 2},
        ...all remaining items in document order...
    ]
}
```

**Response:** Each item gets:
- `standardized_name`: Standardized key (e.g., `cash_and_equivalents`)
- `is_calculated`: Whether this is a subtotal/total line (from CSV mapping)
- `is_operating`: Whether this is an operating item (from CSV mapping)
- `confidence`: Model confidence score

### Step 6: Validate Calculations

Using the `is_calculated` flags from Step 5, verify that totals match their components:

**Validation checks:**
1. Sum of `current_assets` (non-calculated) ≈ Total Current Assets (calculated)
2. Sum of `noncurrent_assets` (non-calculated) ≈ Total Noncurrent Assets (calculated) — if present
3. Total Current Assets + Total Noncurrent Assets ≈ Total Assets
4. Sum of `current_liabilities` (non-calculated) ≈ Total Current Liabilities (calculated)
5. Sum of `noncurrent_liabilities` (non-calculated) ≈ Total Noncurrent Liabilities (calculated) — if present
6. Total Liabilities + Total Stockholders' Equity ≈ Total Liabilities and Equity
7. Total Assets ≈ Total Liabilities and Equity (the accounting equation)

**Tolerance:** Allow differences ≤ 1 (for rounding)

If validation fails, report the errors but still save the data. Do NOT re-extract unless errors are severe (>5% difference).

### Step 7: Fix Accumulated Depreciation Sign

If any line item with `standardized_name` containing "accumulated_depreciation" has a positive value, flip it to negative.

### Step 8: Write Output to Markdown

Append the following section to the document's `.md` file:

```markdown
---

## Balance Sheet

| Field | Value |
|-------|-------|
| Currency | {currency} |
| Unit | {unit} |
| Extraction Date | {current_date_iso} |
| Validation | {PASS or FAIL with error count} |

### Line Items

| # | Line Name | Value | Category | Standardized Name | Calculated | Operating |
|---|-----------|-------|----------|-------------------|------------|-----------|
| 1 | Cash and cash equivalents | 7,509 | current_assets | cash_and_cash_equivalents | No | Yes |
| ... | ... | ... | ... | ... | ... | ... |
```

---

## Error Handling

- If PDF cannot be read → Inform user, skip
- If balance sheet section not found → Inform user, skip
- If transformer server is not running → Inform user (run `.\tools\start_transformer.bat`)
- If validation fails → Save data anyway, report errors in markdown

## Reference

Based on `tiger-cafe\app\app_agents\balance_sheet_extractor.py`
