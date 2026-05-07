---
name: Document Classification
description: Classify financial PDFs by extracting company identity, document type, and date metadata. Validates ticker via Yahoo Finance with multi-step fallback. Uses a Python orchestration script for validation, file modification, and writing markdown.
---

# Document Classification Skill

This skill takes a PDF from `input_data/`, classifies it, abstracts metadata, and uses an orchestration script to validate the company ticker and produce a standardized markdown file in `processing_data/`.

## Prerequisites

- Python 3.10+
- PDFs placed in `input_data/` directory at the project root
- If a static file server is not running on localhost:8181 then ask the user to run `.\tools\start_file_server.bat`

**DO NOT EVER start servers without human user.**

## Inputs

- One or more PDF files in `input_data/`

## Outputs

- Renamed PDF in `processing_data/`: `TICKER_DOCTYPE_YYYYMMDD_temp.pdf`
- Markdown file in `processing_data/`: `TICKER_DOCTYPE_YYYYMMDD_temp.md`

---

## Step-by-Step Instructions

> **Batch Mode:** Repeat Steps 1–6 for EVERY `.pdf` file in `input_data/`. Track which files have been processed and continue until all are done. Report a summary at the end.

### Step 1: Pick the Next PDF to Process

1. List all `.pdf` files in `input_data/`
2. If no PDFs exist (or all have already been processed), stop and inform the user: "No PDFs found in input_data/" or "All PDFs processed."
3. Pick the next unprocessed PDF in `input_data/`. Keep track of its filename.
4. Continue to Step 2 for this PDF.

### Step 2: Read the PDF

1. Ensure a background process running the file server is active (`.\tools\start_file_server.bat`).
2. Open the PDF in the browser using the `browser_subagent` tool:
   - Navigate to the PDF via the local server, e.g., `http://localhost:8181/input_data/{filename}`
   - The browser renders PDFs natively with full visual fidelity
3. Read the first 1–3 pages to extract classification metadata (company name, ticker, document type, dates)
4. For large documents (10-K, 10-Q, analyst reports), you do NOT need to read every page — focus on the cover page and table of contents
5. Do NOT use PyPDF2 or other text extraction libraries — the browser approach preserves table layouts and handles scanned/image-based documents
6. If the PDF cannot be opened in the browser, stop and inform the user

### Step 3: Classify the Document

From the PDF content read in Step 2, extract the following fields. Refer to `skills/document_classification/resources/document_types.json` for validation and exact naming of Document Types.

**Fields to extract:**
| Field | Format | Description |
|-------|--------|-------------|
| `document_type` | string | MUST strictly be one of the keys in `document_types.json` |
| `company_name` | string or null | Company name as found in the document |
| `ticker` | string or null | Stock ticker symbol (uppercase, 1-5 chars) |
| `confidence` | string | One of: `high`, `medium`, `low` |

**Anti-hallucination rules:**
- ONLY extract information EXPLICITLY shown in the document text
- DO NOT invent, infer, or assume company names, tickers, or dates
- If information is not visible, use null
- DO NOT use external knowledge to fill in missing information at this step

### Step 4: Extract Dates

Extract each date field carefully, paying close attention to the document context.

**Fiscal Year Awareness:** Before assigning `time_period`, check `skills/document_classification/resources/fiscal_year_map.json` to see if this company has a non-standard fiscal year. Many retail and tech companies (e.g., LULU, WMT, COST, NKE, BABA) have fiscal years ending in months other than December. This shifts which calendar months map to which fiscal quarters.

- If the ticker IS in the map, use the `fiscal_year_ends` entry to determine the correct fiscal quarter from the `period_end_date`.
- If the ticker is NOT in the map, assume a standard calendar fiscal year (ending December 31).

#### 4a: Extract `document_date`
- The date the document was published or released
- Format: `YYYY-MM-DD`

#### 4b: Extract `time_period`
- The fiscal reporting period
- Format: `Q1 YYYY`, `Q2 YYYY`, `Q3 YYYY`, `Q4 YYYY`, or `FY YYYY`
- **Important:** Use the company's fiscal calendar, not the calendar year. For example, LULU's fiscal year ends in January, so a period ending Jan 28, 2024 is Q4 FY2023, not Q1 2024.

#### 4c: Extract `period_end_date`
- The date the financial period ended (quarter end or fiscal year end)
- Format: `YYYY-MM-DD`

### Step 5: Execute Orchestration Script

Run the python orchestration script to validate and finalize the classification. This script will automatically validate the ticker against Yahoo Finance, rename strings according to document type abbreviations, move the file, and create the final markdown file. 

Execute the following terminal command with the correctly formatted strings from Steps 3 and 4:

```bash
uv run python skills\document_classification\scripts\process_classification.py --filename "FILENAME.pdf" --company_name "Extracted Company Name" --ticker "TICKER" --document_type "document_type" --document_date "YYYY-MM-DD" --time_period "time_period" --period_end_date "YYYY-MM-DD" --confidence "high"
```

If it succeeds, output the success to the user. If there are more PDFs remaining in `input_data/`, return to **Step 1** for the next file. Otherwise, print a final summary of all processed documents and finish the run.

> 💡 **First-File Scenario:** If the document is the first one being processed for a ticker (no `output_data/TICKER` exists), Phase 5 (Qualitative Assessment) will require you to manually initialize the ticker directory and `TICKER_metadata.md` file.

### Step 6: Reflection — Use LLM Knowledge (Fallback)

If the script in Step 5 throws an error (e.g. invalid ticker):
1. Ask the LLM: "Given this company name and document context, what is the correct stock ticker?"
2. The LLM IS allowed to use its knowledge here (unlike Step 3)
3. If a new ticker is found, re-run Step 5 with the new ticker.
4. If it still fails, **ask the human user** for the correct ticker.

---

## Error Handling

- If PDF cannot be opened in the browser → Inform user, skip this PDF
- If classification fails → Retry once, then inform user
- If ticker validation completely fails → Ask human user for the correct ticker
- If date extraction fails → Set failed fields to null, proceed with available data

## Changelog

- 2026-05-06: Updated example command to use `uv run` per project standards. Added note about first-file initialization for qualitative documents.
