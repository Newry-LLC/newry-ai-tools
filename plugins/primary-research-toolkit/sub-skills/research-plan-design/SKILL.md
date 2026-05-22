---
name: prt-research-plan-design
description: Use this sub-skill when starting a new primary research program and needing to decide which branches to prioritize, who to interview, how many, and how to source them. Part of the Primary Research Toolkit. Triggers on "help me plan the research," "which branches should I prioritize," "how many interviews do I need," "help me set up fieldwork for this project."
---

# Research Plan Design — SKILL.md

**Plugin:** Primary Research Toolkit
**Position in workflow:** First — runs before any fieldwork begins
**Feeds:** Interview Acquisition (parallel) + Interview Guide Design (parallel) → Interview Prep → Interview Coding & Synthesis

---

## What this sub-skill does

Takes a project's analytical frame and available scoping context, and produces a structured Research Plan through an interactive review. The plan answers five questions before a single interview is booked:

1. Which branches of the analytical frame are in scope — and which are essential vs. secondary?
2. Who needs to be interviewed, and how many of each type?
3. What is the recommended interview forum (phone, in-person, conference)?
4. What approach should Interview Coding & Synthesis use (direct reading vs. targeted extraction)?
5. Which questions should be standardized across the guide to enable cross-interview comparison?

The Research Plan is the foundation for both Interview Acquisition (who to find) and Interview Guide Design (what to ask). It is also the baseline against which ICS Mode 2's coverage table is assessed.

---

## What you need

**Primary source — read from the project folder first:**
- **`project.md`** — the project manifest; use it to understand scope, workstream boundaries, and where key files are located
- **Analytical frame** — issue tree, research questions, or hypothesis set; typically a PPTX or Word doc in `context/`
- **Scoping context** — SOW, proposal, or kickoff deck in `context/`; used to distinguish Newry's specific workstream from the full issue landscape

If the project folder is not set up or the relevant files are not obvious from `project.md`, ask before proceeding. Do not guess at scope.

**Also look for:**
- A hypothesis slide in the kickoff deck or project initiation materials — if present, use it directly; if not, generate placeholders (see Step 2)
- Any known constraints noted in `project.md` — timeline, interviewee access, geographic scope, budget, regulatory sensitivity
- Any existing ICS corpus noted in `project.md` — if one exists, identify the interviewee types it covers. **Internal-employee interviews are inside-out and do not constitute branch coverage for external research planning.** Only prior external-voice interviews (customers, market participants, experts) count toward coverage when setting branch priorities. If the existing corpus is internal-only, treat every branch as starting from zero for this plan.

**Fallback:** If no project folder exists, the user can paste the analytical frame and scoping context directly. Note this in the output summary.

---

## How this sub-skill works — interactive review

This sub-skill does not produce the full Research Plan in one pass. It works through the plan in four chunks, presenting each one and pausing for the consultant's reaction before moving forward. This keeps the output digestible and ensures the plan reflects the consultant's judgment, not just Claude's inference.

**The four chunks:**

1. **Scope + branch prioritization** — confirm which branches are in scope and what the working hypotheses are; everything downstream depends on this being right
2. **Value chain map + interviewee type map** — who to target and why; react before outreach numbers are locked in
3. **Forum + approach + standardization flags** — operational decisions; quick to react to once the target list is confirmed
4. **Money slide** — a direct question to the consultant; Claude asks, the consultant answers

After each chunk: present the work, ask if it looks right, incorporate feedback, then move to the next chunk. Feedback is free-form — the consultant can say "looks good," make specific changes, or ask questions. There are no menus or structured response formats.

When all four chunks are confirmed, write the final output files (see below). Do not write the files until all chunks are approved.

---

## What you produce

Two files saved to the project's `Primary Research/outputs/` folder:

```
Primary Research/outputs/Research Plan v1.md      — machine-readable reference for downstream sub-skills
Primary Research/outputs/Research Plan v1.docx    — readable version for the consultant and team
```

