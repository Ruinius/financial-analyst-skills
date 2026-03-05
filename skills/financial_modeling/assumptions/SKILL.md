---
name: DCF Assumptions
description: Create the three-stage DCF assumptions (revenue growth, EBITA margin, marginal capital turnover) by blending historical trends with qualitative outlook.
---

# DCF Assumptions (Sub-Skill 5b)

## Prerequisites

- WACC calculated (Sub-Skill 5a)
- Financial History table in `TICKER_metadata.md`
- Qualitative Assessment section in `TICKER_metadata.md` (EBITA Margin Outlook, Organic Growth Outlook)

## Overview

The DCF model uses a **three-stage assumption framework**:

| Stage    | Years | Purpose                                                 |
| -------- | ----- | ------------------------------------------------------- |
| Stage 1  | 1–5   | Near-term: current trajectory + qualitative adjustments |
| Stage 2  | 6–10  | Mid-term: convergence toward steady-state               |
| Terminal | 11+   | Perpetuity: long-run sustainable economics              |

Within each stage, values **interpolate linearly** between the start and end points. For example, if Stage 1 revenue growth is 5% and Stage 2 is 3%, Year 1 = 5%, Year 2 = 4.6%, Year 3 = 4.2%, etc.

## Step-by-Step Instructions

### Step 1: Calculate Historical Averages

From the Financial History table, compute the **trailing 4-quarter averages** (L4Q) for:

| Metric                   | How to Compute                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| **L4Q Revenue**          | Average of last 4 quarters' revenue × 4 (annualized)                                              |
| **L4Q EBITA Margin**     | Average of last 4 quarters' EBITA Margin (skip 0% entries — indicates missing data)               |
| **L4Q Adj Tax Rate**     | Average of last 4 quarters' Adj Tax Rate (skip 0% entries)                                        |
| **L4Q Capital Turnover** | Average of last 4 quarters' Capital Turnover (skip extreme outliers >50x or <0.1x)                |
| **Revenue Growth**       | The most recent `Organic Growth` value that is not N/A; or use Simple Growth from recent quarters |

> ⚠️ **Skip anomalous data points.** Revenue = 0, EBITA Margin = 0%, ROIC > 1000% all indicate incomplete extraction and should be excluded from averages.

### Step 2: Read Qualitative Outlook

From the Qualitative Assessment section:

1. **Organic Growth Outlook**:
   - `Direction` (Increase / Decrease)
   - `Magnitude` (e.g., "+4 pp over 5 years")
   - This tells us how much revenue growth is expected to change

2. **EBITA Margin Outlook**:
   - `Direction` (Expand / Shrink)
   - `Magnitude` (e.g., "-2 pp over 5 years")
   - This tells us how much margins are expected to change

3. **Economic Moat**:
   - `Rating` (Wide / Narrow / None)
   - Wide moat → terminal margins and ROIC can be higher
   - No moat → terminal margins converge to cost of capital

### Step 3: Set Revenue Growth Assumptions

**Stage 1 (starting point):**

```
Stage 1 Revenue Growth = Current organic growth rate (from L4Q)
```

If organic growth is N/A, use simple revenue growth.

**Stage 2 (5-year target):**

```
Stage 2 Revenue Growth = Stage 1 + Organic Growth Outlook adjustment
```

Example: If current growth = -4% and outlook says "+4 pp over 5 years":
→ Stage 2 = -4% + 4% = 0%

**Terminal Growth:**

| Economic Moat | Terminal Growth |
| ------------- | --------------- |
| Wide          | 4.0%            |
| Narrow        | 3.5%            |
| None          | 3.0%            |

> Terminal growth must NEVER exceed WACC. If it does, cap it at WACC - 1%.

### Step 4: Set EBITA Margin Assumptions

**Stage 1 (starting point):**

```
Stage 1 EBITA Margin = L4Q EBITA Margin
```

**Stage 2 (5-year target):**

```
Stage 2 EBITA Margin = Stage 1 + EBITA Margin Outlook adjustment
```

Example: If L4Q margin = 8.7% and outlook says "-2 pp over 5 years":
→ Stage 2 = 8.7% - 2% = 6.7%

**Terminal Margin:**

