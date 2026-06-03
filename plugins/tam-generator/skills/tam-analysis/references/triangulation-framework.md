# Triangulation framework

Detailed methodology, formulas, and worked examples for all four TAM triangulation methods, plus growth rate and dual-metric calculation standards.

---

## Dual-metric requirement

Every estimate must be expressed in both:
1. **Volume** — the primary physical unit (MT of media, units installed, liters treated, number of customers)
2. **Value** — $USD revenue at a stated point in the value chain (ex-works manufacturer price, distributor price, end-customer spend)

The bridge between them is always an explicit price assumption:
```
Value ($) = Volume (units) × Price ($/unit)
```
The price assumption must appear as its own auditable row in every calculation table, with a source and confidence level. If price varies by segment, compute each segment separately then sum.

---

## Growth rate calculation standards

### CAGR formula
```
CAGR = (End value / Start value)^(1 / number of years) − 1
```

Always show:
- Base year value (volume + $)
- Each intermediate year if a projection is requested (year-by-year bridge)
- Target year value (volume + $)
- CAGR for both volume and value separately — they will differ if prices are changing

### Growth driver decomposition
Decompose the total CAGR into its component drivers. Use a multiplicative decomposition:
```
Total value CAGR ≈ Volume CAGR + Price CAGR + (Volume × Price interaction, usually small)
```

For each driver, state:
- What is causing it (new facilities, increased adoption, regulatory pressure, price inflation)
- The basis for the growth rate assumption (sourced growth rate from a Tier 1/2 source, or a proxy)
- Whether it is structural (durable) or cyclical (temporary)

### When to use different growth proxies
| Driver | Best proxy source |
|---|---|
| New facility additions | RAS market CAGR from industry reports (Tier 3), triangulated against announced project pipeline |
| Adoption rate increase | Technology S-curve logic; current penetration vs. ceiling |
| Price change (media) | Commodity pricing indices (activated carbon price data from IMARC, BusinessAnalytiq) |
| Regulatory tailwind | Timeline of specific regulation taking effect |
| Market displacement (GAC losing to ozone/UV) | Technology substitution rate — look for analogous transitions |

### Honest growth rate practice
- Do not simply apply an industry-level CAGR to a niche sub-segment without justification
- If the niche is growing faster than the broader market, explain why
- If the niche is growing slower, explain why
- Always state the CAGR source and what it covers (the whole market vs. the specific segment)
- Distinguish between historical CAGR (measured) and projected CAGR (estimated) — they are different claims

---

## Method 1: Top-down

### When to use
Always. This is the baseline method. Works best when credible industry-level data exists.

### Formula
```
TAM = Broad market size
    × Segment filter 1 (e.g., relevant application share)
    × Segment filter 2 (e.g., relevant geography share)
    × Segment filter 3 (e.g., relevant customer type share)
    × ... (apply as many filters as needed)
```

### Process
1. Find the largest credible market figure that contains your target (e.g., "global water treatment chemicals market," "global aquaculture market," "global activated carbon market")
2. Apply a chain of narrowing filters, each documented with a source and % value
3. Run pessimistic, central, and optimistic scenarios by varying the filter percentages within defensible ranges
4. Document what each filter represents and why the percentage is appropriate

### Source requirements
- The root market figure must come from a Tier 1 or Tier 2 source
- Each filter percentage needs a source — if no direct source, document the proxy logic
- If applying multiple filters, confirm they are independent (not double-counting)

### Common pitfalls
- Starting from a market definition that is too broad (inflates TAM)
- Applying filters without sources (looks arbitrary to skeptics)
- Not accounting for overlap between segments
- Using outdated root figures

### Worked example (geosmin/aquaculture)
```
Global recirculating aquaculture system (RAS) market: ~$1.2B (2024, Grand View Research)
× Share of RAS facilities with documented taste/odor problems: ~40% (FAO 2022 aquaculture quality report)
× Share where geosmin is primary driver vs. other compounds: ~60% (proxy: industry expert interviews)
× Filtration/treatment solution addressability: ~70% (not all use filtration — some use ozone only)

TAM (top-down, central) = $1.2B × 0.40 × 0.60 × 0.70 = ~$202M
Range: $120M – $290M depending on filter assumptions
```

---

## Method 2: Bottom-up

### When to use
Always. This is the most defensible method for B2B niche markets. Requires a customer census or credible estimate of the customer population.

### Formula
```
TAM = Number of addressable customers
    × Average annual spend per customer (or annual volume per customer)
```

For segmented markets:
```
TAM = (Segment A customers × Avg spend A)
    + (Segment B customers × Avg spend B)
    + ...
```

### Process
1. Define the customer: what type of facility/company buys this?
2. Count or estimate the total global (or in-scope) population of potential customers
3. Segment by size if spending differs materially by size
4. Estimate average annual spend per customer, sourced from:
   - Your own deal data (most reliable)
   - Competitor pricing / public case studies
   - Customer interviews / call notes
   - Analogous product pricing in adjacent markets
5. Multiply and range it

### Source requirements for customer count
- Tier 1: Government census data (USDA, FAO, national fishery agencies)
- Tier 2: Industry association member databases
- Tier 3: Trade publication estimates, analyst reports
- Proxy: License or permit databases, regulatory filings, equipment manufacturer installed base

### Source requirements for spend per customer
- Your own sales data (if available)
- Public pricing (list prices, published case studies)
- Customer interviews — ask for annual budget or volume consumed
- Analogous product spend in a comparable market

