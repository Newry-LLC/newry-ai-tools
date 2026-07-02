# Company Research Skill

Generalizable research skill for profiling companies — single deep-dives or large-scale list screening. Designs a tailored research plan based on the specifics of each effort, gets confirmation, then executes.

## Triggers

"research these companies", "enrich this list", "profile this company", "screen these companies", "classify companies against", "build a company list", "company research"

---

## How this skill works

This skill does not have a fixed pipeline. It has a planning step followed by execution. The plan is always tailored to the specific task — different goals, different lists, different industries require different approaches and different sources.

**The sequence:**
1. Intake — understand what you're trying to learn and what you already have
2. Plan design — propose modes, sources, execution order, output schema, check-in points
3. User confirmation — present the plan, get sign-off before executing anything
4. Execution — follow the plan; surface edge cases and judgment calls as they arise
5. Output — deliver results per agreed schema

---

## Step 1: Intake

Ask only what you don't already know from context. Key questions:

- **Context materials** — does a SOW, project launch deck, prior research, or call transcript exist for this engagement? Read these first before asking further questions — they often define the taxonomy, target markets, and framing the client already has in mind.
- **What do you have?** A list of companies, a single company, or nothing yet (need to find them)?
- **What do you want to learn?** Firmographics (size, location), product/capability classification, market focus, competitive intel, contacts — or some combination?
- **If classifying:** is there a taxonomy (keyword list per category) or do we need to discover one?
- **Confidence bar:** quick signal for internal prioritization, or citable evidence for a deliverable?
- **Output destination:** xlsx/CSV, report, Airtable, slide content?

If the request is clear enough to route without asking, propose the plan directly and ask for confirmation instead of running through questions.

---

## Step 2: Plan design

Based on intake, design a plan. The plan must specify:

**Modes needed** (one or more, in order):
- **Sourcing** — find candidate companies matching criteria. Sources depend on the industry, geography, and what's being looked for. Reason about what tools and approaches are likely to have coverage for this specific task — don't assume a fixed source list.
- **Discovery** — given a list, fetch websites to understand what product/capability categories naturally exist across the set. Propose a taxonomy to the user before screening.
- **Screening** — given a list and a taxonomy, classify each company against each category. Website fetch is primary; web search is the fallback for unreachable sites.
- **Deep-dive** — single company, comprehensive profile across multiple source types.

**Sources per field type** — assign the best source for each type of information this task requires. Reason about it given the specific task rather than applying a fixed mapping. Consider:
- What tools are available (see Tools section below)
- What the target companies are like (size, industry, geography, public vs. private)
- What level of evidence is needed (rough signal vs. citable)

Example reasoning: for small private European manufacturers, ZoomInfo HQ data is reliable but revenue is modeled; website fetch is the only way to get real product evidence; web search is needed for sites that block direct fetch.

**Execution approach:**
- Batch size and parallelism
- Where to check in with the user (always after first batch of any screening pass; at natural breakpoints on large lists)
- How to handle unreachable sites and edge cases

**Output schema** — propose columns before executing. Always include record-level source. Paired source columns for any classification fields.

**Existing data** — if the output file or base already has classifications or other enriched fields, explicitly ask: overwrite existing values, append new columns alongside, or skip rows that already have data? Never silently overwrite.

**How to present the plan:**
Write it as a short, readable brief — not a wall of text. Cover:
- What modes will run and in what order
- What fields will be populated and the primary source for each
- Output schema (column list)
- Where check-ins will happen
- Any open decisions or risks (e.g. "site failure rate may be high for this list")

One question at a time if clarification is needed. Get explicit confirmation before proceeding.

**Multi-mode chaining:** when modes chain (e.g. sourcing → screening), treat each mode as a phase with its own check-in. Deliver the output of one mode, confirm it's ready to proceed, then start the next. Don't pipeline automatically.

---

## Step 3: Execution

Follow the confirmed plan. During execution:

- Surface edge cases and hard judgment calls — don't silently resolve them
- Flag quality issues early (high site failure rate, suspected distributors, duplicate entities, revenue outliers)
- Check in at agreed points; don't run ahead
- Apply the sourcing protocol to every output field

---

## Sourcing protocol — non-negotiable

