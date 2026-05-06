---
name: Shared Post-Run Steps
description: Example curation and self-improvement steps shared by all skills. Each skill references this file with its own examples folder path.
---

# Post-Run Steps

After completing a skill, perform both of these steps using the **examples folder** specified by the calling skill.

---

## Example Curation

### 1. Save the Current Run as a New Example

- Copy the **output produced by this skill run** into the examples folder as a new `.md` file.
- Naming convention: `TICKER_example.md` (e.g., `AAPL_example.md`, `MSFT_example.md`).
- The example file should contain:
  - The **complete output** this skill produced (all tables, sections, and values)
  - A brief header noting the source (ticker, document date, period)
  - The **calculation walkthrough** if this is a calculation skill — show intermediate values so a reader can follow the logic

### 2. Review All Examples

- List every `.md` file in the skill's examples folder
- Read each example file and evaluate it on these criteria:
  | Criterion | What to look for |
  |-----------|-----------------|
  | **Completeness** | Does it show ALL output fields this skill produces? |
  | **Correctness** | Are the values accurate and internally consistent? |
  | **Edge coverage** | Does it demonstrate interesting edge cases or fallback logic? |
  | **Clarity** | Is it well-formatted and easy to follow as a reference? |

### 3. Curation and Retention

- Compare the new run against existing examples.
- **Bias toward retention:** Do NOT replace an existing example unless the new one is **significantly superior** (better formatting, more complex data, or clearer logic).
- **Diversity of Examples:** You may keep up to **3 high-quality examples** in the folder IF they demonstrate fundamentally different scenarios (e.g., a simple case vs. a complex ADR case vs. a case with significant non-GAAP adjustments).
- **Delete redundant or inferior examples** to keep the folder lean and high-signal.
- The surviving examples should serve as the **gold-standard reference** for the skill.

> ⚠️ **Rules for example curation:**
>
> - Maintain **at least 1 and at most 3** example files in the folder.
> - **Replacement Bar:** Only replace an existing example if the new one covers the same scenario but with 100% accuracy and better clarity.
> - **Scenario Coverage:** Prioritize examples that cover different "Document Types" or complex accounting treatments (e.g., currency translations).
> - NEVER keep a partial or broken example over a complete one.
> - If the new run adds no new signal or clarity compared to existing ones, **delete the new run's file.**
> - Surviving files must follow the `TICKER_example.md` naming convention.

---

## Self-Improvement

1. **Reflect on the run.** Review what happened during this execution:
   - Did any step fail or require retry?
   - Were there ambiguities in the instructions that caused hesitation or errors?
   - Did you discover an edge case not covered by the current instructions?
   - Was any output wrong, incomplete, or required manual correction?

2. **Propose and apply improvements.** If you identified any issue, update the calling skill's `SKILL.md` file directly. Improvements can include:
   - Adding new edge case handling or fallback logic
   - Clarifying ambiguous wording in existing steps
   - Adding validation checks that would have caught an error earlier
   - Updating examples to cover newly discovered patterns
   - Removing or correcting outdated instructions

3. **Log the change.** Append a brief entry to the changelog at the bottom of the skill's `SKILL.md` so the improvement history is tracked.

> ⚠️ **Rules for self-edits:**
>
> - NEVER delete or weaken existing validation rules — only add or strengthen them
> - Keep changes surgical and focused — do not rewrite sections that are working fine
> - If unsure whether a change is correct, add it as a `> ⚠️ NOTE:` rather than modifying instructions
> - Each changelog entry must include the date and a one-line description
