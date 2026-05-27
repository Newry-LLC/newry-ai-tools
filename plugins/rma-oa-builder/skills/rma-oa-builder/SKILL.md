---
name: rma-oa-builder
description: Use this skill whenever a consultant is building a Rapid Market Assessment (RMA) or Opportunity Assessment — scoping it, designing the research approach, doing secondary research, or drafting sections. Triggers on "I'm starting an RMA," "help me build an opportunity assessment," "scope this RMA," "let's do the market research for this project," "draft the market section," or any request to design, research, or produce an RMA or Opportunity Assessment deliverable, even if the user doesn't use those exact terms.
---

# RMA / Opportunity Assessment Builder

A skill for designing and building Rapid Market Assessments (RMAs) and Opportunity Assessments at Newry. Guides the consultant from project intake through secondary research and section drafting, with a defined handoff to primary research when needed.

**What this skill does not do:** conduct primary research interviews, synthesize transcripts, or produce final polished slides. Primary research is handled by the Primary Research Toolkit. Slide production is the consultant's job.

---

## Step 0 — Project setup and verification

Run the shared project setup block before anything else:
→ `../../project-setup/SKILL.md`

**Skill subfolder for this plugin:** `RMA`
No required sub-subfolders.

If `project-setup/SKILL.md` is not found: ask the consultant to confirm the project name and code, warn that project verification and mismatch detection are unavailable, and proceed without folder structure enforcement.

After Step 0 completes and project identity is confirmed, proceed to Phase 1 below.

---

## Overview

Every RMA follows two phases:

**Phase 1 — RMA Design:** Collect project context, read any SOW or proposal, recommend a tier, scope each section, and produce an RMA Design Document for consultant review and approval.

**Phase 2 — Execution:** Run secondary research section by section, draft each section with available data, flag gaps, check in on whether primary research is warranted, and produce an incrementally-built RMA draft document.

The five canonical content sections of every Newry RMA:
1. **Market** — size (TAM/SAM/SOM), growth, dynamics, regulatory context
2. **Customers** — segmentation, value chain & buying process, pain points, WTP (conditional)
3. **Competitive Landscape** — players, positioning, barriers to entry
4. **Client Fit** — value prop vs. what the market values, differentiation, gaps
5. **Path to Market & Risks** — GTM approach, barriers to adoption, key uncertainties

Depth within each section varies by tier and project specifics set in Phase 1.

---

## Phase 1: Intake & RMA Design

### Step 1 — Collect context

Ask the consultant for the following. If a SOW or proposal is available, read it first — extract what you can before asking questions, and ask only for what's still missing.

Collect all of the following, in as few turns as possible:

1. **Client and project code** — e.g., "DuPont, DUP38"
2. **Product or technology being assessed** — what it is, what it does, where it is in development (early R&D / pre-commercial / commercial)
3. **Target application or market** — what specific application, end market, or use case is being evaluated
4. **Decision this RMA informs** — go/no-go, investment prioritization, partnership decision, internal alignment, other
5. **Engagement timeline** — when is the deliverable due; how many weeks does the team have
6. **Agreed scope** — what has been promised to the client; read any SOW or proposal provided
7. **What's already known** — prior research, existing data, context documents the team has; ask the consultant to share or point to them

If any SOW, proposal, or context document is available, read it before asking questions — extract answers where possible.

### Step 2 — Recommend a tier

Based on intake, recommend one of three tiers. Show the recommendation with a one-sentence rationale and invite the consultant to adjust.

| Tier | Label | Description | When to use |
|------|-------|-------------|-------------|
| 1 | Scoping RMA | Secondary research only; directional output | Early-stage product, short timeline (≤3 weeks), goal is directional go/no-go or internal alignment |
| 2 | Standard RMA | Secondary + targeted primary (3–8 interviews) on key gaps | Defined product, medium timeline (3–6 weeks), SOW includes targeted interviews, need to validate specific hypotheses |
| 3 | Full RMA | Secondary + full primary research program via PRT | Commercial-stage product or technology, longer timeline, SOW specifies significant primary research, multiple application segments |

