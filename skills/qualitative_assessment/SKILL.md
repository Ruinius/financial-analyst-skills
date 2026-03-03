---
name: Qualitative Assessment
description: Assess a company's economic moat, EBITA margin trajectory, and organic growth trajectory from analyst reports, earnings transcripts, or long-form articles. Produces structured qualitative outlook that feeds into the Financial Modeling skill's assumption generation.
---

# Qualitative Assessment Skill

## Purpose

This skill reads qualitative source documents (analyst reports, earnings call transcripts, press articles) and produces a structured assessment of three dimensions that directly feed into the DCF model assumptions:

1. **Economic Moat** — determines terminal growth rate and margin sustainability
2. **EBITA Margin Outlook** — adjusts Stage 2 margin assumptions (+/- pp)
3. **Organic Growth Outlook** — adjusts Stage 2 growth assumptions (+/- pp)

Without this skill, the Financial Modeling skill falls back to pure historical trend continuation, which misses forward-looking information.

## Prerequisites

- The document must already be classified (Skill 1) — ticker, company name, and document type known
- The company's `output_data/TICKER/` directory must already exist (i.e., at least one financial report has been processed)
- `TICKER_metadata.md` should exist with a Financial History table for context

## Inputs

- Classified document in `processing_data/` (analyst report, transcript, or article)
- `output_data/TICKER/TICKER_metadata.md` — for existing assessments to compare/harmonize

## Outputs

- Updated `TICKER_metadata.md` with Qualitative Assessment section (new or harmonized with existing)

---

## Step-by-Step Instructions

### Step 1: Read the Source Document

Read the classified document from `processing_data/`. Identify:

- **Source type**: Analyst report, earnings transcript, press article, etc.
- **Source date**: Publication or earnings call date
- **Author/firm**: e.g., "Morningstar (Dan Romanoff, CPA)"

Also read the company's `TICKER_metadata.md` to check for any existing Qualitative Assessment.

### Step 2: Assess Economic Moat

Determine the company's economic moat rating: **Wide**, **Narrow**, or **None**.

| Rating     | Definition                                                                                                                                                        | Terminal Growth Implication |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| **Wide**   | Structural advantages expected to sustain excess ROIC for 20+ years. Dominant network effects, high switching costs, or irreplaceable intangible assets.          | Terminal growth = 4.0%      |
| **Narrow** | Clear competitive advantage, but likely to face erosion within 10-20 years. Currently outperforming cost of capital but not deep enough for long-term protection. | Terminal growth = 3.0%      |
| **None**   | Highly commoditized or intensely competitive. No sustainable advantage. Short-term excess profits are quickly competed away.                                      | Terminal growth = 2.5%      |

For each moat rating, provide:

- **Rating**: Wide / Narrow / None
- **Confidence**: High / Medium / Low
- **Source**: Document name and date
- **Three bullets of rationale** — each should be specific, cite evidence from the document, and name the moat source (network effects, switching costs, intangible assets, cost advantage, or efficient scale)

> 💡 If the source document explicitly states a moat rating (e.g., Morningstar reports), use that rating and cite it. Your rationale should support or contextualize their assessment.

### Step 3: Assess EBITA Margin Trajectory

Determine whether the company's EBITA margin will **expand** or **shrink** over the next 5 years, and by how much.

| Field          | How to Determine                        |
| -------------- | --------------------------------------- |
| **Direction**  | Expand / Shrink / Stable                |
| **Magnitude**  | +/- 1-4 pp over 5 years (typical range) |
| **Confidence** | High / Medium / Low                     |

For the three bullets of rationale, consider:

- Revenue mix shifts (high-margin vs. low-margin segments growing at different rates)
- Operating leverage (fixed costs being spread over growing revenue)
- Investment cycles (R&D, capex ramps that pressure near-term margins)
- Competitive pricing pressure
- Regulatory costs

> ⚠️ Be conservative. A +2 pp expansion over 5 years is significant. Moves larger than ±4 pp require very strong evidence.

### Step 4: Assess Organic Growth Trajectory

Determine whether the company's organic revenue growth will **increase** or **decrease** relative to the current L4Q trend, and by how much.

| Field          | How to Determine                              |
| -------------- | --------------------------------------------- |
| **Direction**  | Increase / Decrease / Stable                  |
| **Magnitude**  | +/- 1-4 pp over 5 years relative to L4Q trend |
| **Confidence** | High / Medium / Low                           |

