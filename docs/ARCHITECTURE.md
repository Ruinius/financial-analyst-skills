# Tiger-Skills Architecture & System Design

This document describes the architectural principles and pipeline design of the Tiger-Skills project.

## What Are Antigravity Skills?

Skills are a first-class extension mechanism in Antigravity. Each skill is a **folder** containing:

| File/Dir     | Required | Purpose                                                                                                                                                             |
| ------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SKILL.md`   | Yes      | Main instruction file with YAML frontmatter (`name`, `description`) and detailed markdown instructions. This is what the AI reads to know how to execute the skill. |
| `scripts/`   | Optional | Helper scripts (Python, shell, etc.) that the AI can invoke                                                                                                         |
| `examples/`  | Optional | Reference inputs/outputs for the AI to learn from                                                                                                                   |
| `resources/` | Optional | Templates, config files                                                                                                                               |

### How Skills Work

1. You (or the AI) place skill folders in `skills/`
2. When a task matches a skill's description, the AI reads `SKILL.md` for instructions
3. The AI follows those instructions step-by-step, using the scripts/resources in the skill folder
4. Skills can reference other skills, creating composable pipelines

Each `SKILL.md` is essentially a **detailed recipe** for the AI. The AI _is_ the runtime. The skills are the program.

---

## Core Pipeline Design

The pipeline transforms raw PDFs into a structured valuation model via the following phases:

1. **Phase 1: Document Classification**
   - Move PDF from `input_data/` → `processing_data/`
   - Extract company TICKER, name, doc type, and dates.
   - Validate ticker via Yahoo Finance.

2. **Phase 2: Financial Data Extraction**
   - Standardize Balance Sheet, Income Statement, and GAAP reconciliations via Tiger-Transformer.
   - Extract shares outstanding and organic growth.

3. **Phase 3: Financial Calculations**
   - Deterministic script computes EBITA, Tax Rates, Invested Capital, NOPAT, and ROIC.

4. **Phase 4: Document Organization**
   - Consolidate all extractions into `output_data/TICKER/TICKER_metadata.md`.
   - Perform cross-document date healing.

5. **Phase 5: Qualitative Assessment**
   - Assess economic moat and future trajectory from analyst reports/transcripts.

6. **Phase 6: Financial Modeling**
   - Calculate WACC and generate 3-stage DCF assumptions.
   - Project 10-year free cash flows and calculate intrinsic value.

7. **Phase 7: Model JSON Generator**
   - Parse the markdown metadata and export to a structured JSON for the frontend.

---

## Interactive Frontend Viewer

- **Zero-dependency HTML**: `tools/financial_model_viewer.html`
- **Served via**: `tools/simple_frontend_server.py`
- **Functionality**: Reads the generated JSON, allows for real-time assumption adjustments in vanilla JS, and saves scenarios back to the ticker folder.

---

## Local Services

| Service                 | Script                              | Port   | Launcher                      | When to Run                             |
| ----------------------- | ----------------------------------- | ------ | ----------------------------- | --------------------------------------- |
| **Tiger-Transformer**   | `tools/tiger_transformer_server.py` | `8000` | `tools/start_transformer.bat` | During document processing (Skills 1–4) |
| **Browser File Server** | `python -m http.server`             | `8181` | (manual)                      | During PDF extraction                   |
| **Frontend Viewer**     | `tools/simple_frontend_server.py`   | `3000` | `tools/start_frontend.bat`    | When reviewing/modeling results         |

---

## Key Difference: Tiger-Cafe vs. Tiger-Skills

| Aspect                 | Tiger-Cafe                                    | Tiger-Skills                                               |
| ---------------------- | --------------------------------------------- | ---------------------------------------------------------- |
| Architecture           | Full-stack web app (FastAPI + React + SQLite) | Flat file system + AI skills                               |
| Storage                | SQL database with ORM models                  | Markdown files + PDFs in folders                           |
| Orchestration          | Python code (`extraction_orchestrator.py`)    | `SKILL.md` instructions for AI                             |
| Progress Tracking      | Database milestones + WebSocket events        | Markdown sections in `processing_data/`                    |
| Transformer            | In-process Python (PyTorch model)             | Local FastAPI server (`tools/tiger_transformer_server.py`) |
| Qualitative Assessment | Not implemented                               | AI skill reading analyst reports/transcripts               |
| Financial Model UI     | React component (`FinancialModel.jsx`)        | Zero-dependency HTML (`tools/financial_model_viewer.html`) |
| Scenario Persistence   | SQLite database                               | JSON files in `output_data/TICKER/`                        |
