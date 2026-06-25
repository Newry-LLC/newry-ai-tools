"""
deck_writer.py — deterministic PowerPoint write helpers for the Newry deck builder.

Why this exists: ppt-mcp's text/table write tools destroy existing run and cell
formatting, because assigning TextRange.Text is destructive in PowerPoint's object
model. These helpers write the CLEAN way — clear, insert text, then re-stamp the
formatting from known values — which preserves mixed formatting, is idempotent, and
persists to disk. (Validated 2026-06-19. See decision-log.md.)

They do TARGETED writes only: each op touches exactly the shape you name and leaves
the rest of the slide alone, so manual edits elsewhere are never wiped.

USAGE
  python deck_writer.py '<json job>'          # job as inline JSON string
  python deck_writer.py --file job.json       # job from a file
  echo '<json>' | python deck_writer.py -      # job from stdin

JOB SHAPE
{
  "presentation": "active",          # "active", a filename substring, or full path
  "ops": [ <op>, <op>, ... ]
}

OPS
  Write a mixed-format text box / placeholder (explicit formatting per paragraph):
    {"op": "write_textbox", "slide": 3, "shape": 2,
     "paragraphs": [
        {"text": "Bold navy header", "bold": true,  "size": 20, "color": "#1E4C7F"},
        {"text": "Regular body line", "bold": false, "size": 14, "color": "#000000"}
     ]}
    Per-paragraph keys (all optional except text): bold, italic, size, color (#RRGGBB),
    font (name), align ("left"|"center"|"right"|"justify").

  Change text but KEEP the shape's existing formatting (edit mode):
    {"op": "edit_text_preserve", "slide": 3, "shape": 2,
     "paragraphs": ["New line 1", "New line 2"]}   # plain strings
    Re-applies each existing paragraph's format to the new paragraph by position.
    If there are more new paragraphs than old, the last old paragraph's format is reused.

  Write a table cell-by-cell (preserves per-cell alignment/weight; sidesteps the
  set_table_data collapse):
    {"op": "write_table", "slide": 5, "shape": 1,
     "rows": [
        [ {"text":"Criterion","bold":true,"align":"left"}, {"text":"Virgin","bold":true} ],
        [ {"text":"Cost / gal","align":"left"}, {"text":"$3.20"} ]
     ]}
    Cell keys: same as paragraph keys, plus "fill" (#RRGGBB cell background).
    A cell may also be a plain string for "just set the text, keep cell format".

  Shapes are addressed by 1-based index ("shape": 2) OR by name ("shape": "Title 1").

OUTPUT: JSON to stdout — {"ok": bool, "results": [...], "presentation": "..."}.
Each op result includes a read-back ("after") of what is now in the shape, so the
caller can verify the write landed.
"""

import sys
import os
import json
import tempfile
import subprocess
import shutil

try:
    import win32com.client
except ImportError:
    print(json.dumps({"ok": False, "error": "pywin32 not installed"}))
    sys.exit(1)

SPECS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template-specs.json")

# think-cell CLI for filling named chart elements from JSON (.ppttc). Override with the
# THINKCELL_PPTTC env var if installed elsewhere. Used by the build_chart op.
THINKCELL_PPTTC = os.environ.get(
    "THINKCELL_PPTTC", r"C:\Program Files (x86)\think-cell\ppttc.exe")

# --- PowerPoint constants ---
PP_ALIGN = {"left": 1, "center": 2, "right": 3, "justify": 4}
PP_ALIGN_NAME = {1: "left", 2: "center", 3: "right", 4: "justify"}

# Capacity-estimate heuristics (rough, for overflow warnings on arbitrary decks).
# Proportional fonts average ~0.5 em per glyph; default line spacing ~1.2x.
CHAR_W_FACTOR = 0.5
LINE_SPACING = 1.2


def to_bgr(hex_color):
    """'#RRGGBB' -> PowerPoint BGR integer."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return b * 65536 + g * 256 + r


def from_bgr(val):
    """PowerPoint BGR integer -> '#RRGGBB'."""
    val = int(val)
    b, g, r = (val >> 16) & 255, (val >> 8) & 255, val & 255
    return "#%02X%02X%02X" % (r, g, b)


def apply_format(rng, spec):
    """Apply a paragraph/cell format spec to a TextRange."""
    if "bold" in spec:
        rng.Font.Bold = bool(spec["bold"])
    if "italic" in spec:
        rng.Font.Italic = bool(spec["italic"])
    if "size" in spec:
        rng.Font.Size = float(spec["size"])
    if "color" in spec:
        rng.Font.Color.RGB = to_bgr(spec["color"])
    if "font" in spec:
        rng.Font.Name = spec["font"]
    if "align" in spec and spec["align"] in PP_ALIGN:
        rng.ParagraphFormat.Alignment = PP_ALIGN[spec["align"]]
    if "bullet" in spec:
        # Clearing+reinserting text drops the placeholder's native bullets, so set explicitly.
        rng.ParagraphFormat.Bullet.Visible = bool(spec["bullet"])
        if spec["bullet"]:
            rng.ParagraphFormat.Bullet.Type = 1  # ppBulletUnnumbered (character bullet)


def read_format(rng):
    """Read back a TextRange's first-run format for verification."""
    try:
        return {
            "text": rng.Text.strip(),
            "bold": bool(rng.Font.Bold),
            "size": round(rng.Font.Size),
            "color": from_bgr(rng.Font.Color.RGB),
        }
    except Exception as e:
        return {"text": rng.Text.strip(), "note": "format read failed: %s" % e}


def get_shape(slide, ref):
    """Resolve a shape by 1-based index (int) or by name (str)."""
    if isinstance(ref, int):
        return slide.Shapes(ref)
    for sh in slide.Shapes:
        if sh.Name == ref:
            return sh
    raise ValueError("no shape named %r on this slide" % ref)


def clean_write_textbox(tf, paragraphs):
    """Clear the frame and write each paragraph, re-stamping its format.

    Each new run inherits the preceding run's formatting (PowerPoint's InsertAfter
    behaviour), so a bold/navy first line would bleed emphasis into later lines. We
    reset every paragraph to a neutral baseline (regular weight, upright, black) before
    applying its spec — so a paragraph only carries the emphasis it explicitly asks for.
    All callers pass explicit bold/color, so this is invisible to them; it just makes
    sparse specs (e.g. a bold NAME over plain bullet lines) render predictably.
    """
    tf.Text = ""
    for i, p in enumerate(paragraphs):
        if i > 0:
            tf.InsertAfter("\r")
        text = p["text"] if isinstance(p, dict) else str(p)
        if not text:
            continue  # empty paragraph: the surrounding breaks preserve the blank line (InsertAfter('') errors)
        start = len(tf.Text)
        tf.InsertAfter(text)
        rng = tf.Characters(start + 1, len(text))
        rng.Font.Bold = False
        rng.Font.Italic = False
        rng.Font.Color.RGB = to_bgr("#000000")
        if isinstance(p, dict):
            apply_format(rng, p)


