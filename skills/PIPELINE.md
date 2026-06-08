---
name: Skills Orchestrator Pipeline
description: A runbook for reasoning models to execute the complete financial-analyst-skills pipeline in the correct dependency order. Routes documents through different skill chains based on document type.
---

# 🚀 Financial-Analyst-Skills Full Pipeline Runbook

This runbook guides reasoning models through the end-to-end execution of the financial-analyst-skills pipeline. Documents are routed through different skill chains depending on their type.

## Prerequisites

Before starting the pipeline, ensure:

1. PDFs are present in the `input_data/` directory.
2. If Tiger-Transformer is not running on localhost:8000 then ask the user to run `.\tools\start_transformer.bat`
3. If a static file server is not running on localhost:8181 then ask the user to run `.\tools\start_file_server.bat`

**DO NOT EVER start servers without human user.**

---

## 📋 Pipeline Overview

Every document starts with **Phase 1 (Classification)**. After that, the pipeline branches based on document type:

```
                        ┌─ Financial Report ─► Phase 2 → Phase 3 → Phase 4
Phase 1 (Classify) ─────┤
                        └─ Qualitative Doc ──► Phase 5
```

- **Financial reports** (earnings_announcement, quarterly_filing, annual_filing): Phases 1 → 2 → 3 → 4
- **Qualitative documents** (analyst_report, transcript, press_release): Phases 1 → 5

> 💡 **Note:** `earnings_announcement` documents often contain significant qualitative commentary and forward-looking guidance. If an EA is the only document available for a ticker, it should also be routed through **Phase 5** to ensure the financial model (Phase 6) has qualitative inputs.

After all documents are processed, the **company-level skills** can run:

- **Phase 6**: Financial Modeling (requires historical data from Phase 4 + qualitative assessments from Phase 5)
- **Phase 7**: Model JSON Generator (formats the metadata into structured JSON for frontend)

---

## Phase 1: Document Classification

**Skill Reference:** `skills/document_classification/SKILL.md`

Run this for EVERY document regardless of type.

1. Pick a single unprocessed PDF from `input_data/`.
2. Extract high-level metadata: ticker, company name, document type, and dates.
3. Validate the ticker.
4. Copy and rename the PDF into `processing_data/TICKER_DOCTYPE_YYYYMMDD_temp.pdf`.
5. Create the initial markdown file `processing_data/TICKER_DOCTYPE_YYYYMMDD_temp.md`.
6. **Route the document** based on `document_type`:
   - `earnings_announcement`, `quarterly_filing`, `annual_filing` → Continue to **Phase 2**
   - `analyst_report`, `transcript`, `press_release` → Skip to **Phase 5**

---

## Phases 2–4: Financial Report Pipeline

For documents classified as financial reports (earnings announcements, 10-Qs, 10-Ks).

### Phase 2: Financial Data Extraction

**Skill Reference:** `skills/financial_data_extraction/SKILL.md`

Extract all financial statement components (Balance Sheet, Income Statement, Shares Outstanding, Organic Growth, and GAAP Reconciliation) and append them to the markdown file created in Phase 1.

The consolidated skill handles the full extraction workflow: single-pass PDF reading, raw data extraction, transformer standardization, and markdown output via the `transform_and_append.py` script.

### Phase 3: Financial Calculations

Execute the deterministic Python wrapper script to compute derived financial metrics from the Phase 2 data:

**Skill Reference:** `skills/financial_calculations/SKILL.md`

### ⛔ Data Quality Gate (between Phase 3 and Phase 4)

Before proceeding to Phase 4, verify the Summary Table output passes ALL of these checks:

| #   | Check                                  | If Failed                                                           |
| --- | -------------------------------------- | ------------------------------------------------------------------- |
| 1   | Revenue > 0                            | ↩️ Re-run Phase 2 Income Statement — revenue line was not captured  |
| 2   | Tax Rate ≠ 0%                          | ↩️ Re-run Phase 2 IS (missing tax line) then Phase 3 Tax            |
| 3   | Invested Capital ≠ 0 and is reasonable | ↩️ Re-run Phase 2 Balance Sheet — incomplete extraction             |
| 4   | ROIC between -50% and 200%             | ↩️ Check IC and NOPAT — likely incomplete BS                        |
| 5   | Growth ≠ N/A                           | ↩️ Re-run Phase 2 Organic Growth — prior year revenue not extracted |
| 6   | Growth ≠ 0.0%                          | ⚠️ Double-check — statistically implausible                         |

