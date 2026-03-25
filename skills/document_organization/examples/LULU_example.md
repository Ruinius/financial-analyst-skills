# Document Classification

| Field               | Value               |
| ------------------- | ------------------- |
| Company Name        | lululemon athletica inc.     |
| Ticker              | LULU      |
| Document Type       | earnings_announcement |
| Document Date       | 2024-06-05 |
| Time Period         | Q1 2024 |
| Period End Date     | 2024-04-28 |
| Confidence          | high   |
| Original Filename   | 06-05-2024-210527670.pdf     |
| Classification Date | 2026-03-25 |

---

<!-- Sections below will be populated by subsequent skills -->

---
## Balance Sheet
| Field           | Value                           |
| --------------- | ------------------------------- |
| Currency        | USD |
| Unit            | thousands |
| Extraction Date | 2026-03-25 |
| Validation      | PASS |

### Line Items

| # | Line Name | Value | Category | Standardized Name | Calculated | Operating |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Cash and cash equivalents | 1900672 | current_assets | cash_and_equivalents | No | No |
| 2 | Inventories | 1345267 | current_assets | inventory | No | Yes |
| 3 | Prepaid and receivable income taxes | 192955 | current_assets | current_income_tax_receivable | No | Yes |
| 4 | Other current assets | 329193 | current_assets | other_current_assets | No | Yes |
| 5 | Total current assets | 3768087 | current_assets | total_current_assets | Yes | No |
| 6 | Property and equipment, net | 1561185 | noncurrent_assets | property_plant_equipment | No | Yes |
| 7 | Right-of-use lease assets | 1263749 | noncurrent_assets | operating_lease_assets | No | Yes |
| 8 | Goodwill and intangible assets, net | 23992 | noncurrent_assets | goodwill | No | No |
| 9 | Deferred income taxes and other non-current assets | 211482 | noncurrent_assets | deferred_tax_assets | No | Yes |
| 10 | Total assets | 6828495 | noncurrent_assets | total_assets | Yes | No |
| 11 | Accounts payable | 261605 | current_liabilities | accounts_payable | No | Yes |
| 12 | Accrued liabilities and other | 374446 | current_liabilities | other_current_liabilities | No | No |
| 13 | Accrued compensation and related expenses | 132911 | current_liabilities | accrued_compensation | No | Yes |
| 14 | Current lease liabilities | 254443 | current_liabilities | current_lease_liabilities | No | Yes |
| 15 | Current income taxes payable | 53087 | current_liabilities | current_income_taxes_payable | No | Yes |
| 16 | Unredeemed gift card liability | 268296 | current_liabilities | current_deferred_revenue | No | Yes |
| 17 | Other current liabilities | 38783 | current_liabilities | other_current_liabilities | No | No |
| 18 | Total current liabilities | 1383571 | current_liabilities | total_current_liabilities | Yes | No |
| 19 | Non-current lease liabilities | 1147631 | noncurrent_liabilities | long_term_lease_liabilities | No | Yes |
| 20 | Non-current income taxes payable | 15864 | noncurrent_liabilities | long_term_income_taxes_payable | No | Yes |
| 21 | Deferred income tax liability | 29150 | noncurrent_liabilities | deferred_tax_liabilities | No | Yes |
| 22 | Other non-current liabilities | 32471 | noncurrent_liabilities | other_noncurrent_liabilities | No | No |
| 23 | Stockholders' equity | 4219808 | equity | total_equity | Yes | No |
| 24 | Total liabilities and stockholders' equity | 6828495 | equity | total_liabilities_and_equity | Yes | No |

---
## Income Statement
| Field           | Value                           |
| --------------- | ------------------------------- |
| Currency        | USD |
| Unit            | thousands |
| Extraction Date | 2026-03-25 |
| Validation      | PASS |

### Line Items

| # | Line Name | Value | Standardized Name | Calculated | Operating | Expense |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Net revenue | 2208891 | revenue | No | Yes | No |
| 2 | Cost of goods sold | -933823 | cost_of_revenue | No | Yes | Yes |
| 3 | Gross profit | 1275068 | gross_profit | Yes | Yes | No |
| 4 | Selling, general and administrative expenses | -842426 | sales_general_and_administrative_expense | No | Yes | Yes |
| 5 | Amortization of intangible assets | 0 | amortization_acquired | No | No | Yes |
| 6 | Income from operations | 432642 | operating_income | Yes | Yes | No |
| 7 | Other income (expense), net | 23283 | other_income_expense_net | No | No | No |
| 8 | Income before income tax expense | 455925 | income_before_taxes | Yes | No | No |
| 9 | Income tax expense | -134504 | income_tax_provision | No | Yes | Yes |
| 10 | Net income | 321421 | net_income | Yes | No | No |