**Recommendation logic:**
- Default to Tier 1 unless intake signals clearly point to Tier 2 or 3
- Tier 2 signals: SOW mentions interviews; client product has defined specs; key questions (pain points, competitive dynamics, WTP) can't be answered from secondary data alone
- Tier 3 signals: SOW specifies substantial primary research budget; multiple application segments to evaluate; product is defined and client is close to a go/no-go decision requiring high-confidence inputs

### Step 3 — Scope each section

For each of the five canonical sections, determine:
- **Depth:** light (directional framing only) / standard (quantified where possible, evidence-backed) / deep (bottom-up build, primary research required)
- **Key questions:** what specifically does this section need to answer for this project
- **Primary research needed:** yes/no, and for which questions

Use the SOW, agreed scope, and tier to set depth. If the SOW is silent on a section, default to standard depth.

**Section scoping defaults by tier:**

| Section | Tier 1 | Tier 2 | Tier 3 |
|---------|--------|--------|--------|
| Market | Light — top-down sizing, directional growth | Standard — bottom-up SAM + top-down sanity check, key dynamics | Deep — full bottom-up build, regulatory, dynamics |
| Customers | Light — segment identification, pain point framing | Standard — segment sizing, buying process, pain points; primary fills gaps | Deep — full primary research, WTP if applicable |
| Competitive Landscape | Light — incumbent identification, barrier flags | Standard — player profiles, positioning, barrier analysis | Deep — full competitive map, primary-validated dynamics |
| Client Fit | Light — directional fit assessment against known customer needs | Standard — structured value prop mapping | Deep — primary-validated fit, gap analysis |
| Path to Market & Risks | Light — GTM options, key risk flags | Standard — GTM path with evidence, barrier analysis | Deep — primary-validated GTM, scenario analysis |

### Step 4 — Check in

Present the RMA Design Document (see format below) and ask: *"Does this reflect what you're building? Anything to adjust before I start research?"*

Do not proceed to Phase 2 until the consultant confirms.

## Phase 1 close — session log

