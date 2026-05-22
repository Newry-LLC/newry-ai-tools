---
name: newry-knowledge
description: >
  Handles two distinct question types at Newry. (1) Knowledge lookup — any question
  requiring access to Newry-specific internal data: project history, client contacts,
  staff expertise, institutional learnings, documents, policies, templates, or anything
  stored in SharePoint or Airtable. Do not use for general methodology or publicly
  available information. (2) AI tools directory — any question about what AI tools,
  Claude capabilities, or plugins exist at Newry, regardless of how it is phrased:
  "what tools do we have", "what can Claude help with here", "what AI features does
  Newry have", "which tool should I use for X", "show me available plugins", "what has
  the AI program built", "does Newry have a tool for X". Single entry point for both —
  routes internally to the right sub-skill.
---

# Newry Knowledge — Coordinator

Routes questions across Newry's knowledge sources and tools.

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

## Step 0 — Pre-gate: AI tools directory?

Intent check: is the user asking what AI tools, Claude capabilities, or plugins are
available at Newry — or which tool to use for a task?

If yes → **invoke the `tool-directory` sub-skill and stop.** Do not search SharePoint or Airtable.

The phrasing does not matter. "What claude tools does Newry have?", "what can the AI
program help me with?", "is there a tool for primary research?" — all route here if the
underlying question is about what the AI program offers.

---

## Sources at a glance

| Source | Best for |
|--------|----------|
| **Airtable** | Structured facts — contact details, project metadata, AER learnings, staff expertise |
| **SharePoint** | Document content — deliverables, research, policies, templates, prior work evidence |

---

## Step 1 — Gate: is this a Newry knowledge question?

Search only if the question requires access to Newry's files or data.

**Search** when the question is about:
- Specific Newry projects, engagements, or prior work
- Client or staff contacts
- Internal documents — deliverables, research, policies, templates, training materials
- What Newry found, presented, or recommended on a topic
- Firm learnings (AER) or staff expertise

**Do not search** when the question could be answered without any Newry documents:
- General methodology ("how do you build a market sizing model?")
- Public company information ("what is [client]'s business strategy?")
- Market or industry data not tied to a specific Newry engagement

The fact that a client name or industry term appears in the question does not make it Newry-specific. If in doubt, answer from general knowledge rather than searching.

---

## Step 2 — Source: what kind of data answers it?

**Airtable** — structured facts:
- Contact details for a specific person or company
- Project metadata (code, dates, scope, practice area, budget)
- AER learnings across a project type
- Staff expertise (who has worked on X)

**SharePoint** — document content:
- Prior work in a domain or industry (use prior-work sweep mode)
- What a specific document says
- Research, deliverables, presentations, templates, policies
- Newry's methodology or training materials — only when the question explicitly asks what Newry's approach or training says, not for generic methodology questions

**Both — run in parallel** when the question explicitly asks for structured metadata AND document content (e.g., "what projects has Newry done in X and what did the deliverables look like?")

---

## Step 2.5 — Handle source failure

If a source fails or its connector is unavailable, note the degradation inline — e.g., "Airtable isn't connected — showing SharePoint results only" — and continue with whatever is reachable. Do not stop cold.

---

## Step 3 — Synthesize

Weave results into a single direct answer.

- Lead with the answer, not the source
- Cite sources inline (document title + URL for SharePoint; table/record for Airtable)
- If one source added nothing, omit it
- If both sources contributed, a brief note ("drawing on project records and the [document name]") is appropriate

---

## Feedback capture

Apply the shared feedback-capture sub-skill: `plugins/feedback-capture/SKILL.md`.

Set `Plugin: newry-knowledge` and `Sub-skill: [whichever sub-skill was active]` in the log entry.
