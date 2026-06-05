---
name: plugin-auditor
description: Use this skill whenever a Newry plugin or skill needs to be reviewed for quality — before shipping, after a major change, or when something feels off. Triggers on "audit this plugin," "review this skill," "check this SKILL.md," "is this well-designed," "look at the token efficiency," "review the implementation," or any request to evaluate whether a Newry plugin is ready. Audience is program maintainers, not consultants.
---

# Plugin Auditor — SKILL.md

A skill for reviewing Newry AI plugins and sub-skills. Runs three structured passes — design, implementation, and token efficiency — and produces a report covering what's working, gaps, and recommendations.

**Audience:** program maintainers (Sylvan, Matt, successors). Not consultant-facing.

**Designed for:** any plugin or standalone skill. Calibrated against PRT.

---

## What you need

- **The plugin's SKILL.md files** — coordinator + all sub-skills. Read every file before starting any pass.
- **`strategy/principles.md`** — Newry AI Program principles. Required for Pass 1.
- **Any supporting files referenced in the skill** (decisions.md, overview.md, references/) — read if relevant to a finding.

Ask before starting: "Which plugin or skill should I audit? Provide the path or name."

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
  - `fldNHK285dPCOdNhB` (plugin) — `"plugin_auditor"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — `"plugin_auditor"`
  - `fldmTXyfFZRpbZEvQ` (user_id) — use the user's email address from the session context (available in the system prompt `<user>` block); if not available, use `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — `""`

If the write succeeds, continue. If it fails, retry once.

**Step 3 — Local fallback (if Airtable write still failed after retry).**
Silently append one JSON line to `~/.newry/logs/usage-log-<user_id>.jsonl` (create `~/.newry/logs/` if missing):
`{"ts":"<ISO>","plugin":"plugin_auditor","sub_skill":"plugin_auditor","user_id":"<user_id>","project":""}`
No user-facing output. Then continue.

---

## How this skill works

Three sequential passes. Complete each pass fully before starting the next. Do not merge passes or run them in parallel — each pass has a different lens and mixing them muddies both.

After all three passes, produce the report. End with a single question.

---

## Pass 1 — Design

**Question:** Is this the right skill, designed the right way?

Check each criterion. Note findings as you go — do not write the report yet.

**Job-to-be-done (Principle 4)**
- Is the consultant's task named clearly in the skill?
- Is the design built from that task, or from what the technology makes easy?
- Would a consultant recognize their job in the skill's description?

**Lane discipline (Principle 2)**
- Does the skill stay out of judgment calls that belong to the consultant?
- Scan output instructions for language that draws conclusions, makes recommendations, or resolves strategic questions
- Specific signals: "the best option is," "you should," resolving contradictions rather than surfacing them, assessing commercial attractiveness or strategic fit

**Scope (Principle 8)**
- Is the skill's job cleanly bounded — not too broad, not too narrow?
- Could it be evaluated independently, or does it only make sense as part of something larger?
- Is there anything in scope that belongs in a different skill?

**Fit in workflow**
- Does the skill sit in the right position in the workflow?
- Are inputs clearly received from the right upstream skill?
- Does it hand off cleanly to the right downstream skill?
- Are there gaps or overlaps with adjacent skills?

**Over-specification (Principle 5)**
- Are there instructions that encode what the model already knows without Newry-specific calibration?
- Would removing a rule change the output in a meaningful way, or would the model get there anyway?

**Portability (Principle 12)**
- Any instructions that couple the skill to a specific AI platform?
- Would the skill run on a different platform without modification?

---

## Pass 2 — Implementation

**Question:** Will this skill work reliably in practice?

**Completeness**
- Does the skill cover every step of the workflow it claims to own?
- Walk the full workflow: could a consultant get from entry to output without hitting an undescribed step?
- Any inputs assumed but not specified?

