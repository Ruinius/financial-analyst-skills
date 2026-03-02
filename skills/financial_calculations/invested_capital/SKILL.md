---
name: Invested Capital Calculation
description: Calculate Net Working Capital, Net Long-Term Operating Assets, and total Invested Capital from balance sheet data.
---

# Invested Capital Calculation (Sub-Skill 3c)

## Prerequisites

- Balance Sheet extracted (Skill 2a) with `Operating` and `Calculated` flags from Tiger-Transformer

## Key Concept

Invested Capital = Net Working Capital + Net Long-Term Operating Assets

Only **operating** items are included. Non-operating items (like short-term investments, goodwill, debt) are excluded.

## Step-by-Step Instructions

### Step 1: Read Balance Sheet Data

From the document's `.md` file, read the Balance Sheet line items. Each item has:
- `Category`: current_assets, noncurrent_assets, current_liabilities, noncurrent_liabilities, stockholders_equity
- `Calculated`: Yes/No (whether it's a subtotal/total)
- `Operating`: Yes/No (whether it's an operating item)
- `Value`: The numeric value

### Step 2: Calculate Net Working Capital (NWC)

**Formula:**
```
NWC = Operating Current Assets - Operating Current Liabilities
```

**Rules:**
- Only include items where `Category` = `current_assets` or `current_liabilities`
- Only include items where `Operating` = Yes
- **Skip** items where `Calculated` = Yes (these are subtotals like "Total Current Assets")

**Adobe Example:**
| Item | Value | Category | Operating | Include? |
|------|-------|----------|-----------|----------|
| Trade receivables | 1,973 | current_assets | Yes | ✅ |
| Prepaid expenses | 1,447 | current_assets | Yes | ✅ |
| Cash and cash equivalents | 6,758 | current_assets | No | ❌ |
| Short-term investments | 677 | current_assets | No | ❌ |
| Total current assets | 10,855 | current_assets | No | ❌ (calculated) |
| Accrued expenses | 1,951 | current_liabilities | Yes | ✅ |
| Deferred revenue | 6,347 | current_liabilities | Yes | ✅ |
| Income taxes payable | 465 | current_liabilities | Yes | ✅ |
| Operating lease liabilities | 74 | current_liabilities | Yes | ✅ |
| Trade payables | 326 | current_liabilities | Yes | ✅ |
| Debt | 0 | current_liabilities | No | ❌ |

```
Operating Current Assets  = 1,973 + 1,447 = 3,420
Operating Current Liabilities = 326 + 1,951 + 6,347 + 465 + 74 = 9,163
NWC = 3,420 - 9,163 = -5,743
```

### Step 3: Calculate Net Long-Term Operating Assets (NLTOA)

**Formula:**
```
NLTOA = Operating Noncurrent Assets - Operating Noncurrent Liabilities
```

**Same rules** as NWC but for `noncurrent_assets` and `noncurrent_liabilities`:
- Only `Operating` = Yes
- Skip `Calculated` = Yes

**Adobe Example:**
| Item | Value | Category | Operating | Include? |
|------|-------|----------|-----------|----------|
| Property and equipment | 1,893 | noncurrent_assets | Yes | ✅ |
| Operating lease ROU | 266 | noncurrent_assets | Yes | ✅ |
| Deferred income taxes | 1,820 | noncurrent_assets | Yes | ✅ |
| Other assets | 1,638 | noncurrent_assets | Yes | ✅ |
| Goodwill | 12,777 | noncurrent_assets | No | ❌ |
| Other intangibles | 706 | noncurrent_assets | No | ❌ |
| Deferred revenue (LT) | 143 | noncurrent_liabilities | Yes | ✅ |
| Income taxes payable (LT) | 567 | noncurrent_liabilities | Yes | ✅ |
| Operating lease liabilities (LT) | 334 | noncurrent_liabilities | Yes | ✅ |
| Other liabilities | 498 | noncurrent_liabilities | No | ❌ |

```
Operating Noncurrent Assets = 1,893 + 266 + 1,820 + 1,638 = 5,617
Operating Noncurrent Liabilities = 143 + 567 + 334 = 1,044
NLTOA = 5,617 - 1,044 = 4,573
```

### Step 4: Calculate Invested Capital

```
Invested Capital = NWC + NLTOA
                 = -5,743 + 4,573
                 = -1,170
```

### Step 5: Calculate Capital Turnover

```
Capital Turnover = Annualized Revenue / Invested Capital
```

**Annualization rule:**
- If `time_period` starts with Q (quarterly), multiply revenue by 4
- If `time_period` starts with FY (full year), use as-is

```
Annualized Revenue = 5,714 × 4 = 22,856
Capital Turnover = 22,856 / -1,170 = -19.53x
```

(Negative because invested capital is negative — Adobe has more operating liabilities than assets, driven by deferred revenue. This is common for subscription businesses.)

### Step 6: Write Output to Markdown

Append to the document's `.md` file:

```markdown
---

## Invested Capital

| Field | Value |
|-------|-------|
| Net Working Capital | {nwc} |
| Net Long-Term Operating Assets | {nltoa} |
| Invested Capital | {invested_capital} |
| Capital Turnover | {capital_turnover}x |
| Calculation Date | {current_date_iso} |

### Net Working Capital Breakdown

| Component | Items | Total |
|-----------|-------|-------|
| Operating Current Assets | {list of items} | {total} |
| Operating Current Liabilities | {list of items} | {total} |
| **Net Working Capital** | | **{nwc}** |

### Net Long-Term Operating Assets Breakdown

| Component | Items | Total |
|-----------|-------|-------|
| Operating Noncurrent Assets | {list of items} | {total} |
| Operating Noncurrent Liabilities | {list of items} | {total} |
| **Net Long-Term Operating Assets** | | **{nltoa}** |
```

---

## Reference

Based on `calculate_net_working_capital()`, `calculate_net_long_term_operating_assets()`, `calculate_invested_capital()`, and `calculate_capital_turnover()` in `tiger-cafe/app/utils/historical_calculations.py`
