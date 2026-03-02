---
name: Income Statement Extraction
description: Extract income statement line items from a financial PDF, standardize names via Tiger-Transformer, and normalize expense signs.
---

# Income Statement Extraction (Sub-Skill 2b)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- Tiger-Transformer server running at `http://localhost:8000`

## Step-by-Step Instructions

### Step 1: Read the PDF and Classification Metadata

1. Read the classification `.md` file to get: `ticker`, `document_type`, `time_period`, `period_end_date`
2. Read the PDF directly using multimodal capabilities

### Step 2: Locate and Verify the Income Statement Section

1. Find the **Consolidated Statement of Income** (also called "Statement of Operations", "Statement of Earnings", or "Results of Operations")
2. Verify it is the CORRECT section:
   - Column headers match `period_end_date` or `time_period`
   - Is CONSOLIDATED (not segment-level)
   - Starts with Revenue and ends with Net Income (or similar)
3. **ADR / dual-currency documents**: If the statement has BOTH a local currency column (e.g., RMB, TWD, EUR) AND a USD convenience translation column, **always use the local (functional) currency column**. Ignore the USD translation.
4. If not found, inform the user

### Step 3: Extract Line Items

Extract every line item from revenue through net income for the **current period column**.

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

**Extraction rules:**
- Extract values EXACTLY as shown — do NOT round, estimate, or calculate
- `line_name`: Shorten names, remove "net of..." notes
- `line_value`: Numeric only. Use negative values where shown in the document
- `line_category`: Always `"income_statement"` for all income statement items
- `currency`: Use the document's actual currency — do NOT assume or convert to USD
- `unit`: Only set if EXPLICITLY stated (e.g., "In millions", "百万円"). Otherwise null
- **STOP after Net Income** — do not extract EPS or share count rows
- Include ALL subtotals: Revenue, Gross Profit, Operating Income, Net Income, etc.
- Maintain exact document order

**Anti-hallucination rules:**
- ONLY extract values explicitly shown in the document
- Do NOT invent line items or values
- If a value is not visible, use null or omit
- Do NOT use external knowledge

### Step 4: Standardize via Tiger-Transformer

Send **ALL line items together in a single batch request** to the Tiger-Transformer server.

> ⚠️ **CRITICAL: Send ALL items at once, not one at a time.** The model uses a sliding context window that looks at the 2 items before and 2 items after each line to determine its classification. Sending items individually strips this context and causes misclassifications (e.g., "Amortization of intangibles" alone may classify as "revenue" at 52% confidence, but with full context it correctly classifies as "amortization_acquired" at 99%).

**How it works internally:** For each item, the server constructs:
```
[prev_2_name] [prev_1_name] [line_category] [line_name] [next_1_name] [next_2_name]
```
Items at the edges use `<START>` / `<END>` sentinel tokens.

**Request:** `POST http://localhost:8000/predict/income-statement`
```json
{
    "items": [
        {"line_name": "Subscription revenue", "line_category": "income_statement", "line_order": 0},
        {"line_name": "Product revenue", "line_category": "income_statement", "line_order": 1},
        {"line_name": "Total revenue", "line_category": "income_statement", "line_order": 2},
        ...all remaining items in document order...
    ]
}
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
