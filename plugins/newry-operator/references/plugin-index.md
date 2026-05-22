# Newry AI Plugin Index

**Last updated:** 2026-05-18
**Purpose:** Reference for program maintainers and successors. Covers all active plugins and standalone skills — what they do, what they log, what training materials exist, and distribution status.

---

## Summary table

| Plugin | Version | Type | Status | Audience |
|--------|---------|------|--------|----------|
| Primary Research Toolkit | 1.3.8 | Packaged plugin | Active | Consultants |
| SoF Toolkit | 1.0.3 | Packaged plugin | Active | Consultants |
| newry-knowledge | 1.1.14 | Packaged plugin | Active | Consultants |
| Project Technical Onboarding | 0.1.6 | Packaged plugin | In progress | Consultants |
| Project Launch Toolkit | — | Packaged plugin | In progress | Consultants |
| RMA-OA Builder | — | Packaged plugin | In progress | Consultants |
| Plugin Auditor | — | Standalone skill | Active | Maintainers |
| Plugin Builder | — | Standalone skill | Active | Maintainers |
| Synthesis QA | — | Standalone skill | Active | Maintainers |
| log-reader | — | Standalone skill | Active | Maintainers |
| feedback-capture | — | Shared sub-skill | Active | Internal (called by coordinators) |
| project-setup | — | Shared sub-skill | Active | Internal (called by file-writing skills) |

---

## Distribution model

Plugins are distributed via Cowork Org Settings → Plugins. Matt (org owner) installs from `.plugin` files stored in `outputs/` and on GitHub (`Newry-LLC/newry-ai-tools`).

**Auto-update:** If the GitHub repo is connected as a plugin source and "Sync automatically" is enabled in Org Settings, updates auto-propagate to all users on their next session after a merged PR. If "Sync automatically" is off, Matt must manually trigger a sync. Manual file uploads have no auto-update path — re-upload required.

**Recommendation:** Connect `Newry-LLC/newry-ai-tools` as the plugin source and enable "Sync automatically" so version updates reach all users without admin action.

**Installation preferences per plugin:**
- `newry-knowledge` — default install (all users get it automatically)
- `primary-research-toolkit` — available (self-service; not everyone does primary research)
- `sof-toolkit` — available (relevant to consultants working on SoF slides)

---

## Central logs

**Usage logging — all plugins:** `~\Newry Corp\Clients - Claude Master Working Folder\logs\usage-log-<user_id>.jsonl`
One file per consultant (keyed by anonymous UUID from `~/.user_id`). Schema: `{"ts", "plugin", "sub_skill", "user_id", "project"}`. Written at the start of every run. Log-reader aggregates across all `usage-log-*.jsonl` files.

**Feedback logging — all plugins:** `~\Newry Corp\Clients - Claude Master Working Folder\logs\feedback-log-<user_id>.md`
One file per consultant (same UUID). Captured via shared feedback-capture sub-skill on positive/negative signals. Log-reader aggregates across all `feedback-log-*.md` files.

**Per-project local logs (PRT only):**
- `logs/synthesis-log.md` — run details per ICS synthesis (project-scoped)
- `logs/feedback-log.md` — feedback captured during the project (project-scoped)

---

## Plugin detail

### Primary Research Toolkit (PRT)
**Version:** 1.3.8
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

