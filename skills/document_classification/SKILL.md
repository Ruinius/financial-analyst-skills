---
name: Document Classification
description: Classify financial PDFs by extracting company identity, document type, and date metadata. Validates ticker via Yahoo Finance with multi-step fallback.
---

# Document Classification Skill

This skill takes a PDF from `input_data/`, classifies it, extracts metadata, validates the company ticker, and produces a standardized markdown file in `processing_data/`.

## Prerequisites

- Python 3.10+ with `yfinance` installed (`pip install yfinance`) — used only for ticker validation
- PDFs placed in `input_data/` directory at the project root
- If a static file server is not running on localhost:8181 then ask the user to run `python -m http.server 8181 --bind 127.0.0.1`

**DO NOT EVER start servers without human user.**

## Inputs

- One or more PDF files in `input_data/`

## Outputs

- Renamed PDF in `processing_data/`: `TICKER_DOCTYPE_YYYYMMDD_temp.pdf`
- Markdown file in `processing_data/`: `TICKER_DOCTYPE_YYYYMMDD_temp.md`

---

## Step-by-Step Instructions

### Step 1: Pick a PDF to Process

1. List all `.pdf` files in `input_data/`
2. If no PDFs exist, stop and inform the user: "No PDFs found in input_data/"
3. Pick the first unprocessed PDF (i.e., one that does NOT already have a corresponding file in `processing_data/`)
4. Copy (not move yet) the PDF to `processing_data/` with its original name. We will rename it in Step 5.

### Step 2: Read the PDF

1. Ensure a background process running `python -m http.server 8181` is active in the project root.
2. Open the PDF in the browser using the `browser_subagent` tool:
   - Navigate to the PDF via the local server, e.g., `http://localhost:8181/processing_data/{filename}`
   - The browser renders PDFs natively with full visual fidelity
2. Read the first 1–3 pages to extract classification metadata (company name, ticker, document type, dates)
3. For large documents (10-K, 10-Q, analyst reports), you do NOT need to read every page — focus on the cover page and table of contents
4. Do NOT use PyPDF2 or other text extraction libraries — the browser approach preserves table layouts and handles scanned/image-based documents
5. If the PDF cannot be opened in the browser, stop and inform the user

### Step 3: Classify the Document

From the PDF content read in Step 2, extract the following fields:

**Fields to extract:**
| Field | Format | Description |
|-------|--------|-------------|
| `document_type` | string | One of: `earnings_announcement`, `quarterly_filing`, `annual_filing`, `press_release`, `analyst_report`, `news_article`, `transcript`, `other` |
| `company_name` | string or null | Company name as found in the document |
| `ticker` | string or null | Stock ticker symbol (uppercase, 1-5 chars) |
| `confidence` | string | One of: `high`, `medium`, `low` |

**Classification Rules:**
- `earnings_announcement`: Press releases reporting quarterly/annual earnings, revenue, EPS, net income
- `press_release`: All OTHER press releases (product launches, partnerships, executive changes, etc.)
- `quarterly_filing`: SEC 10-Q forms
- `annual_filing`: SEC 10-K forms
- `analyst_report`: Reports from research firms
- `transcript`: Earnings call transcripts
- When in doubt between `earnings_announcement` and `press_release`, choose `earnings_announcement` if the document primarily focuses on financial results

**Anti-hallucination rules:**
- ONLY extract information EXPLICITLY shown in the document text
- DO NOT invent, infer, or assume company names, tickers, or dates
- If information is not visible, use null
- DO NOT use external knowledge to fill in missing information at this step

### Step 4: Extract Dates

Extract each date field carefully, paying close attention to the document context:

#### 4a: Extract `document_date`
- The date the document was published or released
- Usually found on the first page, often near a location (e.g., "CUPERTINO, Calif., January 29, 2026")
- Format: `YYYY-MM-DD`
- Likely the most recent date mentioned in the document (unless it refers to a future event)

#### 4b: Extract `time_period`
- The fiscal reporting period
- Format: `Q1 YYYY`, `Q2 YYYY`, `Q3 YYYY`, `Q4 YYYY`, or `FY YYYY`
- Key hints: "six months" → Q2, "nine months" → Q3, "twelve months" or "annual" → FY/Q4
- Do NOT assume calendar year = fiscal year

