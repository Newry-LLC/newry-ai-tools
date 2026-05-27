---
name: sharepoint-search
description: Search Newry's SharePoint and answer questions about any Newry content. Use this whenever a user asks something that might be answered by a document at Newry — project materials (interview notes, client presentations, deliverables, secondary research), internal resources (Newry Ladder, employee handbook, HR policies, templates, SoW examples), or anything else stored in the company file system. Triggers on questions like "which interviewee mentioned X", "have we presented Y to the client", "what does the Newry Ladder say about PM roles", "find the secondary research on Z", "do we have a template for X", "what's our policy on Y". Don't wait for the user to say "search SharePoint" — if the question sounds like it needs a Newry document, use this skill.
---

# Newry SharePoint Search

Answer questions by searching Newry's SharePoint and synthesizing content from the relevant documents. The goal is to give the user a direct, cited answer — not to hand them a list of files to go read themselves.

## Tools you'll use

- `sharepoint_search` — finds documents by keyword across SharePoint's full index. Returns document names, URLs, paths, and snippets.
- `sharepoint_folder_search` — finds folders by name. Use this to enumerate client folders for prior-work sweep questions.
- `read_resource` — fetches full text content of a document by URI. Use only when snippets are genuinely insufficient to answer the question.

## Step-by-step

### 0. Classify the question

Before searching, identify which type of question this is — it determines your search strategy and output format:

- **Point lookup** — "what did X say about Y", "what does the Newry Ladder say about Z", "who is responsible for X in the workplan" → find the specific document and read the relevant section.
- **Existence check** — "do we have secondary research on X", "have we presented Y to the client" → metadata and snippets are usually sufficient. Do NOT call `read_resource` unless the snippet is genuinely ambiguous.
- **Synthesis/sweep** — "what's been done on the project", "who mentioned X across all interviews", "summarize project status" → run multiple searches in parallel, synthesize from file names, dates, folder structure, and snippets. Only open a file if you need specific content not surfaced in snippets.
- **Prior-work sweep** — "has Newry worked in X domain", "what clients have we served in Y industry", "do we have prior experience with Z" → lead with broad keyword searches against the full index (no folder filter). Harvest which client folders appear in results. Domain knowledge is a supplement only — not the primary filter.

### 0.5. Decompose multi-part questions

If the question contains multiple distinct components, list them explicitly before searching. Each component is a separate obligation.

Example: "Which interviewees mentioned AOC, Reichhold, and Ashland — and what did they say about competitive positioning?" decomposes into:
- Part 1: which interviewees mentioned AOC? (enumeration)
- Part 2: which interviewees mentioned Reichhold? (enumeration)
- Part 3: which interviewees mentioned Ashland as a competitor? (enumeration + judgment — flag that Ashland also appears as company history)
- Part 4: what did they say about competitive positioning? (synthesis)

**Key rule:** if any component is enumerative ("which," "who," "how many," "list all"), answer it fully from search results before reading any documents. Do not let a well-answered synthesis component silently absorb an unanswered enumeration component. If the enumeration surfaces more than 3–4 files to read for the synthesis component, surface the list and confirm scope with the user before proceeding.

**Fire searches in parallel.** For multi-part questions, issue all search calls simultaneously — do not wait for one to return before starting the next.

**Completeness check — required.** Before finalizing any answer, verify it against this decomposition. Every part must be explicitly addressed. Name any part you could not fully answer and explain why. This step is not optional.

### 0.75. Interpret the query

Before searching, state in one or two plain sentences what the user is looking for and any assumptions you're acting on. Keep it to the goal and the assumption — not the mechanics of how you'll search.

Examples:
- "which interviewee mentioned CIPP resin?" → "You're looking for which specific people brought up CIPP resin during interviews."
- "do we have prior work in specialty coatings?" → "You're looking for any past Newry engagements that touched specialty coatings. Assuming any relevant work counts — primary research, deliverables, or secondary — not just a specific document type."
- "what does the Newry Ladder say about PMs?" → "You're looking for the current PM expectations and responsibilities from the Newry Ladder."

If the question is unambiguous and short, skip this step — don't narrate the obvious. Use it when the question is broad, multi-part, or could be interpreted more than one way.

Then proceed immediately to searching — do not wait for the user to confirm the interpretation unless something is genuinely unclear.

### 1. Extract search terms

Pull 2–4 distinctive search terms from the user's question. Prefer specific nouns, named entities, and proper nouns over generic words. Examples:

