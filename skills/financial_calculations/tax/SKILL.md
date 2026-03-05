---
name: Tax Rate Calculation
description: Calculate effective tax rate and adjusted (operating) tax rate from income statement and EBITA data.
---

# Tax Rate Calculation (Sub-Skill 3b)

## Prerequisites

- Income Statement extracted (Skill 2b)
- EBITA calculated (Skill 3a)
- GAAP Reconciliation extracted if available (Skill 2e)

## Step-by-Step Instructions

### Step 1: Read Extracted Data

From the document's `.md` file, read:
1. **Income Statement**: `income_before_taxes`, `income_tax_provision`, `net_income` (by standardized name)
2. **EBITA** result from Sub-Skill 3a
3. **GAAP Reconciliation** items (if available)

### Step 2: Calculate Effective Tax Rate

The simple tax rate based on reported figures:

**Primary formula:**
```
Effective Tax Rate = -(Income Tax Expense / Income Before Taxes)
```

The negation is because tax expense is stored as negative (sign-normalized in Skill 2b).
- Example: `-371 / 2,182 = -0.1700`, negated = `0.1700` (17.00%)

**Fallback** (if tax expense is missing):
```
Effective Tax Rate = (Income Before Taxes - Net Income) / Income Before Taxes
```
- Example: `(2,182 - 1,811) / 2,182 = 0.1700` (17.00%)

### Step 3: Calculate Adjusted (Operating) Tax Rate

The adjusted tax rate accounts for the tax effect of non-operating items that were added back or removed to get EBITA.

**Formula:**
```
Adjusted Tax = Reported Tax + Tax Effect of Adjustments
Adjusted Tax Rate = -(Adjusted Tax / EBITA)
```

**How to calculate Tax Effect:**

For each non-operating adjustment (from GAAP Reconciliation and Income Statement):

1. **Marginal Tax Rate**: Use **25%** as the default
2. **Exception**: Use **0%** for items containing: "impairment", "amortization", or "equity" (these are typically non-deductible)

**For Income Statement intermediate items** (non-operating items between Operating Income and Tax Expense):
```
Tax Effect = -(line_value) × marginal_rate
```
(Negate because IS items are sign-normalized)

**For GAAP Reconciliation addback items** (non-operating):
```
Tax Effect = line_value × marginal_rate
```
(Direct because these are already positive addbacks)

### Step 4: Validate Tax Rates

> ⚠️ **A tax rate of 0% is NEVER acceptable.** If you calculate 0%, something is wrong.

**Hard validation rules:**

| Condition | Action |
|-----------|--------|
| Tax rate = 0% | **ERROR** — Re-check: Is `income_tax_provision` missing from the IS? Did you read all lines between Operating Income and Net Income? |
| Tax rate < 0% | **FLAG** — Report the actual negative rate. This happens in loss quarters with tax benefits. It is real data — do NOT override it. |
| Tax rate > 50% | **WARNING** — Appears unusually high. Flag but proceed. |
| Effective tax rate < 5% | **WARNING** — Appears unusually low. Cross-check with Net Income derivation. |
| Adjusted tax rate between 10-35% | ✅ Normal range for most companies |

**Always compute the actual rate first.** The formula works regardless of whether Income Before Taxes is positive or negative:

```
Effective Tax Rate = -(Income Tax Expense / Income Before Taxes)
```

- Profitable quarter: Pre-tax = +6,577, Tax = -1,619 → Rate = 24.6% ✅
- Loss quarter with tax benefit: Pre-tax = -13,145, Tax = +1,828 → Rate = -(-1,828 / -13,145) = 13.9% ✅
- Loss quarter with tax expense: Pre-tax = -500, Tax = -50 → Rate = -(- 50 / -500) = -10% (negative rate — flag but report)

**Fallback hierarchy** (only if the primary formula produces 0% or cannot execute):

1. **Primary**: `-(Income Tax Expense / Income Before Taxes)` — always try this first
2. **Secondary**: `(Income Before Taxes - Net Income) / Income Before Taxes`
3. **Last resort**: If Income Before Taxes = 0 (division by zero), or both tax and pre-tax are missing, use the **statutory corporate tax rate** for the company's domicile:
   - US companies: **21%**
   - Chinese companies (e.g., BIDU): **25%**
   - European companies: varies, use **20%** as default
   - If unsure, use **21%** as a global default
   - Note in output: "Using statutory rate — division by zero"

**The statutory rate is a LAST RESORT, not a default for loss quarters.** Loss quarters have real tax data that should be reported as-is.

### Step 5: Write Output to Markdown

Append to the document's `.md` file:

```markdown
---

## Tax Rates

| Field | Value |
|-------|-------|
| Income Before Taxes | {income_before_taxes} |
| Income Tax Expense | {income_tax_expense} |
| Net Income | {net_income} |
| Effective Tax Rate | {effective_tax_rate_pct}% |
| Adjusted Tax Rate | {adjusted_tax_rate_pct}% |
| Calculation Date | {current_date_iso} |

### Adjusted Tax Rate Breakdown

| # | Line Name | Value | Tax Effect | Source | Marginal Rate |
|---|-----------|-------|------------|--------|---------------|
| 1 | Interest expense | -62 | 15.50 | Intermediate | 25% |
| 2 | Amortization of intangibles | 83 | 0.00 | Non-GAAP | 0% |
| ... | ... | ... | ... | ... | ... |
| | **Reported Tax** | **-371** | | | |
| | **Total Tax Adjustment** | | **{total}** | | |
| | **Adjusted Tax** | **{adjusted_tax}** | | | |
```

---

## Reference

Based on `calculate_effective_tax_rate_from_inputs()` and `calculate_adjusted_tax_rate()` in `tiger-cafe/app/utils/historical_calculations.py`


---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_calculations/tax/examples/`
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

- List every `.md` file in `skills/financial_calculations/tax/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_calculations/tax/examples/`.
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
