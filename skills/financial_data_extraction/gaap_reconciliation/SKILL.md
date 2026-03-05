---
name: GAAP Reconciliation Extraction
description: Extract GAAP-to-non-GAAP operating income or EBITDA reconciliation tables from earnings announcements.
---

# GAAP Reconciliation Extraction (Sub-Skill 2e)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- **Only runs for `earnings_announcement` document types** — skip for 10-Q, 10-K, etc.
- No external services required (LLM-only)
- If a static file server is not running on localhost:8181 then ask the user to run `.\tools\start_file_server.bat`

**DO NOT EVER start servers without human user.**

## Step-by-Step Instructions

### Step 1: Check Document Type

1. Read the classification `.md` file to get: `document_type`, `time_period`, `period_end_date`
2. **If `document_type` is NOT `earnings_announcement`**, skip this sub-skill entirely
   - GAAP reconciliation tables are typically only found in earnings press releases

### Step 2: Read the PDF

Open the PDF in the browser using the `browser_subagent` tool:

- Navigate to `http://localhost:8181/processing_data/{filename}`
- Navigate to the latter pages of the earnings press release where reconciliation tables are typically found
- Do NOT use PyPDF2 or other text extraction libraries

### Step 3: Locate the Reconciliation Table

Find the **GAAP to non-GAAP operating income** or **EBITDA reconciliation** table.

**What to look for:**

- Tables titled "Reconciliation of GAAP to Non-GAAP" or similar
- Tables showing adjustments from GAAP operating income to adjusted/non-GAAP operating income or EBITDA
- Usually found in the latter pages of earnings press releases

**What to AVOID:**

- Net income reconciliation tables (wrong table)
- Margin reconciliation tables
- EPS reconciliation tables
- Segment-level reconciliations (need consolidated)

### Step 4: Extract Line Items

Extract all line items from the reconciliation table for the current period:

**Output JSON structure:**

```json
{
  "line_items": [
    {
      "line_name": "GAAP operating income",
      "line_value": 2164,
      "unit": "millions",
      "line_category": "Total"
    },
    {
      "line_name": "Stock-based compensation",
      "line_value": 543,
      "unit": "millions",
      "line_category": "Recurring"
    },
    {
      "line_name": "Amortization of intangibles",
      "line_value": 118,
      "unit": "millions",
      "line_category": "Recurring"
    },
    {
      "line_name": "Non-GAAP operating income",
      "line_value": 2825,
      "unit": "millions",
      "line_category": "Total"
    }
  ]
}
```

**Line category classification:**
| Category | Description | Examples |
|----------|-------------|---------|
| `Recurring` | Normal, occurs every period | Depreciation, amortization, stock-based compensation |
| `One-Time` | Unusual or infrequent | Restructuring, impairment, acquisition costs, legal settlements |
| `Total` | Summary or total lines | "GAAP operating income", "Non-GAAP operating income", "Adjusted EBITDA" |

**Extraction rules:**

- Extract values EXACTLY as shown
- The first item is usually the GAAP starting figure (a Total)
- The last item is usually the non-GAAP ending figure (a Total)
- All items in between are adjustments (Recurring or One-Time)

### Step 5: Validate the Reconciliation

Verify that:

```
First item (GAAP figure) + Sum of all adjustments (non-Total items) ≈ Last item (Non-GAAP figure)
```

**Rules:**

- Skip intermediate "Total" items (they are subtotals, not addends)
- The first item is always included in the sum (it's the base)
- Tolerance: ≤ 1

If validation fails, attempt one retry by re-reading the table more carefully. If it still fails, save the data and report the error.

### Step 6: Classify as Operating/Non-Operating

For each adjustment line item (non-Total items), determine if it is operating or non-operating.

**IMPORTANT:** Use the `is_calculated_operating_expense_mapping.csv` in `tools/` as the source of truth. Key classifications:

| Classification    | Examples                                                                                                                                                                          |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Operating**     | Stock-based compensation, depreciation (internal), other operating expenses                                                                                                       |
| **Non-Operating** | Amortization of acquired intangibles, acquisition costs, restructuring/impairment, litigation, interest adjustments, tax adjustments, gain/loss on divestitures, foreign exchange |

**Common mistakes to avoid:**

- ❌ "Amortization of intangibles" is **NOT operating** — it relates to acquired intangibles (purchase accounting), not organic operations
- ❌ "Acquisition-related expenses" are **NOT operating** — they are M&A costs
- ❌ "Restructuring and impairment charges" are **NOT operating** — they are one-time/unusual
- ❌ "Loss contingency" items are **NOT operating** — they are litigation-related
- ✅ "Stock-based compensation" IS operating — it is a recurring cost of employment
- ✅ "Depreciation" IS operating — it relates to internally-owned assets

### Step 7: Write Output to Markdown

Append the following section to the document's `.md` file:

```markdown
---

## GAAP Reconciliation

| Field               | Value                     |
| ------------------- | ------------------------- |
| Reconciliation Type | Operating Income / EBITDA |
| Unit                | {unit}                    |
| Validation          | {PASS or FAIL}            |
| Extraction Date     | {current_date_iso}        |

### Reconciliation Items

| #   | Line Name                   | Value | Category  | Operating |
| --- | --------------------------- | ----- | --------- | --------- |
| 1   | GAAP operating income       | 2,164 | Total     | —         |
| 2   | Stock-based compensation    | 543   | Recurring | Yes       |
| 3   | Amortization of intangibles | 118   | Recurring | Yes       |
| 4   | Non-GAAP operating income   | 2,825 | Total     | —         |
```

---

## Error Handling

- If document is not an earnings announcement → Skip entirely (not an error)
- If reconciliation table not found → Note in markdown ("GAAP Reconciliation: Not found")
- If wrong table type found (net income instead of operating) → Re-search for correct table
- If validation fails → Save data, report error

## Reference

Based on `tiger-cafe\app\app_agents\gaap_reconciliation_extractor.py`

---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_data_extraction/gaap_reconciliation/examples/`
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

- List every `.md` file in `skills/financial_data_extraction/gaap_reconciliation/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_data_extraction/gaap_reconciliation/examples/`.
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
