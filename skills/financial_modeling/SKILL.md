---
name: Financial Modeling
description: Build a multi-stage DCF (Discounted Cash Flow) model from historical financial data and qualitative outlook assumptions. Produces WACC, 10-year projections, terminal value, enterprise value, and intrinsic value per share.
---

# Financial Modeling Skill

This skill reads the company's `TICKER_metadata.md` file (Financial History + Qualitative Assessment) and constructs a complete DCF valuation model. **All calculations are pure arithmetic** — no LLM calls, no external services.

## Prerequisites

- Skills 1–4 must have been run on **at least 4 quarters** of earnings data for reliable base revenue
- The `TICKER_metadata.md` must contain:
  - **Financial History** table (Revenue, EBITA, EBITA Margin, Adj Tax Rate, NOPAT, Invested Capital, ROIC)
  - **Qualitative Assessment** section (Economic Moat, EBITA Margin Outlook, Organic Growth Outlook)

## Inputs

- `output_data/TICKER/TICKER_metadata.md` — the company-level metadata file

## Outputs

- Updated `TICKER_metadata.md` with WACC, Assumptions, DCF Model, and Intrinsic Value sections
- `output_data/TICKER/TICKER_financial_model.json` — machine-readable DCF output for the interactive viewer

## Sub-Skills

| Sub-Skill               | Folder             | Description                                                    | Depends On                    |
| ----------------------- | ------------------ | -------------------------------------------------------------- | ----------------------------- |
| **5a. WACC**            | `wacc/`            | Weighted Average Cost of Capital via CAPM                      | Financial History             |
| **5b. Assumptions**     | `assumptions/`     | Revenue growth, EBITA margins, capital turnover for 3 stages   | WACC + Qualitative Assessment |
| **5c. DCF Model**       | `dcf/`             | 10-year projection + terminal value + enterprise value         | WACC + Assumptions            |
| **5d. Intrinsic Value** | `intrinsic_value/` | Enterprise Value → Equity Value → Per-Share value              | DCF Model + Balance Sheet     |
| **5e. JSON Export**     | `json_export/`     | Write `TICKER_financial_model.json` for the interactive viewer | All above                     |

### Execution Order

1. Run **5a** (WACC) first — independent
2. Run **5b** (Assumptions) — needs WACC + Qualitative Assessment
3. Run **5c** (DCF Model) — needs WACC + Assumptions
4. Run **5d** (Intrinsic Value) — needs DCF + Balance Sheet
5. Run **5e** (JSON Export) last — needs all prior results

### Key Design Principle

The DCF model uses a **three-stage approach** that smoothly interpolates assumptions:

- **Stage 1 (Years 1–5)**: Near-term assumptions, linearly interpolating toward Stage 2
- **Stage 2 (Years 6–10)**: Mid-term assumptions, linearly interpolating toward Terminal
- **Terminal (Year 11+)**: Steady-state assumptions for perpetuity valuation

This structure allows the model to gradually transition between different growth/margin regimes rather than making abrupt jumps.

---

## Reference

Based on `calculate_dcf()` in `tiger-cafe/app/utils/financial_modeling.py` (324 lines)


---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_modeling/examples/`
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

- List every `.md` file in `skills/financial_modeling/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_modeling/examples/`.
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
