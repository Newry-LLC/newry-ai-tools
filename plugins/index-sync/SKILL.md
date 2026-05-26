---
name: index-sync
description: >
  Maintainer skill — audit the plugin folder against plugin-index.md and flag any drift.
  Use when you suspect the index is out of date, at session close after plugin work, or
  any time you want to verify the index is accurate. Triggers on "sync the index",
  "check the index", "is the index up to date", "audit plugins vs index", or as part of
  the session close ritual after plugin work. Not consultant-facing.
---

# Index Sync

A maintainer skill that reads the actual state of the `plugins/` folder and compares it
against `strategy/plugin-index.md`. Reports discrepancies without making changes — the
maintainer decides what to update.

---

## What to check

For each subfolder under `plugins/`, verify:

1. **Present in index?** — Is the plugin listed in the summary table?
2. **Version match** — If a `plugin.json` or `.claude-plugin/plugin.json` exists, does the version in the index match?
3. **Sub-skill count** — Count active sub-skills (exclude any marked deprecated in their SKILL.md). Does the index description match?
4. **Status accuracy** — Does the index status (Active / In progress) reflect reality? A plugin with no `plugin.json` and no `.plugin` file in `outputs/` is not yet packaged — verify status is "In progress."
5. **Logs section** — Does the SKILL.md have a Usage logging section writing to `usage-log-<user_id>.jsonl` (per-consultant, path constructed from `~/.user_id`)? Flag any plugin missing this or still using the old single-file `usage-log.jsonl` path.
6. **New folders not in index** — Any plugin folder with a SKILL.md that has no entry in the index at all.

Also check:
- Any entry in the index that has **no corresponding folder** in `plugins/` — stale entry.
- Any version number in the index that doesn't match the packaged `.plugin` file in `outputs/` (if one exists).

---

## How to run

1. List all subfolders under `plugins/` using Bash.
2. For each folder, check for `SKILL.md`, `plugin.json`, `.claude-plugin/plugin.json`, and sub-skills.
3. Read the summary table from `strategy/plugin-index.md`.
4. Cross-reference. Build a discrepancy report.

---

## Output format

Report as two sections:

**Clean** — plugins where index matches reality (one line each: name + version or "—").

**Discrepancies** — one entry per issue:
- `[folder name]` — what the index says vs. what's actually there
- Severity: HIGH (missing from index entirely, or wrong status) / MEDIUM (version mismatch, sub-skill count off) / LOW (minor description drift)

If no discrepancies: "Index is clean as of [date]."

At the end, ask: "Want me to fix any of these?"

---

## When to run

- At session close, if any plugin work happened that session
- Any time the index feels stale
- After a Plugin Builder run (as a verification step)

Do not make changes during the sync — report only. Changes go through the normal plugin dev process.
