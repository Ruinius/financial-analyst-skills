# Tiger-Skills Roadmap & Architecture Plan

> **Goal**: Port the tiger-cafe agentic pipeline into modular, reusable Antigravity Skills that can be built, tested, and composed independently.

## What Are Antigravity Skills?

Skills are a first-class extension mechanism in Antigravity. Each skill is a **folder** containing:

| File/Dir     | Required | Purpose                                                                                                                                                             |
| ------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SKILL.md`   | Yes      | Main instruction file with YAML frontmatter (`name`, `description`) and detailed markdown instructions. This is what the AI reads to know how to execute the skill. |
| `scripts/`   | Optional | Helper scripts (Python, shell, etc.) that the AI can invoke                                                                                                         |
| `examples/`  | Optional | Reference inputs/outputs for the AI to learn from                                                                                                                   |
| `resources/` | Optional | Templates, CSV mappings, config files                                                                                                                               |

### How Skills Work

1. You (or the AI) place skill folders in `skills/`
2. When a task matches a skill's description, the AI reads `SKILL.md` for instructions
3. The AI follows those instructions step-by-step, using the scripts/resources in the skill folder
4. Skills can reference other skills, creating composable pipelines

Each `SKILL.md` is essentially a **detailed recipe** for the AI. The more specific and structured your instructions are, the more reliably the AI will execute them. Think of it like writing a runbook for a junior analyst.

---

## Pipeline Overview

Human step: Drop PDFs in `input_data/`

**Skill: Document Classification** ✅

- Move PDF from `input_data/` → `processing_data/`
- Read PDF and extract: company TICKER, company name, document type, document_date, fiscal quarter, period_end_date
- Validate ticker via Yahoo Finance (with reflection fallback, then human fallback)
- Rename PDF to standard format: `TICKER_DOCTYPE_YYYYMMDD_temp.pdf`
- Create initial markdown: `TICKER_DOCTYPE_YYYYMMDD_temp.md`

**Skill: Financial Data Extraction** ✅ (for Earnings Announcement, 10K, 10Q, or equivalent financial reports)

- Sub-skill: Balance Sheet extraction → standardize with tiger-transformer + CSV mappings
- Sub-skill: Income Statement extraction → standardize + sign normalization
- Sub-skill: Shares Outstanding extraction
- Sub-skill: Organic Growth calculation + organic/currency-constant growth search
- Sub-skill: GAAP Reconciliation extraction

**Skill: Financial Calculations** ✅ (for Earnings Announcement, 10K, 10Q, or equivalent financial reports)

- Sub-skill: EBITA calculation
- Sub-skill: Tax rate calculation (simple + operating)
- Sub-skill: Invested Capital (NWC + long-term capital)
- Sub-skill: Summary table

**Skill: Document Organization** ✅

- Move processed files to `output_data/TICKER/`
- Create/update `TICKER_metadata.md`
- Cross-document date healing

**Skill: Qualitative Assessment** ✅ (for Analyst Reports, Transcripts, and Long Form Articles)

- Sub-skill: Determine whether the economic moat is Wide, Narrow, or None based on Morningstar-like rating and provide three bullets of rationale. Give a confidence level. Compare, harmonize, update content in `TICKER_metadata.md`
- Sub-skill: Determine whether the EBITA margin will expand or shrink by 1 or 2 percentage points and provide three bullets of rationale. Give a confidence level. Compare, harmonize, update content in `TICKER_metadata.md`
- Sub-skill: Determine whether the organic growth rate will increase or decrease by 1 or 2 percentage points and provide three bullets of rationale. Give a confidence level. Compare, harmonize, update content in `TICKER_metadata.md`

**Skill: Financial Modeling** ✅

- Sub-skill: Calculate WACC using CAPM model (unlever beta → Blume's → CAPM → bound 7-11%) to `TICKER_metadata.md`
- Sub-skill: Create all the assumptions using a combination of historical and output from qualitative assessment to `TICKER_metadata.md`
- Sub-skill: Populate the full DCF model to `TICKER_metadata.md`
- Sub-skill: Populate the translation from DCF value to intrinsic value per share to `TICKER_metadata.md`
- Sub-skill: Create and update `output_data/TICKER/TICKER_financial_model.json`

**Frontend: Zero dependency interactive HTML** ✅ (one-time build)

- Zero-dependency interactive HTML DCF viewer: `tools/financial_model_viewer.html`
- Served via `tools/simple_frontend_server.py` (static file serving + scenario save endpoint)
- Reads data from `output_data/TICKER/TICKER_financial_model.json` via URL param (e.g., `?ticker=ADBE`)
- Financial Modeling skill outputs the JSON; the viewer is static
- **Interactive recalculation**: Editable assumption inputs (revenue growth, EBITA margin, WACC, terminal growth, tax rate, MCT) trigger instant DCF recalculation in vanilla JS
- **Reset to defaults**: Button restores all assumptions to the AI-generated values from the JSON
- **Scenario saving**: Save named snapshots of assumptions + calculated intrinsic value to `output_data/TICKER/TICKER_scenarios.json` via POST endpoint — git-trackable, portable, lives alongside the data

**Shared Tools** ✅

- `tools/market_data.py` — centralized Yahoo Finance tool with `validate`, `profile`, and `fx` subcommands
- `tools/start_transformer.bat` / `tools/start_frontend.bat` — one-click server launchers

---

## Tiger-Cafe References

| Skill                         | Tiger-Cafe Reference File                                           |
| ----------------------------- | ------------------------------------------------------------------- |
| Document Classification       | `app/app_agents/document_classifier.py`                             |
| Balance Sheet                 | `app/app_agents/balance_sheet_extractor.py`                         |
| Income Statement              | `app/app_agents/income_statement_extractor.py`                      |
| Shares Outstanding            | `app/app_agents/shares_outstanding_extractor.py`                    |
| Organic Growth                | `app/app_agents/organic_growth_extractor.py`                        |
| GAAP Reconciliation           | `app/app_agents/gaap_reconciliation_extractor.py`                   |
| Tiger-Transformer Client      | `app/services/tiger_transformer_client.py`                          |
| Extraction Orchestrator       | `app/services/extraction_orchestrator.py`                           |
| Historical Calculations       | `app/utils/historical_calculations.py`                              |
| Timeline Service              | `app/services/timeline_service.py`                                  |
| Qualitative Assessment        | `app/app_agents/qualitative_extractor.py`                           |
| Financial Modeling (WACC/DCF) | `app/utils/financial_modeling.py`                                   |
| Financial Model UI (Frontend) | `frontend/src/components/views/company/FinancialModel.jsx`          |
| Summary Table UI              | `frontend/src/components/views/document/DocumentExtractionView.jsx` |

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

---

## Local Services

To keep skills fast and modular, heavy computational tasks and file serving are handled by local services.

| Service                 | Script                              | Port   | Launcher                      | When to Run                             |
| ----------------------- | ----------------------------------- | ------ | ----------------------------- | --------------------------------------- |
| **Tiger-Transformer**   | `tools/tiger_transformer_server.py` | `8000` | `tools/start_transformer.bat` | During document processing (Skills 1–4) |
| **Browser File Server** | `python -m http.server`             | `8181` | (manual)                      | During PDF extraction                   |
| **Frontend Viewer**     | `tools/simple_frontend_server.py`   | `3000` | `tools/start_frontend.bat`    | When reviewing/modeling results         |

**Quick start:**

- Processing: double-click `tools/start_transformer.bat` + run `python -m http.server 8181 --bind 127.0.0.1`
- Reviewing: double-click `tools/start_frontend.bat` → open `http://127.0.0.1:3000/?ticker=ADBE`