def _safe_get(obj, attr, default=None):
    """Read a COM property that may throw (e.g. -2147467259 'mixed' sentinel)."""
    try:
        return obj.__getattr__(attr) if hasattr(obj, "__getattr__") else getattr(obj, attr)
    except Exception:
        return default


def edit_preserve(tf, new_lines):
    """Replace text but keep the existing per-paragraph formatting (by position).

    Captures each existing paragraph's full format (font, size, weight, color, align,
    bullet character/indent geometry, and spacing) before clearing, then re-stamps it
    onto the new lines by position. Extra new lines reuse the last existing paragraph's
    format. This is how simple slots stay faithful to the template without hardcoding
    any format in the spec.

    Bullet geometry captured:
      - bullet_visible, bullet_type, bullet_char, bullet_rel_size, bullet_color
      - left_indent, first_line_indent  (gap between them = space after bullet char)
      - space_before, space_after       (paragraph spacing)
    """
    old_count = tf.Paragraphs().Count
    fmts = []
    for i in range(1, old_count + 1):
        pr = tf.Paragraphs(i)
        pf = pr.ParagraphFormat
        bullet = pf.Bullet
        b_color = None
        try:
            b_color = from_bgr(int(bullet.Font.Color.RGB))
        except Exception:
            pass
        # Read run-level attributes (bold/italic/size/color/font) from the paragraph's
        # FIRST CHARACTER, not pr.Font.*. When a paragraph mixes runs (e.g. an inline bold
        # phrase mid-line), pr.Font.Bold returns PowerPoint's "mixed" sentinel (-2), which
        # bool()'s to True and would wrongly bold the whole re-stamped line. The first
        # character is always an unambiguous value. (Inline emphasis can't survive a
        # plain-text edit anyway — the line takes its leading run's format.)
        fr = pr.Characters(1, 1).Font if len(pr.Text.strip()) else pr.Font
        f = {
            "bold":              bool(fr.Bold),
            "italic":            bool(fr.Italic),
            "size":              float(fr.Size),
            "color":             from_bgr(fr.Color.RGB),
            "align":             int(pf.Alignment),
            "font":              fr.Name,
            # bullet character & style
            "bullet_visible":    bool(bullet.Visible),
            "bullet_type":       int(bullet.Type),
            "bullet_char":       _safe_get(bullet, "Character"),
            "bullet_rel_size":   _safe_get(bullet, "RelativeSize"),
            "bullet_color":      b_color,
            # indent geometry — left_indent is text start; first_line_indent is negative
            # (hanging), so bullet sits at (left_indent + first_line_indent).
            # The gap between them is the space between bullet char and first word.
            "left_indent":       _safe_get(pf, "LeftIndent"),
            "first_line_indent": _safe_get(pf, "FirstLineIndent"),
            # paragraph spacing
            "space_before":      _safe_get(pf, "SpaceBefore"),
            "space_after":       _safe_get(pf, "SpaceAfter"),
        }
        fmts.append(f)
    tf.Text = ""
    for i, line in enumerate(new_lines):
        if i > 0:
            tf.InsertAfter("\r")
        s = str(line)
        if not s:
            continue  # empty paragraph: surrounding breaks preserve blank line (InsertAfter('') errors)
        start = len(tf.Text)
        tf.InsertAfter(s)
        rng = tf.Characters(start + 1, len(s))
        f = fmts[i] if i < len(fmts) else (fmts[-1] if fmts else None)
        if f:
            rng.Font.Bold = f["bold"]
            rng.Font.Italic = f["italic"]
            rng.Font.Size = f["size"]
            rng.Font.Color.RGB = to_bgr(f["color"])
            rng.Font.Name = f["font"]
            pf = rng.ParagraphFormat
            pf.Alignment = f["align"]
            # indent geometry (restores bullet-to-text spacing)
            if f["left_indent"] is not None:
                try:
                    pf.LeftIndent = f["left_indent"]
                except Exception:
                    pass
            if f["first_line_indent"] is not None:
                try:
                    pf.FirstLineIndent = f["first_line_indent"]
                except Exception:
                    pass
            # paragraph spacing
            if f["space_before"] is not None:
                try:
                    pf.SpaceBefore = f["space_before"]
                except Exception:
                    pass
            if f["space_after"] is not None:
                try:
                    pf.SpaceAfter = f["space_after"]
                except Exception:
                    pass
            # bullet
            pf.Bullet.Visible = f["bullet_visible"]
            if f["bullet_visible"]:
                pf.Bullet.Type = f["bullet_type"] or 1
                if f["bullet_char"] is not None:
                    try:
                        pf.Bullet.Character = f["bullet_char"]
                    except Exception:
                        pass
                if f["bullet_rel_size"] is not None:
                    try:
                        pf.Bullet.RelativeSize = f["bullet_rel_size"]
                    except Exception:
                        pass
                if f["bullet_color"] is not None:
                    try:
                        pf.Bullet.Font.Color.RGB = to_bgr(f["bullet_color"])
                    except Exception:
                        pass


