---
name: account-management
description: Build a stakeholder plan for a new project. Reads relationship history from Airtable (Contacts + Context Log), writes a per-stakeholder standing-context note for each person on this engagement, and outputs a stakeholder plan for the kickoff doc. Gets richer with every project as relationship intelligence accumulates.
---

# Account Management Sub-Skill

Build a per-stakeholder plan for the engagement — grounded in Newry's accumulated relationship history where it exists, and in educated inference where it doesn't.

## Inputs

**Required:**
- Stakeholder list (names, titles, roles — from the problem statement: sponsor, direct contact, others)
- Project code

**Optional:**
- Prior relationship context (surfaced automatically from Airtable — no manual input needed)
- Team roster (used to assign CRM relationship ownership)
- NBD call notes or prior contact context (if available, for first-time clients)

## Airtable Tables

Base: `appRawPuacfAvVH2Z`

| Table | ID | Purpose |
|---|---|---|
| Contacts | `tblomVbLXeELjFIBZ` | Person spine — all people Newry has a relationship with |
| Context Log | `tbl3JoPYzslECv8h8` | Append-only intelligence log; per-engagement context lives here as `Type = Standing Context` notes scoped by the Project link |

> The former **Stakeholder Profiles** table was folded into Context Log and deleted (2026-06-11). Per-person-per-engagement context is now a `Type = Standing Context` note linked to the Person + Project — no separate table.

## What This Skill Does

### Step 1 — Confirm Contacts exist
For each stakeholder named in the problem statement:
- Search `Contacts` by name + company
- If not found: the record is expected to have been created by the Airtable automation on project-launch form submit — flag if missing and prompt the EM to check

### Step 2 — Pull existing relationship history
For each stakeholder found in `Contacts`:
- Query `Context Log` filtered by Person → surface all prior notes, sorted by date (Interactions, Standing Context, Goals, Outcomes)
- Synthesize into a relationship summary: how long Newry has known this person, relationship trajectory, key watch-outs, communication preferences, what's worked

For new relationships (no history): note explicitly and proceed with inference from the SoW and any NBD context.

### Step 3 — Write a Standing Context note per stakeholder
For each stakeholder, create a record in `Context Log` (`tbl3JoPYzslECv8h8`) that captures the engagement plan as durable context:

| Field ID | Field | Value |
|---|---|---|
| `fld8LW5VmFu5TpSNz` | Title | `"Stakeholder plan — [Name] — [Project Code]"` |
| `fldlXziO76Ksf9Dtb` | Note | Role on this engagement (Sponsor / Direct Contact / Influencer / Gatekeeper); what success looks like for this person (not the project — the individual); what's keeping them up at night (risk, pressure, timing, politics); their next challenge after this project and how Newry can help; CRM goals (specific, time-bound, owner-assigned) |
| `fld3hzOyNxzwSKNl6` | Type | `"Standing Context"` |
| `fldTnNBhyrO63BZ6r` | Date | today (YYYY-MM-DD) |
| `fld4DHuOEIAbqH8ew` | Source | `"PLT"` |
| `fldknMUx9vNoVzFwy` | Contact | Contacts record ID from Step 1 |
| `fld5aGSQ131q9zAZn` | Project | this project's record ID |
| `fldgTzPOyno1xPAZU` | Newry Owner | assigned team member — omit unless you have a confirmed record ID |

This `Type = Standing Context` note replaces the old Stakeholder Profiles record — the Type tag + Project link carry the per-engagement structure, and the note becomes part of the history the next EM reads.

### Step 4 — Output the stakeholder plan
Produce the stakeholder plan section of the kickoff doc (see Output Format).

## CRM Goals

CRM goals should be concrete and time-bound, not platitudes. Examples:
- "ED to have dinner with [Sponsor] before kickoff"
- "EM to schedule informal call with [Direct Contact] at 4-week mark — no agenda, just a relationship touchpoint"
- "Feedback call with [Sponsor] within 2 weeks of final; probe for follow-on"

Assign each CRM goal to a specific team member.

## Output Format

```
ACCOUNT MANAGEMENT — [Client Name] — [Project Code]

CLIENT RELATIONSHIP OVERVIEW:
[2–3 sentences on Newry's history with this client. If new: note it's a first engagement.]

PER-STAKEHOLDER PLANS:

STAKEHOLDER: [Name] — [Title]
  Role in this engagement: [Sponsor / Direct Contact / Influencer / Gatekeeper]
  Relationship history: [Summary from prior notes — or "New relationship" if none]
  What does success look like for this person? (Not the project — the individual)
    [Answer — grounded in relationship history where it exists; inferred from context where it doesn't]
  What's keeping them up at night? (Risk, pressure, timing, politics)
    [Answer]
  What is their next challenge after this project? What can we do to help?
    [Answer]
  CRM owner (Newry): [Name]
  CRM goals:
    - [Specific action + timing]
    - [Specific action + timing]

[Repeat for each stakeholder]

RELATIONSHIP RISKS:
- [Any misaligned goals, political dynamics, or relationship risks to flag]

NEXT STEP: Review with ED before kickoff. Update each stakeholder's Standing Context note in Context Log after the kickoff meeting once you have a clearer read on each person.
```

## Design Notes

- **History compounds.** The first run for a new client will be sparse. By the third project, this sub-skill should surface years of relationship context automatically. The value builds over time.
- **Don't fabricate answers to the three questions.** For new relationships, say so explicitly and infer from SoW or NBD context — flag anything inferred as inferred.
- **CRM goals must be actionable.** "Strengthen the relationship" is not a CRM goal. Assign a person, an action, and a timing.
- **Context Log are the accumulation vehicle.** Every PLT run writes a `Standing Context` note per stakeholder. These become the history the next EM reads.
- **Flag missing Contacts records.** The Airtable automation should have created them on form submit. If a stakeholder is missing, something broke in the launch process.

## References

- Project Initiation Template — the account management pages (per-stakeholder success grid, trust-equation worksheet)
- SharePoint: `Consulting Resources/Knowledge Nuggets/Client Overviews and CRM/` — client overview knowledge nuggets
- SharePoint: `Consulting Resources/TOOLS-TRAINING/Trusted Advisor Documents/` — trust equation framework
