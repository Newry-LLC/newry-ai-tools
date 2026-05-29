---
name: sof-toolkit
description: Use this skill whenever a consultant is working on a Summary of Findings (SoF) slide — evaluating whether it's strong, checking whether it matches the deck, or drafting one from source material. Triggers on "review my SoF," "evaluate this summary of findings," "is my headline strong," "does my SoF match the deck," "draft a SoF from these findings," "check this against the pyramid principle," or any request involving a SoF slide in a Newry deck — even if the user doesn't say "SoF" explicitly.
---

# SoF Toolkit

A skill for evaluating, drafting, and aligning Summary of Findings (SoF) slides in Newry consulting decks. The Pyramid Principle is the evaluative standard throughout.

---

## Context

**Mode detection:** If the consultant provides a SoF for feedback → Evaluate. If they want to check whether the SoF matches the deck → Align. If they have source material but no SoF → Draft. When ambiguous, ask one question: "Are you looking for feedback on an existing SoF, checking it against your deck, or drafting one from scratch?"

Every mode needs three things: the material (SoF slide, deck, or source content), background and objectives, and stage and audience. If any are missing, ask for them specifically before proceeding.

1. **Background and objectives** — what Newry was hired to do and what the client's core question was. Ask if not provided; not required, but shapes everything.
2. **Stage** — early working hypothesis, mid-project / iterative, or final deliverable.
3. **Audience** — internal team or client-facing.

Stage and audience together determine how strictly to evaluate and what to prioritize. See `references/universal-standards.md` for coverage standards by stage.

---

## Mode 1: Evaluate

Use when the consultant has a SoF and wants feedback.

**Scope:** SoF slide only. Body slides are not required and should not be consulted. Checking whether the SoF accurately represents the body deck is Align mode's job — do not perform that check here.

### Input handling

**If the consultant uploads a slide image:**
- Read the image directly. Use the visual layout to assess headline, bullets, tables, and any other content.
- Assess headline headroom visually: can you see whether the title box has room for more text? Note what you observe.
- Do not ask about tables or visuals — you can see them.

**If the consultant pastes text:**
- Before evaluating, ask: *"Does this slide include any tables or visuals that carry substantive content? If so, please share them — tables in SoF slides often hold key findings that aren't visible in the text."*
- Wait for the response before proceeding.

### Evaluation output

Produce output in this order using bullets throughout. Descriptive phrases within bullets are fine; avoid prose paragraphs.

**What's working**
- One bullet per strength — name the element and why it works in a phrase or sentence
- Skip if there's nothing genuine to note

**Top 2–3 improvements**
- One bullet per issue, highest-leverage first
- Format: *[element]* — [problem precisely stated] → [what a stronger version would do]

**Headline rewrite** *(if the headline needs improvement)*
- Present the rewrite on its own line
- Add a one-line note on length fit if relevant

**Final consistency pass**
- After completing the evaluation above, re-read the slide top-down — headline, then each bullet and sub-bullet — and check for logical inconsistencies: across levels (does the headline misrepresent what the bullets say?), within a level (do parallel bullets use incompatible assumptions or units?), and across bullets (does one bullet contradict or undermine another?). Flag anything that doesn't hold together.
- Do not cross-reference body slides here. That is Align mode's function.

### Format recognition

Not all Newry SoFs use traditional structure. Common variants:

- **OKR / progress table** — organized by objectives, not importance. Common in Growth Engine and ongoing engagements.
- **Module overview** — three labeled categories (e.g., Impact & ROI / Insights / Recommendations). Common in Growth Engine final readouts.
- **Traditional SoF** — headline + bullets ordered by importance. Standard in Opportunity Assessment and Technical Landscape projects.

When you see a non-traditional format: acknowledge it, evaluate what's there on its own terms, note what the format gains and what it trades away, and flag if a traditional SoF would serve the audience better — but don't penalize for using the format that fits the project type.

---

## Mode 2: Align

Use when the consultant wants to check whether the SoF and the deck are consistent with each other.

**Scope:** SoF + body slides. Does not re-run SoF quality assessment — run Evaluate separately for that. Align checks only whether the SoF accurately represents the deck: coverage, accuracy, order, and figure consistency.

### What to collect

The full deck as a PPTX — the SoF and body slides are in it.

### What to check

- **Coverage**: Do the most important findings in the body appear in the SoF? Flag significant conclusions buried in the body that don't surface in the SoF.
- **Accuracy**: Does the SoF make claims the body doesn't support? Flag anything that overstates, understates, or misrepresents what the body shows.
- **Order**: Does the SoF's sequence reflect the logical structure of the deck? A SoF that leads with a minor finding while burying the key conclusion is a structural problem.
- **Sizing**: Are quantified figures in the SoF consistent with figures in the body slides?

