---
name: daily-prep
description: Produce the user's morning brief for the day. Use when the user says "daily prep", "prep me for my day", "morning brief", "what's on today", "prep me for my meetings", "get me ready for today", "prep me for [a different day]", or when run automatically on a morning schedule. For each meeting on today's calendar it writes a prep card (what it's about, who's in it, what to walk in ready to say/bring/decide), surfaces what needs the user today (replies owed, their open action items, what they're waiting on), looks ahead at the week and month, and once a week checks whether the week's activity points at the user's goals. Role-adaptive — scales to the person's meeting load. Requires M365 (Outlook); enriched by Slack, Airtable, and Otter/Granola.
---

# Daily Prep

Produce a tight, skimmable morning brief that gets the user ready for their day. The brief has three parts — **A · Today**, **B · Looking ahead**, and **C · Goal alignment** (weekly only). Full layout and wording in **`references/output-format.md`**; per-source gathering procedure in **`references/context-sources.md`**.

**Core principle: prep, don't perform.** This skill assembles and delivers a brief the user reads. It never sends anything on the user's behalf to anyone else, never replies to email or Slack, never accepts a meeting. The only message it may send is the brief itself, to the user's *own* self-DM (see Delivery).

**Second principle: flag, don't fabricate.** Every line in the brief must trace to something a source actually shows. If context can't be verified — a recurring meeting whose only recording is about a different topic, an attendee with no record, a project you can't map — say so plainly ("couldn't verify last session") rather than inventing. Empty and honest beats confident and wrong.

## Who is running this

The brief is written for one person — the currently-authenticated user. Establish identity first:
- **M365:** call `get_me` for the user's name, email, job title, and mailbox time zone. The `mail` field is the canonical identity.
- Use that email as the key everywhere the user must be identified (usage log, Airtable Staff lookup). **Personalize by session email — never a hardcoded or guessed `user_id`.**

If `get_me` fails, M365 isn't connected — see preflight; the brief can't be built without the calendar.

## Connector preflight

Check connectors before working. **Degrade gracefully — do not stop on missing enrichers:**
- **M365 (Outlook) — required.** No calendar, no brief. If absent, tell the user to connect it in Cowork Settings → Connectors, and stop.
- **Slack, Airtable, Otter/Granola — enrichers.** If one is missing, build the brief without it and **name the gap in the output** ("Slack not connected — 'needs a reply' covers email only"). Never silently omit; never block.

**⚠️ Slack channel access is not automatic.** Even with Slack connected, the skill can only read channels/DMs it has been explicitly granted. If Slack is connected but returns nothing useful, tell the user once: to get Slack into the brief, add this integration to the specific channels and DMs you want read. Don't treat an access gap as "nothing happening."

## Usage logging

