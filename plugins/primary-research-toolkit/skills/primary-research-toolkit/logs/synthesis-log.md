# Interview Coding & Synthesis — Run Log

Log of every skill invocation. Append an entry at the end of each run.

---

---
Date: 2026-04-30
Project: Alta Performance Materials — Growth Strategy Module 1
Mode: Single (x3)
Transcripts processed: 3 (Blair Quiring, Doug Hofer, Jonathan McKay)
Analytical frame: Issue tree (6 branches across Trunk A and Trunk B)
Branches in scope: 6
Emergent themes surfaced: 6 (2 per interview)
Input quality: Synthesized notes (Anna Jaffe)
Interviewee types: Internal client staff (all 3)
Notes: First test run of the PRT synthesis skill. Single mode output format redesigned mid-session based on Sylvan feedback — moved from branch-by-branch verbose output to compact signal card format: coverage table + findings ordered by importance with branch tags in parens + unexpected findings. SKILL.md updated to reflect new format. Output saved to Alta Internal Interview Signal Cards.docx.
---

---
Date: 2026-04-30
Project: Alta Performance Materials — Growth Strategy Module 1
Mode: Single (x40) + Roll-up
Transcripts processed: 40 (all internal client staff, April 16–29 2026)
Analytical frame: Issue tree (7 branches: A1, A2a, A2b, B1, B2, B3, B4)
Branches in scope: 7
Emergent themes surfaced: 5 (corpus-wide)
Input quality: Synthesized notes (Anna Jaffe) — Medium attribution
Interviewee types: Internal client staff (NA Commercial, NA Technical, NA R&D, NA Operations, EU Commercial, EU Technical, LatAm Commercial)
Notes: Full run across all 40 interviews extracted from the combined "All Internal Interview Notes" file. Signal cards for all 40 interviewees plus full Roll-up synthesis section produced in single Word doc (Alta Internal Interview Signal Cards.docx). Run completed in a continuation session after previous session ran out of context — all data was pre-extracted to interviews_extracted.json in the prior session. Roll-up synthesized patterns, contradictions, gaps, and emergent themes by branch. Key Roll-up findings: CIPP is most corroborated single opportunity (8+ voices); data centers reactive not proactive; composite rebar consistently cited but Alta is a spectator; MOQ/tote barriers quantified and actionable; marine adhesives M&A endorsed by 3+ senior technical voices unprompted; styrene substitution is the highest-stakes single variable. Five emergent themes: succession risk (systemic), Phase 2 pricing (highest near-term lever), web presence liability, Turkish/Asian structural competition, reactive PD posture.
---

---
Date: 2026-05-02
Project: Alta Performance Materials — Growth Strategy Module 1
Mode: Single (x10) + Roll-up
Transcripts processed: 10 (Blair Quiring, Doug Hofer, Graham MacInnis, Jonathan McKay, José Miquel, Junxian Wu, Olivia Woerth, Olli Piiroinen, Sabine Dinger, Shawn Bennett — all internal staff, raw Otter.ai transcripts)
Analytical frame: Issue tree from project initiation deck (slide 15)
Branches in scope: 5 (A flat; B1, B2, B3, B4 sub-branched; trunk-not-branch foundational diagnostic flowing into A and B)
Locked scope statement: Identify findings against Branch A (adjacent applications) and Branch B (strategic portfolio moves: B1 downstream integration, B2 new resin types, B3 M&A, B4 packaged offerings) for Alta's growth strategy in NA and Europe; foundational diagnostic threads (win/loss, customer value, competitive position) flow into A and B; Outside-the-Issue-Tree material captured separately.
Emergent themes surfaced: ~10 cross-corpus patterns + 9 Outside-the-Issue-Tree themes
Input quality: Verbatim Otter.ai (8 High; 1 Medium — Jonathan McKay 11 unknown-speaker turns inferred; 1 Low — Sabine Dinger all-Unknown resolved by alternation, no verbatim quotes)
Interviewee types: 10 internal staff (commercial, technical service, R&D)
Term fixes auto-applied: 70 (Step 3 reconciliation)
Term fixes flagged for review: 26 (best-inference + contextual + file-specific)
Glossary entries added this run: 30 canonical entries written to plugins/primary-research-toolkit/Alta/glossary.md
Notes: First test run of the rewritten ICS workflow (5-step, scope-conversation as only user gate, decisions-at-end). Workflow exercised end-to-end. SKILL.md updated mid-run to canonicalize cards-first-then-Roll-up as the default Step 4 pattern (was previously presented as a fork). Pre-processing produced working files in Pre-processed/ with EU segmentation, speaker resolution, and non-substantive flagging. Term reconciliation produced project glossary. Mode 1 produced 10 signal cards in parallel via subagents. Mode 2 Roll-up produced from cards (not raw transcripts) — first run of cards-first default. Outputs: Alta Internal Signal Cards v3.docx, Alta Internal Interview Rollup v3.docx. Sylvan UX feedback captured in design-notes.md: silent execution, decisions-at-end, no "next move pick one" menus, suppress technical noise, scope conversation minimal-friction, always capture Outside the Issue Tree, standard nested-bullet frame display.
---

