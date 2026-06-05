---
name: decision-capture
description: >
  Log a design decision to the program decision log. Structured intake: what was decided,
  alternatives considered, rationale. Writes to a per-contributor file, then regenerates
  the merged canonical snapshot — no GitHub API or PAT required.
---

# Decision Capture

Structured intake for logging a program design decision. Uses per-contributor files to
eliminate SharePoint sync conflicts when multiple operators work on separate machines.

**Write path:**
- New entry appended to `logs\newry-operator\decision-log-<user_id>.md`
  (in the shared SharePoint logs folder — one file per operator)

**Merge path (runs after every write):**
- All `logs\newry-operator\decision-log-*.md` files merged and sorted by date (descending)
- Merged result written to `logs\newry-operator\decision-log.md` — the live canonical snapshot
- Same content written to `plugins/newry-operator/references/decision-log.md` — bundled
  fallback for when the logs folder isn't synced

All other skills (program-advisor, build-prioritization, operator-dashboard) read from
`logs\newry-operator\decision-log.md` first, falling back to the bundled reference.

This skill is also triggered automatically at the close of `program-advisor` and
`build-prioritization` when a decision has been reached.

---

## Step 1 — Intake

Collect three things. If handed off from `program-advisor` or `build-prioritization` with
context already established, extract them from that context — do not re-ask.

- **What was decided** — the outcome in one sentence
- **Alternatives considered** — what else was on the table (brief)
- **Rationale** — why this option

If any of the three is missing or unclear, ask for it specifically before proceeding.

---

## Step 2 — Format entry

Format the entry as:

```
## YYYY-MM-DD · decision title — 5–8 words, lowercase

**Decided:** [one sentence]
**Alternatives considered:** [brief list or sentence]
**Rationale:** [why this option — 1–3 sentences]

---
```

Show the formatted entry to the operator and ask: "Does this look right?"
Do not proceed to Step 3 until confirmed.

---

## Step 3 — Check for near-duplicate

Read `~\Newry Corp\Clients - Claude Master Working Folder\logs\newry-operator\decision-log.md`
(the merged canonical file). Fall back to bundled `references/decision-log.md` if not synced.
Scan the last 10 entries.
If a near-match exists — same topic, similar outcome — surface it:

> "A similar decision was logged on [date]: [title]. Still want to log this separately?"

Proceed only if confirmed.

---

## Step 4 — Write and merge

All file operations are silent — only report the final result.

**a) Resolve user_id**

Use the user's email address from the session context (available in the system prompt `<user>` block) as the user_id. Same value used for usage logs.

**b) Seed per-contributor file if first run**

Logs folder: `~\Newry Corp\Clients - Claude Master Working Folder\logs\newry-operator\`

Check whether `decision-log-<user_id>.md` exists in that folder.

If it does not: this operator's first capture. Seed from the existing
`logs\newry-operator\decision-log.md` if it exists (migrates prior entries). Otherwise
initialize with the standard header only.

**c) Prepend new entry**

Read `logs\newry-operator\decision-log-<user_id>.md`. Insert the new entry immediately
after the file header (after the `---` separator). Most recent first. Write back.

**d) Merge all contributors**

Run the following to regenerate the canonical snapshot:

```python
import os, re, glob

logs_dir = os.path.expanduser(
    r"~\Newry Corp\Clients - Claude Master Working Folder\logs\newry-operator"
)
# Also find the bundled reference path relative to the working folder
# (working folder = Building Tools for Newry, mounted in Cowork)
working_dir = # resolved by Cowork — same root as project-setup

HEADER = """# Decision Log — Newry AI Program

Running log of design decisions. Each entry captures what was decided, alternatives
considered, and the rationale. Maintained by the program team; updated via the
decision-capture skill.

---
"""

entries = []
for f in glob.glob(os.path.join(logs_dir, "decision-log-*.md")):
    content = open(f, encoding="utf-8").read()
    for block in re.split(r'\n(?=## \d{4}-\d{2}-\d{2})', content):
        block = block.strip()
        if re.match(r'## \d{4}-\d{2}-\d{2}', block):
            entries.append(block)

# Deduplicate by first line (same date+title = same entry)
seen = set()
unique = []
for e in entries:
    key = e.splitlines()[0].strip()
    if key not in seen:
        seen.add(key)
        unique.append(e)

unique.sort(key=lambda e: re.match(r'## (\d{4}-\d{2}-\d{2})', e).group(1), reverse=True)

merged = HEADER + "\n\n---\n\n".join(unique) + "\n"

# Write live canonical snapshot
open(os.path.join(logs_dir, "decision-log.md"), "w", encoding="utf-8").write(merged)

# Write bundled reference (fallback for when logs folder not synced)
ref_path = os.path.join(working_dir, "plugins", "newry-operator", "references", "decision-log.md")
open(ref_path, "w", encoding="utf-8").write(merged)

print("Merge complete —", len(unique), "entries")
```

**e) Report result**

- Success: "Decision logged."
- Failure: "Write failed — [reason]. Decision not saved."

---

## Notes

- One decision per run. If the operator wants to log multiple decisions, run separately.
- Per-contributor files (`logs\newry-operator\decision-log-<user_id>.md`) are the source of record.
  `logs\newry-operator\decision-log.md` is a generated artifact — never edit it directly.
- Deduplication in the merge step uses the first line (date + title) as the key —
  safe to re-run merge without duplicating entries.
- Distribution to all operators happens on the next GitHub push via the packaging cycle.
- Usage logging: write a standard entry to the usage log at the start of the run.
  Path: `$HOME/Newry Corp/Clients - Claude Master Working Folder/logs/usage-log-<user_id>.jsonl`
  Schema: `{"ts", "plugin": "newry-operator", "sub_skill": "decision-capture", "user_id", "project": "program"}`.
  Source `user_id` from the session context email (system prompt `<user>` block); if not available, use `"unknown"`. Fail silently.
