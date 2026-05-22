---
name: prt-interview-prep
description: Use this sub-skill to prepare for a specific confirmed interview — surfaces the most important questions first, adds probe notes from corpus learnings to date, and flags known gaps or contradictions relevant to this interviewee. Part of the Primary Research Toolkit. Triggers on "prep me for my call with [name]," "customize the guide for [name]," "I have an interview tomorrow," "prep for all confirmed interviews this week."
---

# Interview Prep — SKILL.md

**Plugin:** Primary Research Toolkit
**Position in workflow:** After Interview Acquisition (confirmed pipeline) and Interview Guide Design; immediately before the interview itself
**Feeds:** Interview Coding & Synthesis (consultant provides transcript after call)

---

## What this sub-skill does

Produces a customized interview guide for each confirmed interviewee. It takes the standard type-specific guide and reshapes it for this specific person — surfacing the most important questions first, modifying questions based on the interviewee's background, and adding probe points derived from what the corpus has surfaced to date (gaps, thin branches, unresolved claims).

As fieldwork progresses and the corpus grows, the prep gets sharper: the skill draws on existing summary cards or the Roll-up to identify what's well-covered, what's still missing, and what prior interviewees raised but left unresolved.

This sub-skill does not run the interview. The interview is a human conversation.

---

## What you need

**Read from the project folder first:**
- **`Primary Research/outputs/Interview Pipeline v1.xlsx`** — confirmed interviewees, background research, branch focus, interviewee type, status
- **`Primary Research/outputs/Interview Guide — [Type] v1.docx`** — type-specific questions and standardized items for this interviewee's type
- **`project.md`** — project name, client context, blinding status, any constraints

**Load if available (improves quality significantly):**
- **`Primary Research/outputs/[Project Name] Summary Cards vN.docx`** or equivalent — existing summary cards; scan for branch coverage and open threads
- **`Primary Research/outputs/[Roll-up file].docx`** or equivalent — Roll-up if one exists; gaps list and per-branch coverage ratings are the most useful sections

**Ask if not clear:**
- Which interviews to prep for (specific names, a date window, or "all confirmed/scheduled")

**Do not need:**
- Research Plan (branch priorities are in the guide and tracker)
- Master interview guide (type-specific guide is sufficient)

---

## How this sub-skill works

**Triggering patterns:**
- "Prep me for my call with [name]"
- "I have three interviews this week — help me prep"
- "Prep for all confirmed interviews"
- "Customize the guide for [name]"

**Flow:**

1. Load the pipeline tracker (`Primary Research/outputs/Interview Pipeline v1.xlsx`); identify target interviewees (filter to "Confirmed" or "Scheduled", or the names/date range specified)
2. For each interviewee, load their tracker row: background research, type, branch focus, contact method
3. Load the type-specific interview guide
4. Check for summary cards and/or Roll-up; if present, scan for:
   - Branch coverage gaps (thin or missing branches relevant to this interviewee's type)
   - Unresolved claims or findings that need corroboration
   - Themes that have surfaced repeatedly but lack quantification or specificity
5. Produce a customized guide for each interviewee (see structure below)
6. Save as a single batch file to `Primary Research/outputs/`

**Batch vs. single:**
- Default: one file, one section per person
- Single interview: one-section output; filename reflects the interviewee name

---

## What you produce

```
Primary Research/outputs/Interview Prep — [Date or batch label] v1.md
```

Increment version if re-running for the same batch (v2, v3).

---

## Guide structure — one section per interviewee

```
## [Full Name] — [Title], [Company]
**Type:** [Interviewee type]
**Interview date:** [Date / TBD]
**Branch focus:** [Branch codes and labels, e.g. A — Market structure, B2 — Competitive dynamics]
**Contact method:** [Cold outreach / Warm referral / Expert network — AlphaSights / Guidepoint / AlphaSense]

### Key focus for this interview
[2–4 bullets identifying:
(a) gaps in branch coverage this interviewee's type can address, based on corpus coverage to date, and
(b) unresolved claims or thin findings from prior corpus that this interviewee's background makes them well-positioned to address.
Derived from corpus — not a strategic prioritization judgment. Consultant reads it first, then runs the guide.]

### Background
[3–4 sentences from the IA tracker. Who they are, their role, and why they're
relevant. Reference specific experience, company context, or positions held.
If from an expert network, note they must appear as "Anonymous" in client-facing
materials — only title and company can be shown.]

### Customized guide

**Priority questions** *(ask regardless of time)*
[5–8 questions, drawn from the type-specific guide and reordered/adapted for this person.
Prioritization logic: branch focus for this type + corpus gaps + this interviewee's
specific background.

For each question, add a probe note if corpus learnings suggest a particular angle:
  Q: [Question text]
  → Probe: [What to push on; why — e.g. "three prior interviewees cited this mechanism
    but none could quantify it — push for numbers or a range"]

Standardized questions: include exact wording and mark [STANDARDIZED].
Non-standardized: adapt phrasing to this person where it sharpens the question.]

**Secondary questions** *(if time allows)*
[Remaining guide questions relevant to this type but lower priority for this specific
person. No probe notes unless clearly warranted. Omit this section if all questions
fit in Priority — do not create a secondary list just to be complete.]

### Flags
[Bullets. Include only what's meaningful:
- Sensitivities — regulatory, competitive, or NDA-adjacent topics to handle carefully
- Background gaps — areas where tracker research was thin; probe or lower expectations
- Anonymity reminder if from an expert network (title + company only in deliverables)
Omit section entirely if there are nothing meaningful to flag.]

### Notes
[Blank — consultant fills during or immediately after the call]

---
```

---

## After the interview

When the consultant signals an interview is complete, provide a one-line pointer:

> Drop the transcript in `Primary Research/materials/` and run **Interview Coding & Synthesis** when ready.

Update tracker status to "Completed" if asked.

---

## Design principles

- **The guide is the artifact** — not a brief, not a summary. The consultant should be able to run the interview from this document. Format accordingly.
- **Corpus-informed, not corpus-dependent** — the skill runs without summary cards or a Roll-up (first interviews of a project). When they exist, they sharpen the probe notes and key focus considerably. Call out when corpus is not yet available.
- **Priority questions first, always** — the reordering is the job. A consultant 5 minutes before a call should be able to scan the priority list and go.
- **Probe notes are specific or absent** — "probe further" is not a probe note. A probe note names the specific thing to push on and why (what prior evidence exists, what's unresolved). If there's no specific corpus basis, omit it.
- **Standardized questions are sacred** — exact wording, marked [STANDARDIZED], no adaptation. These exist for cross-interview comparability.
- **Anonymity is a hard rule** — expert network interviewees appear as "Anonymous" in client-facing materials. Note this in the guide. Consultants sometimes lose track of which contacts came through which channel.
- **Batch is the default** — one file for all upcoming interviews; one section per person.

---

## Relationship to other sub-skills

| Sub-skill | What Interview Prep receives |
|-----------|------------------------------|
| Interview Acquisition | Confirmed interviewee list; background research per row; branch focus; interviewee type; contact method |
| Interview Guide Design | Type-specific questions; standardized question exact wording |
| Interview Coding & Synthesis | Summary cards and/or Roll-up (if available) — branch coverage ratings, gaps list, unresolved findings |

| Sub-skill | What feeds into it from Interview Prep |
|-----------|----------------------------------------|
| Interview Coding & Synthesis | Nothing directly — consultant runs the interview; transcript goes to `Primary Research/materials/` |