Append a single entry to `RMA/rma-log.md` (create if it doesn't exist):

```
---
Date: [YYYY-MM-DD]
Phase: 1 — Design complete
Project: [project code]
Tier: [1 / 2 / 3]
Sections scoped: [list]
Design doc: RMA/[ProjectCode]-RMA-Design.md
Gaps flagged: [any sections with known data gaps]
Next step: Phase 2 — Execution
```

### RMA Design Document format

Save as `RMA/[ProjectCode]-RMA-Design.md` in the current working folder.

```markdown
# RMA Design Document
**Project:** [Client, Project Code]
**Date:** [YYYY-MM-DD]
**Tier:** [1 / 2 / 3] — [Scoping / Standard / Full]

## Opportunity
[One paragraph: product/technology, target application/market, development stage, decision being informed]

## Tier rationale
[2–3 sentences: why this tier given the timeline, scope, and product stage]

## Section plan

### 1. Market
**Depth:** [light / standard / deep]
**Key questions:**
- [question]
- [question]
**Primary research needed:** [yes — for X / no]

### 2. Customers
**Depth:** [light / standard / deep]
**Key questions:**
- [question]
- [question]
**WTP:** [include / exclude — rationale]
**Primary research needed:** [yes — for X / no]

### 3. Competitive Landscape
**Depth:** [light / standard / deep]
**Key questions:**
- [question]
- [question]
**Primary research needed:** [yes — for X / no]

### 4. Client Fit
**Depth:** [light / standard / deep]
**Key questions:**
- [question]
- [question]
**Primary research needed:** [yes — for X / no]

### 5. Path to Market & Risks
**Depth:** [light / standard / deep]
**Key questions:**
- [question]
- [question]
**Primary research needed:** [yes — for X / no]

## Research plan
**Secondary:** [sources to prioritize — industry reports, trade publications, company filings, prior Newry work]
**SharePoint scan:** [yes — search terms / not applicable]
**Primary:** [Tier 2: targeted interviews — sections and questions; Tier 3: full PRT program]

## Timeline
[Milestones: secondary research complete, check-in, primary fieldwork if applicable, draft complete]

## Key hypotheses to test
- [hypothesis]
- [hypothesis]
```

---

## Phase 2: Execution

### Step 1 — Secondary research

Run all five sections before checking in with the consultant.

For each section, follow this pattern:
1. Search web for relevant data using the key questions from the Design Document as search targets
2. If SharePoint scan was flagged in the design plan, run a targeted search for prior Newry work in adjacent spaces (same client, similar application, same end market)
3. Draft the section with available evidence — be specific: cite numbers, name companies, reference sources
4. Flag gaps and uncertainties inline using `[GAP: description of what's missing and why it matters]`
5. Note where primary research would materially improve confidence

**Source priorities by section:**

*Market*
- Industry analyst reports (MarketsandMarkets, Grand View, IBISWorld, Mordor, IBIS); published market sizes and forecasts
- Trade association publications and industry body data
- Company 10-Ks and earnings calls for market commentary
- Regulatory agency websites when regulatory context is in scope
- Bottom-up sizing: build from unit counts × usage rates × price when top-down reports are unavailable or untrustworthy for the specific application
- Always triangulate top-down (published report) against bottom-up (build from first principles); flag where they diverge

*Customers*
- Trade press and industry publications for segment descriptions and pain point framing
- Company websites, job postings, and LinkedIn for buying role identification
- Earnings calls and investor presentations for market dynamics commentary
- Industry association membership lists for value chain mapping
- Price benchmarks from distributor websites, procurement databases, or product listings to anchor WTP (when applicable)

*Competitive Landscape*
- Company websites and product pages for positioning and specs
- Press releases and news for recent moves, investments, partnerships
- Patent filings for technology differentiation signals
- Trade press for competitive commentary
- Industry association participation lists for player identification

*Client Fit*
- Primarily synthesis of Sections 1–3 combined with client product information from intake documents
- Limited new web research needed; structure the evidence in two parts: (a) what the market values (drawn from Sections 1–3 findings on customer needs, pain points, and competitive dynamics), and (b) what the client offers against those needs (drawn from intake documents and product specs)
- Do not state a fit conclusion — structure the evidence so the consultant can draw their own verdict
- If product specs are not available from intake documents, note this as a gap — fit assessment is limited without them

*Path to Market & Risks*
- Industry reports and trade press on distribution channel structures
- Company websites for channel partner identification
- Regulatory body sites for qualification and certification requirements
- Synthesis of competitive findings for barrier and risk inputs
- News for market timing signals (competitive moves, technology shifts, regulatory changes)

**Drafting standards:**
- Lead each section with a 2–3 sentence summary of the key finding before supporting detail. Exception — Client Fit: lead with the evidence structure (market needs vs. client offering), not a fit verdict.
- Use numbers wherever available — market sizes, growth rates, player counts, price ranges
- Attribute claims to sources (inline, brief: "per MarketsandMarkets 2024")
- Use `[GAP: ...]` consistently — be specific about what's missing, not just that data is unavailable
- Do not pad thin sections with caveats — a short, honest section is better than a long uncertain one

---

### Step 2 — Secondary check-in

After completing all five section drafts, present a structured summary before proceeding:

**What's established** — findings with sufficient secondary evidence to stand; note confidence level where relevant

**Key gaps** — open questions that secondary research could not answer; organized by section

**Primary research recommendation** — one of:
- *Primary research may not be required:* summarize what the secondary evidence covers and what gaps remain, then ask the consultant: "Based on what we have, do you want to proceed to final assembly, or does [gap area] warrant primary research first?" The consultant makes the call; the skill surfaces the evidence.
- *Targeted interviews recommended:* [N] interviews focused on [specific sections and questions]; propose scope
- *Full primary research program recommended:* gaps are material to the decision; hand off to PRT

For Tier 1 engagements where primary research is not warranted: proceed directly to Step 4.

For Tier 2/3 or when primary research is recommended: wait for consultant confirmation on interview scope before handing off.

---

### Step 3 — Primary research handoff (Tier 2 / Tier 3)

When primary research is confirmed, hand off to the Primary Research Toolkit (PRT).

**What to provide to PRT:**
- The RMA Design Document (`RMA/[ProjectCode]-RMA-Design.md`) as project context
- The section drafts with `[GAP: ...]` flags as the research brief — these gaps are the primary research questions
- The five canonical sections as the analytical frame PRT should code against

**Handoff instruction to give the consultant:**
> "Use the Primary Research Toolkit to design interview guides and run fieldwork. Point PRT to this project folder — the design document and section drafts are the framing context. When ICS synthesis is complete, come back here to assemble the final RMA draft."

**On return from PRT:**
- Read the synthesis outputs (roll-up, summary cards) from the `Primary Research/outputs/` folder
- For each `[GAP: ...]` flag, check whether PRT synthesis provides an answer
- Fill confirmed gaps with primary research findings, attributed to source type (e.g., "per [N] customer interviews")
- Retain and annotate gaps that primary research did not resolve

---

### Step 4 — Final assembly

Assemble the RMA draft document from the five completed section drafts.

**Assembly process:**
1. Remove `[GAP: ...]` flags that have been filled — replace with the finding
2. For gaps that remain open after primary research (or in Tier 1 where no primary was run): convert to a clearly labeled "Open questions / areas for further investigation" note at the end of the relevant section
3. Check cross-section consistency — numbers cited in different sections should not conflict; if they do, flag and reconcile
4. Write a one-paragraph framing note at the top of the draft (internal, not client-facing): overall confidence assessment, what the RMA can and cannot support, what would be needed to increase confidence

**Save as `RMA/[ProjectCode]-RMA-Draft.docx`** using python-docx. Structure:

```
Title: [Client] [Application/Market] Opportunity Assessment
Subtitle: DRAFT — [Date]

Section 1: Market
Section 2: Customers
Section 3: Competitive Landscape
Section 4: Client Fit
Section 5: Path to Market & Risks

[Internal note: confidence assessment and open questions]
```

Apply standard Newry document styling: Calibri body font, left-aligned headings, no decorative formatting. The consultant will apply Newry template formatting before client delivery.

For consistent docx styling, reference the ICS docx generation pattern at `../primary-research-toolkit/sub-skills/interview-coding-synthesis/scripts/style_docx.py`. Apply the same Calibri font, heading hierarchy, and section spacing conventions used in ICS outputs.

## Output checklist

Before closing the session, verify all expected files exist in the `RMA/` folder:

- [ ] `RMA/[ProjectCode]-RMA-Design.md` — design document from Phase 1
- [ ] `RMA/[ProjectCode]-RMA-Draft.docx` — assembled draft from Phase 2
- [ ] `RMA/rma-log.md` — session log (Phase 1 and Phase 2 entries)

If any file is missing, recreate or flag before closing.

## Phase 2 close — session log

Append to `RMA/rma-log.md`:

```
---
Date: [YYYY-MM-DD]
Phase: 2 — Execution complete
Project: [project code]
Sections drafted: [list]
Gaps remaining: [any [GAP: ...] items not resolved]
Primary research warranted: [yes / no / partial]
Output: RMA/[ProjectCode]-RMA-Draft.docx
```

---

## Output files

| File | Format | When created |
|------|--------|--------------|
| `RMA/[ProjectCode]-RMA-Design.md` | Markdown | End of Phase 1, after consultant confirms |
| `RMA/[ProjectCode]-RMA-Draft.docx` | Word document | Built incrementally during Phase 2; complete at end |

---

## Usage logging

At the start of every run — before any other work — create one record in the Airtable Plugin Usage Log. Silent and automatic; no user-facing output.

- **Base ID:** `appRawPuacfAvVH2Z` | **Table ID:** `tblmACtwIClniGn5n`
- **Tool:** `create_records_for_table`
- **Fields:**
  - `fldRrr3BkrJW8rE3L` (ts) — current UTC time, ISO 8601 (e.g. `2026-05-26T14:30:00Z`)
  - `fldNHK285dPCOdNhB` (plugin) — `"rma_oa_builder"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — `"phase_1_design"` (intake through design doc) or `"phase_2_execution"` (research through final assembly); use `"general"` if neither applies yet
  - `fldmTXyfFZRpbZEvQ` (user_id) — read `~/.user_id` if it exists; otherwise `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — project code if discernible (e.g. `"DUP38"`); otherwise `""`

If the write fails for any reason, continue silently.

---

## Feedback capture

Read and follow the shared feedback-capture sub-skill: `../feedback-capture/SKILL.md`

When logging:
- `Plugin:` → `rma-oa-builder`
- `Sub-skill:` → `phase-1-design` or `phase-2-execution` depending on where feedback occurs; use `general` if neither applies