---
Date: 2026-05-04
Project: Alta Performance Materials — Growth Strategy Module 1
Mode: Single (x55) + Roll-up
Transcripts processed: 55 (all internal staff; raw Otter.ai .txt verbatim transcripts; the new 5/4/26 dump replacing prior 10-interview run)
Analytical frame: Issue tree from project initiation deck (slide 15), memorialized to context/issue-tree.md
Branches in scope: 6 (A; B1, B2, B3, B4 sub-branched; foundational diagnostic flowing into A and B)
Locked scope statement: How can Alta drive 3 – 6 growth initiatives ≥ $5M EBITDA each in NA & Europe? — A: adjacent applications; B: strategic portfolio moves (B1 downstream integration, B2 new resin types, B3 M&A, B4 packaged/system offerings); foundational diagnostic; Outside the Issue Tree captured separately.
Emergent themes surfaced: 8 cross-corpus main messages + 5 Outside-the-Issue-Tree themes (Mode 2 Section 3)
Input quality: Verbatim Otter.ai. Final attribution distribution after preprocess + intro-spiel anchor + LLM re-diarization on 11 lowest-attribution files: 17 High, 28 Medium-High, 10 Medium. Zero Low / Medium-low remaining.
Interviewee types: 55 internal staff (NA Commercial, NA Technical Service, NA R&D / Process Excellence, NA Operations, EU Commercial, EU Technical, LatAm Commercial).
Term fixes auto-applied: 332 high-confidence (Ulta→Alta ×192, gel code→gelcoat ×60, dericane→DERAKANE ×33, etc.)
Term fixes flagged for review: 68 (32 best-inference + 16 contextual + 20 file-specific)
Glossary entries added this run: 0 new (project glossary stable across the 5x scale-up; tallies refreshed)
Notes: 5x corpus-scale validation run for the committed PRT scripts (preprocess.py, term_reconcile.py, style_docx.py). Four script bugs surfaced and fixed at scale, all logged in feedback-log.md as resolved: (1) OTTER_TURN_RE catastrophic regex backtracking on files >~10KB → replaced with line-based parser; (2) speaker regex excluded digits → "Speaker N" lines invisible; (3) match_filename_to_person used substring on last name → cross-contamination (Joy/Shawn Bennett, Bret/Thomas) → token-based matcher; (4) no fallback when interviewee name not in speaker labels → 5 files had 0 substantive EUs → aggregate-words fallback. Plus one feature add: intro-spiel anchor in resolve_speakers (high-confidence interviewer ID via Newry-keyword density in first 8 turns). Sylvan-driven decisions: (a) re-run Mode 1 with sharpened agent diarization instructions after intro-spiel anchor (v4→v5); (b) LLM-based content re-diarization on the 11 lowest-attribution files (v5→v6) — Otter alternation flagged as fundamentally unreliable per Sylvan because Otter splits single-speaker continuous talk into multiple turns. Saved to feedback memory as project-wide caution. v6 vs. original AI-from-Anna's-notes Signal Cards comparison (10 cards): v6 has more specific evidence (volumes, percentages, verbatim quotes); originals had sharper single-bullet strategic frames and cross-card pattern hints (consultant had read whole corpus before writing each card). Methodological learning saved: AI synthesis quality is bounded by source-material density. Mode 2 Roll-up produced from v6 cards (not raw transcripts), 13.4K words across coverage table + summary of findings (8+5) + branch findings (A=10, B1=8, B2=8, B3=8, B4=8, Foundational=8) + interviewee index (55 entries) + decisions made (full audit trail with 9-item gap list for consultant follow-up). Outputs: Alta Internal Summary Cards v6.docx (55 cards), Alta Internal Interview Roll-up v6.docx.
---
