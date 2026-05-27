# Primary Research Toolkit — Plugin Overview

**Tier:** Tier 1 / Module 1 (Foundational Workstream — Primary Research)
**Status:** Research Plan Design built (2026-05-06); Interview Coding & Synthesis built and tested; remaining sub-skills planned or stub

---

## What this plugin does

Accelerates the most time-intensive, consistency-risky, and cognitively demanding steps in Newry's primary research workflow. The core problem: large interview corpora (often 50–200+ transcripts across multiple streams) need to be mapped to a structured analytical frame (issue tree, research questions, hypothesis set) and distilled into evidence that feeds deliverable production — at consulting speed, without losing fidelity to what was actually said.

---

## Sub-skills

### 1. Research Plan Design *(built — 2026-05-06)*
Pre-fieldwork planning: prioritizes branches of the analytical frame, identifies interviewee types and target sample sizes, forum and approach (targeted extraction vs. direct reading) recommendation, standardization flags for cross-interview comparison, and money slide prompt for working backwards from the key deliverable visual.

### 2a. Interview Acquisition *(stub — not yet built)*
Runs in parallel with Interview Guide Design. Target list generation, outreach drafting, and pipeline tracking aligned to Research Plan requirements. Build when acquisition bottlenecks surface in practice.

### 2b. Interview Guide Design *(planned)*
Runs in parallel with Interview Acquisition. Converts a project's analytical frame into a structured interview guide by interviewee type. Produces branch-aligned question sets with probing follow-ups and a coverage matrix.

### 3. Interview Execution *(stub — not yet built)*
Limited AI scope by design — the interview itself is a human activity. Covers pre-interview prep (interviewee brief, branch alignment, flags) and optionally lightweight in-call note capture structured for ICS ingestion. Build when pre-interview prep or post-call note cleanup emerges as a consistent bottleneck.

### 4. Interview Coding & Synthesis *(built)*
Takes one or more interview transcripts and an analytical frame. Produces branch-mapped summary cards (Single mode) and cross-interview synthesis with pattern detection, contradiction flagging, and emergent theme identification (Roll-up mode). Validated on Alta (55 internal interviews, May 2026).

### ~~5. Coverage & Gap Analysis~~ *(absorbed into ICS Mode 2 — 2026-05-04)*
Originally planned as a separate post-coding pass. ICS Mode 2 Roll-up already produces the coverage table, per-branch gaps, contradictions, and overall coverage rating. Cross-round delta, source-type recommendations, and cross-branch coverage commentary are tracked as ICS Mode 2 enhancements rather than a separate sub-skill. See the CGA folder's SKILL.md for the absorption record.

**Workflow sequence:** Research Plan Design → (Interview Acquisition ∥ Interview Guide Design) → Interview Execution → Coding & Synthesis (cards + Roll-up with coverage and gaps) → SoF Draft mode

**Handoff out:** the Roll-up output feeds either SoF Draft mode or the future Secondary Research Toolkit (Tier 1 / Module 2), where secondary sources are coded against the same analytical frame and triangulated with primary findings. Secondary research integration is out of scope for this plugin by definition.

---

## Design principles

- **Evidence-organizing, not insight-generating** — the toolkit structures and attributes what was said; consultants draw conclusions.
- **Issue tree as the organizing scaffold** — the analytical frame is always a project input, never baked in. The toolkit generalizes across projects.
- **Stream-aware** — synthesis correctly handles and distinguishes different interviewee types (internal staff, customers, experts, competitive sources); findings are never flattened across incompatible sources.
- **Trust-first output** — every claim traces to a named source and verbatim or near-verbatim quote. Paraphrased aggregates are labeled as such.

---

## How feedback works

User-reported issues, friction, and improvement suggestions are captured automatically. When a user describes a problem in conversation — explicit (`feedback:`, `issue:`, `bug:`) or implicit ("this is wrong," "what I actually wanted," "this is missing X") — the skill recognizes the intent and appends an entry to `logs/feedback-log.md` with run context, classification, and severity. The user gets a brief acknowledgment; the skill continues with whatever else they asked for. No prompt at start or end of run.

The log is the input to maintenance: bugs become script fixes, friction becomes SKILL.md sharpening, quality issues become eval cases (when the eval runner ships), feature requests go to the design backlog. Triage is intentionally separate from capture so capture stays frictionless.

---

## Files in this plugin

| File / Folder | Purpose |
|---------------|---------|
| `SKILL.md` | Coordinator — workflow overview, sub-skill routing, shared inputs |
| `overview.md` | This file — plugin purpose, principles, status |
| `decisions.md` | Design decisions and rationale |
| `design-notes.md` | Working notes from design phase |
| `sub-skills/` | One folder per sub-skill, each with its own `SKILL.md` |
| `references/interviewee-segmentation.md` | Segmentation framework for interview types |
| `logs/synthesis-log.md` | Run log for Interview Coding & Synthesis |
| `logs/feedback-log.md` | User-reported feedback, issues, and improvement suggestions |
