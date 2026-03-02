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

### Skill Decomposition

| Skill | Pipeline Steps | Description |
|-------|---------------|-------------|
| **1. Document Classification** | Steps 2–6 | PDF → metadata extraction, ticker validation, file naming |
| **2. Financial Data Extraction** | Steps 7–12 | 5 sub-skills: Balance Sheet, Income Statement, Shares, Growth, GAAP |
| **3. Financial Calculations** | Steps 13–16 | Pure math: EBITA, Tax, Invested Capital, Summary |
| **4. Document Organization** | Steps 17–20 | File moves, metadata, cross-document date healing |
| **5. Financial Modeling** | Step 21 | DCF model (placeholder) |

### Pipeline Flow

Human step: Drop PDFs in `input_data/`

**Skill 1: Document Classification**
- Move PDF from `input_data/` → `processing_data/`
- Read PDF and extract: company TICKER, company name, document type, document_date, fiscal quarter, period_end_date
- Validate ticker via Yahoo Finance (with reflection fallback, then human fallback)
- Rename PDF to standard format: `TICKER_DOCTYPE_YYYYMMDD_temp.pdf`
- Create initial markdown: `TICKER_DOCTYPE_YYYYMMDD_temp.md`

**Skill 2: Financial Data Extraction**
- Create/update `processing_data.md` with progress tracking table
- Sub-skill 2a: Balance Sheet extraction → standardize with tiger-transformer + CSV mappings
- Sub-skill 2b: Income Statement extraction → standardize + sign normalization
- Sub-skill 2c: Shares Outstanding extraction
- Sub-skill 2d: Organic Growth calculation + organic/currency-constant growth search
- Sub-skill 2e: GAAP Reconciliation extraction

**Skill 3: Financial Calculations**
- Sub-skill 3a: EBITA calculation
- Sub-skill 3b: Tax rate calculation (simple + operating)
- Sub-skill 3c: Invested Capital (NWC + long-term capital)
- Sub-skill 3d: Summary table

**Skill 4: Document Organization**
- Move processed files to `output_data/TICKER/`
- Create/update `TICKER_metadata.md`
- Cross-document date healing

**Skill 5: Financial Modeling (Placeholder)**
- DCF model using historical data + assumptions

---

## Build Order

Each phase should be fully tested before moving to the next.

| Phase | Skill | Complexity | Dependencies |
|-------|-------|-----------|-------------|
| **1** | Document Classification | Medium | Yahoo Finance, LLM |
| **2a** | Balance Sheet Extraction | High | Tiger-Transformer, CSV mappings |
| **2b** | Income Statement Extraction | High | Tiger-Transformer, CSV mappings |
| **2c** | Shares Outstanding | Low | LLM only |
| **2d** | Organic Growth | Medium | LLM only |
| **2e** | GAAP Reconciliation | High | LLM only |
| **3** | Financial Calculations | Low | Pure math, no external deps |
| **4** | Document Organization | Low | File system only |
| **5** | Financial Modeling | Medium | Pure math |

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
| Financial Modeling | `app/utils/financial_modeling.py` |
| Summary Table UI | `frontend/src/components/views/document/DocumentExtractionView.jsx` |

---

## Key Difference: Tiger-Cafe vs. Tiger-Skills

| Aspect | Tiger-Cafe | Tiger-Skills |
|--------|-----------|-------------|
| Architecture | Full-stack web app (FastAPI + React + SQLite) | Flat file system + AI skills |
| Storage | SQL database with ORM models | Markdown files + PDFs in folders |
| Orchestration | Python code (`extraction_orchestrator.py`) | `SKILL.md` instructions for AI |
| Progress Tracking | Database milestones + WebSocket events | `processing_data.md` table |
| Transformer | In-process Python (PyTorch model) | Local FastAPI Server (`scripts/tiger_transformer_server.py`) |

---

## Local Services

To keep skills fast and modular, heavy computational tasks (like ML model inference) are handled by local background services.

| Service | Script | Endpoint | Description |
|---------|--------|----------|-------------|
| **Tiger-Transformer** | `scripts/tiger_transformer_server.py` | `http://localhost:8000` | Loads the fine-tuned FINBERT model for line item standardization. |

To start all required services, run: `scripts/start_transformer.bat`
| User Interface | React frontend | Human reads markdown output |

The biggest mental shift: In tiger-cafe, you wrote **code** that does things. In tiger-skills, you write **instructions** that tell the AI how to do things. The AI _is_ the runtime.