- "which interviewee mentioned the Phase 2 pricing plan?" → `Phase 2 pricing Alta`
- "what does the Newry Ladder say about PM responsibilities?" → `project manager Newry Ladder`
- "do we have secondary research on styrene regulation?" → `styrene regulation Alta secondary research`
- "have we presented CIPP findings to the client?" → `CIPP Alta Newry Presentation`

### 2. Search SharePoint

**Narrate as you go.** Before each search call, tell the user what you're doing: "Searching Primary Research for styrene regulation..." Before reading a document: "Found it in ALTA01 — reading now." Users should never be left wondering whether anything is happening.

**Choose your starting point:**

- If the routing cheat sheet clearly maps the question to a specific folder (e.g., HR policy → `People & Recruiting`, templates → `Newry Templates_Client Facing`), apply that `folderName` filter on the first call. Don't start broad when you already know where to look.
- If the question is general or spans multiple areas, start without a folder filter.
- If results are noisy or off-topic, refine with a `folderName` filter on the next call.

**For synthesis/sweep questions:** Fire 2–3 searches in parallel across different folder types (e.g., `Project Management`, `Primary Research`, `Newry Presentation`) before reading anything. File names, folder structure, and last-modified dates carry most of the signal — use them.

**For prior-work sweep questions:**
1. Run 2–3 broad keyword searches on the topic in parallel, with no folder filter. Use variant terms (e.g., "composites laminates", "specialty chemicals resins", "thermoset polymer"). These searches hit SharePoint's full index — relevant client folders will appear in the result paths regardless of whether you recognize the client name.
2. Harvest which client folders appear across results. This is your primary discovery mechanism.
3. Call `sharepoint_folder_search` with `"Clients"` to get the full client list. Cross-check against what keyword search surfaced.
4. Apply domain knowledge as a supplement: identify any clients you'd expect to appear based on what you know about their business, but that didn't show up in keyword results (possible cause: different terminology in older docs, or low index coverage). Run targeted searches within those specific folders.
5. Flag any clients in the full list you couldn't classify either way as **uncertain**. Surface them explicitly: "I wasn't able to confirm whether [X, Y, Z] are relevant to this domain — want me to search their folders?"
6. Run targeted searches within confirmed relevant client folders to surface specifics.

**Query reformulation.** If the first search returns nothing useful, automatically try 1–2 reformulations before surfacing a dead end:
- Synonyms or alternate terms (e.g., "polyester resin" → "thermoset resin" → "unsaturated polyester")
- Project code instead of client name (e.g., "ALTA01" instead of "Alta")
- Broader term if the original was very specific

If reformulations also return nothing, name the dead end clearly and offer specific alternatives (see Step 4).

### 3. Snip-then-stop — then read if needed

**Before calling `read_resource`, ask: does the snippet already answer the question?**

- For **existence checks**: if a snippet confirms the document exists and contains the relevant content, answer from the snippet. Do not read the full document.
- For **point lookups**: if the snippet contains the specific passage needed, answer from it directly.
- Only call `read_resource` when the snippet is genuinely insufficient — you need a full quoted section, the snippet is ambiguous, or you need surrounding context to interpret correctly.

**Pick the right version.** Search results include `lastModifiedDateTime`. When multiple results look like versions of the same document, always prefer the most recently modified one. Filename date conventions are a signal, but `lastModifiedDateTime` is the reliable indicator.

Call `read_resource` on the URI of the most relevant, most recent document. Find the specific section or passage that answers the question — you do not need to read every word.

If the first document doesn't contain the answer, try the next best result.

### 3.5. Handle large files (named step — do not skip)

If `read_resource` returns a truncated result (output saved to a file path rather than returned inline):

- **Do NOT retry the same document.**
- Pivot immediately:
  - For interview questions: search for individual interview notes files in the same folder (e.g., `*Internal (Anna Notes).docx`). Individual files are small and readable in full.
  - For other large docs: run a more targeted keyword search to surface the relevant section via snippets, or identify a more focused sub-document within the same folder.

### 4. Answer with attribution

Give a direct answer. Be specific — quote or paraphrase the relevant passage rather than summarizing vaguely. Always cite your source.

**Standard output format by question type:**

- **Point lookup:** Direct quote or close paraphrase + one sentence of context. Source below.
- **Existence check:** Yes/No + document name, date, and folder. Source below.
- **Synthesis/sweep:** Short table (file name | date | what it covers) + 2–3 sentence synthesis. Source(s) below.
- **Prior-work sweep:** Client-by-client summary (client name | engagement(s) found | relevance). Uncertain clients listed separately with offer to search. Source(s) below.

