---
name: Tax Rate Calculation
description: Calculate effective tax rate and adjusted (operating) tax rate from income statement and EBITA data.
---

# Tax Rate Calculation (Sub-Skill 3b)

## Prerequisites

- Income Statement extracted (Skill 2b)
- EBITA calculated (Skill 3a)
- GAAP Reconciliation extracted if available (Skill 2e)

## Step-by-Step Instructions

### Step 1: Read Extracted Data

From the document's `.md` file, read:
1. **Income Statement**: `income_before_taxes`, `income_tax_provision`, `net_income` (by standardized name)
2. **EBITA** result from Sub-Skill 3a
3. **GAAP Reconciliation** items (if available)

### Step 2: Calculate Effective Tax Rate

The simple tax rate based on reported figures:

**Primary formula:**
```
Effective Tax Rate = -(Income Tax Expense / Income Before Taxes)
```

The negation is because tax expense is stored as negative (sign-normalized in Skill 2b).
- Example: `-371 / 2,182 = -0.1700`, negated = `0.1700` (17.00%)

**Fallback** (if tax expense is missing):
```
Effective Tax Rate = (Income Before Taxes - Net Income) / Income Before Taxes
```
- Example: `(2,182 - 1,811) / 2,182 = 0.1700` (17.00%)

### Step 3: Calculate Adjusted (Operating) Tax Rate

The adjusted tax rate accounts for the tax effect of non-operating items that were added back or removed to get EBITA.

**Formula:**
```
Adjusted Tax = Reported Tax + Tax Effect of Adjustments
Adjusted Tax Rate = -(Adjusted Tax / EBITA)
```

**How to calculate Tax Effect:**

For each non-operating adjustment (from GAAP Reconciliation and Income Statement):

1. **Marginal Tax Rate**: Use **25%** as the default
2. **Exception**: Use **0%** for items containing: "impairment", "amortization", or "equity" (these are typically non-deductible)

**For Income Statement intermediate items** (non-operating items between Operating Income and Tax Expense):
```
Tax Effect = -(line_value) × marginal_rate
```
(Negate because IS items are sign-normalized)

**For GAAP Reconciliation addback items** (non-operating):
```
Tax Effect = line_value × marginal_rate
```
(Direct because these are already positive addbacks)

### Step 4: Validate Tax Rates

Flag unusual tax rates:
- Effective tax rate > 35% → "Appears high"
- Effective tax rate < 10% → "Appears low"
- Adjusted tax rate should generally be between 15-30% for US companies

### Step 5: Write Output to Markdown

Append to the document's `.md` file:

```markdown
---

## Tax Rates

| Field | Value |
|-------|-------|
| Income Before Taxes | {income_before_taxes} |
| Income Tax Expense | {income_tax_expense} |
| Net Income | {net_income} |
| Effective Tax Rate | {effective_tax_rate_pct}% |
| Adjusted Tax Rate | {adjusted_tax_rate_pct}% |
| Calculation Date | {current_date_iso} |

### Adjusted Tax Rate Breakdown

| # | Line Name | Value | Tax Effect | Source | Marginal Rate |
|---|-----------|-------|------------|--------|---------------|
| 1 | Interest expense | -62 | 15.50 | Intermediate | 25% |
| 2 | Amortization of intangibles | 83 | 0.00 | Non-GAAP | 0% |
| ... | ... | ... | ... | ... | ... |
| | **Reported Tax** | **-371** | | | |
| | **Total Tax Adjustment** | | **{total}** | | |
| | **Adjusted Tax** | **{adjusted_tax}** | | | |
```

---

## Reference

Based on `calculate_effective_tax_rate_from_inputs()` and `calculate_adjusted_tax_rate()` in `tiger-cafe/app/utils/historical_calculations.py`