---

The biggest mental shift: In tiger-cafe, you wrote **code** that does things. In tiger-skills, you write **instructions** that tell the AI how to do things. The AI _is_ the runtime.

---

## Performance & Token Optimization Suggestions

> **Context**: A full financial-report pipeline run (Phases 1–4) touches ~14 sequential skills. Each skill's SKILL.md is loaded into the LLM context, and many steps involve browser sessions, script execution, or re-reading the same markdown file. The suggestions below are ordered by estimated impact.

---

### 🔴 High Impact — Do These First

#### 1. Extract Boilerplate into a Shared Include File ✅

**Problem**: Every single SKILL.md (all 20 of them) contains an identical **Example Curation** block (~35 lines) and **Self-Improvement** block (~30 lines). That's **~1,300 lines of pure duplication** loaded into the LLM context on every skill execution. The content is identical except for the folder path.

**Current cost**: ~65 duplicated lines × 20 skills = **~1,300 wasted lines** read across a full pipeline run.

**Suggestion**: Create a shared file `skills/SHARED_POSTRUN.md` with the Example Curation and Self-Improvement templates (using a `{SKILL_EXAMPLES_DIR}` placeholder). Replace the 65 lines in each SKILL.md with a 2-line reference:

```markdown
## Post-Run Steps

Follow the instructions in `skills/SHARED_POSTRUN.md` using examples folder: `./examples/`
```

**Estimated savings**: ~1,200 lines of context per full pipeline run.

#### 2. Eliminate Redundant Browser Sessions for PDF Reading ✅

**Problem**: The PDF is opened via `browser_subagent` up to **7 separate times** during Phases 1–2 for a single financial document:

