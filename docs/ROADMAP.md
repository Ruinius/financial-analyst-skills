# Tiger-Skills Roadmap & Architecture Plan

> **Goal**: Port the tiger-cafe agentic pipeline into modular, reusable Antigravity Skills that can be built, tested, and composed independently.

## What Are Antigravity Skills?

Skills are a first-class extension mechanism in Antigravity. Each skill is a **folder** containing:

| File/Dir | Required | Purpose |
|----------|----------|---------|
| `SKILL.md` | Yes | Main instruction file with YAML frontmatter (`name`, `description`) and detailed markdown instructions. This is what the AI reads to know how to execute the skill. |
| `scripts/` | Optional | Helper scripts (Python, shell, etc.) that the AI can invoke |
| `examples/` | Optional | Reference inputs/outputs for the AI to learn from |
| `resources/` | Optional | Templates, CSV mappings, config files |

### How Skills Work

1. You (or the AI) place skill folders in `skills/`
2. When a task matches a skill's description, the AI reads `SKILL.md` for instructions
3. The AI follows those instructions step-by-step, using the scripts/resources in the skill folder
4. Skills can reference other skills, creating composable pipelines

Each `SKILL.md` is essentially a **detailed recipe** for the AI. The more specific and structured your instructions are, the more reliably the AI will execute them. Think of it like writing a runbook for a junior analyst.

---

## Pipeline Overview

Human step: Drop PDFs in `input_data/`

**Skill: Document Classification**
- Move PDF from `input_data/` → `processing_data/`
- Read PDF and extract: company TICKER, company name, document type, document_date, fiscal quarter, period_end_date
- Validate ticker via Yahoo Finance (with reflection fallback, then human fallback)
- Rename PDF to standard format: `TICKER_DOCTYPE_YYYYMMDD_temp.pdf`
- Create initial markdown: `TICKER_DOCTYPE_YYYYMMDD_temp.md`

**Skill: Financial Data Extraction** (for Earnings Announcement, 10K, 10Q, or equivalent financial reports)
- Sub-skill: Balance Sheet extraction → standardize with tiger-transformer + CSV mappings
- Sub-skill: Income Statement extraction → standardize + sign normalization
- Sub-skill: Shares Outstanding extraction
- Sub-skill: Organic Growth calculation + organic/currency-constant growth search
- Sub-skill: GAAP Reconciliation extraction

**Skill: Financial Calculations** (for Earnings Announcement, 10K, 10Q, or equivalent financial reports)
- Sub-skill: EBITA calculation
- Sub-skill: Tax rate calculation (simple + operating)
- Sub-skill: Invested Capital (NWC + long-term capital)
- Sub-skill: Summary table

**Skill: Document Organization**
- Move processed files to `output_data/TICKER/`
- Create/update `TICKER_metadata.md`
- Cross-document date healing

**Skill: Qualitative Assessment** (for Analyst Reports, Transcripts, and Long Form Articles)
- Sub-skill: Determine whether the economic moat is Wide, Narrow, or None based on Morningstar-like rating and provide three bullets of rationale. Give a confidence level. Compare, harmonize, update content in `TICKER_metadata.md`
- Sub-skill: Determine whether the EBITA margin will expand or shrink by 1 or 2 percentage points and provide three bullets of rationale. Give a confidence level. Compare, harmonize, update content in `TICKER_metadata.md`
- Sub-skill: Determine whether the organic growth rate will increase or decrease by 1 or 2 percentage points and provide three bullets of rationale. Give a confidence level. Compare, harmonize, update content in `TICKER_metadata.md`

**Skill: Financial Modeling**
- Sub-skill: Calculate WACC using CAPM model to `TICKER_metadata.md`
- Sub-skill: Create all the assumptions using a combination of historical and output from qualitative assessment to `TICKER_metadata.md`
- Sub-skill: Populate the full DCF model to `TICKER_metadata.md`
- Sub-skill: Populate the translation from DCF value to intrinsic value per share to `TICKER_metadata.md`
- Sub-skill: Create and update `output_data/TICKER/TICKER_financial_model.json`

