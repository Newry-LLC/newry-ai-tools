# ICS SKILL.md — Post-Rewrite Review

Five evaluation areas, each with findings and sub-recommendations. Walk through, approve or push back per item.

Written 2026-05-03 against SKILL.md after token-efficiency cuts (Rec 1–7) and design-principle implementation gap fixes (Output discipline section, "always surface Outside" wording).

---

## Recommendation 1 — Internal consistency: doc-vs-doc within SKILL.md

**Findings:**

- **"Outside the Issue Tree" / "Outside Issue Tree" / "Outside the issue tree"** — three different casings appear: Step 1 scope display uses "Outside the Issue Tree" (titlecase, with "the"), Mode 1 output uses "Unexpected / Outside Issue Tree" (titlecase, no "the"), Mode 2 uses "Outside the issue tree" (lowercase, with "the"). Inconsistent.
- **Mode 1's inline "Decisions made" block** is a 2-bullet ad-hoc structure (term fixes + boundary/matching calls), while Mode 2 references the full template at `references/decisions-template.md`. The relationship between them isn't stated. Per design-notes, Mode 1 is a "lightweight version" — but SKILL.md doesn't say so.
- **Parallel-execution instruction lost.** The pre-rewrite SKILL.md said Steps 2a, 2b, 3 can run in the background while Step 1 (scope conversation) happens. The rewrite cut the "Background work" subsection (per Rec 2). The implication is preserved in the workflow intro ("Steps 2a, 2b, and 3 run silently") but the parallelism is no longer instructed. The model could now read this as strict sequencing.
- **Step 1 nested-bullet scope display vs. "verbatim locked scope statement" in output headers.** Mode 2 corpus header says `[verbatim locked scope statement from Step 1]` and Mode 1 says `[one-line restatement of locked scope from Step 1]`. Step 1 produces a nested-bullet display, not a one-line statement. So either the model derives a one-line statement (Mode 1) AND records the full nested display (Mode 2 verbatim), or the spec is loose. Unclear.
- **Format conventions referenced consistently** from Mode 1 (line 186) and Mode 2 sections 3 + 4. ✓ Good.
- **Output discipline section** (newly added) is not referenced from anywhere — but it's a workflow-level rule, so that's fine. ✓ OK.

**Sub-recommendations:**

