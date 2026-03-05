---
name: Shares Outstanding Extraction
description: Extract basic and diluted shares outstanding from a financial PDF.
---

# Shares Outstanding Extraction (Sub-Skill 2c)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- No external services required (LLM-only extraction)
- If a static file server is not running on localhost:8181 then ask the user to run `.\tools\start_file_server.bat`

**DO NOT EVER start servers without human user.**

## Step-by-Step Instructions

### Step 1: Read the PDF and Classification Metadata

1. Read the classification `.md` file to get: `time_period`, `period_end_date`
2. Open the PDF in the browser using the `browser_subagent` tool:
   - Navigate to `http://localhost:8181/processing_data/{filename}`
   - Navigate to the page(s) containing share count data (usually the income statement or EPS section)
3. Do NOT use PyPDF2 or other text extraction libraries

### Step 2: Find Share Count Data

Look for basic and diluted shares outstanding. These may NOT be explicitly labeled — search for:

- "Shares used to calculate basic EPS" / "basic EPS shares"
- "Shares used to calculate diluted EPS" / "diluted EPS shares"
- "Weighted average basic shares" / "weighted average diluted shares"
- "Basic weighted average shares" / "diluted weighted average shares"
- Any table or section showing share counts used for EPS calculations
- The bottom rows of the income statement (often appear after Net Income)
- Footnotes or supplemental data sections

### Step 3: Extract Values

Extract for the **current period** (matching `time_period` or `period_end_date`):

| Field                             | Description                                         |
| --------------------------------- | --------------------------------------------------- |
| `basic_shares_outstanding`        | Number of basic shares                              |
| `basic_shares_outstanding_unit`   | One of: `ones`, `thousands`, `millions`, `billions` |
| `diluted_shares_outstanding`      | Number of diluted shares                            |
| `diluted_shares_outstanding_unit` | One of: `ones`, `thousands`, `millions`, `billions` |

**Rules:**

- Extract ONLY if explicitly shown in the document
- Do NOT calculate (e.g., do not divide net income by EPS to derive shares)
- The unit may differ from the income statement unit — check carefully
- If only one type is found, set the other to null

### Step 4: Validate

- `diluted_shares_outstanding` should be ≥ `basic_shares_outstanding` (diluted includes stock options)
- If diluted < basic, flag for user review
- Values should be in a reasonable range (usually millions for large-cap companies)

### Step 5: Write Output to Markdown

Append the following section to the document's `.md` file:

```markdown
---

## Shares Outstanding

| Field                      | Value              |
| -------------------------- | ------------------ |
| Basic Shares Outstanding   | {value}            |
| Basic Unit                 | {unit}             |
| Diluted Shares Outstanding | {value}            |
| Diluted Unit               | {unit}             |
| Extraction Date            | {current_date_iso} |
```

---

## Error Handling

- If share data not found → Set to null, note reason in markdown
- If only one type found → Extract what's available, set other to null

## Reference

Based on `tiger-cafe\app\app_agents\shares_outstanding_extractor.py`

---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_data_extraction/shares_outstanding/examples/`
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

- List every `.md` file in `skills/financial_data_extraction/shares_outstanding/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_data_extraction/shares_outstanding/examples/`.
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
