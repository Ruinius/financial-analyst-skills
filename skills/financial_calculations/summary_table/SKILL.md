---
name: Summary Table
description: Compile all calculated metrics into a final summary table with NOPAT and ROIC.
---

# Summary Table (Sub-Skill 3d)

## Prerequisites

- EBITA calculated (Skill 3a)
- Tax rates calculated (Skill 3b)
- Invested capital calculated (Skill 3c)
- Income Statement and Shares Outstanding data from Skill 2

## Step-by-Step Instructions

### Step 1: Read All Prior Results

From the document's `.md` file, gather:
- Revenue (from Income Statement)
- EBITA and EBITA Margin (from Sub-Skill 3a)
- Effective Tax Rate and Adjusted Tax Rate (from Sub-Skill 3b)
- Net Working Capital, Net Long-Term Operating Assets, Invested Capital, Capital Turnover (from Sub-Skill 3c)
- Interest Expense (from Income Statement, standardized_name = `interest_expense`)
- Basic and Diluted Shares Outstanding (from Skill 2c)
- Organic Growth and Simple Growth (from Skill 2d)
- Time Period, Currency, Unit (from Classification)

### Step 2: Calculate NOPAT

**NOPAT = Net Operating Profit After Tax**

```
NOPAT = EBITA × (1 - Tax Rate)
```

**Tax rate priority:**
1. Use **Adjusted Tax Rate** if available (more accurate for operating profit)
2. Fall back to **Effective Tax Rate** if adjusted is not available

### Step 3: Calculate ROIC

**ROIC = Return on Invested Capital**

```
ROIC = Annualized NOPAT / Invested Capital
```

**Annualization:**
- If time_period is quarterly (Q1, Q2, Q3, Q4): `Annualized NOPAT = NOPAT × 4`
- If time_period is full year (FY): use NOPAT as-is

### Step 4: Write the Summary Table

Append to the document's `.md` file:

```markdown
---

## Financial Summary

| Metric | Value | Notes |
|--------|-------|-------|
| **Revenue** | {revenue} | |
| **EBITA** | {ebita} | |
| **EBITA Margin** | {ebita_margin_pct}% | |
| **Effective Tax Rate** | {effective_tax_rate_pct}% | |
| **Adjusted Tax Rate** | {adjusted_tax_rate_pct}% | |
| **NOPAT** | {nopat} | Using {which_tax_rate} |
| **Net Working Capital** | {nwc} | |
| **Net Long-Term Operating Assets** | {nltoa} | |
| **Invested Capital** | {invested_capital} | |
| **Capital Turnover** | {capital_turnover}x | Annualized |
| **ROIC** | {roic_pct}% | Annualized |
| **Interest Expense** | {interest_expense} | |
| **Basic Shares Outstanding** | {basic_shares} | |
| **Diluted Shares Outstanding** | {diluted_shares} | |
| **Simple Revenue Growth** | {simple_growth_pct}% | YoY |
| **Organic Revenue Growth** | {organic_growth_pct}% | Constant currency |

### Calculation Notes

{Any warnings or notes from prior sub-skills, e.g.:}
- Revenue growth calculated from prior year comparison
- Adjusted tax rate uses 25% marginal rate (0% for amortization/impairment)
```

### Step 5: Validate Cross-Checks (MANDATORY)

Perform these sanity checks. **Items marked ❌ are hard errors** — go back and fix the upstream extraction before proceeding.

| # | Check | Expected | If Violated |
|---|-------|----------|-------------|
| 1 | Revenue > 0 | Always positive | ❌ **Re-extract Income Statement** — Revenue was not captured |
| 2 | Tax Rate ≠ 0% | Never exactly zero | ❌ **Re-run Tax Rate skill** — IS is missing `income_tax_provision` |
| 3 | NOPAT sign matches EBITA sign | Same direction | ⚠️ Tax rate may be inverted |
| 4 | Invested Capital ≠ 0 | Non-zero | ❌ **Re-extract Balance Sheet** — BS is incomplete |
| 5 | EBITA Margin 0-60% | Typical range | ⚠️ Flag if outside range |
| 6 | Revenue × EBITA Margin ≈ EBITA | Cross-check | ⚠️ Calculation error if >1% off |
| 7 | ROIC between -50% and 200% | Typical range | ⚠️ Flag if outside; >1000% means IC is near zero = incomplete BS |
| 8 | Organic/Simple Growth ≠ N/A | Always a number | ❌ **Re-run Organic Growth skill** — prior year revenue was not extracted |
| 9 | Organic/Simple Growth ≠ 0.0% | Almost never exactly zero | ⚠️ Double-check extraction |

If any ❌ error is found, **stop** and note which upstream skill needs to be re-run before the summary can be finalized.

---

## Reference

Based on `calculate_all_historical_metrics()` in `tiger-cafe/app/utils/historical_calculations.py`
