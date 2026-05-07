# Document Classification

| Field               | Value               |
| ------------------- | ------------------- |
| Company Name        | Fiserv, Inc.     |
| Ticker              | FISV      |
| Document Type       | earnings_announcement |
| Document Date       | 2026-05-05 |
| Time Period         | Q1 2026 |
| Period End Date     | 2026-03-31 |
| Confidence          | high   |
| Original Filename   | FISV Q1 '26 Earnings Release - Final to IR.pdf     |
| Classification Date | 2026-05-06 |

---

<!-- Sections below will be populated by subsequent skills -->

---
## Balance Sheet
| Field           | Value                           |
| --------------- | ------------------------------- |
| Currency        | USD |
| Unit            | millions |
| Extraction Date | 2026-05-06 |
| Validation      | PASS |

### Line Items

| # | Line Name | Value | Category | Standardized Name | Calculated | Operating |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Cash and cash equivalents | 829 | current_assets | cash_and_equivalents | No | No |
| 2 | Trade accounts receivable - net | 3882 | current_assets | accounts_receivable | No | Yes |
| 3 | Prepaid expenses and other current assets | 3411 | current_assets | prepaid_expenses | No | Yes |
| 4 | Settlement assets | 16660 | current_assets | settlement_receivable | No | Yes |
| 5 | Total current assets | 24782 | current_assets | total_current_assets | Yes | No |
| 6 | Property and equipment - net | 3225 | noncurrent_assets | property_plant_equipment | No | Yes |
| 7 | Customer relationships - net | 4828 | noncurrent_assets | noncurrent_notes_receivables | No | Yes |
| 8 | Other intangible assets - net | 5154 | noncurrent_assets | intangibles_net | No | No |
| 9 | Goodwill | 37602 | noncurrent_assets | goodwill | No | No |
| 10 | Contract costs - net | 1056 | noncurrent_assets | deferred_contract_costs | No | Yes |
| 11 | Investments in unconsolidated affiliates | 1028 | noncurrent_assets | equity_method_investments | No | No |
| 12 | Other long-term assets | 2873 | noncurrent_assets | other_noncurrent_assets | No | Yes |
| 13 | Total assets | 80548 | noncurrent_assets | total_assets | Yes | No |
| 14 | Accounts payable and other current liabilities | 4591 | current_liabilities | accounts_payable | No | Yes |
| 15 | Short-term and current maturities of long-term debt | 1323 | current_liabilities | current_portion_long_term_debt | No | No |
| 16 | Contract liabilities | 844 | current_liabilities | current_deferred_revenue | No | Yes |
| 17 | Settlement obligations | 16660 | current_liabilities | settlement_payable | No | Yes |
| 18 | Total current liabilities | 23418 | current_liabilities | total_current_liabilities | Yes | No |
| 19 | Long-term debt | 27859 | noncurrent_liabilities | long_term_debt | No | No |
| 20 | Deferred income taxes | 1688 | noncurrent_liabilities | deferred_tax_liabilities | No | Yes |
| 21 | Long-term contract liabilities | 243 | noncurrent_liabilities | long_term_deferred_revenue | No | Yes |
| 22 | Other long-term liabilities | 1119 | noncurrent_liabilities | other_noncurrent_liabilities | No | No |
| 23 | Total liabilities | 54327 | noncurrent_liabilities | total_liabilities | Yes | No |
| 24 | Fiserv shareholders' equity | 26201 | equity | parent_equity | No | No |
| 25 | Noncontrolling interests | 20 | equity | noncontrolling_interests | No | No |
| 26 | Total equity | 26221 | equity | total_equity | Yes | No |

---
## Income Statement
| Field           | Value                           |
| --------------- | ------------------------------- |
| Currency        | USD |
| Unit            | millions |
| Extraction Date | 2026-05-06 |
| Validation      | PASS |

### Line Items

| # | Line Name | Value | Standardized Name | Calculated | Operating | Expense |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Processing and services revenue | 4070 | segment_revenue | No | Yes | No |
| 2 | Product revenue | 957 | segment_revenue | No | Yes | No |
| 3 | Total revenue | 5027 | total_revenue | Yes | Yes | No |
| 4 | Cost of processing and services | -1610 | segment_cost_of_revenue | No | Yes | Yes |
| 5 | Cost of product | -697 | segment_cost_of_revenue | No | Yes | Yes |
| 6 | Selling, general and administrative | -1885 | sales_general_and_administrative_expense | No | Yes | Yes |
| 7 | Net gain on sale of assets | -83 | gain_loss_divestitures | No | No | No |
| 8 | Total expenses | -4109 | total_operating_expenses | Yes | Yes | Yes |
| 9 | Operating income | 918 | operating_income | Yes | Yes | No |
| 10 | Interest expense, net | -347 | interest_expense_net | No | No | Yes |
| 11 | Other income (expense), net | 22 | other_income_expense_net | No | No | No |
| 12 | Income before income taxes | 593 | income_before_taxes | Yes | No | No |
| 13 | Income tax provision | -24 | income_tax_provision | No | Yes | Yes |
| 14 | Income from investments in unconsolidated affiliates | 4 | equity_method_income_loss | No | No | No |
| 15 | Net income | 573 | net_income | Yes | No | No |
| 16 | Net income attributable to noncontrolling interests | 2 | net_income_noncontrolling | No | No | No |
| 17 | Net income attributable to Fiserv | 571 | net_income_parent | Yes | No | No |

---
## Shares Outstanding
| Field | Value |
| --- | --- |
| Basic Shares Outstanding | 535.4 |
| Basic Unit | millions |
| Diluted Shares Outstanding | 535.4 |
| Diluted Unit | millions |
| Extraction Date | 2026-05-06 |

