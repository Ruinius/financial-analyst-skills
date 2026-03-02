---
name: Financial Calculations
description: Compute derived financial metrics (EBITA, tax rates, invested capital, ROIC) from previously extracted data. All calculations are pure math — no LLM calls needed.
---

# Financial Calculations Skill

This skill reads the extracted financial data from the document's `.md` file and computes derived metrics. **All calculations are pure arithmetic** — no LLM calls, no external services.

## Prerequisites

- Skill 2 (Financial Data Extraction) must have been run first
- The document's `.md` file must contain: Balance Sheet, Income Statement, and optionally GAAP Reconciliation sections

## Inputs

- The document's `.md` file in `processing_data/` with extracted financial data
- Key fields needed from the extracted data:
  - **Balance Sheet**: Line items with `Category`, `Operating` flags, `Calculated` flags
  - **Income Statement**: Line items with `Standardized Name`, `Operating` flags, `Expense` flags, sign-normalized values
  - **GAAP Reconciliation** (if available): Adjustment items with `Operating` classification

## Sub-Skills

| Sub-Skill | Folder | Description | Depends On |
|-----------|--------|-------------|------------|
| **3a. EBITA** | `ebita/` | Earnings Before Interest, Tax, and Amortization | Income Statement + GAAP Reconciliation |
| **3b. Tax Rates** | `tax/` | Effective and adjusted (operating) tax rates | Income Statement + EBITA |
| **3c. Invested Capital** | `invested_capital/` | Net Working Capital + Net Long-Term Operating Assets | Balance Sheet |
| **3d. Summary Table** | `summary_table/` | Final summary with NOPAT, ROIC, and all metrics | All above |

### Execution Order

1. Run **3a** (EBITA) and **3c** (Invested Capital) — independent of each other
2. Run **3b** (Tax Rates) after 3a — needs EBITA
3. Run **3d** (Summary Table) last — needs all prior results

### Key Design Principle

These calculations rely entirely on the `is_operating`, `is_calculated`, and `is_expense` flags set by the Tiger-Transformer in Skill 2. No fuzzy matching or LLM calls needed — the transformer already did the hard work of classifying each line item.

---

## Reference

Based on `tiger-cafe/app/utils/historical_calculations.py` (802 lines)
