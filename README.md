# tiger-skills

A collection of modular AI skills for processing financial documents. Each skill is a self-contained set of instructions, scripts, and resources that an AI agent can follow to extract, standardize, and analyze financial data from PDFs.

This is a skill-based reimplementation of [tiger-cafe](https://github.com/Ruinius/tiger-cafe) — instead of a full-stack web app, the AI agent itself is the runtime.

## How It Works

1. Drop financial PDFs (earnings releases, 10-Qs, 10-Ks) into `input_data/`
2. The user can use the `skills/PIPELINE.md` runbook to automate the pipeline, or run the skills one by one by passing their `SKILL.md` files.
3. Processed data is output as structured markdown files in `output_data/`, organized by ticker

## Skills

| Skill                                                          | Status   | Description                                                                    |
| -------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------ |
| [Document Classification](skills/document_classification/)     | ✅ Built | Classify PDFs, extract metadata, validate tickers via Yahoo Finance            |
| [Financial Data Extraction](skills/financial_data_extraction/) | ✅ Built | Extract balance sheets, income statements, shares, growth, GAAP reconciliation |
| [Financial Calculations](skills/financial_calculations/)       | ✅ Built | Compute EBITA, tax rates, invested capital, summary tables                     |
| [Document Organization](skills/document_organization/)         | ✅ Built | Organize outputs by ticker, cross-document date healing                        |
| [Financial Modeling](skills/financial_modeling/)               | ✅ Built | WACC, DCF modeling, intrinsic value from historical data + qualitative outlook |

## Project Structure

```
tiger-skills/
├── skills/                 # AI skill definitions (SKILL.md + scripts + resources)
│   ├── document_classification/
│   ├── financial_data_extraction/
│   ├── financial_calculations/
│   ├── document_organization/
│   └── financial_modeling/
├── tools/                  # Shared tools and utilities
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
│   └── TICKER/
│       ├── TICKER_metadata.md         # Company metadata + financial history
│       ├── TICKER_financial_model.json # DCF model (consumed by viewer)
│       ├── TICKER_scenarios.json      # Saved valuation scenarios
│       └── TICKER_EA_*.md             # Processed earnings documents
```

## Getting Started

### Prerequisites

- Python 3.10+
- An AI agent that supports the [Antigravity Skills](https://github.com/google-deepmind/antigravity) format

### Setup

1. **Clone and Install:**

   ```bash
   git clone https://github.com/Ruinius/financial-analyst-skills.git
   cd tiger-skills
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
