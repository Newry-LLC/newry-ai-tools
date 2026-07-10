# Mode 2 (Roll-up) Output Spec

*Referenced from `../SKILL.md` Step 4 → Mode 2 → Output. Section-by-section templates for the Roll-up document. Read this file when producing or updating a Roll-up.*

**Contents:** [1. Corpus header](#1-corpus-header) · [1a. Locked scope display](#1a-locked-scope-display) · [2. Coverage table](#2-coverage-table) · [3. Summary of findings](#3-summary-of-findings) · [4. Branch findings](#4-branch-findings) · [5. Interviewee index](#5-interviewee-index) · [6. Decisions made](#6-decisions-made)

---

## 1. Corpus header

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

## 1a. Locked scope display

Render the full nested-bullet scope display from Step 1, verbatim. This anchors every downstream section to the exact frame the synthesis was run against. **This is the only place scope is displayed** — it never repeats per-card (see SKILL.md Mode 1 note) or per-section here.

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

## 2. Coverage table

One row per branch. **Include a "What it covers" column** — concrete sub-topics drawn from the corpus, not abstract branch labels. This single column tells the reader what's actually inside the branch at a glance.

```
| Branch | What it covers | ✓ Sub. | ~ Partial | — Not addressed | Overall |
|--------|----------------|--------|-----------|-----------------|---------|
| **A — [Branch name]** | [Concrete sub-topics surfaced in the corpus, e.g., specific applications, product categories, customer segments] | N | N | N | ✓ / ~ / — |
| **B1 — [Sub-branch name]** | [Sub-topics surfaced in the corpus] | N | N | N | ✓ / ~ / — |
...
```

If Research Plan Design provided priorities, replace "What it covers" with "Priority" + "What it covers" as separate columns.

**Overall rating — score evidence strength, never interview volume.** The Overall cell is a proposed read of how well the branch's question is *answered*, rated on three quality sub-signals, each drawn from data the cards already carry. Volume never drives it — a branch with 8 same-type interviews is not "well covered" for that reason.

- *Directness* — the cards' `Input quality` / `Attribution` (verbatim > synthesized > rough).
- *Source diversity* — spread across the cards' `Type` / `Geography` / `Seniority` (many one-type sources ≠ diverse).
- *Specificity* — claims are concrete (named entities, numbers) vs. vague.

Rating (a function of the three, so the same corpus gives the same label — write the marker prefix so shading applies):
- **✓ Strong** — ≥2 sub-signals high, none critically weak, across ≥2 relevant segments (where the question implies multiple segments matter).
- **~ Emerging** — exactly one sub-signal high, or all moderate: a supported direction with a named shortfall. State which sub-signal is short.
- **— Thin** — no sub-signal reaches high, or few/one-sided/low-directness sources. Fires only on this branch's own evidence, never relative to other branches.
- **n/a — insufficient basis** — no codable claims on the branch at all (all sub-topics —). No rating forced; leave the Overall cell `n/a — insufficient basis` (unshaded).

**Consensus is a finding, not a quality signal.** Agreement/disagreement is reported, never used to lower the rating. Direct, diverse, specific sources that genuinely disagree = *strong evidence of a real split* → rate **✓ Strong** and state the divergence ("sources split — a real divide"). Only count disagreement against strength when it comes from thin/low-directness sources.

**Missing metadata (older cards).** If a sub-signal's card field is absent/blank (common on cards coded by an earlier version), drop that sub-signal, lower the stated confidence, and say so ("diversity not assessable — Geography not on these cards"). Never default or invent it. This differs from insufficient basis (missing *claims*, not missing *metadata*).

**Saturation** (optional note, not a rating): mark a branch *saturated* only when a **diverse** converging source set has stopped surfacing new dimensions — never on "the answer stopped changing" alone (a one-sided sample confirming itself). Flag when sources may share one origin (metadata diversity ≠ true independence).

**Scoring-method marker.** Stamp `coverage-method: v2 (evidence-strength)` at the top of the Roll-up. Any consumer reading a prior Roll-up's ratings (the coordinator's startup greeting; the cross-round delta in Pass 4) must treat an older-or-unmarked Roll-up as **not comparable** — surface "re-run to refresh," and in the delta suppress per-branch movement with a "not comparable to prior method" note. Per-sub-topic ✓/~/— counts stay comparable across versions.

Keep the raw counts (✓ Sub. / ~ Partial / — Not addressed) as-is — they remain a factual, version-stable record; only the Overall rating changed basis.

**Docx generation — one pinned pipeline, always a full rebuild.** The canonical Markdown (the `batch-*-cards.md` / `mode2-*.md` files already produced during the pipeline) is the source of truth. The Word doc is **never** edited in place and **never** read back to append to — every run, cards and Roll-up docx are fully regenerated from the current canonical Markdown via two scripts, run in order:

```
python sub-skills/interview-coding-synthesis/scripts/render_docx.py --input <canonical.md> --output "<Output>.docx"
python sub-skills/interview-coding-synthesis/scripts/style_docx.py --input "<Output>.docx" --output "<Output>.docx"
```

This is the entire build — no pandoc dependency (pandoc's presence on a consultant machine isn't guaranteed and wasn't previously specified as an install step; `render_docx.py` uses only `python-docx`, already a dependency of `style_docx.py`). `render_docx.py` renders the constrained Markdown dialect ICS produces (headers, GFM tables, 2-space-nested bullets, `**bold**`) into consistent named styles every time — this is what fixes both the style drift and the literal `>` characters that a prior update run produced. `style_docx.py` then applies coverage-cell shading (✓ light green, ~ light yellow, — light gray, unchanged). **Dependencies:** `pip install python-docx --break-system-packages` (one-time; same install as already required for shading).

---

## 3. Summary of findings

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

## 4. Branch findings

One section per branch. Apply Format conventions. Combine direct findings and patterns — do not split into labeled Type 1 / Type 2 subsections. After the findings bullets, render **Contradictions** and **Gaps** as named subsections (only when present).

```
## [Branch ID] — [Branch name] · [N interviews cited] [Overall: ✓ Strong / ~ Emerging / — Thin / n/a Insufficient basis]

- **[Strategic verdict — what the corpus says about this branch]** — [Multiple supporting facts combined: named customers, volumes, quotes, internal/external split.] [IS-2: Kim], [IS-3: Nguyen], [IS-9: Patel]
- **[Second strategic verdict for this branch]** — [Evidence, named entities, near-verbatim quote.] [IS-1: Smith], [IS-4: Torres]

**Contradictions** [only when sources disagree]
- **[Frame the disagreement — what's the underlying tension]** — [IS-1: Smith] says "[quote]"; [IS-2: Johnson] says "[quote]". Note: [How to think about it; do not resolve.]

**Gaps**
- [What this branch still needs that the corpus didn't address — phrase as gaps to fill, not branch absences]
```

---

## 5. Interviewee index

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

## 6. Decisions made

Audit trail of every non-trivial inference the skill made during the run. Subsections: Scope, Files, Filename ↔ person matching, Term fixes, Input quality, Frame interpretation. Full template at `../references/decisions-template.md`.
