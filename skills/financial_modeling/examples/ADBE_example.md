# Financial Modeling Example: Adobe Inc. (ADBE)

> Source: ADBE_metadata.md (Q1 2024 – Q4 2025 history) + Qualitative Assessment + Yahoo Finance market data pulled 2026-03-03

This example shows the complete end-to-end financial modeling pipeline: WACC → Assumptions → DCF → Intrinsic Value → JSON Export.

---

## Step 1: WACC Calculation

### Inputs

**From `tools/market_data.py profile ADBE`:**

```json
{
  "share_price": 270.99,
  "market_cap": 113436409912,
  "beta": 1.532,
  "currency": "USD",
  "exchange": "NMS"
}
```

**From Balance Sheet (ADBE_EA_20251210.md):**

- Short-term debt: $0M
- Long-term debt: $6,210M
- Total Debt (D): $6,210M

**From Income Statement:**

- Interest Expense (quarterly): $66M
- Interest Expense (annualized): $264M

### Calculation Walkthrough

**1a: D/E Ratio**

```
D/E = $6,210,000,000 / $113,436,409,912 = 0.0547
```

**1b: Unlever Beta (Hamada Equation)**

```
β_unlevered = β_levered / (1 + (1 - t) × D/E)
            = 1.532 / (1 + (1 - 0.25) × 0.0547)
            = 1.532 / 1.0410
            = 1.4716
```

**1c: Blume's Adjustment**

```
β_adjusted = (2/3) × β_unlevered + (1/3) × 1.0
           = (2/3) × 1.4716 + (1/3) × 1.0
           = 1.3144
```

**1d: CAPM (Cost of Equity)**

```
Cost of Equity = Rf + β_adjusted × (ERP + CRP)
               = 4.20% + 1.3144 × (5.00% + 0.00%)
               = 10.77%
```

**1e: Cost of Debt**

```
Cost of Debt = |$264M| / $6,210M = 4.25%
Floor of 5.0% applies → Cost of Debt = 5.00%
```

**1f: Capital Weights**

```
V = E + D = $113,436M + $6,210M = $119,646M
Weight of Equity = E/V = 94.81%
Weight of Debt   = D/V = 5.19%
```

**1g: WACC**

```
WACC = (E/V × CoE) + (D/V × CoD × (1 - t))
     = (0.9481 × 0.1077) + (0.0519 × 0.05 × (1 - 0.25))
     = 10.41%
```

### Output