#### 4c: Extract `period_end_date`
- The date the financial period ended (quarter end or fiscal year end)
- Format: `YYYY-MM-DD`
- Often found in phrases like "quarter ended March 31, 2024" or in financial table column headers
- Usually 15-60 days BEFORE `document_date`

### Step 5: Validate Dates

Cross-validate the three date fields together:

**Validation rules:**
1. `document_date` and `period_end_date` CANNOT be the same date
2. `period_end_date` is usually 15-60 days BEFORE `document_date`
3. `time_period` must match `period_end_date` logically (e.g., Q1 → March 31, Q2 → June 30, etc.)
4. For FY or Q4, look for keywords like "twelve months" in the document

If any field fails validation, correct it. If it cannot be corrected with confidence, set to null.

### Step 6: Validate Ticker via Yahoo Finance

**This is the multi-step fallback chain:**

#### 6a: If ticker was found in Step 3
1. Run `scripts/validate_ticker.py` with the extracted ticker
2. If Yahoo Finance returns a valid company name:
   - Compare the Yahoo name with the extracted `company_name`
   - If they match (even loosely — e.g., "Apple" vs "Apple Inc."), the ticker is confirmed. Use Yahoo's name as the final `company_name`.
   - If they DON'T match, proceed to 6c (reflection)
3. If Yahoo Finance returns nothing, proceed to 6c (reflection)

#### 6b: If NO ticker was found in Step 3
1. Skip to 6c (reflection)

#### 6c: Reflection — Use LLM Knowledge
1. Ask the LLM: "Given this company name and document context, what is the correct stock ticker?"
2. The LLM IS allowed to use its knowledge here (unlike Step 3)
3. If a ticker is found, validate it via Yahoo Finance again (run `scripts/validate_ticker.py`)
4. If Yahoo Finance confirms, use it
5. If Yahoo Finance still fails, **ask the human user** for the correct ticker

### Step 7: Apply Post-Processing Rules

**Document type ↔ time period corrections:**
- If `document_type` is `earnings_announcement` AND `time_period` is `FY YYYY` → change to `Q4 YYYY`
  (Earnings announcements report quarterly results; annual results are reported as Q4)
- If `document_type` is `annual_filing` AND `time_period` is `Q4 YYYY` → change to `FY YYYY`
  (10-K filings cover the full fiscal year)

### Step 8: Rename Files and Create Output

1. Build the standardized filename:
   - Format: `TICKER_DOCTYPE_YYYYMMDD_temp`
   - Example: `AAPL_10Q_20260129_temp`
   - `DOCTYPE` mapping:
     - `earnings_announcement` → `EA`
     - `quarterly_filing` → `10Q`
     - `annual_filing` → `10K`
     - `press_release` → `PR`
     - `analyst_report` → `AR`
     - `transcript` → `TR`
     - `other` → `OTH`
   - `YYYYMMDD` comes from `document_date`

2. Rename the PDF in `processing_data/` to `TICKER_DOCTYPE_YYYYMMDD_temp.pdf`

3. Delete the original PDF from `input_data/`

4. Create the markdown file `TICKER_DOCTYPE_YYYYMMDD_temp.md` in `processing_data/` with the following structure:

```markdown
# Document Classification

| Field | Value |
|-------|-------|
| Company Name | {company_name} |
| Ticker | {ticker} |
| Document Type | {document_type} |
| Document Date | {document_date} |
| Time Period | {time_period} |
| Period End Date | {period_end_date} |
| Confidence | {confidence} |
| Original Filename | {original_filename} |
| Classification Date | {current_date_iso} |

---

<!-- Sections below will be populated by subsequent skills -->
```

---

## Error Handling

- If PDF cannot be opened in the browser → Inform user, skip this PDF
- If classification fails → Retry once, then inform user
- If ticker validation completely fails → Ask human user for the correct ticker
- If date extraction fails → Set failed fields to null, proceed with available data

---

## Reference

This skill is based on `tiger-cafe\app\app_agents\document_classifier.py` which implements:
- 8-step classification pipeline
- Reflection pattern for ticker validation
- Granular date extraction with separate LLM calls per field
- Yahoo Finance identity resolution with LLM fallback
- Document type ↔ time period correction rules
