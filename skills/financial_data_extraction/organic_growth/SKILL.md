---
name: Organic Growth Extraction
description: Extract organic/constant-currency growth percentage and prior-year revenue from a financial PDF.
---

# Organic Growth Extraction (Sub-Skill 2d)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- **Income Statement must be extracted first** (Sub-Skill 2b) — needs current revenue
- No external services required (LLM-only)
- If a static file server is not running on localhost:8181 then ask the user to run `.\tools\start_file_server.bat`

**DO NOT EVER start servers without human user.**

## Step-by-Step Instructions

### Step 1: Read Inputs

1. Read the classification `.md` file to get: `time_period`, `period_end_date`
2. Read the Income Statement section from the `.md` file to get:
   - Current period revenue value
   - Revenue line item name (e.g., "Total revenue", "Net revenues")
   - Currency and unit
3. Open the PDF in the browser using the `browser_subagent` tool:
   - Navigate to `http://localhost:8181/processing_data/{filename}`
   - Search for organic growth / constant-currency growth mentions (often in the first few pages or management discussion)
4. Do NOT use PyPDF2 or other text extraction libraries

### Step 2: Extract Organic Growth Percentage

Search the document for an explicitly stated **organic growth** or **constant-currency growth** percentage.

**What to look for:**

- "organic growth" / "organic revenue growth"
- "constant currency growth" / "constant currency revenue growth"
- "currency-neutral growth"

**Rules:**

- Extract the RAW percentage as a float (e.g., 5.5 for 5.5%, -2.3 for -2.3%)
- Only extract if EXPLICITLY labeled as organic or constant-currency growth
- Do NOT extract simple reported revenue growth in this step
- If not found, set to null — Step 3 will provide the fallback

### Step 3: Extract Prior-Year Revenue (MANDATORY)

Extract the **prior year's revenue** from the comparative column in the income statement. This step is **always required**, regardless of whether organic growth was found in Step 2.

**How to find it:**

1. Look at the income statement in the PDF — it always has at least two columns
2. Identify the prior period column:
   - If current period is Q4 2024 (ends 2024-12-31), prior is Q4 2023 (ends 2023-12-31)
   - The prior period column is usually the column to the RIGHT of the current period
3. Extract the revenue value from the SAME ROW as the current period revenue

**Validation (Reflection):**

- Ensure the prior revenue is from the correct duration (quarterly vs. annual)
  - If current period is Q1, prior should also be a single quarter (not full year)
  - The prior revenue should be in a similar magnitude to current revenue (within 50%)
- If the extracted value seems wrong (e.g., 4x the current revenue), it may be from a full-year column instead of quarterly

### Step 4: Calculate Simple Growth (MANDATORY)

This is the **mandatory fallback** — calculate it regardless of whether organic growth was found.

```
simple_growth = (current_revenue - prior_revenue) / prior_revenue × 100
```

> ⚠️ **VALIDATION: Simple growth MUST produce a real number, not N/A or 0.0%.**
>
> If the result is exactly 0.0%, double-check that:
>
> - Current revenue and prior revenue are different values
> - You are comparing the same time period (Q vs Q, not Q vs FY)
> - You haven't accidentally used the same column for both periods
>
> A 0.0% growth rate is statistically implausible and almost certainly an extraction error.

### Step 5: Determine Final Growth Value

Use this priority order for the growth value written to the output:

1. **Organic Growth** (from Step 2) — if explicitly found in the document
2. **Simple YoY Revenue Growth** (from Step 4) — mandatory fallback

If organic growth was found, also cross-validate:

- Organic growth should be within a reasonable range of simple growth (usually ±5 percentage points)
- If the difference is >10 percentage points, flag for user review

### Step 6: Write Output to Markdown

Append the following section to the document's `.md` file:

```markdown
---

## Organic Growth

| Field                   | Value                                             |
| ----------------------- | ------------------------------------------------- |
| Current Revenue         | {current_revenue}                                 |
| Current Revenue Unit    | {unit}                                            |
| Prior Year Revenue      | {prior_revenue}                                   |
| Prior Year Revenue Unit | {unit}                                            |
| Simple Growth (%)       | {simple_growth}                                   |
| Organic Growth (%)      | {organic_growth or "Not reported"}                |
| **Final Growth (%)**    | **{organic_growth if found, else simple_growth}** |
| Growth Source           | {"Reported organic" or "Calculated simple YoY"}   |
| Extraction Date         | {current_date_iso}                                |
```

---

## Error Handling

- If income statement not yet extracted → Inform user to run Sub-Skill 2b first
- If prior year revenue column not found in the PDF → **Re-read the income statement more carefully.** All earnings announcements and financial filings include a prior-year comparative column. Do NOT give up.
- If organic growth not found → Use simple growth as the final value (this is normal for many companies)
- **NEVER output N/A for the Final Growth field** — simple YoY growth is always calculable from the IS comparative columns

## Reference

Based on `tiger-cafe\app\app_agents\organic_growth_extractor.py`

---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_data_extraction/organic_growth/examples/`
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

- List every `.md` file in `skills/financial_data_extraction/organic_growth/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_data_extraction/organic_growth/examples/`.
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