Both files contain the same content. The markdown file is the reference used by Interview Guide Design and Interview Coding & Synthesis. The docx is for sharing, reviewing, and revisiting mid-fieldwork.

**Contents:**
1. Summary of inputs — files used, constraints noted, any gaps flagged
2. Branch prioritization — Essential / Secondary / Out of scope, with rationale and working hypothesis per branch
3. Value chain map — the landscape of interviewee types and where they sit relative to the client
4. Interviewee type map — types needed, branches they address, target N and outreach count per type
5. Forum recommendation — phone, in-person, or conference, with rationale
6. Approach recommendation — direct reading vs. targeted extraction, with rationale
7. Standardization flags — which questions to ask in identical form across interviewees
8. Money slide — the consultant's description of the key output visual (or flagged as TBD)
9. Next step — what to do next and when to revisit

---

## Steps

### Step 1 — Read the project context

Open `project.md` and identify:
- The project scope and Newry's specific workstream
- Where the analytical frame and scoping documents are located
- Any constraints already noted (timeline, access, geography, budget)
- Whether a hypothesis slide exists in the project initiation materials

Then read the analytical frame in full. Identify:
- **Top-level branches** — the main questions or hypotheses the research is meant to address
- **Sub-branches** — the specific investigative lines under each top branch
- **Leaf nodes** — the most granular questions (these often translate directly to interview guide sections)
- **Total branch count and depth** — signals complexity and likely corpus size

Do not re-structure or summarize the analytical frame. Map it as given.

If key files are missing or the scope is ambiguous, flag it and ask before proceeding.

---

### Chunk 1 — Scope + branch prioritization

**Present:** A summary of what was read (files used, constraints noted, any gaps), followed by the branch prioritization table.

**Branch prioritization table** has four columns: Branch / Classification / Rationale / Working hypothesis.

Classification options:

| Classification | Meaning |
|----------------|---------|
| **Essential** | Must be addressed for this engagement to deliver; gaps here are a project risk |
| **Secondary** | Useful if coverage permits; not blocking but adds confidence |
| **Out of scope** | Explicitly excluded from this workstream; note why |

**Decision rule:**
- SOW names specific deliverables tied to a branch → Essential
- Branch informs a deliverable but is not the primary focus → Secondary
- Branch appears in the frame but is covered elsewhere → Out of scope
- When in doubt, mark Secondary and flag for confirmation
- Prior ICS corpus exists (internal-only) → treat every branch as starting from zero; do not downgrade any branch to Secondary on the basis of internal coverage alone. Internal interviews reflect Alta's view of the market, not the market's view of Alta.

**Working hypothesis per branch:**
- If a hypothesis slide exists in the project materials, pull from it directly
- If not, generate placeholder hypotheses from the issue tree framing
- One sentence per branch: what the team currently believes to be true, and what primary research needs to confirm or refute

Present hypotheses as a two-column table — Claude's draft on the left, "Your edits / comments" blank on the right. The consultant fills in any changes per row; they can confirm, rewrite, or write "no view yet" for any branch.

**After presenting Chunk 1:** Ask two specific questions:
- "Do these branch classifications match how your team is thinking about the workstream scope — particularly the out-of-scope calls?"
- "Do the working hypotheses reflect what your team actually believes going in, or are there branches where you have a stronger or different view?"

Incorporate any changes before moving to Chunk 2.

---

### Chunk 2 — Value chain map + interviewee type map

**Present:** First the value chain map, then the interviewee type map that flows from it.

**Value chain map:** Sketch the relevant value chain and market segments — suppliers, manufacturers, distributors, customers, end users, academics, trade associations, regulators, competitors. This is the primary tool for ensuring the target list covers the full landscape rather than just the most accessible contacts. Include a brief coverage check: are any major players or segments missing?