def write_table(shape, rows, opts=None, slide=None):
    """Write a table cell-by-cell, preserving per-cell format unless overridden.

    PowerPoint applies a built-in TableStyle (header emphasis + row banding) that
    overrides per-cell colors and fights the Newry look. We switch that style off so
    our explicit per-cell fills and font colors win, then default every cell to the
    Newry baseline (white fill, black text) unless the spec overrides it.

    Real data rarely matches the template's row/column count, so we add/remove both
    to fit (e.g. a qualitative-comparison table flexes to however many items there are).
    `opts` carries layout defaults: header_fill, header_bold, swatches (named->hex,
    e.g. {"high":"#89B4E3"}), cell_size.

    A cell may be:
      - a plain string                       -> just set the text
      - {text, fill, color, bold, size, align, swatch}  -> single-format cell
      - {"paragraphs": [ {text, bold, size, color, align, bullet}, ... ]}
            -> a MULTI-PARAGRAPH cell (e.g. a bold NAME over bullet lines, or NAME
               over an email). Each paragraph carries its own format; we clean-write
               them so the per-line formatting survives.
      - {"image": path-or-url, "circle": bool}
            -> drop a picture into the cell's bounds (needs `slide`); used for the
               image row of a qualitative-comparison table.
    """
    opts = opts or {}
    table = shape.Table
    # Capture the table's total width up front so equal_cols can restore it after a
    # column add/delete (deleting columns shrinks the table from the right otherwise).
    orig_total_w = None
    if opts.get("equal_cols"):
        try:
            orig_total_w = float(shape.Width)
        except Exception:
            orig_total_w = None
    # keep_style: leave the built-in TableStyle ON (e.g. a banded interview table whose
    # light row stripes come from the style, not cell fills). Otherwise turn the style off
    # so our explicit per-cell fills/colors win (the gradient-table case).
    keep_style = opts.get("keep_style", False)
    if not keep_style:
        for prop in ("FirstRow", "LastRow", "FirstCol", "LastCol", "HorizBanding", "VertBanding"):
            try:
                setattr(table, prop, False)
            except Exception:
                pass
    # Un-merge to a clean grid (opt-in). Some template tables merge cells (e.g. a category
    # label spanning several rows). Merged cells make row-by-row writes collide — two logical
    # rows share one physical cell, so the second write overwrites the first. Flattening the
    # whole table into one cell and splitting it back to its R×C yields a uniform grid where
    # every (row,col) is independent, so the resize+fill below is exact. We capture and restore
    # column widths so flattening doesn't even out the template's proportions. Opt-in
    # ("unmerge": true) so the edit path leaves intentional client-table merges untouched.
    if opts.get("unmerge"):
        R0, C0 = table.Rows.Count, table.Columns.Count
        orig_widths = []
        for c in range(1, C0 + 1):
            try:
                orig_widths.append(float(table.Columns(c).Width))
            except Exception:
                orig_widths.append(None)
        try:
            table.Cell(1, 1).Merge(table.Cell(R0, C0))
            table.Cell(1, 1).Split(R0, C0)
            for c in range(1, C0 + 1):
                if orig_widths[c - 1]:
                    try:
                        table.Columns(c).Width = orig_widths[c - 1]
                    except Exception:
                        pass
        except Exception:
            pass
    # Capture original table height up front so fill_height can restore it after a row
    # add/delete (which otherwise leaves the table shrunk to the top of the slide).
    orig_total_h = None
    if opts.get("fill_height"):
        try:
            orig_total_h = float(shape.Height)
        except Exception:
            orig_total_h = None
    # header_rows: leave the template's top N rows in place (e.g. a column-label header that
    # also keeps a section subhead clear above the data); data rows are written below them.
    header_rows = int(opts.get("header_rows", 0))
    # Resize the table's row count to match header + data (add at end / delete from end).
    need = len(rows) + header_rows
    while table.Rows.Count < need:
        table.Rows.Add()
    while table.Rows.Count > need:
        table.Rows(table.Rows.Count).Delete()
    # Resize columns to match the widest data row (comparison tables vary in # of items).
    need_cols = max((len(row) for row in rows), default=table.Columns.Count)
    while table.Columns.Count < need_cols:
        table.Columns.Add()
    while table.Columns.Count > need_cols:
        table.Columns(table.Columns.Count).Delete()
    # Optional explicit per-column widths (points) — e.g. narrow spacer columns + wide text
    # columns so emails/names don't wrap mid-word. Sum should match the table's total width.
    col_widths = opts.get("col_widths")
    if col_widths:
        for i, w in enumerate(col_widths, start=1):
            if i <= table.Columns.Count:
                try:
                    table.Columns(i).Width = float(w)
                except Exception:
                    pass
    elif opts.get("equal_cols") and orig_total_w and table.Columns.Count:
        # Even columns across the table's original width (comparison tables with N items).
        each = orig_total_w / table.Columns.Count
        for i in range(1, table.Columns.Count + 1):
            try:
                table.Columns(i).Width = each
            except Exception:
                pass
    swatches = opts.get("swatches", {})
    header_fill = opts.get("header_fill")
    cell_size = opts.get("cell_size")
    # preserve_fill: leave the template's existing cell fills alone (e.g. a banded table
    # whose shading uses transparency we can't reproduce by setting a flat color). We then
    # only write text + font color and never touch the fill.
    preserve_fill = opts.get("preserve_fill", False) or keep_style
    for r, row in enumerate(rows, start=1 + header_rows):
        for c, cell_spec in enumerate(row, start=1):
            cell = table.Cell(r, c)
            tf = cell.Shape.TextFrame.TextRange
            spec = cell_spec if isinstance(cell_spec, dict) else {"text": str(cell_spec)}
            # Fill first — applies whatever the cell's content kind is.
            if not preserve_fill:
                # Fill: explicit > swatch > header default > white baseline.
                fill = spec.get("fill")
                if fill is None and spec.get("swatch") in swatches:
                    fill = swatches[spec["swatch"]]
                if fill is None:
                    fill = header_fill if (r == 1 and header_fill) else "#FFFFFF"
                cell.Shape.Fill.Solid()
                cell.Shape.Fill.ForeColor.RGB = to_bgr(fill)
            elif "fill" in spec:
                cell.Shape.Fill.Solid()
                cell.Shape.Fill.ForeColor.RGB = to_bgr(spec["fill"])
            # Content: image > multi-paragraph (NAME+bullets / NAME+email) > single string.
            if spec.get("image") and slide is not None:
                tf.Text = ""
                place_image(slide, cell.Shape, spec["image"], circle=spec.get("circle", False))
            elif "paragraphs" in spec:
                # Each paragraph carries its own format; clean-write so per-line formatting holds.
                clean_write_textbox(tf, spec["paragraphs"])
            else:
                tf.Text = spec.get("text", "")
                tf.Font.Color.RGB = to_bgr(spec.get("color", "#000000"))
                if "bold" not in spec and r == 1 and opts.get("header_bold", True):
                    tf.Font.Bold = True
                if cell_size and "size" not in spec:
                    tf.Font.Size = float(cell_size)
                apply_format(tf, {k: v for k, v in spec.items() if k in ("bold", "size", "italic", "font", "align")})
    # Force a styled first column independent of the template's per-row fills (e.g.
    # growth-levers: navy lever cells + white bold text), for ANY number of data rows.
    # Header rows are left untouched.
    fc_fill = opts.get("first_col_fill")
    if fc_fill:
        for r in range(header_rows + 1, table.Rows.Count + 1):
            try:
                cell = table.Cell(r, 1)
                cell.Shape.Fill.Solid()
                cell.Shape.Fill.ForeColor.RGB = to_bgr(fc_fill)
                tr = cell.Shape.TextFrame.TextRange
                if opts.get("first_col_color"):
                    tr.Font.Color.RGB = to_bgr(opts["first_col_color"])
                if opts.get("first_col_bold") is not None:
                    tr.Font.Bold = bool(opts.get("first_col_bold"))
                if opts.get("first_col_size"):
                    tr.Font.Size = float(opts["first_col_size"])
            except Exception:
                pass
    # fill_height: spread data rows to fill the table's original height (so a table with
    # fewer rows than the template spans the slide instead of shrinking to the top). Header
    # rows keep their own height; the remainder is split evenly across the data rows.
    if opts.get("fill_height") and orig_total_h and table.Rows.Count > header_rows:
        hdr_h = 0.0
        for r in range(1, header_rows + 1):
            try:
                hdr_h += float(table.Rows(r).Height)
            except Exception:
                pass
        data_rows = table.Rows.Count - header_rows
        each = max(1.0, (orig_total_h - hdr_h) / data_rows)
        for r in range(header_rows + 1, table.Rows.Count + 1):
            try:
                table.Rows(r).Height = each
            except Exception:
                pass
    # After an un-merge, the merge→split step leaves rows with wildly uneven inherited
    # heights (one row hogs the height, others collapse to slivers). Reset each row to a
    # minimal height; PowerPoint clamps it back up to fit the cell's content, giving each
    # row a natural content-sized height. Gated on unmerge so normal tables are untouched.
    if opts.get("unmerge"):
        for r in range(1, table.Rows.Count + 1):
            try:
                table.Rows(r).Height = 1
            except Exception:
                pass


