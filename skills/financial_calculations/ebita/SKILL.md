---
name: EBITA Calculation
description: Calculate EBITA (Earnings Before Interest, Tax, and Amortization) from income statement and GAAP reconciliation data.
---

# EBITA Calculation (Sub-Skill 3a)

## Prerequisites

- Income Statement extracted (Skill 2b)
- GAAP Reconciliation extracted if available (Skill 2e)

## What is EBITA?

EBITA = Operating Income + Non-GAAP Adjustments (non-operating only)

It represents the company's **operating profit before interest, taxes, and acquisition-related amortization** — a cleaner view of operational performance.

## Step-by-Step Instructions

### Step 1: Read Extracted Data

From the document's `.md` file, read:
1. **Income Statement** line items (with standardized names, operating flags, and values)
2. **GAAP Reconciliation** items (if available)

### Step 2: Find the Starting Point (Operating Income)

1. Look for a line item with `standardized_name` = `operating_income` in the Income Statement
2. **Fallback**: If not found, use `income_before_taxes` instead (flag as fallback)
3. Record the starting value and its position (line order) in the table

### Step 3: Add Non-GAAP Adjustments

If GAAP Reconciliation data is available, process each adjustment item:

**Include only if ALL of these are true:**
- `Operating` = No (non-operating adjustments only)
- NOT a Total/Subtotal line
- Has a non-zero value

For each qualifying item, add its value to the running EBITA total.

### Step 4: Add Income Statement Non-Operating Items

Also scan the Income Statement for items that appear BEFORE the Operating Income line:
- Must have `Operating` = No
- Must NOT be a calculated total
- Must NOT already be captured in Step 3 (avoid double-counting — check by name AND absolute value)

For these items, **negate the sign** and add to EBITA:
- If the IS shows `-100` for an expense, the add-back is `+100`

### Step 5: Calculate EBITA Margin

```
EBITA Margin = EBITA / Revenue
```

Express as a decimal (e.g., 0.4765 for 47.65%).

### Step 6: Write Output to Markdown

Append to the document's `.md` file:

```markdown
---

## EBITA

| Field | Value |
|-------|-------|
| Starting Point | Operating Income |
| Starting Value | {operating_income} |
| EBITA | {ebita} |
| EBITA Margin | {ebita_margin_pct}% |
| Calculation Date | {current_date_iso} |

### Adjustments

| # | Line Name | Value | Source |
|---|-----------|-------|--------|
| 1 | Stock-based compensation | 469 | GAAP Reconciliation |
| 2 | Amortization of intangibles | 83 | GAAP Reconciliation |
| ... | ... | ... | ... |
```

---

## Important Notes

- The sign convention matters: GAAP Reconciliation values are addbacks (positive = add to operating income). Income Statement non-operating expenses are negative, so we negate them to add back.
- If using Income Before Taxes as fallback, note this in the output — EBITA accuracy is lower.
- Only non-operating items are adjustments. Operating items (like SBC classified as operating) stay in EBITA.

## Reference

Based on `calculate_ebita()` in `tiger-cafe/app/utils/historical_calculations.py`
