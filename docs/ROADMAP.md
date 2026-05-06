# Tiger-Skills Roadmap

This document outlines the development status and upcoming features for the Tiger-Skills project.

## Current Status (Q1 2026)

- [x] **Phase 1-4**: Core extraction and organization pipeline (stable).
- [x] **Phase 5**: Qualitative assessment (Economic Moat, Margin/Growth trajectory).
- [x] **Phase 6**: Financial modeling (WACC, DCF, Intrinsic Value).
- [x] **Phase 7**: Model JSON Generator (isolated from modeling logic).
- [x] **Interactive Viewer**: Vanilla JS viewer with scenario saving.

---

## Upcoming Features (Next 2-4 Weeks)

### 1. OpenCode Migration & Docker Containerization
- Migrate the entire tiger-skills runtime from **Antigravity** to **OpenCode** inside a **Docker container**. Full design in `docs/AGENT_ORCHESTRATOR_DESIGN.md`.
- Convert existing `SKILL.md` files into OpenCode agents and tools. Deterministic scripts (Phases 3, 6, 7) become direct tool calls — no LLM needed.
- **Multi-Model Sub-Agents**: OpenCode spawns isolated sub-agents backed by different LLM providers (Deepseek, GLM, KIMI) based on task complexity.
- **Model Tiering**: Lightweight models (Deepseek-V3, GLM-4-Flash) for structural phases (1, 4). Heavyweight models (KIMI-K2, Deepseek-R1) for extraction and qualitative reasoning (2, 5).
- Eliminates cross-document contamination, reduces token waste, and enables parallel document processing.

### 2. Phase 8: Comparative Analysis Skill
- Build a skill that aggregates data from multiple tickers in `output_data/`.
- Generate comparative valuation tables (P/E, EV/EBITA, ROIC vs. Cost of Capital) for peer groups.
- Output a `sector_comparison.md` report.

### 3. Automated Gold-Standard Evaluation
- Create a "Testing" skill that compares AI extractions against hand-coded financial models for known tickers (e.g., ADBE).
- Generate "Accuracy Score" reports to identify extraction weaknesses.

---

## Long-term Vision (Q2 2026+)

### 4. Multi-Modal Extraction
- Integrate vision-based extraction for financial charts and graphs that are missed by text-based parsing.
- Support for complex table layouts in quarterly presentations (non-standard formatting).

### 5. Mobile-Optimized Viewer
- Refactor `financial_model_viewer.html` for better mobile responsiveness.
- PWA support for offline model viewing.

### 6. Portfolio Integration
- Aggregate individual ticker models into a portfolio-level view.
- Weighted average intrinsic value vs. market price for the entire portfolio.


