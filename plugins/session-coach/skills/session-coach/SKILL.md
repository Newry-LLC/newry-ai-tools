---
name: session-coach
description: >
  Evaluates a consultant's Cowork session transcript and produces concise scored coaching
  feedback. Fires automatically at session close ("close session", "wrap up", "done for today")
  and via a nightly scheduled task for sessions that weren't formally closed. Use whenever a
  consultant wants to improve how they work with Claude — better prompts, smarter tool use,
  fewer wasted rounds.
---

# Session Coach

Evaluates how effectively a consultant used Cowork in a session and returns a brief scored
report with actionable improvement recommendations.

---

## Usage logging

At the start of every run, write one record to Airtable. Silent — no user-facing output; fail silently on error.

- **Base ID:** `appRawPuacfAvVH2Z` | **Table ID:** `tblmACtwIClniGn5n`
- **Tool:** `create_records_for_table`
- **Fields:** `fldRrr3BkrJW8rE3L` (ts, ISO 8601 UTC) · `fldNHK285dPCOdNhB` (plugin: `"session_coach"`) · `fld4EyuVEhxAhPZEd` (sub_skill: `"session_coach"`) · `fldmTXyfFZRpbZEvQ` (user_id: read `~/.user_id` or `"unknown"`) · `fldu8rvXDfvi2O3jF` (project: `""`)

---

## When this runs

1. **Session close** — fires as part of the close ritual. Ask: *"What model were you using this session?"* (e.g. Sonnet, Opus, Haiku). Record the answer. Then run the evaluation.

2. **Nightly scheduled task** — evaluates all sessions not yet scored:
   - Call `list_sessions` (limit 20)
   - Read watermarks from `coaching-log.md` (the `**Watermark:**` field in each entry)
   - For each session whose ID is not in the watermarks, call `read_transcript` and evaluate
   - If `coaching-log.md` doesn't exist yet, treat all sessions as unevaluated
   - Always append new entries above the `## Running Synthesis` section

---

## Step 1 — Get the transcript

Call `mcp__session_info__read_transcript` for the session. If unavailable, note it and skip gracefully.

---

## Step 2 — Evaluate against the rubric

Score each criterion 1–5. Be honest — 3 is average, not a compliment.

**1. Task framing** — Did they tell Claude what they're trying to accomplish, what's going on around it, and anything that would shape a good answer — before asking for output? A rich brain dump beats a clean but thin prompt. Penalize narrow "just do X" requests with no situation or purpose.
- *2 = thin opener, context came out reactively mid-session*
- *4 = opened with clear goal + situation; Claude could act without clarifying*

**2. Iteration efficiency** — How many rounds to reach a usable output? Correction rounds ("no, actually...") signal thin initial framing. Reward sessions where the first response was close and refinement was deliberate, not corrective.

**3. Skill and tool utilization** — Did they use the right Newry skills for the task? See the Skills Reference at the bottom of this file. Penalize cases where a consultant did manually what a skill handles. Reward correct, intentional skill invocation.

**4. Output verification** — Did they treat Claude's output as a draft to interrogate, or accept it at face value? Reward pushback, spot-checking, requests for alternatives. Penalize copy-paste-without-review — especially for client-facing content.

**5. Context economy** — Did they provide rich context upfront and avoid re-explaining across turns? Two failure modes: (a) under-context — sparse setup forcing clarification rounds; (b) redundant re-pasting — restating background Claude already had. Reward one thorough setup followed by efficient turns.

**6. Token efficiency** — Did they request concise outputs when appropriate? Penalize "rewrite the whole thing" when a targeted edit would do.

**7. Artifacts and files vs. chat** — Did they use files for substantial content, or leave long outputs in chat? Chat is for interaction; files are for deliverables. Reward creating .md, .docx, .html etc. for anything more than a few paragraphs.

---

## Step 3 — Write the coaching entry

Determine the log path:
- If a folder is mounted, write to `coaching-log.md` there
- If no folder is mounted, write to `~/Desktop/coaching-log.md` and note the location

Always append new entries **above** the `## Running Synthesis` section (create the file and section if they don't exist).

### Entry format

```
---
## Session: [YYYY-MM-DD] | Model: [model or "not recorded"]

| Criterion              | Score |
|------------------------|-------|
| Task framing           | X/5   |
| Iteration efficiency   | X/5   |
| Skill & tool use       | X/5   |
| Output verification    | X/5   |
| Context economy        | X/5   |
| Token efficiency       | X/5   |
| Artifacts vs. chat     | X/5   |
| **Overall**            | **X.X/5** |

**Top recommendations:**
- [Most impactful specific behavior to change, with a concrete example from this session]
- [Second recommendation if meaningfully different from the first]

**Watermark:** [session_id]
```

Only include recommendations that are genuinely worth changing. If the consultant scored well overall, say so briefly and skip weak recs.

---

## Step 4 — Update the synthesis

Overwrite (don't append) the `## Running Synthesis` section at the bottom of the file.

```
## Running Synthesis
_Last updated: [YYYY-MM-DD] after [N] sessions_

- [Persistent strength]
- [Recurring pattern to work on]
- [Trend observation]
```

Keep to 3–5 bullets. Drop dimensions where the consultant consistently scores 4–5 — they've internalized it.

---

## Notes

- Short sessions (<5 turns): score conservatively, note limited signal.
- Model is informational only — don't adjust scores based on model used.

---

## Feedback capture

Applies across all runs. Read and follow the shared feedback-capture sub-skill:
`../feedback-capture/SKILL.md`

When logging:
- `Plugin:` → `session-coach`
- `Sub-skill:` → `session-coach`

---

## Skills Reference

Use this to evaluate criterion 3. If a consultant did one of these jobs manually instead of invoking the skill, penalize.

| Skill | Job |
|-------|-----|
| Primary Research Toolkit | Designing research plans, interview guides, synthesizing transcripts, coding corpus |
| SoF Toolkit | Evaluating, aligning, or drafting Summary of Findings slides |
| newry-knowledge | Searching SharePoint or Airtable for Newry project history, contacts, or institutional knowledge |
| Project Technical Onboarding | Getting up to speed on a client's technical landscape |
| RMA-OA Builder | Building RMA or OA sections for project deliverables |
| TAM Generator 