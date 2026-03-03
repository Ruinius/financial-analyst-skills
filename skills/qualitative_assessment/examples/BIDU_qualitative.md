# Qualitative Assessment Example: Baidu, Inc. (BIDU)

> Source: Morningstar Equity Analyst Report (Dec 30, 2025)

## Inputs

- **Document**: Morningstar analyst report on Baidu
- **Source date**: December 30, 2025
- **Author/firm**: Morningstar
- **Existing assessment**: None (first assessment for BIDU)

## Output

The following was appended to `BIDU_metadata.md`:

```markdown
## Qualitative Assessment

_Last updated: 2026-03-02 | Source: Morningstar Equity Analyst Report_

### Economic Moat

| Field      | Value                      |
| ---------- | -------------------------- |
| Rating     | Wide                       |
| Confidence | High                       |
| Source     | Morningstar (Dec 30, 2025) |

1. **Network Effect**: Baidu's dominant search market share creates a powerful data-driven network effect mapping user intents that attracts both users and advertisers.
2. **Intangible Assets**: Decades of compiled search and intent query data that powers best-in-class local Chinese search processing capabilities and ad conversions.
3. **High Competitive Barrier**: "Pull-based" explicit intent search queries continue to offer specialized ROAS values to ad-buyers that cannot be substituted purely by infinite-scroll social applications.

### EBITA Margin Outlook

| Field      | Value              |
| ---------- | ------------------ |
| Direction  | Shrink             |
| Magnitude  | -2 pp over 5 years |
| Confidence | Medium             |

1. **Revenue Mix Shift**: Lower-margin segments like Cloud and Gen AI continue to grow faster than high-margin internet search, mechanically placing downward pressure on margins.
2. **Advertising Headwinds**: A softer consumer macro environment causes traditional search advertising growth to stagnate and decline YoY, directly hitting the most profitable revenue line.
3. **Targeted Investment**: Heavy infrastructure capex and OpEx is required to scale the Ernie foundational model, offsetting recent efficiency gains.

### Organic Growth Outlook

| Field      | Value              |
| ---------- | ------------------ |
| Direction  | Increase           |
| Magnitude  | +4 pp over 5 years |
| Confidence | Medium             |

1. **AI-native Marketing Adoption**: Broad adoption of GenAI marketing tools (+262% YoY) promises to stabilize ROI for advertisers and bring pricing power back to Baidu's core ad products.
2. **Diversified Growth Drivers**: Strong continued momentum in Baidu Cloud (+21% YoY) and AI infra (+33% YoY) provides a secondary structural growth engine offsetting search declines.
3. **Post-Dip Stabilization**: Following the cyclical multi-year lows in advertising budgets, the base-effects for YoY comparisons will ease, creating a mechanical runway for stabilizing positive growth rates moving towards 2026.
```

## Downstream Effect on Assumptions

| Assessment             | Effect                                                               |
| ---------------------- | -------------------------------------------------------------------- |
| Moat = Wide            | Terminal growth = 4.0%, terminal margin = Stage 2 margin (sustained) |
| Margin: Shrink -2 pp   | Stage 2 margin = L4Q margin - 2 pp                                   |
| Growth: Increase +4 pp | Stage 2 growth = L4Q growth + 4 pp                                   |
