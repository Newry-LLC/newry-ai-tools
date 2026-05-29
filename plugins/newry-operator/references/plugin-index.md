# Newry AI Plugin Index

**Last updated:** 2026-05-27
**Purpose:** Reference for program maintainers and successors. Covers all active plugins and standalone skills — what they do, what they log, what training materials exist, and distribution status.

---

## Summary table

| Plugin | Version | Type | Status | Audience |
|--------|---------|------|--------|----------|
| Primary Research Toolkit | 1.3.12 | Packaged plugin | Active | Consultants |
| SoF Toolkit | 1.0.9 | Packaged plugin | Active | Consultants |
| newry-knowledge | 1.1.33 | Packaged plugin | Active | Consultants |
| newry-operator | 1.0.8 | Packaged plugin | Active | Program builders |
| Project Technical Onboarding | 0.1.8 | Packaged plugin | In progress | Consultants |
| Project Launch Toolkit | — | Packaged plugin | In progress | Consultants |
| RMA-OA Builder | 1.0.1 | Packaged plugin | In progress | Consultants |
| Plugin Auditor | 1.0.0 | Packaged plugin | Active | Maintainers |
| Plugin Builder | 1.0.0 | Packaged plugin | Active | Maintainers |
| Synthesis QA | — | Standalone skill | Active | Maintainers |
| log-reader | — | Standalone skill | Active | Maintainers |
| feedback-capture | — | Shared sub-skill | Active | Internal (called by coordinators) |
| project-setup | — | Shared sub-skill | Active | Internal (called by file-writing skills) |

---

## Distribution model

Plugins are distributed via Cowork Org Settings → Plugins. Matt (org owner) installs from `.plugin` files stored in `outputs/` and on GitHub (`Newry-LLC/newry-ai-tools`).

**Auto-update:** GitHub repo (`Newry-LLC/newry-ai-tools`) is connected as the plugin source with "Sync automatically" enabled. Updates auto-propagate to all users on their next session after a push to GitHub. All plugins are on auto-sync.

**To push updates:** Switch to Claude Code and run from the `Building Tools for Newry` folder:
- **Windows:** `PYTHONIOENCODING=utf-8 "C:/Users/sshank/AppData/Local/Programs/Python/Python314/python.exe" "strategy/push-plugins.py"`
- **Mac/Linux:** `python3 "strategy/push-plugins.py"`

The script pushes all `.plugin` files in `outputs/` automatically — no changes needed as new plugins are added. PAT stored at `strategy/.github-token`.

**Installation preferences per plugin:**
- `newry-knowledge` — default install (all users get it automatically)
- `primary-research-toolkit` — available (self-service; not everyone does primary research)
- `sof-toolkit` — available (relevant to consultants working on SoF slides)
- `plugin-auditor`, `plugin-builder`, `newry-operator` — maintainers only

---

## Central logs

**Usage logging — all plugins:** Airtable — Base `appRawPuacfAvVH2Z`, Table `tblmACtwIClniGn5n` (Plugin Usage Log)
Schema: `{ts, plugin, sub_skill, user_id, project}`. Written via `create_records_for_table` at the start of every run. `user_id` read from `~/.user_id` if present; otherwise `"unknown"`. Readable by log-reader skill and operator dashboard via `list_records_for_table`.

**Feedback logging — all plugins:** Airtable — Base `appRawPuacfAvVH2Z`, Table `tbl8xVn3ZbUcWCmUY` (Plugin Feedback Log)
Schema: `{ts, plugin, sub_skill, user_id, signal_type, severity, users_words, what_was_happening, output, notes, status}`. Written via shared feedback-capture sub-skill on positive/negative signals. Draft-confirm pattern before writing.

**Per-project local logs (PRT only):**
- `logs/synthesis-log.md` — run details per ICS synthesis (project-scoped)

---

## Plugin detail