def fill_slot(shape, slot, content, slide=None):
    """Fill one slot on a slide according to its declared kind."""
    kind = slot["kind"]
    tf = shape.TextFrame.TextRange if shape.HasTextFrame else None
    if kind == "text":
        # Explicit format if the spec gives one; otherwise preserve the template's own.
        if "format" in slot:
            clean_write_textbox(tf, [dict(slot["format"], text=str(content))])
        else:
            edit_preserve(tf, [str(content)])
    elif kind == "text_lines":
        lines = content if isinstance(content, list) else [content]
        if "format" in slot:
            clean_write_textbox(tf, [dict(slot["format"], text=str(x)) for x in lines])
        else:
            edit_preserve(tf, [str(x) for x in lines])
    elif kind == "header_bullets":
        # content = {"header": str, "bullets": [str, ...]}
        paras = [dict(slot["header_format"], text=str(content["header"]))]
        for b in content.get("bullets", []):
            paras.append(dict(slot["bullet_format"], text=str(b)))
        clean_write_textbox(tf, paras)
    elif kind == "quote":
        # content = {"quote": str, "attribution": str}
        paras = [
            dict(slot["quote_format"], text=str(content["quote"])),
            dict(slot["attr_format"], text=str(content.get("attribution", ""))),
        ]
        clean_write_textbox(tf, paras)
    elif kind == "table":
        write_table(shape, content, slot.get("table_opts"), slide)  # content = rows
    else:
        raise ValueError("unknown slot kind %r" % kind)


def place_image(slide, placeholder_shape, source, circle=False):
    """Put an image (local path or URL) at a placeholder's position, on top of it.

    We don't delete the placeholder (that would shift shape indices mid-build); the
    image fully covers it. When circle=True (headshots), the image is center-cropped to
    a square first (no distortion of landscape sources) and then masked to an oval, which
    matches the Newry circular-headshot style.
    """
    path = source
    tmp = None
    if isinstance(source, str) and source.lower().startswith(("http://", "https://")):
        # Download via PowerShell Invoke-WebRequest. Python urllib/curl hit WinError 10054
        # (TLS handshake rejected) on Airtable's CDN; IWR negotiates it cleanly on Windows.
        fd, tmp = tempfile.mkstemp(suffix=".img")
        os.close(fd)
        ps = "Invoke-WebRequest -Uri '%s' -OutFile '%s' -UseBasicParsing" % (source, tmp)
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True,
                       capture_output=True, timeout=60)
        path = tmp
    L, T, W, H = placeholder_shape.Left, placeholder_shape.Top, placeholder_shape.Width, placeholder_shape.Height
    # Insert at native size first so we can crop without distortion.
    pic = slide.Shapes.AddPicture(path, False, True, L, T, -1, -1)
    try:
        pic.LockAspectRatio = 0  # msoFalse — lets us set W and H independently
    except Exception:
        pass
    if circle:
        w0, h0 = float(pic.Width), float(pic.Height)
        if w0 > h0:
            c = (w0 - h0) / 2.0
            pic.PictureFormat.CropLeft = c
            pic.PictureFormat.CropRight = c
        elif h0 > w0:
            c = (h0 - w0) / 2.0
            pic.PictureFormat.CropTop = c
            pic.PictureFormat.CropBottom = c
    pic.Width = W
    pic.Height = H
    pic.Left = L
    pic.Top = T
    if circle:
        try:
            pic.AutoShapeType = 9  # msoShapeOval — masks the square crop to a circle
        except Exception:
            pass
    try:
        pic.ZOrder(0)  # msoBringToFront
    except Exception:
        pass
    if tmp:
        try:
            os.remove(tmp)
        except Exception:
            pass
    return {"left": round(L, 1), "top": round(T, 1), "width": round(W, 1), "height": round(H, 1)}


def copy_shape_to(slide, target_placeholder, src_index):
    """Duplicate an existing shape (e.g. an already-cropped circular headshot from the
    template's montage) and move it onto a target placeholder's position/size. No
    re-cropping — the source shape's crop and circular mask carry over untouched.
    """
    L = target_placeholder.Left
    T = target_placeholder.Top
    W = target_placeholder.Width
    H = target_placeholder.Height
    dup = slide.Shapes(int(src_index)).Duplicate()
    d = dup.Item(1) if hasattr(dup, "Item") else dup
    try:
        d.LockAspectRatio = 0
    except Exception:
        pass
    d.Left = L
    d.Top = T
    d.Width = W
    d.Height = H
    return {"copied_from": int(src_index), "left": round(L, 1), "top": round(T, 1)}


