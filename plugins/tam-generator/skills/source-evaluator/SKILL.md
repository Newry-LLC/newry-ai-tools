---
name: source-evaluator
description: >
  Evaluate the credibility, quality, and appropriate use of a data source for
  market sizing. Invoke when the user says "is this a good source", "can I use this
  in my TAM", "how credible is this report", "evaluate this source",
  "should I trust this data", "can I cite this", or pastes a citation, report
  excerpt, or URL they want to use in their analysis. Returns a quality tier
  rating, specific guidance on what the source can and cannot support, caveats
  to disclose, and recommendations for corroborating sources.
---

# Source evaluator

Apply the quality framework from the tam-analysis skill's `references/source-quality-standards.md` to evaluate any source the user provides.

## What to evaluate

The user will provide one of:
- A citation (author, title, organization, year)
- A URL or publication name
- An excerpt or passage from a report
- A data point and the source it came from
- A description of where they found a number

## Evaluation output

Return a structured assessment:

**Source:** [Name as provided]

**Quality tier:** Tier 1 / 2 / 3 / 4
[One sentence explaining why]

**What this source is good for:**
[Specific data types this source reliably supports — e.g., "global production volumes by species," "US facility counts," "directional market sizing"]

**What this source cannot support:**
[Specific claims this source is NOT reliable for — e.g., "this is a vendor report, so competitive share claims are not credible," "this data is from 2016 and the market has changed significantly"]

**Caveats to disclose if used:**
[What must be noted in any analysis that cites this source]

**Suitable for board/investor-grade analysis:** Yes / With caveats / No
[Brief rationale]

**Recommended corroborating sources:**
[1–3 specific sources that would validate or triangulate against this one — name the source, not just the category]

## Handling common scenarios

**Analyst reports (Grand View Research, MarketsandMarkets, Mordor Intelligence, etc.):**
- Always Tier 3 unless they cite primary sources you can verify
- Flag that their methodologies are typically undisclosed
- Recommend finding the primary source they drew from (often a government database or industry association report)
- Suitable for directional context, not as sole basis for a key number

**Company press releases or marketing materials:**
- Tier 4 — the company has an interest in the number being large (or small)
- Market share and TAM claims from competitors require independent verification
- Useful as a lead to find better sources

**Academic papers:**
- Tier 1 or 2 depending on journal quality and methodology
- Check: was this peer-reviewed? Is the methodology disclosed? Is the sample representative?
- Highly credible for technology performance data, economic modeling, and production statistics
- May have narrow scope — check external validity

**Government databases (FAO, USDA, NOAA, EPA):**
- Tier 1
- Note the data collection year (often lags 1–3 years behind publication)
- Check whether the geographic scope matches the TAM

**Old data (>5 years):**
- Flag the age prominently
- Check whether a more recent vintage exists
- Ask: has there been a structural market change since then? (Regulation, technology, COVID, etc.)
- If no better source exists: use it but caveat explicitly in the analysis

**Undated or undisclosed-methodology reports:**
- Treat as Tier 4 until methodology and date can be confirmed
- Do not use as a primary basis for any key number
