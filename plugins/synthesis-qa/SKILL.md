---
name: synthesis-qa
description: Use this skill whenever a synthesis output — a Roll-up, interview summary, or other analytical document — needs a quality review before it goes to the team or client. Triggers on "check this roll-up," "review this synthesis," "QA this output," "are the headlines strong," "check for jargon," "is this precise enough," "review my summary cards," or any request to improve the quality of a finished synthesis document — even if the user says "edit" or "review" rather than "QA."
---

# Synthesis QA

A quality-review skill for synthesis outputs — Roll-ups, summaries, and other analytical documents. Designed as a general-purpose skill; currently housed in PRT because the first use case is Roll-up review.

**What this skill does:** applies a structured quality standard to a synthesis document, rewrites headlines and lightly edits full bullets where needed, and produces a revised output plus a notes section documenting every change.

**What this skill does not do:** restructure the document, change the analytical frame, add new findings, or resolve substantive analytical disagreements. Quality fixes to structure and language only — not analytical substance.

---

## Inputs

**Required:**
- The synthesis document to review (Roll-up, summary, or other analytical output)

**Reference (loaded on demand, not upfront):**
- Source documents — summary cards for a PRT Roll-up, or equivalent source material for other document types. Load specific sections when resolving an ambiguity, not the full set.
- `mode2-route-<date>.md` if available — use the branch-to-card index to identify which cards are relevant to which branch before querying them.

---

## Quality standard

Four checks, applied to every bullet in the document:

**1. Pyramid test**
The bolded headline delivers a structural verdict — not a topic label, not a description of what the section covers. The reader should be able to scan only the headlines and get the argument.

- ✓ "CIPP, utility poles, and composite rebar are execution-constrained, not demand-constrained — the gaps are a blend tank, a pultrusion lab, and a proactive commercial posture."
- ✓ "Phase 2 pricing targets $20–30M of additional annual EBITDA — the largest single identified lever, with Phase 1 already delivering ~$20M/yr ahead of schedule."
- ✗ "Commercial execution challenges" (topic label)
- ✗ "Customer feedback on pricing" (topic label)

**2. Quantitative precision**
Every quantitative claim carries a unit (dollars, volume, percentage, timeframe) and matches the source. Vague magnitude claims ("significant," "substantial," "primary") are replaced with the specific figure if one exists in the source.

**3. Plain language**
No jargon a non-specialist reader wouldn't understand on first pass. Rewrite or remove phrases that sound analytical but don't have clear meaning (e.g., "deal thesis in execution," "the corpus supports").

**4. Headline/evidence consistency**
The headline claim is supported by the bullet's own body text. Named terms in the headline (specific products, mechanisms, figures) appear or are explained in the body. If inconsistent: fix the headline to match the evidence, or note that the body needs strengthening.

---

## Process

**Step 1: Initial read**
Read the full document once without editing. Note sections that are likely to require the most work — typically Summary of findings and branch headlines.

**Step 2: Section-by-section quality pass**
Work through the document section by section. For each bullet, apply the four checks in order.

- **If the fix is clear:** rewrite inline. Preserve the original language in the QA notes.
- **If there is ambiguity** (missing unit, vague claim, unclear whether headline matches evidence): query the relevant source document before rewriting. Use the route index if available to identify the right card(s). Load only the relevant section, not the full document.
- **Rewrite depth:** headlines first; light edits to bullet body only when necessary to align with a headline change or fix a precision issue. Do not restructure or reorder bullets.

**Step 3: Compile QA notes**
Produce a QA notes section listing every change made and every unresolved item.

---

## Output

Two parts delivered together:

**Part 1: Revised document**
The full document with all changes applied. Save as a new version (e.g., `Alta Internal Interview Roll-up v6-edited.docx`) — do not overwrite the original.

**Part 2: QA notes**
Appended at the end of the revised document (or as a companion `qa-notes-<date>.md`).

```
## QA notes

### Changes made

| # | Location | Check failed | Original | Revised | Rationale |
|---|----------|-------------|----------|---------|-----------|
| 1 | Summary of findings, bullet 2 | Quantitative precision | "is the primary value creation mechanism in Alta's near term" | "targets $20–30M of additional annual EBITDA — the largest single identified lever" | Unit and magnitude sourced from Hodge summary card para. 109; "primary value creation mechanism" replaced with specific figure. |
| 2 | ... | ... | ... | ... | ... |

### Unresolved items

Items where ambiguity could not be resolved from the source material. Require consultant judgment before finalizing.

- [Location] — [What's unclear] — [What was checked] — [Recommended action]
```

---

## Notes for general use

When applying this skill to non-PRT synthesis outputs:
- "Summary cards" → whatever source documents the synthesis was built from
- "mode2-route file" → any intermediate index of source-to-section mapping, if it exists
- The four quality checks apply regardless of document type


---

## Feedback capture

Apply the shared feedback-capture sub-skill: `plugins/feedback-capture/SKILL.md`.

Set `Plugin: synthesis-qa` and `Sub-skill: synthesis-qa` in the log entry.
