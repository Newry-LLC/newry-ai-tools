---
name: newry-knowledge
description: >
  Handles three distinct request types at Newry. (1) Knowledge lookup — any question
  requiring access to Newry-specific internal data: project history, client contacts,
  staff expertise, institutional learnings, documents, policies, templates, or anything
  stored in SharePoint or Airtable. Do not use for general methodology or publicly
  available information. (2) AI tools directory — any question about what AI tools,
  Claude capabilities, or plugins exist at Newry, regardless of how it is phrased:
  "what tools do we have", "what can Claude help with here", "what AI features does
  Newry have", "which tool should I use for X", "show me available plugins", "what has
  the AI program built", "does Newry have a tool for X". (3) Add context — adding
  relationship intelligence about a person: "add context about [person]", "I just met
  with / talked to / called [person]", "note that [person] said / prefers / is doing X",
  "add a relationship note", "log that [person] X", "remember that [contact] X".
  Single entry point for all three — routes internally to the right sub-skill.
---

# Newry Knowledge — Coordinator

Routes questions across Newry's knowledge sources and tools.

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
  - `fldNHK285dPCOdNhB` (plugin) — `"newry_knowledge"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — whichever sub-skill is being invoked; use `"general"` if routing hasn't resolved yet
  - `fldmTXyfFZRpbZEvQ` (user_id) — use the user's email address from the session context (available in the system prompt `<user>` block); if not available, use `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — project code if discernible; otherwise `""`

If the write succeeds, continue. If it fails, retry once.

**Step 3 — Local fallback (if Airtable write still failed after retry).**
Silently append one JSON line to `~/.newry/logs/usage-log-<user_id>.jsonl` (create `~/.newry/logs/` if missing):
`{"ts":"<ISO>","plugin":"newry_knowledge","sub_skill":"<sub_skill>","user_id":"<user_id>","project":"<project>"}`
No user-facing output. Then continue.

---

## Step 0 — Pre-gate: AI tools directory?

Intent check: is the user asking what AI tools, Claude capabilities, or plugins are
available at Newry — or which tool to use for a task?

If yes → **invoke the `tool-directory` sub-skill and stop.** Do not search SharePoint or Airtable.

The phrasing does not matter. "What claude tools does Newry have?", "what can the AI
program help me with?", "is there a tool for primary research?" — all route here if the
underlying question is about what the AI program offers.

---

## Step 0.5 — Pre-gate: add context / relationship note?

Intent check: is the user trying to log context about a person, record an interaction,
or write a relationship note?

If yes → **invoke the `add-context` sub-skill and stop.** Do not search anything.

Trigger signals: "add context about", "add a relationship note", "I just met with",
"I just talked to / called / spoke with", "note that [person]", "log that [person]",
"remember that [contact]", "[person] mentioned / told me / said".

---

## Step 0.6 — Pre-gate: review pending context?

Intent check: is the user asking to review, approve, or clear pending context library facts?

If yes → **invoke the `review-context` sub-skill and stop.**

Trigger signals: "review pending", "what's pending in my library", "pending context",
"review context facts", "approve pending facts", "clear my review queue",
"what's in my review queue", "pending review".

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
