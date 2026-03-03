# Qualitative Assessment Example: Adobe Inc. (ADBE)

> Source: Morningstar Equity Analyst Report (Jan 13, 2026) by Dan Romanoff, CPA

## Inputs

- **Document**: Morningstar analyst report on Adobe
- **Source date**: January 13, 2026
- **Author/firm**: Morningstar (Dan Romanoff, CPA)
- **Existing assessment**: None (first assessment for ADBE)

## Output

The following was appended to `ADBE_metadata.md`:

```markdown
## Qualitative Assessment

_Last updated: 2026-03-02 | Source: Morningstar Equity Analyst Report (2026-01-13)_

### Economic Moat

| Field      | Value                           |
| ---------- | ------------------------------- |
| Rating     | **Wide**                        |
| Confidence | High                            |
| Source     | Morningstar (Dan Romanoff, CPA) |

1. **Switching costs in Creative Cloud** — De facto industry standard; nearly impossible to replace at an industry-wide level.
2. **First-mover dominance in Document Cloud** — Created the PDF format; Acrobat remains the gold standard with no truly competitive alternative.
3. **Cross-selling flywheel** — 22,000+ enterprise customers buying 5+ products; natural expansion from content creation to marketing/advertising.

### EBITA Margin Outlook

| Field      | Value                             |
| ---------- | --------------------------------- |
| Direction  | **Expand**                        |
| Magnitude  | +2 pp over 5 years (~0.4 pp/year) |
| Confidence | Medium                            |

1. Declining R&D intensity as generative AI (Firefly) matures past heavy investment phase.
2. Already stellar margins (47.5% non-GAAP operating) limit upside but demonstrate disciplined cost control.
3. AI monetization ($125M ARR, doubling) creates incremental high-margin operating leverage.

### Organic Growth Outlook

| Field      | Value                         |
| ---------- | ----------------------------- |
| Direction  | **Stable to slight decrease** |
| Magnitude  | -1 pp (from ~11% to ~10%)     |
| Confidence | Medium                        |

1. Fiscal 2026 ARR guidance calls for deceleration to 10.2% growth — the "one obvious blemish."
2. AI tailwinds are real but still <1% of total revenue; not yet enough to offset mature Creative Cloud deceleration.
3. Tiered AI pricing structure provides a floor; three consecutive quarters of revenue upside support stable demand.
```

## Downstream Effect on Assumptions

| Assessment             | Effect                                                               |
| ---------------------- | -------------------------------------------------------------------- |
| Moat = Wide            | Terminal growth = 4.0%, terminal margin = Stage 2 margin (sustained) |
| Margin: Expand +2 pp   | Stage 2 margin = 37.93% + 2.0pp = 39.93%                             |
| Growth: Decrease -1 pp | Stage 2 growth = 10.5% - 1.0pp = 9.5%                                |