At the start of every run — before other work — create one record in the Airtable Plugin Usage Log. Silent and automatic; no user-facing output. (Skip only if Airtable isn't connected.)

- **Base ID:** `appRawPuacfAvVH2Z` | **Table ID:** `tblmACtwIClniGn5n`
- **Tool:** `create_records_for_table`
- **Fields:**
  - `fldRrr3BkrJW8rE3L` (ts) — current UTC time, ISO 8601 (e.g. `2026-07-08T11:30:00Z`)
  - `fldNHK285dPCOdNhB` (plugin) — `"daily_prep"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — `"daily_prep"`
  - `fldmTXyfFZRpbZEvQ` (user_id) — the user's email from `get_me` / session context; `"unknown"` if unavailable
  - `fldu8rvXDfvi2O3jF` (project) — `""` (a brief spans many projects)

If the write fails, continue silently.

## The steps

Run in order. Steps 1–2 are the spine (**A · Today**); 3 rounds out Today; 4 is **B**; 5 is **C** and runs only on the weekly day. Do per-meeting and per-source lookups **in parallel** where possible — the brief should assemble fast.

### Step 1 — Anchor the day and pull its calendar

1. **Determine the anchor day.** Default: today, in the user's mailbox time zone (from `get_me`). If the user names a different day ("prep me for last Tuesday," "run this for the 15th," "test it on a busier day") resolve that day instead, in the same time zone.
2. `outlook_calendar_search` for the anchor day's events (afterDateTime = anchor day 00:00, beforeDateTime = anchor day 23:59, order = oldest). Read attendees, organizer, recurrence, location, subject, body.
3. **If the anchor isn't today, say so.** Put it in the header (see output-format.md) and flag that Step 3's action layer (replies owed, open items, waiting on) reflects the *current* inbox/Slack state, not a snapshot as of the anchor day — those items can be stale or mismatched when the anchor isn't today. Everything else (meeting cards, look-ahead) still works on real source material regardless of anchor.
4. **Drop declined events; flag tentative ones.** Skip anything the user declined — it's not part of their day. For "tentative" RSVP status, keep the card but mark it "(tentative)" in the header so the user knows it may not happen.
5. Note the shape of the day early: **0 meetings** → skip straight to a light "no meetings today" A-section plus B (and C if weekly); **many meetings** → full per-meeting cards. This is the role-adaptivity — let the actual calendar drive depth, don't ask. Same rule always: don't ask the user what kind of day they have, read it from the calendar.

### Step 2 — Build a prep card per meeting

For each meeting, gather context and write one card. Full procedure in **`references/context-sources.md`**. In short, per meeting:
- **Classify the meeting** — client/external, internal 1:1, recurring status, or one-off — from attendees' email domains and the subject. The card's emphasis follows the type (see output-format).
- **Who's in it** — external attendees → enrich from Airtable Contacts/Context Log; internal → role/team from Airtable Staff.
- **What it's about** — map to a project (Airtable) when possible; pull the recent email thread; for a recurring meeting, pull the *last session's* notes (Otter/Granola) — **but verify the recording actually matches this meeting** before using it (see the flag-don't-fabricate rule; a real failure case is a recurring slot whose recording is a different conversation).
- **Come prepared to** — synthesize into 2–4 concrete "say / bring / decide" points grounded only in what the sources show.

### Step 3 — What needs you today

Round out **A** with the action layer, from Outlook + Slack (granted channels/DMs):
- **Replies owed** — unanswered threads addressed to the user that look like they want a response.
- **Your open action items** — commitments the user made (in recent meetings, email, Slack) that are still open. Ground each in its source; don't invent.
- **Waiting on** — things the user asked others for that haven't come back.
Keep this tight and only include items with a real source. If a source (e.g. Slack) is unavailable, scope this to what you have and say so.

### Step 4 — Looking ahead (B)

From the calendar (next ~2 weeks and a glance at the month) plus known deliverables:
- Key upcoming events and client-facing meetings.
- Deliverables/deadlines coming due.
- A short "what to start now" nudge for anything that needs lead time.
Keep it to the few things that actually matter — this is a heads-up, not a full calendar dump.

### Step 5 — Goal alignment (C · weekly only)

Run **only on the configured weekly day** (default Monday; skip other days — if the user asks for a different weekly day, use that day instead). Pull the user's goals and give an honest read on whether the week points at them:
- **Project goals + value-creation targets** — from Airtable for the user's active projects (Client Goals `fldDc5Xp5reOkAmTP`, Firm Goals `fldLz6Jz9sXI4P3Hz`; see `references/context-sources.md` for the project lookup). If a dedicated value-creation-target field is wired later, use it.
- **Personal-development goals — PLACEHOLDER.** Source not yet wired. Until it is, render a labeled stub in the output: *"Personal-development goals — not yet connected. [Tell Daily Prep where these live to enable.]"* Do not fabricate personal goals.
- **The read:** compare the week's meetings/activity against those goals and offer one honest observation — where the week is well-aimed, and where it's drifting. Frame as a nudge, not a scold. If evidence is thin, say the alignment can't be judged this week rather than inventing one.

### Step 6 — Assemble and deliver

Assemble A (+B, +C if weekly) per **`references/output-format.md`**: calendar-ordered cards, tight sections, gaps named. Then deliver (below).

## Delivery

- **Interactive run** (user asked for it): render the brief directly in the session.
- **Scheduled run:** send the brief to the user's **own Slack self-DM** (`to:me` / the user's own DM) so it's waiting on their phone in the morning. This is the only send this skill performs, and only ever to the user themselves. If Slack isn't connected, fall back to rendering it for the next interactive session. **Never** send the brief to any channel or other person.

## Scheduling (set up once)

Built to run every morning via Cowork's native `/schedule` (e.g. daily ~6:30am). If the machine is asleep at fire time, Cowork runs it on next launch — a late brief is still useful; just anchor it to the correct "today." Tell a first-time user to set up the schedule with `/schedule` after their first successful manual run. The weekly **C** section keys off the day of week (default Monday), so one daily schedule covers both the daily and weekly cadence.

## Feedback capture

Read and follow the shared feedback-capture sub-skill: `../feedback-capture/SKILL.md`. When logging: `Plugin:` → `daily-prep`, `Sub-skill:` → `daily-prep`.