**Consistency**
- Does terminology hold across the full skill and across all sub-skills?
- Do format conventions, output structures, and naming conventions align?
- Are there conflicting instructions between sections or files?

**Executability**
- Are instructions specific enough for the model to follow without guessing?
- Flag any step described at a level of abstraction that requires interpretation
- Are conditionals (if/when) clearly defined?

**Edge cases**
- Are common failure modes handled? Missing inputs, partial data, ambiguous situations?
- What happens if the consultant enters mid-workflow — is that covered?
- What happens if required files don't exist?

**Calibration examples**
- Where the skill needs the model to hit a specific standard, are there concrete examples?
- Are examples representative of the actual range of inputs — or only the easy cases?

**Output spec**
- Is the output format fully defined?
- Would two runs on the same input produce structurally consistent output?
- Are file names, locations, and versioning conventions specified?

**P-series check: Usage logging (P-LOG)**
- Does the plugin implement the standard 3-step logging block at the start of every run?
- **Step 1:** Does it ping Airtable (`list_records_for_table`, pageSize: 1) and block with a user-facing message if the connector is not connected?
- **Step 2:** Does it write to Airtable (`create_records_for_table`) with the correct schema: `{ts, plugin, sub_skill, user_id, project}`? Does it retry once on failure?
- **Step 3:** Does it fall back silently to `~/.newry/logs/usage-log-<user_id>.jsonl` if the Airtable write fails after retry? Does it create the directory if missing?
- Is `user_id` sourced from the session context email (system prompt `<user>` block); otherwise `"unknown"`?
- Are Steps 2 and 3 silent — no user-facing output?

---

## Pass 3 — Token efficiency

**Question:** Is every word earning its place?

Flag candidates for tightening. For each finding, propose a specific rewrite — don't just identify bloat.

**Rule:** tightening cannot come at the cost of executability. A vague short instruction is worse than a precise long one. When in doubt, keep the precision.

**Redundancy**
- Is anything said more than once within the skill?
- Is anything repeated across sub-skills that could live once in the coordinator and be referenced?

**Over-explanation**
- Any instructions that explain the *why* at length when a short rule captures the same thing?
- Any defensive hedging that adds words without adding meaning?

**Dead weight**
- Headers, sections, or principles present but not doing real work?
- Any scaffolding left over from earlier design iterations?

**Verbosity**
- Instructions that could be tightened without losing precision?
- Passive constructions, filler phrases, or unnecessarily long examples?

---

## Report

After all three passes, write the report. Structure:

```
## Audit — [Plugin name]
**Date:** [YYYY-MM-DD]
**Files reviewed:** [list]

### What's working well
[Bullets. Specific. Credit where it's due — don't skip this section.]

### Gaps and issues
[Grouped by pass (Design / Implementation / Token efficiency).
Each issue: what it is, where it appears, why it matters.]

### Recommendations
[Prioritized. Highest-impact changes first.
Each recommendation: specific, actionable, references the relevant file and section.]
```

End with a single question — do not embed it in the report body:

> Should I walk through the suggested changes one by one?

If yes, present changes one at a time, explain each in plain language, and wait for a reaction before moving to the next.

---

## Design principles

- **Three passes, not one** — each pass has a different lens; mixing them produces muddier findings in all three.
- **Read everything first** — do not start Pass 1 until all SKILL.md files are loaded. Findings often depend on cross-file context.
- **Specific findings only** — vague observations ("this section could be clearer") are not useful. Name the file, section, and specific issue.
- **Tighten without breaking** — token efficiency is not an excuse for vagueness. Every proposed rewrite must preserve the original instruction's precision.
- **Credit where it's due** — the "what's working well" section is not a formality. Noting what works well calibrates what the program should protect when making changes.


---

## Feedback capture

Apply the shared feedback-capture sub-skill: `plugins/feedback-capture/SKILL.md`.

Set `Plugin: plugin-auditor` and `Sub-skill: plugin-auditor` in the log entry.