| Skill                   | Browser Session | Pages Needed                                  |
| ----------------------- | --------------- | --------------------------------------------- |
| Document Classification | Session 1       | Cover page (1–3)                              |
| Balance Sheet           | Session 2       | Balance sheet pages                           |
| Income Statement        | Session 3       | Income statement pages                        |
| Shares Outstanding      | Session 4       | EPS section (often same page as IS)           |
| Organic Growth          | Session 5       | Management discussion + IS comparative column |
| GAAP Reconciliation     | Session 6       | Reconciliation tables (back pages)            |

Each `browser_subagent` call has significant overhead: tool-call latency, page rendering, screenshot processing, and LLM tokens for the sub-agent's own reasoning.

**Suggestion**: Consolidate into **2 browser sessions maximum**:

- **Session A** (Classification): Read cover page, classify the document.
- **Session B** (Extraction): Open the full PDF once, navigate through all financial statement pages, and extract Balance Sheet, Income Statement, Shares Outstanding, Organic Growth, and GAAP Reconciliation data in a **single pass**. Write all extracted data to intermediate JSON or markdown in one go.

This means the `financial_data_extraction/SKILL.md` orchestrator should instruct the AI to keep a single browser session open and extract all 5 sub-skills' data within it, rather than opening/closing 5 times. Shares Outstanding data frequently appears on the same page as the Income Statement, so extracting them together is natural.

**Estimated savings**: ~5 fewer browser_subagent round-trips × ~30 seconds each = **~2.5 minutes of wall-clock time** + significant token savings from eliminating 5 sub-agent conversations.

#### 3. Convert Pure-Math Skills to Python Scripts ✅

**Problem**: Financial Calculations (Phase 3) — EBITA, Tax, Invested Capital, Summary Table — are described as "pure arithmetic, no LLM calls needed," but they're still executed as LLM skills. The AI reads the SKILL.md instructions, reads the markdown data, reasons through the arithmetic, and writes the output. This wastes tokens on work a 50-line Python script could do deterministically and instantly.

Similarly, several Financial Modeling sub-skills (DCF, Intrinsic Value, JSON Export) are pure arithmetic that the LLM is doing token-by-token.

**Currently wasting LLM inference on**:

- EBITA calculation (~200 lines of SKILL.md to produce ~10 lines of output)
- Tax Rate calculation (~218 lines)
- Invested Capital (~232 lines)
- Summary Table (~187 lines)
- DCF Model projections (~291 lines)
- Intrinsic Value bridge (~221 lines)
- JSON Export (~276 lines)

**Suggestion**: Create Python scripts in each skill's `scripts/` folder (e.g., `scripts/calculate.py`) that:

1. Read the markdown file, parse the tables
2. Perform all arithmetic
3. Append the results to the markdown file

The SKILL.md becomes a thin wrapper: "Run `scripts/calculate.py {markdown_file}`" — reducing the LLM's job to invoking one command and validating the output.

**Estimated savings**: ~1,400 lines of SKILL.md context no longer need to be reasoned through + eliminates LLM arithmetic errors + saves ~70% of Phase 3 and Phase 6 execution time.

#### 4. Flatten the Parent ↔ Sub-Skill Hierarchy ✅

**Problem**: The PIPELINE.md calls a parent SKILL.md (e.g., `financial_data_extraction/SKILL.md`), which itself just lists the sub-skills and says "now go read these child SKILL.md files." These parent skills are essentially **routing tables that burn tokens without doing any work**.

Parent skills with minimal unique content:

- `financial_data_extraction/SKILL.md` (149 lines — mostly sub-skill table + boilerplate)
- `financial_calculations/SKILL.md` (123 lines — just lists sub-skills + boilerplate)
- `financial_modeling/SKILL.md` (135 lines — just lists sub-skills + boilerplate)

**Suggestion**: Inline the parent orchestration into `PIPELINE.md` (it already has the execution order and dependency graph). Remove the parent SKILL.md files entirely, or reduce them to a 5-line pointer. The PIPELINE already says "Run 2a, then 2b, then 2c..." — the parent SKILL.md repeats this information redundantly.

**Estimated savings**: ~400 lines of redundant context, and eliminates an extra file-read round-trip per phase.

---

### 🟡 Medium Impact

#### 5. Combine Shares Outstanding into Income Statement Extraction ✅

**Problem**: Shares Outstanding is a tiny skill (167 lines of SKILL.md) that extracts just 2 numbers (basic and diluted shares). These numbers are almost always on the **same page** as the Income Statement (right below Net Income). Running it as a separate skill means:

- A separate SKILL.md read (~167 lines of context)
- A separate browser session (or at minimum, re-navigating to the same page)
- Separate example curation and self-improvement overhead

**Suggestion**: Merge shares outstanding extraction into the Income Statement skill. Add a "Step 3b: Extract Shares Outstanding" between the current Step 3 and Step 4. The IS extraction already says "STOP after Net Income" — just extend it to read 2 more rows.

