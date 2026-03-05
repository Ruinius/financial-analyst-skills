---
name: WACC Calculation
description: Calculate Weighted Average Cost of Capital using CAPM for equity cost and market data for debt cost. WACC is the discount rate used in the DCF model.
---

# WACC Calculation (Sub-Skill 5a)

## Prerequisites

- Financial History in `TICKER_metadata.md` (need latest Revenue, Invested Capital)
- Company ticker validated (for market data lookup)

## What is WACC?

WACC = Weighted Average Cost of Capital — the blended rate of return required by all capital providers (equity + debt).

```
WACC = (E/V × Cost of Equity) + (D/V × Cost of Debt × (1 - Tax Rate))
```

Where:

- `E` = Market cap (equity value)
- `D` = Total debt (from balance sheet)
- `V` = E + D (total enterprise value)
- Cost of Equity = CAPM result
- Cost of Debt = Interest Expense / Total Debt

## Step-by-Step Instructions

### Step 1: Gather Market Data

Run `tools/market_data.py profile TICKER` to retrieve all market data in a single call:

1. **Market Cap** (equity value E) — in USD for US-listed tickers
2. **Raw Levered Beta** — `beta` field in the response
3. **Current Share Price** — `share_price` field
4. **Currency** — `currency` field (for FX conversion later)

If debt is in a foreign currency, also run `tools/market_data.py fx FROM_CURRENCY USD` to get the exchange rate.

If market data is unavailable, use these defaults:

- Raw Beta: **1.0** (market average)
- Market Cap: estimate from shares outstanding × recent price if known

### Step 2: Gather Balance Sheet Data

From the most recent earnings document in `output_data/TICKER/`, read:

1. **Total Debt** = Sum of all debt-classified items on the Balance Sheet:
   - `short_term_debt` + `current_portion_long_term_debt` + `current_portion_convertible_debt` + `long_term_debt` + `convertible_debt`
2. **Interest Expense** (from Income Statement, annualized if quarterly)
3. **Adjusted Tax Rate** (from Financial Summary)

### Step 3: Unlever Beta and Apply Blume's Adjustment

The raw beta from Yahoo Finance is a **levered beta** — it reflects the company's current capital structure. Since our WACC formula already accounts for leverage through the debt/equity weights, we need to **unlever** the beta first to avoid double-counting leverage risk.

#### 3a. Unlever Beta (Hamada Equation)

```
β_unlevered = β_levered / (1 + (1 - t) × (D / E))
```

Where:

- `β_levered` = raw beta from Yahoo Finance
- `t` = statutory tax rate (**25%** as default)
- `D` = Total Debt (from Balance Sheet, converted to USD if needed)
- `E` = Market Cap (equity value from Yahoo Finance)

> ⚠️ D and E must be in the **same currency**. If debt is in local currency (e.g., RMB), convert to USD using `tools/market_data.py fx RMB USD` before computing D/E.

#### 3b. Apply Blume's Adjustment

Blume's adjustment shrinks extreme betas toward 1.0, reflecting the empirical observation that betas mean-revert over time:

```
β_adjusted = (2/3) × β_unlevered + (1/3) × 1.0
```

This is the final beta used in CAPM.

#### 3c. Example (BIDU)

```
Raw Levered Beta   = 1.15 (from Yahoo Finance)
Total Debt          = RMB 97,248M → ~$13,414M USD (at 7.25 rate)
Market Cap          = $30,000M USD
D/E                 = 13,414 / 30,000 = 0.447
Statutory Tax Rate  = 25%

β_unlevered = 1.15 / (1 + 0.75 × 0.447)
            = 1.15 / 1.335
            = 0.861

β_adjusted  = (2/3) × 0.861 + (1/3) × 1.0
            = 0.574 + 0.333
            = 0.907
```

### Step 4: Calculate Cost of Equity (CAPM)

```
Cost of Equity = Risk-Free Rate + β_adjusted × Equity Risk Premium
```

**Default Parameters:**

| Parameter           | Default Value | Source                            |
| ------------------- | ------------- | --------------------------------- |
| Risk-Free Rate      | 4.20%         | US 10-Year Treasury (approximate) |
| Equity Risk Premium | 5.00%         | Market risk premium               |

**Country Risk Premium adjustments:**

| Domicile           | Additional Premium |
| ------------------ | ------------------ |
| US                 | 0.0%               |
| China              | 1.0%               |
| Emerging Markets   | 1.5%               |
| Europe (developed) | 0.5%               |

```
Example (BIDU):
  Cost of Equity = 4.20% + 0.907 × (5.00% + 1.0%)
                 = 4.20% + 5.44%
                 = 9.64%
```

### Step 5: Calculate Cost of Debt

```
Cost of Debt = |Interest Expense (annualized)| / Total Debt
```

- If Total Debt = 0 or Interest Expense = 0, use **5.0%** as default (floor)
- Minimum Cost of Debt: **5.0%**
- If Cost of Debt exceeds 15%, cap at 15% (likely data error)

### Step 6: Calculate Capital Weights

