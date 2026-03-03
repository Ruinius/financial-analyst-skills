---
name: Shares Outstanding Extraction
description: Extract basic and diluted shares outstanding from a financial PDF.
---

# Shares Outstanding Extraction (Sub-Skill 2c)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- No external services required (LLM-only extraction)
- If a static file server is not running on localhost:8181 then ask the user to run `python -m http.server 8181 --bind 127.0.0.1`

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

| Field | Description |
|-------|-------------|
| `basic_shares_outstanding` | Number of basic shares |
| `basic_shares_outstanding_unit` | One of: `ones`, `thousands`, `millions`, `billions` |
| `diluted_shares_outstanding` | Number of diluted shares |
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

| Field | Value |
|-------|-------|
| Basic Shares Outstanding | {value} |
| Basic Unit | {unit} |
| Diluted Shares Outstanding | {value} |
| Diluted Unit | {unit} |
| Extraction Date | {current_date_iso} |
```

---

## Error Handling

- If share data not found → Set to null, note reason in markdown
- If only one type found → Extract what's available, set other to null

## Reference

Based on `tiger-cafe\app\app_agents\shares_outstanding_extractor.py`
