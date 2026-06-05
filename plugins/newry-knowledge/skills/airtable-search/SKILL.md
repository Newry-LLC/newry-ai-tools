---
name: airtable-search
description: Search Newry's Airtable and answer questions about project history, institutional learnings, client contacts, and staff expertise. Use this when a user asks about prior Newry projects ("has Newry worked in X domain?"), wants to mine institutional learnings ("what have we learned from growth strategy projects?", "what do we typically do well on innovation projects?"), needs client contact information ("who are our contacts at Corning?", "who should I reach out to at W.L. Gore?"), or wants to know who at Newry has experience on a topic ("who has worked on automotive projects?"). Also use for specific project lookups by name or code. Complements sharepoint-search — Airtable gives structured project metadata and AER learnings; SharePoint gives document content. When both are relevant, use both. Requires the Airtable connector to be connected in Cowork settings.
---

# Newry Airtable Search

Answer questions using Newry's project knowledge base in Airtable. The goal is a direct, useful answer — project history, contact details, or institutional learnings — not a raw data dump.

## Base

**Base ID:** `appRawPuacfAvVH2Z` (Newry Knowledge Management)

## Tools

- `search_records` — full-text fuzzy search across a table's indexed fields. Use for keyword-based lookups (topic, domain, product, company name). Returns record IDs only — always follow with `list_records_for_table` to retrieve field data.
- `list_records_for_table` — structured query with filters. Use when filtering by linked record IDs (company, staff), singleSelect values, or date ranges. Combine multiple filters in one call to minimize round trips.

## Key tables and fields