**Do NOT proceed to Phase 4 with failing checks.** Re-run the failing upstream skill, then re-run Phase 3 Summary Table.

### Phase 4: Document Organization

**Skill Reference:** `skills/document_organization/SKILL.md`

Finalize the document and integrate it into the long-term storage.

1. Harmonize units across all extracted statements in the markdown document.
2. Initialize or update the master `output_data/TICKER/TICKER_metadata.md` file with the newly calculated history.
3. Perform cross-document date healing if inconsistencies are found with historical data.
4. Move the finished PDF and markdown out of `processing_data/` and into `output_data/TICKER/` (removing the `_temp` suffix).
5. Ensure the original PDF is deleted from `input_data/`.

---

## Phase 5: Qualitative Assessment

**Skill Reference:** `skills/qualitative_assessment/SKILL.md`

For documents classified as analyst reports, transcripts, or press releases. The ticker's `output_data/TICKER/` directory must already exist (i.e., at least one financial report has been processed for this company).

1. Read the classified document from `processing_data/`.
2. Assess the **economic moat** (Wide / Narrow / None) with three bullets of rationale and a confidence level. Compare with any existing assessment in `TICKER_metadata.md` and harmonize.
3. Assess the **EBITA margin trajectory** (expand or shrink by 1–2 percentage points) with three bullets of rationale and a confidence level. Compare with any existing assessment and harmonize.
4. Assess the **organic growth trajectory** (increase or decrease by 1–2 percentage points) with three bullets of rationale and a confidence level. Compare with any existing assessment and harmonize.
5. Update `output_data/TICKER/TICKER_metadata.md` with the assessments.
6. Move the finished PDF and markdown to `output_data/TICKER/` (removing the `_temp` suffix).

---

## Phase 6: Financial Modeling

**Skill Reference:** `skills/financial_modeling/SKILL.md`

This is a **company-level** deterministic Python script. It runs once per ticker after sufficient historical data and qualitative assessments are available. The script executes the complete sequence in a single pass: WACC → Assumptions → DCF → Intrinsic Value.

1. Execute the script: `python skills/financial_modeling/scripts/calculate.py {TICKER} output_data/{TICKER}/{TICKER}_metadata.md`
2. Verify it threw no errors.

---

## Phase 7: Model JSON Generator

**Skill Reference:** `skills/model_json_generator/SKILL.md`

This skill parses the completely generated metadata markdown file and converts the financial model tables into a clean JSON output for the frontend interactive viewer.

1. Execute the script: `python skills/model_json_generator/scripts/generate_json.py {TICKER} output_data/{TICKER}/{TICKER}_metadata.md`
2. Verify it successfully output the `TICKER_financial_model.json` file.

---

## 🔁 Batch Execution Loop

If given a task to "execute the pipeline on all PDFs in `input_data`", follow this loop:

```text
WHILE PDFs remain in input_data/:
  1. PDF = Pick first PDF in input_data/
  2. Execute Phase 1 (Classification)
  3. IF document_type is financial report (EA, 10Q, 10K):
       Execute Phase 2 (Extraction)
       Execute Phase 3 (Calculations)
       Execute Phase 4 (Organization)
  4. ELSE IF document_type is qualitative (analyst_report, transcript, press_release) OR is an EA being used for qualitative insights:
       Execute Phase 5 (Qualitative Assessment)
  5. Confirm PDF is successfully moved to output_data/. Proceed to next.

AFTER all documents processed:
  FOR EACH ticker with sufficient data:
    Execute Phase 6 (Financial Modeling)
    Execute Phase 7 (Model JSON Generator)
```


---

## 🏁 Post-Pipeline Epilogue (Example Curation & Self-Improvement)

To save tokens and time during execution, do not curate examples or run self-improvement after every individual skill. Instead, run them here at the end of the full pipeline for ALL skills you executed during this run.

For each skill executed during this pipeline run:
1. Locate its output and save it as a new `TICKER_example.md` in that skill's `examples/` directory.
2. Review all examples in that `examples/` directory and keep only the single best one (delete the rest).
3. If you found any edge cases or ambiguities during the skill's execution, propose improvements and log them in that skill's `SKILL.md` file.

(See `skills/SHARED_POSTRUN.md` for the exact rules of example curation and self-improvement.)