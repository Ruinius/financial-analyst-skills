# Financial Data Extraction Example: BABA Q3 2026

Source: Alibaba Group Announces December Quarter 2025 Results.pdf
Ticker: BABA
Period: Q3 2026 (Dec 2025)
Currency: RMB

---
## Balance Sheet
| Field           | Value                           |
| --------------- | ------------------------------- |
| Currency        | RMB |
| Unit            | millions |
| Extraction Date | 2026-04-29 |
| Validation      | PASS |

### Line Items

| # | Line Name | Value | Category | Standardized Name | Calculated | Operating |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Cash and cash equivalents | 128174 | current_assets | cash_and_equivalents | No | No |
| 2 | Short-term investments | 179955 | current_assets | short_term_investments | No | No |
| 3 | Restricted cash and escrow receivables | 42345 | current_assets | restricted_cash | No | No |
| 4 | Equity securities and other investments | 29981 | current_assets | equity_method_investments | No | No |
| 5 | Prepayments, receivables and other assets | 231761 | current_assets | prepaid_expenses | No | Yes |
| 6 | Total current assets | 612216 | current_assets | total_current_assets | Yes | No |
| 7 | Equity securities and other investments | 440384 | noncurrent_assets | equity_method_investments | No | No |
| 8 | Prepayments, receivables and other assets | 98329 | noncurrent_assets | other_noncurrent_assets | No | Yes |
| 9 | Investment in equity method investees | 208832 | noncurrent_assets | equity_method_investments | No | No |
| 10 | Property and equipment, net | 254478 | noncurrent_assets | property_plant_equipment | No | Yes |
| 11 | Intangible assets, net | 18607 | noncurrent_assets | intangibles_net | No | No |
| 12 | Goodwill | 245453 | noncurrent_assets | goodwill | No | No |
| 13 | Total Assets | 1878299 | noncurrent_assets | total_assets | Yes | No |
| 14 | Current bank borrowings | 24655 | current_liabilities | short_term_debt | No | No |
| 15 | Income tax payable | 11235 | current_liabilities | current_income_taxes_payable | No | Yes |
| 16 | Accrued expenses, accounts payable and other liabilities | 351293 | current_liabilities | accounts_payable | No | Yes |
| 17 | Merchant deposits | 246 | current_liabilities | advances_from_customers | No | Yes |
| 18 | Deferred revenue and customer advances | 72382 | current_liabilities | current_deferred_revenue | No | Yes |
| 19 | Total current liabilities | 459811 | current_liabilities | total_current_liabilities | Yes | No |
| 20 | Deferred revenue | 4454 | noncurrent_liabilities | long_term_deferred_revenue | No | Yes |
| 21 | Deferred tax liabilities | 46232 | noncurrent_liabilities | deferred_tax_liabilities | No | Yes |
| 22 | Non-current bank borrowings | 51423 | noncurrent_liabilities | long_term_debt | No | No |
| 23 | Non-current unsecured senior notes | 118637 | noncurrent_liabilities | long_term_debt | No | No |
| 24 | Non-current convertible unsecured senior notes | 56473 | noncurrent_liabilities | convertible_debt | No | No |
| 25 | Non-current exchangeable bonds | 11552 | noncurrent_liabilities | convertible_debt | No | No |
| 26 | Other liabilities | 23789 | noncurrent_liabilities | other_noncurrent_liabilities | No | No |
| 27 | Total liabilities | 772371 | noncurrent_liabilities | total_liabilities | Yes | No |
| 28 | Mezzanine equity | 7751 | equity | preferred_stock | No | No |
| 29 | Ordinary shares | 1 | equity | common_stock | No | No |
| 30 | Additional paid-in capital | 382770 | equity | additional_paid_in_capital | No | No |
| 31 | Treasury shares at cost | -36143 | equity | treasury_stock | No | No |
| 32 | Statutory reserves | 16628 | equity | statutory_reserves | No | No |
| 33 | Accumulated other comprehensive income (loss) | -6431 | equity | aoci | No | No |
| 34 | Retained earnings | 682830 | equity | retained_earnings | No | No |
| 35 | Noncontrolling interests | 58522 | equity | noncontrolling_interests | No | No |
| 36 | Total Equity | 1098177 | equity | total_liabilities_and_equity | Yes | No |

---
## Income Statement
| Field           | Value                           |
| --------------- | ------------------------------- |
| Currency        | RMB |
| Unit            | millions |
| Extraction Date | 2026-04-29 |
| Validation      | PASS |

### Line Items

| # | Line Name | Value | Standardized Name | Calculated | Operating | Expense |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Revenue | 284843 | revenue | No | Yes | No |
| 2 | Cost of revenue | -169534 | cost_of_revenue | No | Yes | Yes |
| 3 | Product development expenses | -15480 | research_and_development_expense | No | Yes | Yes |
| 4 | Sales and marketing expenses | -71934 | sales_and_marketing_expense | No | Yes | Yes |
| 5 | General and administrative expenses | -8355 | general_and_administrative_expense | No | Yes | Yes |
| 6 | Amortization and impairment of intangible assets | -841 | amortization_acquired | No | No | Yes |
| 7 | Impairment of goodwill | -9515 | restructuring_and_impairment_charges | No | No | Yes |
| 8 | Other (losses) gains, net | 1461 | other_operating_income_expense_net | No | Yes | No |
| 9 | Income from operations | 10645 | operating_income | Yes | Yes | No |
| 10 | Interest and investment income, net | 16221 | interest_income | No | No | No |
| 11 | Interest expense | -2557 | interest_expense | No | No | Yes |
| 12 | Other income (expense), net | -434 | other_income_expense_net | No | No | No |
| 13 | Income before income tax and share of results of equity method investees | 23875 | income_before_taxes | Yes | No | No |
| 14 | Income tax expenses | -8460 | income_tax_provision | No | Yes | Yes |
| 15 | Share of results of equity method investees | 216 | equity_method_income_loss | No | No | No |
| 16 | Net income | 15631 | net_income | Yes | No | No |

---
## Shares Outstanding
| Field | Value |
| --- | --- |
| Basic Shares Outstanding | 18568 |
| Basic Unit | millions |
| Diluted Shares Outstanding | 19310 |
| Diluted Unit | millions |
| Extraction Date | 2026-04-29 |

---
## Organic Growth
| Field | Value |
| --- | --- |
| Current Revenue | 284843 |
| Current Revenue Unit | millions |
| Prior Year Revenue | 280154 |
| Prior Year Revenue Unit | millions |
| Simple Growth (%) | 1.67 |
| Organic Growth (%) | 9.0 |
| **Final Growth (%)** | **9.0** |
| Growth Source | Reported constant-currency |
| Extraction Date | 2026-04-29 |

---
## GAAP Reconciliation
| Field | Value |
| --- | --- |
| Reconciliation Type | Operating Income |
| Unit | millions |
| Validation | PASS |
| Extraction Date | 2026-04-29 |

### Reconciliation Items

| # | Line Name | Value | Category | Operating |
| --- | --- | --- | --- | --- |
| 1 | Income from operations (GAAP) | 10645 | gaap_item | Yes |
| 2 | Non-cash share-based compensation expense | 2396 | Recurring | Yes |
| 3 | Amortization and impairment of intangible assets | 841 | Recurring | No |
| 4 | Impairment of goodwill, and others | 9515 | One-Time | No |
| 5 | Adjusted EBITA | 23397 | adjusted_item | Yes |
