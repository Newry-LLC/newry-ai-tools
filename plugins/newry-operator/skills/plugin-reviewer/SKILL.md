---
name: plugin-reviewer
description: >
  Quality review for any Newry plugin or skill before shipping. Runs the Plugin Auditor's
  three passes (design, implementation, token efficiency) and produces a structured report.
  Use before packaging any new or changed skill.
---

# Plugin Reviewer

One-command quality review for any Newry plugin or skill. Wraps the Plugin Auditor.

---

## What you need

- **The plugin or skill to review** — path or name. If not provided, ask before proceeding.
- **Plugin Auditor** — load `plugins/plugin-auditor/SKILL.md` from the Cowork working folder.
  Follow its three passes exactly as defined there. If the file isn't found, ask the operator
  for the correct path before proceeding.
- **Principles** — use `references/principles.md` (bundled here) for Pass 1 in place of
  `strategy/principles.md`. They are the same content.

---

## How to run

1. Confirm which plugin or skill to review, and whether to audit the full plugin or only
   what changed. State the scope at the top of the report.
2. Read all relevant SKILL.md files for that plugin.
3. Run the three passes defined in `plugins/plugin-auditor/SKILL.md` in order.
4. Produce the structured report.
5. Ask: "Should I walk through the suggested changes one by one?"

---

## Scope note

Default to **scoped audit** (changed files only) unless the operator asks for a full audit.
A scoped audit is faster, reduces noise, and is sufficient for most shipping decisions.
State the scope explicitly at the top of the report.
