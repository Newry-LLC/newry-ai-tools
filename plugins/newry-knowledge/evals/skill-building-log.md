# Skill Building Log

A running log of observations, misses, and improvements made to Newry Cowork skills. Captures the reasoning behind changes so future skill work doesn't repeat the same mistakes.

---

## 2026-05-22 — GitHub marketplace sync setup

### Observation: Cowork GitHub sync requires directory-based plugins, not zip files

**What happened:** Matt tried to set up `Newry-LLC/newry-ai-tools` as a Cowork plugin marketplace. Initial `marketplace.json` schema had two errors: (1) `plugins[].name` field missing; (2) `owner` was a string (`"Newry-LLC"`) instead of an object (`{"name": "Newry-LLC"}`). Required three rounds of error messages to get to a working schema.

**Root cause:** Cowork's marketplace schema is not publicly documented. Cowork GitHub sync only supports directory-based plugins (each plugin is a folder with `.claude-plugin/plugin.json` + `skills/`). Zip files (`.plugin`) are for manual upload only. This is a non-obvious distinction.

**Fix:** Replaced all zip file references in the repo with `plugins/<name>/` source directories. Each plugin directory has `.claude-plugin/plugin.json` with `name`, `version`, `description`, `author` fields. `marketplace.json` lives at `.claude-plugin/marketplace.json` with correct schema including `owner` as object.

**Portable principle:** When setting up a GitHub-synced plugin marketplace, the `owner` field must be `{"name": "org-name"}` (object), not `"org-name"` (string). And every plugin entry needs both `name` and `source` fields.

---

## 2026-05-18 — `newry-knowledge` coordinator redesign

### Observation: Bandaid accumulation — coordinator had four routing types + Adaptive + Neither case

**What happened:** Over several sessions the coordinator SKILL.md had accumulated: four routing types (AT-primary, SP-primary, both-simultaneous, adaptive fallback), a "Neither" case, negative examples to suppress false positives on T17/T19, and multiple inline caveats. Each fix solved the immediate problem but the design was brittle — adding another routing type or edge case would have made it worse.

**Root cause:** Each improvement patched the symptom (wrong skill fired) rather than asking why the routing decision was hard. The underlying issue: no gate before routing. The skill tried to route everything, including questions that should never trigger either skill. The fix was to add a gate first.

**Fix:** Full rewrite from first principles. Two questions: (1) Is this Newry-specific — could it be answered without any Newry documents? If no, answer from general knowledge. (2) What type of data answers it? AT = structured facts (contacts, project metadata, AER, staff expertise); SP = document content (deliverables, research, policies, templates, training). Both = only when the question explicitly requests both. This eliminated all the edge-case routing types.