**Frontend: Zero dependency interactive HTML** (one-time build)
- Create a zero-dependency interactive HTML DCF viewer as a reusable template
- Lives in `tools/financial_model_viewer.html`
- Served via lightweight custom Python server `tools/serve.py` (static file serving + scenario save endpoint)
- Reads data from `output_data/TICKER/TICKER_financial_model.json` via URL param (e.g., `?ticker=ADBE`)
- Financial Modeling skill outputs the JSON; the viewer is static
- **Interactive recalculation**: Editable assumption inputs (revenue growth, EBITA margin, WACC, terminal growth, tax rate) trigger instant DCF recalculation in vanilla JS
- **Reset to defaults**: Button restores all assumptions to the AI-generated values from the JSON
- **Scenario saving**: Save named snapshots of assumptions + calculated intrinsic value to `output_data/TICKER/TICKER_scenarios.json` via POST endpoint — git-trackable, portable, lives alongside the data
- See `tiger-cafe/frontend/src/components/views/company/FinancialModel.jsx` for reference

---

## Tiger-Cafe References

| Skill | Tiger-Cafe Reference File |
|-------|--------------------------|
| Document Classification | `app/app_agents/document_classifier.py` |
| Balance Sheet | `app/app_agents/balance_sheet_extractor.py` |
| Income Statement | `app/app_agents/income_statement_extractor.py` |
| Shares Outstanding | `app/app_agents/shares_outstanding_extractor.py` |
| Organic Growth | `app/app_agents/organic_growth_extractor.py` |
| GAAP Reconciliation | `app/app_agents/gaap_reconciliation_extractor.py` |
| Tiger-Transformer Client | `app/services/tiger_transformer_client.py` |
| Extraction Orchestrator | `app/services/extraction_orchestrator.py` |
| Historical Calculations | `app/utils/historical_calculations.py` |
| Timeline Service | `app/services/timeline_service.py` |
| Qualitative Assessment | `app/app_agents/qualitative_extractor.py` |
| Financial Modeling (WACC/DCF) | `app/utils/financial_modeling.py` |
| Financial Model UI (Frontend) | `frontend/src/components/views/company/FinancialModel.jsx` |
| Summary Table UI | `frontend/src/components/views/document/DocumentExtractionView.jsx` |

---

## Key Difference: Tiger-Cafe vs. Tiger-Skills

| Aspect | Tiger-Cafe | Tiger-Skills |
|--------|-----------|-------------|
| Architecture | Full-stack web app (FastAPI + React + SQLite) | Flat file system + AI skills |
| Storage | SQL database with ORM models | Markdown files + PDFs in folders |
| Orchestration | Python code (`extraction_orchestrator.py`) | `SKILL.md` instructions for AI |
| Progress Tracking | Database milestones + WebSocket events | Markdown sections in `processing_data/` |
| Transformer | In-process Python (PyTorch model) | Local FastAPI server (`tools/tiger_transformer_server.py`) |
| Qualitative Assessment | Not implemented | AI skill reading analyst reports/transcripts |
| Financial Model UI | React component (`FinancialModel.jsx`) | Zero-dependency HTML (`tools/financial_model_viewer.html`) |
| Scenario Persistence | SQLite database | JSON files in `output_data/TICKER/` |

---

## Local Services

To keep skills fast and modular, heavy computational tasks and file serving are handled by local services.

| Service | Script | Port | When to Run | Description |
|---------|--------|------|-------------|-------------|
| **Tiger-Transformer** | `tools/tiger_transformer_server.py` | `8000` | During document processing (Skills 1–3) | Loads the fine-tuned FINBERT model for line item standardization |
| **Frontend Server** | `tools/serve.py` | `8080` | When reviewing/modeling results | Static file server + scenario save endpoint for the DCF viewer |

**Starting services:**
- Processing: `tools/start_transformer.bat`
- Reviewing: `python tools/serve.py` → open `http://localhost:8080/tools/financial_model_viewer.html?ticker=ADBE`

---

The biggest mental shift: In tiger-cafe, you wrote **code** that does things. In tiger-skills, you write **instructions** that tell the AI how to do things. The AI _is_ the runtime.