# ICS Sub-Skill Scripts

Sub-skill-specific utilities for Interview Coding & Synthesis. For plugin-shared scripts (transcript pre-processing, term reconciliation), see `../../../scripts/`.

## Scripts

### `style_docx.py`

**Purpose:** Apply color shading to coverage-table cells in a Mode 2 Roll-up docx. Pandoc does not carry cell shading from markdown to docx; this is a post-processing step.

**Inputs:**
- `--input <docx>` — input Roll-up docx (typically pandoc-converted from markdown).
- `--output <docx>` — output path. Default: `<input stem>.styled.docx`.

**Outputs:**
- Coverage cells shaded:
  - `✓` → light green (`#C6EFCE`)
  - `~` → light yellow (`#FFEB9C`)
  - `—` → light gray (`#E7E6E6`)

**Detection:**
- Per-cell: any cell whose text starts with `✓`, `~`, or `—`.
- Column-wide: cells in a column whose header row contains a marker get shaded by their count value (used for Mode 2 coverage tables with `✓ Sub.` / `~ Partial` / `— None` column headers).

**Side effects:** writes a new docx. Input file untouched.

**Idempotency:** running on an already-styled file re-applies shading (replaces existing `<w:shd>` elements). Output is deterministic for the same input.

## Contracts

- `style_docx.py` reads `.docx` (any structure); writes `.docx` with `<w:shd>` elements added to matching cells. Shading hex values are constants; change `SHADING_HEX` to recolor.