| Economic Moat | Terminal Margin Rule                       |
| ------------- | ------------------------------------------ |
| Wide          | Stage 2 margin (sustained advantage)       |
| Narrow        | Stage 2 margin × 0.9 (slight erosion)      |
| None          | Stage 2 margin × 0.8 (significant erosion) |

### Step 5: Set Marginal Capital Turnover

Marginal Capital Turnover (MCT) represents how many dollars of incremental revenue each dollar of incremental invested capital produces.

```
MCT = ΔRevenue / ΔInvested Capital
```

A **higher MCT** means the company needs less capital to grow (asset-light). A **lower MCT** means heavy reinvestment is required per dollar of growth (capital-intensive).

**Setting MCT:**

1. Compute L4Q Capital Turnover (Revenue / Invested Capital)
2. If the value is within the **valid range** (`0 < MCT < 100`), use it
3. If the value is **out of range** (negative IC, zero IC, or MCT > 100), default to **100.0x**

The **100.0x default** is correct for asset-light businesses (e.g., SaaS companies like ADBE with negative invested capital). It means almost no incremental capital is needed to grow revenue — which is exactly what "negative invested capital" implies.

> ⚠️ **Do NOT default to 1.0x.** MCT = 1.0x means every $1 of revenue growth requires $1 of new capital — that's a heavy industrial business, not a software company. Getting this wrong will massively undervalue asset-light companies.

| Stage    | MCT                                                   |
| -------- | ----------------------------------------------------- |
| Stage 1  | L4Q Capital Turnover (if valid) or **100.0x** default |
| Stage 2  | Same as Stage 1                                       |
| Terminal | Same as Stage 1                                       |

### Step 6: Set Tax Rate

```
Adjusted Tax Rate = L4Q Adjusted Tax Rate
```

- Floor at **10%** (below this is often a data issue)
- Cap at **40%** (above this is unusual)
- If all L4Q values are 0% or anomalous, use the **statutory rate** for the company's domicile

### Step 7: Write Output to Markdown

Append to `TICKER_metadata.md`:

```markdown
---

## DCF Assumptions

| Parameter                 | Stage 1 (Yr 1-5) | Stage 2 (Yr 6-10) | Terminal  |
| ------------------------- | ---------------- | ----------------- | --------- |
| Revenue Growth            | {g1_pct}%        | {g2_pct}%         | {gt_pct}% |
| EBITA Margin              | {m1_pct}%        | {m2_pct}%         | {mt_pct}% |
| Marginal Capital Turnover | {mct1}x          | {mct2}x           | {mctt}x   |

| Parameter                 | Value              |
| ------------------------- | ------------------ |
| Adjusted Tax Rate         | {tax_pct}%         |
| WACC                      | {wacc_pct}%        |
| Base Revenue (Annualized) | {base_rev}         |
| Base Invested Capital     | {base_ic}          |
| Calculation Date          | {current_date_iso} |

### Assumption Rationale

- Revenue Growth: {explanation of how qualitative outlook modified historical trend}
- EBITA Margin: {explanation}
- Capital Turnover: {explanation, note if defaulted}
- Tax Rate: {explanation, note if capped/floored}
```

---

## Important Notes

- The three-stage framework means the model interpolates smoothly rather than having sharp jumps between stages. Year 3 uses a blended rate between Stage 1 and Stage 2.
- Assumptions should be **conservative but realistic**. The qualitative outlook from analyst reports provides the directional bias.
- If the qualitative assessment is missing, fall back to **historical trend continuation** for Stage 1 → Stage 2, and use standard terminal assumptions based on a Narrow moat default.
- The `base_revenue` is **annualized** (quarterly × 4). This is critical — the DCF projects annual figures.

## Reference

Based on assumption setup logic in `calculate_dcf()` in `tiger-cafe/app/utils/financial_modeling.py`


---

## Example Curation

> **Examples folder for THIS skill:** `skills/financial_modeling/assumptions/examples/`
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

- List every `.md` file in `skills/financial_modeling/assumptions/examples/`
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Keep Only the Best Example

- Compare all example files (including the one you just created) and **select the single best one** — the one that is most complete, correct, and instructive.
- **Delete all other example files** from `skills/financial_modeling/assumptions/examples/`.
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
