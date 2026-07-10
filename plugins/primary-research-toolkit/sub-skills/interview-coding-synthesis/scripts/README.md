# ICS Sub-Skill Scripts

Sub-skill-specific utilities for Interview Coding & Synthesis. For plugin-shared scripts (transcript pre-processing, term reconciliation), see `../../../scripts/`.

## Docx build pipeline

Cards and Roll-up docx files are always produced by running these two scripts in order against the canonical Markdown — never by editing an existing docx or reading one back to append:

```
python render_docx.py --input <canonical.md> --output <Output>.docx
python style_docx.py --input <Output>.docx --output <Output>.docx
```

Dependency: `pip install python-docx --break-system-packages` (shared by both scripts; no pandoc dependency).

## Scripts

### `render_docx.py`

**Purpose:** Deterministically render the ICS Markdown dialect (headers, GFM pipe tables, 2-space-nested bullets, `**bold**`) into a Word doc with consistent named styles every time. Replaces a prior pandoc-based conversion step whose availability was never confirmed and which produced style drift + literal `>` leakage on at least one update run.

**Inputs:**
- `--input <md>` — canonical Markdown (cards or Roll-up).
- `--output <docx>` — output path. Always fully rewritten; never edited in place.

**Contract:** input is the constrained Markdown dialect ICS actually produces — not general-purpose Markdown. A stray `>`-prefixed line (a template regression) has its marker stripped rather than rendered literally.

### `style_docx.py`

**Purpose:** Apply color shading to coverage-table cells in a Mode 2 Roll-up docx. Run after `render_docx.py` (python-docx tables don't carry cell shading from the source Markdown).

**Inputs:**
- `--input <docx>` — input Roll-up/cards docx (produced by `render_docx.py`).
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
