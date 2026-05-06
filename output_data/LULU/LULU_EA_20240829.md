# Document Classification

| Field               | Value               |
| ------------------- | ------------------- |
| Company Name        | lululemon athletica inc.     |
| Ticker              | LULU      |
| Document Type       | earnings_announcement |
| Document Date       | 2024-08-29 |
| Time Period         | Q2 2024 |
| Period End Date     | 2024-07-28 |
| Confidence          | high   |
| Original Filename   | 08-29-2024-210539148.pdf     |
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
| 1 | Cash and cash equivalents | 1610112 | current_assets | cash_and_equivalents | No | No |
| 2 | Inventories | 1429043 | current_assets | inventory | No | Yes |
| 3 | Prepaid and receivable income taxes | 210969 | current_assets | current_income_tax_receivable | No | Yes |
| 4 | Other current assets | 321620 | current_assets | other_current_assets | No | Yes |
| 5 | Total current assets | 3571744 | current_assets | total_current_assets | Yes | No |
| 6 | Property and equipment, net | 1614893 | noncurrent_assets | property_plant_equipment | No | Yes |
| 7 | Right-of-use lease assets | 1302947 | noncurrent_assets | operating_lease_assets | No | Yes |
| 8 | Goodwill and intangible assets, net | 23925 | noncurrent_assets | goodwill | No | No |
| 9 | Deferred income taxes and other non-current assets | 230626 | noncurrent_assets | deferred_tax_assets | No | Yes |
| 10 | Total assets | 6744135 | noncurrent_assets | total_assets | Yes | No |
| 11 | Accounts payable | 317348 | current_liabilities | accounts_payable | No | Yes |
| 12 | Accrued liabilities and other | 396423 | current_liabilities | other_current_liabilities | No | No |
| 13 | Accrued compensation and related expenses | 174702 | current_liabilities | accrued_compensation | No | Yes |
| 14 | Current lease liabilities | 278067 | current_liabilities | current_lease_liabilities | No | Yes |
| 15 | Current income taxes payable | 19231 | current_liabilities | current_income_taxes_payable | No | Yes |
| 16 | Unredeemed gift card liability | 250754 | current_liabilities | current_deferred_revenue | No | Yes |
| 17 | Other current liabilities | 32126 | current_liabilities | other_current_liabilities | No | No |
| 18 | Total current liabilities | 1468651 | current_liabilities | total_current_liabilities | Yes | No |
| 19 | Non-current lease liabilities | 1180823 | noncurrent_liabilities | long_term_lease_liabilities | No | Yes |
| 20 | Deferred income tax liability | 28876 | noncurrent_liabilities | deferred_tax_liabilities | No | Yes |
| 21 | Other non-current liabilities | 34140 | noncurrent_liabilities | other_noncurrent_liabilities | No | No |
| 22 | Stockholders' equity | 4031645 | equity | total_equity | Yes | No |
| 23 | Total liabilities and stockholders' equity | 6744135 | equity | total_liabilities_and_equity | Yes | No |

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
| 1 | Net revenue | 2371078 | revenue | No | Yes | No |
| 2 | Costs of goods sold | -958893 | cost_of_revenue | No | Yes | Yes |
| 3 | Gross profit | 1412185 | gross_profit | Yes | Yes | No |
| 4 | Selling, general and administrative expenses | -871959 | sales_general_and_administrative_expense | No | Yes | Yes |
| 5 | Amortization of intangible assets | 0 | amortization_acquired | No | No | Yes |
| 6 | Income from operations | 540226 | operating_income | Yes | Yes | No |
| 7 | Other income (expense), net | 17994 | other_income_expense_net | No | No | No |
| 8 | Income before income tax expense | 558220 | income_before_taxes | Yes | No | No |
| 9 | Income tax expense | -165298 | income_tax_provision | No | Yes | Yes |
| 10 | Net income | 392922 | net_income | Yes | No | No |