**Logs kept:**
- Central (usage): `logs/usage-log-<user_id>.jsonl` (per-consultant)
- Central (feedback): `logs/feedback-log-<user_id>.md` (per-consultant)
- Local per-project: `logs/synthesis-log.md` (ICS run details), `logs/feedback-log.md` (project-scoped feedback)

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
**Version:** 1.0.3
**File:** `outputs/sof-toolkit.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Evaluates, aligns, and drafts Summary of Findings (SoF) slides using the Pyramid Principle as the evaluative standard.

**Modes:**
- Evaluate — score an existing SoF against the Pyramid Principle; identify structural and quality issues
- Align — check whether a SoF matches the supporting deck content
- Draft — produce a SoF from source findings or a deck

**Logs kept:**
- Central (usage): `logs/usage-log-<user_id>.jsonl` (per-consultant)
- Central (feedback): `logs/feedback-log-<user_id>.md` (per-consultant)

**Training materials (SharePoint — for user access; not bundled):**
- Pyramid Principle 2026 deck: [Pyramid Principle 2026.pptx](https://newrycorp.sharepoint.com/clients/Shared%20Documents/Consulting%20Resources/TOOLS-TRAINING/Pyramid%20Principle/Pyramid%20Principle%202026.pptx) — SharePoint > Consulting Resources > TOOLS-TRAINING > Pyramid Principle

**References bundled:** `references/universal-standards.md` — Newry quality standards applied across all modes.

**Notes:** Tested on Glass Core (multiple runs) and Alta (1 Draft run, 2026-04-30). PPTX annotation feature designed but not built (V1 backlog).

---

### newry-knowledge
**Version:** 1.1.14
**File:** `outputs/newry-knowledge.plugin`
**GitHub:** `Newry-LLC/newry-ai-tools`

**What it does:** Firm-wide knowledge search across Newry's SharePoint and Airtable. Answers questions about project history, client contacts, staff expertise, institutional learnings, and any document content on SharePoint.

**Sub-skills:**
- newry-knowledge (coordinator) — classifies questions, routes to the right source(s), assesses richness, synthesizes a combined answer; single entry point
- sharepoint-search — search SharePoint for project materials, internal resources, templates, research, and any firm content
- airtable-search — search Airtable for project metadata, AER learnings, client contacts, and staff expertise

**Logs kept:**
- Central (usage): `logs/usage-log-<user_id>.jsonl` (per-consultant)
- Central (feedback): `logs/feedback-log-<user_id>.md` (per-consultant)
- Local (eval only): `plugins/newry-knowledge/evals/skill-log.jsonl` — maintainer eval runs; not production logging

**Training materials (SharePoint — for user access; not bundled):**
- Onboarding deck (covers both PRT and newry-knowledge, slides 5–6): [PRT and Newry Knowledge Claude Tools 5.12.26.pptx](https://newrycorp.sharepoint.com/clients/Shared%20Documents/Consulting%20Resources/Knowledge%20Nuggets/Nuggets/AI%20and%20LLMs%202026/PRT%20and%20Newry%20Knowledge%20Claude%20Tools%205.12.26.pptx) — SharePoint > Consulting Resources > Knowledge Nuggets > AI and LLMs 2026

**Key dependencies:** M365 connector (for SharePoint) and Airtable connector must be connected in Cowork settings. Not bundled — users connect individually. Matt installs plugin firm-wide; users configure connectors.

**Notes:** Demo questions confirmed: Q1 (Newry Ladder PM expectations), Q3 (Alta competitors AOC/Reichhold). Trigger tests (20 cases) in `evals/trigger-tests.json` — not yet run.

---

### Project Technical Onboarding
**Version:** 0.1.6 | **File:** `outputs/project-technical-onboarding.plugin` | **GitHub:** `Newry-LLC/newry-ai-tools` (pending push)

**What it does:** Guides a consultant through building a Technical Orientation document in week 1 of any engagement. Structured interview + docx artifact output. Calibrates Claude to the client's technology, value creation logic, and competitive position before strategic analysis begins.

**Sub-skills:**
- technical-orientation — structured intake interview → 4-section Technical Orientation doc (Product & Technology / Value Creation / Value Capture / Key Engagement Questions)

**Logs kept:**
- Central (usage): `~\Newry Corp\Clients - Claude Master Working Folder\logs\usage-log-<user_id>.jsonl`
- Central (feedback): `~\Newry Corp\Clients - Claude Master Working Folder\logs\feedback-log-<user_id>.md`

**Training materials:** None yet.

**Key dependencies:** SharePoint working folder required. M365 connector required. Minimum inputs: SOW/proposal + client website.

**Status / pending:**
- Version note: `plugin.json` says 0.1.6; skill internal metadata says 0.1.4 — reconcile on next repackage
- Evals run on v0.1.5 (3 scenarios, 100% pass with skill / 50% without) — new 4-section structure not yet evaluated
- Eval viewer (`eval-review-technical-orientation.html`) needs human review before finalizing
- Plugin 2 (training module — meta-skill for learning any B2B technical context) not yet built

---

### Project Launch Toolkit (PLT)
**Version:** — (not yet packaged) | **Source:** `plugins/project-launch-toolkit/`

**What it does:** Guides a consultant through the project launch phase — from problem statement and issue tree through value creation hypothesis, workplan, and client account management setup.

**Sub-skills (7 built, no coordinator yet):**
- problem-statement — draft problem statement from SoW/proposal in Newry's standard template
- issue-tree — generate MECE issue tree with hypotheses and prioritization recommendation; maps project types to default frameworks
- value-creation — draft value creation hypothesis and Newry fair share calculation; 4 quantification categories
- individual-value-creation-goals — decompose project-level value creation hypothesis into per-team-member goals tied to Newry's 5 KPI categories
- workplan — convert issue tree into responsibility-assigned workplan table with milestone schedule and budget sanity check
- fact-finding — generate pre-populated fact-finding worksheet; searches SharePoint, Airtable, Pipedrive
- account-management — build/update per-stakeholder client account management profile with trust equation assessments and CRM goals

**Logs kept:** TBD (not yet wired up).

**Training materials:** None yet.

**Status / pending:** All 7 sub-skills built. Missing: coordinator SKILL.md (router + shared context). Scored highest in skills prioritization matrix. Pending: coordinator build → Plugin Auditor pass → packaging → GitHub push.

---

### RMA-OA Builder
**Version:** — (not yet packaged) | **Source:** `plugins/rma-oa-builder/`

**What it does:** Guides a consultant through designing and building a Rapid Market Assessment (RMA) or Opportunity Assessment — from intake and scoping through secondary research and section drafting, with a defined handoff to PRT when primary research is needed.

**Sub-skills:**
- rma-oa-builder — Phase 1: intake → tier recommendation → RMA Design Document; Phase 2: section-by-section secondary research → check-in → PRT handoff → docx assembly

**Canonical sections:** Market / Customers / Competitive Landscape / Client Fit / Path to Market & Risks

**Tiers:** Scoping / Standard / Full (recommended based on intake)

**Logs kept:**
- Central (usage): `~\Newry Corp\Clients - Claude Master Working Folder\logs\usage-log-<user_id>.jsonl`
- Central (feedback): `~\Newry Corp\Clients - Claude Master Working Folder\logs\feedback-log-<user_id>.md`

**Training materials:** None yet.

**Status / pending:** SKILL.md written (both phases). Pending: Plugin Auditor pass → vetting → packaging → GitHub push.

---

## Standalone skills (maintainer-facing)

### Plugin Auditor
**Location:** `plugins/plugin-auditor/SKILL.md`
**Not packaged** — used directly by program maintainer in Cowork.

**What it does:** Reviews any Newry plugin for quality across three passes: design (P2/P4/P5/P8/P12 principles), implementation (completeness/consistency/executability/edge cases/calibration/output spec), and token efficiency. Produces a report and walks through changes one by one.

**Logs kept:** None currently.
**When to use:** Before shipping any new plugin or after a major change.

---

### Plugin Builder
**Location:** `plugins/plugin-builder/SKILL.md`
**Not packaged** — used directly by program maintainer in Cowork.

**What it does:** Packages a plugin folder into a correctly structured `.plugin` file for Cowork installation. Handles versioning, directory entries, plugin.json, and file selection.

**Logs kept:** `logs/plugin-builder/feedback-log.md` (central, feedback only).
**When to use:** Any time a plugin is ready for repackaging after changes.

---

### Synthesis QA
**Location:** `plugins/synthesis-qa/SKILL.md`
**Not packaged** — used directly by program maintainer in Cowork.

**What it does:** Quality review of synthesis outputs (roll-ups, summary cards, analytical documents) across four checks: pyramid test, quantitative precision, plain language, headline/evidence consistency.

**Logs kept:** None currently.
**When to use:** Before any synthesis output goes to the team or client.

---

### Log Reader
**Location:** `plugins/log-reader/SKILL.md` | **Not packaged**

Reads and summarizes the central usage log (`usage-log.jsonl`) and feedback log for the Newry AI program. Computes active users (30d) and run counts (30d) per plugin. Use when a program maintainer wants plugin usage metrics or a feedback summary.

**Logs kept:** None.

---

## Shared sub-skills

### feedback-capture
**Location:** `plugins/feedback-capture/SKILL.md`
**Bundled into:** PRT, SoF Toolkit, newry-knowledge packages.

**What it does:** Canonical feedback capture behavior. Each plugin coordinator references this file. Captures positive signals ("wow," "nailed it," "show this to the team") and negative signals (bugs, friction, quality issues, feature requests). Draft-confirm-log pattern. All entries write to the cross-plugin central log.

**Log format fields:** Plugin, Sub-skill, Signal type, Severity, User's words (verbatim), What was happening, Output, Notes.

---

### project-setup
**Location:** `plugins/project-setup/SKILL.md` | **Bundled into:** PRT, Project Technical Onboarding, RMA-OA Builder

Shared Step 0 block for all file-writing Newry skills. Verifies the correct project folder is mounted, establishes project identity (project code, client, working directory), creates skill-specific subfolders, and generates `project.md` from context files. Supports full mode (SharePoint-connected) and informal mode (local only). Includes graceful degradation when SharePoint is not accessible.

---

## Open items / backlog

### Tools in progress needing manual review
- **Index sync skill** — SKILL.md drafted (`plugins/index-sync/SKILL.md`); needs Plugin Auditor pass before use
- **PLT coordinator** — 7 sub-skills built; missing coordinator SKILL.md to route and share context. Next build priority.
- **RMA-OA Builder** — SKILL.md written; pending Plugin Auditor pass → packaging → GitHub push
- **Project Technical Onboarding** — version mismatch (plugin.json 0.1.6 vs. skill metadata 0.1.4); 4-section structure not yet evaluated; Plugin 2 not yet built
- **Plugin Auditor + Synthesis QA + Plugin Builder** — ~~update feedback sections to use shared feedback-capture sub-skill~~ done 2026-05-16

### Skills to be drafted
- **Onboarding skill** — new consultant onboarding experience; surfaces what tools exist, where to start, links to training. Design pending.
- **Program Concierge** — reads this index + program foundations for Matt/successors. Planned, not built.
- **newry-knowledge coordinator** — drafted 2026-05-16 (`skills/newry-knowledge/SKILL.md`); pending Plugin Auditor pass → repackage → reinstall → GitHub push
- **PRT eval runner** — unbuilt commitment

### Maintenance / process
- **Reinstall + GitHub push** — PRT v1.3.8, SoF v1.0.3, newry-knowledge v1.1.10 repackaged and reinstalled 2026-05-16; pushed to GitHub
- **Auto-update** — enable "Sync automatically" on GitHub plugin source in Cowork Org Settings. Blocked on Matt joining Newry-LLC GitHub org.
- **newry-knowledge trigger tests** — 20 cases in `evals/trigger-tests.json`; not yet run
- **PRT non-Alta corpus validation** — waiting for suitable in-flight project

### Feature backlog

*No active items.*
