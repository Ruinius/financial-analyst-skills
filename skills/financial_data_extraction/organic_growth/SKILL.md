---
name: Organic Growth Extraction
description: Extract organic/constant-currency growth percentage and prior-year revenue from a financial PDF.
---

# Organic Growth Extraction (Sub-Skill 2d)

## Prerequisites

- Classification metadata available in `processing_data/TICKER_DOCTYPE_DATE_temp.md`
- **Income Statement must be extracted first** (Sub-Skill 2b) — needs current revenue
- No external services required (LLM-only)

## Step-by-Step Instructions

### Step 1: Read Inputs

1. Read the classification `.md` file to get: `time_period`, `period_end_date`
2. Read the Income Statement section from the `.md` file to get:
   - Current period revenue value
   - Revenue line item name (e.g., "Total revenue", "Net revenues")
   - Currency and unit
3. Read the PDF directly using multimodal capabilities

### Step 2: Extract Organic Growth Percentage

Search the document for an explicitly stated **organic growth** or **constant-currency growth** percentage.

**What to look for:**
- "organic growth" / "organic revenue growth"
- "constant currency growth" / "constant currency revenue growth"
- "currency-neutral growth"

**Rules:**
- Extract the RAW percentage as a float (e.g., 5.5 for 5.5%, -2.3 for -2.3%)
- Only extract if EXPLICITLY labeled as organic or constant-currency growth
- Do NOT extract simple reported revenue growth
- If not found, set to null (many companies don't report this)

### Step 3: Extract Prior-Year Revenue

Extract the **prior year's revenue** from the comparative column in the income statement.

**How to find it:**
1. Identify the prior period column:
   - If current period ends `2025-02-28`, prior period is `2024-03-01` (same quarter, one year prior)
   - The prior period column is usually the column to the right of the current period
2. Extract the revenue value from the SAME ROW as the current period revenue

**Validation (Reflection):**
- Ensure the prior revenue is from the correct duration (quarterly vs. annual)
  - If current period is Q1, prior should also be a single quarter (not full year)
  - The prior revenue should be in a similar magnitude to current revenue (within 50%)
- If the extracted value seems wrong (e.g., 4x the current revenue), it may be from a full-year column instead of quarterly

### Step 4: Calculate Simple Growth

If both current and prior revenue are available:

```
simple_growth = (current_revenue - prior_revenue) / prior_revenue × 100
```

### Step 5: Cross-Validate (if organic growth was found)

If organic growth percentage was extracted in Step 2:
- Compare it with the calculated simple growth from Step 4
- Organic growth should be within a reasonable range of simple growth (usually ±5 percentage points)
- If the difference is >10 percentage points, flag for user review

### Step 6: Write Output to Markdown

Append the following section to the document's `.md` file:

```markdown
---

## Organic Growth

| Field | Value |
|-------|-------|
| Current Revenue | {current_revenue} |
| Current Revenue Unit | {unit} |
| Prior Year Revenue | {prior_revenue} |
| Prior Year Revenue Unit | {unit} |
| Simple Growth (%) | {simple_growth} |
| Organic Growth (%) | {organic_growth or "Not reported"} |
| Extraction Date | {current_date_iso} |
```

---

## Error Handling

- If income statement not yet extracted → Inform user to run Sub-Skill 2b first
- If prior year revenue not found → Set to null, still extract organic growth if available
- If organic growth not found → Set to null (this is normal for many companies)

## Reference

Based on `tiger-cafe\app\app_agents\organic_growth_extractor.py`