**If nothing found after reformulation:** be direct but warm — this document may not exist yet, may live under a different name, or may predate good SharePoint indexing. Say which of these is most likely given what you searched. Then give a specific next step: the folder to browse manually, a different search angle worth trying, or the person at Newry most likely to know. Never leave the user with nowhere to go.

**Completeness check — required.** Run the check from Step 0.5. Every decomposed part must be explicitly addressed in the answer. If any part is unanswered, name it and explain why.

## Source attribution

End every answer with a Sources section. For each document, include a one-phrase note explaining why this is the right source — what makes it authoritative or current. Keep it to the point.

- A direct link to the document
- A link to the folder it lives in (derive by stripping the filename from the `webUrl`)
- A brief note on why this source (e.g., "most recent version, updated Feb 2026", "the active workplan as of last week", "the only Alta deck in the Newry Presentation folder")

Format:

**Sources:**
- [Document name](document webUrl) — [Open folder](folder URL) — *why this source*

If multiple sources, list each one.

## SharePoint map

**Site root:** `newrycorp.sharepoint.com/clients/Shared Documents/`

**`Clients/`** — all project work
- One folder per client (e.g. `ALTA Performance Materials/`, `CORNING/`, `Chase Corporation/`)
- `Newry Internal/` — internal Newry initiatives run like client engagements (same folder structure)
- Each client → one folder per engagement, named `{CODE}-{Engagement Name}` (e.g. `ALTA01-Growth Strategy`)
- Standard engagement subfolders (consistent base set; some variation across projects):
  - `Primary Research/` → `Internal Interviews/`
  - `Secondary Research/`
  - `Newry Presentation/`
  - `Project Management/` ← per-engagement SoWs typically live here
  - `From Client/`
  - `Data and Analysis/`
  - `Drafts/`
  - `Conferences/`
- **Corning note:** by far the highest volume of projects across all clients. Almost exclusively a retainer client — most Corning projects will not have SoWs or proposals.

**`Consulting Resources/`** — internal firm resources
- `Document Templates/`
  - `Newry Templates_Client Facing/` — all PPTX and Excel templates, both client-facing and internal (includes quant research models, market sizing templates); folder name is a misnomer — internal templates live here too
  - `Newry SME Documents/` — SME contracting docs (NDA, independent contractor agreement, W-8 forms)
- `People & Recruiting/`
  - `ACC Templates and Ladder/` — Newry Ladder (most recent: `202602 Newry Consulting Ladder and Review Process.pptx`), mentor packages
  - `On Boarding Materials/` — onboarding resources including The Newry Way
  - `Newry Employee Handbook - 20250227.docx` — directly in this folder
- `TOOLS-TRAINING/`
  - `Growth Strategy/` — Growth Strategy frameworks and tools
  - `Interviewing Training/`
  - `Pyramid Principle/`
  - `Slide and Document Design/` → `Hero Slides and Documents/` — example deliverables by type (Opportunity Assessments, Market Forecasts, SONAR Deep Dives, RMAs, etc.)

**`Marketing and New Business Development/`** — BD and marketing
- `New Business Development/` → `Proposals and SOWs/` ← SoW examples may also live here
- `New Business Development/` → `Pitch Materials/` → `One-Pager Case Studies/`
- `Marketing and PR/` → `Events and Public Presentations/`
- `Offering Development/`

**Routing cheat sheet:**
- Project deliverables, research, workplans → `Clients/{client}/{engagement}/`
- PPTX or Excel templates → `Consulting Resources/Document Templates/Newry Templates_Client Facing/`
- Newry Ladder, HR policies, handbook → `Consulting Resources/People & Recruiting/` — use `folderName: People & Recruiting`; search term for the Ladder is "Newry Consulting Ladder" (not "Newry Ladder"); do NOT use `folderName: ACC Templates and Ladder` — that filter does not work
- Example slides, training materials → `Consulting Resources/TOOLS-TRAINING/`
- SoWs → check `Project Management/` within the relevant engagement first; `New Business Development/Proposals and SOWs/` as a secondary source (not all engagements have them — Corning almost never does)
- Secondary research → lives within each project folder, no firm-wide library

