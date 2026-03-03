---
name: DCF Model
description: Project 10 years of free cash flow using three-stage interpolated assumptions, calculate terminal value, and derive enterprise value via discounted cash flow.
---

# DCF Model (Sub-Skill 5c)

## Prerequisites

- WACC calculated (Sub-Skill 5a)
- Assumptions set (Sub-Skill 5b)

## Overview

This is the core DCF engine. It takes the base year financials and assumptions, then projects 10 years of:

- Revenue → EBITA → NOPAT → Free Cash Flow → Present Value

Plus a terminal value for Year 11+.

## Step-by-Step Instructions

### Step 1: Establish Base Year (Year 0)

From the Assumptions section, read:

- `Base Revenue` (annualized)
- `Base Invested Capital` (from latest quarter balance sheet)

Also compute:

- `Base EBITA` = average of L4Q EBITA × 4 (annualized)
- `Base NOPAT` = Base EBITA × (1 - Tax Rate)
- `Base ROIC` = Base NOPAT / Base Invested Capital

### Step 2: Project Years 1–10

For each year from 1 to 10:

#### 2a. Determine Growth Rate and Margin (Linear Interpolation)

**Stage 1 (Years 1–5):**

```
growth_rate(year) = g1 + ((g2 - g1) / 5) × (year - 1)
margin(year)      = m1 + ((m2 - m1) / 5) × (year - 1)
```

**Stage 2 (Years 6–10):**

```
growth_rate(year) = g2 + ((g_terminal - g2) / 5) × (year - 6)
margin(year)      = m2 + ((m_terminal - m2) / 5) × (year - 6)
```

This creates a smooth transition: Year 1 starts at Stage 1 values, Year 5 reaches Stage 2 values, Year 10 reaches Terminal values.

#### 2b. Calculate Revenue

```
Revenue(year) = Revenue(year-1) × (1 + growth_rate)
```

#### 2c. Calculate EBITA and NOPAT

```
EBITA(year) = Revenue(year) × margin(year)
NOPAT(year) = EBITA(year) × (1 - tax_rate)
```

#### 2d. Calculate Invested Capital Change

```
ΔRevenue = Revenue(year) - Revenue(year-1)
ΔIC = ΔRevenue / Marginal Capital Turnover
IC(year) = IC(year-1) + ΔIC
```

MCT source:

- Years 1–5: `marginal_capital_turnover_stage1`
- Years 6–10: `marginal_capital_turnover_stage2`

#### 2e. Calculate Free Cash Flow

```
FCF(year) = NOPAT(year) - ΔIC
```

FCF = operating profit after tax minus what you had to reinvest to grow.

#### 2f. Calculate Present Value (Mid-Year Convention)

```
Discount Factor = 1 / (1 + WACC)^(year - 0.5)
PV_FCF(year) = FCF(year) × Discount Factor
```

The `-0.5` applies the **mid-year convention**: assumes cash flows arrive mid-year, not year-end.

#### 2g. Calculate ROIC

```
ROIC(year) = NOPAT(year) / IC(year)
```

### Step 3: Calculate Terminal Value

Terminal Value represents the present value of all cash flows beyond Year 10.

#### 3a. Terminal Year (Year 11) Financials

```
Revenue_terminal = Revenue(Year 10) × (1 + g_terminal)
EBITA_terminal   = Revenue_terminal × margin_terminal
NOPAT_terminal   = EBITA_terminal × (1 - tax_rate)
```

#### 3b. RONIC (Return on New Invested Capital)

```
RONIC = margin_terminal × (1 - tax_rate) × MCT_terminal
```

This represents the return the company earns on each incremental dollar of capital deployed.

#### 3c. Reinvestment Rate

```
Reinvestment Rate = g_terminal / RONIC
```

This tells us what fraction of NOPAT must be reinvested to sustain the terminal growth rate.

> ⚠️ If RONIC = 0, set Reinvestment Rate = 0 (no growth, 100% of NOPAT is FCF).

#### 3d. Terminal FCF

```
FCF_terminal = NOPAT_terminal × (1 - Reinvestment Rate)
```

#### 3e. Terminal Value (Gordon Growth Model)

```
Terminal Value = FCF_terminal / (WACC - g_terminal)
```

> ⚠️ If WACC ≤ g_terminal, the formula breaks (infinite value). In this case, cap g_terminal at WACC - 1%.

#### 3f. PV of Terminal Value

```
PV_Terminal = Terminal Value × Discount Factor(Year 10)

where Discount Factor = 1 / (1 + WACC)^(10 - 0.5)
```

### Step 4: Calculate Enterprise Value

```
Enterprise Value = Sum of PV_FCF(Years 1-10) + PV_Terminal_Value
```

### Step 5: Write Output to Markdown

Append to `TICKER_metadata.md`:

```markdown
---

## DCF Model

### Projections

|                  | Base   | Yr 1  | Yr 2 | Yr 3 | Yr 4 | Yr 5 | Yr 6 | Yr 7 | Yr 8 | Yr 9 | Yr 10  | Terminal |
| ---------------- | ------ | ----- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ------ | -------- |
| Revenue          | {base} | {y1}  | {y2} | ...  | ...  | ...  | ...  | ...  | ...  | ...  | {y10}  | {term}   |
| Growth           | —      | {g1}  | {g2} | ...  | ...  | ...  | ...  | ...  | ...  | ...  | {g10}  | {gt}     |
| EBITA            | {base} | {y1}  | ...  |      |      |      |      |      |      |      | {y10}  | {term}   |
| Margin           | {base} | {m1}  | ...  |      |      |      |      |      |      |      | {m10}  | {mt}     |
| NOPAT            | {base} | {y1}  | ...  |      |      |      |      |      |      |      | {y10}  | {term}   |
| Invested Capital | {base} | {y1}  | ...  |      |      |      |      |      |      |      | {y10}  | {term}   |
| ROIC             | {base} | {y1}  | ...  |      |      |      |      |      |      |      | {y10}  | {term}   |
| FCF              | —      | {y1}  | ...  |      |      |      |      |      |      |      | {y10}  | {TV}     |
| Discount Factor  | —      | {df1} | ...  |      |      |      |      |      |      |      | {df10} | {dft}    |
| PV of FCF        | —      | {pv1} | ...  |      |      |      |      |      |      |      | {pv10} | {pvt}    |

### Valuation

| Field                         | Value                    |
| ----------------------------- | ------------------------ |
| Sum of PV (Years 1-10)        | {sum_pv_fcf}             |
| PV of Terminal Value          | {pv_terminal}            |
| Terminal Value (undiscounted) | {terminal_value}         |
| **Enterprise Value**          | **{enterprise_value}**   |
| RONIC                         | {ronic_pct}%             |
| Reinvestment Rate             | {reinvestment_rate_pct}% |
| Calculation Date              | {current_date_iso}       |
```

---

## Important Notes

- **Mid-year convention** is critical. Without it, the model systematically undervalues by assuming all cash arrives at year-end.
- **Linear interpolation** between stages ensures there are no abrupt jumps in the model. This is more realistic than step-function assumptions.
- The Terminal Value typically represents **60-80%** of total Enterprise Value. If it's >90%, the near-term projections may be too pessimistic, or the terminal growth rate is too high.
- **RONIC** (Return on New Invested Capital) is a key sanity check. If RONIC < WACC, the company destroys value by growing — which means higher growth actually _decreases_ the stock's value.
- All monetary values should be in the company's **local currency** and **prevailing unit** (e.g., RMB millions).

## Reference

Based on `calculate_dcf()` in `tiger-cafe/app/utils/financial_modeling.py`