def _apply_active_phase(slide, phase_chevrons, active_phase):
    """Recolor phase chevrons so the specified phase is highlighted.

    Template ships with phase 1 active (navy fill, white text). To highlight a
    different phase: reads the inactive fill/text from S_stage2 (always inactive
    in the source template), then sets all chevrons to inactive and the target to active.
    """
    shapes = phase_chevrons.get("shapes", [])
    if not shapes or int(active_phase) == 1:
        return  # phase 1 is already active in the template; nothing to change
    active_fill = phase_chevrons.get("active_fill", "#1E4C7F")
    active_text = phase_chevrons.get("active_text_color", "#FFFFFF")
    # Read inactive fill+text from S_stage2 (index 1), which is inactive in the template.
    inactive_fill = "#C6DBF2"
    inactive_text = "#000000"
    if len(shapes) > 1:
        try:
            sh2 = get_shape(slide, shapes[1])
            inactive_fill = from_bgr(int(sh2.Fill.ForeColor.RGB))
        except Exception:
            pass
        try:
            sh2 = get_shape(slide, shapes[1])
            inactive_text = from_bgr(int(sh2.TextFrame.TextRange.Font.Color.RGB))
        except Exception:
            pass
    for i, ref in enumerate(shapes):
        is_active = ((i + 1) == int(active_phase))
        try:
            sh = get_shape(slide, ref)
            sh.Fill.Solid()
            sh.Fill.ForeColor.RGB = to_bgr(active_fill if is_active else inactive_fill)
            if sh.HasTextFrame:
                sh.TextFrame.TextRange.Font.Color.RGB = to_bgr(
                    active_text if is_active else inactive_text
                )
        except Exception:
            pass


def build_slide(pres, layout_def, fields, position, source_decks=None):
    """Insert the layout's source slide into `pres` and fill its slots.

    If the source deck is the same file as `pres`, duplicates in-place (fast, preserves
    think-cell OLE objects). Otherwise uses InsertFromFile to pull the slide from the
    slide library (or any other source deck registered in source_decks).
    source_decks: dict mapping key (e.g. 'newry_template', 'slide_library') → filename,
    resolved relative to SPECS_PATH's directory.
    """
    src_idx = layout_def["source_slide"]
    src_deck_key = layout_def.get("source_deck", "newry_template")
    specs_dir = os.path.dirname(os.path.abspath(SPECS_PATH))
    src_filename = (source_decks or {}).get(src_deck_key, "Newry Powerpoint Template 2024.pptx")
    src_path = os.path.join(specs_dir, src_filename)

    # Compare normalized paths to decide in-place vs. cross-file copy.
    try:
        same_file = os.path.normcase(os.path.abspath(pres.FullName)) == os.path.normcase(src_path)
    except Exception:
        same_file = False

    if same_file:
        new_slide = pres.Slides(src_idx).Duplicate().Item(1)
        if position == "end":
            new_slide.MoveTo(pres.Slides.Count)
        elif isinstance(position, int):
            new_slide.MoveTo(position)
    else:
        # Cross-file insert via InsertFromFile (preserves OLE/think-cell objects).
        if position == "end":
            insert_after = pres.Slides.Count
        elif isinstance(position, int):
            insert_after = max(0, int(position) - 1)
        else:
            insert_after = pres.Slides.Count
        pres.Slides.InsertFromFile(src_path, insert_after, src_idx, src_idx)
        new_slide = pres.Slides(insert_after + 1)
    res = _fill_slots(new_slide, layout_def, fields)
    return {"slide_index": new_slide.SlideIndex, **res}


def _fill_slots(new_slide, layout_def, fields):
    """Fill a slide's text/table/image/chevron slots from `fields`. Shared by
    build_slide and build_chart. Returns {filled, unknown_fields, [removed_shapes],
    [warnings]}. (The chart itself, if any, is filled separately via ppttc.)"""
    slots = layout_def["slots"]
    # Meta-fields handled outside the slot loop (not slot fills, not unknown fields).
    _META_FIELDS = {"active_phase"}
    filled, skipped, warnings = [], [], []
    for name, content in fields.items():
        if name not in slots:
            if name not in _META_FIELDS:
                skipped.append(name)
            continue
        slot = slots[name]
        # Overflow guard: warn (don't auto-shrink — fixed sizes are a brand standard).
        mc = slot.get("max_chars")
        if mc and isinstance(content, str) and len(content) > mc:
            warnings.append("'%s' is %d chars (slot fits ~%d at fixed size); shorten it or split the slide."
                            % (name, len(content), mc))
        shape = new_slide.Shapes(slot["shape"])
        if slot["kind"] == "copy_shape":
            copy_shape_to(new_slide, shape, content)
        elif slot["kind"] == "image":
            place_image(new_slide, shape, content, circle=slot.get("circle", False))
        else:
            if "set_width" in slot:
                try:
                    shape.Width = float(slot["set_width"])
                except Exception:
                    pass
            fill_slot(shape, slot, content, new_slide)
            # Real post-write overflow check (BoundHeight vs container). Complements the
            # max_chars heuristic above and catches what it misses. Only one warning per
            # slot — skip if max_chars already flagged it.
            if not (mc and isinstance(content, str) and len(content) > mc):
                w = _overflow_warning(shape, name)
                if w:
                    warnings.append(w)
        filled.append(name)
    # Apply active phase highlighting (e.g. nbd_phase_breakout with active_phase=2 or 3).
    active_phase = fields.get("active_phase")
    if active_phase is not None and "phase_chevrons" in layout_def:
        _apply_active_phase(new_slide, layout_def["phase_chevrons"], int(active_phase))
        filled.append("active_phase")
    # Optional cleanup: delete shapes the layout marks as removable (e.g. the team-page
    # full-firm montage). Done last, in reverse index order, so fill indices stay valid.
    removed = []
    for idx in sorted(layout_def.get("remove_shapes", []), reverse=True):
        try:
            new_slide.Shapes(idx).Delete()
            removed.append(idx)
        except Exception:
            pass
    out = {"filled": filled, "unknown_fields": skipped}
    if removed:
        out["removed_shapes"] = sorted(removed)
    if warnings:
        out["warnings"] = warnings
    return out


# --- think-cell chart build (build_chart op) ---

def _num(v):
    """Wrap a value as a think-cell .ppttc number cell (None -> null cell)."""
    if v is None:
        return None
    return {"number": float(v)}


