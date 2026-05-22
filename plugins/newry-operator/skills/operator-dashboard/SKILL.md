---
name: operator-dashboard
description: >
  Creates or refreshes the Newry AI Program operator dashboard — a persistent Cowork artifact
  showing current plugins, program milestones, and recent decisions. Use when a program builder
  asks "what's been built", "show me program status", "show the dashboard", or "refresh the
  dashboard". Also runs automatically at the start of any operator session via the coordinator.
---

# Operator Dashboard

Generates or refreshes the persistent Cowork artifact for Newry AI Program operators. Shows
program direction, the current plugin registry, milestones, and recent decisions in a single
persistent view.

**Audience:** Program builders. Data sourced from live logs folder and bundled references.

---

## What to load

**From live logs folder** (preferred):
- `~\Newry Corp\Clients - Claude Master Working Folder\logs\newry-operator\decision-log.md`
  — most recent 5 decisions. Fall back to bundled `references/decision-log.md` if folder
  not synced; note in the artifact which source was used.

**From Cowork working folder:**
- `strategy/program-status.md` — current plugin versions and status. Fall back to bundled
  `references/plugin-index.md` if not found; note in the artifact which source was used.

**From bundled references:**
- `references/plugin-index.md` — fallback for plugin data
- `references/north-star.md` — north star statement, business outcome target, milestones
- `references/vision.md` — May 2027 vision narrative

---

## What to extract

**From north-star.md:**
- North star statement
- Business outcome target
- Milestones table (date, target, what it signals)
- Leading indicators (active weekly usage rate, eval pass rate)

**From vision.md:**
- "May 2027" section — the vivid future state narrative
- "What this commits us to" — the two commitments

**From program-status.md (preferred) or plugin-index.md (fallback):**
- Plugin name, version, status, audience for each plugin/tool
- Any items with "pending" or open items

**From decision-log.md:**
- The 5 most recent entries
- For each: date, title, decided (one sentence)

---

## Build the artifact

Generate a clean HTML dashboard with these sections in order:

### 1. Program header
- Title: "Newry AI Program — Operator Dashboard"
- North star statement (quoted, prominent)
- Business outcome target
- Data currency note: "Plugin data from [source: program-status.md or plugin-index.md],
  current as of [date]. Decisions from [GitHub or bundled snapshot].
  Usage data from local logs, trailing 30 days as of [date].
  Refresh by re-running 'show the dashboard'."

### 2. Program direction (expandable, collapsed by default)
A single collapsible block labelled **"Program Direction ▸"** containing three sub-sections:

- **North Star** — the statement + the "why" breakdown (same team / materially better work /
  the P&L shows it)
- **Business Outcome** — 2x profit per consultant by May 2027; leading indicators
  (active weekly usage rate + eval pass rate) as the measurable path to it
- **Vision** — the May 2027 narrative (what a typical morning looks like; what shifts at
  the firm level; what this commits us to)

### 3. Plugin registry

**Before building this section**, compute usage metrics from the log files:

```python
import os, glob, json
from datetime import datetime, timezone, timedelta

logs_dir = os.path.expanduser(r"~\Newry Corp\Clients - Claude Master Working Folder\logs")
cutoff = datetime.now(timezone.utc) - timedelta(days=30)
usage = {}  # plugin → {users: set, runs: int, last_run: str|None}

for f in glob.glob(os.path.join(logs_dir, "usage-log-*.jsonl")):
    with open(f) as fh:
        for line in fh:
            try:
                e = json.loads(line)
                ts = datetime.fromisoformat(e["ts"].replace("Z", "+00:00"))
                if ts < cutoff: continue
                p = e.get("plugin", "unknown")
                if p not in usage: usage[p] = {"users": set(), "runs": 0, "last_run": None}
                usage[p]["users"].add(e.get("user_id", ""))
                usage[p]["runs"] += 1
                if not usage[p]["last_run"] or e["ts"] > usage[p]["last_run"]:
                    usage[p]["last_run"] = e["ts"]
            except: pass
```

If the logs folder doesn't exist or no files are found, set `usage = {}` and show "No data yet" for all plugins. Do not surface an error.

Render the plugin summary with expandable cards and status badges:
- **Active** → green badge
- **In progress** → amber badge
- **Maintainer tool** → gray badge

Show: Name | Version | Status | Audience. Include pending notes where present.

**Inside each expanded card**, add a **Usage (30d)** field showing the three metrics inline:
`Active users: N · Runs: N · Last run: YYYY-MM-DD` (or `—` if no data).
Use `usage.get(plugin_snake_case_name, {})` to look up each plugin. Plugin name keys match the `plugin` field in the log entries (e.g. `newry_knowledge`, `primary_research_toolkit`, `sof_toolkit`).

### 4. Milestones
Three milestones as a horizontal timeline:
- Date | Target | Signal
- Mark as Upcoming / Passed based on today's date

### 5. Recent decisions
Last 5 decisions, compact: date · title · one-sentence summary.
Expandable to show alternatives considered and rationale.

---

## Create or update artifact

Check whether the artifact already exists:
```
list_artifacts() → look for name "newry_operator_dashboard"
```

- If it doesn't exist: call `create_artifact` with the generated HTML.
- If it exists: call `update_artifact` with the refreshed HTML.

Artifact metadata:
- **name:** `newry_operator_dashboard`
- **title:** "Newry AI Program — Operator Dashboard"

---

## Output to operator

After creating/updating:

> "Dashboard [created/refreshed]. Plugin data from [source], decisions from [GitHub/bundled].
> Re-run 'show the dashboard' to refresh."

Do not display the full artifact content in chat — it's visible in the sidebar.
