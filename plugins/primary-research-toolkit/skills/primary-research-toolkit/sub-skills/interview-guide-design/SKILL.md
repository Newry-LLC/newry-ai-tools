---
name: prt-interview-guide-design
description: Use this sub-skill to build structured interview guides from a research plan — a master guide covering all branches and type-specific versions per interviewee type. Part of the Primary Research Toolkit. Triggers on "build interview guides," "what should I ask [interviewee type]," "create a guide for these branches," "design the interview guide."
---

# Interview Guide Design — SKILL.md

**Plugin:** Primary Research Toolkit
**Position in workflow:** Runs in parallel with Interview Acquisition, after Research Plan Design
**Feeds:** Interview Prep → Interview Coding & Synthesis

---

## What this sub-skill does

Takes the Research Plan (or equivalent inputs) and produces structured interview guides. Builds a comprehensive master guide covering all branches and interviewee types first, then derives type-specific versions. Each guide gives a consultant everything they need to run a productive interview: an intro script, branch-aligned questions, standardized questions marked for exact wording, probing follow-ups, and a notes section for capturing key items in real time.

---

## What you need

**Read from the project folder first:**
- **`Primary Research/outputs/Research Plan v1.md`** — primary input if it exists; contains branch priorities, working hypotheses, interviewee types, standardization flags, and the money slide
- **Analytical frame** in `context/` — for leaf-node questions and sub-branch coverage
- **`project.md`** — for project name, client context, blinding status, and any constraints

**If the Research Plan is missing:** do not stop. Ask the consultant directly for:
- Which branches are in scope (and which are Essential vs. Secondary)
- Which interviewee types will be interviewed
- The money slide — what is the key output visual the client needs to see?
- Any standardization requirements

**Also check:**
- Prior interview guides from similar projects in `context/` or accessible via SharePoint — useful as reference for question framing, not to copy wholesale
- Any notes in `project.md` about interviewee-specific constraints (e.g., regulatory sensitivity, time limits, expert network sourcing)

**Flag before proceeding if:**
- No standardization flags exist — ask whether standardized questions are intended; do not assume
- The money slide is TBD — flag that the guide will be less focused without it, but proceed if the consultant confirms

---

## How this sub-skill works — interactive review

Works through guide design in three steps, pausing for the consultant's reaction at each.

**The three steps:**

1. **Master guide** — one comprehensive guide covering all branches and interviewee types; confirm before deriving type-specific versions
2. **Type-specific guides** — derived from the master; show the consultant the types and branch coverage, ask if any should be reviewed now or deferred until prepping for that interview type
3. **Standardized questions review** — all standardized questions across all guides presented together for final word-for-word confirmation

Feedback is free-form at each pause. Write final output files only after the consultant confirms.

---

## What you produce

One guide per interviewee type, saved to the project's `Primary Research/outputs/` folder:

```
Primary Research/outputs/Interview Guide — Master v1.docx         — comprehensive guide; all branches and types
Primary Research/outputs/Interview Guide — [Type] v1.docx          — working document for the consultant
```

Each guide contains:
1. Header — project, interviewee type, date, Newry team
2. Priority focus — 1–3 blank bullets for the consultant to fill in before each specific interview (the most important things to learn from this particular person)
3. Intro script — project/Newry overview, confidentiality reminder, interviewee background warmup
4. Interview objectives — which branches this guide covers and what we need to learn
5. Questions by branch — primary questions and probing follow-ups; standardized questions clearly marked; working hypothesis visible above each branch
6. Closing — referral ask, conferences/publications, thank you, confirm availability for follow-up
7. Notes section — space below each question set for capturing key items in real time (quotes, numbers, reactions); AI note-taker handles the transcript

---

## Steps

### Step 1 — Read the project context

Open `Primary Research/outputs/Research Plan v1.md` if it exists. Extract:
- Branch prioritization (Essential / Secondary / Out of scope)
- Working hypotheses per branch
- Interviewee types and which branches each covers
- Standardization flags and proposed question stems
- Money slide

If the Research Plan is missing, ask the consultant for the inputs listed in "What you need" above before proceeding.

Then read the analytical frame for the sub-branch and leaf-node detail that will inform individual questions.

---

### Step 2 — Master guide

Build one comprehensive guide covering all branches and all interviewee types. The master guide is the source material for all type-specific versions — every question, probe, and standardized item lives here first.

**Master guide structure:**

---
**[Project Name] — Interview Guide (Master)**
**Date:** [date]
**Newry team:** [from project.md]

**Money slide reminder:** [one line from the Research Plan money slide — keeps the guide focused]

---

**Intro script**
*Interviewer uses this to open every interview. Adapt as needed for blinded vs. unblinded engagements.*