**Results:** 19/20 trigger tests pass. T14 ("What industry has Newry worked in the most?") is a known AT limitation (search_records can't aggregate) — not a coordinator routing failure.

**Portable principle:** When a skill accumulates multiple patches for edge cases, the correct response is to redesign the classification logic from first principles, not add another branch. Bandaids compound; a clean gate eliminates a whole class of failures.

---

## 2026-05-18 — `newry-knowledge` trigger tests — first full run

### Observation: Trigger tests reveal coordinator routing behavior end-to-end

**What happened:** Ran all 20 trigger test cases with v1.1.14 coordinator installed. Pre-rewrite, T17 ("What is a market sizing model?") and T19 ("What is Corning's business strategy?") both incorrectly triggered sharepoint-search. Post-rewrite gate, both route correctly to neither (answer from general knowledge).

**Result summary:**
- T01–T07: sharepoint-search only — all pass
- T08: sharepoint-search (SP prior-work sweep; AT metadata too spotty for domain coverage) — pass
- T09–T14: airtable-search — 5/6 pass; T14 aggregate query is AT limitation, not routing failure
- T15–T16: both — pass
- T17, T19: neither — pass (post-rewrite gate fix)
- T18, T20: sharepoint-search — pass

**Portable principle:** Run trigger tests after any coordinator change. Routing failures are invisible without explicit test cases — the skill appears to work on happy-path demos even when it fires on questions it shouldn't.

---

## 2026-05-12 — `newry-knowledge` eval suite expansion

### Observation: Eval coverage was limited to 3 happy-path point lookups

**What happened:** Original evals.json had 3 cases, all testing the same pattern (find document, return content). Every behavior added since v1.0.0 — parallel search, snip-then-stop, query reformulation, completeness check, query interpretation, prior-work sweep redesign, dead-end paths, source context, airtable-search — had zero eval coverage.

**Root cause:** Evals were written at launch to test basic function, not updated as the skill evolved. Each improvement was shipped without a corresponding eval case.

**Fix:** Expanded evals.json to 20 cases across both skills. Added trigger-tests.json (20 cases) for trigger quality testing. Going forward: any skill change should include a new eval case or an update to an existing one.

**What the new evals cover:**
- sharepoint-search: snip-then-stop, parallel synthesis/sweep, keyword-first prior-work sweep, multi-part completeness, query reformulation, query interpretation (fires vs. skips), targeted first search, source context in attribution, warm dead-ends
- airtable-search: connector check, prior project lookup, AER mining (thematic synthesis), AER mining (what goes wrong), client contact lookup, staff expertise lookup, specific project lookup
- trigger-tests.json: 7 sharepoint-only, 7 airtable-only, 2 both, 4 neither/edge cases

**Portable principle:** Eval coverage is not automatic — it requires a deliberate step at skill-change time. Without it, improvements are unverified and regressions are invisible.

---

## 2026-05-06 — `newry-knowledge:sharepoint-search`

### Observation 1: Large file fallback
**What happened:** The consolidated Alta internal interview notes file (`All Internal Interview Notes - Anna.docx`) had grown large enough to truncate on `read_resource`. An earlier eval that passed (CIPP interviewees) had used this file when it was smaller. The re-run failed to find all three interviewees until the skill fell back to individual files.

**Root cause:** No guidance existed for what to do when `read_resource` returned a truncated result.

**Fix:** Added "Large file fallback" guidance to Step 3: when truncation occurs, switch to individual files rather than retrying the consolidated doc.

---

### Observation 2: Query classification
**What happened:** For an Alta project status question, the first run defaulted to a single-document read rather than sweeping across folder types. The second run (after skill update) surfaced the live DRAFT biweekly deck modified that day — a much better answer.

**Root cause:** No guidance distinguished synthesis/sweep questions (which need multi-folder fan-out) from point lookups (which need one targeted read).

**Fix:** Added Step 0 classification — point lookup vs. existence check vs. synthesis/sweep — with explicit strategy for each type.

---

### Observation 3: Multi-part question coverage
**What happened:** The demo question "Which interviewees mentioned AOC, Reichhold, Ashland — and what did they say about competitive positioning?" had four distinct parts. The skill answered the synthesis component (what they said) by reading 4 files, but never surfaced the full enumeration (which of the 70 interviewees mentioned each competitor). 15 files total were indexed for competitor mentions; only 4 were read. The user never saw the full list.

**Root cause:** No mechanism to decompose multi-part questions before searching. The skill defaulted to the most tractable component (synthesis) and let it absorb the enumeration component.

**Fix:** Added Step 0.5 — explicit decomposition of multi-part questions before searching. Rule: enumeration components ("which," "who," "how many") must be answered fully from search results before reading anything. Scope must be confirmed with the user if >3–4 files would need to be read for synthesis. Final answer must check off every decomposed part.

---

### Observation 4: Enumeration + synthesis scope confirmation
**What happened:** Related to Obs 3. Even if the skill had surfaced all 15 files, silently reading all 15 would have been its own problem. The right behavior is: surface the full list, then let the user decide how deep to go.

**Root cause:** Same as Obs 3 — no decomposition step, no scope confirmation gate.

**Fix:** Covered by the Step 0.5 addition above. The 3–4 file threshold is the practical trigger for pausing and confirming scope.

---

### Observation 5: Prior-work sweep — keyword search is unreliable for whole-corpus coverage
**What happened:** Demo Q2 asked "Has Newry done prior work in composites, specialty chemicals, or thermoset resins?" Keyword search returned Teckrez and Edgewater but missed Norplex-Micarta (a direct composites laminates client from May 2025), Chase Corporation, Collano AG, and NeoGraf Solutions — all active clients that were invisible to keyword queries.

**Root cause:** `sharepoint_search` returns ranked top-N results. For a targeted query it's reliable; for a whole-corpus coverage question ("what clients have we served in domain X"), it's unreliable because relevant clients are named after companies, not domains. A folder containing nothing but a Norplex-Micarta deliverable will not surface on a search for "composites." The skill had no guidance for this question type.

**Fix:** Added "Prior-work sweep" as a fourth question type in Step 0. Correct pattern: (1) call `sharepoint_folder_search` with `"Clients"` to get the exhaustive client list (folder enumeration is not ranked — it's complete), (2) apply LLM domain knowledge to filter which client names are relevant to the domain in question, (3) run targeted `sharepoint_search` within those client folders to confirm scope and surface specifics. Also added `sharepoint_folder_search` to the tools list and a prior-work sweep example.

---

## Template for future entries

```
## YYYY-MM-DD — `skill-name`

### Observation N: [short title]
**What happened:** [describe the miss or insight]
**Root cause:** [why did this happen — skill gap, prompt gap, design gap?]
**Fix:** [what was changed, or what should be changed]
```


---

## 2026-05-08 — `primary-research-toolkit:research-plan-design`

### Observation: Internal corpus coverage does not transfer to external research planning

**What happened:** In Chunk 1 of a Research Plan Design run for ALTA01, Claude classified Branch A6 (Technical fit / right to win) and the Foundational branch as Secondary, citing the existing v6 ICS corpus (55 internal Alta sales/ops interviews) as partial coverage. The consultant flagged this immediately: internal interviews are inside-out — they reflect what Alta's team believes about the market, not what the market actually thinks. They do not constitute coverage for any branch in an external research plan.

**Why it happened:** The SKILL.md had no guidance on how to treat an existing ICS corpus when building a new research plan. The decision rule for branch classification only referenced SOW deliverables and scope — not interviewee type mix. Claude filled the gap with plausible-but-wrong reasoning.

**The fix:** Two targeted edits to `sub-skills/research-plan-design/SKILL.md`:
- Step 1 "Also look for": added interviewee-type check — if existing corpus is internal-only, treat every branch as starting from zero for external planning
- Chunk 1 decision rule: added explicit rule — internal-only corpus does not reduce branch priority; do not downgrade on this basis

**Portable principle:** When a skill uses prior run outputs as context inputs, it must track *what type of sources* those outputs came from — not just *that coverage exists*. Source type determines whether coverage transfers. This applies anywhere a skill might inherit results from a prior pass (ICS → Research Plan Design, ICS Round 1 → Round 2 delta, etc.).

---

## 2026-05-08 — `primary-research-toolkit:interview-coding-synthesis`

### Observation 1: Required outputs not checked at session close

**What happened:** Three required outputs were not produced during the ALTA01 Run 2 ICS session and had to be built retroactively after the user flagged each one:
1. `Summary Cards v1.docx` — SKILL specifies "append to a single project Word doc as interviews are processed"
2. `Interview Matrix v1.xlsx` — SKILL specifies matrix update after each card: branch rows, question rows, emerging topics, Dashboard, segmentation tabs
3. Both were caught only when the user asked; no self-check was run at session close

**Root cause:** No end-of-session outputs checklist. The SKILL describes each output in its relevant section but there is no single place that enumerates everything expected and triggers a verification pass before reporting completion.

**Fix:** Add a "Required outputs checklist" section to SKILL.md (after Mode 2 output section, before Step 5 Logging) listing all expected artifacts per mode. Skill must verify each item exists before closing any ICS session. Missing items are produced immediately, not flagged for later.

---

### Observation 2: Batched Mode 1 breaks the per-card matrix update pattern

**What happened:** The SKILL specifies updating the Interview Matrix after each card. In a batched run (76 transcripts, 14 parallel sub-batches), this is not feasible — agents can't write to a shared Excel file concurrently, and the matrix didn't exist yet at batch time.

**Root cause:** The SKILL was written for sequential single-transcript Mode 1. No guidance existed for how to handle matrix population when running parallel batches.

**Fix:** Add a "Batched runs" note to the Mode 1 Matrix update block. Correct pattern: (1) initialize the matrix workbook before batches begin — branch rows, question rows from the interview guide, empty Emerging Topics, interviewee columns from the metadata tracker; (2) populate branch coverage rows in bulk after all Mode 1 cards complete, using the Pass 1 route index as the source; (3) approximate question rows from branch coverage; (4) populate Emerging Topics from Pass 2 OIT cross-tab flags. Matrix is complete before Mode 2 begins.

**Portable principle:** When a skill has an "update X as you go" pattern, it needs an explicit fallback for batched/parallel execution — otherwise the pattern silently fails and the output is missing entirely.

---

### Observation 4: Interview guide questions not extracted as a structured artifact during setup

**What happened:** During project setup, the interview guide docx was read for context but the question list was never extracted and saved. When the matrix build needed numbered questions, they were re-parsed on the fly from the docx. Works, but leaves the project less self-contained — anyone picking it up mid-run has to re-find and re-parse the guide.

**Root cause:** No step in the ICS setup sequence says "extract and save questions from the interview guide." The guide was treated as read-only reference material, not as a source of structured data to persist.

**Fix:** Add to ICS Step 1 (project setup): after reading the interview guide, write `questions.md` to the project root — numbered questions grouped by section, extracted from the guide. This file is then referenced by the matrix build (question rows) and Mode 1 cards (Q coverage), making the project self-contained without re-parsing the source docx on every run.

---

### Observation 3: Segmentation tab formulas fail without a metadata row

**What happened:** The By Type and By Geography tabs in the Interview Matrix were built with correct column headers but all-zero values. The agent wrote COUNTIF formulas intended to reference a "type" metadata row in the Matrix tab, but no such row exists — interviewee type is only in the route file's register, not embedded in the Matrix itself.

**Root cause:** The SKILL gave no guidance on how to implement the segmentation tabs technically. The agent defaulted to a COUNTIF approach that assumed a metadata row it couldn't find, wrote empty formulas, and reported completion without verifying the output.

**Fix:** Add explicit implementation guidance to the Matrix build instructions: segmentation tabs must be computed in Python by mapping each interviewee column index to its type/geography from the interviewee register, writing integer counts directly (not formulas). Add a totals row (bold, dark blue) at the bottom of each summary tab. Verify non-zero values before reporting completion.

---

## 2026-05-08 — `primary-research-toolkit:interview-coding-synthesis` + `preprocess.py`

### Observation 5: preprocess.py not invoked — SKILL describes in-context steps instead of script call

**What happened:** preprocess.py was not run during ALTA01 Run 2. The v6 run (which explicitly ran the script) achieved 0% Low attribution across 55 transcripts. Run 2 (which skipped it) produced 14.3% Low. Both runs used the same SKILL.

**Root cause:** SKILL.md Step 2b describes preprocessing as a set of in-context analytical steps ("identify input quality", "segment into exchange units", etc.) rather than saying "run preprocess.py." Batched card agents did informal inline speaker resolution instead of using the structured script output. The script existed and worked — it just wasn't referenced.

**Fix:** Replace Step 2b in-context description with an explicit script invocation: "Run preprocess.py against the transcript folder. Feed `.preprocessed.md` files to card agents instead of raw transcripts."

**Portable principle:** If a script exists to automate a step, the SKILL must reference it explicitly. Describing the step's logic in prose does not cause the agent to use the script — it causes the agent to replicate the logic informally, with lower consistency.

---

### Observation 6: Input type categories too granular in the wrong dimension

**What happened:** preprocess.py uses 4 input-type categories (verbatim, lightly edited, synthesized notes, rough bullets). Sylvan confirmed the right categories are 3: transcripts, synthesized notes, rough notes. "Lightly edited" is not a meaningful distinction in practice.

**Root cause:** The 4-category system was designed defensively for a general-purpose tool. Newry's workflow doesn't produce "lightly edited transcripts" as a distinct category.

**Fix:** Collapse to 3 categories in preprocess.py. Add within-transcript quality assessment (speaker label resolution, completeness signals, turn structure) as the granularity dimension within the transcript category — since that's where meaningful attribution variation actually lives.

**Portable principle:** Input categories should reflect how inputs actually arrive in the workflow, not every theoretically possible format. Over-categorization dilutes the signal on dimensions that matter.

---

### Observation 7: Alternation heuristic is broken for Otter and should be removed

**What happened:** preprocess.py's speaker resolution cascade falls back to alternation (first turn = interviewer, alternating thereafter) as a last resort. This produces incorrect speaker assignments for Otter transcripts because Otter frequently splits a single speaker's continuous narrative into multiple consecutive turns — alternation then assigns wrong roles mid-monologue.

**Root cause:** Alternation is a reasonable heuristic for clean two-party transcripts. It fails for Otter because Otter's splitting behavior is independent of actual speaker changes.

**Fix:** Remove alternation entirely. If the cascade (name match → intro-spiel anchor → aggregate-words) fails to resolve speakers, flag the transcript for LLM re-diarization and mark attribution as Low. Do not produce misleading speaker assignments.

**Portable principle:** A fallback that produces confidently wrong output is worse than no fallback. Better to flag for human/LLM intervention than to silently misattribute.

---

## 2026-05-09 — `design:design-critique`

### Observation 8: Design critique skill misses strategic design decisions, catches only implementation issues

**What happened:** Used `design:design-critique` on slide 1 of the PRT consultant deck (Primary Research Workflow). The critique surfaced implementation issues (text wrapping, size contrast, column density imbalance) correctly. It did not flag the structural design problems that were the actual root cause of quality: the inputs column was wrong for this audience, the output row was framed as tool artifacts rather than consultant work products, and step numbers made the slide read as a process diagram rather than a description of daily work. Sylvan's 10-minute manual redesign was directionally better than multiple AI critique rounds.

**Root cause:** The design:design-critique plugin is a general-purpose product design tool calibrated for UI/UX work (buttons, flows, screens). Consultant presentation design has a different quality standard — information architecture, audience framing, and "what to leave out" are the hard decisions. The plugin has no frame for those.

**Fix:** Do not use design:design-critique as the quality gate for Newry consultant presentations. Backlog item: build a purpose-built `newry:presentation-critique` skill calibrated to Newry's slide standards (Pyramid Principle framing, message-driven titles, appropriate information density for a partner-facing deck).

**Portable principle:** A critique tool is only as good as its calibration target. General-purpose design critique catches implementation noise but misses the strategic signal that matters most for specialist audiences.
