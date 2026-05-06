# Project Documentation Index

## Folder Structure

- `.agents/`: Agent-specific configuration and data.
- `assets/`: Project assets (images, etc.).
- `docs/`: Project documentation.
  - `AGENT_ORCHESTRATOR_DESIGN.md`: Architecture brainstorming for agentic orchestration.
  - `ARCHITECTURE.md`: Core system design, skill definitions, and pipeline overview.
  - `DOC_INDEX.md`: This file.
  - `ROADMAP.md`: Project status and upcoming features.
- `input_data/`: Directory for input PDF files to be processed.
- `output_data/`: Final processed data organized by ticker.
- `processing_data/`: Temporary directory for files currently being processed.
- `skills/`: Core logic and skills for the pipeline.
  - `document_classification/`: Skill for classifying documents.
  - `document_organization/`: Skill for organizing processed documents.
  - `financial_calculations/`: Skill for derived metric calculations.
  - `financial_data_extraction/`: Skill for extracting data from PDFs.
  - `financial_modeling/`: Skill for DCF and valuation modeling.
  - `model_json_generator/`: Skill for formatting metadata into structured JSON.
  - `qualitative_assessment/`: Skill for moat and margin assessment.
  - `PIPELINE.md`: Full pipeline runbook.
  - `SHARED_POSTRUN.md`: Post-pipeline execution tasks.
- `tmp/`: Temporary logs and scripts.
- `tools/`: Utility scripts and server startup batches.

## Skills Overview

See `skills/PIPELINE.md` for the full execution flow.
