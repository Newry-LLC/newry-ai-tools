---
name: prt-interview-coding-synthesis
description: Use this sub-skill to code interview transcripts against a project's analytical frame and synthesize findings across the corpus. Produces summary cards per interview (Mode 1) and a Roll-up across the full corpus (Mode 2). Part of the Primary Research Toolkit. Triggers on "I have transcripts to code," "synthesize these interviews," "build summary cards," "create a roll-up," "code and synthesize these interviews."
---

# Primary Research Toolkit — Interview Coding & Synthesis

A skill for coding interview transcripts against a project's analytical frame and synthesizing findings across the corpus. Produces branch-mapped summary cards (Single mode) and aggregated patterns, contradictions, and emergent themes (Roll-up mode) with full source attribution.

**What this skill does not do:** draw conclusions, make recommendations, prioritize findings, assess commercial attractiveness or strategic fit, or resolve contradictions between sources. That is the consultant's job.

The workflow runs five steps. Step 1 (Scope conversation) is the only user-facing gate. Steps 2a, 2b, 3 are non-interactive and complete in the same response as Step 1's initial scope read; they report judgment calls in a Decisions made section at the end of the output, so corrections happen after the fact rather than via mid-run prompts.

---

## Output discipline

- **Pre-flight echo at the top of every output.** Before any synthesis content, emit a 4–6 line block reporting what the skill found and is acting on. This catches wrong-folder or wrong-input mistakes before the consultant scrolls through the synthesis. Format:

  ```
  **Pre-flight**

  - Corpus: [N] transcripts ([file types — e.g., "10 .docx"])
  - Scope: see Section 1a (locked from Step 1)
  - Glossary: [N entries at <path> | created on this run]
  - Prior Roll-up: [used for delta from <date> | none]
  - Pre-flight warnings: [bullet list, or "none"]
  ```

  Pre-flight warnings include: missing or unmatched interviewee metadata, transcripts that couldn't be parsed, glossary not found in the expected location, prior Roll-up provided but doesn't match the locked scope. Pre-flight is informational — it does NOT gate the run. It does not ask "is this right? proceed?" Just report what was seen and continue.

- **Output ends at Decisions made — except for a single static trailer.** Do not append next-step menus, "what would you like to do" prompts, or other post-result decision invitations. Present results, surface decisions, then emit one static trailer line naming what was produced and the natural next step. Form: `Output saved at <path>. Next typical step: <one short statement>.` The trailer is a pointer, not a question. No follow-up prompt. Examples:
  - Mode 1: `Summary card appended to <path>. Next typical step: continue with remaining transcripts, then run Mode 2 (Roll-up) when the corpus is complete.`
  - Mode 2: `Roll-up saved at <path>. Next typical step: review Decisions made, then re-run with new interviews if more rounds are planned, or hand to SoF Toolkit Draft mode.`

- **Suppress technical noise.** Internal mechanics (Q&A segmentation logic, per-passage substantive flags, regex detection details, file-loading minutiae) are working state, not user-facing output. Decisions made surfaces only what the consultant needs to act on: input quality per transcript, attribution warnings, speaker resolution calls that affect quote reliability, file mapping calls, scope/branch interpretation, term fixes.

---

## Feedback capture

Handled at the coordinator level — see the coordinator's Feedback capture section. Log to `Primary Research/logs/feedback-log.md`. Acknowledge briefly and continue; do not pause the run.

---

## What you need before starting

**Required:** an analytical frame (issue tree preferred; SOW, kickoff deck, proposal, or research questions also workable, with more interpretive work to extract questions and scope) and transcripts or notes (.txt, .md, .docx — folders recursed; combined files auto-split; .docx body text and tables read, tracked changes and comments skipped and noted). Input category (transcript / synthesized notes / rough notes) affects attribution reliability and is declared in every output.

**Attribution levels** declared in every card header:
- **High** — transcript with confirmed speaker identification (name match or intro-spiel anchor). Quotable verbatim.
- **Medium** — transcript with inferred speaker identification (aggregate-words resolved), or synthesized notes. Attributable but paraphrase in Roll-up.
- **Low** — transcript where speaker resolution failed (flagged for LLM re-diarization), or rough notes. Paraphrase only; note limitation.

**Useful:** interview guide / research questions (most important when working from synthesized notes, where the original question is often not visible in the text; standardized question stems in the guide are also used to identify questions for cross-tab treatment in Mode 2), and interviewee metadata — type (internal staff / customer / SME / competitive intel / other), name, role, company, company type or segment (e.g., Tier 1 distributor, regional OEM, national chain), geography/region (e.g., NA, EU, APAC, or more granular), seniority level (C-suite, VP, Director, Manager, IC), date, ID, blind status. More metadata improves summary card headers, the Interviewee Index, and cross-tabulation claims. Filename ↔ person matching is auto-attempted; mismatches surface in Decisions made.

