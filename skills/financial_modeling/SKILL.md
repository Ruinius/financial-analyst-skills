---
name: Financial Modeling
description: Build a multi-stage DCF (Discounted Cash Flow) model from historical financial data and qualitative outlook assumptions. Produces WACC, 10-year projections, terminal value, enterprise value, and intrinsic value per share.
---

# Financial Modeling Skill

This skill reads the company's `TICKER_metadata.md` file (Financial History + Qualitative Assessment) and constructs a complete DCF valuation model. **All calculations are pure arithmetic** — no LLM calls, no external services.

## Prerequisites

- Skills 1–4 must have been run on **at least 4 quarters** of earnings data for reliable base revenue
- The `TICKER_metadata.md` must contain:
  - **Financial History** table (Revenue, EBITA, EBITA Margin, Adj Tax Rate, NOPAT, Invested Capital, ROIC)
  - **Qualitative Assessment** section (Economic Moat, EBITA Margin Outlook, Organic Growth Outlook)

## Inputs

- `output_data/TICKER/TICKER_metadata.md` — the company-level metadata file

## Outputs

- Updated `TICKER_metadata.md` with WACC, Assumptions, DCF Model, and Intrinsic Value sections
- `output_data/TICKER/TICKER_financial_model.json` — machine-readable DCF output for the interactive viewer

## Sub-Skills

| Sub-Skill               | Folder             | Description                                                    | Depends On                    |
| ----------------------- | ------------------ | -------------------------------------------------------------- | ----------------------------- |
| **5a. WACC**            | `wacc/`            | Weighted Average Cost of Capital via CAPM                      | Financial History             |
| **5b. Assumptions**     | `assumptions/`     | Revenue growth, EBITA margins, capital turnover for 3 stages   | WACC + Qualitative Assessment |
| **5c. DCF Model**       | `dcf/`             | 10-year projection + terminal value + enterprise value         | WACC + Assumptions            |
| **5d. Intrinsic Value** | `intrinsic_value/` | Enterprise Value → Equity Value → Per-Share value              | DCF Model + Balance Sheet     |
| **5e. JSON Export**     | `json_export/`     | Write `TICKER_financial_model.json` for the interactive viewer | All above                     |

### Execution Order

1. Run **5a** (WACC) first — independent
2. Run **5b** (Assumptions) — needs WACC + Qualitative Assessment
3. Run **5c** (DCF Model) — needs WACC + Assumptions
4. Run **5d** (Intrinsic Value) — needs DCF + Balance Sheet
5. Run **5e** (JSON Export) last — needs all prior results

### Key Design Principle

The DCF model uses a **three-stage approach** that smoothly interpolates assumptions:

- **Stage 1 (Years 1–5)**: Near-term assumptions, linearly interpolating toward Stage 2
- **Stage 2 (Years 6–10)**: Mid-term assumptions, linearly interpolating toward Terminal
- **Terminal (Year 11+)**: Steady-state assumptions for perpetuity valuation

This structure allows the model to gradually transition between different growth/margin regimes rather than making abrupt jumps.

---

## Reference

Based on `calculate_dcf()` in `tiger-cafe/app/utils/financial_modeling.py` (324 lines)
