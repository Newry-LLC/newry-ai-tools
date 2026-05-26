---
name: log-reader
description: Maintainer skill — read and summarize the central usage log and feedback log for the Newry AI program. Use when a program maintainer asks for plugin usage metrics, active users, run counts, or a feedback summary. Not consultant-facing.
---

# Log Reader

A maintainer-facing skill for querying the Newry AI program's central usage log. Produces per-plugin metrics and optionally surfaces a feedback log summary. No preamble — output is the table and a timestamp line.

**Audience:** program maintainers (Sylvan, Matt, successors). Not for consultant use.

---

## Data sources

- **Usage logs:** Airtable — Base `appRawPuacfAvVH2Z`, Table `tblmACtwIClniGn5n` (Plugin Usage Log)
  - One record per skill run
  - Fields: `fldRrr3BkrJW8rE3L` (ts, ISO 8601), `fldNHK285dPCOdNhB` (plugin, snake_case singleSelect), `fld4EyuVEhxAhPZEd` (sub_skill), `fldmTXyfFZRpbZEvQ` (user_id, anonymous UUID), `fldu8rvXDfvi2O3jF` (project, code or empty)
  - Fetch via `list_records_for_table`; paginate with `cursor` if response includes `nextCursor`

- **Feedback logs:** `~\Newry Corp\Clients - Claude Master Working Folder\logs\feedback-log-*.md`
  - One file per consultant; glob all matching files and aggregate
  - Markdown; structured entries per the feedback-capture schema

---

## Default run: usage metrics table

Call `list_records_for_table` with `baseId: appRawPuacfAvVH2Z`, `tableId: tblmACtwIClniGn5n`, `pageSize: 8000`. Paginate if needed. Filter to records where `ts` ≥ today minus 30 days. Compute metrics per plugin.

**Per-plugin metrics:**
- **Active users (30d)** — count of distinct `user_id` values across records in the window
- **Runs (30d)** — count of records in the window
- **Last run** — most recent `ts` value for that plugin (formatted as `YYYY-MM-DD HH:MM UTC`)

**Output format — no preamble, just the table:**

```
Plugin                   | Active Users (30d) | Runs (30d) | Last Run
-------------------------|-------------------|------------|------------------
newry_knowledge          | 3                 | 47         | 2026-05-12 14:22 UTC
primary_research_toolkit | 2                 | 18         | 2026-05-11 09:05 UTC
sof_toolkit              | 1                 | 6          | 2026-05-10 16:44 UTC
rma_oa_builder           | 1                 | 3          | 2026-05-08 11:30 UTC
```

Sort by Runs (30d) descending. Include all plugins that appear in the log — do not hard-code the plugin list.

Then output a single timestamp line:

```
Generated: 2026-05-13 10:30 UTC
```

---

## Optional: filter by plugin or date range

If the user specifies a plugin name or date range, apply the filter before computing metrics.

- **Plugin filter** — match on the `plugin` field (exact or partial, case-insensitive). Show only matching rows.
- **Date range** — override the default 30-day window with the specified range. Accept natural language ("last 7 days", "April 2026", "since May 1").

If both are specified, apply both filters.

---

## Optional: sub-skill breakdown

If the user asks for a breakdown by sub-skill, add a second table below the plugin-level summary:

```
Plugin                   | Sub-skill          | Runs (30d) | Last Run
-------------------------|--------------------|------------|------------------
newry_knowledge          | sharepoint_search  | 31         | 2026-05-12 14:22 UTC
newry_knowledge          | airtable_search    | 16         | 2026-05-11 08:50 UTC
primary_research_toolkit | ics                | 12         | 2026-05-11 09:05 UTC
...
```

---

## Optional: feedback log summary

If the user asks for a feedback summary, glob all `feedback-log-*.md` files in the logs folder, read and concatenate all entries, then produce:

**Feedback summary — [date range or "all time"]**

```
Open items: N
By classification: bug (N), friction (N), quality (N), feature (N), question (N)
By severity: high (N), medium (N), low (N)
```

Then list open high- and medium-severity items:

```
High severity (open):
- [Date] [Plugin/skill] — [What went wrong, one line]

Medium severity (open):
- [Date] [Plugin/skill] — [What went wrong, one line]
```

Low-severity and closed items are omitted from the summary unless the user asks for them.

---

## Error handling

- If the Airtable query returns no records or fails, output: `No usage data found. Logs may not have been written yet, or the Airtable connector may not be connected.`
- If a line fails to parse as JSON, skip it silently and continue.
- If no `feedback-log-*.md` files are found, output: `Feedback logs not found — skipping feedback summary.`
- Do not surface parsing errors or stack traces to the user.
