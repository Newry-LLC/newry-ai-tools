---
name: primary-research-toolkit
description: Use this skill for any step in Newry's primary research workflow — designing a research plan, building interview guides, sourcing interviewees, preparing for a specific interview, synthesizing transcripts into summary cards and roll-ups, or querying a coded corpus. Triggers on "I have transcripts to synthesize," "build interview guides for this project," "I need a research plan," "prep me for my interview with X," "create summary cards," "build a roll-up," "I'm starting primary research," "who talked about X," "what did people say about X," "go deeper on [name]," or any request involving interview-based research on a Newry project — even if the user doesn't name a specific sub-skill.
---

# Primary Research Toolkit

A plugin for accelerating the most time-intensive steps in Newry's primary research workflow. Takes a project's analytical frame and interview corpus as inputs. Produces structured, evidence-attributed outputs that feed directly into deliverable production.

**What this toolkit does not do:** draw conclusions, make recommendations, prioritize findings, or assess strategic fit. That is the consultant's job.

---

## Step 0 — Project setup and verification

Run the shared project setup block before routing to any sub-skill:
→ `../../project-setup/SKILL.md`

**Skill subfolder for this plugin:** `Primary Research`
Required sub-subfolders to create if missing: `materials/`, `preprocessed/`, `outputs/`, `logs/`

If `project-setup/SKILL.md` is not found: ask the consultant to confirm the project name and code, warn that project verification and mismatch detection are unavailable, and proceed without folder structure enforcement.

After Step 0 completes and project identity is confirmed, proceed to routing below.

**SharePoint path guardrail:** If the current working directory path contains `Newry Corp`, do not navigate above that root under any circumstances — do not read, write, or scaffold outside the current project folder tree.

---

## Usage logging

At the start of every run — before any other work — write a single JSONL entry to the central usage log. This is silent and automatic; no user-facing output.

**Log path:** `"$HOME/Newry Corp/Clients - Claude Master Working Folder/logs/usage-log-<user_id>.jsonl"`
(construct path dynamically using the UUID from `~/.user_id` — creates a per-consultant file)

**Entry format:**
```json
{"ts": "2026-05-13T10:30:00Z", "plugin": "primary_research_toolkit", "sub_skill": "<sub_skill>", "user_id": "<uuid>", "project": "<PROJECT_CODE_OR_null>"}
```

**Field instructions:**
- `ts` — ISO 8601 timestamp at run start (UTC)
- `plugin` — always `primary_research_toolkit`
- `sub_skill` — whichever sub-skill is being invoked: `ics`, `corpus_query`, `rpd`, `igd`, `ia`, `interview_prep`; use `general` if routing hasn't resolved yet
- `user_id` — check for a UUID in `~/.user_id`; if the file doesn't exist, generate a UUID (uuid4) and write it there; reuse on every subsequent run. Also used in the log filename.
- `project` — project code if discernible from context (e.g., `ALTA01`), otherwise `null`

Write the entry using the Bash tool. If the log file or directory doesn't exist, create it. If writing fails for any reason, skip silently — do not surface an error.

---

## Feedback capture

Applies across all sub-skills. Read and follow the shared feedback-capture sub-skill: `../feedback-capture/SKILL.md`

When logging:
- `Plugin:` → `primary-research-toolkit`
- `Sub-skill:` → whichever sub-skill is active (e.g., `interview-coding-synthesis`, `corpus-query`); use `general` if none

---

## Sub-skills

| Sub-skill | Status | Purpose |
|-----------|--------|---------|
| [Research Plan Design](sub-skills/research-plan-design/SKILL.md) | Built | Prioritize branches, identify interviewee types and target N, plan sourcing approach |
| [Interview Guide Design](sub-skills/interview-guide-design/SKILL.md) | Built | Convert prioritized branches into a structured interview guide by interviewee type |
| [Interview Acquisition](sub-skills/interview-acquisition/SKILL.md) | Built | Draft outreach and expert network briefs; research targets; manage the pipeline tracker through to confirmed interview |
| [Interview Prep](sub-skills/interview-prep/SKILL.md) | Built | Customized interview guide per confirmed interviewee: key questions at top, probe notes from corpus learnings to date, flags |
| [Interview Coding & Synthesis](sub-skills/interview-coding-synthesis/SKILL.md) | Built | Code transcripts against the analytical frame; synthesize findings across the corpus, including coverage and gaps |
| [Corpus Query](sub-skills/corpus-query/SKILL.md) | Built | Query the coded corpus by topic, person, segment, or branch; retrieve findings, counts, quotes, cross-tabs, and source exchanges from preprocessed transcripts |
| ~~Coverage & Gap Analysis~~ | Absorbed into ICS Mode 2 (2026-05-04) | Coverage table, per-branch gaps, and contradictions are produced by the Roll-up. Cross-round delta and source-type recommendations are tracked as ICS Mode 2 enhancements. |

