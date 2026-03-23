---
name: Financial Modeling
description: Execute a single deterministic Python script to compute WACC, DCF assumptions, projected free cash flows, enterprise value, and intrinsic value per share. Updates both the metadata markdown and the JSON export for the interactive viewer.
---

# Financial Modeling (Phase 6)

All modeling logic is consolidated into a single script that executes the complete sequence: WACC → Assumptions → DCF → Intrinsic Value → JSON Export.

1. Execute the script: `python skills/financial_modeling/scripts/calculate.py {TICKER} {TICKER_metadata_path}`
2. Verify it threw no errors.

## What the Script Does

| Step | Action | Details |
|------|--------|---------|
| 1 | Fetch Market Data | Calls `tools/market_data.py profile {TICKER}` for share price, beta, market cap |
| 2 | Read Historical Data | Parses Financial History table from metadata for L4Q averages |
| 3 | Read Qualitative Data | Parses Economic Moat, Margin Outlook, Growth Outlook from metadata |
| 4 | Calculate WACC | CAPM with Blume-adjusted beta, capital structure weights |
| 5 | Generate Assumptions | Three-stage DCF assumptions blending historical trends + qualitative outlook |
| 6 | Run DCF Projections | 10-year projections with interpolated growth/margin, terminal value via Gordon Growth |
| 7 | Compute Intrinsic Value | Equity bridge: EV + Cash - Debt → Per Share |
| 8 | Update Metadata | Replaces WACC, Assumptions, DCF Model, and Intrinsic Value sections in markdown |
| 9 | Update JSON Export | Patches `TICKER_financial_model.json` for the interactive viewer |

## Prerequisites

- `output_data/TICKER/TICKER_metadata.md` must exist with Financial History and Qualitative Assessment sections
- Internet access required for Yahoo Finance market data lookup
- Python 3.10+ with `yfinance` installed

## Key Parameters

| Parameter | Source | Default |
|-----------|--------|---------|
| Risk-Free Rate | Hardcoded (TODO: fetch 10Y Treasury) | 4.20% |
| Equity Risk Premium | Hardcoded | 5.00% |
| Terminal Growth | Moat rating: Wide=4%, Narrow=3%, None=2.5% | 3.00% |
| MCT | Derived from IC, default if negative IC | 100.0x |
| Tax Rate (statutory) | Hardcoded for WACC | 25% |
| Tax Rate (NOPAT) | L4Q average adjusted tax rate | Varies |
| WACC Bounds | Floor 6%, Cap 15% | — |
