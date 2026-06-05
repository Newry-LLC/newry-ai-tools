# ICS SKILL.md — Token-Efficiency Walkthrough

Working file. Captures decisions on each recommendation as we walk through them. Apply to SKILL.md after the full pass.

Source: 7 recommendations to take SKILL.md from 428 → ~270 lines.

---

## Recommendation 1 — Add "Format conventions" section near top

**Original:** Add a single "Format conventions" section near the top (~15 lines) covering: pyramid headlines required, 4–6 dense bullets per card / per branch / per Summary, citation format, branch-tag placement. Then strip these rules from Mode 1 "Format discipline" (lines 206–211) and Mode 2 prose in sections 3 and 4 (lines 285, 305). Saves ~25 lines.

**Decisions:**
- Use **"pyramid principle"** (known concept — model recognizes it) rather than "pyramid headlines required." Label alone is enough; no need to spell out structure.
- Bullet count: **"4–6 dense bullets — synthesize, don't enumerate."** Target with judgment-room, not a hard cap. The principle is synthesis; the count enforces it.

**Status:** Applied 2026-05-03.

---

## Recommendation 2 — Silent-execution rule stated once

**Original:** State "Steps 2a, 2b, 3 run silently and report in Decisions made" once in the workflow intro. Delete the per-step restatements in Steps 2a (line 66), 3 (line 103), and the "Background work" subsection (lines 58–60). Saves ~8 lines.

**Decisions:** Approved as-is. Low risk — silent execution is a global behavior, right level of abstraction is workflow intro. Modest line savings but improves signal-to-noise in per-step instructions.

**Status:** Applied 2026-05-03.

---

## Recommendation 3 — Compress Step 1 to ~10 lines

**Original:** Compress Step 1 to ~10 lines consistent with the minimal-friction principle: "Surface a tight read on frame + branches + in/out + ambiguous edges. Default output is the nested-bullet scope display from design-notes; escalate to a question only when an edge is genuinely ambiguous. Lock on user go-ahead; record verbatim in output." Cut the Round 1 7-item list and Conversation pattern subsection. Saves ~15 lines.

**Decisions:** Approved as-is.

**Status:** Applied 2026-05-03.

---

## Recommendation 4 — Move "What this skill does not do" to frontmatter

**Original:** Move "What this skill does not do" (lines 420–428) into the description frontmatter as a one-liner. It's a boundary statement, not workflow content. Saves ~10 lines.

**Decisions:** Approved as-is.

**Status:** Applied 2026-05-03.

---

## Recommendation 5 — Move Step 6 Decisions template to references/

**Original:** Move Step 6 Decisions Made template (lines 345–374) to a separate `references/decisions-template.md`. The SKILL.md only needs a one-line pointer. Saves ~30 lines.

**Decisions:** Approved as-is.

**Status:** Applied 2026-05-03.

---

## Recommendation 6 — Delete explanatory "Why" prose under steps

**Original:** Delete the explanatory "Why" prose under Step 1 ("Scope is the one call that, if wrong, invalidates the entire synthesis…"), Step 3 ("Catches transcription errors before synthesis runs"), and similar. The model doesn't need rationale; it needs instructions. Move rationale to design-notes if not already there. Saves ~10 lines.

**Decisions:** Approved as-is.

**Status:** Applied 2026-05-03.

---

## Recommendation 7 — Compress "What you need before starting"

**Original:** Compress "What you need before starting" — Required + Useful context + Hard stop currently runs ~20 lines. Tighten to ~10 by collapsing the bulleted hierarchies into prose. Saves ~10 lines.

**Decisions:** Approved — but compression must preserve information, only the format. The same content needs to remain available because it's the raw material for future user-facing "hand-holding" / onboarding behavior (telling users what they need before starting). When applying, verify nothing is dropped — just tightened.

**Forward note:** Future PRT UX layer should expose this kind of "what you need before starting" content directly to consultants in a guided way, not bury it in SKILL.md. Hold the source content here for that.

**Status:** Applied 2026-05-03. Content preserved (no info dropped); only format compressed.
