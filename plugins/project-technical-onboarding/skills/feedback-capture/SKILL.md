---
name: feedback-capture
description: >
  Internal shared sub-skill — not invoked directly by users. Each plugin coordinator
  references this file to apply consistent feedback capture behavior across all Newry
  plugins. Logs positive and negative signals to the cross-plugin central feedback log.
---

# Feedback Capture — Shared Sub-skill

**Purpose:** Capture feedback across all Newry plugins — both problems and positive signals — into a single cross-plugin log for evals and program improvement.

This is a shared sub-skill. It is not invoked directly by consultants. Each plugin coordinator references this file and applies these instructions.

---

## When to capture

Capture feedback whenever the user's message contains a feedback signal — positive or negative — regardless of which sub-skill is active or whether a run is in progress.

**Positive signals:**
- Explicit: "feedback:", "love this," "this is great," "nailed it," "exactly right," "perfect"
- Implicit: "wow," "that's really cool," "show this to the team," "use this as a template," "this is exactly what I wanted," "impressive," "this works," "exactly what I needed," "save this," "this is the one"

**Negative signals:**
- Explicit prefix: `feedback:`, `issue:`, `bug:`, `problem:`
- Implicit: "this is wrong," "what I actually wanted was…," "does not work," "this is missing X," "the output should have…," "I'd expect…," "why did it…," "this is confusing," "that's not right," "not what I asked for"

If a signal is ambiguous (e.g., "interesting"), do not log. Capture only when signal intent is clear.

---

## Draft, confirm, then log

Before writing, reconstruct the interaction context from the recent conversation, draft the log entry, and show it to the user:

> Here's what I'd log — does this capture it?
> ```
> [draft entry]
> ```
> Anything to add or correct?

Once confirmed (or corrected), append the final entry to **both**:
- Local: `logs/feedback-log.md` in the current working folder (create if it does not exist)
- Central: `~\Newry Corp\Clients - Claude Master Working Folder\logs\feedback-log-<user_id>.md`
  (construct path using the UUID from `~/.user_id` — same UUID as the usage log; create if it does not exist)

If the central log is not accessible, skip silently — do not surface an error to the user.

If feedback comes mid-run, pause briefly for the draft-confirm step, then continue the run.

---

## Log entry format

```
---
Date: [YYYY-MM-DD HH:MM TZ]
Plugin: [primary-research-toolkit | sof-toolkit | newry-knowledge | plugin-auditor | other]
Sub-skill: [sub-skill name | "general"]
Signal type: [positive | bug | friction | quality | feature | question]
Severity: [high | medium | low | n/a]
User's words: "[verbatim quote]"
What was happening: [one line — what the skill was doing when signal occurred]
Output: [one line — what was produced or attempted]
Notes: [positive → what specifically landed well; negative → what went wrong]
Status: open
```

**Signal type definitions:**
- *positive* — something worked well; worth repeating or citing
- *bug* — broken behavior or malformed output
- *friction* — hard to use, unclear instructions, wasted effort
- *quality* — wrong finding, off synthesis, inaccurate output
- *feature* — capability not currently in the skill
- *question* — how to do something (log so instructions can be sharpened)

**Severity:**
- *high* — output unusable or blocks the task
- *medium* — correctable quality issue or meaningfully slows the run
- *low* — feature wish, minor friction, question
- *n/a* — use for positive signals

**Infer, don't ask.** Populate all fields from the recent conversation context. Ask only if something critical is genuinely ambiguous. Never prompt the user to fill in log fields.

---

## Coordinator instructions

Each plugin coordinator that references this sub-skill should:

1. Supply the correct `Plugin:` value for its context
2. Supply the correct `Sub-skill:` value based on which sub-skill is active at the time of capture
3. Follow all instructions above verbatim
