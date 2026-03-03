# JSON Export Example: Adobe Inc. (ADBE)

> Source: All prior sub-skills (5a–5d) for ADBE

## Input

All data is read from `ADBE_metadata.md` sections: Financial History, WACC, DCF Assumptions, DCF Model, and Intrinsic Value.

## Output File

`output_data/ADBE/ADBE_financial_model.json`

## Output JSON

```json
{
  "ticker": "ADBE",
  "company_name": "Adobe Inc.",
  "currency": "USD",
  "unit": "millions",
  "generated_date": "2026-03-03",

  "historical": [
    {
      "time_period": "Q1 2024",
      "revenue": 5182,
      "ebita": 1998,
      "ebita_margin": 0.3856,
      "adj_tax_rate": 0.2927,
      "nopat": 1413,
      "invested_capital": -1104,
      "organic_growth": 0.12
    },
    {
      "time_period": "Q2 2024",
      "revenue": 5309,
      "ebita": 1969,
      "ebita_margin": 0.3709,
      "adj_tax_rate": 0.1756,
      "nopat": 1623,
      "invested_capital": -887,
      "organic_growth": 0.11
    },
    {
      "time_period": "Q3 2024",
      "revenue": 5408,
      "ebita": 2030,
      "ebita_margin": 0.3754,
      "adj_tax_rate": 0.1647,
      "nopat": 1695,
      "invested_capital": -595,
      "organic_growth": 0.11
    },
    {
      "time_period": "Q4 2024",
      "revenue": 5606,
      "ebita": 2141,
      "ebita_margin": 0.3819,
      "adj_tax_rate": 0.1399,
      "nopat": 1841,
      "invested_capital": -1277,
      "organic_growth": 0.11
    },
    {
      "time_period": "Q1 2025",
      "revenue": 5714,
      "ebita": 2246,
      "ebita_margin": 0.3931,
      "adj_tax_rate": 0.1756,
      "nopat": 1852,
      "invested_capital": -1170,
      "organic_growth": 0.11
    },
    {
      "time_period": "Q2 2025",
      "revenue": 5873,
      "ebita": 2192,
      "ebita_margin": 0.3732,
      "adj_tax_rate": 0.185,
      "nopat": 1786,
      "invested_capital": -1020,
      "organic_growth": 0.11
    },
    {
      "time_period": "Q3 2025",
      "revenue": 5988,
      "ebita": 2252,
      "ebita_margin": 0.3761,
      "adj_tax_rate": 0.185,
      "nopat": 1835,
      "invested_capital": -855,
      "organic_growth": 0.1
    },
    {
      "time_period": "Q4 2025",
      "revenue": 6194,
      "ebita": 2322,
      "ebita_margin": 0.3749,
      "adj_tax_rate": 0.185,
      "nopat": 1892,
      "invested_capital": -1606,
      "organic_growth": 0.1
    }
  ],

  "wacc": {
    "risk_free_rate": 0.042,
    "equity_risk_premium": 0.05,
    "country_risk_premium": 0.0,
    "beta_levered": 1.532,
    "beta_unlevered": 1.4716,
    "beta_adjusted": 1.3144,
    "cost_of_equity": 0.1077,
    "cost_of_debt": 0.05,
    "total_debt": 6210,
    "interest_expense_annual": 264,
    "market_cap_usd": 113436409912,
    "weight_equity": 0.9481,
    "weight_debt": 0.0519,
    "tax_rate": 0.25,
    "wacc_calculated": 0.1041,
    "wacc": 0.1041
  },

  "assumptions": {
    "revenue_growth_stage1": 0.105,
    "revenue_growth_stage2": 0.095,
    "revenue_growth_terminal": 0.04,
    "ebita_margin_stage1": 0.3793,
    "ebita_margin_stage2": 0.3993,
    "ebita_margin_terminal": 0.3993,
    "marginal_capital_turnover_stage1": 100.0,
    "marginal_capital_turnover_stage2": 100.0,
    "marginal_capital_turnover_terminal": 100.0,
    "adjusted_tax_rate": 0.1827,
    "base_revenue": 23769,
    "base_invested_capital": -1606
  },

  "projections": [
    {
      "year": "Base",
      "revenue": 23769,
      "growth_rate": null,
      "ebita": 9012,
      "margin": 0.3793,
      "nopat": 7365,
      "invested_capital": -1606,
      "roic": -4.5859,
      "fcf": null,
      "discount_factor": null,
      "pv_fcf": null
    },
    {
      "year": 1,
      "revenue": 26265,
      "growth_rate": 0.105,
      "ebita": 9963,
      "margin": 0.3793,
      "nopat": 8143,
      "invested_capital": -1581,
      "delta_ic": 25,
      "roic": -5.1505,
      "fcf": 8118,
      "discount_factor": 0.9517,
      "pv_fcf": 7726
    },
    {
      "year": 2,
      "revenue": 28970,
      "growth_rate": 0.103,
      "ebita": 11105,
      "margin": 0.3833,
      "nopat": 9077,
      "invested_capital": -1554,
      "delta_ic": 27,
      "roic": -5.8408,
      "fcf": 9050,
      "discount_factor": 0.862,
      "pv_fcf": 7801
    },
    {
      "year": 3,
      "revenue": 31896,
      "growth_rate": 0.101,
      "ebita": 12354,
      "margin": 0.3873,
      "nopat": 10098,
      "invested_capital": -1525,
      "delta_ic": 29,
      "roic": -6.6226,
      "fcf": 10068,
      "discount_factor": 0.7807,
      "pv_fcf": 7861
    },
    {
      "year": 4,
      "revenue": 35054,
      "growth_rate": 0.099,
      "ebita": 13717,
      "margin": 0.3913,
      "nopat": 11212,
      "invested_capital": -1493,
      "delta_ic": 32,
      "roic": -7.5089,
      "fcf": 11180,
      "discount_factor": 0.7071,
      "pv_fcf": 7906
    },
    {
      "year": 5,
      "revenue": 38454,
      "growth_rate": 0.097,
      "ebita": 15202,
      "margin": 0.3953,
      "nopat": 12425,
      "invested_capital": -1459,
      "delta_ic": 34,
      "roic": -8.5153,
      "fcf": 12391,
      "discount_factor": 0.6405,
      "pv_fcf": 7936
    },
    {
      "year": 6,
      "revenue": 42107,
      "growth_rate": 0.095,
      "ebita": 16814,
      "margin": 0.3993,
      "nopat": 13743,
      "invested_capital": -1423,
      "delta_ic": 37,
      "roic": -9.6605,
      "fcf": 13707,
      "discount_factor": 0.5801,
      "pv_fcf": 7951
    },
    {
      "year": 7,
      "revenue": 45644,
      "growth_rate": 0.084,
      "ebita": 18227,
      "margin": 0.3993,
      "nopat": 14898,
      "invested_capital": -1387,
      "delta_ic": 35,
      "roic": -10.739,
      "fcf": 14862,
      "discount_factor": 0.5254,
      "pv_fcf": 7809
    },
    {
      "year": 8,
      "revenue": 48976,
      "growth_rate": 0.073,
      "ebita": 19557,
      "margin": 0.3993,
      "nopat": 15985,
      "invested_capital": -1354,
      "delta_ic": 33,
      "roic": -11.8065,
      "fcf": 15952,
      "discount_factor": 0.4759,
      "pv_fcf": 7591
    },
    {
      "year": 9,
      "revenue": 52013,
      "growth_rate": 0.062,
      "ebita": 20770,
      "margin": 0.3993,
      "nopat": 16976,
      "invested_capital": -1324,
      "delta_ic": 30,
      "roic": -12.8262,
      "fcf": 16946,
      "discount_factor": 0.431,
      "pv_fcf": 7304
    },
    {
      "year": 10,
      "revenue": 54665,
      "growth_rate": 0.051,
      "ebita": 21829,
      "margin": 0.3993,
      "nopat": 17842,
      "invested_capital": -1297,
      "delta_ic": 27,
      "roic": -13.756,
      "fcf": 17816,
      "discount_factor": 0.3904,
      "pv_fcf": 6955
    }
  ],

  "terminal": {
    "revenue": 56852,
    "growth_rate": 0.04,
    "ebita": 22702,
    "margin": 0.3993,
    "nopat": 18556,
    "invested_capital": -1274,
    "roic": -14.5616,
    "ronic": 32.6388,
    "reinvestment_rate": 0.0012,
    "fcf_terminal": 18533,
    "terminal_value": 289241,
    "discount_factor": 0.3904,
    "pv_terminal": 112921
  },

  "valuation": {
    "sum_pv_fcf": 76840,
    "pv_terminal_value": 112921,
    "enterprise_value": 189761,
    "cash_and_equivalents": 5431,
    "short_term_investments": 1164,
    "long_term_investments": 0,
    "total_debt": 6210,
    "equity_value": 190146,
    "diluted_shares": 417,
    "intrinsic_value_per_share": 455.99,
    "current_price": 270.99,
    "upside_downside_pct": 68.3
  }
}
```

## Validation Checks

| #   | Check                                        | Result              |
| --- | -------------------------------------------- | ------------------- |
| 1   | `projections` has 11 items (Base + Yr 1-10)  | ✅ 11 items         |
| 2   | `enterprise_value > 0`                       | ✅ $189,761M        |
| 3   | `equity_value > 0`                           | ✅ $190,146M        |
| 4   | `wacc.wacc` between 0.05 and 0.20            | ✅ 0.1041           |
| 5   | Terminal `reinvestment_rate` between 0 and 1 | ✅ 0.0012           |
| 6   | All numeric values are numbers               | ✅ No string values |

## Completion Report

```
Financial Model exported:
   output_data/ADBE/ADBE_financial_model.json
   Enterprise Value: $189,761M
   Intrinsic Value/Share: $455.99
   Current Price: $270.99
   Upside/Downside: +68.3%
```

### Notes

- ADBE is a straightforward US-listed company: no ADR conversion, no FX, no minority interests
- The `roic` values are negative because invested capital is negative — this is economically correct for an asset-light SaaS company
- The JSON is consumed by `tools/financial_model_viewer.html` at `http://127.0.0.1:3000/?ticker=ADBE`