**Projects** (`Projects`)
Core fields for all queries:
- `Project Code` — unique identifier (e.g., `COR741`, `ALTA01`)
- `Project Name` — full name of the engagement (singleLineText, searchable)
- `Company` — linked record to Companies table. **Cannot filter by text string — requires record IDs.** To filter by company: (1) run `search_records` on Companies with the company name to get all matching record IDs, then (2) filter Projects `Company` field using `hasAnyOf` with those IDs. A single client name may map to multiple Companies records (e.g., "Corning" → Corning Incorporated, Corning EIG, Corning CTO, etc.) — always fetch all variants first.
- `Company Name` — formula rendering of the linked company name. **Not filterable.** Use `Company` (linked record) for filtering instead.
- `Industry` — client industry (singleSelect, filterable). **Weak signal for industry-based questions** — the field uses a fixed category list that rarely matches the specific language a user will search with (e.g., "specialty chemicals" won't match). Don't rely on it as a primary search filter. Use keyword search on `Product or Technology` and `End Use System Or Market` instead. `Industry` can serve as a coarse first-pass filter when the user's language maps cleanly to a category value and you want to narrow a large result set.
- `Project Practice Area` — practice area, e.g., Innovation, Growth Strategy (singleSelect, filterable)
- `Project Type` — type of engagement (singleSelect, filterable)
- `Year` — year of the engagement (singleSelect, filterable — quick alternative to date range when an exact year is known)
- `Product or Technology` — specific product or technology focus (multilineText, searchable via `search_records`)
- `End Use System Or Market` — end market or application (multilineText, searchable via `search_records`)
- `Project Description` — scope and objectives. **Not in the search index** — `search_records` queries against this field return nothing. Use `Project Name`, `Product or Technology`, and `End Use System Or Market` for keyword search instead.
- `Status` — Completed, In Progress, Lost, etc. (singleSelect, filterable)
- `Start Date Actual` / `End Date Actual` — engagement dates (date fields, filterable with `>=`, `<=`, `isWithin` operators)
- `Staff Members` — lookup of staff names from Project Roles (multipleLookupValues, field ID `fldtlTPqWdjQ6ElW1`). **Confirmed searchable via `search_records`.** When looking for projects by staff member, search Projects directly on this field — this avoids the multi-hop Project Roles traversal entirely. Use full name (e.g., `Louis Lazar`). Expect 20–60+ results for active staff; that's correct.

AER fields (institutional knowledge — only populated for completed projects):
- `AER 3 Takeaways` — top learnings, things to do differently next time
- `What did we do well?` — specific strengths on this engagement
- `What would we do differently?` — specific improvements for next time
- `Did We Wow the Client?` — client satisfaction signal

Navigation:
- `SharePoint Project Folder Url` — direct link to SharePoint project folder

**Clients** (`Clients`)
- `Name` (full name), `First Name`, `Last Name`
- `Job Title`, `Division`
- `Company` (linked to Companies)
- `Email`, `Phone: Business`, `Phone: Mobile`, `LinkedIn`
- `Notes` — relationship context, history
- `Newry Contact` — linked Newry staff owner of relationship

**Companies** (`Companies`)
- `Name` (field ID `fldjEvNf3ybm3YO5g`), `Industry`, `Website`, `Description`
- `SharePoint Url` — link to company's SharePoint folder
- `Parent Company` / `Child Companies` — linked records capturing corporate hierarchy (e.g., Corning Incorporated → Corning EIG, Corning CTO). If you already know a parent company's record ID, fetching its Child Companies can surface all related entities without a fuzzy search.

**Staff** (`Staff`)
- `Full Name`, `Role`, `Job Title`, `Status`, `Type`, `Expertise`

**Project Roles** (`Project Roles`)
- `Project`, `Staff`, `Type`, `Budgeted Days`, `Actual Days`
- Use to find who worked on which projects

## Step-by-step

### -1. Check connector availability

Before doing anything else, verify that Airtable tools are available by attempting a lightweight call. If `search_records` or `list_records_for_table` are not available or return a connection error, stop immediately and tell the user:

> "It looks like the Airtable connector isn't connected yet. To use this skill, go to Cowork Settings → Connectors and connect Airtable. Once connected, try your question again."

Do not attempt to answer the question through other means. Do not proceed past this step if the connector is unavailable.

### 0. Classify the question

Identify which type of question this is — it determines your search strategy and output format:

- **Prior project lookup** — "has Newry worked in composites?", "find projects involving battery materials", "what engagements have we done in specialty chemicals?" → search Projects by topic/domain/product keywords; return project metadata + SharePoint link
- **AER mining** — "what have we learned from growth strategy projects?", "what do we typically do well on innovation work?", "what goes wrong on multi-company engagements?", "what would Newry do differently on market sizing?" → search Projects by topic/type, return AER fields synthesized across matches
- **Client contact lookup** — "who are our contacts at Corning?", "do we have a contact at W.L. Gore?", "find Amy Alberg's details" → search Clients or Companies; return contact card
- **Staff expertise lookup** — "who at Newry has worked on automotive projects?", "who has experience in specialty coatings?" → search Project Roles filtered to relevant projects; surface staff names and their roles
- **Specific project lookup** — "what was the scope of COR741?", "tell me about the Aurora capstock project" → retrieve the specific project record by code or name

### 0.5. Interpret the query

For anything other than a simple specific project lookup, state in one or two plain sentences what the user is looking for and any assumptions you're acting on. Then proceed immediately.

Examples:
- "has Newry worked in specialty coatings?" → "You're looking for past Newry engagements that touched specialty coatings or surface protection. Assuming any relevant work counts — not just a specific project type."
- "what have we learned from client management on complex projects?" → "You're looking for AER learnings across completed projects where client management was a notable factor. I'll synthesize across matches."
- "who are our contacts at Corning?" → skip — obvious.

### 1. Search

**Narrate as you go.** Before each call, briefly say what you're searching: "Searching Projects for specialty coatings engagements..." Users should know something is happening.

**For prior project lookups and AER mining:**
Use `search_records` on the `Projects` table with relevant keywords. Search across: `Product or Technology`, `End Use System Or Market`, `Project Name`. Do **not** include `Project Description` — it is not in the search index and will return nothing.

- Use 2–4 distinctive keywords — specific nouns, product names, domain terms
- If first search returns few results, try variant terms (e.g., "surface protection" → "protective film" → "coatings")
- Filter to `Status = Completed` for AER mining (only completed projects have AER data)
- For AER mining, run 2–3 searches with different keyword angles to maximize coverage — AER learnings are only as good as the breadth of matching projects

**For company-based project lookups** (e.g., "all Corning projects", "find projects for W.L. Gore"):
1. `search_records` on Companies — query: the company name (e.g., `Corning`). Returns record IDs via fuzzy match — **includes false positives** (e.g., searching "Corning" may return Owens Corning, Dow Corning, unrelated companies). After getting IDs, call `list_records_for_table` on Companies filtered to those IDs to retrieve the `Name` field, then **discard any record whose name does not contain the search term as a substring** (case-insensitive). Use only the verified record IDs in step 2.
2. `list_records_for_table` on Projects — filter `Company` field using `hasAnyOf` with the verified record IDs from step 1. Combine with additional filters in the same call:
   - `Status` filter if only completed/active projects are needed
   - For date scoping, use **both** `Start Date Actual <= [end of range]` AND `End Date Actual >= [start of range]` — this captures any project with overlap in the window, not just projects that started within it. Example for 2022–2024: `Start Date Actual <= 2024-12-31` AND `End Date Actual >= 2022-01-01`.

**For client contact lookups:**
- If searching by company: use `search_records` on `Clients` with the company name, or look up the Companies record(s) and pull linked Clients
- If searching by person name: use `search_records` on `Clients` with the person's name
- **Important:** `search_records` returns record IDs only — no field data. Always follow with `list_records_for_table` filtered to those record IDs to retrieve names, titles, emails, and phone numbers.

**For staff expertise lookups:**
1. First find the relevant projects via `search_records` on `Projects`
2. Get staff from Project Roles: `list_records_for_table` on `Project Roles` filtered by project record IDs — use `hasAnyOf` on the `Project` field with the project record IDs
3. Aggregate by person — who appears across the most relevant projects

**For staff-on-a-company lookups** (e.g., "who has worked on Corning projects?"):
1. Get company record IDs from Companies (as above)
2. Get project record IDs: `list_records_for_table` on Projects filtered by `Company` hasAnyOf + date range if applicable — returns project IDs and `Staff Members` field values
3. Extract staff names directly from the `Staff Members` field (field ID `fldtlTPqWdjQ6ElW1`) on returned Projects records — no Project Roles lookup needed
4. Aggregate and deduplicate across projects

**For specific project lookups:**
Use `search_records` on `Projects` with the project code or name. Project codes are exact (e.g., `COR741`) — include them verbatim in the query.

**Pagination / result truncation.** `list_records_for_table` has a page size cap (typically 100 records). If a query returns exactly 100 (or another suspiciously round number) and the scope is broad, results are likely truncated. Do not treat a truncated result as complete. Instead: add a tighter filter (narrower date range, Status = Completed, specific company), re-run, and note to the user that you've narrowed the query to stay within result limits.

**Query reformulation.** If first search returns nothing useful, automatically try 1–2 reformulations before surfacing a dead end:
- Synonyms or broader terms (e.g., "battery" → "energy storage", "lithium")
- Alternate company spellings or abbreviations
- Related end markets (e.g., "automotive" → "transportation", "EV")

### 2. Answer directly

Give a direct answer. Be specific. Always include attribution (project code + name, or contact full name + company).

**Standard output format by question type:**

**Prior project lookup:**
For each relevant project:
- `[Project Code]` — [Project Name] ([Company], [Year])
- [1–2 sentence description of relevance]
- SharePoint: [link if available]

If 5+ projects found, group by sub-topic or recency rather than listing exhaustively.

**AER mining:**
Synthesize across all matched projects. Group learnings thematically — don't list project by project. Lead with the pattern, then illustrate with specific examples.

Format:
**[Theme]** — [synthesized insight]. *(seen in [Project Code], [Project Code])*

Cover: what tends to go well, what tends to go wrong, and any surprise or counterintuitive findings. Call out if a finding appears in many projects vs. just one.

**Client contact lookup:**
For each contact:
- **[Full Name]** — [Job Title], [Division if known]
- [Company]
- Email: [email] | Phone: [phone] | LinkedIn: [url]
- [Notes if substantive]
- Newry relationship owner: [name if available]

**Staff expertise lookup:**
- **[Staff Name]** — [Role/Title] — worked on: [Project Code] ([Company], [Year]), [Project Code] ([Company], [Year])

**Specific project lookup:**
- **[Project Code] — [Project Name]**
- Client: [Company] | Dates: [Start] → [End] | Practice Area: [area]
- Description: [key scope points]
- AER (if available): [brief synthesis of takeaways]
- SharePoint: [link]

**If nothing found after reformulation:** say which search angles were tried and why they likely came up empty (topic may not be in the Airtable corpus, or may predate current records). Suggest the most likely alternative — a broader search term, a related domain, or checking SharePoint directly.

**Completeness check.** For multi-part questions, ensure every component is addressed before finalizing. Name any unanswered part and explain why.

## Connecting to SharePoint

Whenever a project lookup or AER mining query returns projects with a `SharePoint Project Folder Url`, include the link. This lets the user pivot immediately to document content without a separate search.

For AER mining specifically: if the user wants to go deeper on a specific project's learnings, point them to the project's SharePoint folder for the actual deliverables and research.

## Examples

**"Has Newry done prior work in specialty coatings or surface protection?"**
Classify: prior project lookup.
Narrate: "Searching Projects for surface protection and coatings engagements..."
Search 1: `search_records` on Projects — query: `surface protection coating film` (fields: `Product or Technology`, `End Use System Or Market`, `Project Name`)
Search 2: `search_records` on Projects — query: `protective materials substrate`
Output: Project-by-project list with codes, companies, years, brief relevance note, SharePoint links.

**"What Corning projects did we work on in 2023–2024?"**
Classify: company-based project lookup.
Narrate: "Looking up Corning company records, then filtering projects..."
Step 1: `search_records` on Companies — query: `Corning` → get candidate record IDs
Step 1b: `list_records_for_table` on Companies filtered to those IDs → retrieve `Name` field → discard any record whose name does not contain "Corning" (e.g., drop Owens Corning, Dow Corning if not relevant, or any unrelated false positives) → keep only verified Corning entity IDs
Step 2: `list_records_for_table` on Projects — filter: `Company` hasAnyOf [verified Corning record IDs], `Start Date Actual` <= 2023-12-31, `End Date Actual` >= 2023-01-01
Output: Project list with codes, names, dates, SharePoint links.

**"What have we learned from projects where we had to manage complex client teams or multi-stakeholder engagements?"**
Classify: AER mining.
Narrate: "Searching for AER learnings on multi-stakeholder projects..."
Search 1: `search_records` on Projects — query: `multi-stakeholder client management complex`, filter: Completed
Search 2: `search_records` on Projects — query: `consortium partnership collaboration`, filter: Completed
Synthesize AER fields across matches. Group thematically: what works, what goes wrong, what's counterintuitive.

**"Who are our contacts at W.L. Gore?"**
Classify: client contact lookup.
Narrate: "Looking up contacts at W.L. Gore..."
`search_records` on Clients — query: `Gore`
Follow with `list_records_for_table` on Clients filtered to returned record IDs to get full contact data.
Output: Contact cards for each person linked to W.L. Gore.

**"Who at Newry has worked on rare earth or critical minerals projects?"**
Classify: staff expertise lookup.
Narrate: "Searching for rare earth and critical minerals projects, then pulling staff..."
Step 1: `search_records` on Projects — query: `rare earth critical minerals`
Step 2: `list_records_for_table` on Project Roles — filter: `Project` hasAnyOf [matched project record IDs]
Output: Staff names with project list.

**"What was the scope of COR741?"**
Classify: specific project lookup.
`search_records` on Projects — query: `COR741`
Follow with `list_records_for_table` on Projects filtered to that record ID to get full field data.
Output: Full project card including description, AER, SharePoint link.

---

## Logging

After every run, append a single-line JSON entry to the skill log:

```bash
echo '{"ts":"<ISO timestamp>","query":"<user question>","type":"<prior_project|aer_mining|contact_lookup|staff_expertise|specific_project>","tables_searched":["<name>",...],"records_returned":<n>}' >> "$HOME/Newry Corp/Clients - Claude Master Working Folder/logs/newry-knowledge-skill-log.jsonl"
```

Fill in all fields from the actual run. Single line only. If log isn't accessible, skip silently.

---

## Usage logging

At the start of every run — before any other work:

**Step 1 — Check Airtable connectivity.**
Call `list_records_for_table` (Base ID: `appRawPuacfAvVH2Z`, Table ID: `tblmACtwIClniGn5n`, pageSize: 1). If this call fails, stop and show:

> "⚠ **Airtable isn't connected.** This tool requires Airtable for usage logging. Go to Cowork Settings → Connectors, connect Airtable, then start a new session."

Do not proceed until resolved.

**Step 2 — Write to Airtable.**
Call `create_records_for_table` with:
- **Base ID:** `appRawPuacfAvVH2Z` | **Table ID:** `tblmACtwIClniGn5n`
- **Fields:**
  - `fldRrr3BkrJW8rE3L` (ts) — current UTC time, ISO 8601 (e.g. `2026-05-27T14:30:00Z`)
  - `fldNHK285dPCOdNhB` (plugin) — `"newry_knowledge"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — always `"airtable_search"`
  - `fldmTXyfFZRpbZEvQ` (user_id) — use the user's email address from the session context (available in the system prompt `<user>` block); if not available, use `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — project code if discernible (e.g. `"ALTA01"`); otherwise `""`

If the write succeeds, continue. If it fails, retry once.

**Step 3 — Local fallback (if Airtable write still failed after retry).**
Silently append one JSON line to `~/.newry/logs/usage-log-<user_id>.jsonl` (create `~/.newry/logs/` if missing):
`{"ts":"<ISO>","plugin":"newry_knowledge","sub_skill":"airtable_search","user_id":"<user_id>","project":"<project>"}`
No user-facing output. Then continue.

---

## Feedback capture

Read and follow the shared feedback-capture sub-skill: `../../../feedback-capture/SKILL.md`

When logging:
- `Plugin:` → `newry-knowledge`
- `Sub-skill:` → `airtable-search`
