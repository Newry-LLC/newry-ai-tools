---
name: tool-directory
description: >
  Show the Newry AI Tools directory — a consultant-facing guide to what AI tools are
  available at Newry, what they do, and how to use them. Use whenever someone is asking
  about Newry's AI capabilities, tools, or plugins — regardless of exact phrasing. The
  question might reference "tools", "plugins", "Claude features", "what the AI program
  offers", or ask which tool to use for a specific task. Creates a persistent artifact
  in the Cowork sidebar with expandable cards organized by task type.
---

# Tool Directory

Produces a consultant-facing directory of available Newry AI tools as a Cowork artifact.

**SKILL_VERSION: 1.3** — bump this (and the matching `<div id="skill-version">` in
`directory.html`) when tool content changes. That is the only edit needed for a refresh.

**HTML source:** `directory.html` in this skill's directory (same folder as this SKILL.md).
The skill system prints the base directory path at load time — use it to construct the full
path: `{base_directory}/directory.html`.

---

## Steps

### Step 0 — Respond immediately with a text summary

Before touching any artifact tools, output this table in the chat now so the user has the answer instantly:

---

**4 tools available · 2 more coming soon**

| Tool | What it does | Setup needed? |
|---|---|---|
| **newry-knowledge** | Search SharePoint docs + Airtable — project history, contacts, expertise, any Newry document | M365 + Airtable connectors |
| **Primary Research Toolkit** | Plan, guide, prep, code, and synthesize interview-based primary research end-to-end | M365 + SharePoint working folder |
| **SoF Toolkit** | Evaluate, align, or draft the content for a Summary of Findings slide against the Pyramid Principle | None — works immediately |
| **Project Launch Toolkit** | Full project launch flow — problem statement, issue tree, value creation, workplan, ownership & goals, stakeholder plan | Airtable connector |

*Coming soon: RMA-OA Builder · Project Technical Onboarding*

Full details with example phrases and training links are in the artifact (loading now…).

---

Then proceed to Step 1.

### Step 1 — Check for existing artifact and version

Call `list_artifacts`. Look for id `newry-tool-directory`.

**If NOT found:** proceed to Step 2 to create it.

**If found:**
- Read the artifact file at the `path` returned by `list_artifacts`
- Find `<div id="skill-version" style="display:none">` and extract the version string
- Compare to `SKILL_VERSION` above (`1.3`)
- **If versions match:** proceed to Step 2 (call `update_artifact` to surface the artifact panel — a link alone does not open it).
- **If versions differ (or version tag missing):** proceed to Step 2.

### Step 2 — Pass the static HTML file to the artifact tool

Read `{base_directory}/directory.html` (the base directory was printed at skill load time).
Pass that absolute path directly to `create_artifact` or `update_artifact` — no rewriting needed.

Artifact metadata:
- **id:** `newry-tool-directory`
- **description:** "Consultant-facing directory of available Newry AI tools — organized by task type. What to use, when, and exactly what to say."
- **update_summary** (if updating): "Tool directory refreshed to v1.1."

### Step 3 — Surface the artifact link

Add a single line after the artifact loads:

"Expanded details in the [Newry tools directory](artifact://newry-tool-directory) — also accessible any time from the Live Artifacts link in the left sidebar."