**Everything requiring a judgment call must be sourced. No exceptions.**

### Record-level source
One field per company capturing where baseline data came from (e.g. "ZoomInfo", "web (Claude)", "Clay keyword search"). Applies to the whole record when data comes from a single structured source.

### Field-level source
Required whenever a judgment was made or something was inferred:
- Classification calls (Yes/No/Unknown against a category)
- Verdicts or tiers (PASS/REVIEW/FAIL or equivalent)
- Market or segment assignments
- Any value synthesized or inferred rather than directly looked up

**What goes in a field-level source:**
- Exact quote from the source, not a paraphrase
- URL of the specific page, not just the domain
- If no URL (PDF, call transcript, internal doc): source type and name

**For No and Unknown, also note what was checked:**
- No: "homepage + /products reviewed — no match found"
- Unknown: specific reason — "SSL cert error", "site too thin to confirm", "product page 404"

**The test:** if someone asked "how do you know that?" — can you point them somewhere specific? If not, it needs a source.

### What doesn't need field-level sourcing
Direct database lookups where the value is unambiguous and the record-level source covers it (HQ city from ZoomInfo, employee count). Revenue always gets a note that it's estimated regardless of source.

---

## Classification rules

Classification schemes are defined at plan time based on what you're assessing — not imported from a prior project. During plan design, propose the scheme to the user and get confirmation before executing.

**Common patterns:**

*Binary capability screening (Yes/No/Unknown)* — used when the question is "does this company make/do X?"
- Yes — clear evidence the company is a primary manufacturer or provider. Not a distributor or reseller. Confirm with user at plan time whether primary producer only or broader.
- No — reviewed their complete offering, definitively no match. Only use No when you've seen enough to be certain.
- Unknown — evidence thin, site unreachable, or offering only partially visible. **When in doubt, Unknown not No.**

*Tier/verdict* (e.g. PASS/REVIEW/FAIL) — holistic judgment across multiple signals. Define the criteria for each tier at plan time.

*Fit scoring* (e.g. Strong/Partial/Weak) — how well does the company match a target profile? Define what constitutes each level at plan time.

*Category assignment* — which segment, market, or type does this company primarily belong to? Define the categories and any overlap rules at plan time.

*Presence confirmation* — does this company have meaningful presence in a geography, end market, or channel? Define "meaningful" at plan time.

**The constant across all schemes:** every classification is a judgment call and requires a field-level source per the sourcing protocol. The scheme changes; the sourcing requirement does not.

Source requirements for Yes/No/Unknown specifically:
- Yes → exact quote + source URL
- No → note what was checked (e.g. "homepage + /products reviewed — no match found")
- Unknown → reason (e.g. "SSL cert error", "site too thin to confirm")

---

## Quality checks — run before every write

- **Distributor/reseller filter** — any Yes classification where the company might be a distributor? Flag it.
- **Duplicate check** — same entity under two names or domains?
- **Revenue outliers** — database tools sometimes return parent company revenue for subsidiaries. Flag anything implausibly large.
- **Site failure rate** — if >20% of a batch returned Unknown due to site issues, flag before continuing. May indicate a list quality problem.

---

## Available tools

Know the general strengths and weaknesses of each. Apply judgment about which fits the specific task.

- **ZoomInfo** (`mcp__3cfd859f-b148-41d1-94ab-71d3d7f45d5e__enrich_companies`, `search_companies`, `search_contacts`) — reliable for HQ location and headcount ranges; revenue is modeled/estimated for private companies; good match rate for established companies, weaker for small or non-US
- **Web fetch** — primary source for product/capability evidence and anything requiring judgment; fetch homepage + /products + /solutions + /markets; try multiple paths if homepage is thin
- **Web search** — fallback when direct fetch fails; also useful for news, competitive intel, trade press
- **Clay** — keyword-based company sourcing; good for finding companies by product type or market focus; used in Alta FRP sourcing
- **Otter.ai / call transcripts** — primary source for anything discussed in a client call
- **Airtable MCP** — reading/writing structured data to Airtable bases
- **Python + openpyxl** — reading/writing xlsx files
- **LinkedIn, Crunchbase, trade association directories, conference exhibitor lists** — situationally useful depending on industry and what's being sourced; reason about fit per task