### Output

Use three labeled bullet groups. One line per entry where possible.

**Matches well**
- [item]

**Missing from SoF**
- [item]

**Overstated / misstated**
- [item]

---

## Mode 3: Draft

Use when the consultant has underlying findings but no SoF, or wants to build the story before constructing the deck.

**Scope:** Source material and objectives only. No existing SoF to evaluate or body deck to align against — this mode produces a SoF from scratch.

### What to expect

- **Reliable:** Key findings, figures, and what matters most are correctly identified.
- **Not reliable:** Story structure. The "why this situation exists" claim is often missing; bullets are ordered by analytical weight, not by what the client needs to hear first. The headline may need rewriting.
- **How to use:** Treat as a strong first draft of the analytical content. Plan a quick editorial pass on structure and headline before sending to a client.

### What to collect

1. **Source material** — any combination of: interview notes, secondary research, quantitative analysis, OKR tables, or rough bullet points summarizing what was learned
2. **Background and objectives** — what Newry was hired to do and the client's core question (essential for this mode)
3. **Stage and audience** — shapes what level of synthesis and completeness to aim for

### Drafting process

0. Identify the story structure using Minto's Situation-Complication-Resolution framework. If the source material is a well-constructed deck, follow the slide sequence as the argument structure. If it's unstructured (raw analysis, interview notes, loose slides), use SCR to find the narrative arc before ordering findings. The Complication is often a finding, not background — if it makes a claim about what is true (e.g., a technology is hitting limits, a market is shifting), it must appear as a bullet, not just as context in the pre-draft analysis.
1. Identify the single most important conclusion — this becomes the headline
2. Order remaining findings by importance to the client (if the source is a well-constructed deck, the slide sequence likely reflects this already)
3. Draft a headline that makes a complete assertive claim, captures the key tension or answer, and fits within 150–175 characters
4. Draft 4–6 bullets, each leading with a bolded claim followed by supporting detail
5. Check each bullet: is it a finding, or does it describe methodology or background? Rewrite any that don't make a claim.

### Output format

> **Headline:** [drafted headline]
>
> - **[Bolded claim].** Supporting detail.
> - **[Bolded claim].** Supporting detail.
> *(etc.)*

Then flag any bullets where findings were thin or ambiguous:

**Needs more substance**
- *[bullet]* — [what's missing or uncertain]

---

## Logging Eval Results

For eval run logging format, see `eval/eval-log-format.md`.

---

## Usage logging

At the start of every run — before any other work:

**Step 1 — Check Airtable connectivity.**
Call `list_records_for_table` (Base ID: `appRawPuacfAvVH2Z`, Table ID: `tblmACtwIClniGn5n`, pageSize: 1). If this call fails, stop and show:

> "⚠ **Airtable isn't connected.** This tool requires Airtable for usage logging. Go to Cowork Settings → Connectors, connect Airtable, then start a new session."

Do not proceed until resolved.

**Step 2 — Write to Airtable.**
Call `create_records_for_table` with:
- **Base ID:** `appRawPuacfAvVH2Z` | **Table ID:** `tblmACtwIClniGn5n`
- **Fields:**
  - `fldRrr3BkrJW8rE3L` (ts) — current UTC time, ISO 8601 (e.g. `2026-05-27T14:30:00Z`)
  - `fldNHK285dPCOdNhB` (plugin) — `"sof_toolkit"`
  - `fld4EyuVEhxAhPZEd` (sub_skill) — whichever mode is active: `"evaluate"`, `"align"`, `"draft"`; use `"general"` if none
  - `fldmTXyfFZRpbZEvQ` (user_id) — read `~/.user_id` if it exists; otherwise `"unknown"`
  - `fldu8rvXDfvi2O3jF` (project) — project code if discernible (e.g. `"ALTA01"`); otherwise `""`

If the write succeeds, continue. If it fails, retry once.

**Step 3 — Local fallback (if Airtable write still failed after retry).**
Silently append one JSON line to `~/.newry/logs/usage-log-<user_id>.jsonl` (create `~/.newry/logs/` if missing):
`{"ts":"<ISO>","plugin":"sof_toolkit","sub_skill":"<sub_skill>","user_id":"<user_id>","project":"<project>"}`
No user-facing output. Then continue.

---

## Feedback capture

Read and follow the shared feedback-capture sub-skill: `../feedback-capture/SKILL.md`

When logging:
- `Plugin:` → `sof-toolkit`
- `Sub-skill:` → whichever mode is active (`evaluate`, `align`, `draft`); use `general` if none
