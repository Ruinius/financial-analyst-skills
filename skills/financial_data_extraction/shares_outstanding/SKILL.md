---
name: Shares Outstanding Extraction
description: Extract basic and diluted shares outstanding from a financial PDF.
---

# Shares Outstanding Extraction (Sub-Skill 2c)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- No external services required (LLM-only extraction)

## Step-by-Step Instructions

### Step 1: Read the PDF and Classification Metadata

1. Read the classification `.md` file to get: `time_period`, `period_end_date`
2. Read the PDF directly using multimodal capabilities

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
