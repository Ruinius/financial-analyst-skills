# WACC Example: Adobe Inc. (ADBE)

> Source: ADBE Q4 2025 (period ending 2025-11-28) + Yahoo Finance market data pulled 2026-03-03

## Inputs

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

## Calculation Walkthrough

### Step 1: Gather Market Data

- Market Cap (E) = $113,436,409,912
- Raw Levered Beta = 1.532
- Total Debt (D) = $6,210M = $6,210,000,000

No FX conversion needed (ADBE is US-listed, USD-denominated).

### Step 2: Compute D/E Ratio

```
D/E = $6,210,000,000 / $113,436,409,912 = 0.0547
```

### Step 3a: Unlever Beta (Hamada Equation)

```
β_unlevered = β_levered / (1 + (1 - t) × D/E)
            = 1.532 / (1 + (1 - 0.25) × 0.0547)
            = 1.532 / (1 + 0.75 × 0.0547)
            = 1.532 / 1.0410
            = 1.4716
```

### Step 3b: Blume's Adjustment

```
β_adjusted = (2/3) × β_unlevered + (1/3) × 1.0
           = (2/3) × 1.4716 + (1/3) × 1.0
           = 0.9811 + 0.3333
           = 1.3144
```

### Step 4: CAPM (Cost of Equity)

```
Cost of Equity = Rf + β_adjusted × (ERP + CRP)
               = 4.20% + 1.3144 × (5.00% + 0.00%)
               = 4.20% + 6.57%
               = 10.77%
```

Country Risk Premium = 0.0% (US company).

### Step 5: Cost of Debt

```
Cost of Debt = |$264M| / $6,210M = 4.25%
```

Floor of 5.0% applies → **Cost of Debt = 5.00%**

### Step 6: Capital Weights

```
V = E + D = $113,436M + $6,210M = $119,646M
Weight of Equity = E/V = 94.81%
Weight of Debt   = D/V = 5.19%
```

### Step 7: WACC

```
WACC = (E/V × CoE) + (D/V × CoD × (1 - t))
     = (0.9481 × 0.1077) + (0.0519 × 0.05 × (1 - 0.25))
     = 0.1021 + 0.0019
     = 10.41%
```

Bounded range [7%, 11%]: **WACC = 10.41%** ✓ (within bounds)

## Output

```markdown
## WACC

| Field                   | Value            |
| ----------------------- | ---------------- |
| Risk-Free Rate          | 4.20%            |
| Equity Risk Premium     | 5.00%            |
| Country Risk Premium    | 0.00%            |
| Raw Levered Beta        | 1.532            |
| Unlevered Beta          | 1.4716           |
| Adjusted Beta (Blume's) | 1.3144           |
| Cost of Equity          | 10.77%           |
| Total Debt              | $6,210M          |
| Interest Expense (Ann.) | $264M            |
| Cost of Debt            | 5.00%            |
| Market Cap              | $113,436,409,912 |
| Weight of Equity        | 94.81%           |
| Weight of Debt          | 5.19%            |
| Tax Rate (Statutory)    | 25.00%           |
| Calculated WACC         | 10.41%           |
| **WACC (Bounded)**      | **10.41%**       |
| Calculation Date        | 2026-03-03       |
```
