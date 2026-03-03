---
name: Income Statement Extraction
description: Extract income statement line items from a financial PDF, standardize names via Tiger-Transformer, and normalize expense signs.
---

# Income Statement Extraction (Sub-Skill 2b)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- If Tiger-Transformer is not running on localhost:8000 then ask the user to run `.\tools\start_transformer.bat`
- If a static file server is not running on localhost:8181 then ask the user to run `python -m http.server 8181 --bind 127.0.0.1`

**DO NOT EVER start servers without human user.**

## Step-by-Step Instructions

### Step 1: Read the PDF and Classification Metadata

1. Read the classification `.md` file to get: `ticker`, `document_type`, `time_period`, `period_end_date`
2. Open the PDF in the browser using the `browser_subagent` tool:
   - Navigate to `http://localhost:8181/processing_data/{filename}`
   - Navigate to the page(s) containing the **Consolidated Statement of Income** (or equivalent)
   - For large filings (10-K, 10-Q), use the table of contents or scroll to the financial statements section
3. Do NOT use PyPDF2 or other text extraction libraries

### Step 2: Locate and Verify the Income Statement Section

1. Find the **Consolidated Statement of Income** (also called "Statement of Operations", "Statement of Earnings", or "Results of Operations")
2. Verify it is the CORRECT section:
   - Column headers match `period_end_date` or `time_period`
   - Is CONSOLIDATED (not segment-level)
   - Starts with Revenue and ends with Net Income (or similar)
3. **ADR / dual-currency documents**: If the statement has BOTH a local currency column (e.g., RMB, TWD, EUR) AND a USD convenience translation column, **always use the local (functional) currency column**. Ignore the USD translation.
4. If not found, inform the user

### Step 3: Extract Line Items

Extract **every** line item from revenue through net income for the **current period column**. The extraction must be **complete** — do not skip or abbreviate any rows.

**Output JSON structure:**
```json
{
    "currency": "JPY",
    "unit": "millions",
    "time_period": "Q1 2025",
    "period_end_date": "2025-02-28",
    "line_items": [
        {
            "line_name": "Total revenue",
            "line_value": 5714,
            "line_category": "income_statement"
        }
    ]
}
```

> ⚠️ **COMPLETENESS CHECK — MANDATORY**
>
> After extraction, verify that ALL of the following critical line items are present:
>
> | # | Required Line Item | Typical Standardized Name |
> |---|---|---|
> | 1 | Revenue / Total Revenue | `revenue` or `total_revenue` |
> | 2 | Operating Income / Operating Profit | `operating_income` |
> | 3 | Income Before Income Taxes | `income_before_taxes` |
> | 4 | Income Tax Expense / Benefit | `income_tax_provision` |
> | 5 | Net Income | `net_income` |
>
> If **any** of these 5 are missing, go back to the PDF and re-read the income statement more carefully. These lines are required for downstream calculations (EBITA, Tax Rate, NOPAT). Do NOT proceed with an incomplete extraction.

**Extraction rules:**
- Extract values EXACTLY as shown — do NOT round, estimate, or calculate
- `line_name`: Shorten names, remove "net of..." notes
- `line_value`: Numeric only. Use negative values where shown in the document
- `line_category`: Always `"income_statement"` for all income statement items
- `currency`: Use the document's actual currency — do NOT assume or convert to USD
- `unit`: Only set if EXPLICITLY stated (e.g., "In millions", "百万円"). Otherwise null
- **STOP after Net Income** — do not extract EPS or share count rows
- Include ALL subtotals: Revenue, Gross Profit, Operating Income, Net Income, etc.
- Include ALL intermediate items between Operating Income and Net Income (interest income, interest expense, equity method gains/losses, FX, other income/expense, etc.)
- Maintain exact document order

**Anti-hallucination rules:**
- ONLY extract values explicitly shown in the document
- Do NOT invent line items or values
- If a value is not visible, use null or omit
- Do NOT use external knowledge

### Step 4: Standardize via Tiger-Transformer

Send **ALL line items together in a single batch request** to the Tiger-Transformer server.

> ⚠️ **CRITICAL: Send ALL items at once, not one at a time.** The model uses a sliding context window that looks at the 2 items before and 2 items after each line to determine its classification. Sending items individually strips this context and causes misclassifications (e.g., "Amortization of intangibles" alone may classify as "revenue" at 52% confidence, but with full context it correctly classifies as "amortization_acquired" at 99%).

**Avoid Shell Escaping Issues:** Do NOT try to send the large JSON payload via `curl` or `Invoke-RestMethod` inline on the command line. Write a temporary Python script (`tmp/run_is_transformer.py`) using the `write_to_file` tool to send the HTTP request, then execute that script.

**Example Temporary Python Script:**
```python
import urllib.request
import json
import sys

payload = {
    "items": [
        {"line_name": "Subscription revenue", "line_category": "income_statement", "line_order": 0},
        {"line_name": "Product revenue", "line_category": "income_statement", "line_order": 1},
        {"line_name": "Total revenue", "line_category": "income_statement", "line_order": 2},
        # ... your extracted items ...
    ]
}

req = urllib.request.Request('http://localhost:8000/predict/income-statement', 
                             method='POST', 
                             headers={'Content-Type': 'application/json'}, 
                             data=json.dumps(payload).encode('utf-8'))

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
```

**Response:** Each item gets:
- `standardized_name`: Standardized key (e.g., `total_revenue`)
- `is_calculated`: Whether this is a subtotal/total (from CSV mapping)
- `is_operating`: Whether this is an operating item (from CSV mapping)
- `is_expense`: Whether this is an expense item (from CSV mapping)
- `confidence`: Model confidence score

### Step 5: Normalize Signs

Using the `is_expense` flag from the transformer:
- If `is_expense` is `true` AND `line_value` is positive → flip to negative
- If `is_expense` is `true` AND `line_value` is already negative → keep as-is
- Revenue and income items should remain positive

**The sign convention is: Revenue = positive, Expenses = negative, Income = positive**

This allows simple addition down the statement: Revenue + (negative expenses) = Income

### Step 6: Validate Calculations

Verify key relationships (using the SIGN-NORMALIZED values from Step 5):

1. Revenue - Cost of Revenue ≈ Gross Profit (if all three exist)
2. Sum of operating items ≈ Operating Income
3. All non-calculated operating items + Operating Income items should balance

**Tolerance:** Allow differences ≤ 1

If validation fails but is within 5%, save anyway and report the discrepancy. If >5%, flag for user review.

### Step 7: Write Output to Markdown

Append the following section to the document's `.md` file:

```markdown
---

## Income Statement

| Field | Value |
|-------|-------|
| Currency | {currency} |
| Unit | {unit} |
| Extraction Date | {current_date_iso} |
| Validation | {PASS or FAIL with error count} |

### Line Items

| # | Line Name | Value | Standardized Name | Calculated | Operating | Expense |
|---|-----------|-------|-------------------|------------|-----------|---------|
| 1 | Total revenue | 5,714 | total_revenue | Yes | Yes | No |
| 2 | Subscription cost of revenue | -490 | cost_of_revenue_subscription | No | Yes | Yes |
| ... | ... | ... | ... | ... | ... | ... |
```

---

## Error Handling

- If income statement section not found → Inform user, skip
- If transformer server is not running → Inform user
- If validation fails → Save data anyway, report errors

## Reference

Based on `tiger-cafe\app\app_agents\income_statement_extractor.py`
