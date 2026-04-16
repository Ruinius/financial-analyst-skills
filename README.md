# financial-analyst-skills

**Turn any earnings PDF into a full DCF valuation with AI agents using Skills.**

Drop a financial document into a folder, point an AI agent at the skills in this repo, and get a complete equity research workflow: document classification, structured data extraction, financial calculations, qualitative assessment, and a 10-year discounted cash flow model with an interactive viewer. No databases, no backend, no React — just markdown files, a fine-tuned transformer, and an AI that follows instructions.

This project reimagines the traditional financial analysis stack. Instead of writing code that _does_ the analysis, you write **skills** — step-by-step instructions that tell an AI agent _how_ to do the analysis. The AI is the runtime. The skills are the program. The output is a set of portable, git-trackable markdown and JSON files that capture the complete analytical chain from raw PDF to intrinsic value per share.

Built as a skill-based reimplementation of [tiger-cafe](https://github.com/Ruinius/tiger-cafe) (a full-stack FastAPI + React app), this project achieves the same analytical depth with zero infrastructure.

> **⚠️ Personal Project** — This is a personal learning and research project. Expect rough edges, bugs, and evolving workflows. You're welcome to fork it and experiment, but I won't be reviewing pull requests.

## How It Works

1. **Drop** financial PDFs (earnings releases, 10-Qs, 10-Ks, analyst reports) into `input_data/`
2. **Run** the [Pipeline](skills/PIPELINE.md) — the AI agent classifies documents, extracts financials, computes metrics, and organizes everything by ticker
3. **Model** — the Financial Modeling skill builds a WACC → DCF → intrinsic value chain from historical data + qualitative outlook
4. **Interact** — open the zero-dependency HTML viewer to adjust assumptions and see instant DCF recalculations

```
PDF → Classification → Extraction → Calculations → Organization → DCF Model → Interactive Viewer
```

## Skills

All 7 skills are registered in [`skills/skills_metadata.json`](skills/skills_metadata.json). Each skill is a single, consolidated `SKILL.md` with step-by-step instructions, worked examples, validation checks, and expected output formats. A shared [`SHARED_POSTRUN.md`](skills/SHARED_POSTRUN.md) defines common example-curation and self-improvement steps.

| Phase | Skill                                                          | Description                                                                                                    |
| ----- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| —     | [**Pipeline Orchestrator**](skills/PIPELINE.md)                | Runbook that routes documents through the full skill chain based on document type                               |
| 1     | [**Document Classification**](skills/document_classification/) | Classify PDFs, extract metadata (ticker, date, doc type), validate via Yahoo Finance                           |
| 2     | [**Financial Data Extraction**](skills/financial_data_extraction/) | Extract balance sheet, income statement, shares, organic growth, and GAAP reconciliation; standardize via Tiger-Transformer |
| 3     | [**Financial Calculations**](skills/financial_calculations/)   | Single deterministic script computes EBITA, tax rates, invested capital, NOPAT, ROIC, and summary table        |
| 4     | [**Document Organization**](skills/document_organization/)     | Move outputs to `output_data/TICKER/`, create/update metadata, cross-document date healing                     |
| 5     | [**Qualitative Assessment**](skills/qualitative_assessment/)   | Assess economic moat, margin trajectory, and growth trajectory from analyst reports                             |
| 6     | [**Financial Modeling**](skills/financial_modeling/)            | Single script: WACC → three-stage assumptions → 10-year DCF → intrinsic value per share → JSON export          |

## Project Structure

```
financial-analyst-skills/
├── skills/                     # AI skill definitions
│   ├── PIPELINE.md             # Pipeline orchestrator runbook
│   ├── SHARED_POSTRUN.md       # Shared example-curation & self-improvement steps
│   ├── skills_metadata.json    # Skill registry
│   ├── document_classification/
│   │   ├── SKILL.md
│   │   ├── examples/           # Gold-standard worked example
│   │   ├── resources/          # Reference files (document-type taxonomy, etc.)
│   │   └── scripts/            # Automation scripts
│   ├── financial_data_extraction/
│   │   ├── SKILL.md            # Consolidated: BS + IS + shares + organic growth + GAAP recon
│   │   ├── examples/
│   │   ├── resources/
│   │   └── scripts/            # transform_and_append.py
│   ├── financial_calculations/
│   │   ├── SKILL.md            # Consolidated: EBITA + tax + invested capital + summary
│   │   ├── examples/
│   │   └── scripts/            # calculate.py
│   ├── document_organization/
│   │   ├── SKILL.md
│   │   ├── examples/
│   │   └── scripts/            # organize.py
│   ├── qualitative_assessment/
│   │   ├── SKILL.md
│   │   └── examples/
│   └── financial_modeling/
│       ├── SKILL.md            # Consolidated: WACC + assumptions + DCF + intrinsic value + JSON
│       ├── examples/
│       └── scripts/            # calculate.py
├── tools/                      # Shared tools and utilities
│   ├── markdown_parser.py                      # Utility for parsing markdown outputs
│   ├── market_data.py                          # Yahoo Finance lookups (validate, profile, fx)
│   ├── tiger_transformer_server.py             # Local transformer model server
│   ├── financial_model_viewer.html             # Interactive DCF viewer (zero-dependency)
│   ├── simple_frontend_server.py               # Static file server + scenario save endpoint
│   ├── bs_calculated_operating_mapping.csv     # Balance-sheet operating-item mapping
│   ├── is_calculated_operating_expense_mapping.csv  # Income-statement expense mapping
│   ├── model/                                  # (gitignored) Tiger-transformer model files
│   ├── start_transformer.bat                   # Launch transformer server
│   ├── start_file_server.bat                   # Launch file server for PDF reading
│   └── start_frontend.bat                      # Launch frontend viewer server
├── docs/                       # Project documentation and roadmap
├── input_data/                 # (gitignored) Drop PDFs here to process
├── processing_data/            # (gitignored) Files currently being processed
└── output_data/                # (gitignored) Final output organized by ticker
    └── TICKER/
        ├── TICKER_metadata.md         # Company metadata + financial history
        ├── TICKER_financial_model.json # DCF model (consumed by viewer)
        ├── TICKER_scenarios.json      # Saved valuation scenarios
        └── TICKER_EA_*.md             # Processed earnings documents
```

## Getting Started

### Prerequisites

- Python 3.10+
- An AI agent that supports the [Antigravity Skills](https://github.com/google-deepmind/antigravity) format

### Setup

1. **Clone and Install:**

   ```bash
   git clone https://github.com/Ruinius/financial-analyst-skills.git
   cd financial-analyst-skills
   python -m venv .venv
   source .venv/bin/activate       # Linux/Mac
   .venv\Scripts\activate          # Windows
   pip install -r requirements.txt
   ```

2. **Configure Tiger-Transformer:**
   The extraction skill requires the [tiger-transformer](https://huggingface.co/Ruinius/tiger-transformer) model.
   - Download the model repository files (including `model.safetensors`, `config.json`, `label_map.json`, etc.) from HuggingFace.
   - Create a `tools/model/` directory in this project and place all downloaded files inside it.

3. **Start the Local Services:**
   Before running skills, start these servers in separate terminals:

   A. **Transformer server** (Port 8000) — required for data extraction:

   ```bash
   .\tools\start_transformer.bat
   ```

   B. **Browser agent file server** (Port 8181) — required for PDF reading:

   ```bash
   .\tools\start_file_server.bat
   ```

   C. **Frontend viewer** (Port 3000) — for interactive DCF model:

   ```bash
   .\tools\start_frontend.bat
   ```

### Usage

1. Place one or more financial PDFs in `input_data/`
2. Ask the AI agent to execute the full document processing pipeline by following the [Pipeline Runbook](skills/PIPELINE.md)
3. The agent will process each document through Classification → Extraction → Calculations → Organization
4. Run the [Financial Modeling](skills/financial_modeling/) skill on a ticker to generate WACC, DCF projections, and intrinsic value
5. View the interactive model at `http://127.0.0.1:3000/?ticker=ADBE`

### Tools

| Tool                                   | Description                                      |
| -------------------------------------- | ------------------------------------------------ |
| `tools/market_data.py validate TICKER` | Validate a stock ticker via Yahoo Finance        |
| `tools/market_data.py profile TICKER`  | Get price, beta, market cap, shares, currency    |
| `tools/market_data.py fx RMB USD`      | Get exchange rate between currencies             |
| `tools/financial_model_viewer.html`    | Interactive DCF viewer with editable assumptions |

## Documentation

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full architecture plan, pipeline breakdown, and build order.

## Related Projects

- [tiger-cafe](https://github.com/Ruinius/tiger-cafe) — Full-stack financial document processing app (FastAPI + React)
- [tiger-transformer](https://github.com/Ruinius/tiger-transformer) — Fine-tuned FINBERT model for standardizing financial line items
