# tiger-skills

A collection of modular AI skills for processing financial documents. Each skill is a self-contained set of instructions, scripts, and resources that an AI agent can follow to extract, standardize, and analyze financial data from PDFs.

This is a skill-based reimplementation of [tiger-cafe](https://github.com/Ruinius/tiger-cafe) — instead of a full-stack web app, the AI agent itself is the runtime.

## How It Works

1. Drop financial PDFs (earnings releases, 10-Qs, 10-Ks) into `input_data/`
2. The AI reads each skill's `SKILL.md` and follows the step-by-step instructions
3. Processed data is output as structured markdown files in `output_data/`, organized by ticker

## Skills

| Skill                                                      | Status     | Description                                                                    |
| ---------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------ |
| [Document Classification](skills/document_classification/) | ✅ Built   | Classify PDFs, extract metadata, validate tickers via Yahoo Finance            |
| Financial Data Extraction                                  | 🔲 Planned | Extract balance sheets, income statements, shares, growth, GAAP reconciliation |
| Financial Calculations                                     | 🔲 Planned | Compute EBITA, tax rates, invested capital, summary tables                     |
| Document Organization                                      | 🔲 Planned | Organize outputs by ticker, cross-document date healing                        |
| Financial Modeling                                         | 🔲 Planned | DCF modeling from historical data                                              |

## Project Structure

```
tiger-skills/
├── skills/                 # AI skill definitions (SKILL.md + scripts + resources)
│   ├── document_classification/
│   ├── financial_data_extraction/
│   ├── financial_calculations/
│   ├── document_organization/
│   └── financial_modeling/
├── tools/                  # Static CSV mappings for financial standardization
├── docs/                   # Project documentation and roadmap
├── data/                   # Static data and configurations
├── scripts/                # Standalone utility scripts
├── input_data/             # (gitignored) Drop PDFs here to process
├── processing_data/        # (gitignored) Files currently being processed
└── output_data/            # (gitignored) Final output organized by ticker
```

## Getting Started

### Prerequisites

- Python 3.10+
- An AI agent that supports the [Antigravity Skills](https://github.com/google-deepmind/antigravity) format

### Setup

1. **Clone and Install:**

   ```bash
   git clone https://github.com/Ruinius/tiger-skills.git
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
   Before running extraction skills, you need to start two local servers in separate terminals:

   A. Start the transformer server (Port 8000):

   ```bash
   .\tools\start_transformer.bat
   ```

   B. Start the static file server for the browser agent (Port 8181):

   ```bash
   python -m http.server 8181 --bind 127.0.0.1
   ```

### Usage

1. Place one or more financial PDFs in `input_data/`
2. Ask the AI agent to execute the full document processing pipeline by following the [Pipeline Runbook](skills/PIPELINE.md)
3. The agent will process each document through Classification, Financial Extraction, and Calculations, before organizing the final outputs into `output_data/TICKER/`

## Documentation

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full architecture plan, pipeline breakdown, and build order.

## Related Projects

- [tiger-cafe](https://github.com/Ruinius/tiger-cafe) — Full-stack financial document processing app (FastAPI + React)
- [tiger-transformer](https://github.com/Ruinius/tiger-transformer) — Fine-tuned FINBERT model for standardizing financial line items
