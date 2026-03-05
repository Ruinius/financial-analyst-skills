---
name: Balance Sheet Extraction
description: Extract balance sheet line items from a financial PDF, standardize names via Tiger-Transformer, and validate calculations.
---

# Balance Sheet Extraction (Sub-Skill 2a)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- If Tiger-Transformer is not running on localhost:8000 then ask the user to run `.\tools\start_transformer.bat`
- If a static file server is not running on localhost:8181 then ask the user to run `.\tools\start_file_server.bat`

**DO NOT EVER start servers without human user.**

## Step-by-Step Instructions

### Step 1: Read the PDF and Classification Metadata

1. Read the classification `.md` file to get: `ticker`, `document_type`, `time_period`, `period_end_date`
2. Open the PDF in the browser using the `browser_subagent` tool:
   - Navigate to `http://localhost:8181/processing_data/{filename}`
   - Navigate to the page(s) containing the **Consolidated Balance Sheet**
   - For large filings (10-K, 10-Q), use the table of contents or scroll to the financial statements section
3. Do NOT use PyPDF2 or other text extraction libraries

### Step 2: Locate and Verify the Balance Sheet Section

1. In the PDF, find the **Consolidated Balance Sheet** (or "Consolidated Balance Sheets")
2. Verify it is the CORRECT section — it should:
   - Have column headers matching the `period_end_date` or `time_period`
   - Be a CONSOLIDATED statement (not a subsidiary or segment)
   - Contain both Assets AND Liabilities/Equity sections
   - Not be a condensed summary table from a press release header — look for the full table
3. **ADR / dual-currency documents**: If the statement has BOTH a local currency column (e.g., RMB, TWD, EUR) AND a USD convenience translation column, **always use the local (functional) currency column**. Ignore the USD translation.
4. If the correct section cannot be found, inform the user

### Step 3: Extract Line Items

Extract **every** line item from the balance sheet table for the **current period column only** (the column matching `period_end_date`). The extraction must be **complete** — do not skip or abbreviate any rows.

**Output JSON structure:**

```json
{
  "currency": "RMB",
  "unit": "millions",
  "time_period": "Q1 2025",
  "period_end_date": "2025-02-28",
  "line_items": [
    {
      "line_name": "Cash and cash equivalents",
      "line_value": 7509,
      "line_category": "current_assets"
    }
  ]
}
```

> ⚠️ **COMPLETENESS CHECK — MANDATORY**
>
> After extraction, verify that ALL of the following section totals are present:
>
> | #   | Required Total             | Category                               |
> | --- | -------------------------- | -------------------------------------- |
> | 1   | Total Current Assets       | `current_assets`                       |
> | 2   | Total Assets               | `noncurrent_assets` (or computed)      |
> | 3   | Total Current Liabilities  | `current_liabilities`                  |
> | 4   | Total Liabilities          | `noncurrent_liabilities` (or computed) |
> | 5   | Total Stockholders' Equity | `stockholders_equity`                  |
>
> Additionally, verify that each section has **individual line items**, not just the totals. A valid balance sheet extraction should have:
>
> - **Current Assets**: At minimum Cash, Receivables, and 1+ other items
> - **Non-Current Assets**: At minimum PP&E/Fixed Assets, and 1+ other items
> - **Current Liabilities**: At minimum Payables, and 1+ other items
> - **Non-Current Liabilities**: At minimum Long-term debt or 1+ other items
>
> If any section is missing or has only a total with no breakdown, go back to the PDF and re-read. An incomplete balance sheet will cause Invested Capital calculations to be nonsensical.

**Extraction rules:**

- Extract values EXACTLY as shown — do NOT round, estimate, or calculate
- `line_name`: Shorten names, remove "net of..." notes
- `line_value`: Numeric only (no commas, no currency symbols). Use negative values where shown
- `line_category`: One of: `current_assets`, `noncurrent_assets`, `current_liabilities`, `noncurrent_liabilities`, `stockholders_equity`
- `unit`: Only set if EXPLICITLY stated (e.g., "In millions"). Otherwise null
- `currency`: Use the document's actual currency — do NOT assume or convert to USD. Common values: USD, EUR, GBP, JPY, CAD, RMB, CHF, AUD, KRW, INR, SEK, etc.
- Include ALL subtotals and totals (Total Current Assets, Total Assets, Total Liabilities, etc.)
- Include ALL individual line items within each section — do NOT summarize or aggregate
- Maintain the exact order from the document