**Hard stop:** if no analytical frame is found in `context/`, do not ask for one inline — direct the user to add project documents (SOW, proposal, kickoff deck, interview guide) to the project's `context/` folder and re-run. The project setup step is where framing documents should have been placed. If transcripts are missing (expected at `Primary Research/materials/`), ask for them before proceeding.

---

## Format conventions

Apply across all synthesis output (Mode 1 summary cards, Mode 2 Roll-up).

- **Pyramid principle.** Every finding bullet leads with a bolded headline that delivers the strategic verdict, not a description of the topic. The reader should be able to scan only the bolded leads and get the verdict.

  *Calibration — headlines must deliver verdicts, not describe topics:*
  - ✓ "CIPP, utility poles, and composite rebar are execution-constrained, not demand-constrained — the gaps are a blend tank, a pultrusion lab, and a proactive commercial posture." (named specifics + verdict + mechanism)
  - ✓ "Phase 2 pricing targets $20–30M of additional annual EBITDA — the largest single identified lever, with Phase 1 already delivering ~$20M/yr ahead of schedule." (specific figure + unit + comparative grounding)
  - ✗ "Commercial execution challenges" (topic label — says what it's about, not what the corpus says)
  - ✗ "Customer feedback on pricing" (topic label)

- **4–6 dense bullets — hard cap. Synthesize, don't enumerate.** Per summary card, per Roll-up branch, per Summary of findings. Combine related facts into one dense bullet rather than splitting them. If you have 8 bullets, combine the weakest two pairs. Do not exceed 6 under any circumstance, including large corpora.
- **Quote where the interviewee's phrasing is sharp.** Verbatim or near-verbatim citation form (direct text from the transcript) for high-impact claims; paraphrase otherwise. Low-attribution sources: paraphrase only.
- **Preserve card language for quantitative claims and named mechanisms.** When a summary card states a specific figure (dollar amounts, volumes, percentages, timeframes) or names a mechanism, program, or target, carry that language forward verbatim into the Roll-up. Do not paraphrase quantitative claims — paraphrasing drops units, loses precision, and replaces sharp source language with vaguer reconstruction. If the card says "$50M annualized, ~25% of current $200M EBITDA," the Roll-up says that, not "a significant EBITDA improvement."
- **Citations.** `[IS-NN: Name]` format inline — name included so the reader doesn't have to flip to the index. List 4–8 most representative when the corpus has many sources for one finding.
- **Branch ID** in parens at the end of each Mode 1 finding bullet — canonical ID (A, B1, B2, foundational, etc.).
- **Cross-tabulation claims.** When a finding appears in multiple interviewee types and the distribution is meaningfully uneven — i.e., the split is part of the story — make it explicit. Inline form: "cited by 5 of 8 distributors, 3 of 5 OEMs, and 1 of 4 end-users." Table form when distribution is the main message:

  | Type | Cited | Total |
  |------|-------|-------|
  | Distributor | 5 | 8 |
  | OEM | 3 | 5 |
  | End-user | 1 | 4 |

  Use when: (a) the finding appears in 3+ cards and (b) type distribution varies meaningfully (one type heavily cited, another absent or opposite). Do not produce cross-tabs when all types show similar distributions — inline citation is sufficient. Cross-tab dimensions: interviewee type, company type/segment, geography, seniority — use whichever cut tells the story.

---

## Step 1: Scope conversation

Surface a tight read on frame + branches + in/out + ambiguous edges. Default output is the nested-bullet scope display:

```
- **<Top question>**
  - **A. <Branch>**
  - **B. <Branch>**
    - B1. <Sub-branch>
    - B2. <Sub-branch>
  - *Foundational diagnostic* (trunk, not a branch) — <one-line note>
  - *Out of scope* — <list>
  - *Outside the Issue Tree* — captured separately
```

Escalate to a focused question only when an edge is genuinely ambiguous. Lock on user go-ahead. Record the locked scope display verbatim at the top of every output (per-card in Mode 1, in a dedicated Section 1a in Mode 2) and in the run log.

**Interview guide questions** — if an interview guide is present in `context/`, extract the question list during Step 1 and write it to `<project-root>/Primary Research/questions.md` — numbered questions grouped by section. Do this once at project setup; subsequent runs read from `Primary Research/questions.md` rather than re-parsing the docx. This file is used for question rows in the Interview Matrix and Q-coverage tracking in Mode 1 cards.

**Corpus planning** — surface alongside the scope display when the corpus has >15 transcripts or mixed source types. State recommendations; don't ask questions. User confirms scope + corpus plan together.

- **Batching (>15 transcripts):** recommend splitting Mode 1 into batches of ~15–20. Propose named batches based on interviewee type first, then geography or function (e.g., "Batch A — NA Commercial, ~20 transcripts"). If metadata is unavailable, split by folder or file order.
- **Mixed source types:** recommend running all types together — interviewee type coding and cross-tab handle the distinction, and one Roll-up is more useful than separate ones the team must reconcile manually.

---

## Step 2a: Load and split

### File loading

- Accept folder paths (recursed) or file lists.
- Read .txt, .md, and .docx natively. For .docx: extract body text and tables (preserving row order — some templates put Q/A in tables); skip tracked changes and comments and note their presence; skip headers/footers unless they contain metadata.
- Preserve speaker labels and paragraph breaks.

### Combined-file detection

A single file may contain multiple interviews. Boundary signals to look for:
- Explicit headers ("Interview 1:", "Call with [Name] —", date+name patterns at section breaks)
- Heading styles (Heading 1 / Heading 2 in .docx)
- Horizontal rules
- Repeated metadata blocks (e.g., a recurring "Date / Interviewee / Role" block)

Split on best inference. Boundaries that required uncertain calls are reported in Decisions made for review.

### Filename ↔ person matching

When interviewee metadata is provided, auto-match filenames to people. Common patterns: "01 - John Smith - 2026-04-15.docx", "Smith_interview.txt", "<Project>_IS_Smith.docx". Confirmed matches feed the Interviewee Index. Ambiguous or unmatched files appear in Decisions made.

---

## Step 2b: Per-transcript pre-processing

`preprocess.py` is required. Do not proceed to card generation without it — raw transcripts produce unreliable attribution and lower synthesis quality.

**Locate the script:** it is bundled with the PRT plugin at `../../scripts/preprocess.py` relative to this sub-skill's directory (two levels up from `sub-skills/interview-coding-synthesis/`). If it is not found at that path:
1. Search for it within the plugin directory
2. If found elsewhere, copy it to `../../scripts/preprocess.py` and proceed
3. If not found at all, stop and tell the consultant: "I can't locate `preprocess.py` — this script is required and should be bundled with the PRT plugin. It may not have been installed correctly. Please reinstall the PRT plugin and try again."

Run the script against the transcript folder:

```bash
python ../../scripts/preprocess.py \
  --input <transcripts-folder> \
  --output <project-root>/Primary Research/preprocessed \
  --metadata <project-root>/Primary Research/metadata.json   # optional but recommended
```

Feed the resulting `.preprocessed.md` files to card agents instead of raw transcripts. The script handles:
- **Input category detection** — transcript / synthesized notes / rough notes
- **Speaker resolution cascade** — name match → intro-spiel anchor → aggregate-words fallback → resolution failure (flagged for LLM re-diarization). No alternation heuristic.
- **Attribution assignment** — High / Medium / Low based on category + resolution outcome
- **Exchange-unit segmentation** — groups turns into substantive Q&A units; strips backchannels and logistics
- **Non-substantive flagging** — marks intro spiel, pleasantries, and closing exchanges

After running, check `Primary Research/preprocessed/INDEX.md` for any transcripts flagged for LLM re-diarization (attribution = Low, speaker resolution failed). Run LLM re-diarization on those files before proceeding to card generation — do not generate cards from unresolved Low-attribution transcripts if avoidable.

**Extract interviewee demographic fields** from each preprocessed file header or metadata: company, company type/segment, geography/region, seniority level. Infer from job title and company name if not stated explicitly; flag as inferred in Decisions made. Required for cross-tabulation in Mode 2.

---

## Step 3: Term reconciliation

### When it runs vs. skips

- **Transcript** — full pass.
- **Synthesized notes / rough notes** — skip entirely.

### Glossary

Stored at `<project-root>/Primary Research/glossary.md` (inside the Primary Research folder — travels with the project). Three states per term:
- **Confirmed correction** — auto-apply forever in this project (e.g., altar → Alta)
- **Confirmed non-correction** — never flag again (e.g., "altar" is literal in a church-renovation client)
- **Pending** — surfaces for review or is auto-applied per the matrix below

On first run for a project, the skill seeds the glossary from:
- Project / client name
- Interviewee names from metadata
- Branch labels and key concepts from the analytical frame
- Acronyms and proper nouns appearing in the SOW or issue tree

Subsequent runs reuse and grow the glossary; review surface area drops sharply after run #1.

### Detection categories

- Proper nouns mistranscribed as common words (people, companies, products, geographies, named competitors)
- Industry / technical jargon drifted (e.g., "polly silicon" → "polysilicon")
- Repeated odd words across transcripts — strong signal it's the same misheard term
- Acronyms misexpanded or split
- Out-of-distribution words that don't fit project context

Speech disfluencies, filler, and grammar are not touched. Anything ambiguous without project-context evidence is flagged separately as "review only," not "suggested replacement."

### Impact × confidence matrix

| Impact × Confidence | Action |
|---|---|
| High-confidence, **any** impact | Auto-apply (logged in Decisions made, grouped by canonical fix) |
| Med/Low confidence, high-impact | Best-inference applied, surfaced in Decisions made for review |
| Med/Low confidence, low-impact | Skipped (counted in the log, not surfaced) |

**High-impact** = proper nouns; terms that appear in the analytical frame; words inside passages that map to a branch finding; words inside quoted phrases.

**Low-impact** = generic words in passages not mapped to any branch; words inside passages flagged non-substantive in Step 2b.

Working copies of transcripts carry auto-applied fixes; originals are untouched. The glossary file is updated with new confirmed entries.

---

## Step 4: Synthesis

After scope is locked and Steps 2a/2b/3 complete, run synthesis. There are two modes — Mode 1 (Single summary card) and Mode 2 (corpus Roll-up) — and the canonical workflow uses both.

**Default workflow: cards-first, then Roll-up.** When the corpus has more than one transcript, run Mode 1 on every transcript first, then run Mode 2 against the resulting cards rather than against raw transcripts.

**When to skip cards and go straight to Roll-up:** corpus is so small (≤3 transcripts) that per-transcript artifacts cover everything the Roll-up would say. In that case, run Mode 1 only and skip Mode 2.

**Minimum for reliable patterns in Roll-up: 5 transcripts.** Below 5, flag all pattern and count claims as directional, not evidential.

### Mode 1: Single

Used per transcript. Produces a compact summary card — one record per interview, appended to a single project summary-cards Word doc as interviews are processed. Most valuable for raw transcripts and rough notes; also useful for synthesized notes where the goal is branch-mapped structuring before Roll-up.

#### Process

1. Assess coverage: for each branch, determine whether the transcript addresses it substantively (✓), partially / in passing (~), or not at all (—).
2. Extract all findings that directly address a branch question — every specific, named, or attributable claim. Order by rough importance (most specific and actionable first), not by branch.
3. **Always identify and surface exchanges that don't map to any branch — never skip.** These are unexpected findings.

Do not produce branch-by-branch sections. Do not include absence claims in the findings list — use the coverage table instead.

#### Output

Mode 1 coverage is a simplified 2-column view; Mode 2 uses the full coverage table with What-it-covers and substantive/partial/none counts.

```
> [Name] | [Role] | [Company] | [Type] | [Geography] | [Seniority] | [Date]
> Input quality: [verbatim / synthesized notes / rough bullets] | Attribution: [High / Medium / Low]

**Locked scope (verbatim from Step 1):**

- **<Top question>**
  - **A. <Branch>**
  - **B. <Branch>**
    - B1. <Sub-branch>
  - *Foundational diagnostic* (trunk, not a branch) — <one-line note>
  - *Out of scope* — <list>
  - *Outside the Issue Tree* — captured separately

## Coverage

| Branch | Coverage |
|---|---|
| [Branch label] | ✓ / ~ / — |
...

✓ Substantive  ~ Partial / mentioned  — Not addressed

## Issue Tree Findings

- **[Headline message — the strategic frame, not the topic]** — [supporting detail, named entities, quote where available] (Branch ID)
- **[Next headline]** — [evidence and detail] (Branch ID)
- ...

## Unexpected / Outside the Issue Tree

- **[Finding headline]** — [supporting detail]

## Decisions made

Lightweight per-card version — full template applies in Mode 2 only.

- Term fixes applied: [count + brief list]
- [Any boundary, matching, or interpretation calls worth noting]
```

Apply Format conventions. One record per interview. Append to the project Word doc as interviews are processed.

Note on claim types: findings in Single output are implicitly Type 1 (direct, named, specific). Pattern claims (Type 2/3) and synthesis observations (Type 4) belong in Roll-up, not Single.

#### Matrix update

After producing the summary card, update `Primary Research/outputs/Interview Matrix v1.xlsx`:

1. **Locate the interviewee's column** by matching their name and interviewee code. If no column exists yet, add one with the interviewee name and code as the header.
2. **Fill branch rows** — enter ✓/~/— for each branch based on the coverage table just produced in the summary card.
3. **Fill question rows** — enter ✓/~/— for each interview guide question based on whether the transcript substantively addressed it (✓), touched on it (~/mentioned), or did not address it (—).
4. **Emerging topics** — for any finding in the Unexpected / Outside the Issue Tree section, check whether a row already exists in the Emerging topics section of the matrix. If yes, mark ✓ for this interviewee. If no, add a new row with the theme label and mark ✓. Count the ✓s across the row — if 3 or more interviewees have now covered this theme, flag it as a promotion candidate: move the row into the main matrix (below the question rows, above the Emerging topics section) and note in Decisions made.
5. **Update Dashboard tab** — recalculate ✓, ~, — counts for each row.
6. **Update segmentation tabs** — refresh value chain and interviewee type tabs by pulling updated counts from the matrix and interviewee metadata from the pipeline tracker.

Report the matrix update in one line at the end of Decisions made: `Matrix updated — [N] branch rows, [N] question rows filled; [N] emerging topics added/promoted.`

**Batched runs:** When Mode 1 runs in parallel batches (corpus >15 transcripts), per-card matrix updates are not feasible in real time. Instead:
1. **Initialize the matrix before the first batch** — create the workbook with branch rows, question rows from `Primary Research/questions.md`, and an empty Emerging Topics section. Populate interviewee columns from the metadata tracker.
2. **After all Mode 1 cards are complete, populate branch coverage rows in bulk** from the Pass 1 route index (which captures ✓/~/— per card per branch).
3. **Populate question rows** using branch coverage as a proxy. Note in the Dashboard tab that question rows are approximated from branch coverage.
4. **Populate Emerging Topics** from the OIT cross-tab flags in the Pass 2 extract file.

This sequencing — initialize before batches, populate after — is the correct workflow for large corpora. The matrix is complete before Mode 2 begins.

**Segmentation tabs (By Type, By Geography):** do NOT use COUNTIF formulas referencing a metadata row — the Matrix tab has no such row. Compute counts directly in Python by mapping each interviewee column to its type and geography from the interviewee register, then write hardcoded integer values. Add a totals row (bold, dark blue background) at the bottom of each summary tab. Verify non-zero values before reporting completion.

### Mode 2: Roll-up

Used to synthesize N transcripts against the analytical frame after Mode 1 has produced a card per transcript. The Roll-up reads from the cards (Type 1 findings, coverage assessments, Outside the Issue Tree items) and aggregates rather than re-reading transcripts. Pattern claims (Type 2/3) and synthesis observations (Type 4) are introduced here, with each pattern claim resolving back to specific cited cards.

#### Process — 4-pass pipeline

Mode 2 runs in four sequential passes. Each pass reads from files and writes to files; context resets cleanly between passes. Intermediate files live in `Primary Research/outputs/` alongside the final Roll-up.

**Pass 1: Route**
Read all summary cards in the corpus. Extract each card's coverage table. Build a branch-to-card index: for each branch, list which card IDs have ✓ or ~ coverage (exclude — only). Note interviewee type per card for source-distribution tracking.

Output: `Primary Research/outputs/mode2-route-<YYYY-MM-DD>.md` — branch-to-card index, one section per branch, listing card IDs and coverage level. Also record interviewee type, company type/segment, geography, and seniority per card — these are the cross-tab dimensions available in Pass 2.

This is a structured extraction pass. Do not write findings, verdicts, or synthesis.

**Pass 2: Extract**
For each branch (in route-index order):
- Load only the cards marked ✓ or ~ for that branch
- Extract only the finding bullets tagged with that branch ID, with full attribution preserved
- Record source distribution per branch: count, interviewee types, and type-level breakdown by company type/segment, geography, and seniority where available
- For each finding that appears in 3+ cards, note whether type distribution varies meaningfully — flag for cross-tab treatment in Pass 3
- Flag thin branches (fewer than 3 cards with substantive coverage) — carry forward as a gap note for Pass 3. For each thin branch, also record which interviewee types DID cover it and which are absent. Example: "B3 M&A: 6 ✓ cards, all R&D/scientist roles. Missing: ops leadership, corp dev, commercial. Recommended next-round sources: operations leader, CFO/corp dev, external M&A advisor." This source-type note travels into the Gaps subsection of that branch in Pass 3.
- Collect all Outside the Issue Tree items across all cards (for Pass 4)

Output: `Primary Research/outputs/mode2-extract-<YYYY-MM-DD>.md` — one section per branch containing only the relevant finding bullets with attribution; one section for Outside the Issue Tree items; source-distribution summary per branch.

This is a filtering pass. Do not write new findings, interpretations, or synthesis.

**Pass 3: Branch synthesis**
For each branch, load only its evidence bundle from the extract file — not the full cards, not other branches. Write the branch findings section:
- Apply Format conventions: pyramid principle headlines, 4–6 bullets (hard cap), citations
- For findings flagged for cross-tab treatment in Pass 2, produce a cross-tab claim (inline or table) per the Format conventions cross-tab format — choose the cut (type, company segment, geography, seniority) that tells the story
- Combine direct findings and patterns — do not split into labeled subsections
- Surface Contradictions where sources disagree (both sides; do not resolve)
- Write Gaps from thin-branch flags and coverage holes

Write one branch at a time. Append each section to `Primary Research/outputs/mode2-branches-<YYYY-MM-DD>.md`. Do not load other branches' bundles during a branch pass.

**Pass 4: Summary synthesis**
Load all branch findings sections from the branches file (not the original cards). Write:
- **Summary of findings** — main messages and cross-branch patterns: what the corpus delivers on the issue tree as a whole. Apply Format conventions: pyramid principle headlines, 4–6 bullets (hard cap).
- **Cross-branch commentary** — after writing main messages, scan across all branch findings sections for connections, tensions, or shared mechanisms that the branch-by-branch structure can't surface on its own. Write 2–4 observations as a named subsection. These are Type 4 synthesis observations — label each as interpretation, not finding. Examples: a pricing dynamic in B1 and a capacity constraint in B3 that point to the same root cause; a contradiction between what internal staff believe and what customers report across two separate branches. Omit if no meaningful cross-branch pattern exists — do not pad.
- **Outside the Issue Tree** — from the collected items in the extract file.
- **Cross-round delta** (only if a prior Roll-up exists in `Primary Research/outputs/`) — detect automatically; no user prompt needed. To find the prior Roll-up: sort Roll-up files in `Primary Research/outputs/` by the YYYY-MM-DD date in their filename; use the most recent one that predates today's run. If its locked scope differs from the current run's locked scope, note the mismatch in Decisions made and compare at branch level only — do not produce delta claims that assume matching scope. Compare the current Roll-up against the identified prior Roll-up:
  - For each branch: did the overall rating improve (—→~ or ~→✓), hold, or weaken?
  - Which branches gained substantive new evidence (new ✓ cards)?
  - Which outside-the-tree items are new this round vs. carried forward?
  - Are any prior findings no longer supported (cards removed or attribution dropped)?
  Lightweight — read branch ratings and outside-tree section from prior Roll-up only; do not re-read prior cards. Append as a named subsection **"Cross-round delta"** at the end of Summary of findings, before Outside the Issue Tree. Format: one bullet per changed branch + one for outside-tree additions. If no meaningful change, say so in one line. If no prior Roll-up exists, omit the section entirely — do not note its absence.

**Promotion candidates.** After writing Outside the Issue Tree, scan the collected OIT items. Any theme appearing in 3+ cards is a promotion candidate — it recurred often enough to warrant tracking as a formal branch in subsequent rounds. Flag these at the end of the Outside the Issue Tree section:

> **Promotion candidates:** [Theme] appeared in N cards ([IS-NN: Name], ...). To promote to a tracked code in subsequent rounds, say: "promote [theme] as [code label]."

If no OIT theme reached 3 cards, omit this block. See Emergent code promotion section for what happens when the consultant responds.

Assemble the final Roll-up from: corpus header + locked scope + coverage table (from route file) + summary of findings + branch findings (from branches file) + interviewee index + decisions made.

**Final Roll-up filename:** `Primary Research/outputs/[Project Name] Interview Roll-up v1.docx`. Increment the version number on re-runs (v2, v3, etc.).

#### Output

**Section order:**

```
1. Corpus header
1a. Locked scope display (nested bullet, verbatim from Step 1)
2. Coverage table
3. Summary of findings
   3a. Main messages
   3b. Cross-branch commentary (only when meaningful cross-branch patterns exist)
   3c. Cross-round delta (only when prior Roll-up exists)
   3d. Outside the Issue Tree
4. Branch findings
5. Interviewee index
6. Decisions made
```

---

##### 1. Corpus header

Render as a 2-column label/value table — clean and scannable. Avoid bulleted lists with bolded labels.

```
| | |
|---|---|
| **Project** | [Name] |
| **Transcripts** | [N — e.g., "40 internal interviews"] |
| **Interview dates** | [Range] |
| **Interviewee types** | [e.g., "Internal staff only — NA Commercial, NA Technical, EU Commercial"] |
| **Input quality** | [Verbatim / Synthesized notes / Mixed] — [attribution per source if mixed] |
| **Scope** | See Section 1a (Locked scope display) below |
| **Key limitation** | [Anything the reader needs to know about what the corpus does NOT cover — e.g., "Internal-only; no external voice-of-customer or competitive intelligence."] |
| **Decisions made** | [N] judgment calls — see Section 6 |
```

---

##### 1a. Locked scope display

Render the full nested-bullet scope display from Step 1, verbatim. This anchors every downstream section to the exact frame the synthesis was run against.

```
**Locked scope (verbatim from Step 1):**

- **<Top question>**
  - **A. <Branch>**
  - **B. <Branch>**
    - B1. <Sub-branch>
    - B2. <Sub-branch>
  - *Foundational diagnostic* (trunk, not a branch) — <one-line note>
  - *Out of scope* — <list>
  - *Outside the Issue Tree* — captured separately
```

---

##### 2. Coverage table

One row per branch. **Include a "What it covers" column** — concrete sub-topics drawn from the corpus, not abstract branch labels. This single column tells the reader what's actually inside the branch at a glance.

```
| Branch | What it covers | ✓ Sub. | ~ Partial | — Not addressed | Overall |
|--------|----------------|--------|-----------|-----------------|---------|
| **A — [Branch name]** | [Concrete sub-topics surfaced in the corpus, e.g., specific applications, product categories, customer segments] | N | N | N | ✓ / ~ / — |
| **B1 — [Sub-branch name]** | [Sub-topics surfaced in the corpus] | N | N | N | ✓ / ~ / — |
...
```

If Research Plan Design provided priorities, replace "What it covers" with "Priority" + "What it covers" as separate columns. Overall rating reflects both volume and source mix — a branch covered by 8 interviews all from one interviewee type may rate ~ even if volume is high.

**Color shading (docx output):** Coverage cells are color-shaded in the final docx — ✓ light green, ~ light yellow, — light gray. Apply via `sub-skills/interview-coding-synthesis/scripts/style_docx.py` after pandoc conversion (pandoc does not carry shading).

---

##### 3. Summary of findings

Apply Format conventions. Citations use `[IS-NN: Name]` format.

```
## Summary of findings

- **[Strategic verdict — what the corpus tells us, not what it covered]** — [Supporting evidence packed densely: numbers, named entities, representative quote.] [IS-1: Smith], [IS-4: Patel], [IS-9: Kim], [IS-15: Johnson]
- **[Second strategic verdict]** — [Evidence with multiple supporting facts combined.] [IS-2: Lee], [IS-7: Brown]
- ...

### Outside the Issue Tree

- **[Strategic verdict on a theme not mapped to any branch]** — [Supporting evidence; how many interviewees raised it.] [IS-3: Davis], [IS-12: Garcia]
```

---

##### 4. Branch findings

One section per branch. Apply Format conventions. Combine direct findings and patterns — do not split into labeled Type 1 / Type 2 subsections. After the findings bullets, render **Contradictions** and **Gaps** as named subsections (only when present).

```
## [Branch ID] — [Branch name] · [N interviews] / [Total] [Overall ✓ / ~ / —]

- **[Strategic verdict — what the corpus says about this branch]** — [Multiple supporting facts combined: named customers, volumes, quotes, internal/external split.] [IS-2: Kim], [IS-3: Nguyen], [IS-9: Patel]
- **[Second strategic verdict for this branch]** — [Evidence, named entities, near-verbatim quote.] [IS-1: Smith], [IS-4: Torres]

**Contradictions** [only when sources disagree]
- **[Frame the disagreement — what's the underlying tension]** — [IS-1: Smith] says "[quote]"; [IS-2: Johnson] says "[quote]". Note: [How to think about it; do not resolve.]

**Gaps**
- [What this branch still needs that the corpus didn't address — phrase as gaps to fill, not branch absences]
```

---

##### 5. Interviewee index

Full lookup table. Codes are assigned in order of first appearance in the corpus.

```
| Code | Name | Company | Company type | Type | Title | Geography | Seniority | Date | ID | Blind? |
|------|------|---------|-------------|------|-------|-----------|-----------|------|----|--------|
| IS-1 | [Name] | [Company] | [e.g., Tier 1 distributor] | Internal staff | [e.g., VP of Sales] | [e.g., NA] | [e.g., VP] | [Date] | [ID] | Y/N |
| C-1  | [Name] | [Company] | [e.g., Regional OEM] | Customer | [Title] | [Geography] | [Seniority] | [Date] | [ID] | Y/N |
| E-1  | [Name] | [Company] | [e.g., Trade association] | Expert / SME | [Title] | [Geography] | [Seniority] | [Date] | [ID] | Y/N |
| CI-1 | [Name] | [Company] | [e.g., Direct competitor] | Competitive intel | [Title] | [Geography] | [Seniority] | [Date] | [ID] | Y/N |
```

**Type codes:** IS = internal staff · C = customer · E = expert/SME · CI = competitive intelligence · O = other

**Seniority codes:** C-suite · VP · Director · Manager · IC (individual contributor) · Unknown

These fields power cross-tabulation claims in Mode 2. Leave blank (not "N/A") if genuinely not determinable.

---

##### 6. Decisions made

Audit trail of every non-trivial inference the skill made during the run. Subsections: Scope, Files, Filename ↔ person matching, Term fixes, Input quality, Frame interpretation. Full template at `references/decisions-template.md`.

---

## Emergent code promotion

When the consultant promotes an OIT theme to a tracked branch — either in response to a promotion candidate flag or at any point — handle as follows.

**Trigger:** consultant says "promote [theme] as [code]" or equivalent.

**For the current Roll-up (if promotion happens during a Roll-up session):**
- Add the promoted code to the locked scope display going forward, marked: `[X] — [Theme label] *(promoted from OIT, Round N)*`
- Add a branch section for the promoted code immediately after Outside the Issue Tree, with a note: "Promoted from Outside the Issue Tree in Round N. [N] prior cards contain relevant evidence under OIT — those findings are the evidence base for this section. Cards were not formally coded against this branch."
- List the relevant prior cards and their OIT bullets so the consultant can assess coverage without a full re-run.

**For subsequent Mode 1 runs:**
- Include the promoted code in the branch list in the Step 1 scope display and code new transcripts against it explicitly.
- Scope display entry: `[X] — [Theme label] *(promoted from OIT, Round N)*`

**For the project glossary (`Primary Research/glossary.md`):**
- Add an entry: `[Code X]: [Theme label] — promoted from OIT, [date], Round [N]`

**What it does not do:** re-run prior transcripts or revise prior Mode 1 cards. The evidence base for the promoted branch is the OIT bullets already captured. If the consultant wants richer coverage from prior transcripts, they can re-run Mode 1 on selected cards with the new code added to scope — the skill will handle it as a targeted incremental run.

---

## Required outputs checklist

Before closing any ICS session, verify all expected outputs exist. If any item is missing, produce it before reporting completion. If the session ends before all outputs are complete, note missing items in `Primary Research/logs/synthesis-log.md` and surface them at the start of the next session.

**Mode 1 (after all transcripts processed):**
- `Primary Research/outputs/[Project Name] Summary Cards v1.docx` — single Word doc, all cards appended in order; increment version on re-runs
- `Primary Research/outputs/batch-*-cards.md` — intermediate markdown per batch, kept for Mode 2 pipeline
- `Primary Research/outputs/Interview Matrix v1.xlsx` — branch coverage rows, question rows, Emerging Topics; Dashboard, By Type, By Geography tabs
- `Primary Research/outputs/[Project Name] Corpus Claims v1.xlsx` — one row per finding bullet; columns: code, name, type, geography, seniority, branch, claim, quote, attribution, topic_tags

**Mode 2:**
- `Primary Research/outputs/mode2-route-YYYY-MM-DD.md`
- `Primary Research/outputs/mode2-extract-YYYY-MM-DD.md`
- `Primary Research/outputs/mode2-branches-YYYY-MM-DD.md`
- `Primary Research/outputs/[Project Name] Interview Roll-up v[N].docx`

**Both modes:**
- `Primary Research/logs/synthesis-log.md` updated
- `Primary Research/glossary.md` updated with any new confirmed terms

---

## Step 5: Logging

At the end of every run, append to `Primary Research/logs/synthesis-log.md`:

```
---
Date: [YYYY-MM-DD]
Project: [Project name]
Mode: [Single / Roll-up]
Transcripts processed: [N]
Analytical frame: [Issue tree / SOW / Kickoff deck / Research questions]
Branches in scope: [N]
Locked scope statement: [verbatim]
Emergent themes surfaced: [N]
Input quality: [Verbatim / Notes / Mixed]
Interviewee types: [List]
Term fixes auto-applied: [N]
Term fixes flagged for review: [N]
Glossary entries added this run: [N]
Notes: [Anything notable — user corrections, unusual inputs, output quality issues]
```

---

## Claim types

Every finding is labeled with one of these types. Never mix types in the same voice.

| Type | Label | What it is | Attribution required |
|------|-------|-----------|----------------------|
| 1 | Direct finding | One source made a specific statement | Verbatim/near-verbatim quote + named source + ID |
| 2 | Pattern claim | Multiple sources said similar things | Count + source list + representative quote |
| 3 | Count claim | Quantitative statement about the corpus | Count + underlying source list |
| 4 | Synthesis observation | Skill's interpretation across sources | Labeled as interpretation; Type 1/2 evidence cited beneath it |
| 5 | Absence claim | Something was not raised by the corpus | Labeled as absence; note retrieval limitations |

**Type 4 rule:** synthesis observations must be labeled as interpretations, never stated as findings. Every Type 4 claim must be supportable by reading the Type 1/2 evidence directly beneath it. If it isn't, remove it.

**Type 5 rule:** absence in retrieved or reviewed passages is not evidence of absence. Note the limitation.