**Interviewee type map:** For each Essential and Secondary branch, identify which types can provide evidence. Standard types: Internal, Customer / end user, Expert, Competitive / market participant, Channel / distribution partner, Regulatory / policy stakeholder.

Aggregate across branches to produce a table: interviewee type / value chain position / branches covered / target interviews / target outreach / planning factor.

**Sample sizing:**
- Minimum per branch: 3–5 interviews of the right type; stop when new conversations stop producing new themes
- Aim for breadth within each type: mix segments, geographies, job titles, seniority levels
- Do not flatten types — customer and expert findings are not interchangeable

**Outreach planning factor — default 5X.** Adjust:
- Higher (7–10X): cold outreach, regulatory sensitivity, hard-to-reach populations, international interviews (allow 2–4 weeks lead time)
- Lower (2–3X): warm contacts, captive pool, conference setting

**Sequencing note:** Flag which types to approach first. Grounding interviews (academics, consultants, trade associations) should start Day 1 — they refine the guide before harder targets are engaged and often point to better sources. For hard-to-reach populations, flag whether an expert network (AlphaSights, Guidepoint, AlphaSense/Tegus) is warranted and note budget implications.

**After presenting Chunk 2:** Ask two specific questions:
- "Does this capture the right value chain? If not, I can help you refine it."
- "Do the target numbers look right? Tell me which types or numbers you'd adjust and I'll update."

Incorporate any changes before moving to Chunk 3.

---

### Chunk 3 — Forum + approach + standardization flags

**Present:** Three quick operational decisions.

**Forum recommendation:**

| Forum | When to use |
|-------|------------|
| **Phone / video** | Default; efficient, low barrier, suits sensitive topics, easy to schedule |
| **In-person** | High-priority interviewees; complex or sensitive topics; facility visits |
| **Conference** | High volume of targets in one place; compressed guide (20–30 min max); plan schedule before the event; verify target population will be present |

**Approach recommendation** — based on projected corpus size:

| Projected corpus | Recommended approach |
|-----------------|---------------------|
| < ~30 transcripts | **Direct reading** |
| ~30–80 transcripts | **Evaluate at kickoff** — reassess as corpus grows |
| > ~80 transcripts | **Targeted extraction** |

**Standardization flags:** The key question to settle before fieldwork begins — which questions should be asked in identical form to all interviewees of a given type? This must be decided now because it shapes the interview guide and cannot be retrofitted after fieldwork.

Flag a branch as a standardization candidate if:
- It has a clear working hypothesis to test
- The client will want segment-level breakdowns ("X of Y interviewees said Z")
- It is Essential and the question is contested across interviewee types

For each flagged branch, note the proposed question stem. Interview Guide Design will refine the wording.

**After presenting Chunk 3:** Ask two specific questions:
- "Are there questions you'd want to ask every interviewee of a given type in exactly the same way — word for word — so the answers can be compared directly?"
- "Anything else here look off?"

Incorporate any changes before moving to Chunk 4.

---

### Chunk 4 — Money slide

**Do not generate this section.** Ask the consultant directly:

> "Before we finalize the plan — what's the key output visual your client needs to see at the end of this workstream? The more specific you can be, the sharper the interview guide will be. For example: a bar chart showing distributor views on each barrier, a 2×2 of willingness to pay vs. switching cost by segment, a waterfall showing where candidates are lost across the funnel. What are you driving toward?"

Wait for the consultant's answer. Record it in their words.

If they can't answer yet, note it as TBD and flag it as an open item — but push for an answer first. A placeholder here is a real cost: the interview guide will be less focused without it.

**After Chunk 4:** Confirm the full plan is complete, then write both output files.

---

## Output format