**Routing gap — consulting process training:** Questions about problem statements, issue trees, workplanning, project execution, and EM skills are NOT well-served by broad keyword search — those terms appear in many unrelated documents. Instead, search directly within these subfolders:
- `TOOLS-TRAINING/EM Training and Materials/` — EM Skill Building series, CLST Series (2022–2025), EM Handbook, Problem Structuring subfolder
- `TOOLS-TRAINING/Thought Leadership/` — Thought Leadership Training series (including 2019 series)
- `People & Recruiting/On Boarding Materials/` — onboarding decks including the 2025 "Consulting Process and Thought Leadership Onboarding"
- Use `folderName` filters like `EM Training and Materials`, `CLST Series`, `Thought Leadership`, or `Onboarding` rather than relying on keyword search alone.

## Examples

**"Which interviewee mentioned CIPP resin?"**
Classify: point lookup.
Narrate: "Searching Internal Interviews for CIPP resin..."
Search: `CIPP Alta internal interviews` with `folderName: Internal Interviews` → if consolidated notes doc is truncated, pivot immediately to individual files (Step 3.5) → search `CIPP filled resin` against `*Internal (Anna Notes).docx` files → read each and compile.
Output: Direct quote from each interviewee mentioning CIPP + source link.

**"What does the Newry Ladder say about Project Manager responsibilities?"**
Classify: point lookup. Routing cheat sheet → `ACC Templates and Ladder`.
Narrate: "Searching ACC Templates and Ladder for the Newry Ladder..."
Search: `Newry Ladder project manager` with `folderName: ACC Templates and Ladder` → read most recent PPTX → pull PM section.
Output: Direct quote of PM responsibility list + source link.

**"Have we presented our styrene findings to Alta?"**
Classify: existence check.
Narrate: "Searching Alta Newry Presentation folder for styrene..."
Search: `styrene Alta Newry Presentation` with `folderName: Newry Presentation` → if snippet confirms, answer without reading full doc.
Output: Yes/No + deck name and date + source link.

**"What's the current status of the Alta project?"**
Classify: synthesis/sweep.
Narrate: "Running parallel searches across Alta Project Management, Newry Presentation, and Primary Research..."
Fire in parallel:
- Search 1: `Alta project management workplan`
- Search 2: `Alta biweekly update` with `folderName: Newry Presentation`
- Search 3: `Alta interview tracker` with `folderName: Primary Research`
Synthesize from file names, dates, and snippets. Open 1–2 files only if specific content isn't inferrable from metadata.
Output: Table (file | date | what it covers) + 2–3 sentence synthesis.

**"Has Newry done prior work in composites or specialty chemicals?"**
Classify: prior-work sweep.
Narrate: "Searching SharePoint index for composites and specialty chemicals..."
Fire in parallel (no folder filter):
- Search 1: `composites laminates specialty materials`
- Search 2: `specialty chemicals resins thermoset`
- Search 3: `adhesives coatings polymer`
Harvest client folders from result paths → cross-check full client list via `sharepoint_folder_search` → domain knowledge supplement for any expected-but-missing clients → flag uncertain clients to user.
Output: Client-by-client summary + uncertain clients listed with offer to search.

---

## Logging

After every run, append a single-line JSON entry to the skill log using the Bash tool:

```bash
echo '{"ts":"<ISO timestamp>","query":"<user question>","type":"<point_lookup|existence_check|synthesis_sweep|prior_work_sweep>","docs_searched":["<name>",...],"docs_read":["<name>",...],"truncated":<true|false>}' >> "$HOME/Newry Corp/Clients - Claude Master Working Folder/logs/newry-knowledge-skill-log.jsonl"
```

Fill in all fields from the actual run. Keep the entry on a single line. If the log file isn't accessible, skip logging silently — do not surface an error to the user.

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
  - `fld4EyuVEhxAhPZEd` (sub_skill) — always `"sharepoint_search"`
  - `fldmTXyfFZRpbZEvQ` (user_id) — read `~/.user_id` if it exists; otherwise `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — project code if discernible (e.g. `"ALTA01"`); otherwise `""`

If the write succeeds, continue. If it fails, retry once.

**Step 3 — Local fallback (if Airtable write still failed after retry).**
Silently append one JSON line to `~/.newry/logs/usage-log-<user_id>.jsonl` (create `~/.newry/logs/` if missing):
`{"ts":"<ISO>","plugin":"newry_knowledge","sub_skill":"sharepoint_search","user_id":"<user_id>","project":"<project>"}`
No user-facing output. Then continue.

---

## Feedback capture

Read and follow the shared feedback-capture sub-skill: `../../../feedback-capture/SKILL.md`

When logging:
- `Plugin:` → `newry-knowledge`
- `Sub-skill:` → `sharepoint-search`