| Field | Value |
|-------|-------|
| Risk-Free Rate | 4.20% |
| Equity Risk Premium | 5.00% |
| Raw Levered Beta | 1.532 |
| Unlevered Beta | 1.4716 |
| Adjusted Beta (Blume's) | 1.3144 |
| Cost of Equity | 10.77% |
| Total Debt | $6,210M |
| Cost of Debt | 5.00% |
| Weight of Equity | 94.81% |
| Weight of Debt | 5.19% |
| **WACC (Bounded)** | **10.41%** |

---

## Step 2: DCF Assumptions

### Inputs

**Financial History (L4Q = Q1-Q4 2025):**

| Quarter | Revenue | EBITA | EBITA Margin | Adj Tax Rate | IC | Organic Growth |
|---------|---------|-------|--------------|--------------|----|----------------|
| Q1 2025 | 5,714 | 2,246 | 39.31% | 17.56% | -1,170 | 11.0% |
| Q2 2025 | 5,873 | 2,192 | 37.32% | 18.50% | -1,020 | 11.0% |
| Q3 2025 | 5,988 | 2,252 | 37.61% | 18.50% | -855 | 10.0% |
| Q4 2025 | 6,194 | 2,322 | 37.49% | 18.50% | -1,606 | 10.0% |

**Qualitative Assessment:**

- Economic Moat: **Wide** (switching costs, first-mover, cross-sell flywheel)
- EBITA Margin Outlook: **Expand +2 pp** over 5 years
- Organic Growth Outlook: **Stable to slight decrease, -1 pp**

### Calculation Walkthrough

```
L4Q Revenue (annualized)   = 5714 + 5873 + 5988 + 6194 = $23,769M
L4Q EBITA Margin (average) = (39.31 + 37.32 + 37.61 + 37.49) / 4 = 37.93%
L4Q Adj Tax Rate (average) = (17.56 + 18.50 + 18.50 + 18.50) / 4 = 18.27%
L4Q Organic Growth (avg)   = (11.0 + 11.0 + 10.0 + 10.0) / 4 = 10.5%
MCT: IC is negative → default to 100.0x (asset-light software)
```

### Output

| Parameter | Stage 1 (Yr 1-5) | Stage 2 (Yr 6-10) | Terminal |
|-----------|-------------------|--------------------|----------|
| Revenue Growth | 10.50% | 9.50% | 4.00% |
| EBITA Margin | 37.93% | 39.93% | 39.93% |
| Marginal Capital Turnover | 100.0x | 100.0x | 100.0x |

**Rationale:**
- Revenue Growth: L4Q ~10.5%. Qualitative: -1 pp → Stage 2 = 9.5%. Wide moat → terminal 4.0%.
- EBITA Margin: L4Q ~37.9%. Qualitative: +2 pp → Stage 2 = 39.9%. Wide moat sustains terminal.
- Capital Turnover: Negative IC → MCT = 100.0x (minimal reinvestment needed).

---

## Step 3: DCF Model

### Projections

| | Base | Yr 1 | Yr 2 | Yr 3 | Yr 4 | Yr 5 | Yr 6 | Yr 7 | Yr 8 | Yr 9 | Yr 10 | Terminal |
|---|------|------|------|------|------|------|------|------|------|------|-------|----------|
| Revenue | 23,769 | 26,265 | 28,970 | 31,896 | 35,054 | 38,454 | 42,107 | 45,644 | 48,976 | 52,013 | 54,665 | 56,852 |
| Growth | -- | 10.50% | 10.30% | 10.10% | 9.90% | 9.70% | 9.50% | 8.40% | 7.30% | 6.20% | 5.10% | 4.00% |
| EBITA | 9,012 | 9,963 | 11,105 | 12,354 | 13,717 | 15,202 | 16,814 | 18,227 | 19,557 | 20,770 | 21,829 | 22,702 |
| NOPAT | 7,365 | 8,143 | 9,077 | 10,098 | 11,212 | 12,425 | 13,743 | 14,898 | 15,985 | 16,976 | 17,842 | 18,556 |
| FCF | -- | 8,118 | 9,050 | 10,068 | 11,180 | 12,391 | 13,707 | 14,862 | 15,952 | 16,946 | 17,816 | 289,241 |
| PV of FCF | -- | 7,726 | 7,801 | 7,861 | 7,906 | 7,936 | 7,951 | 7,809 | 7,591 | 7,304 | 6,955 | 112,921 |

### Valuation

| Field | Value |
|-------|-------|
| Sum of PV (Years 1-10) | $76,840M |
| PV of Terminal Value | $112,921M |
| **Enterprise Value** | **$189,761M** |
| TV as % of EV | 59.5% |

### Key Observations

- **MCT = 100x** means virtually all NOPAT converts to FCF (~$25-37M/year reinvestment).
- **Invested capital stays negative** throughout — ADBE's deferred revenue exceeds operating assets.
- **TV as % of EV = 59.5%** — healthy range. If this exceeds ~80%, near-term projections are likely too pessimistic.

---

## Step 4: Intrinsic Value

### Inputs

**From Balance Sheet (Q4 2025):**

- Cash and Equivalents: $5,431M
- Short-Term Investments: $1,164M
- Long-Term Investments: $0M
- Total Debt: $6,210M

**From Shares Outstanding:** Diluted = 417M

**Current Price:** $270.99

### Equity Bridge

```
Equity Value = EV - Debt + Cash + STI + LTI
             = $189,761 - $6,210 + $5,431 + $1,164 + $0
             = $190,146M

IV/Share = $190,146M / 417M = $455.99
Upside   = ($455.99 / $270.99) - 1 = +68.3%
```

### Output

| Field | Value |
|-------|-------|
| Enterprise Value | $189,761M |
| (+) Cash and Equivalents | $5,431M |
| (+) Short-Term Investments | $1,164M |
| (-) Total Debt | $6,210M |
| **Equity Value** | **$190,146M** |
| **Intrinsic Value Per Share** | **$455.99** |
| **Upside/Downside** | **+68.3%** |

**Bridge Notes:**
- Balance sheet from ADBE Q4 2025 (period ending 2025-11-28)
- No ADR conversion needed (US-listed, USD-denominated)

---

## Step 5: JSON Export

The complete model is exported to `output_data/ADBE/ADBE_financial_model.json` for the interactive frontend viewer (`tools/financial_model_viewer.html`).

### Validation Checks

| # | Check | Result |
|---|-------|--------|
| 1 | `projections` has 11 items (Base + Yr 1-10) | ✅ |
| 2 | `enterprise_value > 0` | ✅ $189,761M |
| 3 | `equity_value > 0` | ✅ $190,146M |
| 4 | `wacc.wacc` between 0.05 and 0.20 | ✅ 0.1041 |
| 5 | Terminal `reinvestment_rate` between 0 and 1 | ✅ 0.0012 |
| 6 | All numeric values are numbers | ✅ |

### Notes

- ADBE is a straightforward US-listed company: no ADR conversion, no FX, no minority interests
- The `roic` values are negative because invested capital is negative — economically correct for asset-light SaaS
- The JSON is consumed by `tools/financial_model_viewer.html` at `http://127.0.0.1:3000/?ticker=ADBE`
