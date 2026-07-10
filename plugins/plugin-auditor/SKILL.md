---
name: plugin-auditor
description: Use this skill whenever a Newry plugin or skill needs to be reviewed for quality — before shipping, after a major change, or when something feels off. Triggers on "audit this plugin," "review this skill," "check this SKILL.md," "is this well-designed," "look at the token efficiency," "review the implementation," or any request to evaluate whether a Newry plugin is ready. Audience is program maintainers, not consultants.
---

# Plugin Auditor — SKILL.md

A skill for reviewing Newry AI plugins and sub-skills. Runs three structured passes — design, implementation, and token efficiency — and produces a report covering what's working, gaps, and recommendations.

**Audience:** program maintainers (Sylvan, Matt, successors). Not consultant-facing.

**Designed for:** any plugin or standalone skill. Calibrated against PRT.

**Authority:** the checks below derive from `strategy/skill-authoring-standard.md` (Part 4, 19-row checklist). This skill *runs* that checklist and applies three-lens judgment on top — it does not restate the rules. Cite the standard's row/section numbers; do not re-explain them. When the standard changes, this skill inherits the change.

---

## What you need

- **The plugin's SKILL.md files** — coordinator + all sub-skills. Read every file before starting any pass.
- **`strategy/skill-authoring-standard.md`** — the checklist and rule tags (`[M]`/`[J]`). Required for all three passes.
- **`strategy/principles.md`** — the 15 principles the standard cites. Required for Pass 1 judgment.
- **The plugin's `evals/` and `plugin.json`** — needed for eval and versioning checks.
- **`plugins/newry-knowledge/evals/skill-building-log.md`** — the cross-skill failure log (row 18).
- **Any supporting files referenced in the skill** (decisions.md, overview.md, references/) — read if relevant to a finding.

Ask before starting: "Which plugin or skill should I audit? Provide the path or name."

---

## Usage logging

At the start of every run — before any other work:

**Step 1 — Check Airtable connectivity.**
Call `list_records_for_table` (Base ID: `appRawPuacfAvVH2Z`, Table ID: `tblmACtwIClniGn5n`, pageSize: 1). If this call fails, Airtable isn't connected — skip Step 2 and log locally via Step 3, then continue. Usage logging is best-effort: never block the run and never show a connection warning.

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

Each pass runs a named subset of the standard's Part 4 checklist, then adds the pass's own judgment lens. For every checklist row:

- **Blocker (mechanical, `[M]`)** — deterministic pass/fail. A fail is a **blocker**: report it under "Blockers" and state it must be fixed before shipping.
- **Review (judgment, `[J]`)** — heuristic. Assess with reasoning and report under "Review flags," not as pass/fail.

Row numbers below refer to `strategy/skill-authoring-standard.md` Part 4. Read the row's "How to verify" column there — don't reproduce it here.

After all three passes, produce the report. End with a single question.

---

## Pass 1 — Design

**Question:** Is this the right skill, designed the right way?

**Checklist rows to run (standard Part 4):**
- **Row 1** — `description` ≤1024, third person, no XML. *(Blocker)*
- **Row 2** — `name` ≤64, lowercase/digits/hyphens, no reserved words. *(Blocker)*
- **Row 3** — `description` says what + when, front-loads use, lists real trigger phrases, reads pushy. *(Review — compare to §1 ✓/✗.)*
- **Row 14** — built from a named observed consultant task + the consultant it serves (Principle 4). *(Review)*
- **Row 7** — degrees of freedom match fragility: judgment loose, fragile steps pinned (§3). *(Review)*
- **Row 11** — coordinator/sub-skill composition: trigger phrases distinct and non-overlapping. *(Review)*
- **Row 17** — lane discipline (Principle 2): the tool states no recommendation and no client action; it proposes and structures only. Scan the output spec for verdict language ("the best option is," "you should," resolving contradictions rather than surfacing them). *(Review)*

**Design judgment lens (beyond the rows):**
- **Job recognition** — would a consultant recognize their own job in the description?
- **Scope (Principle 8)** — cleanly bounded, independently evaluable; nothing in scope that belongs in another skill.
- **Fit in workflow** — right position; inputs received from the right upstream skill; clean handoff downstream; no gaps or overlaps with adjacent skills.
- **Over-specification (Principle 5)** — flag rules that encode what the model already knows without Newry-specific calibration. Would removing the rule change the output, or would the model get there anyway?

---

## Pass 2 — Implementation

**Question:** Will this skill work reliably in practice?

