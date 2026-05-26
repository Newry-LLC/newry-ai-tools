---
name: technical-orientation
description: >
  Use this skill at the start of any new client engagement to build a Technical Orientation document.
  Triggers on: "start technical orientation", "build tech orientation", "run technical onboarding",
  "project technical orientation", "tech orientation doc", "kick off the technical doc",
  "map the client's technology", or any request to understand a client's technology and
  competitive position at project launch.
metadata:
  version: "0.1.4"
  author: "Newry Corp"
---

# Technical Orientation Skill

## Purpose

Guide a consultant through building a Technical Orientation document at the start of a new engagement. The output is a structured .docx artifact that maps the client's technology, customer value, competitive position, and open questions. The consultant shares this with the project team during week 1.

This is a collaborative process — not a form-fill. Push back on vague answers, offer hypotheses based on your knowledge of the sector and competitive landscape, flag gaps, and actively help the consultant produce a sharper artifact than they would alone.

---

## Usage logging

At the start of every run — before any other work — create one record in the Airtable Plugin Usage Log. Silent and automatic; no user-facing output.

- **Base ID:** `appRawPuacfAvVH2Z` | **Table ID:** `tblmACtwIClniGn5n`
- **Tool:** `create_records_for_table`
- **Fields:**
  - `fldRrr3BkrJW8rE3L` (ts) — current UTC time, ISO 8601 (e.g. `2026-05-26T14:30:00Z`)
  - `fldNHK285dPCOdNhB` (plugin) — `"project_technical_onboarding"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — always `"technical_orientation"`
  - `fldmTXyfFZRpbZEvQ` (user_id) — read `~/.user_id` if it exists; otherwise `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — infer from SOW, proposal, or project code if mentioned; otherwise `""`

If the write fails for any reason, continue silently.

---

## Step 0 — Project setup and verification

Note: Usage logging (above) runs first — before Step 0. Step 0 runs before Steps 1–4.

Run the shared project setup block before anything else:
→ `../../../project-setup/SKILL.md`

**Skill subfolder for this plugin:** `Technical Orientation`
No required sub-subfolders.

If `project-setup/SKILL.md` is not found: ask the consultant to confirm the project name and code, warn that project verification and mismatch detection are unavailable, and proceed without folder structure enforcement.

After Step 0 completes and project identity is confirmed, ask:

> "Are we building a new Technical Orientation document, or updating an existing one?"

**If fresh run:** proceed to Step 1.

**If update:** ask the consultant to share the existing document and describe what has changed or what new understanding needs to be captured. Then:
- Read the existing document
- Ask focused questions only about the sections that need updating — do not re-run the full interview
- Apply the same collaboration behaviors as Step 2 (push back, offer hypotheses, flag gaps)
- Regenerate only the affected sections, or regenerate the full document if changes are substantial — confirm with the consultant which they prefer before generating
- Update the status line in the document header to reflect the new version (e.g., "Updated Draft — [Month Year]")

---

## Step 1: Inputs Prompt

Before beginning the interview, tell the consultant what to pull together:

> "Before we start, gather whatever you have of the following — the more you bring, the stronger the first draft:
> - **Project proposal or SOW** — scope, engagement type, objectives
> - **Client website and product pages** — especially product descriptions and customer-facing materials
> - **Spec sheets, data sheets, or technical documentation** — if available
> - **Prior Newry materials** on this client or sector (check SharePoint or Airtable)
> - **Key client contacts** identified so far, especially any technical contacts
> - **Any secondary research** already gathered on the sector or competitive landscape
>
> At minimum I need: (1) a project-context document — SOW, proposal, kickoff deck, or similar — OR a description from you of what the engagement is and what you're trying to accomplish, and (2) the client's website and the specific product(s) or technology(ies) relevant to the engagement. Without these I won't have enough context to be useful."

Wait for the consultant to share inputs. If they have not provided the minimum (project context + product/technology scope), do not proceed — ask for them directly before starting the interview. Review all materials provided before beginning Step 2.

---

## Step 2: Guided Interview

Work through the four artifact sections in order. Treat this as a thinking partnership, not a data collection exercise.

**For each section:**
- Ask conversationally, not as a checklist
- Synthesize answers into draft artifact language in real time
- Push back when answers are vague, circular, or don't pass the "so what" test
- Offer your own hypotheses where you have relevant knowledge of the sector, technology, or competitive landscape — label these clearly as hypotheses for the consultant to validate
- Flag explicitly when a section has gaps that need to be resolved via client interviews or research
- Confirm each section's draft with the consultant before moving on

See `references/interview-guide.md` for the full question bank, follow-up probes, and guidance on what good looks like for each section.

### Sections

**1. Product & Technology** — What does the product do and how does it work at a functional level? The consultant should be able to explain this to a colleague in plain language. Covers: function, mechanism, key performance parameters, known limitations, and production/delivery where relevant.

**2. Value Creation** — The analytical core. Work through four sub-sections:
- *Value Chain Position:* Where does the client sit? Who are their customers and their customers' customers? What does their product enable downstream?
- *How Value Is Created:* Map the technology against the four value creation categories (system performance, efficiency, reliability/risk reduction, market expansion). Identify the primary mechanism and be specific about magnitude.
- *Differentiated vs. Commodity:* Determine whether this is a differentiated-tech play or a commodity-plus-business play. For differentiated: source, specifics, durability. For commodity: build the table stakes checklist, then identify where the client actually wins.
- *Competitive Value Creation:* Who else creates similar value? Map the competitive set technically — who leads, who's at parity, who trails, and what could change in 3–5 years.

**3. Value Capture** — Who captures the value created, how much flows to the client, and what drives or limits monetization. Covers: value distribution across the chain, customer buying dynamics (who decides, why, what substitutes), pricing power, and switching costs.

**4. Key Engagement Questions** — The bridge between technical understanding and engagement objectives. Identify 3–6 questions whose answers materially affect how the team should approach *this specific engagement*, drawn directly from the project SOW or proposal. For each: why it matters, how it gets resolved, who owns it, and by when.

---

## Step 3: Collaborative Drafting

Draft artifact sections in real time as the interview progresses — do not wait until the end. After each section is confirmed, move to the next. Apply the same collaboration behaviors described in Step 2 throughout the drafting process.

---

## Step 4: Generate the Document

When all five sections are complete and confirmed, generate the .docx artifact.

Before generating: set `TECHNICAL_POSITION_TYPE` in the script to `'differentiated'` or `'commodity'` based on the determination made in Step 3. This controls which template renders for Section 3 — getting this wrong produces the wrong document structure.

- See `references/artifact-structure.md` for the exact document structure, section content, and formatting guidance
- See `references/docx-generation.md` for the complete docx-js generation code pattern

**File naming:** `[Client Name] Technical Orientation — [Project Code].docx`
Save to `Technical Orientation/[Client Name] Technical Orientation — [Project Code].docx` within the current working directory.

After saving, remind the consultant: this is a living document. Update it as the engagement progresses and new technical understanding emerges. It should reflect what the team actually knows, not just what was known at kickoff.

---

## Feedback capture

Applies across all interactions. Read and follow the shared feedback-capture sub-skill: `../../../feedback-capture/SKILL.md`

Populate `Plugin: project-technical-onboarding` and `Sub-skill: technical_orientation` in all log entries.
