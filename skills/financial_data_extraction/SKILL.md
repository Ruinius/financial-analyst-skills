---
name: Financial Data Extraction
description: Extract structured financial data from classified PDFs. Contains 5 sub-skills for balance sheet, income statement, shares outstanding, organic growth, and GAAP reconciliation.
---

# Financial Data Extraction Skill

This skill reads a classified PDF from `processing_data/` and extracts structured financial data, appending results to the document's markdown file.

## Prerequisites

- Skill 1 (Document Classification) must have been run first
- If Tiger-Transformer is not running on localhost:8000 then ask the user to run `.\tools\start_transformer.bat`
- If a static file server is not running on localhost:8181 then ask the user to run `.\tools\start_file_server.bat`

**DO NOT EVER start servers without human user.**

## Inputs

- A classified PDF and its corresponding `.md` file in `processing_data/`
  - Example: `ADBE_EA_20250312_temp.pdf` + `ADBE_EA_20250312_temp.md`

## Outputs

- Updated markdown file with extracted financial data appended as new sections

## Sub-Skills

This skill contains 5 sub-skills that should be run in order:

| Sub-Skill                   | Folder                 | Description                                                     | Depends On       |
| --------------------------- | ---------------------- | --------------------------------------------------------------- | ---------------- |
| **2a. Balance Sheet**       | `balance_sheet/`       | Extract balance sheet line items, standardize via transformer   | Classification   |
| **2b. Income Statement**    | `income_statement/`    | Extract income statement, standardize, normalize signs          | Classification   |
| **2c. Shares Outstanding**  | `shares_outstanding/`  | Extract basic and diluted share counts                          | Classification   |
| **2d. Organic Growth**      | `organic_growth/`      | Extract organic/constant-currency growth and prior-year revenue | Income Statement |
| **2e. GAAP Reconciliation** | `gaap_reconciliation/` | Extract GAAP-to-non-GAAP operating income reconciliation        | Classification   |

### Execution Order

1. Read the classification metadata from the `.md` file (ticker, document_type, time_period, period_end_date)
2. Open the PDF in the browser using the `browser_subagent` tool (navigate to `http://localhost:8181/processing_data/{filename}`)
3. Navigate to the relevant pages for each sub-skill (e.g., balance sheet, income statement). You do NOT need to read every page — use page navigation to jump to the sections you need.
4. Run **2c** (can run in parallel with 2a/2b)
5. Run **2d** after **2b** (needs income statement revenue data)
6. Run **2e**

### Output Format

Each sub-skill appends a section to the markdown file. See individual sub-skill SKILL.md files for exact output formats.

### Currency and Unit Policy

- **Currency**: Always extract in the **document's local (functional) currency** — do NOT use USD convenience translations.
- **ADR handling**: Foreign companies listed in the US (ADRs) often present financial statements in both their local currency AND a USD translation side by side. **Always use the local currency column** (e.g., RMB for BABA, TWD for TSM, EUR for SAP). The USD column is a convenience translation and should be ignored.
- **How to identify local vs USD**: The local currency column is typically labeled as the primary/functional currency, appears first, or is in the document's stated reporting currency. Look for headers like "RMB", "¥", "€", or the company's domicile currency.
- **Unit**: Extract the unit exactly as stated in the document (e.g., "In millions", "百万円", "In thousands"). Each section records its own unit.
- **Unit harmonization** happens later in Skill 4 (Document Organization), not during extraction.

---

## Reference

Based on the following tiger-cafe source files:

- `app/app_agents/balance_sheet_extractor.py` (869 lines)
- `app/app_agents/income_statement_extractor.py` (830 lines)
- `app/app_agents/shares_outstanding_extractor.py` (277 lines)
- `app/app_agents/organic_growth_extractor.py` (510 lines)
- `app/app_agents/gaap_reconciliation_extractor.py` (778 lines)
- `app/app_agents/extractor_utils.py` (193 lines)

---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_data_extraction/examples/`
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

- List every `.md` file in `skills/financial_data_extraction/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_data_extraction/examples/`.
- The surviving example should serve as the **gold-standard reference** for anyone reading this skill.

> ⚠️ **Rules for example curation:**
>
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
>
> - NEVER delete or weaken existing validation rules — only add or strengthen them
> - Keep changes surgical and focused — do not rewrite sections that are working fine
> - If unsure whether a change is correct, add it as a `> ⚠️ NOTE:` rather than modifying instructions
> - Each changelog entry must include the date and a one-line description

### Changelog

| Date | Change           |
| ---- | ---------------- |
| —    | (no changes yet) |