**Checklist rows to run (standard Part 4):**
- **Row 9** — imperative voice; one term per concept; forward slashes in paths; no time-sensitive phrasing. *(Blocker)*
- **Row 8** — repeatable/fragile logic lives in a bundled script, invoked "Run X", with dependencies + install listed — not re-implemented in prose. *(Review)*
- **Row 10** — ≥3 eval scenarios + a scoring path, and **this change ships a new or updated eval case** (§6). *(Blocker)*
- **Row 12** — every MCP tool referenced as `ServerName:tool_name`; a bare name is a portability bug. *(Blocker)*
- **Row 13** — no Claude Code-only frontmatter in a Cowork plugin; on a Code skill, every Claude-specific use is flagged so a future non-Claude port is bounded (Principle 12, standard Part 2). *(Blocker)*
- **Row 15** — numbered version (in `plugin.json`, not SKILL.md frontmatter) and usage logging present. *(Blocker — see P-LOG below for the detailed logging audit.)*
- **Row 16** — the judgment step is transparent, proposal-framed, overridable, and contestable; the confirm-gate scales to stakes (§3B). *(Review — compare to §3B ✓/✗.)*
- **Row 19** — self-verification before output: a deterministic check runs first (outputs exist, counts non-zero, every Type-4 claim has Type-1/2 evidence); a judge pass only where quality can't be checked deterministically (§3C). *(Review)*
- **Row 18** — recurring failures are captured in `plugins/newry-knowledge/evals/skill-building-log.md` and the fix is promoted into the skill at the point of failure — logged in the log, fixed in the skill, not duplicated (§3C). *(Review)*

**Implementation judgment lens (beyond the rows):**
- **Completeness** — walk the full workflow entry-to-output; flag any undescribed step or unspecified assumed input.
- **Consistency** — terminology, format conventions, and output structures hold across all files; no conflicting instructions between sections.
- **Executability** — instructions specific enough to follow without guessing; conditionals (if/when) clearly defined.
- **Edge cases (Principle 13/14)** — missing inputs, partial data, mid-workflow entry, missing files handled; shared dependencies degrade gracefully rather than blocking.
- **Calibration examples** — concrete input→output examples where output quality depends on style/format, representative of the real input range, not just easy cases.

**P-LOG — usage-logging block audit:**
Verify the plugin implements the standard 3-step block at the start of every run:
- **Step 1:** pings Airtable (`list_records_for_table`, pageSize: 1) and, on failure, **skips to local logging and continues** — best-effort, never blocks, never shows a connection warning. *(This is the graceful-degradation behavior per Principle 13; flag any version that blocks or warns the user instead.)*
- **Step 2:** writes to Airtable (`create_records_for_table`) with schema `{ts, plugin, sub_skill, user_id, project}`, and retries once on failure.
- **Step 3:** falls back silently to `~/.newry/logs/usage-log-<user_id>.jsonl` if the Airtable write fails after retry, creating the directory if missing.
- `user_id` sourced from the session-context email (system prompt `<user>` block); otherwise `"unknown"`.
- Steps 2 and 3 are silent — no user-facing output.

---

## Pass 3 — Token efficiency

**Question:** Is every word earning its place?

Flag candidates for tightening. For each finding, propose a specific rewrite — don't just identify bloat.

**Rule:** tightening cannot come at the cost of executability. A vague short instruction is worse than a precise long one. When in doubt, keep the precision.

**Checklist rows to run (standard Part 4):**
- **Row 4** — body ≤500 lines / ~2,000 words. *(Blocker)*
- **Row 5** — references one level deep from SKILL.md; any reference >100 lines opens with a TOC. *(Blocker)*
- **Row 6** — the body reads as a table of contents pointing to detail, not the detail itself; references are domain-partitioned so unrelated contexts never co-load (Principle 5). *(Review)*

**Token judgment lens (beyond the rows):**
- **Redundancy** — anything said more than once within the skill, or repeated across sub-skills that could live once in the coordinator and be referenced.
- **Over-explanation** — *why* explained at length where a short rule captures it; defensive hedging that adds words without meaning.
- **Dead weight** — headers, sections, or principles present but not doing real work; scaffolding left over from earlier iterations.
- **Verbosity** — passive constructions, filler phrases, over-long examples.

---

## Report

After all three passes, write the report. Structure:

```
## Audit — [Plugin name]
**Date:** [YYYY-MM-DD]
**Files reviewed:** [list]

### What's working well
[Bullets. Specific. Credit where it's due — don't skip this section.]

### Blockers
[Failed mechanical checks (standard rows tagged Blocker). Each: the row #, what failed,
where it appears, and the fix. These must be resolved before shipping.]

### Review flags
[Judgment checks that need attention, grouped by pass (Design / Implementation / Token
efficiency). Each: the row # or lens, what it is, where it appears, why it matters.]

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
- **Derive from the standard** — checks come from `strategy/skill-authoring-standard.md`, not from freestanding rules here. Cite row/section numbers; the auditor runs the checklist and adds judgment.
- **Blockers vs. review flags** — mechanical (`[M]`) failures are blockers reported as pass/fail; judgment (`[J]`) checks are reasoned assessments. Never demote a blocker to a suggestion or inflate a judgment call into a hard fail.
- **Read everything first** — do not start Pass 1 until all SKILL.md files are loaded. Findings often depend on cross-file context.
- **Specific findings only** — vague observations ("this section could be clearer") are not useful. Name the file, section, and specific issue.
- **Tighten without breaking** — token efficiency is not an excuse for vagueness. Every proposed rewrite must preserve the original instruction's precision.
- **Credit where it's due** — the "what's working well" section is not a formality. Noting what works well calibrates what the program should protect when making changes.


---

## Feedback capture

Apply the shared feedback-capture sub-skill: `plugins/feedback-capture/SKILL.md`.

Set `Plugin: plugin-auditor` and `Sub-skill: plugin-auditor` in the log entry.
