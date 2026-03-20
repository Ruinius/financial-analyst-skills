---
name: Financial Calculations
description: Execute a single deterministic Python script to compute all derived financial metrics (EBITA, Invested Capital, Tax Rates, Summary Table) from extracted financial data.
---

# Financial Calculations (Phase 3)

All calculation logic is consolidated into a single script that enforces the correct dependency chain internally.

1. Execute the script: `python skills/financial_calculations/scripts/calculate.py {markdown_file}`
2. Verify no errors were thrown.