---
## Shares Outstanding
| Field | Value |
| --- | --- |
| Basic Shares Outstanding | 125.989 |
| Basic Unit | millions |
| Diluted Shares Outstanding | 126336.0 |
| Diluted Unit | millions |
| Extraction Date | 2026-03-25 |

---
## Organic Growth
| Field | Value |
| --- | --- |
| Current Revenue | 2208891 |
| Current Revenue Unit | thousands |
| Prior Year Revenue | 2000792 |
| Prior Year Revenue Unit | thousands |
| Simple Growth (%) | 10.4 |
| Organic Growth (%) | 7.0 |
| **Final Growth (%)** | **7.0** |
| Growth Source | Reported constant-currency |
| Extraction Date | 2026-03-25 |

---
## GAAP Reconciliation
| Field | Value |
| --- | --- |
| Reconciliation Type | Operating Income |
| Unit | thousands |
| Validation | PASS |
| Extraction Date | 2026-03-25 |

### Reconciliation Items

| # | Line Name | Value | Category | Operating |
| --- | --- | --- | --- | --- |


---

## EBITA

| Field | Value |
|-------|-------|
| Starting Point | Operating Income |
| Starting Value | 432642.0 |
| EBITA | 432642.0 |
| EBITA Margin | 19.59% |
| Calculation Date | 2026-03-25 |



---

## Invested Capital

| Field | Value |
|-------|-------|
| Net Working Capital | 897073.0 |
| Net Long-Term Operating Assets | 1843771.0 |
| Invested Capital | 2740844.0 |
| Capital Turnover | 3.22x |
| Calculation Date | 2026-03-25 |

### Net Working Capital Breakdown

| Component | Items | Total |
|-----------|-------|-------|
| Operating Current Assets | Inventories, Prepaid and receivable income taxes, Other current assets | 1867415.0 |
| Operating Current Liabilities | Accounts payable, Accrued compensation and related expenses, Current lease liabilities, Current income taxes payable, Unredeemed gift card liability | 970342.0 |
| **Net Working Capital** | | **897073.0** |

### Net Long-Term Operating Assets Breakdown

| Component | Items | Total |
|-----------|-------|-------|
| Operating Noncurrent Assets | Property and equipment, net, Right-of-use lease assets, Deferred income taxes and other non-current assets | 3036416.0 |
| Operating Noncurrent Liabilities | Non-current lease liabilities, Non-current income taxes payable, Deferred income tax liability | 1192645.0 |
| **Net Long-Term Operating Assets** | | **1843771.0** |



---

## Tax Rates

| Field | Value |
|-------|-------|
| Income Before Taxes | 455925.0 |
| Income Tax Expense | -134504.0 |
| Net Income | 321421.0 |
| Effective Tax Rate | 29.50% |
| Adjusted Tax Rate | 31.09% |
| Calculation Date | 2026-03-25 |

### Adjusted Tax Rate Breakdown

| # | Line Name | Value | Tax Effect | Source | Marginal Rate |
|---|-----------|-------|------------|--------|---------------|
| | **Reported Tax** | **-134504.0** | | | |
| | **Total Tax Adjustment** | | **0.00** | | |
| | **Adjusted Tax** | **-134504.00** | | | |


---

## Financial Summary

| Metric | Value | Notes |
|--------|-------|-------|
| **Revenue** | 2208891.0 | |
| **EBITA** | 432642.0 | |
| **EBITA Margin** | 19.59% | |
| **Effective Tax Rate** | 29.50% | |
| **Adjusted Tax Rate** | 31.09% | |
| **NOPAT** | 298138.00 | Using Adjusted Tax Rate |
| **Net Working Capital** | 897073.0 | |
| **Net Long-Term Operating Assets** | 1843771.0 | |
| **Invested Capital** | 2740844.0 | |
| **Capital Turnover** | 3.22x | Annualized |
| **ROIC** | 43.51% | Annualized |
| **Interest Expense** | 0 | |
| **Basic Shares Outstanding** | 125.989 | |
| **Diluted Shares Outstanding** | 126.336 | |
| **Simple Revenue Growth** | 10.40% | YoY |
| **Organic Revenue Growth** | 7.00% | Constant currency |

### Calculation Notes

- Computed NOPAT automatically using EBITA x (1 - applicable tax rate)
- Annualization multiplier applied to NOPAT for ROIC calculation: 4x
