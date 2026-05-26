# PRT Plugin-Shared Scripts

Plugin-level utilities used by multiple sub-skills (currently Interview Coding & Synthesis; Coverage & Gap Analysis when built will reuse the same primitives).

## Scripts

### `preprocess.py`

**Purpose:** ICS Step 2a (Load and split) + Step 2b (Per-transcript pre-processing).

**Inputs:**
- `--input <file|folder>` (repeatable) — accepts .txt, .md, .docx; folders recursed.
- `--output <folder>` — destination for `.preprocessed.md` files + `INDEX.md`.
- `--metadata <metadata.json>` (optional) — JSON list of interviewee records: `[{name, role, date, location, type, id, blind}, ...]`. Used for filename ↔ person matching.
- `--intro-keywords <comma-separated>` — keywords identifying the interviewer team's intro spiel. Defaults to Newry-team keywords (Newry, Cleveland, Corning, DuPont, Norplex, …); override per project.

**Outputs:**
- `<output>/<basename>.preprocessed.md` — one per transcript, with header (input quality, attribution, EU counts, substantive window, interviewers), speaker resolution notes, term reconciliation placeholder, and exchange units.
- `<output>/INDEX.md` — per-corpus summary table + methodology block.

**Side effects:** none. Originals never modified.

**Idempotency:** running twice with the same inputs produces identical outputs (deterministic; no timestamps in output bodies).

**Heuristics:**
- Substantive question = >12 words + interrogative pattern.
- Non-substantive flags: intro spiel, pre-intro warmup, pleasantries, closing/wrap-up, logistical interruptions (<25 words).
- Speaker resolution: alternation when all unknown; length heuristic (<25 words → interviewer) when partial unknown alongside named interviewee; mapping of generic "Speaker N" → "Interviewer (inferred)" when named interviewers present.

### `term_reconcile.py`

**Purpose:** ICS Step 3 (Term reconciliation). Applies project glossary fixes to pre-processed transcripts.

**Inputs:**
- `--input <folder>` — folder of `.preprocessed.md` files.
- `--glossary <path>` — project `glossary.md` (typically `<project_root>/glossary.md`).
- `--no-inplace` — write to `.reconciled.md` instead of modifying in place.
- `--dry-run` — compute fix counts without writing files.

**Outputs:**
- Updated `.preprocessed.md` (or `.reconciled.md`) with corrections applied and "Term reconciliation" section populated with per-file fix counts.
- Updated `glossary.md` with refreshed "Project-wide totals (this run)" block.

**Glossary format:** Markdown sections — Confirmed corrections, Best-inference corrections, Contextual corrections (with anchor keywords), File-specific corrections. Entries: `- **<canonical>** ← \`variant1\`, \`variant2\``.

**File-specific scope** (two forms, can combine):
- H2 parenthetical: `## File-specific corrections (Olli Piiroinen — phonetic mishearings)`. The leading identifier before the em-dash is the scope; entries below inherit it. Use this when the whole section covers one file.
- H3 sub-scope: `### <scope name>` underneath the H2; entries underneath the H3 use that scope and override any H2 default. Use this when one section covers multiple files.
- Filename match is token-based: every whitespace-separated token ≥3 chars in the scope must appear in the normalized filename (separators collapsed, case-insensitive).

**Side effects:** modifies pre-processed files in place by default; updates the glossary's totals block. Originals (un-pre-processed transcripts) never touched.

**Idempotency:** safe to re-run. Two mechanisms guarantee this:
1. Word-boundary regex with `re.IGNORECASE` — the canonical form doesn't match its own variants.
2. The "## Term reconciliation" and "## Decisions made" H2 sections are masked from substitution, so prior fix logs (`Poland→Polynt ×7`) are never re-rewritten.

## When to use

These scripts are invoked by the ICS sub-skill workflow. Standalone CLI invocation is supported for ad-hoc runs and reusability across sub-skills.

## Contracts (for future doc-vs-code consistency checks)

- `preprocess.py` reads `.txt/.md/.docx`; writes `.preprocessed.md` + `INDEX.md`. Schema of the .preprocessed.md is defined by `render_preprocessed_md` in the script.
- `term_reconcile.py` reads `.preprocessed.md` + `glossary.md`; writes corrected `.preprocessed.md` + updated `glossary.md`. Glossary parser (`parse_glossary`) is the source of truth for the glossary's markdown format.
