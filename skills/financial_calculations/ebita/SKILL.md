---
name: EBITA Calculation
description: Calculate EBITA (Earnings Before Interest, Tax, and Amortization) from income statement and GAAP reconciliation data.
---

# EBITA Calculation (Sub-Skill 3a)

## Prerequisites

- Income Statement extracted (Skill 2b)
- GAAP Reconciliation extracted if available (Skill 2e)

## What is EBITA?

EBITA = Operating Income + Non-GAAP Adjustments (non-operating only)

It represents the company's **operating profit before interest, taxes, and acquisition-related amortization** — a cleaner view of operational performance.

## Step-by-Step Instructions

### Step 1: Read Extracted Data

From the document's `.md` file, read:
1. **Income Statement** line items (with standardized names, operating flags, and values)
2. **GAAP Reconciliation** items (if available)

### Step 2: Find the Starting Point (Operating Income)

1. Look for a line item with `standardized_name` = `operating_income` in the Income Statement
2. **Fallback**: If not found, use `income_before_taxes` instead (flag as fallback)
3. Record the starting value and its position (line order) in the table

### Step 3: Add Non-GAAP Adjustments

If GAAP Reconciliation data is available, **iterate over EVERY adjustment item** and process it:

**Include only if ALL of these are true:**
- `Operating` = No (non-operating adjustments only)
- NOT a Total/Subtotal line (i.e., `line_category` ≠ "Total")
- Has a non-zero value

For each qualifying item, add its value to the running EBITA total. **Also record it in an Adjustments list** for the output table.

> ⚠️ **DO NOT cherry-pick adjustments by name.** You must iterate over ALL items in the GAAP Reconciliation and apply the filter above. Common non-operating adjustments include (but are NOT limited to):
>
> | Adjustment Type | Typical Names | Operating? |
> |---|---|---|
> | Amortization of acquired intangibles | "Amortization and impairment of intangible assets" | No |
> | **Impairment of long-lived assets** | "Impairment of long-lived assets", "Goodwill impairment" | **No** |
> | Restructuring charges | "Restructuring and severance" | No |
> | Gain/loss on disposal | "Gain on divestiture" | No |
> | Stock-based compensation | "Share-based compensation expenses" | **Yes** (stays in EBITA) |
>
> **Impairment is NON-OPERATING and MUST be added back.** This is a common source of error — impairment charges can be very large (e.g., billions) and missing them will make EBITA wildly wrong.

### Step 3b: Cross-Check Against Non-GAAP Operating Income

The GAAP Reconciliation typically ends with a **Non-GAAP Operating Income** total. Use this to validate:

```
Expected: EBITA ≈ Non-GAAP Operating Income - SBC addback
(Because EBITA adds back non-operating items but keeps SBC, while Non-GAAP adds back everything)
```

If your computed EBITA is dramatically different from `Non-GAAP OpInc - SBC`, you likely missed an adjustment. Go back and re-check.

### Step 4: Add Income Statement Non-Operating Items

Also scan the Income Statement for items that appear BEFORE the Operating Income line:
- Must have `Operating` = No
- Must NOT be a calculated total
- Must NOT already be captured in Step 3 (avoid double-counting — check by name AND absolute value)

For these items, **negate the sign** and add to EBITA:
- If the IS shows `-100` for an expense, the add-back is `+100`

### Step 5: Calculate EBITA Margin

```
EBITA Margin = EBITA / Revenue
```

Express as a decimal (e.g., 0.4765 for 47.65%).

### Step 6: Write Output to Markdown

Append to the document's `.md` file:

```markdown
---

## EBITA

| Field | Value |
|-------|-------|
| Starting Point | Operating Income |
| Starting Value | {operating_income} |
| EBITA | {ebita} |
| EBITA Margin | {ebita_margin_pct}% |
| Calculation Date | {current_date_iso} |

### Adjustments

| # | Line Name | Value | Source |
|---|-----------|-------|--------|
| 1 | Stock-based compensation | 469 | GAAP Reconciliation |
| 2 | Amortization of intangibles | 83 | GAAP Reconciliation |
| ... | ... | ... | ... |
```

---

## Important Notes

- The sign convention matters: GAAP Reconciliation values are addbacks (positive = add to operating income). Income Statement non-operating expenses are negative, so we negate them to add back.
- If using Income Before Taxes as fallback, note this in the output — EBITA accuracy is lower.
- Only non-operating items are adjustments. Operating items (like SBC classified as operating) stay in EBITA.
- **NEVER hardcode which adjustments to include by name.** Always iterate over all GAAP recon items and filter by the `operating` flag. New adjustment types (e.g., impairment, restructuring) will appear in different quarters and must be picked up automatically.
- The Adjustments table in the output is MANDATORY — it provides an audit trail showing exactly which items were added back and allows the user to verify correctness.

## Reference

Based on `calculate_ebita()` in `tiger-cafe/app/utils/historical_calculations.py`


---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_calculations/ebita/examples/`
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

- List every `.md` file in `skills/financial_calculations/ebita/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_calculations/ebita/examples/`.
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
