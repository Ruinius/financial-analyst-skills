# DCF Model Example: Adobe Inc. (ADBE)

> Source: WACC (10.41%) + Assumptions from Sub-Skills 5a–5b

## Inputs

- **Base Revenue**: $23,769M (annualized L4Q)
- **Base Invested Capital**: -$1,606M
- **WACC**: 10.41%
- **Tax Rate**: 18.27%
- **Growth**: S1=10.5% → S2=9.5% → T=4.0%
- **Margin**: S1=37.93% → S2=39.93% → T=39.93%
- **MCT**: 100.0x (all stages)

## Calculation Walkthrough

### Step 1: Base Year (Year 0)

```
Base Revenue  = $23,769M
Base EBITA    = (2246 + 2192 + 2252 + 2322) = $9,012M
Base NOPAT    = $9,012M × (1 - 0.1827) = $7,365M
Base IC       = -$1,606M
Base ROIC     = $7,365M / (-$1,606M) = negative (IC < 0)
```

### Step 2: Year 1 Projection (example)

```
Growth Rate   = g1 + ((g2 - g1) / 5) × (1 - 1) = 10.50%
Margin        = m1 + ((m2 - m1) / 5) × (1 - 1) = 37.93%
Revenue       = $23,769M × 1.105 = $26,265M
ΔRevenue      = $26,265 - $23,769 = $2,496M
EBITA         = $26,265M × 0.3793 = $9,963M
NOPAT         = $9,963M × (1 - 0.1827) = $8,143M
ΔIC           = $2,496M / 100.0 = $25M          ← minimal reinvestment!
IC            = -$1,606M + $25M = -$1,581M
FCF           = $8,143M - $25M = $8,118M
Discount Fac  = 1 / (1.1041)^(1 - 0.5) = 0.9517  ← mid-year convention
PV of FCF     = $8,118M × 0.9517 = $7,726M
```

### Step 3: Terminal Value

```
Revenue_T    = $54,665M × 1.04 = $56,852M
EBITA_T      = $56,852M × 0.3993 = $22,702M
NOPAT_T      = $22,702M × (1 - 0.1827) = $18,556M
RONIC        = 0.3993 × (1 - 0.1827) × 100.0 = 3263.88%
Reinvest Rate = 4.0% / 3263.88% = 0.12%
FCF_T        = $18,556M × (1 - 0.0012) = $18,533M
TV           = $18,533M / (0.1041 - 0.04) = $289,241M
PV_TV        = $289,241M × 0.3904 = $112,921M
```

### Step 4: Enterprise Value

```
Sum PV FCF (Yr 1-10) = $76,840M
PV Terminal Value     = $112,921M
Enterprise Value      = $189,761M
TV as % of EV         = 59.5%
```

## Output

```markdown
## DCF Model

### Projections

|           | Base   | Yr 1   | Yr 2   | Yr 3   | Yr 4   | Yr 5   | Yr 6   | Yr 7   | Yr 8   | Yr 9   | Yr 10  | Terminal |
| --------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | -------- |
| Revenue   | 23,769 | 26,265 | 28,970 | 31,896 | 35,054 | 38,454 | 42,107 | 45,644 | 48,976 | 52,013 | 54,665 | 56,852   |
| Growth    | --     | 10.50% | 10.30% | 10.10% | 9.90%  | 9.70%  | 9.50%  | 8.40%  | 7.30%  | 6.20%  | 5.10%  | 4.00%    |
| EBITA     | 9,012  | 9,963  | 11,105 | 12,354 | 13,717 | 15,202 | 16,814 | 18,227 | 19,557 | 20,770 | 21,829 | 22,702   |
| Margin    | 37.93% | 37.93% | 38.33% | 38.73% | 39.13% | 39.53% | 39.93% | 39.93% | 39.93% | 39.93% | 39.93% | 39.93%   |
| NOPAT     | 7,365  | 8,143  | 9,077  | 10,098 | 11,212 | 12,425 | 13,743 | 14,898 | 15,985 | 16,976 | 17,842 | 18,556   |
| IC        | -1,606 | -1,581 | -1,554 | -1,525 | -1,493 | -1,459 | -1,423 | -1,387 | -1,354 | -1,324 | -1,297 | -1,274   |
| FCF       | --     | 8,118  | 9,050  | 10,068 | 11,180 | 12,391 | 13,707 | 14,862 | 15,952 | 16,946 | 17,816 | 289,241  |
| PV of FCF | --     | 7,726  | 7,801  | 7,861  | 7,906  | 7,936  | 7,951  | 7,809  | 7,591  | 7,304  | 6,955  | 112,921  |

### Valuation

| Field                         | Value         |
| ----------------------------- | ------------- |
| Sum of PV (Years 1-10)        | $76,840M      |
| PV of Terminal Value          | $112,921M     |
| Terminal Value (undiscounted) | $289,241M     |
| **Enterprise Value**          | **$189,761M** |
| RONIC                         | 3263.88%      |
| Reinvestment Rate             | 0.12%         |
| TV as % of EV                 | 59.5%         |
| Calculation Date              | 2026-03-03    |
```

### Key Observations

- **MCT = 100x** means ΔIC is negligible (~$25-37M/year). Virtually all NOPAT converts to FCF.
- **Invested capital stays negative** throughout the projection because ADBE's deferred revenue liability consistently exceeds its operating assets.
- **RONIC is extremely high** (3264%) — an artifact of negative IC. This is economically reasonable: ADBE doesn't need capital to grow.
- **TV as % of EV = 59.5%** — healthy range. If this exceeds ~80%, the near-term projections are likely too pessimistic.
- **PV of FCF is remarkably stable** across years ($7.3-7.9K range) — growth and discounting roughly offset each other.