---
## Organic Growth
| Field | Value |
| --- | --- |
| Current Revenue | 5027 |
| Current Revenue Unit | millions |
| Prior Year Revenue | 5130 |
| Prior Year Revenue Unit | millions |
| Simple Growth (%) | -2.01 |
| Organic Growth (%) | -4.0 |
| **Final Growth (%)** | **-4.0** |
| Growth Source | Reported constant-currency |
| Extraction Date | 2026-05-06 |

---
## GAAP Reconciliation
| Field | Value |
| --- | --- |
| Reconciliation Type | Operating Income |
| Unit | millions |
| Validation | PASS |
| Extraction Date | 2026-05-06 |

### Reconciliation Items

| # | Line Name | Value | Category | Operating |
| --- | --- | --- | --- | --- |
| 1 | Operating income (GAAP) | 918 | gaap_item | Yes |
| 2 | Merger and integration costs | 29 | One-Time | No |
| 3 | One Fiserv transformation program expenses | 142 | One-Time | No |
| 4 | Severance costs | 73 | One-Time | No |
| 5 | Amortization of acquisition-related intangible assets | 311 | Recurring | No |
| 6 | Net gain on sale of assets | -83 | One-Time | No |
| 7 | Adjusted operating income | 1390 | adjusted_item | Yes |


---

## EBITA

| Field | Value |
|-------|-------|
| Starting Point | Operating Income |
| Starting Value | 918.0 |
| EBITA | 1473.0 |
| EBITA Margin | 29.30% |
| Calculation Date | 2026-05-06 |

### Adjustments

| # | Line Name | Value | Source |
|---|-----------|-------|--------|
| 1 | Merger and integration costs | 29.0 | GAAP Reconciliation |
| 2 | One Fiserv transformation program expenses | 142.0 | GAAP Reconciliation |
| 3 | Severance costs | 73.0 | GAAP Reconciliation |
| 4 | Amortization of acquisition-related intangible assets | 311.0 | GAAP Reconciliation |
| 5 | Net gain on sale of assets | -83.0 | GAAP Reconciliation |
| 6 | Net gain on sale of assets | 83.0 | Income Statement |


---

## Invested Capital

| Field | Value |
|-------|-------|
| Net Working Capital | 1858.0 |
| Net Long-Term Operating Assets | 10051.0 |
| Invested Capital | 11909.0 |
| Capital Turnover | 1.69x |
| Calculation Date | 2026-05-06 |

### Net Working Capital Breakdown

| Component | Items | Total |
|-----------|-------|-------|
| Operating Current Assets | Trade accounts receivable - net, Prepaid expenses and other current assets, Settlement assets | 23953.0 |
| Operating Current Liabilities | Accounts payable and other current liabilities, Contract liabilities, Settlement obligations | 22095.0 |
| **Net Working Capital** | | **1858.0** |

### Net Long-Term Operating Assets Breakdown

| Component | Items | Total |
|-----------|-------|-------|
| Operating Noncurrent Assets | Property and equipment - net, Customer relationships - net, Contract costs - net, Other long-term assets | 11982.0 |
| Operating Noncurrent Liabilities | Deferred income taxes, Long-term contract liabilities | 1931.0 |
| **Net Long-Term Operating Assets** | | **10051.0** |



---

## Tax Rates

| Field | Value |
|-------|-------|
| Income Before Taxes | 593.0 |
| Income Tax Expense | -24.0 |
| Net Income | 573.0 |
| Effective Tax Rate | 4.05% |
| Adjusted Tax Rate | -2.51% |
| Calculation Date | 2026-05-06 |

### Adjusted Tax Rate Breakdown

| # | Line Name | Value | Tax Effect | Source | Marginal Rate |
|---|-----------|-------|------------|--------|---------------|
| 1 | Merger and integration costs | 29.0 | 7.25 | GAAP Reconciliation | 25% |
| 2 | One Fiserv transformation program expenses | 142.0 | 35.50 | GAAP Reconciliation | 25% |
| 3 | Severance costs | 73.0 | 18.25 | GAAP Reconciliation | 25% |
| 4 | Amortization of acquisition-related intangible assets | 311.0 | 0.00 | GAAP Reconciliation | 0% |
| 5 | Net gain on sale of assets | -83.0 | -20.75 | GAAP Reconciliation | 25% |
| 6 | Net gain on sale of assets | 83.0 | 20.75 | Income Statement | 25% |
| | **Reported Tax** | **-24.0** | | | |
| | **Total Tax Adjustment** | | **61.00** | | |
| | **Adjusted Tax** | **37.00** | | | |


---

## Financial Summary

| Metric | Value | Notes |
|--------|-------|-------|
| **Revenue** | 5027.0 | |
| **EBITA** | 1473.0 | |
| **EBITA Margin** | 29.30% | |
| **Effective Tax Rate** | 4.05% | |
| **Adjusted Tax Rate** | -2.51% | |
| **NOPAT** | 1510.00 | Using Adjusted Tax Rate |
| **Net Working Capital** | 1858.0 | |
| **Net Long-Term Operating Assets** | 10051.0 | |
| **Invested Capital** | 11909.0 | |
| **Capital Turnover** | 1.69x | Annualized |
| **ROIC** | 50.72% | Annualized |
| **Interest Expense** | 0 | |
| **Basic Shares Outstanding** | 535.4 | |
| **Diluted Shares Outstanding** | 535.4 | |
| **Simple Revenue Growth** | -2.01% | YoY |
| **Organic Revenue Growth** | -4.00% | Constant currency |

### Calculation Notes

- Computed NOPAT automatically using EBITA x (1 - applicable tax rate)
- Annualization multiplier applied to NOPAT for ROIC calculation: 4x
