---
name: Document Organization
description: Execute a single deterministic Python script to harmonize units, create/update metadata, move files to output_data/, and clean up input_data/.
---

# Document Organization (Phase 4)

All organization logic is consolidated into a single script that handles the complete lifecycle: classification parsing, unit harmonization, metadata management, file archival, and input cleanup.

1. Execute the script: `python skills/document_organization/scripts/organize.py {markdown_file}`
2. Verify no errors were thrown.

## What the Script Does

| Step | Action | Details |
|------|--------|---------|
| 1 | Read Classification | Extracts ticker, company name, document type, dates, currency from the classification table |
| 2 | Harmonize Units | Detects prevailing unit from BS/IS, converts Shares Outstanding and Organic Growth values if they differ. Supports: ones, thousands, ten_thousands (万), millions, hundred_millions (億), billions |
| 3 | Read Financial Summary | Extracts Revenue, EBITA, NOPAT, ROIC, Growth etc. for metadata |
| 4 | Create/Update Metadata | Creates or updates `output_data/TICKER/TICKER_metadata.md` with document entry + financial history row. Handles deduplication and date sorting |
| 5 | Move & Cleanup | Moves `.md` and `.pdf` from `processing_data/` → `output_data/TICKER/` (removing `_temp` suffix). Deletes matching source PDF from `input_data/` |
| 6 | Verify | Confirms destination files exist and source files are removed |

## Unit Conversion Reference

The script uses a deterministic conversion table:

| Unit | Factor to Ones | Alias |
|------|---------------|-------|
| ones | 1 | — |
| thousands | 1,000 | thousand |
| ten_thousands | 10,000 | 万 |
| millions | 1,000,000 | million |
| hundred_millions | 100,000,000 | 億 |
| billions | 1,000,000,000 | billion |

## Metadata Management

- **New ticker**: Creates `TICKER_metadata.md` with header, processed documents table, and financial history table
- **Existing ticker**: Appends new rows, sorts by period end date, deduplicates by time period (re-processing overwrites)
- **Last Updated** field is always refreshed

## Error Handling

- Missing source files → warns and continues
- Unknown units → raises ValueError with descriptive message
- Duplicate time periods → replaces existing row (re-processing scenario)
- Missing input_data/ files → logs info message (may have been manually cleaned)

## Cross-Document Date Healing

Date healing (checking fiscal calendar consistency) is NOT automated by this script. If the agent identifies date inconsistencies after reviewing the metadata, it should flag them manually in the metadata file per the original SKILL instructions (Step 6 of the legacy spec).