---

## Workflow sequence

Primary research work at Newry typically follows this sequence. Not every project uses every step — enter the toolkit at the stage that matches where you are.

```
1. Research Plan Design
   ↓  (branch priorities + interviewee mix + sourcing approach)
2. Interview Guide Design          Interview Acquisition  ← run in parallel
   ↓  (type-specific guides)       ↓  (confirmed pipeline + background research per interviewee)
   └──────────────────────────────┘
3. Interview Prep  ←─────────────────────────────────────────────────────┐
   ↓  (customized guide: key questions first, probe notes from corpus     │
       learnings to date, flags)                                          │
   [consultant runs the interview; transcript goes to Primary Research/materials/] │
4. Interview Coding & Synthesis  ─────────────────────────────────────────┘
   ↓  (summary cards + Roll-up; Roll-up feeds back into Interview Prep for subsequent rounds)
5. Corpus Query  ← available once ICS Mode 1 is complete (claims table + cards exist)
   ↓  (query findings by topic, person, segment; retrieve source exchanges from preprocessed transcripts)
   → SoF Draft mode (deliverable production)
   → Secondary Research Toolkit (future Tier 1 / Module 2 — triangulates secondary sources against the same analytical frame)
```

**Re-running across rounds:** when new interviews come in, re-run Interview Coding & Synthesis on the expanded corpus. The Roll-up surfaces what's covered and what's still missing. (Cross-round delta — explicitly calling out what shifted since the prior round — is a tracked ICS Mode 2 enhancement.)

---

## How to use this toolkit

The user describes their situation in plain language. Match against the patterns below and route to the right sub-skill (and mode) without further conversation. Do not ask the user to identify which sub-skill they want.

**Routing patterns (interpret loosely — semantic match, not literal phrasing):**

| User says something like… | Route to |
|---|---|
| "I have a folder of transcripts and an issue tree" / "I need to code these interviews" / "code and roll up these interviews" | **Interview Coding & Synthesis** — Mode 1 across all transcripts, then Mode 2 Roll-up. The default workflow. |
| "I just have a few transcripts" (≤3) / "small batch of interviews" | **Interview Coding & Synthesis** — Mode 1 only; skip Roll-up. |
| "I have new interviews to add to an existing project" / "next round of interviews" | **Interview Coding & Synthesis** — incremental Mode 1 on new transcripts; Mode 2 against the broader card corpus. If a prior Roll-up is available, pass it as delta input (when that enhancement ships). |
| "I want to know what the interviews have covered" / "what's missing from the corpus" / "where are the gaps" | The Roll-up's coverage table and per-branch Gaps subsections answer this. If a Roll-up doesn't exist yet, run **ICS Mode 2**. |
| "I'm about to start fielding — help me write interview guides" / "what should I ask?" | **Interview Guide Design** |
| "I'm starting a new research project" / "help me plan the research" | **Research Plan Design** |
| "Just give me a single summary card for this one transcript" | **Interview Coding & Synthesis** — Mode 1 only on the named transcript. |
| "Help me reach out to experts" / "draft outreach for [type]" / "add these names to the pipeline" / "update status for [name]" / "write an AlphaSights brief" | **Interview Acquisition** |
| "Prep me for my call with [name]" / "I have interviews this week — help me prep" / "customize the guide for [name]" / "prep for all confirmed interviews" | **Interview Prep** |
| "Who talked about X" / "how many people mentioned X" / "what did people say about X" / "find interviewees who raised X" / "query the corpus" / "search the interviews" / "what did [name] say about X" / "which [type/geography] interviewees raised X" | **Corpus Query** — route to corpus-query sub-skill. |
| "Go deeper on [name]" / "show me the transcript for [name]" / "what else did [name] say about X" | **Corpus Query** — Go Deeper flow. |
| "What does this do?" / "How do I use this?" / "What can this tool help me with?" / "Where do I start?" / "explain the toolkit" | **Orientation** — produce the overview below. |
| "How do I get started?" / "how do I set up my folder?" / "how do I create a working folder?" / "where should I put my files?" / "how do I set up Cowork for this?" / "what do I need before I begin?" | **Setup** — draw on the setup context below to answer what the user actually needs. Don't produce the full setup guide unless asked; respond to the specific question. |

**If the situation doesn't clearly match any pattern**, ask one focused question — not a menu. Example: "Are you coding new interviews, or working with a corpus that's already been coded?" Lock and proceed.

**Required inputs across all routes:** an analytical frame and the relevant primary material (transcripts, summary cards, or both). The scope conversation in Step 1 of each sub-skill confirms framing before heavy work runs.

---

## Orientation

When the consultant asks what this tool does or where to start, produce the following overview in plain language. Do not route to a sub-skill until the consultant indicates they are ready.

---

