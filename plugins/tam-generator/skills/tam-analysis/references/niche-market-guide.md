# Niche market source discovery guide

Strategies and source lists for finding credible data in specialized B2B and industrial markets where general analyst reports are sparse or unreliable.

---

## General strategies for niche markets

### 1. Start with the regulator
Regulatory bodies that govern a market often publish the best production statistics:
- Who must report to regulators? Those entities are your customer population.
- Permit databases, license registries, and discharge reports can serve as customer censuses
- Enforcement actions and inspection reports reveal industry scale

### 2. Find the industry association
Every industry has a trade association. They typically publish:
- Annual industry reports with production and economic statistics
- Member directories (useful for customer census)
- Conference presentations with market size claims from credible practitioners
- Advocacy materials citing regulatory impact statistics (often well-sourced)

### 3. Mine public company filings
Even in niche markets, at least one publicly traded company typically competes:
- Their 10-K or annual report will often describe market size, competitive dynamics, and growth drivers
- Investor day presentations contain detailed market sizing slides
- Earnings call transcripts contain analyst questions that probe market size claims
- Search SEC EDGAR (US) or equivalent for any public company in the space

### 4. Use trade publications
Industry-specific publications cover markets that general business press ignores:
- Reporters in trade publications often know the market better than analyst firms
- Look for annual industry surveys, market reviews, or "state of the industry" issues
- Editors can sometimes point to better primary sources

### 5. Count the equipment
For markets where a physical system is installed at each customer:
- Equipment manufacturers publish installed base figures in investor materials
- Maintenance contract counts = active customer count (proxy)
- Equipment import/export statistics from trade databases (ITC Trade Map, US Census trade data) reveal market scale

### 6. Follow the supply chain
Work backwards from inputs:
- How much of [raw material] is consumed by this market?
- What do suppliers report about their sales into this segment?
- Chemical distributors, media suppliers, and component manufacturers often have segment-specific revenue in filings

---

## Vertical-specific sources

### Aquaculture / fisheries
- **FAO** (Food and Agriculture Organization): Global aquaculture production statistics by species, country, and production method. Best primary source for facility counts and production volumes. https://www.fao.org/fishery/en/statistics
- **NOAA Fisheries**: US aquaculture production data, imports, market reports. https://www.fisheries.noaa.gov/contact/office-aquaculture
- **USDA NASS**: US aquaculture census (conducted every 5 years). Facility counts, species, sales data. https://www.nass.usda.gov/
- **Nofima**: Norwegian Institute of Food, Fisheries and Aquaculture Research. Detailed RAS and salmon farming economics. https://nofima.no/en/
- **GlobalSalmonIndex / Kontali Analyse**: Industry analytics for salmon specifically (subscription, but data cited widely in public reports)
- **Fish Farming Expert**: Trade publication covering RAS, recirculating systems, geosmin/off-flavor issues specifically
- **Aquaculture North America, Hatchery International**: Trade press with market coverage
- **Global Aquaculture Alliance**: Member association with industry data
- **IntraFish**: Business news for seafood industry including production statistics

### Water treatment (filtration media, activated carbon, process chemicals)
- **EPA**: Drinking water regulations, treatment technology requirements. https://www.epa.gov/dwanalytics
- **AWWA** (American Water Works Association): Water utility statistics, technology adoption
- **Water Research Foundation**: Applied research with utility survey data
- **IWA** (International Water Association): Global water industry statistics
- **Global Water Intelligence**: Market data and intelligence (subscription)
- **Bluefield Research**: Water sector market intelligence
- **IBISWorld Water Treatment industry reports**: Useful for US context (Tier 3)

### Industrial filtration and separation
- **Filtration+Separation** (trade publication): Annual market surveys
- **McIlvaine Company**: Specialized industrial filtration market research
- **BCC Research**: Filtration market reports (Tier 3, use with caution)
- **EPA TRI** (Toxics Release Inventory): Chemical discharge data that implies facility counts

### Carbon materials and adsorbents
- **CEFIC** (European Chemical Industry Council): Carbon and chemical production statistics
- **USGS Minerals Yearbook**: US production data for carbon materials including activated carbon
- **IHS Markit / S&P Global**: Activated carbon market data (subscription, but cited in many reports)
- **Asian Development Bank** and **World Bank**: Development project documents often contain excellent market structure analysis for developing-country applications

---

## Key databases for bottom-up customer counting

### Global facility registries
- **FAO Global Aquaculture Production database**: Facility-level production data by country
- **EPA Facility Registry Service**: US industrial facility database
- **EU EMAS Registry**: European environmental management system participants
- **ISO certified facilities databases**: Facilities with specific quality certifications

### Trade and commerce databases (for demand-side sizing)
- **UN Comtrade / ITC Trade Map**: Import/export statistics by HS code. Useful for inferring market size from trade flows. https://www.trademap.org
- **USITC DataWeb**: US trade data with detailed HS codes
- **Eurostat COMEXT**: EU trade statistics

### Patent and IP databases (for technology adoption proxies)
- **USPTO Patent Full-Text Database**: Search for patents in specific application areas — filings indicate commercial activity
- **EPO Espacenet**: European and global patent search

---

## Interview and primary research sources

When secondary data is insufficient (common in niche markets):

### Who to interview
- Operations managers at customer facilities (best source for spend per customer)
- Procurement officers (confirm budgets and purchasing process)
- Application engineers at solution providers (understand deployment rates)
- Industry consultants who advise facility operators
- Regulatory inspectors (understand compliance-driven demand)

### What to ask in interviews (for TAM purposes)
- "How many facilities like yours exist in [geography]?" (customer count proxy)
- "What do you currently spend on [problem area] per year?" (spend per customer)
- "What percentage of facilities like yours have this problem?" (penetration rate)
- "What's the typical replacement cycle for [media/equipment]?" (recurring revenue basis)
- "Who else should I talk to about this?" (snowball sampling)

### Documenting interview data
- Note: name, role, company type, date, and whether the person spoke on record
- Treat as directional intelligence (Tier 3) unless the person is a recognized industry authority
- Use interview data to calibrate assumptions from secondary sources, not replace them
- Multiple interviews pointing in the same direction increases confidence level

---

## Proxies for hard-to-find data

When direct data does not exist, use documented proxies:

| Data needed | Proxy approach |
|-------------|---------------|
| Global RAS facility count | FAO production data ÷ average facility output per size tier |
| Geosmin-affected facilities | Academic prevalence studies × total facility count |
| Spend per facility on filtration | Activated carbon consumption rate × media cost × replacement cycle |
| Market growth rate | Aquaculture production growth rate (FAO) as a proxy for input demand |
| Competitive landscape | Patent analysis + LinkedIn company searches in target market |

Always label proxies explicitly in your analysis. State: "This figure is estimated by proxy — [proxy logic]. Direct measurement data was not available."
