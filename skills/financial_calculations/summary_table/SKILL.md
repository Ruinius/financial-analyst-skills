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


---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_calculations/summary_table/examples/`
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

- List every `.md` file in `skills/financial_calculations/summary_table/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_calculations/summary_table/examples/`.
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
