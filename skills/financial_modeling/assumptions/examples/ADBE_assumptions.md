# DCF Assumptions Example: Adobe Inc. (ADBE)

> Source: ADBE_metadata.md Financial History (Q1 2025 – Q4 2025) + Qualitative Assessment

## Inputs

**Financial History (L4Q = Q1-Q4 2025):**

| Quarter | Revenue | EBITA | EBITA Margin | Adj Tax Rate | NOPAT | IC     | Organic Growth |
| ------- | ------- | ----- | ------------ | ------------ | ----- | ------ | -------------- |
| Q1 2025 | 5,714   | 2,246 | 39.31%       | 17.56%       | 1,852 | -1,170 | 11.0%          |
| Q2 2025 | 5,873   | 2,192 | 37.32%       | 18.50%       | 1,786 | -1,020 | 11.0%          |
| Q3 2025 | 5,988   | 2,252 | 37.61%       | 18.50%       | 1,835 | -855   | 10.0%          |
| Q4 2025 | 6,194   | 2,322 | 37.49%       | 18.50%       | 1,892 | -1,606 | 10.0%          |

**Qualitative Assessment:**

- Economic Moat: **Wide** (switching costs, first-mover, cross-sell flywheel)
- EBITA Margin Outlook: **Expand +2 pp** over 5 years (AI monetization, declining R&D intensity)
- Organic Growth Outlook: **Stable to slight decrease, -1 pp** (ARR deceleration to ~10%)

**WACC:** 10.41% (from Sub-Skill 5a)

## Calculation Walkthrough

### Step 1: Historical Averages (L4Q)

```
L4Q Revenue (annualized)    = (5714 + 5873 + 5988 + 6194) = 23,769M
L4Q EBITA Margin (average)  = (39.31 + 37.32 + 37.61 + 37.49) / 4 = 37.93%
L4Q Adj Tax Rate (average)  = (17.56 + 18.50 + 18.50 + 18.50) / 4 = 18.27%
L4Q Organic Growth (latest) = 10.5% (average of 11%, 11%, 10%, 10%)
```

### Step 2: Revenue Growth

```
Stage 1 = L4Q organic growth = 10.5%
Stage 2 = 10.5% + (-1 pp) = 9.5%     ← Qualitative: -1 pp
Terminal = 4.0%                         ← Wide moat default
```

Terminal (4.0%) < WACC (10.41%) ✓

### Step 3: EBITA Margin

```
Stage 1 = L4Q EBITA Margin = 37.93%
Stage 2 = 37.93% + 2.0 pp = 39.93%    ← Qualitative: +2 pp expansion
Terminal = Stage 2 = 39.93%             ← Wide moat: sustained advantage
```

### Step 4: Marginal Capital Turnover

```
L4Q Capital Turnover = Revenue / Invested Capital
                     = 23,769 / (-1,606)
                     = -14.8x (NEGATIVE — out of valid range)

→ Default to 100.0x (asset-light, per reference logic)
```

ADBE has **negative invested capital** because its deferred revenue (~$7B) exceeds operating assets. MCT = 100x means virtually no capital reinvestment needed to grow.

### Step 5: Tax Rate

```
Adjusted Tax Rate = 18.27% (L4Q average)
Floor check: 18.27% > 10% ✓
Cap check:   18.27% < 40% ✓
```

## Output

```markdown
## DCF Assumptions

| Parameter                 | Stage 1 (Yr 1-5) | Stage 2 (Yr 6-10) | Terminal |
| ------------------------- | ---------------- | ----------------- | -------- |
| Revenue Growth            | 10.50%           | 9.50%             | 4.00%    |
| EBITA Margin              | 37.93%           | 39.93%            | 39.93%   |
| Marginal Capital Turnover | 100.0x           | 100.0x            | 100.0x   |

| Parameter                 | Value      |
| ------------------------- | ---------- |
| Adjusted Tax Rate         | 18.27%     |
| WACC                      | 10.41%     |
| Base Revenue (Annualized) | $23,769M   |
| Base Invested Capital     | $-1,606M   |
| Calculation Date          | 2026-03-03 |

### Assumption Rationale

- **Revenue Growth**: L4Q organic growth averages ~10.5%. Qualitative outlook: -1 pp, so Stage 2 = 9.5%. Wide moat → terminal 4.0%.
- **EBITA Margin**: L4Q margin ~37.9%. Qualitative outlook: +2 pp, so Stage 2 = 39.9%. Wide moat sustains terminal.
- **Capital Turnover**: ADBE has negative invested capital (deferred revenue > operating assets). IC out of valid range → MCT defaulted to 100.0x per reference logic.
- **Tax Rate**: L4Q average adjusted tax rate (18.27%), within 10-40% bounds.
```