1. Pick one canonical form for "Outside the Issue Tree" — recommend titlecase with "the" — and replace everywhere.
2. In Mode 1 output template, add a one-line note: "Decisions made (lightweight per-card version) — full template applies in Mode 2 only."
3. Restore parallel-execution instruction with a single line in Step 2a or workflow intro: "Steps 2a, 2b, 3 may begin as soon as inputs are provided and run in parallel with Step 1's scope conversation."
4. Disambiguate the scope-recording spec: clarify whether Mode 2's "verbatim locked scope statement" is the full nested-bullet display or a derived one-line summary. Recommend: full nested display in Mode 2 header (it's structured and scannable); one-line restatement in Mode 1 header (single transcript doesn't need the full tree).

**Decisions:**

1. Approved.
2. Approved.
3. Approved with revised phrasing: "Steps 2a, 2b, 3 are non-interactive and complete in the same response as Step 1's initial scope read; they report judgment calls in a Decisions made section at the end of the output, so corrections happen after the fact rather than via mid-run prompts." (Replaces the existing workflow intro line 7 — single-sentence change, no new section.)
4. Approved with override: **full nested-bullet scope display in BOTH Mode 1 and Mode 2 headers** (not just Mode 2). Drop the one-line restatement option for Mode 1.

**Status:** Applied 2026-05-03.

---

## Recommendation 2 — Internal consistency: terminology

**Findings:**

- **"branch tag" vs. "branch ID" vs. "canonical branch ID"** — Format conventions uses "Branch tag" as the rule name and "canonical branch ID" as what it is. Mode 1 output template says "(Branch tag)". Two terms for one thing.
- **"signal card" vs. "Single signal card" vs. "Mode 1 card" vs. "card"** — Mode 1 section header is "Mode 1: Single," section text says "compact signal card" and "one record per interview." The artifact's canonical name drifts. Pre-rewrite brief calls it "Signal Cards v3" / "Alta Internal Signal Cards." A consultant or future contributor would benefit from one canonical term.
- **"Decisions made" capitalization** — used as a proper section name throughout, which is consistent. ✓ OK.
- **"verbatim"** has two meanings — input quality type ("verbatim transcript") and citation form ("verbatim quote"). Distinguishable from context but worth a single mention to clarify.
- **"issue tree" vs. "Issue Tree"** — lowercase as common noun ("the issue tree"), titlecase in section names ("Outside the Issue Tree"). Acceptable, but pick a rule.
- **"trunk" vs. "foundational diagnostic"** — Step 1 scope display has "*Foundational diagnostic* (trunk, not a branch)". One use, one place. ✓ OK as a one-time clarification.
- **"exchange unit" / "EU"** — used in SKILL.md only as "exchange units" (Step 2b). Pre-processed transcripts use "EU" abbreviation but SKILL.md doesn't introduce that abbreviation. ✓ Internally consistent in SKILL.md.

**Sub-recommendations:**

1. Standardize on **"branch ID"** everywhere. Drop "branch tag" — "tag" implies labeling style, not identity. The Format conventions rule becomes "Branch ID in parens at the end of each Mode 1 finding bullet."
2. Standardize on **"signal card"** as the artifact name. Use "Mode 1" only as the mode label. Replace "Single signal card" → "signal card." The mode is "Mode 1: Single," produces "signal cards." Less drift.
3. Add a short one-liner where "verbatim" first appears in Format conventions or Step 2b distinguishing the two senses (input quality vs. citation form).
4. Pick "issue tree" (lowercase, common noun) as default; reserve titlecase only for proper section names like "Outside the Issue Tree." Already mostly the case — confirm no drift.

**Decisions:**

1. Approved.
2. Approved with override: rename **"signal card" → "summary card"** throughout SKILL.md. Mode 1 produces "summary cards." Note: minor naming overlap with Mode 2's "Summary of findings" section (different scopes — per-transcript vs. corpus) but distinguishable from context. Historical Alta v3 artifacts remain named "Signal Cards"; new instances use "summary card."
3. Approved.
4. Approved.

**Status:** Applied 2026-05-03.

---

## Recommendation 3 — Doc-vs-code (supporting artifacts)

**Status: N/A but worth flagging.** The Python scripts referenced in the Session Startup brief (`preprocess.py`, `term_reconcile.py`, `style_docx.py`) **do not exist in the workspace.** They were inline during the Alta runs and were never persisted.

**Implications:**

- SKILL.md describes behaviors (Step 2b segmentation, Step 3 reconciliation matrix, color-coded docx coverage cells) that imply pre-built tooling.
- The "reusability pass on `preprocess.py` / `term_reconcile.py` / `style_docx.py`" open item in Session Startup brief presupposes scripts that don't exist.
- Without committed code, behaviors get re-implemented inline each run — its own form of drift, and a quality risk on the next corpus.

**Sub-recommendations:**

1. Build and commit the three scripts before the next ICS run on a new corpus. Extract from the Alta run as a starting point. Place under `sub-skills/interview-coding-synthesis/scripts/`.
2. Until scripts exist, soften SKILL.md language that implies pre-built tooling. Step 3's impact × confidence matrix reads like an automated gate; in practice the model is doing this inference. Either (a) commit the script and wire it in, or (b) phrase the matrix as a decision rule the model applies, not a tool that runs.
3. Update Session Startup brief open item: "Build/commit `preprocess.py`, `term_reconcile.py`, `style_docx.py` (currently inline-only); reusability pass after."
4. Add a `scripts/README.md` placeholder when the scripts are committed, describing each script's contract (inputs, outputs, side effects). This is what doc-vs-code consistency will be checked against in future passes.

**Decisions:**

1. **Done.** Scripts written and committed 2026-05-03:
   - `plugins/primary-research-toolkit/scripts/preprocess.py` (plugin-shared)
   - `plugins/primary-research-toolkit/scripts/term_reconcile.py` (plugin-shared)
   - `plugins/primary-research-toolkit/sub-skills/interview-coding-synthesis/scripts/style_docx.py` (ICS-specific)
2. **Not needed.** SKILL.md language now matches reality.
3. **Pending session close.** Roll into next Session Startup brief update.
4. **Done.** READMEs at both `scripts/` folders, with contracts and idempotency notes.

**Status:** Scripts committed; SKILL.md language alignment to be verified in Rec 4 walkthrough.

**Known issue (carry forward):** term_reconcile.py is context-blind — it applies fixes inside metadata sections like the glossary's own "Project-wide totals" block and the per-file "Term reconciliation" log. False positives are low-impact (the variants are literal text in those contexts) but should be addressed via a "skip text inside Decisions made / Term reconciliation blocks" heuristic before the next corpus.

---

## Recommendation 4 — Output spec clarity in isolation

Question: could a fresh model produce correct output from the SKILL.md templates alone, without seeing v3 examples on disk?

**Findings:**

- **Mode 2 Section 6 (Decisions made) is template-by-pointer.** SKILL.md just says "Use template at `references/decisions-template.md`." A model has to fetch the file to know the structure. Functional, but if the model doesn't fetch it, output structure is at risk.
- **Color-coded coverage cells are unspecified.** Design-notes describes "✓ light green, ~ light yellow, — light gray (post-processing via python-docx — pandoc doesn't carry shading)." SKILL.md doesn't mention this. A model rendering the Mode 2 docx output won't know to apply shading. Either describe the post-processing requirement or hand off explicitly to a script.
- **Mode 1's "Coverage" table format is bare.** `| Branch | Coverage |` with no header underline shown. Mode 2's coverage table is fully specified. Mode 1's simplicity is intentional (single-transcript view) but worth noting explicitly: "Mode 1 coverage is a 2-column simplified view; Mode 2 expands to the full coverage table."
- **Mode 2 coverage table column shorthand** — "✓ Sub. | ~ Partial | — None" — works, but the legend in Mode 1 says "Not addressed," not "None." Minor, but worth normalizing to one term.
- **Mode 1 output uses unmarked section headings** ("Issue Tree Findings", "Unexpected / Outside Issue Tree", "Decisions made") without `##` or any markdown header marker. Mode 2 uses markdown `##` headers. The Mode 1 output is intended to land in a Word doc; Mode 2 is also docx. Consistent rendering should use markdown headers in both, with conversion handling the docx step.
- **"Verbatim or near-verbatim" citation rule** is specified once (Format conventions, line 27) but quotes appear in many places. ✓ Single source of truth; good.
- **Pyramid headline examples** ("X is execution-constrained, not demand-constrained") are concrete and helpful. ✓ Good.

**Sub-recommendations:**

1. In Mode 2 Section 6, add a one-line outline of the template's subsections (Scope / Files / Filename matching / Term fixes / Input quality / Frame interpretation) so the model has structure in context without needing to fetch the file.
2. Add a sentence under Mode 2 coverage table or in the docx-output post-processing area: "Coverage cells are color-shaded in the final docx — ✓ light green, ~ light yellow, — light gray. Apply via post-processing (python-docx); pandoc does not carry shading."
3. Normalize "Not addressed" / "None" to one term. Recommend "Not addressed" since it's more precise.
4. Add markdown `##` headers to Mode 1 output template ("## Issue Tree Findings", "## Unexpected / Outside Issue Tree", "## Decisions made"). Matches Mode 2 convention and renders cleanly through pandoc.
5. Add a one-line lead under Mode 1 output template: "Mode 1 coverage is a simplified 2-column view; Mode 2 uses the full coverage table with What-it-covers and substantive/partial/none counts."

**Decisions:** All five approved as written.

**Status:** Applied 2026-05-03.

---

## Recommendation 5 — Coupling / reuse (Alta-bound vs. project-agnostic)

Goal: would the ICS sub-skill work on a non-Alta project without edits?

**Findings:**

- **Filename example** at line 72 includes "Alta_IS_Smith.docx" — Alta named in the example. Easy fix.
- **Mode 2 coverage table example** at lines 247–248: "A — Adjacent applications" with "CIPP, utility poles, rebar, data centers, lock-gates" and "B1 — Downstream integration" with "SMC compounding, marine adhesives as companion product." These are Alta-specific (composites, structural materials). Anchors the spec to one domain.
- **Glossary seeding** (lines 102–106) — generic. ✓ Good.
- **Logging spec** (Step 5) — generic. ✓ Good.
- **Decisions made template** — generic. ✓ Good.
- **Interviewee type codes** (IS, C, E, CI, O) — generic. ✓ Good.
- **Glossary example terms** ("altar → Alta", "altar in church-renovation client") — Alta + a generic counter-example. The Alta example is fine for illustrative purposes since it's named as an example, not embedded in spec.
- **Design-notes.md** is heavily Alta-flavored (test-run captures from 2026-05-02). That's appropriate — design-notes is a working journal, not for the model. ✓ OK.

**Sub-recommendations:**

1. Replace Alta-specific filename example "Alta_IS_Smith.docx" with a generic placeholder like "Acme_IS_Smith.docx" or the project-agnostic "<Project>_IS_Smith.docx".
2. Replace Alta-specific coverage table examples with abstract placeholders. Recommended: keep the structure but use bracket placeholders for the sub-topics — "[Concrete sub-topics surfaced in the corpus, e.g., specific applications or product categories]" rather than naming "CIPP, utility poles, rebar." Drop the "SMC compounding, marine adhesives" too.
3. Keep the "altar → Alta" glossary example. It's named as illustrative ("e.g.,") and the contrasting "church-renovation client" makes it clear the example is not project-bound.
4. No SKILL.md changes needed for design-notes — leave as Alta-flavored journal.

**Decisions:** All four approved as written.

**Status:** Applied 2026-05-03.

---

## Summary

5 evaluation areas, ~15 sub-recommendations total. Most are small wording or pointer fixes; only Rec 3 (commit the scripts) is substantive work.

**If approved, suggested order to apply:**
1. Rec 5 (coupling) — quick string edits, lowest risk.
2. Rec 2 (terminology) — small string normalization across SKILL.md.
3. Rec 1 (doc-vs-doc) — requires a couple of judgment calls (sub-rec 4 on scope-recording spec).
4. Rec 4 (output spec clarity) — adds one or two paragraphs.
5. Rec 3 (scripts) — separate workstream; requires actually building and committing the scripts.
