# OpenCode Orchestrator Architecture (Design)

> [!NOTE]
> This document is currently for **design and brainstorming purposes only**. The implementation details are still being evaluated, specifically regarding how to execute this architecture in a cost-effective way without relying on complex custom infrastructure or high-overhead API management.

## The Problem with the Current Pipeline

Currently, the `tiger-skills` pipeline (`skills/PIPELINE.md`) is fully sequential. It processes one file at a time from `input_data/` using a single continuous context window. This approach has significant drawbacks:

1. **Context Window Pollution / LLM Confusion:** As more documents are processed, the context window fills up with previous extractions, leading to hallucinated data or cross-contamination between companies/documents.
2. **Token Consumption:** Carrying the history of all previously processed documents into the processing of the next document wastes an enormous amount of tokens.
3. **Speed:** Processing documents sequentially is slow.

To resolve these issues, we are transitioning from a linear batch script to an **OpenCode Orchestrator & Sub-Agent** architecture.

## Proposed Architecture: OpenCode in Docker

The entire tiger-skills system would be re-hosted inside a **Docker container** running an **OpenCode** instance. OpenCode replaces Antigravity as the agentic runtime, and the current `SKILL.md` files are converted into OpenCode agents and tools. The Docker container provides a reproducible, portable environment that bundles OpenCode, the Tiger-Transformer model, and all Python dependencies.

### Infrastructure Layer

```
┌─────────────────────────────────────────────────┐
│  Docker Container                               │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │  OpenCode (Orchestrator)                  │  │
│  │  - Reads PIPELINE.md as its system prompt │  │
│  │  - Spawns sub-agents per document         │  │
│  │  - Assigns models per task complexity     │  │
│  └────────┬──────────┬───────────┬───────────┘  │
│           │          │           │               │
│     ┌─────▼──┐ ┌─────▼──┐ ┌─────▼──────┐       │
│     │Sub-Agt │ │Sub-Agt │ │ Sub-Agt    │       │
│     │Deepseek│ │  GLM   │ │   KIMI     │       │
│     │(cheap) │ │(medium)│ │ (reasoning)│       │
│     └────────┘ └────────┘ └────────────┘       │
│                                                 │
│  ┌─────────────────────┐  ┌──────────────────┐  │
│  │ Tiger-Transformer   │  │ market_data.py   │  │
│  │ (localhost:8000)     │  │ (Yahoo Finance)  │  │
│  └─────────────────────┘  └──────────────────┘  │
│                                                 │
│  Volume Mounts:                                 │
│    /input_data  → host input_data/              │
│    /output_data → host output_data/             │
└─────────────────────────────────────────────────┘
```

### How It Works

1. **OpenCode Orchestrator** — A single OpenCode instance acts as the main controller. It reads `PIPELINE.md` as its system prompt, scans `input_data/` for pending documents, and dispatches work to sub-agents. It does _not_ process documents itself, keeping its context lightweight.

2. **Sub-Agent Spawning** — For each document, the Orchestrator spawns an isolated OpenCode sub-agent. Each sub-agent receives:
   - A specific **model assignment** (e.g., Deepseek for extraction, KIMI for qualitative reasoning).
   - The relevant **skill instructions** (converted from current `SKILL.md` files into OpenCode agent definitions).
   - Only the context of its assigned document — zero cross-contamination.

3. **Synchronization** — The Orchestrator waits for all document-level sub-agents to complete before spawning the modeling phase. This barrier ensures all base data is written to `output_data/` before cross-ticker analysis begins.

4. **Modeling Phase** — A single sub-agent executes Phase 6 (Financial Modeling) and Phase 7 (JSON Generation) across all tickers with sufficient data. This agent reasons over the clean, finalized metadata.

5. **Post-Run** — A final sub-agent curates examples, updates skill files, and performs self-improvement tasks.

### Skill → Agent Migration

The existing Antigravity skills map directly to OpenCode agents:

| Current Antigravity Skill    | OpenCode Agent             | Notes                                        |
| ---------------------------- | -------------------------- | -------------------------------------------- |
| `document_classification/`   | `classify-document` agent  | Structural task, lightweight model           |
| `financial_data_extraction/` | `extract-financials` agent | Complex reasoning, heavyweight model         |
| `financial_calculations/`    | Python script (tool call)  | Deterministic — no LLM needed, just `uv run` |
| `document_organization/`     | `organize-document` agent  | Structural task, lightweight model           |
| `qualitative_assessment/`    | `assess-qualitative` agent | Deep reasoning, heavyweight model            |
| `financial_modeling/`        | Python script (tool call)  | Deterministic — no LLM needed, just `uv run` |
| `model_json_generator/`      | Python script (tool call)  | Deterministic — no LLM needed, just `uv run` |

> [!TIP]
> Phases 3, 6, and 7 are fully deterministic Python scripts. In OpenCode, these don't need an LLM sub-agent at all — the orchestrator can invoke them directly as tool calls, saving significant cost.

### Model Tiering Strategy

The core advantage of OpenCode is the ability to assign **different LLM providers** to different sub-agents based on task complexity:

| Tier              | Models (candidates)              | Assigned Phases                                  | Rationale                                                                         |
| ----------------- | -------------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------- |
| **Lightweight**   | Deepseek-V3, GLM-4-Flash         | Phase 1 (Classification), Phase 4 (Organization) | Structural, pattern-matching tasks. Fast and cheap.                               |
| **Heavyweight**   | KIMI-K2, GLM-4-Plus, Deepseek-R1 | Phase 2 (Extraction), Phase 5 (Qualitative)      | Requires deep reasoning over complex financial tables and qualitative narratives. |
| **None (Script)** | —                                | Phase 3, 6, 7                                    | Pure Python. No LLM invocation.                                                   |

> [!NOTE]
> Model selection is not final. The goal is to benchmark multiple providers on extraction accuracy and cost-per-document, then lock in the best tier assignments.

### Key Benefits

- **Zero Cross-Contamination:** Each document gets its own sub-agent with isolated context.
- **Cost Optimization:** Cheap models for simple tasks, expensive models only where reasoning matters, and no LLM at all for deterministic scripts.
- **Parallelism:** Document-level sub-agents can run concurrently.
- **Portability:** The entire system runs inside a single Docker container. Clone, build, run.
- **Model Flexibility:** Swap providers without changing any skill logic — just update the orchestrator's model assignments.

### Open Questions

- [ ] How does OpenCode handle sub-agent spawning concurrency? Is there a max parallelism setting?
- [ ] What's the best way to pass the Tiger-Transformer server URL to sub-agents inside the container?
- [ ] Should the Docker image bundle the transformer model weights, or mount them from the host?
- [ ] How to handle API key management for multiple LLM providers (Deepseek, GLM, KIMI) inside the container?
- [ ] What is the error recovery strategy when a sub-agent fails mid-extraction?