**This is the Primary Research Toolkit — a set of tools for running primary research at Newry.** It covers the full workflow from planning a research program through coding and synthesizing interview findings.

Here's what it can do, in order:

**1. Research Plan Design** — before you field a single interview. Helps you decide which branches of your analytical frame to prioritize, who to talk to and how many, and how to approach the fieldwork. Works through the plan interactively in four chunks; you react to each before moving on.

**2. Interview Guide Design** — builds the interview guide from your research plan. Produces a master guide covering all branches, then derives type-specific versions (one per interviewee type). Standardized questions are locked and marked word-for-word.

**3. Interview Acquisition** — runs in parallel with guide design. Drafts outreach emails and expert network briefs, researches individual targets, and manages a living pipeline tracker from "targeted" through to "confirmed." You can use it for a full setup or just ask it to research a specific name or draft a follow-up.

**4. Interview Prep** — for each confirmed interview. Takes the standard type-specific guide and reshapes it for the specific person: surfaces the most important questions first, adds probe notes based on what the corpus has surfaced so far (gaps, unresolved claims, thin branches). Gets sharper as fieldwork progresses.

**5. Interview Coding & Synthesis** — the core of the toolkit. Codes transcripts against your analytical frame and produces a summary card per interview. When you have enough cards, runs a Roll-up: synthesizes findings across the corpus, surfaces patterns and contradictions, produces a coverage table showing what's been addressed and what's still missing.

**6. Corpus Query** — once you have a coded corpus. Ask questions directly in plain language: "who talked about pricing pressure?", "what did people say about distributor strategy?", "how many EU interviewees raised CIPP?" Returns findings from the claims table with source codes and attribution. Say "go deeper on [name]" to pull what their summary card captured — or go all the way to the source exchange from the preprocessed transcript.

**You don't need to start at step 1.** Enter wherever you are — if you have a folder of transcripts and an issue tree, start with coding. If you just need to prep for tomorrow's call, start with Interview Prep.

**What you'll need to get going:**
- Your analytical frame (issue tree preferred; a SOW, kickoff deck, or research questions also work)
- Your project folder open in Cowork (or be ready to tell me where it is)

What would you like to do first?

---

## Setup context

Use this to answer questions about getting started, folder setup, or working environment. Respond to what the user actually asked — don't produce the full guide unless they need it.

**Project folder structure on SharePoint:**
- In SharePoint, create a folder called `Claude Working Folder - [Project Code]` alongside the other standard project folders (Project Management, Secondary Research, etc.) within the project
- Inside it, create a `Primary Research` subfolder — this is the Cowork working directory for the PRT
- Other skills will get their own subfolders inside `Claude Working Folder` as they're added

**Syncing to Windows:**
- Click **Sync** in the SharePoint toolbar to sync the Clients library to the local machine
- The folder appears in Windows File Explorer under `Newry Corp` in the left nav
- Once synced, new folders created in SharePoint appear locally automatically

**Starting a Cowork session:**
- Open Cowork and select the `Primary Research` subfolder as the working directory
- Place context materials (SOW, proposal, kickoff deck, anything created before fieldwork) in `context/` before running any sub-skill
- The toolkit will scaffold the rest of the folder structure (`Primary Research/materials/`, `Primary Research/outputs/`, `Primary Research/logs/`, etc.) on first run

**What to expect:**
- The PRT does the heavy lifting on structure, synthesis, and consistency
- It needs good inputs — a real issue tree, actual transcripts, your judgment on what matters
- Garbage in, garbage out still applies

---

All sub-skills in this toolkit are anchored to the same analytical frame. Provide it once at the start of a session; it carries forward.

**Analytical frame** (required for all sub-skills) — the questions to answer and the scope boundary. Best to worst:
- Issue tree — gold standard
- Project scoping document (SOW, kickoff deck, proposal)
- Interview guide / research questions — workable but scope boundary must be inferred

**Scope clarification** — before any sub-skill runs synthesis or coding, it will surface the branches it has identified and ask you to confirm scope. This is mandatory and happens once per session.

---

## Files in this plugin

```
primary-research-toolkit/
  SKILL.md                          ← this file (coordinator)
  overview.md                       ← plugin purpose, principles, status (human doc)
  decisions.md                      ← design decisions and rationale
  design-notes.md                   ← working notes from design phase
  sub-skills/
    research-plan-design/
      SKILL.md
    interview-guide-design/
      SKILL.md
    interview-acquisition/
      SKILL.md
    interview-prep/
      SKILL.md
    interview-coding-synthesis/
      SKILL.md
      eval/
      scripts/
        style_docx.py
    corpus-query/
      SKILL.md
    coverage-gap-analysis/
      SKILL.md                        ← absorbed into ICS Mode 2 (2026-05-04); folder kept for the absorption record
  references/
    interviewee-segmentation.md
  logs/
    synthesis-log.md
    feedback-log.md
```