For the three bullets of rationale, consider:

- TAM expansion or saturation
- New product launches and adoption curves
- Competitive dynamics and market share trends
- Macro/cyclical headwinds or tailwinds
- Management guidance and forward-looking commentary
- Base effects (easy or tough YoY comparisons)

### Step 5: Harmonize with Existing Assessment

If `TICKER_metadata.md` already has a Qualitative Assessment section:

1. **Compare** each dimension (moat, margin, growth) with the existing assessment
2. **If the new source agrees** with the existing assessment: keep the existing, update the "Last updated" date and source
3. **If the new source disagrees**:
   - Consider recency (more recent = more weight)
   - Consider source quality (Morningstar analyst > news article)
   - Consider confidence levels
   - Update the assessment if the new evidence is stronger; otherwise keep existing and note the disagreement in a comment

### Step 6: Write Output to Markdown

Write or update the following section in `TICKER_metadata.md`:

```markdown
---

## Qualitative Assessment

_Last updated: {date} | Source: {source_description}_

### Economic Moat

| Field      | Value                  |
| ---------- | ---------------------- |
| Rating     | **{Wide/Narrow/None}** |
| Confidence | {High/Medium/Low}      |
| Source     | {source and date}      |

1. **{Moat Source 1}**: {specific evidence from the document}
2. **{Moat Source 2}**: {specific evidence}
3. **{Moat Source 3}**: {specific evidence}

### EBITA Margin Outlook

| Field      | Value                      |
| ---------- | -------------------------- |
| Direction  | **{Expand/Shrink/Stable}** |
| Magnitude  | {+/- N pp over 5 years}    |
| Confidence | {High/Medium/Low}          |

1. {Specific rationale with evidence}
2. {Specific rationale with evidence}
3. {Specific rationale with evidence}

### Organic Growth Outlook

| Field      | Value                          |
| ---------- | ------------------------------ |
| Direction  | **{Increase/Decrease/Stable}** |
| Magnitude  | {+/- N pp over 5 years}        |
| Confidence | {High/Medium/Low}              |

1. {Specific rationale with evidence}
2. {Specific rationale with evidence}
3. {Specific rationale with evidence}
```

### Step 7: Move Source Document

Move the processed document from `processing_data/` to `output_data/TICKER/`:

- Rename to remove the `_temp` suffix
- Both the PDF and the markdown file

---

## How Downstream Skills Use This Output

The Financial Modeling assumptions skill (`skills/financial_modeling/assumptions/`) reads this section to adjust historical trends:

| Assessment                         | Downstream Effect                                                       |
| ---------------------------------- | ----------------------------------------------------------------------- |
| **Economic Moat = Wide**           | Terminal growth 4.0%, terminal margin = Stage 2 margin (sustained)      |
| **Economic Moat = Narrow**         | Terminal growth 3.0%, terminal margin converges toward industry average |
| **Economic Moat = None**           | Terminal growth 2.5%, terminal margin = industry average                |
| **EBITA Margin: Expand +2 pp**     | Stage 2 margin = L4Q margin + 2 pp                                      |
| **EBITA Margin: Shrink -2 pp**     | Stage 2 margin = L4Q margin - 2 pp                                      |
| **Organic Growth: Increase +4 pp** | Stage 2 growth = L4Q growth + 4 pp                                      |
| **Organic Growth: Decrease -1 pp** | Stage 2 growth = L4Q growth - 1 pp                                      |

If no qualitative assessment exists, the assumptions skill defaults to **Narrow moat** behavior and **pure historical continuation**.

---

## Important Notes

- **Be specific, not generic.** Every rationale bullet should cite evidence from the source document — numbers, quotes, product names, dates. Avoid vague statements like "strong brand" or "good management."
- **Three bullets per dimension, no more.** Forces prioritization of the most important factors.
- **Magnitude matters.** "+2 pp" and "+4 pp" produce very different DCF outcomes. Be precise and conservative.
- **Confidence is about the evidence quality**, not your personal certainty. A Morningstar deep-dive = High. A single news article = Low.
- **The margin and growth outlooks are relative to the current L4Q trend**, not absolute targets. If L4Q margin is 38% and you say "Expand +2 pp", the assumptions skill will set Stage 2 margin to 40%.

## Reference

Based on `extract_qualitative_assessment()` in `tiger-cafe/app/app_agents/qualitative_extractor.py`, adapted from LLM-only assessment to document-grounded analysis.
