---
name: issue-tree
description: Generate an initial MECE issue tree for a new Newry project. Takes the problem statement and project type as input and produces a Cowork artifact with a collapsible issue tree and editable hypothesis boxes per issue. The most analytically rigorous sub-skill in the PLT.
---

# Issue Tree Sub-Skill

Generate an initial issue tree — structured and MECE — that the team can use as the backbone of the engagement. This is a starting point for EM review and team iteration, not a final artifact.

## Inputs

**Required:**
- Problem statement (from the Problem Statement sub-skill or provided directly)
- Project type (see list below)

**Optional:**
- SoW / proposal (for additional context on what the client expects to be answered)
- Value hypothesis (from value-creation sub-skill) — key assumptions from the value estimate are natural inputs to the tree; see Step 0 below

## Project Types and Default Frameworks

The issue tree structure depends heavily on project type. The skill selects a starting framework based on project type:

| Project Type | Default Framework | Notes |
|---|---|---|
| Growth Strategy | Open-form (Where to play / How to win) | Build deductively from the problem statement |
| Growth Engine | Growth Levers | Expanding existing sales, core markets, aftermarket, cross-sell, adjacencies, new applications, M&A |
| Innovation / Tech Push | RWW (Real-Win-Worth) | Is it real? Can we win? Is it worth it? — adapt branch structure to the technology |
| Market Pull | Open-form (needs/segments/value chain) | Build around unmet needs and customer segments |
| M&A / Licensing | Deal thesis decomposition | Strategic fit, deal quality, value creation levers |
| Competitive Analysis | Competitive position decomposition | Market share drivers, cost position, value prop, go-to-market |
| Strategy Facilitation | Open-form | Build from the client's strategic decision |

If the project type is ambiguous, ask one clarifying question before proceeding.

**Read the method first.** Before drafting, read `references/project initiation resources/Problem Structuring Training - Issue Trees (2015).md` (issue-tree fundamentals + MECE) and `references/project initiation resources/2025 CLST Forum 2 - Thought Leadership and Problem Solving.md` (the issue→hypothesis→analysis chain + RWW). Build to Newry's method.

## What This Skill Does

0. **Sanity-check against the value hypothesis (if it exists).** If key assumptions were flagged in the value hypothesis — SOM, capture probability, months accelerated, decision size, price lift — check whether they're covered by branches in the tree. If not, consider whether they should be. This is a check, not a structural input; the problem statement drives the tree.

1. **Root question** — restate the core problem from the problem statement as the root question. Every branch is a MECE decomposition of what must be resolved to answer it.
2. **Propose a framework** by reading the problem statement — don't classify project type first. Let the content of the problem signal the right structure. State the proposed framework and rationale in one line; invite the EM to redirect if wrong. Consult the framework table above if the structure isn't obvious.
3. **Draft Level 1 issues** (typically 3–5 branches; each a MECE, yes/no question).
4. **Expand Level 2 sub-issues** under each branch.
5. **Add Level 3** where the problem statement gives enough specificity to go deeper. Do not force uniformity — real issue trees are asymmetric.
6. **Flag structural choices** — what alternative framings were considered, and why this structure was chosen.

Two steps. First deliver the issue tree as an editable artifact plus a table in chat. After the EM reviews and approves the structure, update the artifact to add hypothesis boxes.

## Step 1 — Issue tree artifact + chat table

**Artifact** (Cowork sidebar):

- Read-only header: project name and root question
- **Embed the problem statement** as a JS constant at the top of the artifact script: `const PROBLEM_STATEMENT = "<full problem statement text>";` — this is used by the Suggest Hypotheses button in Step 2 and does not need to be visible in the UI.
- Issues rendered as a **nested draggable list** — Level 1 branches and Level 2 sub-issues can be dragged to reorder or moved to a different Level 1 parent to restructure the tree. Implement using the HTML5 Drag and Drop API.
- Each issue is an **editable input field** — consultant can revise wording directly
- At the bottom:
  - **"Add hypotheses"** button — calls `sendPrompt("Add hypotheses to the issue tree")`
  - **"Download as CSV"** button — generates a CSV (Level, Issue text) and triggers a browser download; opens in Excel

Keep the artifact visually simple: white background, plain typography, clear indentation for Level 2.

**Chat output** (immediately after delivering the artifact):

Post the full issue tree as a markdown table:

| Level | Issue |
|---|---|
| 1.1 | [Level 1 issue text] |
| 1.1.1 | [Level 2 sub-issue] |
| 1.1.2 | [Level 2 sub-issue] |
| 1.2 | [Level 1 issue text] |
| ... | ... |

Then one brief paragraph: framework selected and why, structural choices made, prompt to review and edit in the sidebar or redirect in chat.

## Step 2 — Hypotheses added

When the consultant clicks "Add hypotheses" (or says equivalent in chat), update the artifact to add below each issue:

- An editable textarea for the hypothesis, placeholder: *"What do we think the answer is, and why?"*

Also add at the top of the artifact:
- A **"Suggest Hypotheses"** button:
  - Calls `window.cowork.askClaude()` with all current issue text and `PROBLEM_STATEMENT` (the JS constant embedded in Step 1)
  - Populates empty hypothesis boxes with directional suggestions (likely resolution + one-line rationale per issue)
  - Does not overwrite boxes that already have content

And at the bottom:
- A **"Copy All"** button: copies each issue + hypothesis as clean formatted text, ready to paste into PowerPoint or a doc
- **"Download as CSV"** button remains — now includes hypothesis column

## Design Notes

- **MECE is non-negotiable at Level 1.** Every top-level branch must be mutually exclusive and collectively exhaustive. Verify before outputting and flag any violations.
- **The root question must come from the problem statement.** Don't paraphrase loosely — the root question should feel like a direct restatement of the core problem, sharp enough that answering it would resolve the engagement.
- **Asymmetry is correct.** Some branches go 3 levels deep, others stay at 2. Forcing uniformity produces bad issue trees.
- **Surface structural choices.** The team should know what alternative framings were considered. This is how the skill teaches as it produces.
- **"Iterate" is part of the output.** The issue tree is never final. Instruct the team to revisit after the first week of data gathering and before every major client update.
- **This is the most analytically intensive sub-skill.** Quality here directly determines the quality of the workplan, analyses, and client output.
- **Hands off to workplan.** This skill stops at issues + hypotheses. Turning the approved issues into a sequenced activity list is the workplan sub-skill's job — don't generate activities here.

## References

- `references/project initiation resources/2025 CLST Forum 2 - Thought Leadership and Problem Solving.md` — issue tree examples (Stellex/Crest, Teckrez, AFR), RWW framework
- `references/project initiation resources/EM Training Module 0 - Thought Leadership and Problem Structuring (2019).md` — MECE tips, prioritization criteria
- `references/project initiation resources/Problem Structuring Training - Issue Trees (2015).md` — issue tree fundamentals, MECE exercises
- `references/project initiation resources/2025 Consulting Process and Thought Leadership Onboarding.md` — issue tree → workplan chain
- Project Initiation Template — the issue tree page and the issue-tree-to-activities bridge page
- `references/project initiation resources/2025 CLST Workplanning (Module 1 and 2).md` — issue tree → workplan transition
