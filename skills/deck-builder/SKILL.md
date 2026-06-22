# Deck Builder Skill

Build and edit Newry PowerPoint slides by calling a small Python tool (`deck_writer.py`) that controls a live PowerPoint window. The tool writes text and tables the *clean* way, so it never destroys the formatting that's already on a slide.

## Triggers

"build slides", "create a deck", "make a slide", "add a slide", "draft slides", "update the deck", "ppt"

## The one thing to understand first

A consulting slide is almost never plug-and-play. Most of the time a consultant hands you data and a rough idea and wants a *custom* slide. So this tool is built around two jobs:

- **Editing a slide that already exists** (any deck, any template, ours or a client's) — change the words, keep the look exactly as it was.
- **Building a new slide** — start from one of our ready-made layouts, fill it in, and adjust from there.

The ready-made layouts are **starting points, not finished slides.** Treat them as "the closest thing we already have — clone it and adapt."

## Before you touch anything

1. PowerPoint must be open with the target file. The tool drives the open window.
2. ppt-mcp must be loaded in this session (the `ppt_*` tools). You use those to *look* at slides; you use `deck_writer.py` to *change* them.
3. Always confirm which presentation you're working on with `ppt_list_presentations`, then `ppt_activate_presentation`.

## How to run the tool

The tool takes a "job" — a small JSON file listing what you want done — and runs it.

```
PYTHONIOENCODING=utf-8 "C:/Users/sshank/AppData/Local/Programs/Python/Python314/python.exe" \
  "<workspace>/skills/deck-builder/deck_writer.py" --file job.json
```

Write the job to a temp file (e.g. in `Downloads`) and pass it with `--file`. The tool prints back JSON saying what it did, including any **overflow warnings** and a read-back of what it wrote. Always read that output.

## The loop — do this every time

1. **Look** — `ppt_get_slide_preview` to see the slide; for editing, also **profile** it (below).
2. **Act** — run a `deck_writer.py` job.
3. **Check** — re-preview the slide and read the tool's output. The visual preview is the approval step.

If you invented any specific facts (numbers, names, dates), say so plainly after writing: "I generated these numbers — verify before using."

---

## Profile: how to understand any slide

Before editing an unfamiliar slide, profile it. This is the move that lets the tool work on *any* deck, not just ours.

```json
{"presentation": "Glass Core", "ops": [{"op": "profile", "slide": 12}]}
```

For every object on the slide it tells you:
- **What it is** — a best-guess role (title, body, footnote, section tag, table, image, chart, decorative). It's a guess from position and type — sanity-check it against the preview.
- **Where it is** — position and size.
- **How it's formatted** — font, size, bold/italic, color, alignment, bullets, per paragraph.
- **How much fits** — a rough character/line budget for the box. Use it to catch overflow *before* you write.

The profile is read-only. Use what it tells you to write edits that match the slide and won't overflow.

---

## Mode A — Edit an existing slide

Goal: change the words, keep the formatting.

1. **Profile** the slide (and/or `ppt_get_text` on the shape) so you know its structure and how much text fits.
2. **Write the edit** with `edit_text_preserve`. You pass plain lines of text; the tool keeps each line's existing format (size, bold, color, bullets, indent) by position.

```json
{"presentation": "Glass Core", "ops": [
  {"op": "edit_text_preserve", "slide": 12, "shape": 3,
   "paragraphs": ["KEY FINDINGS", "First point goes here", "Second point goes here"]}
]}
```

- Line 1 keeps line 1's old format, line 2 keeps line 2's, and so on. Add more lines than were there and the extras copy the last line's format.
- If your new text is longer than the box holds (the profile told you the budget), it will overflow. Fixed font sizes are a Newry brand standard — **don't shrink to fit.** Shorten the text or split the slide.

Use `write_textbox` (Mode B style) instead only when you're deliberately changing the formatting, not just the words.

---

## Mode B — Build a new slide

Goal: a strong first draft, fast, from the closest layout we already have.

1. **Pick the nearest layout** from the library table below. State your pick: "I'll use the figure-two-thirds layout — say if you'd rather something else."
2. **Fill it** with a `build` job. Give it the fields the layout lists.
3. **Preview, then adapt** — resize, add, or remove pieces as the actual content needs. The layouts are starting points; expect to adjust.

```json
{"presentation": "Glass Core", "ops": [
  {"op": "build", "layout": "findings_summary", "position": "end",
   "fields": {
     "title": "Three forces are reshaping the market",
     "body": {"header": "KEY FINDINGS", "bullets": ["First finding", "Second finding", "Third finding"]},
     "callout_bar": "Source: Newry analysis"
   }}
]}
```

- `position` is `"end"` (append) or a slide number to insert at.
- Each layout's exact fields are described in `template-specs.json` (the `description` on each layout). Read it when filling a layout you haven't used.
- Charts and figures stay **manual / think-cell** — the build fills only the text around them.

### Tables (used by several layouts)

Pass a table as rows. Row 1 is usually the header. Cells can be a plain string, or `{text, fill, color, bold, size, align, swatch}` for a colored/styled cell, or `{paragraphs: [...]}` for a cell with multiple formatted lines. `swatch` maps a name to a color set on the layout (e.g. `pursue` → green on the prioritization table). The table flexes its row and column count to fit your data.

**Merged cells:** some template tables merge cells (e.g. a category label spanning rows). Merged cells collide with row-by-row writing — two logical rows share one physical cell. A layout whose table needs to flex sets `"unmerge": true` in its `table_opts`, which flattens the table to a clean grid before filling. On the **edit** path, leave it off so a client table's intentional merges are respected; turn it on only when you want to flatten-and-rewrite a merged table.

---

## The layout library

19 starting-point layouts. Most come from our blank template; five come from the strategic marketing reference deck. The tool pulls each from the right source file automatically.

| Layout | Use it for |
|---|---|
| `cover` | Title / cover page |
| `chapter_divider` | Section divider |
| `toc` | Table of contents |
| `content` | General content: subhead + bullets, optional pull-quotes + takeaway |
| `findings_summary` | Summary of findings — subhead + dense bullets, optional bottom bar |
| `two_column` | Two columns, each a header + bullets (e.g. background & objectives) |
| `comparison_table` | Gradient comparison table (high / medium / low shading) |
| `qualitative_comparison` | Side-by-side cards across N items, image row on top |
| `prioritization_table` | Opportunity/segment table color-coded pursue / investigate / deprioritize |
| `value_chain` | 4-stage process flow (chevrons) with supporting points |
| `process_flow_quotes` | Multi-stage manufacturing flow + bullets + expert quotes |
| `timeline` | Fixed 10-year timeline with 3 events |
| `interview_list` | List of interviewees (name / title / organization) |
| `team_page` | Engagement team bios with circular headshots |
| `market_sizing` | Text around a think-cell market-size chart |
| `figure_two_thirds` | Figure on left ~2/3, notes column on right |
| `full_chart` | Full-width chart, source line at bottom |
| `full_visual_quote` | Full-page visual (e.g. a map) with a quote bar at the bottom |
| `back_page` | Closing page: confidentiality + contributors |

### Adding a new layout

Two steps, ~15 minutes:
1. Put a clean copy of the slide in `slide-library.pptx` (or use a slide already in our template).
2. Add an entry to `template-specs.json`: which source deck + slide, and a named slot for each shape you want to fill (shape index + kind + any format). Run `ppt_list_shapes` on the slide to get the indices.

---

## Job reference (the ops)

All jobs look like: `{"presentation": "<name or substring>", "ops": [ ... ]}`. `presentation` can be `"active"`.

| Op | What it does | Key fields |
|---|---|---|
| `profile` | Read a slide: every object's role, format, capacity | `slide` |
| `edit_text_preserve` | Change text, keep existing format | `slide`, `shape`, `paragraphs` (plain strings) |
| `write_textbox` | Write text with formatting you specify | `slide`, `shape`, `paragraphs` (objects: text/bold/size/color/italic/font/align) |
| `write_table` | Write a table cell-by-cell, keeping Newry colors | `slide`, `shape`, `rows`, optional `table_opts` |
| `build` | Make a new slide from a layout | `layout`, `fields`, optional `position` |

`shape` is the 1-based index from `profile` / `ppt_list_shapes` (or the shape's name).

---

## Gotchas worth remembering

- **Don't use `ppt_set_text` / `ppt_find_replace_text` on a shape with mixed formatting** (a bold header over normal bullets). It collapses everything into one style. That's the whole reason `deck_writer.py` exists — use it instead.
- **`ppt_find_replace_text` strips whitespace** from the search text, so ` - ` matches hyphens inside words. Inspect per-shape instead of blind find/replace.
- **Charts stay manual / think-cell.** The tool fills the title, units, notes, and labels around a chart — never the chart data.
- **Airtable headshots:** download with PowerShell (`Invoke-WebRequest`), not Python/curl (they fail with a TLS error), and use the `thumbnails.full.url` link. `place_image` already does this.
- **Process-flow arrows** are the "Chevron" shape (type 52), not "Pentagon".
- **Overflow = warn, never shrink.** Fixed sizes are a brand standard. Shorten or split. Both `build` and `edit_text_preserve` return a warning when text won't fit; the text is still written.
- **Editing drops inline emphasis.** `edit_text_preserve` keeps each line's *paragraph* format (size, color, bold, bullets) but a rewritten line can't keep a bold/colored phrase from the *middle* of the old text — the line takes its leading format. Expected: on a rewrite, re-apply any mid-line emphasis you want in the new version.
- **Always re-check after writing** — re-preview the slide and read the tool's output. The preview is for your eyes and the user's approval.

## Non-Newry / client decks

Same approach. Skip our layouts and brand standards — profile the deck first to learn its own fonts, colors, and structure, then edit in place with `edit_text_preserve` so you match whatever is already there.
