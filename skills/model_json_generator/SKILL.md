---
name: Model JSON Generator
description: Extracts the WACC, assumptions, and DCF projections from the markdown metadata file and converts them into a clean, structured JSON file for the frontend interactive viewer.
---

# Model JSON Generator (Phase 7)

This skill reads the completed `TICKER_metadata.md` file and converts the financial modeling tables into `TICKER_financial_model.json`. 

1. Execute the script: `python skills/model_json_generator/scripts/generate_json.py {TICKER} {TICKER_metadata_path}`
2. Verify it threw no errors.

## What the Script Does

- Reads `TICKER_metadata.md`
- Parses tables for Financial History, WACC, DCF Assumptions, DCF Model Projections, and Intrinsic Value.
- Transforms the flat table data into a nested JSON structure.
- Writes to `output_data/TICKER/TICKER_financial_model.json` for consumption by the interactive viewer.

## Prerequisites

- Phase 6 (Financial Modeling) must have already run and populated the WACC, DCF Assumptions, and DCF Model sections in the metadata.