def _chart_ppttc_table(chart_type, data):
    """Build the think-cell .ppttc datasheet `table` for a chart type from structured
    data. Mappings verified 2026-06-24 (see decision-log). Data shapes:
      bar/column/stacked: {categories:[...], series:[{name, values:[...]}, ...]}
      waterfall:          {categories:[...], values:[...], total_label?:"Total"}
      mekko:              {categories:[...], widths:[...], series:[{name, values:[...]}]}
      bubble:             {points:[{label, x, y, size}, ...]}
    """
    t = (chart_type or "").lower()
    if t in ("bar", "column", "stacked_bar", "stacked_column", "stacked"):
        cats = data["categories"]
        row0 = [None] + [{"string": str(c)} for c in cats]
        # think-cell's stacked-column datasheet consumes the first data row, so the first
        # real series would be dropped. Prepend a throwaway zero row (null label) so every
        # supplied series renders. Verified 2026-06-24.
        rows = [row0, [None] + [_num(0) for _ in cats]]
        for s in data["series"]:
            rows.append([{"string": str(s["name"])}] + [_num(v) for v in s["values"]])
        return rows
    if t == "waterfall":
        cats = list(data["categories"])
        vals = list(data["values"])
        total_label = data.get("total_label", "Total")
        # Transparent base series: 0 for the first bar, running cumulative before each
        # subsequent bar, 0 for the total column.
        base, running = [], 0.0
        for i, v in enumerate(vals):
            base.append(0.0 if i == 0 else running)
            running += float(v)
        base.append(0.0)
        row0 = [None] + [{"string": str(c)} for c in cats] + [{"string": str(total_label)}]
        base_row = [{"string": "Series1"}] + [_num(b) for b in base]
        # Visible series: the increments, then "e" so think-cell computes the total.
        vis_row = [{"string": "Series2"}] + [_num(v) for v in vals] + [{"string": "e"}]
        return [row0, base_row, vis_row]
    if t == "mekko":
        row0 = [None] + [{"string": str(c)} for c in data["categories"]]
        width_row = [None] + [_num(w) for w in data["widths"]]   # X-extent row (null first cell)
        rows = [row0, width_row]
        for s in data["series"]:
            rows.append([{"string": str(s["name"])}] + [_num(v) for v in s["values"]])
        return rows
    if t == "bubble":
        rows = [[None, {"string": "X"}, {"string": "Y"}, {"string": "Size"}]]
        for p in data["points"]:
            rows.append([{"string": str(p.get("label", ""))},
                         _num(p["x"]), _num(p["y"]), _num(p["size"])])
        return rows
    raise ValueError("unknown chart type %r (have: bar, column, stacked, waterfall, mekko, bubble)" % chart_type)


def _run_ppttc(template_path, name, table):
    """Fill the named think-cell element in template_path with `table` via ppttc.exe.
    Returns the path to the filled output deck. Raises on failure."""
    if not os.path.isfile(THINKCELL_PPTTC):
        raise RuntimeError("ppttc.exe not found at %s — set the THINKCELL_PPTTC env var "
                           "to your think-cell ppttc.exe path." % THINKCELL_PPTTC)
    doc = [{"template": template_path, "data": [{"name": name, "table": table}]}]
    tmpdir = tempfile.mkdtemp(prefix="tcbuild_")
    ppttc_path = os.path.join(tmpdir, "job.ppttc")
    out_path = os.path.join(tmpdir, "filled.pptx")
    with open(ppttc_path, "w", encoding="utf-8") as f:
        json.dump(doc, f)
    r = subprocess.run([THINKCELL_PPTTC, ppttc_path, "-o", out_path],
                       capture_output=True, text=True)
    if r.returncode != 0 or not os.path.isfile(out_path):
        raise RuntimeError("ppttc failed (exit %s): %s"
                           % (r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()))
    return out_path


def build_chart(pres, layout_def, fields, position, source_decks=None):
    """Build a think-cell chart slide: fill the named chart in the library deck via
    ppttc, InsertFromFile the filled slide into `pres` (preserves the live think-cell
    chart), then fill the surrounding text slots. The chart TYPE + element name live in
    layout_def["chart"] = {name, type}; the chart DATA comes from fields["chart"]."""
    chart_def = layout_def["chart"]
    src_idx = layout_def["source_slide"]
    specs_dir = os.path.dirname(os.path.abspath(SPECS_PATH))
    src_filename = (source_decks or {}).get(layout_def.get("source_deck", "thinkcell_library"),
                                             "think-cell-library.pptx")
    lib_path = os.path.join(specs_dir, src_filename)
    if "chart" not in fields:
        raise ValueError("build_chart requires a 'chart' field with the chart data")

    # Fill the chart in a throwaway copy of the library so the source is untouched.
    tmpdir = tempfile.mkdtemp(prefix="tclib_")
    work = os.path.join(tmpdir, "lib.pptx")
    shutil.copy(lib_path, work)
    table = _chart_ppttc_table(chart_def["type"], fields["chart"])
    filled = _run_ppttc(work, chart_def["name"], table)

    # InsertFromFile the filled chart slide into pres (keeps the chart live + named).
    if isinstance(position, int):
        insert_after = max(0, int(position) - 1)
    else:
        insert_after = pres.Slides.Count
    pres.Slides.InsertFromFile(filled, insert_after, src_idx, src_idx)
    new_slide = pres.Slides(insert_after + 1)

    # Fill the text chrome (everything except the chart data).
    text_fields = {k: v for k, v in fields.items() if k != "chart"}
    res = _fill_slots(new_slide, layout_def, text_fields)
    return {"slide_index": new_slide.SlideIndex, "chart": chart_def["name"], **res}


def refresh_chart(app, pres, op):
    """Replace a named think-cell chart's data in place, keeping the rest of the deck.

    Hosting-agnostic round-trip through PowerPoint ("approach A") — works for local,
    personal-OneDrive, and team-site SharePoint decks without any URL/path guessing:
      1. Save (flush edits) and remember the deck's real home (FullName — a local path
         OR a cloud URL).
      2. SaveCopyAs to a guaranteed-local temp file — PowerPoint hands us a real on-disk
         copy regardless of where the deck actually lives.
      3. Close the original (frees the handle).
      4. Run ppttc on the temp copy (updates only the named chart; preserves everything).
      5. Open the refreshed temp file and SaveAs back to the original home — PowerPoint
         uploads to SharePoint/OneDrive natively (validated silent: no check-out / keep-
         format / co-authoring prompt). Local homes just overwrite in place.
    Returns (reopened_pres, info).

    Op fields: chart_name (the think-cell element name), type (chart type for the data
    encoder), data (new data in that type's shape — same as build_chart's `chart`).
    Run as its own job — it closes and reopens the presentation."""
    name = op["chart_name"]
    table = _chart_ppttc_table(op["type"], op["data"])
    original = pres.FullName            # the deck's real home (local path or cloud URL)
    pres.Save()                         # flush current edits before copying
    tmpdir = tempfile.mkdtemp(prefix="tcrefresh_")
    local_copy = os.path.join(tmpdir, "deck.pptx")
    pres.SaveCopyAs(local_copy)         # guaranteed-local copy — no path guessing
    pres.Close()                        # release the original handle
    try:
        out = _run_ppttc(local_copy, name, table)
    except Exception as e:
        # ppttc failed — nothing was written back; reopen the ORIGINAL untouched.
        newpres = app.Presentations.Open(original, WithWindow=True)
        return newpres, {"chart": name, "refreshed": False,
                         "presentation": newpres.Name,
                         "error": "refresh failed (deck reopened unchanged): %s" % e}
    refreshed = app.Presentations.Open(out, WithWindow=True)
    refreshed.SaveAs(original)          # round-trips back to the real home (uploads if cloud)
    return refreshed, {"chart": name, "refreshed": True, "presentation": refreshed.Name}


