---
name: JSON Export
description: Export the complete DCF model, assumptions, and intrinsic value into a machine-readable JSON file for the interactive financial model viewer.
---

# JSON Export (Sub-Skill 5e)

## Prerequisites

- All prior sub-skills (5a–5d) must be completed
- All data must be present in `TICKER_metadata.md`

## Overview

This sub-skill reads all the financial modeling outputs from the markdown file and writes them into a structured JSON file that can be consumed by the interactive HTML viewer (`tools/financial_model_viewer.html`).

## Step-by-Step Instructions

### Step 1: Read All Model Data

From `TICKER_metadata.md`, read:

1. **Company Info**: Ticker, Company Name, Currency, Unit
2. **Financial History**: All rows from the Financial History table
3. **WACC**: All fields from the WACC section
4. **Assumptions**: All fields from the DCF Assumptions section
5. **Projections**: All rows/columns from the DCF Model Projections table
6. **Valuation**: Enterprise Value, Terminal Value, PV breakdown
7. **Intrinsic Value**: Equity Value, Per-Share value, ADR conversion

### Step 2: Construct JSON Structure

Build the following JSON structure:

```json
{
  "ticker": "BIDU",
  "company_name": "Baidu, Inc.",
  "currency": "RMB",
  "unit": "millions",
  "generated_date": "2026-03-03",

  "historical": [
    {
      "time_period": "Q4 2023",
      "period_end": "2023-12-31",
      "revenue": 34951,
      "ebita": 5437,
      "ebita_margin": 0.1556,
      "adj_tax_rate": 0.0335,
      "nopat": 5255,
      "invested_capital": 47888,
      "roic": 0.1097,
      "organic_growth": null
    }
  ],

  "wacc": {
    "risk_free_rate": 0.0425,
    "equity_risk_premium": 0.055,
    "country_risk_premium": 0.01,
    "beta": 1.15,
    "cost_of_equity": 0.1173,
    "cost_of_debt": 0.04,
    "weight_equity": 0.75,
    "weight_debt": 0.25,
    "tax_rate": 0.25,
    "wacc": 0.0955
  },

  "assumptions": {
    "revenue_growth_stage1": 0.05,
    "revenue_growth_stage2": 0.03,
    "revenue_growth_terminal": 0.03,
    "ebita_margin_stage1": 0.087,
    "ebita_margin_stage2": 0.067,
    "ebita_margin_terminal": 0.067,
    "marginal_capital_turnover_stage1": 2.0,
    "marginal_capital_turnover_stage2": 2.0,
    "marginal_capital_turnover_terminal": 2.0,
    "adjusted_tax_rate": 0.25,
    "base_revenue": 130000,
    "base_invested_capital": 57339
  },

  "projections": [
    {
      "year": "Base",
      "revenue": 130000,
      "growth_rate": null,
      "ebita": 11310,
      "margin": 0.087,
      "nopat": 8483,
      "invested_capital": 57339,
      "roic": 0.148,
      "fcf": null,
      "discount_factor": null,
      "pv_fcf": null
    },
    {
      "year": 1,
      "revenue": 136500,
      "growth_rate": 0.05,
      "ebita": 11231,
      "margin": 0.083,
      "nopat": 8423,
      "invested_capital": 60589,
      "roic": 0.139,
      "fcf": 5173,
      "discount_factor": 0.955,
      "pv_fcf": 4940
    }
  ],

  "terminal": {
    "revenue": 150000,
    "growth_rate": 0.03,
    "ebita": 10050,
    "margin": 0.067,
    "nopat": 7538,
    "invested_capital": 70000,
    "roic": 0.108,
    "ronic": 0.1005,
    "reinvestment_rate": 0.2985,
    "fcf": 5287,
    "terminal_value": 81338,
    "discount_factor": 0.42,
    "pv_terminal": 34162
  },

  "valuation": {
    "sum_pv_fcf": 40000,
    "pv_terminal_value": 34162,
    "enterprise_value": 74162,
    "cash_and_equivalents": 38620,
    "short_term_investments": 86195,
    "long_term_investments": 46596,
    "total_debt": 85000,
    "equity_value": 160577,
    "diluted_shares": 2713,
    "intrinsic_value_per_share": 59.19,
    "adr_ratio": 8,
    "intrinsic_value_per_adr": 473.49,
    "fx_rate": 7.25,
    "intrinsic_value_per_adr_usd": 65.31
  }
}
```

> ⚠️ All percentages/rates must be stored as **decimals** (0.05 not 5%). All monetary values stay in the company's local currency and stated unit (e.g., RMB millions).

### Step 3: Write JSON File

Save to:

```
output_data/TICKER/TICKER_financial_model.json
```

Example: `output_data/BIDU/BIDU_financial_model.json`

### Step 4: Validate JSON

Perform these checks on the output JSON:

| #   | Check                                        | Expected                                                |
| --- | -------------------------------------------- | ------------------------------------------------------- |
| 1   | `projections` has 12 items                   | Base + Years 1-10 + Terminal                            |
| 2   | `enterprise_value > 0`                       | Should be positive                                      |
| 3   | `equity_value > 0`                           | Should be positive (though can be negative in distress) |
| 4   | `wacc.wacc` between 0.05 and 0.20            | Reasonable range                                        |
| 5   | Terminal `reinvestment_rate` between 0 and 1 | Cannot reinvest more than 100%                          |
| 6   | All numeric values are actual numbers        | No strings like "N/A" in numeric fields                 |

### Step 5: Confirm Completion

Report to the user:

```
✅ Financial Model exported:
   output_data/BIDU/BIDU_financial_model.json
   Enterprise Value: RMB {enterprise_value}M
   Intrinsic Value/ADR: ${iv_per_adr_usd}
   Current Price: ${current_price} (if available)
   Upside/Downside: {pct}%
```

---

## Important Notes

- The JSON structure is designed to be consumed by the interactive HTML viewer. Changing the schema requires updating the viewer too.
- Historical entries should include **all** available quarters, even those with incomplete data (they'll show as `null` values in the viewer).
- The `projections` array should include the base year as the first element (year = "Base"), followed by years 1-10. The terminal column is a separate object.
- When the viewer is built (see ROADMAP), users will be able to modify assumptions interactively and see instant recalculations.

## Reference

JSON schema designed to match the data contract expected by the tiger-cafe `FinancialModel.jsx` component.
