---
name: plugin-builder
description: Use this skill whenever a Newry plugin needs to be packaged into a .plugin file for Cowork installation. Triggers on "package this plugin," "build the plugin file," "repackage," "create the .plugin," or any request to turn a plugin folder into an installable file. Maintainer-facing — not consultant-facing.
---

# Plugin Builder

Packages a Newry plugin folder into a correctly structured `.plugin` file for Cowork installation.

---

## Required .plugin structure

The Cowork installer requires this exact layout — missing directory entries or a malformed plugin.json will cause installation to fail:

```
.claude-plugin/             ← explicit directory entry required
.claude-plugin/plugin.json  ← metadata (see fields below)
skills/                     ← explicit directory entry required
skills/<plugin-name>/       ← explicit directory entry required
skills/<plugin-name>/SKILL.md
skills/<plugin-name>/sub-skills/...
skills/<plugin-name>/scripts/...
skills/<plugin-name>/references/...
README.md                   ← at zip root; use overview.md as source if present
```

All intermediate subdirectories also need explicit directory entries in the zip.

## plugin.json fields

```json
{
  "name": "<from SKILL.md frontmatter name field>",
  "version": "<see versioning below>",
  "description": "<from SKILL.md frontmatter description field>",
  "author": { "name": "Sylvan Shank" },
  "repository": "https://github.com/Newry-LLC/newry-ai-tools"
}
```

## Versioning

- If a `.plugin` already exists in `outputs/`, read its current version and bump the patch number (e.g. 1.1.0 → 1.1.1)
- If no prior version exists, start at 1.0.0

## What to include

Include SKILL.md files, scripts, and reference files the skill needs to run. Use judgment to exclude anything that's internal to development — logs, design notes, decisions docs, deprecated sub-skills, build artifacts, `__pycache__`, `.pyc` files.

---

## Pre-packaging checklist

Before building, verify the coordinator SKILL.md contains both required logging blocks. If either is missing, add it before proceeding — do not package without them.

**1. Usage logging** — must appear near the top of the coordinator SKILL.md, before the routing section:

```markdown
## Usage logging

At the start of every run — before any other work — create one record in the Airtable Plugin Usage Log. Silent and automatic; no user-facing output.

- **Base ID:** `appRawPuacfAvVH2Z` | **Table ID:** `tblmACtwIClniGn5n`
- **Tool:** `create_records_for_table`
- **Fields:**
  - `fldRrr3BkrJW8rE3L` (ts) — current UTC time, ISO 8601 (e.g. `2026-05-26T14:30:00Z`)
  - `fldNHK285dPCOdNhB` (plugin) — `"<plugin_name>"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — whichever sub-skill is being invoked; use `"general"` if routing hasn't resolved yet
  - `fldmTXyfFZRpbZEvQ` (user_id) — read `~/.user_id` if it exists; otherwise `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — project code if discernible; otherwise `""`

If the write fails for any reason, continue silently.
```

**2. Feedback capture** — coordinator SKILL.md must reference the shared sub-skill:

```markdown
## Feedback capture

Applies across all sub-skills. Read and follow the shared feedback-capture sub-skill:
`../feedback-capture/SKILL.md`

When logging:
- `Plugin:` → `<plugin-name>`
- `Sub-skill:` → whichever sub-skill is active; use `general` if none
```

If either block is missing, add it with the correct plugin name substituted in, then continue with packaging.

---

## How to build

Write and execute a short Python script using the `zipfile` module. Key requirement: write explicit `ZipInfo` directory entries for every directory in the archive before adding files — the Cowork installer requires them.

Output to `outputs/<plugin-name>.plugin`. Report the final file list and size.

---

## After packaging

- Clean up any temp files left in `outputs/` by the zipfile module — delete any files that
  do not end in `.plugin` or `.html`. Run as part of the packaging script:
  ```python
  import os
  outputs_dir = os.path.join(base, "outputs")
  for f in os.listdir(outputs_dir):
      if not f.endswith(".plugin") and not f.endswith(".html"):
          os.remove(os.path.join(outputs_dir, f))
  ```
- If a prior version is installed in Cowork, the user must uninstall it before installing the new one
- **To push to GitHub**, tell Sylvan:

  > "Plugins are packaged. Switch to Claude Code and run from the `Building Tools for Newry` folder:
  > - **Windows:** `PYTHONIOENCODING=utf-8 "C:/Users/sshank/AppData/Local/Programs/Python/Python314/python.exe" "strategy/push-plugins.py"`
  > - **Mac/Linux:** `python3 "strategy/push-plugins.py"`
  > This pushes all plugins in `outputs/` to `Newry-LLC/newry-ai-tools`.
  > Auto-sync will distribute the updates to all users on their next Cowork session."

  The push script reads the PAT from `strategy/.github-token` and handles all plugins automatically — no changes needed when new plugins are added.


---

## Feedback capture

Apply the shared feedback-capture sub-skill: `plugins/feedback-capture/SKILL.md`.

Set `Plugin: plugin-builder` and `Sub-skill: plugin-builder` in the log entry.