**Estimated savings**: ~167 lines of context + 1 fewer skill transition.

#### 6. Defer Example Curation and Self-Improvement to End-of-Pipeline ✅

**Problem**: Even after extracting boilerplate to a shared file (suggestion #1), each skill still has to _execute_ the curation and self-improvement steps. This means:

- List examples directory, read example files, compare, delete losers, write winner — after _every single_ sub-skill
- Reflect, propose edits, update SKILL.md — after _every single_ sub-skill

For a 14-skill pipeline, that's 14 rounds of file listing, file reading, file comparison, and file writing — none of which contribute to the document processing output.

**Suggestion**: Move example curation and self-improvement to a **post-pipeline epilogue** — a single step that runs after all skills complete. Batch the example curation: save all intermediate outputs, then curate all 14 examples at once. Batch self-improvement: collect all reflections, then propose edits in one pass.

Add a `## Post-Pipeline Epilogue` section to `PIPELINE.md` that says: "Now run example curation and self-improvement for all skills that were executed."

**Estimated savings**: ~12 fewer curation cycles × ~5 file operations each = **~60 fewer tool calls** per pipeline run.

#### 8. Single-Pass PDF Read with Structured Extraction Prompt ✅

**Problem**: Even within a single browser session, the AI often navigates forward and backward through the PDF — jumping to the balance sheet, then back to the income statement, then forward to GAAP reconciliation tables. Each page turn in the browser is a tool call.

**Suggestion**: For earnings announcements (which are typically 8–15 pages), read the **entire document** in the browser in one forward pass, capturing all financial data into a single structured JSON. Then process the JSON data offline (no more browser needed). This is a "read once, process many" pattern.

For larger filings (10-K, 10-Q at 100+ pages), use the table of contents to jump to the 3–4 relevant pages, but still extract everything in one session rather than revisiting.

**Estimated savings**: Eliminates multiple page-navigation tool calls per extraction.

---

### 🟢 Lower Impact (Polish)

#### 9. Reduce SKILL.md Verbosity for Stable Skills ✅

**Problem**: Many SKILL.md files are very verbose with explanations that were useful during initial development but are now just context overhead. For example, the EBITA skill has a long "What is EBITA?" section and the Invested Capital skill has a full worked Adobe example. Once the skill is stable and the example file is good, this tutorial-style content wastes tokens.

**Suggestion**: After a skill has been stable for 5+ runs, trim the SKILL.md to its essential instructions. Move the worked examples and conceptual explanations to a `resources/README.md` within the skill folder — available if needed, but not loaded into context on every run. Keep only the step-by-step and the validation rules in SKILL.md.

**Estimated savings**: ~30-50% reduction in SKILL.md size across mature skills.

#### 10. Skip GAAP Reconciliation for Non-EA Documents ✅

**Problem**: The GAAP Reconciliation skill already checks `document_type` and skips for non-earnings-announcement documents, but the skill is still **loaded and read** by the LLM before it reaches that check. That's 252 lines of context for a no-op.

**Suggestion**: Move the document-type check into the parent orchestrator / PIPELINE. Add a conditional in Phase 2: "If document_type is NOT earnings_announcement, skip 2e." This way the GAAP Reconciliation SKILL.md is never even opened.

**Estimated savings**: ~252 lines of context on non-EA documents.

---

### 📊 Summary of Estimated Savings

| #   | Suggestion                      | Token Savings                    | Time Savings      | Effort |
| --- | ------------------------------- | -------------------------------- | ----------------- | ------ |
| 1   | Shared boilerplate file ✅      | ~1,200 lines/run                 | Moderate          | Low    |
| 2   | Consolidate browser sessions ✅ | ~5 sub-agent calls               | ~2.5 min          | Medium |
| 3   | Python scripts for math ✅      | ~1,400 lines + no LLM arithmetic | ~50% of Phase 3+6 | High   |
| 4   | Flatten parent skills ✅        | ~400 lines                       | Minor             | Low    |
| 5   | Merge shares into IS ✅         | ~167 lines                       | Minor             | Low    |
| 6   | Defer curation to epilogue ✅   | ~60 tool calls/run               | ~3–5 min          | Medium |
| 8   | Single-pass PDF read ✅         | ~10 tool calls                   | ~1–2 min          | Medium |
| 9   | Trim verbose SKILL.md ✅        | ~30-50% per skill                | Moderate          | Low    |
| 10  | Skip GAAP early ✅              | ~252 lines (non-EA)              | Minor             | Low    |

**Conservatively**, implementing suggestions 1–4 alone could reduce total pipeline tokens by **~40%** and wall-clock time by **~30%**.
