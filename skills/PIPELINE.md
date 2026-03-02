---
name: Skills Orchestrator Pipeline
description: A runbook for reasoning models to execute the complete tiger-skills pipeline in the correct dependency order.
---

# 🚀 Tiger-Skills Full Pipeline Runbook

This runbook guides reasoning models through the end-to-end execution of the tiger-skills pipeline. The goal of this pipeline is to process raw financial PDFs from `input_data/`, extract structured financial data using various specialized sub-skills, calculate key financial metrics, and finally organize the completed work into `output_data/`.

## Prerequisites

Before starting the pipeline, ensure:
1. PDFs are present in the `input_data/` directory.
2. The Tiger-Transformer server is running in the background (start via `tools/start_transformer.bat`), as it is required by the extraction skills.

---

## 📋 The Pipeline Execution Order

The pipeline is designed to process **one document from start to finish (Phases 1-4)** before moving on to the next document. Do NOT run Phase 1 on all documents before moving to Phase 2.

For a single PDF, follow these steps in strict sequence:

### Phase 1: Document Classification
**Skill Reference:** `skills/document_classification/SKILL.md`
1. Pick a single unprocessed PDF from `input_data/`.
2. Extract high-level metadata: ticker, company name, document type, and dates.
3. Validate the ticker.
4. Copy and rename the PDF into `processing_data/TICKER_DOCTYPE_YYYYMMDD_temp.pdf`.
5. Create the initial markdown file `processing_data/TICKER_DOCTYPE_YYYYMMDD_temp.md`.

### Phase 2: Financial Data Extraction
**Skill Reference:** `skills/financial_data_extraction/SKILL.md`
Extract specific components of the financial statements and append them to the markdown file created in Phase 1. Follow this sub-skill order:
1. **2a. Balance Sheet** (`balance_sheet/`) & **2b. Income Statement** (`income_statement/`) — *These are independent and can be run first.*
2. **2c. Shares Outstanding** (`shares_outstanding/`) — *Can be run in parallel with 2a/2b.*
3. **2d. Organic Growth** (`organic_growth/`) — *DEPENDS ON: 2b Income Statement.*
4. **2e. GAAP Reconciliation** (`gaap_reconciliation/`) — *Extracts non-GAAP adjustments.*

### Phase 3: Financial Calculations
**Skill Reference:** `skills/financial_calculations/SKILL.md`
Compute derived financial metrics using purely arithmetic operations on the data extracted in Phase 2. Follow this order:
1. **3a. EBITA** (`ebita/`) & **3c. Invested Capital** (`invested_capital/`) — *These are independent and can be run first.*
2. **3b. Tax Rates** (`tax/`) — *DEPENDS ON: 3a EBITA.*
3. **3d. Summary Table** (`summary_table/`) — *DEPENDS ON: All prior calculations.*

### Phase 4: Document Organization
**Skill Reference:** `skills/document_organization/SKILL.md`
Finalize the document and integrate it into the long-term storage.
1. Harmonize units across all extracted statements in the markdown document.
2. Initialize or update the master `output_data/TICKER/TICKER_metadata.md` file with the newly calculated history.
3. Perform cross-document date healing if inconsistencies are found with historical data.
4. Move the finished PDF and markdown out of `processing_data/` and into `output_data/TICKER/` (removing the `_temp` suffix).
5. Ensure the original PDF is deleted from `input_data/`.

---

## 🔁 Batch Execution Loop

If given a task to "execute skills on all PDFs in `input_data`", follow this loop:

```text
WHILE PDFs remain in input_data/:
  1. PDF = Pick first PDF in input_data/
  2. Execute Phase 1 (Classification)
  3. Execute Phase 2 (Extraction Sub-skills 2a -> 2e)
  4. Execute Phase 3 (Calculations Sub-skills 3a -> 3d)
  5. Execute Phase 4 (Organization & Cleanup)
  6. Confirm PDF is successfully moved to output_data/. Proceed to next.
```
