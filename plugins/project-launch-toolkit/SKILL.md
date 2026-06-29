---
name: project-launch-toolkit
description: Orchestrate a complete Newry project launch. Takes a SoW or proposal and runs the full suite of launch sub-skills — launch intake (Airtable record), problem statement, fact-finding, value creation, issue tree, workplan, ownership and goals, and account management. Can run the full flow or any individual sub-skill on demand.
---

# Project Launch Toolkit — Coordinator

The entry point for all PLT sub-skills. Run the full launch flow from a SoW, or jump directly to a specific sub-skill.

## Sub-Skills

| Sub-skill | What it produces | Depends on |
|---|---|---|
| `launch-intake` | Airtable project record — factual fields from the SoW | SoW/proposal |
| `problem-statement` | Problem statement in Newry's standard template | SoW/proposal |
| `fact-finding` | Pre-populated fact-finding worksheet | Problem statement |
| `value-creation` | Value creation hypothesis — 6 Airtable value fields + the deck value-creation page | Problem statement |
| `issue-tree` | MECE issue tree with hypotheses + prioritization | Problem statement |
| `workplan` | Sequenced activity list per issue + timeline guidance | Issue tree + timeline |
| `ownership-and-goals` | Ownership & responsibilities table — who owns what + value-creation & development goals | Value hypothesis + activity list + team roster |
| `account-management` | Stakeholder plan + per-stakeholder Standing Context notes (Context Log) | Problem statement + stakeholder list |

## Usage logging

At the start of every run — before any other work — create one record in the Airtable Plugin Usage Log. Silent and automatic; no user-facing output.

- **Base ID:** `appRawPuacfAvVH2Z` | **Table ID:** `tblmACtwIClniGn5n`
- **Tool:** `create_records_for_table`
- **Fields:**
  - `fldRrr3BkrJW8rE3L` (ts) — current UTC time, ISO 8601 (e.g. `2026-05-26T14:30:00Z`)
  - `fldNHK285dPCOdNhB` (plugin) — `"project-launch-toolkit"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — whichever sub-skill is being invoked; use `"general"` if routing hasn't resolved yet
  - `fldmTXyfFZRpbZEvQ` (user_id) — use the user's email address from the session context (available in the system prompt `<user>` block); if not available, use `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — project code if discernible; otherwise `""`

If the write fails for any reason, continue silently.

## Feedback capture

Applies across all sub-skills. Read and follow the shared feedback-capture sub-skill:
`sub-skills/feedback-capture/SKILL.md`

When logging:
- `Plugin:` → `project-launch-toolkit`
- `Sub-skill:` → whichever sub-skill is active; use `general` if none

## Inputs

**Required:**
- SoW or proposal (uploaded file, pasted text, or SharePoint link)

**Collected during the flow:**
- Project code (needed for workplan, account management)
- Team roster with roles (needed for ownership and goals, account management)
- Project timeline — start date, key milestones, end date (needed for workplan)

**Optional:**
- Specific sub-skill to run (if not running the full flow)

## How to Use

### Full launch flow
Say: "Run a project launch" or "Let's launch [project name/code]"

### Individual sub-skill
Say: "Run the issue tree" / "Give me the fact-finding worksheet" / "Build the workplan"

The coordinator routes directly to that sub-skill and collects only the inputs it needs.

## Opening Question

**The first thing the coordinator always does** — before asking for any materials — is show this checklist and ask where the EM is in the process:

```
Welcome to the Project Launch Toolkit. Here's the full launch checklist:

  1. Launch intake — Airtable project record (Phase 0)
  2. Problem statement
  3. Fact-finding worksheet
  4. Value creation hypothesis
  5. Issue tree
  6. Workplan
  7. Ownership & goals
  8. Account management / stakeholder plan

Have you already completed any of these steps? List the numbers (e.g., "1, 2") or say "none" to start from the beginning.
```

Based on the response:
- **"None"** → start at Step 1; ask for the SoW/proposal
- **Some steps done** → skip completed steps; ask for the relevant outputs before continuing (e.g., if Steps 1–3 are done, ask for the existing problem statement and issue tree before building the workplan)
- **Jumping to a specific step** → collect only the inputs that step needs

