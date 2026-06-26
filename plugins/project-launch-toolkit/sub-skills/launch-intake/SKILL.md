---
name: launch-intake
description: Phase 0 of the Project Launch Toolkit. Takes a SoW and creates or updates the Airtable project record — writing every factual field that can be read from the SoW (type, industry, scope, company/staff links, fees, dates). Replaces the manual Airtable New Project Form. Runs first, before the rest of the launch. The value creation hypothesis is a separate step (value-creation), after the problem statement.
---

# Launch Intake Sub-Skill

Phase 0 of every project launch: create or update the Airtable project record from the SoW, writing the factual fields automatically. This replaces the manual Airtable New Project Form so the project exists in Airtable before the team starts the launch deck.

This skill writes **factual fields only**. The value creation hypothesis (the six value fields) is built later, by the **value-creation** sub-skill, after the problem statement exists — value creation leans on the SMART objective, so it can't run before the problem statement.

## Inputs

**Required — at least one source describing the project.** A SoW is ideal but not assumed; many projects won't have one. Use whatever exists: SoW, signed proposal, proposal or scoping deck, scoping notes, kickoff emails, or call notes. More context = better fill.

Feed it any way that's convenient — pasted text, uploaded or dragged-in files, or a path to a mounted / SharePoint folder (the skill reads what's there). If multiple materials are provided, read across all of them.

**Optional (improves output quality):**
- Additional client-provided materials (RFP, scope supplement, budget breakdown)
- Names of Account Manager, Sales Lead, and project team if not in the source materials

If little is available, fill what's determinable and flag the rest in the report — a sparse-but-honest record beats a blocked one.

> Throughout the steps below, "SoW" is shorthand for *whatever source materials were provided*.

## Flow

**Step 1 — Check for existing record**

Search Projects table (`tbl3FaAcnmFWjRwqr`) for a matching record:
- Search by client company name (substring match on Company Name formula field)
- Cross-reference against project description / SoW date range to narrow if multiple matches

**If found:** update the existing record (do not create a duplicate)
**If not found:** create a new record

**Step 2 — Extract fields from SoW**

Read the SoW and extract values for each auto-fill field (see Field Reference below). For select/multi-select fields, match to the closest valid choice. Skip fields that can't be determined and flag in the report.

**Step 3 — Resolve record-link fields (verify, then create-if-new)**

Several fields are record links (dropdowns) — they store a pointer to a record in another table, not plain text. Names in the source materials often differ from the database (e.g., "Corning" vs. "Corning Incorporated" vs. "Corning EIG"), so resolve carefully — match to the right table:

- **Company** → Companies (`tbl3p52vtnJdUJO4D`) — the client organization
- **Client Payer** → Companies (`tbl3p52vtnJdUJO4D`) — the paying entity (usually the same org)
- **Clients** → the **Clients** table (`tblD9CnnbQHJsCUt9`) — these are **people** (client stakeholders), *not* the company

(Staffing — ED, EM, Account Manager, team — is handled in Step 4, not here.)

For each link:
1. Search the right table for a match.
2. **Confirm with the EM before linking** when the match is fuzzy, has multiple candidates, or the name drifted from the materials. On a clean exact match, link it and just note what you matched.
3. **If there's no match:** for **Company / Client Payer / Clients**, propose creating a new record (a new client company, or a new client person) — but **never create it without the EM's explicit confirmation**.

**Nothing gets created silently.** Present the resolved links in one short confirmation before writing — matches to link, plus any companies/people you propose to create — and wait for the EM's go-ahead. Never write a guessed or wrong record ID.

**Step 4 — Staffing (the project team)**