---
## Shares Outstanding
| Field | Value |
| --- | --- |
| Basic Shares Outstanding | 124721 |
| Basic Unit | thousands |
| Diluted Shares Outstanding | 124857 |
| Diluted Unit | thousands |
| Extraction Date | 2026-03-25 |

---
## Organic Growth
| Field | Value |
| --- | --- |
| Current Revenue | 2371078 |
| Current Revenue Unit | thousands |
| Prior Year Revenue | 2209165 |
| Prior Year Revenue Unit | thousands |
| Simple Growth (%) | 7.33 |
| Organic Growth (%) | 8.0 |
| **Final Growth (%)** | **8.0** |
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
| Starting Value | 540226.0 |
| EBITA | 540226.0 |
| EBITA Margin | 22.78% |
| Calculation Date | 2026-03-25 |



---

## Invested Capital

| Field | Value |
|-------|-------|
| Net Working Capital | 921530.0 |
| Net Long-Term Operating Assets | 1938767.0 |
| Invested Capital | 2860297.0 |
| Capital Turnover | 3.32x |
| Calculation Date | 2026-03-25 |

### Net Working Capital Breakdown

| Component | Items | Total |
|-----------|-------|-------|
| Operating Current Assets | Inventories, Prepaid and receivable income taxes, Other current assets | 1961632.0 |
| Operating Current Liabilities | Accounts payable, Accrued compensation and related expenses, Current lease liabilities, Current income taxes payable, Unredeemed gift card liability | 1040102.0 |
| **Net Working Capital** | | **921530.0** |

### Net Long-Term Operating Assets Breakdown

| Component | Items | Total |
|-----------|-------|-------|
| Operating Noncurrent Assets | Property and equipment, net, Right-of-use lease assets, Deferred income taxes and other non-current assets | 3148466.0 |
| Operating Noncurrent Liabilities | Non-current lease liabilities, Deferred income tax liability | 1209699.0 |
| **Net Long-Term Operating Assets** | | **1938767.0** |



---

## Tax Rates

| Field | Value |
|-------|-------|
| Income Before Taxes | 558220.0 |
| Income Tax Expense | -165298.0 |
| Net Income | 392922.0 |
| Effective Tax Rate | 29.61% |
| Adjusted Tax Rate | 30.60% |
| Calculation Date | 2026-03-25 |

### Adjusted Tax Rate Breakdown

| # | Line Name | Value | Tax Effect | Source | Marginal Rate |
|---|-----------|-------|------------|--------|---------------|
| | **Reported Tax** | **-165298.0** | | | |
| | **Total Tax Adjustment** | | **0.00** | | |
| | **Adjusted Tax** | **-165298.00** | | | |


---

## Financial Summary

| Metric | Value | Notes |
|--------|-------|-------|
| **Revenue** | 2371078.0 | |
| **EBITA** | 540226.0 | |
| **EBITA Margin** | 22.78% | |
| **Effective Tax Rate** | 29.61% | |
| **Adjusted Tax Rate** | 30.60% | |
| **NOPAT** | 374928.00 | Using Adjusted Tax Rate |
| **Net Working Capital** | 921530.0 | |
| **Net Long-Term Operating Assets** | 1938767.0 | |
| **Invested Capital** | 2860297.0 | |
| **Capital Turnover** | 3.32x | Annualized |
| **ROIC** | 52.43% | Annualized |
| **Interest Expense** | 0 | |
| **Basic Shares Outstanding** | 124721.0 | |
| **Diluted Shares Outstanding** | 124857.0 | |
| **Simple Revenue Growth** | 7.33% | YoY |
| **Organic Revenue Growth** | 8.00% | Constant currency |

### Calculation Notes

- Computed NOPAT automatically using EBITA x (1 - applicable tax rate)
- Annualization multiplier applied to NOPAT for ROIC calculation: 4x
