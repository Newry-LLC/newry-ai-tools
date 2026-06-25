# Deck Builder Skill

Build and edit Newry PowerPoint slides by calling a small Python tool (`deck_writer.py`) that controls a live PowerPoint window. It writes text and tables the clean way, without destroying the formatting already on a slide.

## Triggers

"build slides", "create a deck", "make a slide", "add a slide", "draft slides", "update the deck", "ppt"

## The one thing to understand first

Every slide needs custom work. This tool handles two jobs:

- **Editing a slide that already exists** (any deck, any template, ours or a client's) — change the words, keep the look exactly as it was.
- **Building a new slide** — start from one of our ready-made layouts, fill it in, and adjust from there.

The ready-made layouts are **starting points, not finished slides.** Treat them as "the closest thing we already have — clone it and adapt."

## Model selection

Pick the model before starting. The choice matters — previews and shape-dump results accumulate in context fast, and the wrong model wastes either money or quality.

- **Sonnet** — default for most sessions: handles formatting judgment, layout decisions, and mechanical edits at a good cost/speed balance.
- **Haiku** — when edits are fully specified upfront (exact text supplied, no content decisions needed). Faster and cheaper; may miss edge cases in formatting or overflow.
- **Opus** — when writing consulting-grade content from scratch (pyramid structure, argument design, so-what synthesis). Overkill for pure edit/build work.

## Before you touch anything

1. PowerPoint must be open with the target file. The tool drives the open window.
2. ppt-mcp must be loaded in this session (the `ppt_*` tools). **You use those only to *look* at slides; you always use `deck_writer.py` to *change* text and tables — never the `ppt_*` write tools.** (Why: see the rule below.)
3. Always confirm which presentation you're working on with `ppt_list_presentations`, then `ppt_activate_presentation`.

---

## Newry slide standards

Apply these to every new slide and every edit. Check before finishing any slide.

**Typography**
- Font: Aptos throughout — never substitute another font
- Slide title (H1): Aptos Display, 28pt, 1–2 lines max
- Section subhead (H2): APTOS BOLD, ALL CAPS, Newry Blue (#1E4C7F)
- Column/box header (H3): Aptos Bold, Capitalize Each Word, Black
- Body text: 14–20pt; table text: 12pt minimum
- No final punctuation on bulleted text
- Line spacing: 6–12pt between lines

**Punctuation**
- En dashes (–) not em dashes (—) for parentheticals, ranges, and quote attributions
- Spaces on both sides of en dashes
- No periods at end of bullet points
- Oxford comma

**Bullets**
- Consistent bullet style across all slides in the deck
- ¼" between bullet/dash character and text
- No single-item bullets — one point becomes a sentence, not a bullet

**Shapes and layout**
- Square corners only — no rounded corners
- No 3D gradients, no drop shadows
- Chevrons: square edge first, then indented
- Align all shape edges and text box boundaries to page margins

**Colors**
- Newry Blue (#1E4C7F): chart/text box titles, shape fill (the primary color)
- Quotes: always light grey fill (#D9D9D9)
- Non-quote text blocks: second lightest blue fill
- Red (#920D29) and yellow (#FDBC0D): sparingly — highlights and stoplight charts only; never general text fill

**Tables**
- Header row: light grey by default
- Gradient chart preferred over traditional stoplight (accessibility)

**Sourcing**
- Every body slide that cites data or research needs a source line: Aptos 12pt, grey, bottom of slide
- Superscript numbers for footnote citations

**Slide titles — action title standard**
- Titles state the "so what" as a declarative sentence, not a topic label. Full rule in "Writing consulting-grade slides" below.

---

## Writing consulting-grade slides

Formatting is necessary but not sufficient — a well-formatted slide that says nothing still fails. This is the Pyramid Principle as Newry practices it; apply it while drafting any content.

**One slide, one claim.** Every slide makes a single point, and that point *is* its title; the body exists only to prove it. Two unrelated points = two slides.

**The title is a claim, not a label.** Write it as a complete declarative sentence stating the conclusion — the "so what" — not the topic.
- Before writing it, ask: *"So what? Who cares? What should the reader conclude?"*
- It must summarize the slide *and* flow with the slides around it — one rung of the deck's argument, not a standalone.
- Label → claim: "Market overview" → "The specialty chemicals market is growing 8% annually, driven by automotive demand."

**Every bullet makes a claim too** — a finding, result, or conclusion, not a description of process, how the work was organized, or background. If a bullet describes method or context instead of asserting something, rewrite it or cut it.

**The body proves the title — completely and without overlap:**
- *Parallel* — same-level points are the same type of idea at the same altitude (don't mix a cause, a number, and a recommendation as peers)
- *Ordered* — by a logic the reader follows (importance, sequence, structure), not the order you discovered them
- *MECE* — no two points overlap, and together they're complete enough to prove the claim
- *Tight* — every line relates to the title; nothing repeats another

**A multi-slide deck is itself a pyramid.** Overall conclusion on top; each section's main message supports it; each slide supports its section. Standard arc: introduction (background & objectives, method) → body (each main message with its supporting slides) → summary of findings with a clear call to action → conclusion / next steps. Sketch the sequence of slide *titles* first, so each is one rung of one argument. (The summary-of-findings page has its own skill — the SOF Toolkit.)

---

## How to run the tool

The tool takes a "job" — a small JSON file listing what you want done — and runs it.

```
PYTHONIOENCODING=utf-8 python "<workspace>/skills/deck-builder/deck_writer.py" --file job.json
```

If `python` isn't on your PATH, use the full path to your Python executable instead. Write the job to a temp file (e.g. in `Downloads`) and pass it with `--file`. The tool prints back JSON with what it did, including any **overflow warnings** and a read-back of what it wrote. Always read that output.

---

## Profile: how to understand any slide

Before editing an unfamiliar slide, profile it.

```json
{"presentation": "Glass Core", "ops": [{"op": "profile", "slide": 12}]}
```

For every object on the slide it tells you:
- **What it is** — a best-guess role (title, body, footnote, section tag, table, image, chart, decorative). Sanity-check against the preview.
- **Where it is** — position and size.
- **How it's formatted** — font, size, bold/italic, color, alignment, bullets, per paragraph.
- **How much fits** — a rough character/line budget for the box. Use it to catch overflow *before* you write.

The profile is read-only.

**Re-profile after external edits.** If a consultant edits slides in PowerPoint between your operations, call `ppt_get_slide_info` on the affected slides. If the shape count changed compared to the last profile, re-profile before issuing any edit ops — otherwise your shape indices will be wrong.

---

## Mode A — Edit an existing slide

Goal: change the words, keep the formatting. For non-Newry / client decks: skip the Newry standards above — profile the deck first to learn its own fonts and colors, then edit in place.

1. **Profile** the slide (and/or `ppt_get_text` on the shape) to know its structure and how much text fits.
2. **Write the edit** with `edit_text_preserve`. Pass plain lines of text; the tool keeps each line's existing format (size, bold, color, bullets, indent) by position.

```json
{"presentation": "Glass Core", "ops": [
  {"op": "edit_text_preserve", "slide": 12, "shape": 3,
   "paragraphs": ["KEY FINDINGS", "First point goes here", "Second point goes here"]}
]}
```

- Line 1 keeps line 1's old format, line 2 keeps line 2's, and so on. Extra lines copy the last line's format.
- **Inline bold:** wrap a phrase in `**…**` to bold just that span (e.g. `"**Lack of alignment:** no common standards"` → bold label, regular rest). Works in `edit_text_preserve`, `write_textbox`, and table cells — one call, no second pass.
- If your new text is longer than the box holds (the profile told you the budget), it will overflow. Fixed font sizes are a Newry brand standard — **don't shrink to fit.** Shorten the text or split the slide. The tool measures the actual rendered text height after writing and returns a precise overflow warning — read it.
- **Underflow matters too.** If your replacement is much *shorter* than what it replaced, the box looks half-empty and unbalanced against the rest of the slide. Aim to roughly match the **length and structure** of the text you're replacing (same number of bullets, similar line count) — don't just drop in one short line where three full ones were.
- Read the tool's output after every write. **Preview sparingly** — the overflow check and read-back are sufficient for clean mechanical edits. Use `ppt_get_slide_preview` only when: (a) the overflow check fired, (b) the layout is visually complex (bold labels, merged cells, multi-column), or (c) it's the final approval checkpoint for that slide. Don't preview after every individual shape write.

Use `write_textbox` (Mode B style) only when you're deliberately changing the formatting, not just the words.

---

## Mode B — Build a new slide

Goal: a strong first draft, fast, from the closest layout we already have.

**One slide at a time by default** — build one, preview it, get a reaction, then move on. If the consultant explicitly wants several built in one go ("build all five," "batch these"), do it: a single job can carry multiple `build` ops, and you still preview each afterward. Don't batch unprompted — a wrong call multiplied across slides is worse than catching it on slide one.

0. **Which deck family?** Settle this before picking a layout — the two families don't mix.
   - **NBD proposal** — a pitch/proposal for a prospective client. Use the **NBD proposal layouts** (`nbd_*` family). Covers, dividers, growth levers, approach modules, team, and back cover are all purpose-built for proposals.
   - **Project / report deck** — findings, analysis, client deliverables. Use the **project / report layouts** (everything else).
   - If the request doesn't make it obvious, ask in one line: "Is this an NBD proposal or a project/report deck?" The answer picks the family. Don't mix them.

1. **Pick the nearest layout** from the right family's table below. State your pick: "I'll use the figure-two-thirds layout — say if you'd rather something else."
2. **Fill it** with a `build` job. Give it the fields the layout lists.
3. **Preview at completion checkpoints, not after every op.** Run `ppt_get_slide_preview` once after finishing a slide (or a batch of slides), not after each individual write. Check:
   - No text overflow — all text visible, nothing cut off
   - Font is Aptos (not a substituted font)
   - H2 subheads are ALL CAPS and Newry Blue
   - Bullet style matches surrounding slides in the deck
   - Action title states a clear so-what (not a topic label)
   - Source line present if any data or citations appear on the slide
   - No rounded corners or drop shadows on shapes
4. **Adapt** — resize, add, or remove pieces as the content needs. The layouts are starting points; expect to adjust.

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
- Each layout's exact fields are in `template-specs.json` (the `description` on each layout). Read it when filling a layout you haven't used.
- Charts and figures stay **manual / think-cell** — the build fills only the text around them.

### Tables (used by several layouts)

Pass a table as rows. Row 1 is usually the header. Cells can be a plain string, or `{text, fill, color, bold, size, align, swatch}` for a colored/styled cell, or `{paragraphs: [...]}` for a cell with multiple formatted lines. `swatch` maps a name to a color set on the layout (e.g. `pursue` → green on the prioritization table). The table flexes its row and column count to fit your data.

**Editing an existing table preserves its formatting by default** — each cell's fill, font color, weight, and size stay put; only the text changes (plus any explicit cell overrides). So a navy header row or a white-on-logo hidden column survives a text swap. Cell text also supports `**bold**` markup. To restyle a table wholesale instead, pass `table_opts: {"preserve_format": false}`.

**Merged cells:** some template tables merge cells (e.g. a category label spanning rows). Merged cells collide with row-by-row writing. A layout whose table needs to flex sets `"unmerge": true` in its `table_opts`, which flattens the table to a clean grid before filling. On the **edit** path, leave it off so a client table's intentional merges are respected; turn it on only when you want to flatten-and-rewrite a merged table.

---

## The layout library

34 starting-point layouts in **two families** (you settled the family in Mode B step 0). Six of them are live think-cell chart layouts built with `build_chart` (see "Building think-cell charts"). **Pick by the slide's job:** find the intent group below — it narrows you to a few candidates — then disambiguate within it. Don't scan the whole list and gestalt-match. The tool pulls each from the right source file automatically; you never name the source deck.

**Cross-family overlap:** `cover`, `chapter_divider`, the team page, and the back page exist in both libraries — use the `nbd_` variant in a proposal, the plain one in a project deck.

### Project / report layouts (25)

For findings, analysis, and client deliverables. Grouped by intent — exact fields for each are in `template-specs.json`.

**Front / back matter** — `cover` (title page) · `chapter_divider` (section divider) · `toc` (contents) · `back_page` (confidentiality + contributors)

**Make a text argument** — pick by what supports the point:
- `content` — subhead + bullets with room for pull-quotes and a takeaway bar; use when quotes back the point
- `findings_summary` — dense bullets, no quote boxes (more body space); use when the bullets are the whole story
- `two_column` — two parallel header+bullet groups (e.g. background & objectives)

**Show a chart / figure** — two kinds:
- **Build a real think-cell chart** (`chart_*` layouts, via the `build_chart` op — see "Building think-cell charts" below): `chart_waterfall` (cost/bridge breakdown) · `chart_bubble` (2×2 quadrant matrix) · `chart_stacked_bar` (+ `_half`) · `chart_mekko` (+ `_half`). The chart is live and editable; you supply the data and the tool draws it.
- **Text-only chart layouts** (the chart stays think-cell/manual — these fill just the text around a chart you place yourself): `full_chart` (chart fills the body, source line only) · `figure_two_thirds` (chart left ~2/3, notes column right) · `market_sizing` (market-size chart — CAGR oval, year axis, notes) · `full_visual_quote` (full-bleed image/map + quote bar)

**Compare options:**
- `comparison_table` — gradient shading by rating (high / medium / low)
- `qualitative_comparison` — a card per item across N columns, image row on top
- `prioritization_table` — rows color-coded pursue / investigate / deprioritize

**Process / flow** — `value_chain` (4 chevron stages + supporting points) · `process_flow_quotes` (multi-stage flow + bullets + expert quotes)

**Timeline** — `timeline` (fixed 10-year axis, 3 events)

**People** — `team_page` (3 featured bios, circular headshots) · `interview_list` (list of interviewees: name / title / org)

### NBD proposal layouts (9)

For new-business proposals/pitches. Source: the NBD proposal template. **Use these — not the project layouts — whenever you're building a proposal.**

| Layout | Use it for |
|---|---|
| `nbd_cover` | Proposal cover — value-prop headline + "Proposal for \<Client\>" |
| `nbd_section_divider` | Proposal section divider (e.g. "Approach", "Our Team") |
| `nbd_experience_grid` | Prior Newry experience across the client's value chain |
| `nbd_growth_levers` | Growth-levers table — one row per strategic lever |
| `nbd_approach_modules` | Two-module approach overview with timeframes |
| `nbd_module_breakout` | Breakout page for one module of a 2-module approach |
| `nbd_phase_breakout` | Breakout page for one phase of a 3-phase approach |
| `nbd_team_six` | Engagement team — 6 people, 2×3 headshot grid |
| `nbd_back_cover` | Back cover — Newry contacts + confidentiality notice |

---

## Building think-cell charts (`build_chart`)

Newry charts are think-cell charts. `build_chart` makes a real, live think-cell chart slide: you give it the numbers, it fills one of our named chart templates (via think-cell's `ppttc` tool) and drops the finished slide into the deck. The chart stays a true think-cell chart — editable, refreshable, with think-cell's own connectors and labels.

Requires think-cell installed (it is, firm-wide). Use `build_chart` — **not** `build` — for these.

**Available chart layouts:** `chart_waterfall` (cost/bridge breakdown) · `chart_bubble` (2×2 quadrant matrix) · `chart_stacked_bar` / `chart_stacked_bar_half` (stacked column, two-thirds / half width) · `chart_mekko` / `chart_mekko_half` (marimekko — width encodes share).

A `build_chart` job is like a `build` job plus a `chart` field carrying the data. The chart type comes from the layout; you provide the data in the shape that type expects:

- **Waterfall** — `{"categories": [...], "values": [n, n, ...], "total_label": "Total"}`. One value per category (the increments); the tool floats the bars and computes the total automatically. Column count flexes to your data.
- **Bubble** — `{"points": [{"label": "A", "x": 1.5, "y": 3.0, "size": 6}, ...]}`. One point per bubble; `size` sets the circle size.
- **Stacked bar/column** — `{"categories": [...], "series": [{"name": "Premium", "values": [...]}, ...]}`. Up to 3 series (the template holds 3; more are dropped). The tool handles the datasheet quirks for you.
- **Mekko** — `{"categories": [...], "widths": [n, ...], "series": [{"name": "...", "values": [...]}, ...]}`. `widths` set the column widths (segment share); the series stack within each column.

```json
{"presentation": "Glass Core", "ops": [
  {"op": "build_chart", "layout": "chart_waterfall", "position": "end",
   "fields": {
     "chart": {"categories": ["Materials", "Labor", "Overhead"], "values": [40, 25, 20], "total_label": "Total Cost"},
     "title": "Materials drive over half of unit cost",
     "subhead": "COST STRUCTURE",
     "notes": ["KEY TAKEAWAYS", "First point", "Second point"],
     "source": "Source: Newry analysis"
   }}
]}
```

The text fields (`title`, `subhead`, `notes`, `source`) fill the slide's chrome, same as a normal `build`. Preview and approve after, like any build.

**Two things to watch:**
- **Theme colors.** The chart slide adopts the target deck's theme. Build into a Newry-themed deck so colors come out right (in a blank/non-Newry deck, accent colors shift).
- **Category labels** that carry footnote superscripts in the template may keep the template's text — check and fix the labels in the preview.

### Refreshing an existing chart with new numbers (`refresh_chart`)

Update a chart's data in place, keeping the rest of the slide and deck. The chart must have a think-cell **name**:
- **Charts built with `build_chart` are already named** — refresh them directly.
- **A chart someone made by hand is usually unnamed.** Name it once in think-cell: click the chart, type a unique name in the **AddRangeData Name** field on its mini-toolbar, save. After that it's refreshable forever. (If the consultant asks to refresh an unnamed chart, walk them through this once.)

```json
{"presentation": "Glass Core", "ops": [
  {"op": "refresh_chart", "chart_name": "waterfall v1 two thirds page", "type": "waterfall",
   "data": {"categories": ["A", "B", "C"], "values": [50, 30, 15], "total_label": "Total"}}
]}
```

`type` + `data` use the same per-type shapes as `build_chart` (above). Two things to know:
- **Run it as its own job.** ppttc can only rewrite the whole file, so refresh saves, closes, rewrites, and reopens the deck — the window briefly closes and reopens. Don't combine it with other ops.
- **Works on any deck — local, OneDrive, or team-site SharePoint.** It round-trips through PowerPoint: it saves a local copy, refreshes that, then saves back to wherever the deck actually lives (uploading to SharePoint/OneDrive natively). No local-sync requirement and no path guessing — a deck open straight from a SharePoint web address works fine.

---

## Job reference (the ops)

All jobs look like: `{"presentation": "<name or substring>", "ops": [ ... ]}`. `presentation` can be `"active"`.

| Op | What it does | Key fields |
|---|---|---|
| `profile` | Read a slide: every object's role, format, capacity | `slide` |
| `edit_text_preserve` | Change text, keep existing format (supports `**bold**`) | `slide`, `shape`, `paragraphs` (plain strings) |
| `write_textbox` | Write text with formatting you specify (supports `**bold**`) | `slide`, `shape`, `paragraphs` (objects: text/bold/size/color/italic/font/align) |
| `write_table` | Edit a table; preserves each cell's formatting by default | `slide`, `shape`, `rows`, optional `table_opts` |
| `build` | Make a new slide from a layout | `layout`, `fields`, optional `position` |
| `build_chart` | Make a new slide with a live think-cell chart | `layout` (a `chart_*` one), `fields` (incl. `chart` data), optional `position` |
| `refresh_chart` | Update a named chart's data in place (own job; works on local/OneDrive/SharePoint) | `chart_name`, `type`, `data` |

`shape` is the 1-based index from `profile` / `ppt_list_shapes` (or the shape's name).

---

## The core rule: always write through deck_writer.py

**Never use `ppt_set_text`, `ppt_set_placeholder_text`, or `ppt_find_replace_text` to change slide content. Always use `deck_writer.py` (`edit_text_preserve`, `write_textbox`, `write_table`, `build`, or `build_chart`).** No exceptions, no judgment call about whether a shape "looks simple."

Why: the `ppt_*` write tools flatten a shape's formatting into a single style. A slide with a bold navy header over normal black bullets comes out with header and bullets looking identical, and there's no clean undo. `deck_writer.py` writes the careful way — it captures each line's formatting first, inserts the new text, then re-applies the formatting line by line — so headers stay headers and bullets stay bullets. That is the entire reason the tool exists.

The `ppt_*` tools are for *reading* (preview, profile, get_text, list_shapes) only.

## Gotchas worth remembering

- **Preview discipline.** Each preview image lands in context as base64 and adds up fast. Trust the overflow check and tool read-back for mechanical edits; reserve previews for overflow warnings, visually complex layouts, and final per-slide sign-off.
- **`ppt_find_replace_text` strips whitespace** from the search text, so ` - ` matches hyphens inside words. Inspect per-shape instead of blind find/replace.
- **Airtable headshots:** download with PowerShell (`Invoke-WebRequest`), not Python/curl (TLS error), and use the `thumbnails.full.url` link. `place_image` already does this.
- **Process-flow arrows** are the "Chevron" shape (type 52), not "Pentagon".
- **Overflow = warn, never shrink.** Fixed sizes are a brand standard. Shorten or split. `build`, `write_textbox`, and `edit_text_preserve` measure the actual rendered text height against the box after writing and return a precise warning when it overflows; the text is still written. (Falls back to a character-budget estimate only if the box can't be measured.)
- **Inline emphasis on a rewrite:** `edit_text_preserve` keeps each line's *paragraph* format but doesn't carry a bold phrase over from the old text automatically. Mark it in the new text with `**…**` (e.g. `"**Label:** rest"`) and the tool bolds just that span. (Colored mid-line phrases still need a `ppt_format_text_range` pass.)
- **Always re-check after writing** — re-preview the slide and read the tool's output.

---

## If deck_writer.py fails

If the tool returns a non-zero exit code, malformed JSON, or a read-back that doesn't match what you intended:
1. Read the full stdout — it usually names the problem (shape not found, wrong slide, file locked, bad JSON).
2. Common fixes: wrong shape index (re-profile); presentation name mismatch (check `ppt_list_presentations`); file open read-only (save and reopen writable); JSON syntax error in the job (validate before retrying).
3. If the slide is in a broken state, undo with Ctrl+Z in PowerPoint before retrying.
4. Fix the issue before retrying — don't re-run the same job unchanged.