Staff are assigned during launch, so capture the team here. Pre-fill any names found in the materials (the SoW often lists some or all — but sometimes none, or there's no SoW), then present a roles table for the EM to confirm and complete:

| Role | Name |
|---|---|
| Executive Director (ED) | |
| Engagement Manager (EM) | |
| Account Manager | |
| Team Member 1–5 | (as many as apply) |

Keep it flexible — leave roles blank if undecided, and don't force five team members (most projects have 1–2; some have none). Ask the EM to fill gaps.

Once confirmed, **offer to enter the team into Airtable** — link each person's existing **Staff** record (`tblAeAug2APoy0Jgf`) to the project: ED / EM / team via **Project Roles** (`tblYG4PfBYTnsv0WC`); Account Manager / Sales Lead / Contract Accountability via their direct Project link fields. Do **not** create new Staff records — if a name isn't in Staff, flag it (new hires are added by ops). Confirm before writing.

**Project Roles write spec** — one record per person, three fields:

| Field | Airtable ID | Value |
|---|---|---|
| Type | `fldRgACuXbe7SOonv` | Select: `ED`, `EM`, `Team Member`, or `Editor` |
| Staff | `fldjnWTwVjYv926Yf` | Link to Staff record ID |
| Project | `fldMHFHFX3R7RtUK1` | Link to Project record ID |

**Step 5 — Write to Airtable**

First create any new Company / Clients records confirmed in Step 3, then write the project: call `update_records_for_table` (or `create_records_for_table` if the project is new) with all successfully extracted factual fields — including the resolved record links — in a single call. Then enter the confirmed staffing (Step 4).

**Step 6 — Report**

```
LAUNCH INTAKE COMPLETE — [Client Name] — [Project Code if known]
[Created new record / Updated existing record: {record ID}]

✅ WRITTEN
  Project Description, Project Type, Industry, Geographic Scope,
  Product or Technology, End Use System or Market, Company (linked),
  Client Payer (linked), Account Manager (linked), Project Fee Budget,
  Start Date Budgeted, End Date Budgeted, Year

⚠️ NOT FILLED (fill in Airtable)
  [field: reason not filled]

Next: draft the problem statement, then build the value creation hypothesis (value-creation sub-skill).
```

## Field Reference

### Auto-fill fields

| Field | Airtable ID | Source | Notes |
|---|---|---|---|
| Project Description | `fldhAgARKAFCQ5THV` | SoW | 2–4 sentence summary. Use SoW language closely; don't editorialize. |
| Project Type | `fldSFzadKir5W6bkb` | SoW | Select — classify from list below |
| Industry | `fldy6CkT1O8hGyowc` | SoW | Select — classify from list below |
| Geographic Scope | `fld4NEsw2Umda2wa9` | SoW | e.g., "North America", "Global", "US residential construction" |
| Product or Technology | `fldHIBsKv2iECfSaS` | SoW | The specific product, material, or technology at the center of the work |
| End Use System or Market | `fldmK5RHWWvobyzdu` | SoW | Downstream market or application (e.g., "AR waveguides", "residential windows") |
| Company | `fld20oC2XHucFNgfG` | SoW | Record link → Companies (the org). Verify match; create if new. |
| Clients | `fldvU6K9zQdgX0klY` | SoW | Record link → **Clients** table `tblD9CnnbQHJsCUt9` (the **people** / client stakeholders). Verify; create new person if absent. |
| Client Payer | `fldOuBTSPJYBGU1xv` | SoW | Record link → Companies (paying entity); usually same org as Company |
| Account Manager | `fldVN9xKte5Hk4s7l` | SoW / team | Record link → Staff table |
| Sales Lead | `flddLTU11eybQRhZn` | SoW / team | Record link → Staff table |
| Sales Contributor(s) | `fldlDFk6aB9Q1SP7C` | SoW / team | Record link → Staff table; multi-link |
| Contract Accountability | `fldgbEd563FTF6z` | SoW / team | Record link → Staff table |
| Project Fee Budget | `fldRRyOGQ21N15RpC` | SoW | Total fees in dollars |
| Start Date Budgeted | `fldWC9bLfEOBAyKCX` | SoW | ISO format (YYYY-MM-DD) |
| End Date Budgeted | `fldLlhOqerzq2l6r2` | SoW | ISO format (YYYY-MM-DD) |
| Year | `fldEAFg4Pbq2uXxw4` | Start date | Calendar year of Start Date Budgeted |

### Never fill

- **Project Name** (`fldU9JlF5KzJUw1G3`) — EM sets this in Airtable
- **Project Practice Area** (`fldG8KGRK4GX6n9RH`) — EM classifies
- **Status** (`fldJtAz4FzU3U3P6S`) — do not set; Airtable default applies
- **Project Code** — auto-generated or set by ops
- **Six value creation fields** — written later by the value-creation sub-skill, not here
- **Is Retainer Project, SharePoint Folder Name, Discount/Markup Rationale, Billing Type, Referral Fees, Allocated Expenses Billing Type, Ruddr Project URL** — ops-owned; never touch

### Project Type classification (15 choices)

Application Development · Competitive Assessment · Customer/Market Research · Feasibility · Financial Analysis · Go-to-Market · Growth Engine · Innovation Assessment · Innovation Road Map · M&A · Market Entry · Opportunity Assessment · Positioning · Supply Chain · Technology Push · Other

When ambiguous: pick the best fit and note the assumption in the report.

### Industry classification

Use `get_table_schema` on the Projects table (`tbl3FaAcnmFWjRwqr`) to retrieve the full list of Industry choices for field `fldy6CkT1O8hGyowc` before writing. Do not write a value not in the list. When a project spans multiple industries, select the primary one.

## Design Notes

- **Runs first, before the PPT sub-skills.** It establishes the Airtable record the rest of the launch hangs off.
- **Create vs. update:** always check for an existing record before creating. Duplicate Projects records break reporting and AER tracking.
- **Record link failures are not blocking.** Skip the field, flag it, continue. Don't fail the write because one name wasn't found.
- **Factual only.** The value creation fields are deliberately out of scope here — they need the problem statement and EM judgment, and are owned by the value-creation sub-skill.

## References

- `strategy/airtable-base.md` — canonical table/field reference (`appRawPuacfAvVH2Z`)
- Projects: `tbl3FaAcnmFWjRwqr` · Companies: `tbl3p52vtnJdUJO4D` · Staff: `tblAeAug2APoy0Jgf`
- Interface "1. Project Launch" (`pagg4NxS9WehhvYE8`) — 52-field launch view
- Project Initiation Template — the project creation/launch process and the factual launch fields
