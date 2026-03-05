---
name: Financial Calculations
description: Compute derived financial metrics (EBITA, tax rates, invested capital, ROIC) from previously extracted data. All calculations are pure math — no LLM calls needed.
---

# Financial Calculations Skill

This skill reads the extracted financial data from the document's `.md` file and computes derived metrics. **All calculations are pure arithmetic** — no LLM calls, no external services.

## Prerequisites

- Skill 2 (Financial Data Extraction) must have been run first
- The document's `.md` file must contain: Balance Sheet, Income Statement, and optionally GAAP Reconciliation sections

## Inputs

- The document's `.md` file in `processing_data/` with extracted financial data
- Key fields needed from the extracted data:
  - **Balance Sheet**: Line items with `Category`, `Operating` flags, `Calculated` flags
  - **Income Statement**: Line items with `Standardized Name`, `Operating` flags, `Expense` flags, sign-normalized values
  - **GAAP Reconciliation** (if available): Adjustment items with `Operating` classification

## Sub-Skills

| Sub-Skill | Folder | Description | Depends On |
|-----------|--------|-------------|------------|
| **3a. EBITA** | `ebita/` | Earnings Before Interest, Tax, and Amortization | Income Statement + GAAP Reconciliation |
| **3b. Tax Rates** | `tax/` | Effective and adjusted (operating) tax rates | Income Statement + EBITA |
| **3c. Invested Capital** | `invested_capital/` | Net Working Capital + Net Long-Term Operating Assets | Balance Sheet |
| **3d. Summary Table** | `summary_table/` | Final summary with NOPAT, ROIC, and all metrics | All above |

### Execution Order

1. Run **3a** (EBITA) and **3c** (Invested Capital) — independent of each other
2. Run **3b** (Tax Rates) after 3a — needs EBITA
3. Run **3d** (Summary Table) last — needs all prior results

### Key Design Principle

These calculations rely entirely on the `is_operating`, `is_calculated`, and `is_expense` flags set by the Tiger-Transformer in Skill 2. No fuzzy matching or LLM calls needed — the transformer already did the hard work of classifying each line item.

---

## Reference

Based on `tiger-cafe/app/utils/historical_calculations.py` (802 lines)


---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_calculations/examples/`
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

- List every `.md` file in `skills/financial_calculations/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_calculations/examples/`.
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