## Full Launch Flow

```
Phase 0: launch-intake
  → Reads SoW; creates/updates the Airtable project record (factual fields only)
  → Runs before everything else

Step 1: problem-statement
  → Reads SoW; drafts problem statement; flags gaps
  → Output reviewed by EM before proceeding

Step 2: fact-finding  *(can run in parallel with Step 1)*
  → Mines SharePoint, Airtable, web for prior work + SMEs + external sources

Step 3: value-creation
  → Takes the problem statement; builds the value hypothesis with the EM (collaborative);
    writes the 6 Airtable value fields + feeds the deck value-creation page
  → Requires the problem statement (leans on the SMART objective)

Step 4: issue-tree
  → Takes problem statement; proposes framework by reading the problem (not a project-type classification); drafts MECE tree as editable drag-and-drop artifact + chat table + CSV download
  → Output reviewed by EM before proceeding to workplan

Step 5: workplan
  → Converts issue tree → sequenced activity list per issue + timeline guidance (EM builds the Gantt); ends with a named workstream summary that feeds the ownership matrix
  → Requires timeline (budget optional)

Step 6: ownership-and-goals
  → Opens with a question; presents an editable responsibility matrix (rows = suggested workstreams, columns = team members, cells = Lead/Support/— with free-text popover); synthesizes per-person value creation goals from value hypothesis + responsibilities; drafts professional development goals
  → Requires team roster + value hypothesis (value-creation) + workstream summary (workplan)

Step 7: account-management
  → Pulls relationship history from Airtable; writes a Standing Context note per stakeholder to Context Log; outputs stakeholder plan
  → Requires stakeholder list from problem statement
```

## Launch Data File

After each sub-skill completes, the coordinator writes that section incrementally to `launch-data.json`. This file is consumed by the deck-builder `fill_launch_deck` operation in a Code session to auto-populate the open project initiation PPT.