**Anti-hallucination rules:**

- ONLY extract values explicitly shown in the document
- Do NOT invent line items or values
- If a value is not visible, use null
- Do NOT use external knowledge

### Step 4: Validate Section Categories

Check that all `line_category` values are valid. If any are missing or invalid, fix them using this fallback logic:

1. Inherit from the previous item
2. Inherit from the next item
3. Infer from the line name (e.g., "equity" → `stockholders_equity`)
4. Last resort: use `current_assets`

### Step 5: Standardize via Tiger-Transformer

Send **ALL line items together in a single batch request** to the Tiger-Transformer server.

> ⚠️ **CRITICAL: Send ALL items at once, not one at a time.** The model uses a sliding context window that looks at the 2 items before and 2 items after each line to classify it. Sending items individually (or in small groups) strips this context and causes misclassifications. Always send the complete list in document order.

**Avoid Shell Escaping Issues:** Do NOT try to send the large JSON payload via `curl` or `Invoke-RestMethod` inline on the command line. Write a temporary Python script (`tmp/run_bs_transformer.py`) using the `write_to_file` tool to send the HTTP request, then execute that script.

**Example Temporary Python Script:**

```python
import urllib.request
import json
import sys

payload = {
    "items": [
        {"line_name": "Cash and cash equivalents", "line_category": "current_assets", "line_order": 0},
        {"line_name": "Short-term investments", "line_category": "current_assets", "line_order": 1},
        # ... your extracted items ...
    ]
}

req = urllib.request.Request('http://localhost:8000/predict/balance-sheet',
                             method='POST',
                             headers={'Content-Type': 'application/json'},
                             data=json.dumps(payload).encode('utf-8'))

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
```

**Response:** Each item gets:

- `standardized_name`: Standardized key (e.g., `cash_and_equivalents`)
- `is_calculated`: Whether this is a subtotal/total line (from CSV mapping)
- `is_operating`: Whether this is an operating item (from CSV mapping)
- `confidence`: Model confidence score

### Step 6: Validate Calculations

Using the `is_calculated` flags from Step 5, verify that totals match their components:

**Validation checks:**

1. Sum of `current_assets` (non-calculated) ≈ Total Current Assets (calculated)
2. Sum of `noncurrent_assets` (non-calculated) ≈ Total Noncurrent Assets (calculated) — if present
3. Total Current Assets + Total Noncurrent Assets ≈ Total Assets
4. Sum of `current_liabilities` (non-calculated) ≈ Total Current Liabilities (calculated)
5. Sum of `noncurrent_liabilities` (non-calculated) ≈ Total Noncurrent Liabilities (calculated) — if present
6. Total Liabilities + Total Stockholders' Equity ≈ Total Liabilities and Equity
7. Total Assets ≈ Total Liabilities and Equity (the accounting equation)

**Tolerance:** Allow differences ≤ 1 (for rounding)

If validation fails, report the errors but still save the data. Do NOT re-extract unless errors are severe (>5% difference).

### Step 7: Fix Accumulated Depreciation Sign

If any line item with `standardized_name` containing "accumulated_depreciation" has a positive value, flip it to negative.

### Step 8: Write Output to Markdown

Append the following section to the document's `.md` file:

```markdown
---

## Balance Sheet

| Field           | Value                           |
| --------------- | ------------------------------- |
| Currency        | {currency}                      |
| Unit            | {unit}                          |
| Extraction Date | {current_date_iso}              |
| Validation      | {PASS or FAIL with error count} |

### Line Items

| #   | Line Name                 | Value | Category       | Standardized Name         | Calculated | Operating |
| --- | ------------------------- | ----- | -------------- | ------------------------- | ---------- | --------- |
| 1   | Cash and cash equivalents | 7,509 | current_assets | cash_and_cash_equivalents | No         | Yes       |
| ... | ...                       | ...   | ...            | ...                       | ...        | ...       |
```

---

## Error Handling

- If PDF cannot be opened in the browser → Inform user, skip
- If balance sheet section not found → Inform user, skip
- If transformer server is not running → Inform user (run `.\tools\start_transformer.bat`)
- If validation fails → Save data anyway, report errors in markdown

## Reference

Based on `tiger-cafe\app\app_agents\balance_sheet_extractor.py`

---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_data_extraction/balance_sheet/examples/`
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

- List every `.md` file in `skills/financial_data_extraction/balance_sheet/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_data_extraction/balance_sheet/examples/`.
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
