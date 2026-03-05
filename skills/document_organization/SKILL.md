---
name: Document Organization
description: Move processed documents from processing_data/ to output_data/TICKER/, create/update company metadata, and perform cross-document date healing.
---

# Document Organization Skill

This skill is the final step in the single-document pipeline. It takes a fully processed document (with all extraction and calculation sections) from `processing_data/` and archives it into the organized `output_data/` structure.

## Prerequisites

- Skills 1-3 must have been completed
- The document's `.md` file in `processing_data/` must contain all sections: Classification, Balance Sheet, Income Statement, Shares Outstanding, Organic Growth, GAAP Reconciliation, EBITA, Tax Rates, Invested Capital, and Financial Summary

## Inputs

- `processing_data/TICKER_DOCTYPE_YYYYMMDD_temp.pdf` — the source PDF
- `processing_data/TICKER_DOCTYPE_YYYYMMDD_temp.md` — the fully processed markdown

## Outputs

- `output_data/TICKER/TICKER_DOCTYPE_YYYYMMDD.pdf` — archived PDF (renamed, `_temp` removed)
- `output_data/TICKER/TICKER_DOCTYPE_YYYYMMDD.md` — archived markdown (renamed, `_temp` removed)
- `output_data/TICKER/TICKER_metadata.md` — company-level metadata file (created or updated)

## Step-by-Step Instructions

### Step 1: Read Classification Metadata

From the document's `.md` file, extract:
- `ticker` (e.g., `ADBE`)
- `company_name` (e.g., `Adobe Inc.`)
- `document_type` (e.g., `earnings_announcement`)
- `document_date` (e.g., `2025-03-12`)
- `time_period` (e.g., `Q1 2025`)
- `period_end_date` (e.g., `2025-02-28`)
- `currency` (e.g., `USD`, `RMB`, `JPY`)

Also scan each section (Balance Sheet, Income Statement, Shares Outstanding, GAAP Reconciliation) to collect the `unit` used in each.

### Step 2: Harmonize Units

Different sections of the same document may use different units. Before archiving, normalize all monetary values to a single **prevailing unit**.

**How to determine the prevailing unit:**
1. Check the `Unit` field in each section header (Balance Sheet, Income Statement, GAAP Reconciliation)
2. The prevailing unit is the one used by the **Balance Sheet** and **Income Statement** — they should agree
3. If they disagree, use the most common unit across sections

**Common units and conversion factors:**

| Unit | Factor to Ones | Example |
|------|---------------|---------|
| ones | 1 | ¥123,456,789 |
| thousands | 1,000 | $123,457 (thousands) |
| ten_thousands (万) | 10,000 | ¥12,346 (万円) |
| millions | 1,000,000 | $123 (millions) |
| hundred_millions (億) | 100,000,000 | ¥1.2 (億円) |
| billions | 1,000,000,000 | $0.12 (billions) |

**What to harmonize:**

| Section | Likely to differ? | Action if different |
|---------|-------------------|--------------------|
| Balance Sheet | Rarely | Convert all values |
| Income Statement | Rarely | Convert all values |
| Shares Outstanding | **Often** — shares may be in ones or thousands while financials are in millions | Convert to prevailing unit |
| GAAP Reconciliation | Rarely | Convert all values |
| Organic Growth (prior-year revenue) | Sometimes | Convert to prevailing unit |
| EBITA / Tax / Invested Capital | These use IS/BS values — should already match | Verify only |
| Financial Summary | Aggregates above — should already match | Verify only |

**Example — Shares Outstanding harmonization:**
```
Prevailing unit: millions
Shares Outstanding section says: 436 (unit: millions) → No change needed
If it said: 436,000,000 (unit: ones) → Convert: 436,000,000 / 1,000,000 = 436 millions
If it said: 436,000 (unit: thousands) → Convert: 436,000 / 1,000 = 436 millions
```

**After harmonization:**
1. Update unit values in each section header to show the prevailing unit
2. Add a note at the top of the markdown:
   ```
   | Prevailing Unit | {prevailing_unit} |
   ```
3. If any conversion was performed, add a note: "Unit harmonized from {original} to {prevailing}"

### Step 3: Create Output Directory

Create the ticker directory if it doesn't exist:
```
output_data/TICKER/
```
Example: `output_data/ADBE/`

### Step 4: Move and Rename Files

