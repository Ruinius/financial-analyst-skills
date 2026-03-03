# Intrinsic Value Example: Adobe Inc. (ADBE)

> Source: DCF Model (Sub-Skill 5c) + Balance Sheet from ADBE_EA_20251210.md

## Inputs

**From DCF Model:**

- Enterprise Value: $189,761M

**From Balance Sheet (Q4 2025, period ending 2025-11-28):**

- Cash and Equivalents: $5,431M
- Short-Term Investments: $1,164M
- Long-Term Investments: $0M (none on ADBE's balance sheet)
- Short-Term Debt: $0M
- Long-Term Debt: $6,210M
- Total Debt: $6,210M

**From Shares Outstanding:**

- Diluted Shares Outstanding: 417M

**From `tools/market_data.py profile ADBE`:**

- Current Share Price: $270.99
- Currency: USD (no ADR/FX conversion needed)

## Calculation Walkthrough

### Step 1: Enterprise Value

```
EV = $189,761M (from DCF Model)
```

### Step 2: Balance Sheet Bridge

```
(+) Cash and Equivalents     = $5,431M
(+) Short-Term Investments   = $1,164M
(+) Long-Term Investments    = $0M
(-) Total Debt               = $6,210M
```

### Step 3: Equity Value

```
Equity Value = EV - Debt + Cash + STI + LTI
             = $189,761 - $6,210 + $5,431 + $1,164 + $0
             = $190,146M
```

### Step 4: Intrinsic Value Per Share

```
IV/Share = $190,146M / 417M = $455.99
```

### Step 5: Upside/Downside

```
Upside = ($455.99 / $270.99) - 1 = +68.3%
```

### ADR/FX Notes

No conversion needed: ADBE is US-listed on NASDAQ, denominated in USD. No ADR ratio or exchange rate applies.

## Output

```markdown
## Intrinsic Value

| Field                         | Value         |
| ----------------------------- | ------------- |
| Enterprise Value              | $189,761M     |
| (+) Cash and Equivalents      | $5,431M       |
| (+) Short-Term Investments    | $1,164M       |
| (+) Long-Term Investments     | $0M           |
| (-) Total Debt                | $6,210M       |
| **Equity Value**              | **$190,146M** |
| Diluted Shares Outstanding    | 417M          |
| **Intrinsic Value Per Share** | **$455.99**   |
| Currency                      | USD           |
| Current Market Price          | $270.99       |
| **Upside/Downside**           | **+68.3%**    |
| Calculation Date              | 2026-03-03    |

### Bridge Notes

- Balance sheet from ADBE Q4 2025 (period ending 2025-11-28)
- No ADR conversion needed (US-listed, USD-denominated)
- No long-term investments on Adobe's balance sheet
```
