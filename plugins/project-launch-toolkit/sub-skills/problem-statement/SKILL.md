---
name: problem-statement
description: Draft a Newry project problem statement from a SoW or proposal. Use at the start of every project launch. Produces a filled-in problem statement in Newry's standard template, ready for team review at kickoff.
---

# Problem Statement Sub-Skill

Draft a complete Newry problem statement from a proposal or SoW, ready for the EM to share with the team and editor at kickoff.

## Inputs

**Required — at least one source describing the project.** A SoW or proposal is ideal but not assumed; use whatever exists (proposal/scoping deck, scoping notes, kickoff emails, call notes). Fed by paste, uploaded/dragged-in files, or a mounted/SharePoint folder path. Read across all materials provided. "SoW" below is shorthand for whatever was provided.

**Optional (used if available):**
- Prior relationship history from Airtable (surfaced automatically if this client has prior Context Log notes)
- Past AER learnings from Airtable (if Newry has worked with this client before)
- Any client-provided materials (from `From Client/` folder on SharePoint)

**Read the method first.** Before drafting, read `references/project initiation resources/Problem Structuring Training - Issue Trees (2015).md` (problem-statement template) and `references/project initiation resources/2025 Consulting Process and Thought Leadership Onboarding.md` (SMART criteria). Match Newry's standard structure — don't improvise it.

## What This Skill Does

1. **Reads the proposal/SoW** and extracts: client business context, stated objectives, scope boundaries, stakeholders named, timeline, and any risks mentioned
2. **Pulls prior context (Airtable only)** — queries Airtable Context Log filtered by company to surface prior engagement intelligence, watch-outs, and relationship history. Deep SharePoint/document digging is fact-finding's job — don't duplicate it here.
3. **Drafts the problem statement** in Newry's standard template (see Output Format below)
4. **Flags gaps** — fields it couldn't fill from available materials, with a note on what to ask the client or ED

## Output Format

```
CLIENT BUSINESS CONTEXT:
[2–4 bullets on the client's situation and complication — the "why now" for this engagement, including the key assumptions the client holds that this work will test]

STAKEHOLDERS:
  Sponsor: [name + title]
  Sponsor's goals: [what success looks like for them]
  Direct contact: [name + title]
  Direct contact's goals: [their specific objectives]
  Other stakeholders/goals: [any others named in proposal]

SCOPE:
  In scope: [explicit scope from SoW]
  Out of scope: [explicit exclusions; infer from SoW if not stated]
  Client's preferred level of accuracy: [infer from project type and budget; flag if unclear]

PROJECT OBJECTIVE:
[One SMART sentence — Specific, Measurable, Action-oriented, Relevant, Time-bound — stating what success looks like: the information the client needs to act, and where Newry can go above and beyond]
[If SoW objective is vague, draft a tighter version and note the assumption]

RISKS:
[3–5 risks — pull from SoW risk language; supplement with standard project risks for this project type]

KEY CLIENT MILESTONES:
[Dates from SoW; flag if none specified]

⚠️ GAPS (items requiring EM/ED input before kickoff):
[List any fields that couldn't be filled from available materials]
```

## Design Notes

- **SMART objective is the highest-leverage output.** SoW language is often vague; the skill should draft a sharper version and explicitly note any assumptions made (e.g., "assumed 12-week timeline based on fee schedule").
- **Don't hallucinate stakeholders.** If stakeholder names aren't in the SoW, leave blank with a prompt to fill in at kickoff rather than guessing.
- **Scope inference is acceptable for common exclusions** (e.g., implementation is typically out of scope for Newry strategy engagements) but should be flagged as inferred.
- **Risks should be project-type-aware.** Growth Engine risks differ from Innovation/Tech Push risks differ from M&A risks. The skill should be calibrated to Newry's common project types.
- **Weave in assumptions and success — there are no separate slide boxes for them.** Surface the client's key assumptions-to-test inside Client Business Context (they also seed the issue tree), and the success definition inside the SMART objective. Don't create orphan fields the slide can't hold.
- **Output is a draft, not a final.** Close with: "Review with your team at kickoff. The editor should also receive this before the first deck review."

## References

- `references/project initiation resources/2025 Consulting Process and Thought Leadership Onboarding.md` — problem statement template and SMART criteria
- `references/project initiation resources/Problem Structuring Training - Issue Trees (2015).md` — alternate template format
- `references/202602 Project Initiation Template.pptx` — the problem statement page (read via the pptx skill if the live artifact structure is needed)