### Primary Research Toolkit (PRT)
**Version:** 1.3.12
**File:** `outputs/primary-research-toolkit.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Supports the full primary research workflow from planning through synthesis. Six active sub-skills covering every stage of an interview-based research engagement.

**Sub-skills (6 active):**
- Research Plan Design — prioritize branches, set target N, plan sourcing
- Interview Guide Design — convert branches into structured guides by interviewee type
- Interview Acquisition — draft outreach and expert network briefs; manage pipeline
- Interview Prep — customized guide per confirmed interviewee with corpus-informed probes
- Interview Coding & Synthesis (ICS) — code transcripts; synthesize findings; produce roll-up
- Corpus Query — query the coded corpus by topic, person, segment, or branch

*Note: A `coverage-gap-analysis` sub-skill exists in the source folder but is deprecated — absorbed into ICS Mode 2 (2026-05-04). Not active.*

**Bundled reference files:**
- `references/primary-research-onboarding.md` — verbatim extraction of `202504 Primary Research Onboarding.pptx`; covers full interview workflow from sourcing through synthesis/coding
- `references/interviewee-segmentation.md` — segmentation framework

**Training materials (SharePoint — for user access; not bundled):**
- Primary onboarding deck (revised May 2025): [202504 Primary Research Onboarding.pptx](https://newrycorp.sharepoint.com/clients/Shared Documents/Consulting Resources/People & Recruiting/On Boarding Materials/The Newry Way 2025 revisions/202504 Primary Research Onboarding.pptx)
- Qualitative Research Series KNs: SharePoint > Consulting Resources > Knowledge Nuggets > Qualitative Research Series
- Folder structure diagram (`PRT Folder Structure.html`) — also bundled in plugin
- 6-slide Cowork onboarding deck: [PRT and Newry Knowledge Claude Tools 5.12.26.pptx](https://newrycorp.sharepoint.com/clients/Shared%20Documents/Consulting%20Resources/Knowledge%20Nuggets/Nuggets/AI%20and%20LLMs%202026/PRT%20and%20Newry%20Knowledge%20Claude%20Tools%205.12.26.pptx) — SharePoint > Consulting Resources > Knowledge Nuggets > AI and LLMs 2026
- Architecture diagram (`PRT Architecture.pptx`) — Building Tools for Newry folder

**Scripts bundled:**
- `preprocess.py` — transcript preprocessing and quality assessment
- `term_reconcile.py` — speaker label reconciliation
- `style_docx.py` — output document styling

**Key dependencies:** SharePoint working folder (`Claude Working Folder - [Project Code]`) must be set up before first run. M365 connector required.

**Notes:** Tested end-to-end on ALTA01 (55-card corpus). Non-Alta corpus validation pending.

---

### SoF Toolkit
**Version:** 1.0.9
**File:** `outputs/sof-toolkit.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Evaluates, aligns, and drafts Summary of Findings (SoF) slides using the Pyramid Principle as the evaluative standard.

**Modes:**
- Evaluate — score an existing SoF against the Pyramid Principle; identify structural and quality issues
- Align — check whether a SoF matches the supporting deck content
- Draft — produce a SoF from source findings or a deck

**References bundled:** `references/universal-standards.md` — Newry quality standards applied across all modes.

