# financial-analyst-skills

**Turn any earnings PDF into a full DCF valuation — automatically.**

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

All 21 skills are registered in [`skills/skills_metadata.json`](skills/skills_metadata.json). Each includes a `SKILL.md` with step-by-step instructions, worked examples, validation checks, and expected output formats.

| #   | Skill                                                                          | Description                                                                          |
| --- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| 0   | [**Pipeline Orchestrator**](skills/PIPELINE.md)                                | Runbook that routes documents through the full skill chain based on document type    |
|     |                                                                                |                                                                                      |
| 1   | [**Document Classification**](skills/document_classification/)                 | Classify PDFs, extract metadata (ticker, date, doc type), validate via Yahoo Finance |
|     |                                                                                |                                                                                      |
| 2   | [**Financial Data Extraction**](skills/financial_data_extraction/)             | Extract structured financial data from classified PDFs                               |
| 2a  | ↳ [Balance Sheet](skills/financial_data_extraction/balance_sheet/)             | Extract balance sheet line items, standardize via Tiger-Transformer                  |
| 2b  | ↳ [Income Statement](skills/financial_data_extraction/income_statement/)       | Extract income statement line items, normalize expense signs                         |
| 2c  | ↳ [Shares Outstanding](skills/financial_data_extraction/shares_outstanding/)   | Extract basic and diluted share counts                                               |
| 2d  | ↳ [Organic Growth](skills/financial_data_extraction/organic_growth/)           | Extract organic/constant-currency growth rates                                       |
| 2e  | ↳ [GAAP Reconciliation](skills/financial_data_extraction/gaap_reconciliation/) | Extract GAAP-to-non-GAAP operating income reconciliation                             |
|     |                                                                                |                                                                                      |
| 3   | [**Financial Calculations**](skills/financial_calculations/)                   | Compute derived metrics from extracted data (pure math, no LLM)                      |
| 3a  | ↳ [EBITA](skills/financial_calculations/ebita/)                                | Earnings Before Interest, Tax, and Amortization                                      |
| 3b  | ↳ [Tax Rate](skills/financial_calculations/tax/)                               | Effective and adjusted (operating) tax rates                                         |
| 3c  | ↳ [Invested Capital](skills/financial_calculations/invested_capital/)          | NWC + net long-term operating assets                                                 |
| 3d  | ↳ [Summary Table](skills/financial_calculations/summary_table/)                | Final summary with NOPAT, ROIC, and all key metrics                                  |
|     |                                                                                |                                                                                      |
| 4   | [**Document Organization**](skills/document_organization/)                     | Move outputs to `output_data/TICKER/`, create metadata, cross-document date healing  |
|     |                                                                                |                                                                                      |
| 5   | [**Financial Modeling**](skills/financial_modeling/)                           | Build a multi-stage DCF from historical data + qualitative outlook                   |
| 5a  | ↳ [WACC](skills/financial_modeling/wacc/)                                      | Weighted Average Cost of Capital via CAPM (unlever beta → Blume's → bound 7-11%)     |
| 5b  | ↳ [Assumptions](skills/financial_modeling/assumptions/)                        | Three-stage revenue growth, EBITA margin, capital turnover from history + outlook    |
| 5c  | ↳ [DCF Model](skills/financial_modeling/dcf/)                                  | 10-year FCF projections + terminal value via Gordon Growth Model                     |
| 5d  | ↳ [Intrinsic Value](skills/financial_modeling/intrinsic_value/)                | Enterprise Value → equity bridge → intrinsic value per share                         |
| 5e  | ↳ [JSON Export](skills/financial_modeling/json_export/)                        | Export model to JSON for the interactive HTML viewer                                 |

## Project Structure

```
financial-analyst-skills/
├── skills/                 # AI skill definitions (SKILL.md + examples + scripts)
│   ├── document_classification/
│   ├── financial_data_extraction/
│   ├── financial_calculations/
│   ├── document_organization/
│   └── financial_modeling/
├── tools/                  # Shared tools and utilities
│   ├── model/                        # (gitignored) Tiger-transformer model files
│   ├── market_data.py                # Yahoo Finance lookups (validate, profile, fx)
│   ├── tiger_transformer_server.py   # Local transformer model server
│   ├── financial_model_viewer.html   # Interactive DCF viewer (zero-dependency)
│   ├── simple_frontend_server.py     # Static file server + scenario save endpoint
│   ├── start_transformer.bat         # Launch transformer server
│   └── start_frontend.bat            # Launch frontend viewer server
├── docs/                   # Project documentation and roadmap
├── data/                   # Static data and configurations
├── input_data/             # (gitignored) Drop PDFs here to process
├── processing_data/        # (gitignored) Files currently being processed
└── output_data/            # (gitignored) Final output organized by ticker
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
   python -m venv venv
   source venv/bin/activate        # Linux/Mac
   venv\Scripts\activate           # Windows
   pip install -r requirements.txt
   ```

2. **Configure Tiger-Transformer:**
   The standardization skills require the [tiger-transformer](https://huggingface.co/Ruinius/tiger-transformer) model.
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
   python -m http.server 8181 --bind 127.0.0.1
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
