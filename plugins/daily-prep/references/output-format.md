# Output format — the morning brief

Tight, skimmable, ~30 seconds per meeting card. Lead with the date and a one-line read on the day. Sections in order: **A · Today**, **B · Looking ahead**, **C · Goal alignment** (weekly day only). Name any missing source inline rather than omitting silently.

## Header

```
☀️ Daily Prep — {Weekday, Month D, YYYY}
{one-line read on the day: "3 meetings, one client-facing" / "No meetings — a build day" / "Packed: 6 meetings back-to-back"}
```

If the anchor day isn't today, add a line: *"Anchored to {date}, not today — 'What needs you today' below reflects your current inbox/Slack, not a snapshot from that day."*

## A · Today

### Meeting cards (calendar order)

One card per meeting. Emphasis follows the meeting type (see context-sources classify step). Template:

```
## {start–end tz} · {subject}
{platform / location · organizer · "recurring" if so}

**What this is about**
{1–3 sentences — the point of the meeting, mapped to the project where known}

**Who's in it**
- {Newry}: {names + roles}
- {Client/external}: {names + roles; relationship note if Airtable has one}

**Come prepared to**
- {2–4 concrete say / bring / decide points, grounded in sources}

{⚠️ only if relevant: a verification gap, e.g. "Couldn't verify last session — the recording under this title is a different conversation."}
```

Type-specific emphasis:
- **Client/external** → relationship history + project status + what to bring.
- **Internal 1:1** → last time's open items (+ goal-check on the weekly day).
- **Recurring status** → last action items + blockers.
- **One-off/all-hands** → light card: what it's for, any prep.

If **0 meetings**: skip cards; one line ("No meetings today — a build/heads-down day") and let B and the action layer carry the brief.

### What needs you today

```
**Needs a reply** — {sender/topic → what they're waiting on}
**Your open items** — {commitment → source, still open}
**Waiting on** — {who/what you're waiting for}
```
Only real, sourced items. If a source is off (e.g. Slack), note it: "(email only — Slack not connected)".

## B · Looking ahead

```
### Looking ahead
- **This week:** {key events/deliverables}
- **This month:** {the few that matter}
- **Start now:** {anything needing lead time}
```
A heads-up, not a calendar dump. Skip a line if there's genuinely nothing.

## C · Goal alignment (weekly day only)

```
### Goal check (weekly)
- **Project goals / value creation:** {the goals, from Airtable}
- **Personal development:** Not yet connected. [Tell Daily Prep where these live to enable.]
- **This week's read:** {one honest observation — well-aimed vs. drifting; or "can't judge this week — thin signal"}
```
Nudge, not scold. Never fabricate goals or the read.

## Footer

```
Sources: {which connectors fed this run}. {Any gaps.} Reply "shorter", "more on {meeting}", or "add {source}" to refine.
```

## Voice

- Plain, direct, everyday words. No jargon, no filler, no preamble.
- Confident where sourced; explicitly uncertain where not.
- The whole brief should read in about a minute.
