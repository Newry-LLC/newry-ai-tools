---
name: newry-operator
description: >
  For anyone building or stewarding the Newry AI program. Use for design questions
  ("should we build X / how should we structure Y"), logging decisions ("we decided /
  log this"), build prioritization ("what should we work on next"), and plugin quality
  review ("audit / review this skill before shipping"). Not for consultant workflows —
  use newry-knowledge or the relevant consultant plugin for those.
---

# Newry Operator

Coordinator for the Newry AI program operator plugin. Routes design, decision, prioritization,
and quality review requests to the right sub-skill.

**Audience:** Anyone building or stewarding the Newry AI program — current or future contributors.

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
  - `fldNHK285dPCOdNhB` (plugin) — `"newry_operator"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — whichever sub-skill is being invoked; use `"general"` if routing hasn't resolved yet
  - `fldmTXyfFZRpbZEvQ` (user_id) — read `~/.user_id` if it exists; otherwise `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — always `""`

If the write succeeds, continue. If it fails, retry once.

**Step 3 — Local fallback (if Airtable write still failed after retry).**
Silently append one JSON line to `~/.newry/logs/usage-log-<user_id>.jsonl` (create `~/.newry/logs/` if missing):
`{"ts":"<ISO>","plugin":"newry_operator","sub_skill":"<sub_skill>","user_id":"<user_id>","project":""}`
No user-facing output. Then continue.

---

## Feedback capture

Applies across all sub-skills. Read and follow the shared feedback-capture sub-skill:
`../feedback-capture/SKILL.md`

When logging:
- `Plugin:` → `newry-operator`
- `Sub-skill:` → whichever sub-skill is active; use `general` if none

---

## Check 0 — SharePoint log folder sync

Before any other work, silently check whether the log folder is accessible:

```python
import os
exists = os.path.exists(os.path.expanduser(r"~\Newry Corp\Clients - Claude Master Working Folder\logs"))
```

If it does not exist and `~/.newry-sync-warned` does not exist: create `~/.newry-sync-warned`, show the message below once, then continue.
If `~/.newry-sync-warned` exists: skip silently.

> "**One quick setup step:** To enable usage logging, the Claude Master Working Folder needs to be synced from SharePoint to your machine.
>
> 1. Copy this link and paste it into Microsoft Edge: `https://newrycorp.sharepoint.com/clients/SitePages/Home.aspx?RootFolder=%2Fclients%2FShared%20Documents%2FConsulting%20Ops%2FClaude%20Master%20Working%20Folder&FolderCTID=0x0120001E5A3B5DC4435348B27C9444F34FA80E&View=%7B9352A612%2DAF51%2D4D22%2D9834%2DC437D38F2209%7D`
> 2. Click **Sync** — it's in the toolbar just below where it says "Documents," between **Upload** and **Share**
> 3. Once it appears in File Explorer under `Newry Corp`, logging will work automatically
>
> You only need to do this once. Continuing with your request now."

---

## Session start

At the start of any operator session, run `operator-dashboard` automatically before
responding to the operator's first request. This ensures the dashboard artifact is current
and visible in the sidebar without the operator having to ask.

---

## Gate

Before routing, confirm this is a program-building question. If the request is about using
a Newry tool for client work (e.g., how to run PRT, how to search SharePoint), redirect:

> "This plugin is for program builders. For [topic], use [relevant consultant plugin]."

---

## Routing

| Request type | Sub-skill |
|---|---|
| Design or architecture question: "should we...", "how should we structure...", "I'm thinking about building X", "what's the right approach for Y" | `program-advisor` |
| Decision logging: "log this decision", "we decided", "capture this", "record that we..." | `decision-capture` |
| Build prioritization: "what should we work on next", "what's highest priority", "what should we build" | `build-prioritization` |
| Quality review: "audit this", "review this skill", "is this ready to ship", "check this SKILL.md" | `plugin-reviewer` |
| Dashboard / program status: "show the dashboard", "what's been built", "show me program status", "refresh the dashboard" | `operator-dashboard` |
| Orientation / onboarding: "orient me on the program", "how does this work", "I'm new to this", "walk me through the program", "what should I know to get started" | Read `onboarding.md` and walk the builder through it |

If the request spans multiple types (e.g., "advise me and then log the decision"), run
`program-advisor` first, then offer to hand off to `decision-capture`.

---

## Sub-skills

- `skills/program-advisor/SKILL.md`
- `skills/decision-capture/SKILL.md`
- `skills/build-prioritization/SKILL.md`
- `skills/plugin-reviewer/SKILL.md`
- `skills/operator-dashboard/SKILL.md`

## Reference files (bundled)

- `references/principles.md` — 15 design principles
- `references/north-star.md` — durable program horizon
- `references/vision.md` — May 2027 end state
- `references/plugin-index.md` — current plugin registry (name, version, status, audience)

## Decision log (live)

- `~\Newry Corp\Clients - Claude Master Working Folder\logs\newry-operator\decision-log.md`
  — shared across operators via SharePoint sync; read directly at runtime.
  Fall back to bundled `references/decision-log.md` if folder not synced.
