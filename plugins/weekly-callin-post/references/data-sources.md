# Data sources — gathering the week's progress per project

Goal: enough grounded material to write a truthful *Findings/Status*, *Editorial needs*, and *Issues/Risks* for each project. **Everything in the draft must trace to something a source actually shows. Never invent progress or risks.**

## Lookback window

From the timestamp of the user's last #weekly_call_in post on this project → now. On a first run with no prior post, use the past 7 days. (Getting the last post also gives you continuity — see source 4.)

## The five sources

Run the independent lookups in parallel where possible; they're per-project.

### 1. Meeting transcripts (richest signal)

People record in different tools — check broadly:
- **Otter** — search meetings in the window whose title/attendees map to this project/client. Pull transcripts of the relevant ones.
- **Granola** — some people use it instead of Otter (e.g. David). If a Granola connector is present, search it too.
- **SharePoint fallback** — not everyone records into Otter/Granola. Search the project's SharePoint folder (and general SharePoint) for transcript/notes files dated in the window.
- Extract: decisions made, findings surfaced, commitments, client reactions, new risks.

### 2. SharePoint — recently changed project files

Start from the project's `SharePoint Project Folder Url` (Airtable `fldbEfKoq99a16y8X`) or `SharePoint Folder Name` (`fldxyhKxcytbdHzGs`). Look for files created/modified in the window — new or edited decks, memos, models, SoFs. A new deck or a heavily edited analysis is usually the week's headline progress.

### 3. Outlook email — client correspondence

Search the user's Outlook mail in the window for threads with the client (known client contacts/domain for this project; infer domain from the client name if needed). Surface: what was sent to / received from the client, scheduling, asks, decisions. Respect client confidentiality — this is for the internal post only.

### 4. The user's own last post on this project (continuity)

Retrieve the most recent prior post for this project. Use it to:
- Close the loop on last week's *Next Update* / promised next steps — did they happen?
- Avoid restating old news — this week's Findings should be the delta, not a repeat.
- Carry forward the static fields (Purpose, Team) and the person's exact code string and label style.

### 5. Outlook calendar — upcoming client meetings → Editorial needs

Scan the user's calendar for the next ~1–2 weeks for client-facing meetings on this project. Use them to:
- Populate *Next Update* / *Final Update* timing.
- Drive *Editorial needs*: a client meeting next week usually implies a deck is needed. State it concretely from the calendar — e.g. "major client meeting next Wednesday → likely deck needed," or "regular weekly client check-in next week." Don't over-infer beyond what the calendar shows.

## Synthesis discipline

- Tie each Findings bullet to real source material; if sources are thin for a project, a short honest status ("interviews in progress; synthesis next week") beats padded detail.
- If nothing happened on a project this week, say so plainly rather than manufacturing activity.
- Keep the client's confidential specifics appropriate for an internal channel, but this is internal — normal project detail is fine.
