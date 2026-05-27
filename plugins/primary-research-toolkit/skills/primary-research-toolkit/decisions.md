# Primary Research Toolkit — Design Decisions

Decisions made, options ruled out, and why. Add an entry when a choice is made that future sessions might otherwise revisit or reverse.

---

## Mode 2 decomposed into 4-pass pipeline
**Date:** 2026-05-05
**Decision:** Replace single-pass Mode 2 with a 4-pass pipeline: Route → Extract → Branch synthesis → Summary synthesis. Intermediate state lives in files between passes so context resets cleanly between each.
**Why:** Root cause of the v6 vs. v2b synthesis quality gap was context-window pressure — 55 cards (~48,500 tokens) in a single pass caused the model to enumerate rather than synthesize, and to write topic-label headlines rather than structural verdicts. v2b ran on ~10 cards (5x smaller context), which is why its headlines were sharper despite both runs being AI-throughout. Per-branch decomposition reduces per-branch context from 20–30K tokens to ~4–6K regardless of corpus size.
**Alternatives ruled out:** (a) Python for Passes 1–2 — rejected because silent failures on structural drift in Mode 1 output introduce more risk than they save in tokens; LLM handles variation gracefully, Python won't. (b) Summarizing cards before synthesis — adds a token-burning step without solving the underlying enumeration problem.
**Reference:** `comparisons/alta-rollup-v6-vs-v2b.md`

## 4–6 bullet cap hardened to a hard cap
**Date:** 2026-05-05
**Decision:** Changed "4–6 dense bullets — synthesize, don't enumerate" to a hard cap with explicit enforcement instruction ("if you have 8 bullets, combine the weakest two pairs; do not exceed 6 under any circumstance").
**Why:** v6 Roll-up violated the 4–6 cap in every branch, drifting to 8–10 bullets under context pressure. Soft language ("synthesize, don't enumerate") is insufficient at scale.

## Synthesis QA sub-skill created (formerly "Editorial Review")
**Date:** 2026-05-05
**Decision:** Added `sub-skills/editorial-review/SKILL.md` — a general-purpose quality review of synthesis outputs. Triggered by quality issues found in the Alta v2b Roll-up: imprecise headlines, missing units on quantitative claims, jargon, headline/body inconsistency. Designed as a fresh-context pass (separate from the synthesis run) with access to source cards on demand. Output is revised document + editorial notes table. Housed in PRT for now; designed for general use. Renamed to Synthesis QA (2026-05-08) — moved to `plugins/synthesis-qa/SKILL.md`.
**Four checks:** pyramid test on headlines, quantitative precision (units, source match), plain language (no jargon), headline/evidence consistency.
**Rewrite scope:** headlines primary; light full-bullet edits where needed; no restructuring.

## Pyramid calibration examples added to Format conventions
**Date:** 2026-05-05
**Decision:** Added four concrete examples (2 ✓, 2 ✗) to the pyramid principle instruction in Format conventions.
**Why:** v6 headlines were largely topic labels ("Commercial execution challenges") rather than structural verdicts. Examples provide a calibration anchor the model can check against during synthesis.

---

## "RAG" terminology replaced with "targeted extraction"
**Date:** 2026-05-07
**Decision:** Use "targeted extraction" throughout. Updated in overview.md. No instances found in SKILL.md files.
**Why:** "RAG" implies vector stores and embedding-based retrieval, which is not what ICS does. The actual approach is passage-level extraction and targeted reading of source material.

---

## Program-level backlog: cross-project learning capture
**Date:** 2026-05-07
**Status:** Design backlog — not yet scoped
**Idea:** Passive capture of project learnings as users interact with PRT tools (same recognition-based pattern as feedback log). Learnings stored in a structured external store (AirTable candidate) with queryable fields: industry, interviewee type, sourcing channel, topic area, outcome. On new project startup, PRT queries the store for relevant prior learnings and surfaces them as context — no separate user step required. Example: starting a new automotive project, skill surfaces "AlphaSights worked well for ADAS component experts; LinkedIn yielded low response rate for this type."
**Why valuable:** Newry's institutional knowledge about what works for sourcing (and other primary research decisions) currently lives in people's heads. This makes it queryable and compounding.
**Dependencies:** AirTable MCP connector; data model design (fields for capture and retrieval); account ownership at Newry.
**Capture side:** straightforward extension of existing feedback-log pattern. **Retrieval side:** requires connector + data model work.