- Introduce yourself and Newry: [brief description of Newry and your role on the project]
- Describe the project: [what you are studying; for blinded engagements, describe the client's industry and situation without naming the client]
- Confidentiality: remind the interviewee you won't pursue anything sensitive or confidential
- Warm up: ask the interviewee to walk you through their background and current role

---

**[Branch name]**
*Interviewee types this branch applies to: [list types]*
*What we believe going in:* [working hypothesis — one sentence]

- [Primary question 1]
  - *Probe:* [follow-up]
  - *Probe:* [follow-up]
- [Primary question 2]
  - *Probe:* [follow-up]
  - *Probe:* [follow-up]
- **[STANDARDIZED — ask word for word]** [standardized question stem]
  - *Probe:* [follow-up]

*Notes:*
[blank]

---

**[Next branch]**
[same structure]

---

**Closing**
- Ask if they would recommend anyone else we should speak with
- Ask about relevant conferences, publications, or associations
- Thank them for their time
- Confirm whether they are available for follow-up

---

**After presenting the master guide:** Ask:
- "Does this cover the right ground — any branches that need more depth, different framing, or questions that are missing?"

Incorporate feedback before moving to Step 3.

---

### Step 3 — Type-specific guides

Derive a guide for each interviewee type by pulling the relevant branches from the master. Present a summary table:

| Guide | Interviewee type | Branches covered |
|-------|-----------------|-----------------|
| 1 | [Type] | [Branches] |
| 2 | [Type] | [Branches] |

Note where branches overlap across types — this is intentional. Flag any Essential branch with thin coverage for a given type.

**Ask:**
- "Do these look right? Would you like to review any of the individual guides now, or save them for when you're prepping for that interview type?"

If the consultant wants to review a guide now, produce it in full (see guide structure below), pause for feedback, incorporate changes, then ask about the next type. If they prefer to defer, save the type-specific guides as drafts and move on.

**Type-specific guide structure:**

---
**[Project Name] — Interview Guide**
**Interviewee type:** [Type]
**Date:** [date]
**Newry team:** [from project.md]

**Money slide reminder:** [one line]

---

**Priority focus** *(fill in before each interview)*
- [blank]
- [blank]
- [blank]

---

**Intro script**
[pulled from master; adjusted for this interviewee type if needed]

---

**Interview objectives**
[what we need to learn from this type; organized by branch; bullet points]

---

**[Branch name]**
*What we believe going in:* [working hypothesis]

[questions pulled from master for this type]

*Notes:*
[blank]

---

**[Next branch]**
[same structure]

---

**Closing**
[standard closing from master]

---

### Step 4 — Standardized questions review

After the master guide is confirmed, pull all standardized questions across all guides into a single view:

| Guide | Branch | Standardized question |
|-------|--------|-----------------------|
| [Type 1] | [Branch A] | "[question]" |
| [Type 2] | [Branch A] | "[question]" |

The same branch may have a standardized question across multiple guide types — these should be as close to identical as possible so responses are directly comparable.

**Ask:**
- "Read through these — are they worded exactly as you'd want to ask them in a real interview?"

Incorporate any wording changes. These are locked at this point and flow back into the individual guides before files are written.

---

## Question writing guidance

- Default to open-ended questions; use closed or directive questions when you need a specific data point
- Use clarifying, elaborating, challenging, and triangulating probes
- 2–3 primary questions per branch is the norm for a 60-minute interview covering 3–4 branches
- Hypotheses orient the interviewer — include them in the guide as context; they are not read aloud to the interviewee
- Standardized questions must be written in plain, natural language — they need to work in a live conversation

---

## Output format

Apply standard Newry document formatting. The guide should be clean and usable during a live interview — enough white space for notes, branch headers clearly visible, standardized questions visually distinct (bold or boxed), priority focus section prominent at the top.

**Producing the docx:** Use `style_docx.py` or equivalent. One docx per guide type, plus the master.

---

## Design principles (inherited from PRT)

- **Research Plan preferred, not required** — use it if it exists; if not, ask for the key inputs before proceeding
- **Master guide first** — build comprehensively, then derive type-specific versions; do not build type guides in isolation
- **Type-specific review on demand** — show the consultant the type summary; let them choose to review now or defer until prepping for that interview type
- **Standardized questions locked after master** — confirmed after master guide review; flow into all type-specific guides before files are written
- **Hypotheses orient the interviewer, not the interviewee** — include them in the guide as context; they are not read aloud
- **Priority focus is consultant-filled** — the 1–3 bullets at the top are left blank; the consultant fills them in before each specific interview
- **Notes section is for real-time capture** — key quotes, numbers, reactions; not a transcript (AI note-taker handles that)
- **Flag gaps inline** — thin branch coverage, TBD money slide, missing standardization flags — note in the output; research lead decides how to resolve
- **Docx only** — one docx per guide type plus the master; no markdown reference files needed for guides

---

## Relationship to other sub-skills

| Sub-skill | What it receives from Interview Guide Design |
|-----------|---------------------------------------------|
| Interview Prep | Completed interview guides (one per type); standardized questions marked; master guide as reference |
| Interview Coding & Synthesis | Standardized question stems (used to identify and cross-tabulate standardized responses during coding) |

See `SKILL.md` at the plugin root for the full workflow sequence.
