---
name: weekly-callin-post
description: Draft the user's weekly #weekly_call_in project update for the Tuesday call-in. Use when the user says "draft my call-in post", "weekly update post", "my call-in update", "write my weekly Slack update", "prep my call-in", or when run automatically on a schedule. Pulls the user's active projects from Airtable, reconciles against their recent Slack posts, gathers the week's progress from meetings/SharePoint/email/calendar, and produces a review-ready Slack draft — it never posts. Requires Airtable, Slack, and M365 (Outlook + SharePoint) connectors.
---

# Weekly Call-In Post

Draft this week's project update(s) for the #weekly_call_in Slack channel (channel ID `CRHE9H6F2`), ahead of the Tuesday 10am call-in. One update block per project the user is EM/PM on.

**Core principle: this skill drafts, it never posts.** Always end by creating a Slack *draft* the user reviews and sends themselves. Never call `slack_send_message` to the channel.

## Who is running this

The post is written from the perspective of one person — the currently-authenticated user. Get their identity first:
- Slack: `slack_search_users` on `to:me` context / the logged-in user, or ask if ambiguous.
- Their name maps to a Newry Staff record for the Airtable lookup (see `references/airtable-lookup.md`).

If run interactively and you don't know who "the user" is, ask once: "Whose call-in post am I drafting — you? (I'll use your Slack + Airtable identity.)"

## Connector preflight

Before anything else, confirm the required connectors respond: **Airtable, Slack, Otter, and M365 (Outlook + SharePoint)**. **Granola** is optional — check it too if the person uses it for meeting notes. If a required connector is missing, tell the user exactly which to connect in Cowork Settings → Connectors, and stop. Do not try to work around a missing connector — a post drafted without the data sources will be wrong.

## The five steps

Run these in order. Steps 1–2 are cheap; do them first and get the human checkpoint before spending effort on the heavier gathering in step 3.

### Step 1 — Determine the person's active projects (baseline)

Full procedure and exact field IDs in **`references/airtable-lookup.md`**. In short:
1. Find the person's Staff record.
2. Find Project Roles where Staff = them AND Type = EM, linked to a Project with Status = In Progress.
3. That linked-project set is the **baseline candidate list**.

This is the baseline, not the final list — Airtable is known to be imperfect (see step 2).

### Step 2 — Reconcile against reality, then get a human checkpoint

Build the working list from two inputs: the Airtable baseline (step 1) and the user's own posting history in #weekly_call_in. To read their history: resolve their Slack ID via `slack_search_users`, then `slack_search_public` / `slack_read_channel` with `in:#weekly_call_in from:<@THEIR_ID>` — the `from:` filter needs the ID form; a plain name returns nothing.

**Prior posting history is sufficient evidence — don't ask.** If the user has posted on a project before, that alone justifies drafting on it this week. Include it and draft, no confirmation needed. This is true regardless of what Airtable says:
- A **quiet** project they used to post but haven't lately → include it, draft on it. (Erin: COR766 Tahiti — she's posted it before, so draft it; don't ask "still live?")
- A project they post on but **aren't the EM-of-record** for in Airtable → include it, draft on it. (Erin: IN02/INGEV02 — Airtable lists Amy Fritz as EM, but Erin posts it every week, so draft it.)

So the working list = (Airtable EM + In Progress) ∪ (every project the user has posted on before), minus the exclusions below.

**Only two things require judgment, not a blanket question:**
- **Done projects** — if the most recent post on a project is a "Final Update: Done!" style close-out, drop it (don't re-draft a finished project). If ambiguous, this is the one case worth a quick ask.
- **Brand-new projects with no posting history** — a project in the Airtable baseline the user has *never* posted on. Include it (they're EM on an active project), but flag it as new so they can confirm it belongs.

**Then show the working list and let them adjust** before drafting:
> "Drafting updates for: [list]. [New/ambiguous items flagged.] Adjust anything, or go?"

Keep this light — it's a glance-and-go confirmation, not an interrogation. It's also where org-wide Airtable mismatches surface for later manual cleanup (note them; don't fix in Airtable). On an unattended scheduled run, proceed with the working list and note any flagged items at the top of the draft for the user to resolve on review.

**Do NOT write corrections back to Airtable.** v1 flags only; closeout and EM fixes happen manually through the normal process. The same flag may recur next week — that's acceptable.

### Step 3 — Gather the week's progress per confirmed project

For each confirmed project, gather material since the user's last post on it (or the past ~7 days on a first run). Full source-by-source procedure in **`references/data-sources.md`**. The five sources:
1. **Meeting transcripts** — Otter/Granola, falling back to SharePoint-stored transcripts.
2. **SharePoint** — files changed in the project folder this period (new/edited decks, memos).
3. **Outlook email** — client correspondence this period.
4. **The user's own last post** on this project — for continuity (close the loop on last week's "next steps"; don't restate old news).
5. **Outlook calendar** — upcoming client meetings → feeds *Editorial needs* directly.

### Step 4 — Draft each project block

Assemble each project into the **one standard format used by everyone**. Full template and field-by-field sourcing in **`references/post-format.md`**. Key rules:
- **Use the standard format and field labels for every person, every project — no exceptions.** Do NOT mirror how someone posted before. Prior posts vary ("Findings/Progress", "Background/Purpose", "Update", underscore dividers); the skill's job is to normalize all of that to the single canonical template. Consistency across the channel is the goal.
- **Project code:** use the project's established code as it's recognized in the channel (Airtable's code may differ — e.g. "IN02" vs "INGEV02"; match internally on client + fuzzy code, but the value shown should be the code the team actually uses for that project). This is a data value, not a style choice — don't invent a new code.
- **Findings/Status is the substance** — synthesize the week's actual progress into tight bullets, grounded only in what the sources show. Do not invent progress.
- **Issues/Risks stays conservative** — only include a risk a source actually surfaced (a concern raised in a meeting, a slipped date). Otherwise "None" — never invent a risk to fill the field.
- Static fields (Purpose, Team) come from Airtable and rarely change week to week — carry them forward, but conform the labels to the standard.

### Step 5 — Duplicate check, then create the draft

1. **Per-project duplicate check:** before drafting each project, check whether a post for that project already exists in #weekly_call_in *this week* (posted manually, by a teammate, or on another device). If one exists, skip that project and note it was skipped. This is what lets a late/catch-up run be safe with no time cutoff. If every project is already covered, don't create an empty draft — just tell the user everything's already posted.
2. Combine the surviving project blocks into one message (multiple projects = multiple blocks in a single post; blank line between blocks).
3. Create it as a **Slack draft** in `CRHE9H6F2` via `slack_send_message_draft`. Return the draft link and a one-line summary of what to review (especially any items flagged in step 2).
4. **Handle the one-draft-per-channel limit.** Slack allows only one attached draft per channel; if one already exists, the tool returns `draft_already_exists`. Do NOT silently overwrite or fail. Instead: read the existing draft, and if it's a prior run of this skill (an unsent weekly post), tell the user it's there and ask whether to replace it (they delete the old one in Slack, then re-run) or keep it. If it looks like something they wrote themselves, never touch it — surface it and hand back the new content for them to merge. Never call `slack_send_message` to the channel under any circumstance.

## Scheduling (set up once)

This skill is built to run weekly via Cowork's native `/schedule` (e.g. Tuesday ~7am). If the machine is asleep/closed at fire time, Cowork runs it on next launch — so a late catch-up run is normal and expected, which is exactly why step 5's duplicate check exists. Tell a first-time user to set up the schedule with `/schedule` after their first successful manual run.
