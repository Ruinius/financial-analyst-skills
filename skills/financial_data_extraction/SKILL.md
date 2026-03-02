---
name: Financial Data Extraction
description: Extract structured financial data from classified PDFs. Contains 5 sub-skills for balance sheet, income statement, shares outstanding, organic growth, and GAAP reconciliation.
---

# Financial Data Extraction Skill

This skill reads a classified PDF from `processing_data/` and extracts structured financial data, appending results to the document's markdown file.

## Prerequisites

- Skill 1 (Document Classification) must have been run first
- Tiger-Transformer server running at `http://localhost:8000` (needed for balance sheet and income statement standardization)
  - Start with: `.\tools\start_transformer.bat`

## Inputs

- A classified PDF and its corresponding `.md` file in `processing_data/`
  - Example: `ADBE_EA_20250312_temp.pdf` + `ADBE_EA_20250312_temp.md`

## Outputs

- Updated markdown file with extracted financial data appended as new sections

## Sub-Skills

This skill contains 5 sub-skills that should be run in order:

| Sub-Skill | Folder | Description | Depends On |
|-----------|--------|-------------|------------|
| **2a. Balance Sheet** | `balance_sheet/` | Extract balance sheet line items, standardize via transformer | Classification |
| **2b. Income Statement** | `income_statement/` | Extract income statement, standardize, normalize signs | Classification |
| **2c. Shares Outstanding** | `shares_outstanding/` | Extract basic and diluted share counts | Classification |
| **2d. Organic Growth** | `organic_growth/` | Extract organic/constant-currency growth and prior-year revenue | Income Statement |
| **2e. GAAP Reconciliation** | `gaap_reconciliation/` | Extract GAAP-to-non-GAAP operating income reconciliation | Classification |

### Execution Order

1. Read the classification metadata from the `.md` file (ticker, document_type, time_period, period_end_date)
2. Read the PDF directly using multimodal capabilities
3. Run sub-skills **2a** and **2b** first (they are independent of each other)
4. Run **2c** (can run in parallel with 2a/2b)
5. Run **2d** after **2b** (needs income statement revenue data)
6. Run **2e**

### Output Format

Each sub-skill appends a section to the markdown file. See individual sub-skill SKILL.md files for exact output formats.

### Currency and Unit Policy

- **Currency**: Always extract in the **document's local (functional) currency** — do NOT use USD convenience translations.
- **ADR handling**: Foreign companies listed in the US (ADRs) often present financial statements in both their local currency AND a USD translation side by side. **Always use the local currency column** (e.g., RMB for BABA, TWD for TSM, EUR for SAP). The USD column is a convenience translation and should be ignored.
- **How to identify local vs USD**: The local currency column is typically labeled as the primary/functional currency, appears first, or is in the document's stated reporting currency. Look for headers like "RMB", "¥", "€", or the company's domicile currency.
- **Unit**: Extract the unit exactly as stated in the document (e.g., "In millions", "百万円", "In thousands"). Each section records its own unit.
- **Unit harmonization** happens later in Skill 4 (Document Organization), not during extraction.

---

## Reference

Based on the following tiger-cafe source files:
- `app/app_agents/balance_sheet_extractor.py` (869 lines)
- `app/app_agents/income_statement_extractor.py` (830 lines)
- `app/app_agents/shares_outstanding_extractor.py` (277 lines)
- `app/app_agents/organic_growth_extractor.py` (510 lines)
- `app/app_agents/gaap_reconciliation_extractor.py` (778 lines)
- `app/app_agents/extractor_utils.py` (193 lines)
