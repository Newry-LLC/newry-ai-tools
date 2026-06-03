# Source quality standards

A tiered framework for evaluating and citing data sources in TAM analysis. Every material data point must have a named source at Tier 3 or above. Tier 4 sources require a Tier 1–3 corroboration.

---

## Tier 1 — Primary / government / regulatory (highest confidence)

These sources carry the highest credibility and should be preferred wherever available.

**Examples:**
- Government statistical agencies: USDA NASS, NOAA fisheries, FAO (UN Food and Agriculture Organization), EPA, FDA, EU Eurostat, national statistics offices
- Regulatory filings: SEC 10-K, 10-Q, 20-F; EU prospectuses
- Central bank and trade ministry data
- International organizations: World Bank, OECD, ITC Trade Map
- Patent databases (for technology adoption proxies): USPTO, EPO

**Use for:** Customer counts, production volumes, trade statistics, equipment installation counts, regulatory compliance scope

**Caveats:**
- Government data often lags 1–3 years — note the publication date
- Definitions vary by country — reconcile before combining

**How to cite:**
`[Agency], "[Report title]," [Country/Organization], [Year], [URL or database name]`

---

## Tier 2 — Industry associations and academic research (high confidence)

Highly credible, often more specific to niche markets than government data.

**Examples:**
- Trade associations: Aquaculture Association of America, Water Quality Association, AWWA, IAFMM, FishTech, etc.
- Academic journals: peer-reviewed research with methodology disclosed
- Industry census reports produced by associations (membership surveys, installation databases)
- Conference proceedings from established industry conferences

**Use for:** Industry-specific production figures, technology adoption rates, customer pain points and economics, niche market structure

**Caveats:**
- Association data may reflect member-only statistics — ask if they're representative of full market
- Academic research may focus on narrow conditions — check external validity

**How to cite:**
`[Association/Author], "[Report/Paper title]," [Publication/Journal], [Year], [URL or DOI]`

---

## Tier 3 — Reputable analyst firms and trade press (medium confidence)

Useful for top-down sizing and market structure. Must always be triangulated against Tier 1/2 sources — do not use as sole basis for a material number.

**Examples:**
- Major analyst firms: IBISWorld, Grand View Research, MarketsandMarkets, Mordor Intelligence, Frost & Sullivan, Wood Mackenzie, GlobalData
- Reputable trade publications: Fish Farming Expert, Water & Wastes Digest, Aquaculture Magazine, Chemical Week
- Mainstream business press citing named industry sources: Reuters, Bloomberg, WSJ, FT

**Use for:** Broad market context, growth rates, competitive landscape overview, quick directional sizing

**Caveats:**
- Analyst report methodologies are often undisclosed — treat ranges as directional, not precise
- Market definitions vary widely between reports — always check the scope section
- Some "reports" from lower-tier firms are algorithmically generated with no primary research
- Do not use as the sole basis for any key assumption in an investor-grade analysis

**How to cite:**
`[Firm], "[Report title]," [Year], [Report page/URL if available]`
Note explicitly: "Triangulated against [Tier 1/2 source]"

---

## Tier 4 — Company-generated and unverified (low confidence — must corroborate)

Treat these as leads and hypotheses, not evidence. Every material claim from a Tier 4 source must be verified against a Tier 1–3 source before use.

**Examples:**
- Company press releases, marketing materials, website claims
- Competitor market share claims in pitch decks or sales materials
- Unattributed blog posts, LinkedIn articles
- AI-generated summaries without cited primary sources
- Analyst reports from unknown firms (no methodology disclosed)
- Social media, forum posts, community surveys

**Use for:** Generating hypotheses to test; identifying what questions to ask of better sources

**How to cite:**
`[Company/Author], "[Title/Source]," [Date], [URL]`
Flag: "Tier 4 — requires corroboration. Not used as standalone evidence."

---

## Source age standards

| Age | Status |
|-----|--------|
| 0–3 years | Current — use freely |
| 3–5 years | Acceptable — note the date, flag if market is changing rapidly |
| 5–10 years | Use with caution — explicitly note age, check for more recent data |
| >10 years | Exclude or flag as historical baseline only — do not use for current sizing |

Exception: Long-dated government census data (e.g., FAO fisheries statistics) may be the best available — use it but note the vintage and any known structural changes since publication.

---

## Source evaluation checklist

For any source, ask:
- [ ] Who produced it, and what is their incentive? (Industry association vs. vendor marketing)
- [ ] What methodology did they use? Is it disclosed?
- [ ] What is the geographic scope? Does it match our TAM scope?
- [ ] What is the product/market definition? Does it match ours precisely?
- [ ] When was the data collected? (Not just the publication date — when was the fieldwork done?)
- [ ] Is this a primary source or is it citing another source? Trace to the primary.
- [ ] Does this number appear in multiple independent sources? (Corroboration adds confidence)

---

## Handling conflicting sources

When two credible sources give different numbers:
1. Check if the market definitions are actually the same
2. Check the data collection dates
3. Check geography scope
4. If all aligned and they still differ: use both, state the range, explain possible causes of divergence
5. Do not silently pick the number that supports your hypothesis

Document the conflict in the "Limitations and caveats" section of the output.
