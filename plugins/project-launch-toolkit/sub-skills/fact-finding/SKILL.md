---
name: fact-finding
description: Generate a pre-populated fact-finding worksheet for a new project launch. Searches Airtable and SharePoint to surface client history, analogous prior work, and internal SMEs. Pre-populates the fact-finding slide before the kickoff meeting so the team arrives with context rather than building it from scratch.
---

# Fact Finding Sub-Skill

Pre-populate the fact-finding worksheet using Newry's Airtable and SharePoint. Output mirrors the fact-finding page of the Project Initiation Template and is ready to share with the team at kickoff.

## Inputs

**Required:**
- Client name
- Stakeholder list (from problem statement; ask if not provided)
- Problem statement and/or SoW — the basis for generating search keywords (ask if neither is available)

**Optional:**
- Project code

## Routing

Invoked by the coordinator or run directly. This sub-skill generates its own search keywords (Step 0) and gets EM approval before searching — keyword generation is not done elsewhere.

Can run in parallel with `problem-statement`, but it needs the problem statement *or* the SoW as the basis for keywords — if neither exists yet, ask for the project context first.

## What This Skill Does

### Step 0 — Generate search keywords (then confirm with EM)

Derive a keyword list from the problem statement and/or SoW: the client's product/technology, end-use markets, key topics, adjacent terms, and any named competitors or applications. Expand to synonyms and product names — broad searches need variety to hit.

Present the list to the EM for quick approval or edits **before searching**. Don't run any searches until the EM confirms — bad keywords waste the whole pass.

### Step 1 — Airtable: client history

**By person** — for each stakeholder named in the problem statement:
- Run `airtable-search` on Contacts (`tblomVbLXeELjFIBZ`) to find the person's record
- Pull all Context Log entries (`tbl3JoPYzslECv8h8`) linked to that person (all types: Interactions, Standing Context, Goals, Outcomes), sorted by date
- If the person is not found in Contacts: flag as "not in Contacts — no prior relationship history available"

**By company** — search Projects (`tbl3FaAcnmFWjRwqr`):
- Filter where Company Name contains the client name (substring match — handles multi-division clients like Corning automatically)
- Filter to last 2 years (Start Date Actual)
- Return: total count + Project Name, Project Code, Start Date for each
- Also pull AER 3 Takeaways (`fldx8JwT0Y0MgToRk`) from each project where populated

### Step 2 — Analogous prior work (Airtable + SharePoint)

Using the confirmed keyword list, search both sources for topically-similar past work — across *all* clients, not just this one:

**Airtable — analogous projects:** use `airtable-search` to query Projects by keyword against the **Project Description** field (`fldhAgARKAFCQ5THV`, contains-match) to surface past Newry projects on similar topics/technologies regardless of client. Return project name + code + a description snippet.

**SharePoint — analogous deliverables:**
- Run `sharepoint-search` for each keyword (or keyword combination)
- Surface relevant past deliverables — documents, presentations, reports on similar topics/technologies
- Return: document name + SharePoint link for each result

Aim for quality over quantity in both — surface the most relevant, not everything that matches.

### Step 3 — Airtable: internal SMEs

Two signals, combined:

**From project staffing** — take the projects surfaced in Step 2 (keyword-matched SharePoint results). If those projects have Airtable records, pull Staff Members. Also search Airtable Projects directly using the keyword list and pull Staff Members from matching records.

**From Staff Expertise field** — query Staff table (`tblAeAug2APoy0Jgf`), active only (`Status = Active`), keyword match against Expertise field (`fldg5gPZRs1xMf4sQ`).

Merge and deduplicate. Flag anyone appearing in both signals as a stronger match. Output: name + expertise note + signal source.

Note: Expertise field is sparsely populated and free-text — matches are suggestive, not definitive. Present as "suggested SMEs — verify with ED."

### Step 4 — Generate the worksheet

Assemble Steps 1–3 into the output format below.

## Output Format

```
FACT-FINDING WORKSHEET — [Client Name] — [Project Code if known]

CRM FINDINGS:
  [Per stakeholder — name, summary of Context Log entries, most recent interaction date]
  [Flag any stakeholder not found in Contacts]

PAST AER LEARNINGS:
  [AER 3 Takeaways from client's projects in the last 2 years, by project name + code]
  [Blank if no AER data found]

RELEVANT PAST PROJECTS ([X] projects for [Client] in last 2 years):
  [Project Name — Code — Start Date]
  [Project Name — Code — Start Date]
  ...

ANALOGOUS PROJECTS (by topic/keyword, any client):
  [Project Name — Code — one-line description]
  [Project Name — Code — one-line description]
  ...

BEST IN CLASS WORK PRODUCTS:
  [Document name + SharePoint link from Step 2]
  [Document name + SharePoint link from Step 2]
  ...

INTERNAL SMEs:
  [Name — Expertise — Signal: staffing / expertise match / both]
  [Name — Expertise — Signal: staffing / expertise match / both]
  ...

⚠️ GAPS:
  [Stakeholders not found in Contacts]
  [Steps where no results were returned]
  [Any other items requiring human input]
```

## Design Notes

- **Prefer newry-knowledge sub-skills for search.** Use `sharepoint-search` and `airtable-search` if newry-knowledge is installed. If not, flag it to the user ("newry-knowledge isn't installed — running search directly via MCP tools") and call the SharePoint and Airtable MCP tools directly. Search behavior is the same either way.
- **Degrade gracefully.** If any step returns no results, say so clearly in the output and move on. Partial output with gap flags is still highly valuable.
- **Substring match for multi-division clients.** "Corning" matches Corning EIG EMT, Corning CTO, Corning Incorporated, etc. Apply this pattern to any large client with multiple divisions.
- **Output is for team orientation.** It mirrors the fact-finding page of the Project Initiation Template. PPT population is a future automation — for now, the team copies relevant content into the slide.
- **Confirm keywords before searching.** Generate them in Step 0 and get EM approval — bad keywords waste the entire pass. Once approved, use them as-is across all steps.

## References

- Project Initiation Template — the pre-project-initiation fact-finding page
- Airtable base `appRawPuacfAvVH2Z`: Projects (`tbl3FaAcnmFWjRwqr`), Contacts (`tblomVbLXeELjFIBZ`), Context Log (`tbl3JoPYzslECv8h8`), Staff (`tblAeAug2APoy0Jgf`)