**Training materials (SharePoint — for user access; not bundled):**
- Pyramid Principle 2026 deck: [Pyramid Principle 2026.pptx](https://newrycorp.sharepoint.com/clients/Shared%20Documents/Consulting%20Resources/TOOLS-TRAINING/Pyramid%20Principle/Pyramid%20Principle%202026.pptx) — SharePoint > Consulting Resources > TOOLS-TRAINING > Pyramid Principle

**Notes:** Tested on Glass Core (multiple runs) and Alta (1 Draft run, 2026-04-30). PPTX annotation feature designed but not built (V1 backlog).

---

### newry-knowledge
**Version:** 1.1.33
**File:** `outputs/newry-knowledge.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Firm-wide knowledge search across Newry's SharePoint and Airtable. Answers questions about project history, client contacts, staff expertise, institutional learnings, and any document content on SharePoint.

**Sub-skills:**
- newry-knowledge (coordinator) — classifies questions, routes to the right source(s), assesses richness, synthesizes a combined answer; single entry point
- sharepoint-search — search SharePoint for project materials, internal resources, templates, research, and any firm content
- airtable-search — search Airtable for project metadata, AER learnings, client contacts, and staff expertise

**Training materials (SharePoint — for user access; not bundled):**
- Onboarding deck (covers both PRT and newry-knowledge, slides 5–6): [PRT and Newry Knowledge Claude Tools 5.12.26.pptx](https://newrycorp.sharepoint.com/clients/Shared%20Documents/Consulting%20Resources/Knowledge%20Nuggets/Nuggets/AI%20and%20LLMs%202026/PRT%20and%20Newry%20Knowledge%20Claude%20Tools%205.12.26.pptx) — SharePoint > Consulting Resources > Knowledge Nuggets > AI and LLMs 2026

**Key dependencies:** M365 connector (for SharePoint) and Airtable connector must be connected in Cowork settings. Not bundled — users connect individually.

**Notes:** Demo questions confirmed: Q1 (Newry Ladder PM expectations), Q3 (Alta competitors AOC/Reichhold). Trigger tests (20 cases) in `evals/trigger-tests.json` — not yet run.

---

### Project Technical Onboarding
**Version:** 0.1.8
**File:** `outputs/project-technical-onboarding.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Guides a consultant through building a Technical Orientation document in week 1 of any engagement. Structured interview + docx artifact output. Calibrates Claude to the client's technology, value creation logic, and competitive position before strategic analysis begins.

**Sub-skills:**
- technical-orientation — structured intake interview → 4-section Technical Orientation doc (Product & Technology / Value Creation / Value Capture / Key Engagement Questions)

**Key dependencies:** SharePoint working folder required. M365 connector required. Minimum inputs: SOW/proposal + client website.

**Status / pending:**
- Evals run on v0.1.5 (3 scenarios, 100% pass with skill / 50% without) — 4-section structure not yet evaluated
- Eval viewer (`eval-review-technical-orientation.html`) needs human review
- Plugin 2 (training module) not yet built

---

### RMA-OA Builder
**Version:** 1.0.1
**File:** `outputs/rma-oa-builder.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Guides a consultant through designing and building a Rapid Market Assessment (RMA) or Opportunity Assessment — from intake and scoping through secondary research and section drafting, with a defined handoff to PRT when primary research is needed.

**Sub-skills:**
- rma-oa-builder — Phase 1: intake → tier recommendation → RMA Design Document; Phase 2: section-by-section secondary research → check-in → PRT handoff → docx assembly

**Canonical sections:** Market / Customers / Competitive Landscape / Client Fit / Path to Market & Risks

**Tiers:** Scoping / Standard / Full (recommended based on intake)

**Status / pending:** SKILL.md written (both phases). Pending: Plugin Auditor pass → vetting.

---

### newry-operator
**Version:** 1.0.8
**File:** `outputs/newry-operator.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Operator plugin for anyone building or stewarding the Newry AI program. Design advisor, decision logger, build prioritization, quality review, and program dashboard — in one plugin.

**Sub-skills (6):**
- newry-operator (coordinator) — gate + routing
- program-advisor — applies principles + decision history to advise on architecture/design
- decision-capture — structured intake → appends to decision-log.md → repackages → git push
- build-prioritization — scored recommendation on what to build next (reads program-status.md live)
- plugin-reviewer — Plugin Auditor three-pass quality review before shipping
- operator-dashboard — creates/refreshes the `newry-operator-dashboard` Cowork artifact

**Bundled reference files:**
- `references/principles.md` — 15 design principles
- `references/north-star.md` — north star statement + milestones
- `references/vision.md` — May 2027 end state
- `references/plugin-index.md` — plugin registry (bundled at packaging time; portable cross-machine)
- `references/decision-log.md` — program decisions (bundled; updated via decision-capture skill)

**Live files (read at runtime):**
- `strategy/decision-log.md` — preferred over bundled copy when accessible
- `strategy/program-status.md` — read by build-prioritization

**Artifact:** `newry-operator-dashboard` — persistent Cowork sidebar showing plugins (expandable), milestones, recent decisions. Refresh by saying "show the dashboard."

---

### Plugin Auditor
**Version:** 1.0.0
**File:** `outputs/plugin-auditor.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Reviews any Newry plugin for quality across three passes: design (P2/P4/P5/P8/P12 principles), implementation (completeness/consistency/executability/edge cases/calibration/output spec), and token efficiency. Produces a report and walks through changes one by one.

**When to use:** Before shipping any new plugin or after a major change.

---

### Plugin Builder
**Version:** 1.0.0
**File:** `outputs/plugin-builder.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Packages a plugin folder into a correctly structured `.plugin` file for Cowork installation. Handles versioning, directory entries, plugin.json, and file selection.

**When to use:** Any time a plugin is ready for repackaging after changes.

---

### Project Launch Toolkit (PLT)
**Version:** — (not yet packaged) | **Source:** `plugins/project-launch-toolkit/`

**What it does:** Guides a consultant through the project launch phase — from problem statement and issue tree through value creation hypothesis, workplan, and client account management setup.

**Sub-skills (7 built, no coordinator yet):**
- problem-statement, issue-tree, value-creation, individual-value-creation-goals, workplan, fact-finding, account-management

**Status / pending:** All 7 sub-skills built. Missing: coordinator SKILL.md. Scored highest in skills prioritization matrix.

---

## Standalone skills (maintainer-facing, not yet packaged)

### Synthesis QA
**Location:** `plugins/synthesis-qa/SKILL.md`

Quality review of synthesis outputs (roll-ups, summary cards, analytical documents) across four checks: pyramid test, quantitative precision, plain language, headline/evidence consistency.

---

### Log Reader
**Location:** `plugins/log-reader/SKILL.md`

Reads and summarizes the central usage and feedback logs from Airtable. Computes active users (30d) and run counts (30d) per plugin.

---

## Shared sub-skills

### feedback-capture
**Location:** `plugins/feedback-capture/SKILL.md`
**Bundled into:** all packaged plugins

Canonical feedback capture behavior. Each plugin coordinator references this file. Captures positive and negative signals via draft-confirm-log pattern. Writes to Airtable Plugin Feedback Log (Base `appRawPuacfAvVH2Z`, Table `tbl8xVn3ZbUcWCmUY`).

---

### project-setup
**Location:** `plugins/project-setup/SKILL.md`
**Bundled into:** PRT, Project Technical Onboarding, RMA-OA Builder

Shared Step 0 block for all file-writing skills. Verifies project folder, establishes project identity, creates subfolders, generates `project.md`. Supports full mode (SharePoint-connected) and informal mode (local only).

---

## Open items / backlog

- **PLT coordinator** — 7 sub-skills built; missing coordinator SKILL.md. Next build priority.
- **RMA-OA Builder** — pending Plugin Auditor pass → vetting
- **Project Technical Onboarding** — 4-section structure not evaluated; Plugin 2 not built; eval viewer needs review
- **newry-knowledge trigger tests** — 20 cases in `evals/trigger-tests.json`; not yet run
- **PRT non-Alta corpus validation** — waiting for suitable in-flight project
- **user_id provisioning** — all usage/feedback logs show `"unknown"` until `~/.user_id` is provisioned in Cowork onboarding