Remove the `_temp` suffix from both files and move them:

| Source | Destination |
|--------|------------|
| `processing_data/ADBE_EA_20250312_temp.pdf` | `output_data/ADBE/ADBE_EA_20250312.pdf` |
| `processing_data/ADBE_EA_20250312_temp.md` | `output_data/ADBE/ADBE_EA_20250312.md` |

**Rules:**
- If the destination file already exists, this is a re-processing scenario — overwrite the existing file
- The `_temp` suffix was only for the processing pipeline; final files should not have it

### Step 5: Create or Update Company Metadata

Check if `output_data/TICKER/TICKER_metadata.md` exists.

#### If it does NOT exist — Create it:

```markdown
# {Company Name} ({TICKER})

| Field | Value |
|-------|-------|
| Ticker | {TICKER} |
| Company Name | {company_name} |
| Currency | {currency} |
| Unit | {unit} |
| Last Updated | {current_date_iso} |

---

## Processed Documents

| # | File | Document Type | Time Period | Period End Date | Document Date | Processed |
|---|------|--------------|-------------|-----------------|---------------|-----------|
| 1 | [TICKER_DOCTYPE_YYYYMMDD.md](TICKER_DOCTYPE_YYYYMMDD.md) | {document_type} | {time_period} | {period_end_date} | {document_date} | {current_date_iso} |

---

## Financial History

| Time Period | Period End | Revenue | EBITA | EBITA Margin | Adj Tax Rate | NOPAT | Invested Capital | ROIC | Organic Growth |
|-------------|-----------|---------|-------|--------------|-------------|-------|-----------------|------|----------------|
| {time_period} | {period_end_date} | {revenue} | {ebita} | {ebita_margin} | {adj_tax_rate} | {nopat} | {invested_capital} | {roic} | {organic_growth} |
```

#### If it DOES exist — Update it:

1. **Add a new row** to the "Processed Documents" table with the new document's info
2. **Add a new row** to the "Financial History" table with the summary metrics
3. **Sort** both tables by `period_end_date` (ascending — oldest first)
4. Update the `Last Updated` field
5. **Check for duplicates**: If a row with the same `time_period` already exists, replace it (re-processing scenario)

### Step 6: Cross-Document Date Healing

If the metadata file already has other documents for this ticker, perform date healing:

**What is date healing?**
Sometimes document classification gets a date slightly wrong (e.g., `period_end_date` is `2024-12-31` when it should be `2024-11-29` for Adobe's fiscal year). When multiple documents are available, we can detect and fix these inconsistencies.

**How to heal:**
1. Read all existing documents for this ticker from the metadata
2. Check if the fiscal calendar is consistent:
   - Are period end dates roughly evenly spaced? (3 months for quarterly, 12 for annual)
   - Does the company use a non-standard fiscal year? (e.g., Adobe ends ~Nov/Feb/May/Aug)
3. If the NEW document's `period_end_date` seems inconsistent with the established pattern, flag it:
   - Add a note to the metadata: "⚠️ Period end date may be incorrect for {time_period}"
   - Do NOT auto-correct — flag for human review
4. Update any previously flagged dates if the new document provides clarifying context

**Example:**
```
Existing:   Q4 2024 → 2024-11-29, Q3 2024 → 2024-08-30
New:        Q1 2025 → 2025-02-28
Pattern:    ~3 months apart ✓ (Nov → Feb = 3 months)
Result:     No healing needed
```

### Step 7: Confirm Completion

After moving files: 
1. Verify the source files no longer exist in `processing_data/`
2. Verify the destination files exist in `output_data/TICKER/`
3. Verify the metadata file is valid markdown
4. Report completion to the user with a summary:

```
✅ Document organized:
   ADBE_EA_20250312.md → output_data/ADBE/
   Metadata updated: 1 document(s) for ADBE
   Date healing: No issues detected
```

---

## Error Handling

- If source files not found in `processing_data/` → Inform user, skip
- If metadata file is corrupted → Back up and recreate
- If conflicting time periods → Flag for user review, do not auto-resolve
- If directory creation fails → Inform user

## Reference

Based on the tiger-cafe document processing pipeline and file management patterns.


---

## Example Curation

> **Examples folder for THIS skill:** `skills/document_organization/examples/`
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

- List every `.md` file in `skills/document_organization/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/document_organization/examples/`.
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
