# Financial Data Extraction Example: PYPL Q3 2025

---
## Balance Sheet
| Field           | Value                           |
| --------------- | ------------------------------- |
| Currency        | USD |
| Unit            | millions |
| Extraction Date | 2026-05-05 |
| Validation      | PASS |

### Line Items

| # | Line Name | Value | Category | Standardized Name | Calculated | Operating |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Cash and cash equivalents | 8995 | current_assets | cash_and_equivalents | No | No |
| 2 | Short-term investments | 1760 | current_assets | short_term_investments | No | No |
| 3 | Accounts receivable, net | 973 | current_assets | accounts_receivable | No | Yes |
| 4 | Loans and interest receivable, held for sale | 1404 | current_assets | current_notes_receivables | No | Yes |
| 5 | Loans and interest receivable, net | 6396 | current_assets | current_notes_receivables | No | Yes |
| 6 | Funds receivable and customer accounts | 38668 | current_assets | funds_held_for_clients | No | Yes |
| 7 | Prepaid expenses and other current assets | 1980 | current_assets | prepaid_expenses | No | Yes |
| 8 | Total current assets | 60176 | current_assets | total_current_assets | Yes | No |
| 9 | Long-term investments | 3601 | noncurrent_assets | long_term_investments | No | No |
| 10 | Property and equipment, net | 1656 | noncurrent_assets | property_plant_equipment | No | Yes |
| 11 | Goodwill | 10941 | noncurrent_assets | goodwill | No | No |
| 12 | Intangible assets, net | 226 | noncurrent_assets | intangibles_net | No | No |
| 13 | Other assets | 3201 | noncurrent_assets | other_noncurrent_assets | No | Yes |
| 14 | Total assets | 79801 | noncurrent_assets | total_assets | Yes | No |

---
## Income Statement
| Field           | Value                           |
| --------------- | ------------------------------- |
| Currency        | USD |
| Unit            | millions |
| Extraction Date | 2026-05-05 |
| Validation      | PASS |

### Line Items

| # | Line Name | Value | Standardized Name | Calculated | Operating | Expense |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Net revenues | 8417 | revenue | No | Yes | No |
| 2 | Transaction expense | -4063 | cost_of_revenue | No | Yes | Yes |
| 3 | Transaction and credit losses | -483 | merger_and_acquisition_costs | No | No | Yes |
| 4 | Customer support and operations | -447 | cost_of_revenue | No | Yes | Yes |
| 5 | Sales and marketing | -521 | sales_and_marketing_expense | No | Yes | Yes |
| 6 | Technology and development | -801 | research_and_development_expense | No | Yes | Yes |
| 7 | General and administrative | -513 | general_and_administrative_expense | No | Yes | Yes |
| 8 | Restructuring and other | -69 | restructuring_and_impairment_charges | No | No | Yes |
| 9 | Total operating expenses | -6897 | total_operating_expenses | Yes | Yes | Yes |
| 10 | Operating income | 1520 | operating_income | Yes | Yes | No |
| 11 | Other income (expense), net | 13 | other_income_expense_net | No | No | No |
| 12 | Income before income taxes | 1533 | income_before_taxes | Yes | No | No |
| 13 | Income tax expense | -285 | income_tax_provision | No | Yes | Yes |
| 14 | Net income (loss) | 1248 | net_income | Yes | No | No |

---
## Shares Outstanding
| Field | Value |
| --- | --- |
| Basic Shares Outstanding | 950 |
| Basic Unit | millions |
| Diluted Shares Outstanding | 960 |
| Diluted Unit | millions |
| Extraction Date | 2026-05-05 |

---
## Organic Growth
| Field | Value |
| --- | --- |
| Current Revenue | 8417 |
| Current Revenue Unit | millions |
| Prior Year Revenue | 7847 |
| Prior Year Revenue Unit | millions |
| Simple Growth (%) | 7.26 |
| Organic Growth (%) | 6.0 |
| **Final Growth (%)** | **6.0** |
| Growth Source | Reported constant-currency |
| Extraction Date | 2026-05-05 |

---
## GAAP Reconciliation
| Field | Value |
| --- | --- |
| Reconciliation Type | Operating Income |
| Unit | millions |
| Validation | PASS |
| Extraction Date | 2026-05-05 |

### Reconciliation Items

| # | Line Name | Value | Category | Operating |
| --- | --- | --- | --- | --- |
| 1 | GAAP operating income | 1520 | gaap_item | Yes |
| 2 | Amortization of acquired intangible assets | 47 | Recurring | No |
| 3 | Restructuring | 1 | One-Time | No |
| 4 | Non-GAAP operating income | 1568 | adjusted_item | Yes |
