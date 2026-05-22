#!/usr/bin/env python3
"""
style_docx.py — Apply color shading to coverage-table cells in ICS Mode 2 docx.

Pandoc does not carry cell shading from markdown to docx. This script
post-processes a Roll-up docx to apply:
- ✓ → light green
- ~ → light yellow
- — → light gray

Detection: any table cell whose text equals (or starts with) one of those
markers, or any cell in a table whose first row contains "✓" / "~" / "—"
header markers.

Usage:
    python style_docx.py --input <Rollup.docx> [--output <styled.docx>]

If --output is omitted, writes to <input stem>.styled.docx.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SHADING_HEX = {
    "check": "C6EFCE",   # light green
    "tilde": "FFEB9C",   # light yellow
    "dash":  "E7E6E6",   # light gray
}


def _set_cell_shading(cell, hex_color: str) -> None:
    """Apply background shading to a python-docx cell via XML manipulation."""
    from docx.oxml.ns import qn  # type: ignore
    from docx.oxml import OxmlElement  # type: ignore

    tc_pr = cell._tc.get_or_add_tcPr()
    # Remove any existing shd
    for existing in tc_pr.findall(qn("w:shd")):
        tc_pr.remove(existing)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def _classify(text: str) -> str | None:
    t = text.strip()
    if not t:
        return None
    if t.startswith("✓"):
        return "check"
    if t.startswith("~"):
        return "tilde"
    if t.startswith("—") or t.startswith("-") and len(t) <= 2:
        return "dash"
    # Bare counts can also be shaded if column headers are markers; handled below
    return None


def style_docx(in_path: Path, out_path: Path) -> int:
    try:
        from docx import Document  # type: ignore
    except ImportError:
        print("ERROR: python-docx not installed. "
              "pip install python-docx --break-system-packages", file=sys.stderr)
        return 2

    doc = Document(str(in_path))
    cells_shaded = 0

    for tbl in doc.tables:
        if not tbl.rows:
            continue

        # Determine column markers from header row (look at first row)
        header_cells = tbl.rows[0].cells
        column_markers: dict[int, str] = {}
        for i, h in enumerate(header_cells):
            cls = _classify(h.text)
            if cls:
                column_markers[i] = cls

        # Iterate body rows
        for row in tbl.rows[1:]:
            for i, cell in enumerate(row.cells):
                # Per-cell marker
                cls = _classify(cell.text)
                if cls:
                    _set_cell_shading(cell, SHADING_HEX[cls])
                    cells_shaded += 1
                    continue
                # Column-header marker (count cells)
                if i in column_markers and cell.text.strip():
                    _set_cell_shading(cell, SHADING_HEX[column_markers[i]])
                    cells_shaded += 1

    doc.save(str(out_path))
    print(f"Shaded {cells_shaded} cells. Wrote: {out_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--input", required=True, help="Input docx path")
    parser.add_argument("--output", default=None,
                        help="Output docx path (default: <stem>.styled.docx)")
    args = parser.parse_args(argv)

    in_path = Path(args.input)
    if not in_path.is_file():
        print(f"ERROR: input file not found: {in_path}", file=sys.stderr)
        return 2

    out_path = (
        Path(args.output) if args.output
        else in_path.with_suffix(".styled.docx")
    )
    return style_docx(in_path, out_path)


if __name__ == "__main__":
    sys.exit(main())