```
E = Market Cap (USD)
D = Total Debt (converted to USD if needed)
V = E + D

Weight of Equity = E / V
Weight of Debt   = D / V
```

### Step 7: Calculate WACC

```
WACC = (E/V × Cost of Equity) + (D/V × Cost of Debt × (1 - Tax Rate))
```

Use the **statutory marginal tax rate** (25%) for the tax shield on debt.

**Bounding:** Clamp the final WACC to the **7–11%** range for use as the default in the DCF model. The user may override this.

**Reasonableness check:**

- WACC should typically be between 7% and 11%
- WACC < 7%: ⚠️ Unusually low — verify inputs
- WACC > 11%: ⚠️ Very risky company — verify beta and debt levels

### Step 8: Write Output to Markdown

Append to the `TICKER_metadata.md` file:

```markdown
---

## WACC

| Field                   | Value                  |
| ----------------------- | ---------------------- |
| Risk-Free Rate          | {rfr_pct}%             |
| Equity Risk Premium     | {erp_pct}%             |
| Country Risk Premium    | {crp_pct}%             |
| Raw Levered Beta        | {raw_beta}             |
| Unlevered Beta          | {unlevered_beta}       |
| Adjusted Beta (Blume's) | {adjusted_beta}        |
| Cost of Equity          | {coe_pct}%             |
| Total Debt              | {total_debt}           |
| Interest Expense (Ann.) | {interest_expense_ann} |
| Cost of Debt            | {cod_pct}%             |
| Market Cap              | {market_cap}           |
| Weight of Equity        | {we_pct}%              |
| Weight of Debt          | {wd_pct}%              |
| Tax Rate                | {tax_rate_pct}%        |
| **WACC**                | **{wacc_pct}%**        |
| Calculation Date        | {current_date_iso}     |
```

---

## Important Notes

- WACC is a **single number** that feeds into the DCF model as the discount rate. Getting it wrong by even 1 percentage point materially changes the valuation.
- For Chinese companies (like BIDU), the additional Country Risk Premium is important because of regulatory and geopolitical risk.
- **Beta must be unlevered before use.** The raw beta from Yahoo Finance reflects the company's current leverage. Since the WACC formula already weights equity and debt costs by their capital structure proportions, using a levered beta would double-count leverage risk.
- **Blume's Adjustment** is applied _after_ unlevering to account for the empirical mean-reversion of betas.
- If `yfinance` is not available, the user should provide raw beta and market cap manually.

## Reference

Based on CAPM, Hamada equation, and Blume's beta adjustment methodology. Reference implementation in `tiger-cafe/app/services/company_service.py`.


---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_modeling/wacc/examples/`
> (Relative to this SKILL.md: `./examples/`)

After completing this skill, you MUST perform the following example curation step:

### 1. Save the Current Run as a New Example

- Copy the **output produced by this skill run** into the examples folder as a new `.md` file.
- Naming convention: `TICKER_example.md` (e.g., `AAPL_example.md`, `MSFT_example.md`).
- The example file should contain:
  - The **complete output** this skill produced (all tables, sections, and values)
  - A brief header noting the source (ticker, document date, period)
  - The **calculation walkthrough** if this is a calculation skill — show intermediate values so a reader can follow the logic

### 2. Review All Examples

- List every `.md` file in `skills/financial_modeling/wacc/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_modeling/wacc/examples/`.
- The surviving example should serve as the **gold-standard reference** for anyone reading this skill.

> ⚠️ **Rules for example curation:**
> - There must be **exactly 1 example file** in the folder after curation
> - NEVER keep a partial or broken example over a complete one
> - If the new run's output is worse than the existing example, keep the old one and delete the new one
> - If no existing example has all required fields, the new run's output wins by default
> - The surviving file must be renamed to `TICKER_example.md` format if not already

---

## Self-Improvement

After completing this skill, you MUST perform the following self-improvement step:

1. **Reflect on the run.** Review what happened during this execution:
   - Did any step fail or require retry?
   - Were there ambiguities in the instructions that caused hesitation or errors?
   - Did you discover an edge case not covered by the current instructions?
   - Was any output wrong, incomplete, or required manual correction?

2. **Propose and apply improvements.** If you identified any issue, update THIS `SKILL.md` file directly. Improvements can include:
   - Adding new edge case handling or fallback logic
   - Clarifying ambiguous wording in existing steps
   - Adding validation checks that would have caught an error earlier
   - Updating examples to cover newly discovered patterns
   - Removing or correcting outdated instructions

3. **Log the change.** Append a brief entry to the changelog below so the improvement history is tracked.

> ⚠️ **Rules for self-edits:**
> - NEVER delete or weaken existing validation rules — only add or strengthen them
> - Keep changes surgical and focused — do not rewrite sections that are working fine
> - If unsure whether a change is correct, add it as a `> ⚠️ NOTE:` rather than modifying instructions
> - Each changelog entry must include the date and a one-line description

### Changelog

| Date | Change |
|------|--------|
| — | (no changes yet) |
