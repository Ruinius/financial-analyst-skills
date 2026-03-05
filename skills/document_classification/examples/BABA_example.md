# Example: Alibaba Group Holding Limited (BABA) Q3 FY2024

**Input:** Unprocessed PDF `input_data/Alibaba Group Announces December Quarter 2023 Results.pdf`.
**Action:** Document Classifier extracts dates, notes non-calendar fiscal year (Dec 31 is Q3 for BABA), verifies ticker via Yahoo Finance, and writes initial markdown file to `processing_data/BABA_EA_20240207_temp.md`.

## Output Appended to Markdown

```markdown
# Document Classification

| Field               | Value                                                     |
| ------------------- | --------------------------------------------------------- |
| Company Name        | Alibaba Group Holding Limited                             |
| Ticker              | BABA                                                      |
| Document Type       | earnings_announcement                                     |
| Document Date       | 2024-02-07                                                |
| Time Period         | Q3 2024                                                   |
| Period End Date     | 2023-12-31                                                |
| Confidence          | high                                                      |
| Original Filename   | Alibaba Group Announces December Quarter 2023 Results.pdf |
| Classification Date | 2026-03-05                                                |

---

<!-- Sections below will be populated by subsequent skills -->
```
