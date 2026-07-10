# Context sources — gathering material for the brief

Goal: enough grounded material to write truthful prep cards, a real action layer, an honest look-ahead, and (weekly) a goal-alignment read. See SKILL.md's flag-don't-fabricate principle — it governs everything below. Run independent lookups in parallel.

## Identity & time

- `get_me` → name, `mail` (canonical identity), `jobTitle`, and mailbox time zone. Anchor "today" in that time zone.
- Use `mail` as the key for the usage log and the Airtable Staff lookup.

## Per-meeting context (Step 2)

For each of today's events:

### Classify
From attendee email domains + subject:
- **Client / external** — any external domain among attendees → emphasize relationship history + project status + what to bring.
- **Internal 1:1** — one other Newry person → emphasize last time's open items; on the weekly day, fold in the goal-check.
- **Recurring status** — recurring series, mostly internal → emphasize last session's action items + blockers.
- **One-off / large / all-hands** — light card; what it's for and any prep.

### Who's in it
- **External attendees** → Airtable Contacts + Context Log (relationship intelligence: who they are, last interaction, standing facts). Enrich only from what's there.
- **Internal attendees** → Airtable Staff for role/team.

### What it's about
- **Map to a project** where possible (see Airtable project lookup below) — gives you goals, status, folder, team.
- **Email thread** — `outlook_email_search` for the recent thread on this subject/with these attendees; read the latest substantive message for current state. **Watch for quoted text inside reply summaries** — a reply's snippet often blends its own new text with the prior message it quotes (tell: an embedded `Subject:`/`From:`/`Sent:` header mid-snippet, or the same sentence appearing in two different emails in the thread). Before attributing a specific quote or decision to a named sender, confirm whose words they actually are — pull the full message via `read_resource` if the snippet leaves it ambiguous. Never quote-attribute from a snippet alone when the sender is unclear. (Real failure case observed: a "pulled back from a live demo" line was actually the meeting organizer's own quoted words embedded in someone else's reply, not that person's statement.)
- **Recurring meeting → last session** — search Otter/Granola for the prior occurrence by title/attendees. **Verify the recording matches the meeting before using it:** confirm the transcript's topic/participants line up with this meeting. If the only recording under the meeting's title is clearly a different conversation, do NOT use it — note "couldn't verify last session" instead. (Real failure case observed: a client working-group slot whose Otter recording was an unrelated internal discussion.)

### Come prepared to
Synthesize 2–4 concrete points — what to say, bring, or decide — grounded only in the above. No filler.

## Action layer (Step 3)

- **Replies owed** — `outlook_email_search` for recent unanswered threads addressed to the user (received, no sent reply after) that read as needing a response. Slack: search granted channels/DMs for direct questions/mentions awaiting the user.
- **Open action items** — commitments the user made, from recent meeting transcripts (Otter/Granola), sent email, and Slack. Each must cite its source.
- **Waiting on** — asks the user made of others with no response yet.
Only include items with a real source. Name any unavailable source.

## Look-ahead (Step 4)

- `outlook_calendar_search` for the next ~2 weeks (and a glance across the month) — client-facing meetings, reviews, deadlines.
- Cross-reference project deliverables/dates where known (Airtable).
- Surface only the few things that matter + a "start now" nudge for anything needing lead time.

## Airtable project lookup (for mapping meetings → projects, and weekly goals)

Base: **Newry Knowledge Management** `appRawPuacfAvVH2Z`. Operate on record/field IDs, never names.

| Table | ID |
|---|---|
| Staff | `tblAeAug2APoy0Jgf` |
| Project Roles | `tblYG4PfBYTnsv0WC` |
| Projects | `tbl3FaAcnmFWjRwqr` |

**User's active projects:**
1. Staff record: `list_records_for_table` on Staff, Full Name (`fldMWoJwEEujuf82V`) contains the user's name; confirm via email (`fldSp1YgJ9TWfHDaa`). Keep the record ID.
2. Project Roles (`tblYG4PfBYTnsv0WC`) AND filter: Staff (`fldjnWTwVjYv926Yf`) `hasAnyOf` [their ID]; Project Status (`fldSuODm0x67u1LrS`) = In Progress (`selkVIFGOzjF1HWWA`). Read Project (`fldMHFHFX3R7RtUK1`). Type choices: ED `seltrFAkd8XIGRXZl`, EM `selchiHG3ThvhSWMk`, Team Member `sel8P4z2faCqffDG5`, Editor `selTT9l6qGaGmScs3`.

**Per-project metadata** (Projects `tbl3FaAcnmFWjRwqr`):

| Field | ID | Use |
|---|---|---|
| Project Name | `fldU9JlF5KzJUw1G3` | label |
| Project Code | `fldlCZtRzO8hORE9V` | matching key |
| Status | `fldJtAz4FzU3U3P6S` | confirm In Progress |
| Project Description | `fldhAgARKAFCQ5THV` | what it's about |
| Client Goals | `fldDc5Xp5reOkAmTP` | goal alignment |
| Firm Goals | `fldLz6Jz9sXI4P3Hz` | goal alignment (value-creation proxy) |
| SharePoint Project Folder Url | `fldbEfKoq99a16y8X` | docs a meeting needs |
| SharePoint Folder Name | `fldxyhKxcytbdHzGs` | SharePoint search fallback |

**Meeting → project matching:** match on client/company + fuzzy code, not exact string (codes drift, e.g. "IN02" vs Airtable "INGEV02"). Use the client/project name as the strong key. If you can't confidently map a meeting to a project, leave it unmapped and say so — don't force it.

## Goal alignment (Step 5, weekly)

- **Project goals + value-creation targets** — Client Goals (`fldDc5Xp5reOkAmTP`) + Firm Goals (`fldLz6Jz9sXI4P3Hz`) across the user's active projects. If a dedicated value-creation-target field is wired later, prefer it.
- **Personal-development goals — PLACEHOLDER, source not wired.** Render the labeled stub; never fabricate.
- **The read:** compare this week's meetings/activity to the goals; one honest observation (well-aimed vs. drifting). If evidence is thin, say alignment can't be judged this week.

## Synthesis discipline

- Tie every line to real source material. Thin sources → a short honest note beats padded detail.
- Nothing on a project/day → say so plainly.
- Respect confidentiality, but the brief is for the user's eyes only — normal detail is fine.