**Write path (in order):**
1. `~/newry-projects/<project-code>/launch-data.json` — create the folder if it doesn't exist
2. Fallback: `~/Desktop/<project-code>-launch-data.json` — if `newry-projects\` root doesn't exist or folder creation fails

**On every write:** note in chat where the file was written.

**Section mapping** — each sub-skill writes its key when it completes:

| Sub-skill | JSON key written |
|---|---|
| launch-intake | `project` |
| problem-statement | `problem_statement` |
| value-creation | `value_creation` |
| issue-tree | `issue_tree` |
| workplan | `workplan` |
| ownership-and-goals | `ownership` |
| account-management | `account_management` |

**Write behavior:** read the existing file if it exists, merge the new section in, write back. Never overwrite the whole file — preserve sections written by prior sub-skills.

**Structure:**
```json
{
  "project": { "code": "", "client": "", "date": "" },
  "problem_statement": { "situation": "", "complication": "", "question": "", "smart_objective": "", "scope": "" },
  "value_creation": { "category": "", "value_low": 0, "value_mid": 0, "value_high": 0, "fair_share": 0, "upside": 0, "confidence": "", "narrative": "", "key_assumptions": [] },
  "issue_tree": { "root_question": "", "issues": [] },
  "workplan": { "workstreams": [] },
  "ownership": { "team": [] },
  "account_management": { "client_overview": "", "stakeholders": [] }
}
```

**Inner structure — arrays:**

`issue_tree.issues` — one entry per row of the issue tree markdown table:
```json
{ "level": "1.1", "text": "Issue text", "hypothesis": "Hypothesis text or null" }
```

`workplan.workstreams` — one entry per workstream from the workstream summary. Group activities from the issue-based activity list into the workstream they belong to:
```json
{ "name": "Workstream name", "description": "One-line description", "activities": ["Activity 1", "Activity 2"] }
```

`ownership.team` — one entry per person from the ownership table:
```json
{ "role": "EM", "name": "Name", "responsibilities": "...", "value_goal": "...", "dev_goal": "..." }
```

`account_management.stakeholders` — one entry per stakeholder, mapping the three questions directly:
```json
{ "name": "", "title": "", "role": "Sponsor", "success": "...", "concerns": "...", "next_challenge": "...", "crm_owner": "", "crm_goals": ["..."] }
```

**Extraction mapping** — what to pull from each sub-skill's output when writing its JSON section:

| Sub-skill | JSON key | Extract from |
|---|---|---|
| launch-intake | `project` | Project code, client name, start date — from the LAUNCH INTAKE COMPLETE confirmation block |
| problem-statement | `problem_statement` | situation + complication from CLIENT BUSINESS CONTEXT bullets; question + smart_objective from PROJECT OBJECTIVE; scope from SCOPE section |
| value-creation | `value_creation` | All fields from the VALUE CREATION COMPLETE block; key_assumptions as an array of strings |
| issue-tree | `issue_tree` | root_question from the root question line; issues as flat array from the markdown table (level, text, hypothesis) |
| workplan | `workplan` | workstreams from the Suggested workstreams block; activities grouped from the issue-based activity list into the workstream each belongs to |
| ownership-and-goals | `ownership` | team as array from the ownership table (role, name, responsibilities, value_goal, dev_goal per person) |
| account-management | `account_management` | client_overview from the CLIENT RELATIONSHIP OVERVIEW paragraph; stakeholders as array (name, title, role, success, concerns, next_challenge, crm_owner, crm_goals per person) |

**Design note:** `launch-data.json` is a point-in-time snapshot written as each sub-skill completes. Sections are not updated if artifacts are edited after the PLT run — the deck fill reflects the state at time of writing.

## Coordinator Behavior

- **Always open with the checklist question.** Don't assume the EM is starting from scratch.
- **Accept prior work as inputs.** If the EM says steps are already done, ask them to share those outputs before proceeding — don't re-run completed steps.
- **Pause for review after high-stakes outputs.** After problem-statement and issue-tree, pause and ask the EM to review before proceeding. These outputs gate everything downstream.
- **Don't re-collect inputs already provided.** If the problem statement has already been produced in this session, use it.
- **Handle partial flows gracefully.** If the EM only wants one step today, run it and stop. Don't push for the full flow.
- **Flag gaps explicitly.** If a sub-skill can't be completed due to missing inputs (e.g., workplan needs team roster), flag what's missing and offer to proceed with what's available.
- **Compile on request.** At any point the EM can ask for a compiled launch document — the coordinator assembles all outputs produced so far into a single structured doc.

## Compiled Launch Document Format

When compiled, the full launch package follows the project initiation template structure:

```
PROJECT LAUNCH — [Client Name] — [Project Code]
Date: [date]

SECTION 1: PROBLEM STATEMENT
[output from problem-statement sub-skill]

SECTION 2: FACT-FINDING WORKSHEET
[output from fact-finding sub-skill]

SECTION 3: VALUE CREATION
[output from value-creation sub-skill]

SECTION 4: ISSUE TREE
[output from issue-tree sub-skill]

SECTION 5: WORKPLAN
[output from workplan sub-skill]

SECTION 6: OWNERSHIP & GOALS
[output from ownership-and-goals sub-skill]

SECTION 7: ACCOUNT MANAGEMENT
[output from account-management sub-skill]

⚠️ GAPS & OPEN ITEMS:
[Aggregated list of all flagged gaps across sub-skills]
```

## Design Notes

- **Launch-intake is Phase 0 and runs first.** It writes the factual Airtable project record. Value creation runs after the problem statement because the value hypothesis leans on the SMART objective.
- **Problem statement is the foundation.** Every other sub-skill depends on it directly or indirectly. If it's weak, everything downstream is weak. The pause-and-review after problem-statement is intentional.
- **Issue tree gates the workplan.** Do not proceed to workplan with a weak issue tree. Flag this explicitly if the EM tries to skip the review.
- **Account management is the most Airtable-dependent sub-skill.** It reads from and writes to Contacts + Context Log. If Airtable is unavailable, it degrades to output-only mode and flags that persistence did not occur.

## References

- `references/202602 Project Initiation Template.pptx` — full project initiation template structure
- `references/project initiation resources/2025 Consulting Process and Thought Leadership Onboarding.md` — full project launch process
