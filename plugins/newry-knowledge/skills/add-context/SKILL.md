---
name: add-context
description: >
  Add relationship intelligence about a person — log an interaction, record a standing
  fact, note a goal, or capture an outcome. Writes to Relationship Notes in Airtable.
  Triggers on: "add context about [person]", "I just met with / talked to / called [person]",
  "note that [person] said / is doing / prefers X", "add a relationship note", "log that
  [person] X", "remember that [contact] X", "[person] mentioned / told me / said".
---

# Add Context — Relationship Intelligence Entry

Captures freeform context about a person and writes it to the Relationship Notes table in Airtable. This is the manual write path into the relationship intelligence layer.

**Base ID:** `appRawPuacfAvVH2Z`
**Relationship Contacts:** `tblomVbLXeELjFIBZ`
**Relationship Notes:** `tbl3JoPYzslECv8h8`

---

## Usage logging

Before any other work, log this run:

**Step 1 — Check connectivity.**
Call `list_records_for_table` (Base: `appRawPuacfAvVH2Z`, Table: `tblmACtwIClniGn5n`, pageSize: 1). If it fails, show:

> "⚠ **Airtable isn't connected.** Go to Cowork Settings → Connectors, connect Airtable, then try again."

Do not proceed until resolved.

**Step 2 — Write usage log.**
`create_records_for_table` (Base: `appRawPuacfAvVH2Z`, Table: `tblmACtwIClniGn5n`):
- `fldRrr3BkrJW8rE3L` (ts) — current UTC time, ISO 8601
- `fldNHK285dPCOdNhB` (plugin) — `"newry_knowledge"`
- `fld4EyuVEhxAhPZEd` (sub_skill) — `"add_context"`
- `fldmTXyfFZRpbZEvQ` (user_id) — session context email; `"unknown"` if unavailable
- `fldu8rvXDfvi2O3jF` (project) — project code if mentioned; otherwise `""`

Retry once on failure; on second failure silently append to `~/.newry/logs/usage-log-<user_id>.jsonl`.

---

## Step 1 — Parse the input

Extract the following from the user's freeform input:

| Field | Required? | How to extract |
|---|---|---|
| **Person name** | Yes | Named explicitly or implied ("just met with Sarah Chen"). If unclear, ask before proceeding. |
| **Note content** | Yes | The substance of what was said / learned / observed. |
| **Note type** | Yes | Classify (see below). |
| **Company** | No | Extract if mentioned ("at Corning", "from W.L. Gore"). |
| **Project** | No | Extract project code if mentioned (e.g., "COR771"). |
| **Date** | No | Default to today (YYYY-MM-DD). Extract if the user specifies a different date. |

**Classify Note type:**
- **Interaction** — a meeting, call, or conversation occurred ("I just met with", "talked to", "called")
- **Standing Context** — a durable, stable fact about this person ("prefers email", "hates long decks", "now VP of X", "her key concern is Y")
- **Goal** — something they want, are targeting, or are working toward
- **Outcome** — a result from a project or engagement ("the engagement led to X", "they decided to proceed")

Default to **Interaction** if the input describes a meeting or contact. Default to **Standing Context** if the input is a stable fact with no specific event attached. If ambiguous, pick the most likely one and state your assumption.

---

## Step 2 — Find the Relationship Contacts record

Search for the person in `tblomVbLXeELjFIBZ`.

1. `search_records` on `tblomVbLXeELjFIBZ` — query: person's full name (or last name if full name not available).
2. Follow with `list_records_for_table` on `tblomVbLXeELjFIBZ` filtered to the returned record IDs to retrieve the `Name` field (`fld615DD5h5OeIytR`).

**Match outcomes:**
- **One clear match** — confirm inline: "Found: [Name]." Proceed to Step 4.
- **Multiple matches** — list them briefly (name only) and ask which one. Wait for response, then proceed to Step 4.
- **No match** — tell the user: "No record found for [name] in Relationship Contacts. I can create a new contact — go ahead?" Wait for confirmation, then proceed to Step 3.

---

## Step 3 (conditional) — Create new Relationship Contacts record

Only if Step 2 found no match and the user confirmed creation.

`create_records_for_table` on `tblomVbLXeELjFIBZ`:
- `fld615DD5h5OeIytR` (Name) — full name
- `fldOMhUaMmLj5vSfW` (First Name) — split from full name
- `fld3qWn1wE5rLtIlO` (Last Name) — split from full name
- `fldT8PIJSC1yrLLke` (Relationship Strength) — `"New"`

Do not populate other fields (Company link, Relationship Type, etc.) unless the user provided that information explicitly.

Capture the new record ID returned by the create call — you'll need it in Step 4.

---

## Step 4 — Write the Relationship Note

Generate a **Title**: a concise one-line summary of the note content (max 80 characters). This is what shows at a glance in Airtable — make it specific and scannable (e.g., "Discussed SiC expansion plans — COR771", "Prefers async over meetings", "Role change: now Director of R&D").

`create_records_for_table` on `tbl3JoPYzslECv8h8`:

| Field ID | Field | Value |
|---|---|---|
| `fld8LW5VmFu5TpSNz` | Title | Generated summary (max 80 chars) |
| `fldlXziO76Ksf9Dtb` | Note | Full note content from Step 1 |
| `fld3hzOyNxzwSKNl6` | Type | Classified type from Step 1 |
| `fldTnNBhyrO63BZ6r` | Date | Date from Step 1 (YYYY-MM-DD) |
| `fld4DHuOEIAbqH8ew` | Source | `"Manual entry"` |
| `fldknMUx9vNoVzFwy` | Person | Relationship Contacts record ID from Step 2 or 3 |
| `fld5aGSQ131q9zAZn` | Project | Project record ID if resolvable; omit if not |

Omit Company (`fld8Xl9cFYfHeclVd`) and Newry Owner (`fldgTzPOyno1xPAZU`) unless you have a confirmed record ID — never link on an unresolved name.

---

## Step 5 — Confirm

Reply briefly:

> "Added [Type] note for **[Name]**: '[Title]'"

If a new contact was created, add:
> "Also created a new Relationship Contacts record for [Name]."

If the note is **Standing Context**, offer one follow-up:
> "This sounds like a durable fact about [Name] — want me to also update their Communication Style or Key Watch-outs field on the contact record?"

Otherwise, stop. Do not ask follow-up questions unprompted.

---

## Feedback capture

Apply the shared feedback-capture sub-skill: `plugins/feedback-capture/SKILL.md`.
- `Plugin:` → `newry-knowledge`
- `Sub-skill:` → `add-context`