```
# Research Plan — [Project Name]
**Date:** [date]
**Prepared by:** Primary Research Toolkit (Research Plan Design)

---

## Summary of inputs

- Analytical frame: [source file; X top-level branches, Y sub-branches]
- Scoping context: [source file]
- Hypothesis slide: [found and used / not found — placeholders generated]
- Constraints noted: [or "none noted"]
- Gaps or open items: [anything unresolved; "none" if none]

---

## Branch prioritization

| Branch | Classification | Rationale | Working hypothesis |
|--------|---------------|-----------|-------------------|
| [Branch 1] | Essential | [reason] | [hypothesis] |
| [Branch 2] | Secondary | [reason] | [hypothesis — PLACEHOLDER if not confirmed] |
| [Branch 3] | Out of scope | [reason] | — |

---

## Value chain map

[Description of the relevant value chain and market segments]

**Coverage check:** [any major players or segments missing from the target list, or "none identified"]

---

## Interviewee type map

| Interviewee type | Value chain position | Branches covered | Target interviews | Target outreach | Planning factor |
|-----------------|---------------------|-----------------|------------------|-----------------|-----------------|
| [Type 1] | [position] | [Branches A, B] | [N] | [N × factor] | [factor]× |
| [Type 2] | [position] | [Branch C] | [N] | [N × factor] | [factor]× |

**Notes on mix:** [breadth guidance]
**Sequencing:** [which types to approach first; expert network flags]
**Lead time flags:** [any types requiring extended lead time]

---

## Forum recommendation

| Interviewee type | Recommended forum | Rationale |
|-----------------|------------------|-----------|
| [Type 1] | Phone | [reason] |
| [Type 2] | In-person | [reason] |

---

## Approach recommendation

**Recommended approach:** [Direct reading / Targeted extraction / Evaluate at kickoff]
**Basis:** Projected corpus of ~[N] transcripts; [rationale]

---

## Standardization flags

| Branch | Standardization candidate? | Proposed question stem |
|--------|--------------------------|----------------------|
| [Branch A] | Yes | "[question stem]" |
| [Branch B] | No | — |

---

## Money slide

[Consultant's description of the key output visual, in their words]

— or —

**TBD** — team should align on this before Interview Guide Design begins.

---

## Next step

This Research Plan feeds two parallel tracks:
- **Interview Acquisition** — use the interviewee type map and outreach targets to begin contact identification; start grounding interviews on Day 1
- **Interview Guide Design** — use branch priorities, working hypotheses, standardization flags, and money slide to build the guide

**Mid-fieldwork review:** After the first 5–8 interviews, revisit this plan. Have branch priorities shifted? Have new themes emerged? Update before continuing fieldwork.

When fieldwork is complete, return to **Interview Coding & Synthesis** and reference target N as the coverage baseline for Mode 2's coverage table.
```

**Producing the docx:** Use the same approach as ICS (`style_docx.py` or equivalent). Apply standard Newry document formatting. Save as `Research Plan v1.docx` in `Primary Research/outputs/`.

---

## Design principles (inherited from PRT)

- **Chunked and interactive** — present the plan in four chunks; pause for feedback after each; incorporate changes before moving forward. Within each chunk, act and report — do not prompt for one input at a time.
- **Read from the project folder first** — use `project.md` and `context/` as the primary source; ask if files are missing or scope is unclear; accept pasted input only as a fallback.
- **Flag gaps inline** — where inputs are thin, hypotheses are missing, or decisions can't be made from available context, flag it in the output. The research lead decides how to resolve.
- **Always write both files** — markdown and docx, regardless of how much or how little feedback was given during the review.
- **Issue tree as the organizing scaffold** — the analytical frame is always a project input; never impose an assumed structure.

---

## Relationship to other sub-skills

| Sub-skill | What it receives from Research Plan Design |
|-----------|------------------------------------------|
| Interview Acquisition | Interviewee types, target N, outreach count, planning factor, sequencing notes, lead time flags |
| Interview Guide Design | Branch priorities, working hypotheses, standardization flags, money slide, interviewee types |
| Interview Coding & Synthesis | Approach recommendation (direct reading vs. targeted extraction); target N per type (coverage baseline for Mode 2) |

See `SKILL.md` at the plugin root for the full workflow sequence.
