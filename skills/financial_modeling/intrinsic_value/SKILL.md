---
name: Intrinsic Value Calculation
description: Convert Enterprise Value to equity value per share by subtracting debt, adding cash, and dividing by diluted shares outstanding.
---

# Intrinsic Value Calculation (Sub-Skill 5d)

## Prerequisites

- DCF Model completed (Sub-Skill 5c) — need Enterprise Value
- Latest Balance Sheet data (from most recent earnings document)
- Shares Outstanding (from most recent earnings document)

## Overview

Enterprise Value is the value of the entire business. To get the intrinsic value per share, we need to:

1. Bridge from Enterprise Value to Equity Value
2. Divide by diluted shares

```
Equity Value = Enterprise Value - Net Debt + Excess Cash
Intrinsic Value Per Share = Equity Value / Diluted Shares
```

## Step-by-Step Instructions

### Step 1: Read Enterprise Value

From the DCF Model section of `TICKER_metadata.md`, read:

- `Enterprise Value`

### Step 2: Read Balance Sheet Components

From the most recent earnings document (`output_data/TICKER/TICKER_EA_*.md`), read the Balance Sheet to compute:

**Cash and Equivalents** (non-operating current assets):

- `cash_and_equivalents`
- `restricted_cash`
- `short_term_investments`

**Total Debt** (all debt-classified items):

- `short_term_debt`
- `current_portion_long_term_debt`
- `current_portion_convertible_debt`
- `long_term_debt`
- `convertible_debt`

**Other non-operating items** to add back:

- `long_term_investments` (if material)

> Note: Use the Balance Sheet values from the **same document** used as the base year for the DCF model.

### Step 3: Calculate Net Debt

```
Net Debt = Total Debt - Cash and Equivalents
```

If Net Debt is negative, the company has more cash than debt (net cash position).

### Step 4: Calculate Equity Value

```
Equity Value = Enterprise Value - Total Debt + Cash and Equivalents + Long-Term Investments
```

Equivalently:

```
Equity Value = Enterprise Value + Net Cash - Long-Term Debt + Long-Term Investments
```

The key principle: add back all **non-operating assets** and subtract all **non-operating liabilities** (debt) from Enterprise Value.

### Step 5: Read Shares Outstanding

From the Shares Outstanding section of the most recent document:

- Use **Diluted Shares Outstanding** for the per-share calculation
- Note the unit (typically millions)

### Step 6: Calculate Intrinsic Value Per Share

```
Intrinsic Value Per Share = Equity Value / Diluted Shares Outstanding
```

Both must be in the same unit. If Equity Value is in millions and shares are in millions, the result is in the company's local currency per share.

**For ADR conversion** (Chinese companies like BIDU):

- BIDU: 1 ADR = 8 Class A ordinary shares
- If you computed intrinsic value per ordinary share, multiply by 8 to get per-ADR value
- Then convert from RMB to USD using the current exchange rate

### Step 7: Write Output to Markdown

Append to `TICKER_metadata.md`:

```markdown
---

## Intrinsic Value

| Field                         | Value                       |
| ----------------------------- | --------------------------- |
| Enterprise Value              | {enterprise_value}          |
| (+) Cash and Equivalents      | {cash}                      |
| (+) Short-Term Investments    | {sti}                       |
| (+) Long-Term Investments     | {lti}                       |
| (-) Total Debt                | {total_debt}                |
| **Equity Value**              | **{equity_value}**          |
| Diluted Shares Outstanding    | {diluted_shares}            |
| **Intrinsic Value Per Share** | **{iv_per_share}**          |
| Currency                      | {currency}                  |
| ADR Ratio                     | {adr_ratio} (if applicable) |
| Intrinsic Value Per ADR       | {iv_per_adr} {currency}     |
| Exchange Rate                 | {fx_rate} (if applicable)   |
| Intrinsic Value Per ADR (USD) | {iv_per_adr_usd} USD        |
| Calculation Date              | {current_date_iso}          |

### Bridge Notes

- {notes about which balance sheet was used as source}
- {notes about ADR conversion if applicable}
```

---

## Important Notes

- The Equity Bridge is where many valuation errors occur. Make sure the balance sheet items are **comprehensive** — missing a large debt item or cash balance will materially affect the per-share value.
- For companies with **multiple share classes** (like BIDU's Class A and Class B), use total diluted shares across all classes.
- **Minority interests** (noncontrolling interests) can optionally be subtracted from Equity Value for a more precise parent-only valuation. For simplicity, this skill does not adjust for minority interests unless they are very large (>10% of equity value).
- The intrinsic value is in the company's **local currency**. For US-listed ADRs of foreign companies, an additional FX conversion step is needed to get a USD-denominated price target.

## Reference

Standard equity bridge methodology used in investment banking DCF models.
