# Agentic Orchestration Architecture (Brainstorm)

> [!NOTE]
> This document is currently for **design and brainstorming purposes only**. The implementation details are still being evaluated, specifically regarding how to execute this architecture in a cost-effective way without relying on complex custom infrastructure or high-overhead API management.

## The Problem with the Current Pipeline

Currently, the `tiger-skills` pipeline (`skills/PIPELINE.md`) is fully sequential. It processes one file at a time from `input_data/` using a single continuous context window. This approach has significant drawbacks:
1. **Context Window Pollution / LLM Confusion:** As more documents are processed, the context window fills up with previous extractions, leading to hallucinated data or cross-contamination between companies/documents.
2. **Token Consumption:** Carrying the history of all previously processed documents into the processing of the next document wastes an enormous amount of tokens.
3. **Speed:** Processing documents sequentially is slow.

## Proposed Solution: Agentic Orchestrator Pattern

To resolve these issues, we can transition from a linear batch script to an **Orchestrator & Sub-Agent** architecture.

### Architecture Overview

1. **The Orchestrator (Main Controller)**
   - Acts as the central dispatcher.
   - Scans the `input_data/` directory to identify all pending documents.
   - Responsible for spawning, monitoring, and synchronizing sub-agents.
   - Does *not* process documents itself, keeping its context lightweight.

2. **Document Sub-Agents (Parallel Execution)**
   - The Orchestrator spawns a separate sub-agent for *each* document in `input_data/`.
   - Each Document Sub-Agent is completely isolated, possessing only the context of its assigned document.
   - **Responsibilities:**
     - Execute Phase 1 (Classification).
     - Route and execute Phase 2-4 (Financial Extraction/Calculation/Organization) OR Phase 5 (Qualitative Assessment).
   - Once the sub-agent successfully moves the processed file to `output_data/`, it terminates and reports success back to the Orchestrator.

3. **Synchronization Barrier**
   - The Orchestrator waits until all Document Sub-Agents have reported completion. This ensures all base data is extracted and organized before cross-document or company-level calculations occur.

4. **Financial Modeling Sub-Agent**
   - After the barrier is passed, the Orchestrator spawns a single `Financial Modeling Sub-Agent`.
   - **Responsibilities:**
     - Execute Phase 6 (Financial Modeling) for all tickers that now have sufficient data.
     - Because all underlying data is already extracted, this sub-agent only needs to reason over the clean `output_data` metadata, making it highly efficient.
   - Terminates and reports success.

5. **Shared Post-Run Sub-Agent**
   - Finally, the Orchestrator spawns the `Shared Postrun Sub-Agent`.
   - **Responsibilities:**
     - Execute the Post-Pipeline Epilogue.
     - Curate examples, update `SKILL.md` files with edge cases, and perform self-improvement tasks.
     - Aggregates insights from the entire run without polluting the actual extraction logic.

## Key Benefits
- **Zero Cross-Contamination:** Each document extraction is perfectly isolated.
- **Cost Efficiency:** Token usage scales linearly with the document size rather than exponentially with the number of documents in a batch.
- **Speed:** Document extraction can be fully parallelized.
- **Maintainability:** Clear separation of concerns (Extraction vs. Modeling vs. Maintenance).
