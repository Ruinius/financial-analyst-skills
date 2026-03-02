---
name: GAAP Reconciliation Extraction
description: Extract GAAP-to-non-GAAP operating income or EBITDA reconciliation tables from earnings announcements.
---

# GAAP Reconciliation Extraction (Sub-Skill 2e)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- **Only runs for `earnings_announcement` document types** — skip for 10-Q, 10-K, etc.
- No external services required (LLM-only)

## Step-by-Step Instructions

### Step 1: Check Document Type

1. Read the classification `.md` file to get: `document_type`, `time_period`, `period_end_date`
2. **If `document_type` is NOT `earnings_announcement`**, skip this sub-skill entirely
   - GAAP reconciliation tables are typically only found in earnings press releases

### Step 2: Read the PDF

Read the PDF directly using multimodal capabilities.

### Step 3: Locate the Reconciliation Table

Find the **GAAP to non-GAAP operating income** or **EBITDA reconciliation** table.

**What to look for:**
- Tables titled "Reconciliation of GAAP to Non-GAAP" or similar
- Tables showing adjustments from GAAP operating income to adjusted/non-GAAP operating income or EBITDA
- Usually found in the latter pages of earnings press releases

**What to AVOID:**
- Net income reconciliation tables (wrong table)
- Margin reconciliation tables
- EPS reconciliation tables
- Segment-level reconciliations (need consolidated)

### Step 4: Extract Line Items

Extract all line items from the reconciliation table for the current period:

**Output JSON structure:**
```json
{
    "line_items": [
        {
            "line_name": "GAAP operating income",
            "line_value": 2164,
            "unit": "millions",
            "line_category": "Total"
        },
        {
            "line_name": "Stock-based compensation",
            "line_value": 543,
            "unit": "millions",
            "line_category": "Recurring"
        },
        {
            "line_name": "Amortization of intangibles",
            "line_value": 118,
            "unit": "millions",
            "line_category": "Recurring"
        },
        {
            "line_name": "Non-GAAP operating income",
            "line_value": 2825,
            "unit": "millions",
            "line_category": "Total"
        }
    ]
}
```

**Line category classification:**
| Category | Description | Examples |
|----------|-------------|---------|
| `Recurring` | Normal, occurs every period | Depreciation, amortization, stock-based compensation |
| `One-Time` | Unusual or infrequent | Restructuring, impairment, acquisition costs, legal settlements |
| `Total` | Summary or total lines | "GAAP operating income", "Non-GAAP operating income", "Adjusted EBITDA" |

**Extraction rules:**
- Extract values EXACTLY as shown
- The first item is usually the GAAP starting figure (a Total)
- The last item is usually the non-GAAP ending figure (a Total)
- All items in between are adjustments (Recurring or One-Time)

### Step 5: Validate the Reconciliation

Verify that:
```
First item (GAAP figure) + Sum of all adjustments (non-Total items) ≈ Last item (Non-GAAP figure)
```

**Rules:**
- Skip intermediate "Total" items (they are subtotals, not addends)
- The first item is always included in the sum (it's the base)
- Tolerance: ≤ 1

If validation fails, attempt one retry by re-reading the table more carefully. If it still fails, save the data and report the error.

### Step 6: Classify as Operating/Non-Operating

For each adjustment line item (non-Total items), determine if it is operating or non-operating.

**IMPORTANT:** Use the `is_calculated_operating_expense_mapping.csv` in `tools/` as the source of truth. Key classifications:

| Classification | Examples |
|---------------|---------|
| **Operating** | Stock-based compensation, depreciation (internal), other operating expenses |
| **Non-Operating** | Amortization of acquired intangibles, acquisition costs, restructuring/impairment, litigation, interest adjustments, tax adjustments, gain/loss on divestitures, foreign exchange |

**Common mistakes to avoid:**
- ❌ "Amortization of intangibles" is **NOT operating** — it relates to acquired intangibles (purchase accounting), not organic operations
- ❌ "Acquisition-related expenses" are **NOT operating** — they are M&A costs
- ❌ "Restructuring and impairment charges" are **NOT operating** — they are one-time/unusual
- ❌ "Loss contingency" items are **NOT operating** — they are litigation-related
- ✅ "Stock-based compensation" IS operating — it is a recurring cost of employment
- ✅ "Depreciation" IS operating — it relates to internally-owned assets

### Step 7: Write Output to Markdown

Append the following section to the document's `.md` file:

```markdown
---

## GAAP Reconciliation

| Field | Value |
|-------|-------|
| Reconciliation Type | Operating Income / EBITDA |
| Unit | {unit} |
| Validation | {PASS or FAIL} |
| Extraction Date | {current_date_iso} |

### Reconciliation Items

| # | Line Name | Value | Category | Operating |
|---|-----------|-------|----------|-----------|
| 1 | GAAP operating income | 2,164 | Total | — |
| 2 | Stock-based compensation | 543 | Recurring | Yes |
| 3 | Amortization of intangibles | 118 | Recurring | Yes |
| 4 | Non-GAAP operating income | 2,825 | Total | — |
```

---

## Error Handling

- If document is not an earnings announcement → Skip entirely (not an error)
- If reconciliation table not found → Note in markdown ("GAAP Reconciliation: Not found")
- If wrong table type found (net income instead of operating) → Re-search for correct table
- If validation fails → Save data, report error

## Reference

Based on `tiger-cafe\app\app_agents\gaap_reconciliation_extractor.py`