def find_presentation(app, ref):
    if ref in (None, "active"):
        return app.ActivePresentation
    for p in app.Presentations:
        if ref.lower() in p.Name.lower() or ref.lower() in p.FullName.lower():
            return p
    # Not open — try to open it.
    return app.Presentations.Open(ref, WithWindow=True)


# ---------------------------------------------------------------------------
# profile op — characterize every object on a slide so we can edit ANY deck
# (Newry template, client deck, brand-new layout) while preserving formatting
# and catching overflow. Read-only.
# ---------------------------------------------------------------------------

def _guess_role(sh, slide_w, slide_h):
    """Heuristic role for a shape from its type, position, and content.

    Always a GUESS — positional, ~80% right on normal layouts. The caller (Claude)
    should sanity-check against the slide preview before relying on it.
    """
    name = (sh.Name or "").lower()
    t = _safe_get(sh, "Type")
    top = float(sh.Top); left = float(sh.Left); w = float(sh.Width)
    has_text = False
    try:
        has_text = bool(sh.HasTextFrame and sh.TextFrame.HasText)
    except Exception:
        pass
    if "slide number" in name:
        return "slide_number"
    if t == 19:
        return "table"
    if t == 13:
        return "image"
    if t == 3:
        return "chart"
    if t == 7:
        return "embedded_object"   # think-cell data, OLE
    if "title" in name:
        return "title"
    if not has_text:
        return "decorative"
    # text shapes, by position on the canvas. A title is a full-width banner near the
    # top; a column sub-header is only ~half width, so require >60% width to avoid
    # mis-tagging sub-heads as titles.
    if top < 0.16 * slide_h and w > 0.60 * slide_w:
        return "title"
    if top < 0.12 * slide_h and left > 0.55 * slide_w:
        return "section_tag"
    if top > 0.90 * slide_h:
        return "footnote"
    return "body"


def _profile_paragraph(pr):
    """Per-paragraph format snapshot (tolerant of mixed/inherited COM sentinels)."""
    pf = pr.ParagraphFormat
    bullet = pf.Bullet
    color = None
    try:
        color = from_bgr(int(pr.Font.Color.RGB))
    except Exception:
        pass
    align = _safe_get(pf, "Alignment")
    return {
        "text": pr.Text.replace("\r", "").strip(),
        "font": _safe_get(pr.Font, "Name"),
        "size": _safe_get(pr.Font, "Size"),
        "bold": bool(_safe_get(pr.Font, "Bold", False)),
        "italic": bool(_safe_get(pr.Font, "Italic", False)),
        "color": color,
        "align": PP_ALIGN_NAME.get(int(align), align) if isinstance(align, (int, float)) and align in PP_ALIGN_NAME else align,
        "bullet": bool(_safe_get(bullet, "Visible", False)),
    }


def _estimate_capacity(sh, font_size):
    """Rough character/line budget for a text shape at a given font size."""
    ml = mr = 7.2
    mt = mb = 3.6
    try:
        tf = sh.TextFrame
        ml = _safe_get(tf, "MarginLeft", 7.2) or 7.2
        mr = _safe_get(tf, "MarginRight", 7.2) or 7.2
        mt = _safe_get(tf, "MarginTop", 3.6) or 3.6
        mb = _safe_get(tf, "MarginBottom", 3.6) or 3.6
    except Exception:
        pass
    usable_w = max(1.0, float(sh.Width) - ml - mr)
    usable_h = max(1.0, float(sh.Height) - mt - mb)
    fs = float(font_size) if font_size and font_size > 0 else 18.0
    cpl = max(1, int(usable_w / (fs * CHAR_W_FACTOR)))
    max_lines = max(1, int(usable_h / (fs * LINE_SPACING)))
    return {
        "chars_per_line": cpl,
        "est_max_lines": max_lines,
        "est_char_capacity": cpl * max_lines,
        "based_on_font_size": round(fs, 1),
    }


def _measure_overflow(shape):
    """Real post-write overflow check: compare the actual laid-out text height
    (TextRange.BoundHeight, what PowerPoint really rendered) against the usable
    container height. Far more accurate than the char/line heuristic, and it
    catches cases the heuristic misses (wrapping, mixed sizes, hidden growth
    from a substituted font). Returns None if it can't measure (no text frame,
    empty, or the COM call fails) so callers can fall back to the heuristic.

    Tolerance is 1pt. Does not consider autofit: Newry boxes are fixed-size
    (autofit off), so BoundHeight > usable height is a true overflow."""
    try:
        if not shape.HasTextFrame:
            return None
        tf = shape.TextFrame
        tr = tf.TextRange
        if not tr.Text.strip():
            return None
        bound_h = float(tr.BoundHeight)
        mt = _safe_get(tf, "MarginTop", 3.6) or 3.6
        mb = _safe_get(tf, "MarginBottom", 3.6) or 3.6
        usable_h = max(1.0, float(shape.Height) - mt - mb)
        return {
            "bound_height": round(bound_h, 1),
            "usable_height": round(usable_h, 1),
            "fill_ratio": round(bound_h / usable_h, 2) if usable_h else None,
            "overflows": bound_h > usable_h + 1.0,
        }
    except Exception:
        return None


