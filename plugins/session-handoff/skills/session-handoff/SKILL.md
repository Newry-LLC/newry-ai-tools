---
name: session-handoff
description: >
  Sylvan's personal baton between Claude Code and Cowork build sessions for the Newry AI
  program. Use at session START ("let's go", "go", "startup", "resume", "continue where we
  left off", or the first message of a build session) to read the handoff batons and resume.
  Use at session CLOSE ("close session", "wrap up", "let's stop here") to update this
  session's baton. Mirrors the CLAUDE.md startup ritual on the Code side.
---

# Session Handoff

Personal handoff for Sylvan's Newry AI build work. Sylvan only — not distributed.

Batons live in **`handoff/`** at the `Building Tools for Newry` root — **one file per session**
(`handoff/<surface>-<date>-<id>.md`, e.g. `handoff/cowork-2026-05-29-a3f.md`). Per-session files
mean concurrent sessions never overwrite each other.

## Locating the workspace

`handoff/` is in `Building Tools for Newry`. If not already the working dir, request access via
`request_cowork_directory` / `request_directory` — never tell Sylvan to do it manually. If access
fails, say so and continue without the baton.

## START (triggers: "let's go", "go", "startup", "resume", first message of a session)

1. Read all batons in `handoff/`. Archive any >24h old to `handoff/archive/`.
2. **Reconcile against reality** — cross-check batons vs. git status, recent file mtimes, and
   `strategy/decision-log.md`. If a baton looks stale (e.g. a forgotten close), flag it.
3. Show the recent batons briefly; if more than one is live, ask which to resume.
4. State resume point + next step + any unpushed/unsynced flag. Wait for go-ahead.
5. Then read `Session Startup.md`.

If `handoff/` is empty, say so and fall back to `Session Startup.md`.

## DURING the session — keep the baton fresh

Don't wait for close. Update this session's baton at milestones, decisions, and file writes, so a
forgotten close costs nothing. First substantive action of a session: create this session's baton file.

## CLOSE (triggers: "close session", "wrap up", "let's stop here")

Overwrite this session's baton. Keep every field to a line or two:

```markdown
# HANDOFF — <surface> <date>

**Last update:** <ISO timestamp>
**Active task:** <one line>
**Left off:** <the half-finished thing>
**Next step:** <first concrete action next session takes>
**Unpushed/unsynced:** <edited-but-not-pushed / written-but-not-packaged — or "None">
**Files touched:**
- <path>
**Open threads (not blocking):**
- <anything worth remembering>
```

If it's a full close (not just a baton drop), prompt Sylvan to run the rest of the CLAUDE.md ritual
(Session Startup, auto-memory, stories-and-lessons, plugin-index).

## Style

Be as brief as possible. Bullets, no preamble.
