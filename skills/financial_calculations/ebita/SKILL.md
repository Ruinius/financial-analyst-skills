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

If GAAP Reconciliation data is available, **iterate over EVERY adjustment item** and process it:

**Include only if ALL of these are true:**
- `Operating` = No (non-operating adjustments only)
- NOT a Total/Subtotal line (i.e., `line_category` ≠ "Total")
- Has a non-zero value

For each qualifying item, add its value to the running EBITA total. **Also record it in an Adjustments list** for the output table.

> ⚠️ **DO NOT cherry-pick adjustments by name.** You must iterate over ALL items in the GAAP Reconciliation and apply the filter above. Common non-operating adjustments include (but are NOT limited to):
>
> | Adjustment Type | Typical Names | Operating? |
> |---|---|---|
> | Amortization of acquired intangibles | "Amortization and impairment of intangible assets" | No |
> | **Impairment of long-lived assets** | "Impairment of long-lived assets", "Goodwill impairment" | **No** |
> | Restructuring charges | "Restructuring and severance" | No |
> | Gain/loss on disposal | "Gain on divestiture" | No |
> | Stock-based compensation | "Share-based compensation expenses" | **Yes** (stays in EBITA) |
>
> **Impairment is NON-OPERATING and MUST be added back.** This is a common source of error — impairment charges can be very large (e.g., billions) and missing them will make EBITA wildly wrong.

### Step 3b: Cross-Check Against Non-GAAP Operating Income

The GAAP Reconciliation typically ends with a **Non-GAAP Operating Income** total. Use this to validate:

```
Expected: EBITA ≈ Non-GAAP Operating Income - SBC addback
(Because EBITA adds back non-operating items but keeps SBC, while Non-GAAP adds back everything)
```

If your computed EBITA is dramatically different from `Non-GAAP OpInc - SBC`, you likely missed an adjustment. Go back and re-check.

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
- **NEVER hardcode which adjustments to include by name.** Always iterate over all GAAP recon items and filter by the `operating` flag. New adjustment types (e.g., impairment, restructuring) will appear in different quarters and must be picked up automatically.
- The Adjustments table in the output is MANDATORY — it provides an audit trail showing exactly which items were added back and allows the user to verify correctness.

## Reference

Based on `calculate_ebita()` in `tiger-cafe/app/utils/historical_calculations.py`