def _overflow_warning(shape, name=None):
    """Return an actionable overflow warning string (or None). Prefers the real
    measurement; silent on anything it can't measure."""
    mo = _measure_overflow(shape)
    if not mo or not mo["overflows"]:
        return None
    label = ("'%s' " % name) if name else ""
    return ("%stext overflows its box by ~%dpt (needs ~%dpt, box holds ~%dpt at "
            "fixed size) — shorten or split the slide; don't shrink the font."
            % (label, round(mo["bound_height"] - mo["usable_height"]),
               round(mo["bound_height"]), round(mo["usable_height"])))


def profile_slide(slide, slide_w, slide_h):
    """Return a per-shape profile of a slide: index, name, role guess, geometry,
    per-paragraph formatting, and a capacity estimate for text shapes."""
    out = []
    for i in range(1, slide.Shapes.Count + 1):
        sh = slide.Shapes(i)
        entry = {
            "index": i,
            "name": sh.Name,
            "type": _safe_get(sh, "Type"),
            "role_guess": _guess_role(sh, slide_w, slide_h),
            "geometry": {
                "left": round(float(sh.Left), 1),
                "top": round(float(sh.Top), 1),
                "width": round(float(sh.Width), 1),
                "height": round(float(sh.Height), 1),
            },
        }
        has_tf = False
        try:
            has_tf = bool(sh.HasTextFrame and sh.TextFrame.HasText)
        except Exception:
            pass
        if has_tf:
            tr = sh.TextFrame.TextRange
            pc = tr.Paragraphs().Count
            paras, sizes = [], []
            for p in range(1, pc + 1):
                pp = _profile_paragraph(tr.Paragraphs(p))
                paras.append(pp)
                if isinstance(pp["size"], (int, float)) and pp["size"] > 0:
                    sizes.append(pp["size"])
            body_fs = max(set(sizes), key=sizes.count) if sizes else 18.0
            entry["char_count"] = len(tr.Text.replace("\r", "").rstrip())
            entry["paragraph_count"] = pc
            entry["paragraphs"] = paras
            entry["capacity"] = _estimate_capacity(sh, body_fs)
        if _safe_get(sh, "Type") == 19:  # table
            try:
                tbl = sh.Table
                entry["table"] = {"rows": tbl.Rows.Count, "cols": tbl.Columns.Count}
            except Exception:
                pass
        out.append(entry)
    return out


def run_job(job):
    app = win32com.client.Dispatch("PowerPoint.Application")
    pres = find_presentation(app, job.get("presentation", "active"))
    specs = None
    results = []
    mutated = False
    for op in job.get("ops", []):
        kind = op.get("op")
        try:
            if kind == "profile":
                sidx = op["slide"]
                sl = pres.Slides(sidx)
                sw = float(pres.PageSetup.SlideWidth)
                shh = float(pres.PageSetup.SlideHeight)
                prof = profile_slide(sl, sw, shh)
                results.append({"op": kind, "slide": sidx, "ok": True,
                                "slide_size": {"width": round(sw, 1), "height": round(shh, 1)},
                                "shapes": prof})
                continue
            if kind in ("build", "build_chart"):
                mutated = True
                if specs is None:
                    with open(SPECS_PATH, "r", encoding="utf-8") as f:
                        specs = json.load(f)
                layout_name = op["layout"]
                if layout_name not in specs["layouts"]:
                    raise ValueError("unknown layout %r (have: %s)" % (layout_name, ", ".join(specs["layouts"])))
                layout_def = specs["layouts"][layout_name]
                src_decks = specs.get("source_decks", {})
                fn = build_chart if kind == "build_chart" else build_slide
                built = fn(pres, layout_def, op.get("fields", {}), op.get("position", "end"),
                           source_decks=src_decks)
                results.append({"op": kind, "layout": layout_name, "ok": True, "after": built})
                continue
            if kind == "refresh_chart":
                # Closes + reopens the presentation (ppttc rewrites the file). Run as its
                # own job — reassigns `pres`; the file is already saved so no trailing save.
                pres, info = refresh_chart(app, pres, op)
                results.append({"op": kind, "ok": info.get("refreshed", False), "after": info})
                continue
            slide = pres.Slides(op["slide"])
            shape = get_shape(slide, op["shape"])
            mutated = True
            edit_warn = None
            if kind == "write_textbox":
                tf = shape.TextFrame.TextRange
                clean_write_textbox(tf, op["paragraphs"])
                after = [read_format(tf.Paragraphs(i)) for i in range(1, tf.Paragraphs().Count + 1)]
                edit_warn = _overflow_warning(shape)
            elif kind == "edit_text_preserve":
                tf = shape.TextFrame.TextRange
                edit_preserve(tf, op["paragraphs"])
                after = [read_format(tf.Paragraphs(i)) for i in range(1, tf.Paragraphs().Count + 1)]
                # Overflow check: prefer the real post-write measurement (BoundHeight vs
                # container). Fall back to the char/line heuristic only if the measurement
                # can't be taken. Warn, never shrink — fixed sizes are a brand standard.
                edit_warn = _overflow_warning(shape)
                if edit_warn is None and _measure_overflow(shape) is None:
                    try:
                        fsz = float(tf.Paragraphs(1).Characters(1, 1).Font.Size)
                    except Exception:
                        fsz = 18.0
                    cap = _estimate_capacity(shape, fsz)
                    cpl = max(1, cap["chars_per_line"])
                    lines_needed = sum(((len(str(p)) + cpl - 1) // cpl) for p in op["paragraphs"] if str(p).strip())
                    if lines_needed > cap["est_max_lines"]:
                        edit_warn = ("edited text needs ~%d lines but the box fits ~%d at this size; "
                                     "it will overflow — shorten or split the slide."
                                     % (lines_needed, cap["est_max_lines"]))
            elif kind == "write_table":
                write_table(shape, op["rows"], op.get("table_opts"), slide)
                after = "table written (%d rows)" % len(op["rows"])
            else:
                raise ValueError("unknown op %r" % kind)
            res = {"op": kind, "slide": op["slide"], "shape": op["shape"], "ok": True, "after": after}
            if edit_warn:
                res["warnings"] = [edit_warn]
            results.append(res)
        except Exception as e:
            results.append({"op": kind, "slide": op.get("slide"), "shape": op.get("shape"), "ok": False, "error": str(e)})
    if mutated:
        pres.Save()
    return {"ok": all(r["ok"] for r in results), "presentation": pres.Name, "results": results}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "no job provided"}))
        sys.exit(1)
    arg = sys.argv[1]
    if arg == "--file":
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            job = json.load(f)
    elif arg == "-":
        job = json.load(sys.stdin)
    else:
        job = json.loads(arg)
    print(json.dumps(run_job(job), indent=2))


if __name__ == "__main__":
    main()