### Worked example (geosmin/aquaculture)
```
Global RAS facilities (salmon + tilapia + catfish focus): ~3,500 facilities (FAO 2023 aquaculture census)
× Facilities with active geosmin problem (taste/odor failures): ~40% = ~1,400 facilities
× Facilities large enough to justify dedicated filtration system (>50 MT/yr output): ~60% = ~840 facilities

Average annual spend on geosmin filtration media/system:
  - Small facility (50–200 MT/yr): ~$15,000/yr [proxy: activated carbon replacement cycles, industry interviews]
  - Large facility (>200 MT/yr): ~$60,000/yr [proxy: same]
  - Mix assumption: 70% small, 30% large

Blended average: (0.70 × $15K) + (0.30 × $60K) = $28,500/facility/yr

TAM (bottom-up) = 840 facilities × $28,500 = ~$24M/yr

Note: This is a narrow TAM for pure geosmin filtration media. Expand to full water quality treatment system TAM for larger figure.
```

---

## Method 3: Value-theory

### When to use
When you can quantify the economic value the solution delivers to a customer. Best used as an upper-bound check and to validate pricing power.

### Formula
```
Value delivered per customer per year
× Willingness-to-pay fraction (typically 10–30% for B2B)
× Number of addressable customers
= Value-theory TAM
```

### How to quantify value delivered
Identify the specific economic benefit the solution creates:
- Cost savings (reduced losses, avoided fines, lower labor)
- Revenue protection (preventing product rejection, maintaining premium pricing)
- Compliance value (avoiding regulatory penalties)
- Yield improvement (more output from same inputs)

For each value driver:
1. Quantify the problem in customer-facing terms (e.g., "20% of fish production rejected for off-flavor = X% revenue loss per facility")
2. Estimate how much of that problem the solution eliminates
3. Express as annual $ value per customer

### Willingness-to-pay fraction
B2B buyers typically pay 10–30% of the value they receive. Use:
- 10%: Commodity-like solution, many substitutes, customer has high bargaining power
- 20%: Differentiated solution with clear ROI, moderate competition
- 30%: Mission-critical, few substitutes, high switching cost

Document your WTP assumption and rationale.

### Worked example (geosmin/aquaculture)
```
Problem: Geosmin causes fish to fail sensory quality tests → rejected product
Average salmon farm (200 MT/yr output): 
  - Revenue: 200 MT × $7/kg = $1.4M/yr
  - Off-flavor rejection rate without treatment: ~15% of production
  - Value of protected revenue: $1.4M × 15% = $210,000/yr/facility

Solution eliminates ~80% of rejection events (not 100% — other flavor issues remain)
Net value per facility: $210,000 × 80% = $168,000/yr

WTP fraction: 20% (differentiated solution, some substitutes like ozone, UV)
WTP per facility: $168,000 × 20% = $33,600/yr

Addressable facilities (>200 MT/yr with geosmin problem): ~250 globally

Value-theory TAM = 250 × $33,600 = ~$8.4M/yr (large facilities only)
Full addressable base incl. smaller facilities: ~$15–25M/yr

Note: This approach yields a narrower figure than top-down because it focuses on 
pure economic ROI for filtration. Value-theory is useful to confirm pricing power 
and customer willingness to invest, not to size the full market.
```

---

## Method 4: Comparable transactions

### When to use
As a cross-check when M&A activity, funding rounds, or disclosed revenue figures exist for comparable companies. Not a primary method — use to validate, not anchor.

### Process
1. Identify companies that:
   - Operate in the same or adjacent market segment
   - Have been acquired, gone public, or raised disclosed funding rounds
2. For acquisitions: find the deal value and any disclosed revenue multiple
3. For public companies: find revenue and any analyst coverage mentioning market share
4. For funding rounds: infer implied valuation and what it implies about revenue scale
5. Use disclosed revenue × implied market share to back into total market size

### Formula
```
Market size = Comparable company revenue / Implied market share
or
Market size = Deal value / Acquisition multiple / Implied market share
```

### Source requirements
- SEC filings (for US public companies and disclosed acquisitions)
- Press releases and investor presentations
- Crunchbase, PitchBook (for funding data)
- Trade press coverage of M&A

### Worked example (geosmin/aquaculture)
```
Comparable: [Water treatment company X] acquired [aquaculture inputs company Y] for $45M
Disclosed: Target had ~$8M revenue from aquaculture water quality segment
Implied revenue multiple: 5.6×
If acquirer believed target had ~15% market share in its addressable segment:
  Implied segment TAM = $8M / 0.15 = ~$53M

Cross-check: Does this align with bottom-up ($24M) and top-down ($200M)?
  - Bottom-up is narrower (pure filtration media only, conservative facility count)
  - Top-down is broader (full RAS treatment market, not just geosmin)
  - Comps figure at $53M falls between — suggests bottom-up undercounts 
    either market size or spend per facility. Investigate.
```

---

## Reconciliation logic

After running all methods, reconcile divergence explicitly:

**If methods broadly agree (within 2×):** Average or weight by confidence level. State which method you weight most and why.

**If methods diverge significantly (>2×):** Investigate before averaging. Common causes:
- Different market definitions (one method includes adjacent products, another doesn't)
- Different customer populations (one counts all potential customers, another counts only current buyers)
- Different unit metrics ($ revenue vs. volume vs. installed base)
- One method using stale data

Resolve the definition discrepancy first. Then re-run with consistent definitions. If still diverging, present both with explanation — don't force a false reconciliation.

**Confidence weighting:**
- Bottom-up from your own deal data: weight 40%
- Top-down from Tier 1 source: weight 30%
- Value-theory: weight 20%
- Comps: weight 10%

Adjust weights based on data quality in your specific situation.
