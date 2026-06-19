# Deck Builder Skill

Build and edit PowerPoint slides using the Newry template via live PowerPoint control (ppt-mcp COM server).

## Triggers

"build slides", "create a deck", "make a slide", "add a slide", "draft slides", "update the deck", "ppt"

## Prerequisites

- PowerPoint must be open with the target file
- ppt-mcp must be configured in `~/.claude.json` and loaded in this session
- Confirm with `ppt_get_presentation_info` before any writes

---

## Intake modes

There are two intake modes. Claude identifies which applies based on what the user provides.

### Working file
Most decks will be Newry-branded whether or not they started from the blank template. The same brand standards (fonts, colors, sizing) apply everywhere. The only difference is structural familiarity:

- **Blank Newry template** — shape structure is known; use the source slide table directly.
- **Real Newry deck in progress** — shapes vary slide to slide; inspect the target slides first (`ppt_list_shapes`, `ppt_get_text`) before writing anything, then apply the same brand standards.

There is no separate "edit mode." Adding slides, editing content, fixing formatting, and deleting slides are all in scope for any open Newry deck. When the target file isn't the blank template, inspect before touching — otherwise proceed normally.

- **Non-Newry decks** (client decks, partner decks, other brands) are also supported. In these cases the Newry source slide table and brand standards don't apply — inspect the deck first to understand its structure and style, then follow whatever conventions are already in use.

---

## Intake — Mode 1: CLI request ("build me a slide about X")

### Template
Default to the Newry template. Check if it's already open first:
```
ppt_list_presentations()
```
If the Newry template is open, activate it. If not, open it from the default path:
```
C:\Users\sshank\OneDrive - Newry Corp\Desktop\Newry non-project and backup\AI Tool Building\reference\Newry Powerpoint Template 2024 (1).pptx
```
Look for clues in the request that the user wants a different file (e.g., they mention a client name, a specific deck, or a file path). If it's clearly a different file, ask which one before proceeding.

### Research vs. provided context
Only ask if the request doesn't make it clear. If the user says "build a slide on germanium supply chain" with no context, ask: "Do you want me to research this, or do you have content to provide?" If they paste text or attach a file alongside the request, skip the question — they've provided context.

### Layout selection
Pick confidently from the source slide table and state the choice: "I'm going to use the process flow layout — let me know if you'd prefer something else." Only ask explicitly if the request is genuinely ambiguous between two layouts (e.g., could be a body slide or a comparison table).

### Title
Draft one — don't ask. The title should reflect the actual content, not a placeholder. User can revise.

### Write behavior
Write directly, then surface the preview. Visual review IS the approval step. If Claude invented specific facts (numbers, company names, dates), flag them explicitly after writing: "I generated these numbers — verify before using."

## Intake — Mode 2: Content → Slides

Triggered when the user provides source material — paste, file, or a connected source — and wants slides built from it.

### Input sources

| Source | How to access |
|---|---|
| Pasted text | Direct from chat |
| File on disk (PDF, Word, txt) | `Read` tool with file path |
| SharePoint | SharePoint MCP connector |
| Outlook email | Outlook MCP connector |
| Slack | Slack MCP connector |
| Otter (meeting transcripts) | Otter MCP connector |

For connected sources: search automatically based on context clues in the request (meeting → Otter, email → Outlook, doc → SharePoint). Report what you found before proceeding — "Found a Corning kickoff transcript from June 12 in Otter — using that. Let me know if that's the wrong one." Only ask if search returns nothing or results are ambiguous.

### Assess input quality first

Before synthesizing, assess what the user brought:

- **Already structured** (outline, bullets, synthesized findings) → skip to plan, map content to layouts, build. No synthesis step needed.
- **Lightly unstructured** (a few interview transcripts, a contained secondary data set, short research notes) → synthesize inline, then go through the three-stage flow below.
- **Too raw or too large** (big document dumps, many unstructured transcripts, unsynthesized research) → stop and redirect with guidance:
  - If the material is **primary research** (interview transcripts, call notes): "Do a synthesis pass first using the PRT in Cowork, then bring the output back here."
  - For everything else: "This needs a synthesis pass before going to slides. Recommended steps: (1) identify the 3–5 key themes or findings; (2) for each theme, pull 2–3 supporting points; (3) decide which findings belong on slides vs. appendix — not everything needs to be there; (4) structure into a simple outline (theme → bullets) and bring that back. A clean outline is all this skill needs to build from."
  - Do not attempt to synthesize large dumps in this skill.

Note: slides are the output of thinking, not the place where thinking happens. Pre-synthesis is the norm; the lightly-unstructured path is the exception.

### Three-stage flow (for lightly unstructured or structured input)

**Stage 1 — Lightweight plan**
Show slide-by-slide structure before writing anything:
```
Slide 1 — "Germanium Supply Chain Overview" — body slide — 4 key findings
Slide 2 — "Mine to Market" — process flow — 4 stages
Slide 3 — "Processing Capacity" — chart slide — annotations only
```
User approves structure and layout choices. Redirect if wrong layout or wrong number of slides.

**Stage 2 — Text content review**
Show full bullet content for each slide inline. User approves or edits before anything goes on slides. This prevents a long fix cycle after building.

**Stage 3 — Build**
Write confirmed content to slides. Preview after each batch.

### Batching
If the plan is more than ~4 slides, ask before building: "This is X slides — want me to build in batches of 3–4 so we can review as we go, or all at once?"

## Intake — Mode 3: Style Reference Deck

Triggered when the user says something like "match the style of this deck" or "make it look like X" alongside a build request.

1. Open and activate the reference deck.
2. `ppt_get_presentation_info` — note fonts, dimensions, theme colors.
3. `ppt_get_all_text(slide_index=None)` — read all content to understand tone and structure.
4. `ppt_list_shapes` on 2–3 representative slides — note typical shape positions, sizes, naming patterns.
5. Switch back to the target deck and apply extracted conventions. Report what you extracted: "Using Calibri/18pt body, #2F5496 header color, no sub-header TextBox pattern."

If the reference deck is the Newry template, skip this mode — Mode 1/2 already applies Newry standards.

---

## Core Procedure

### 1. Activate
```
ppt_activate_presentation(file_path=<path>)
```
Locks all subsequent tool calls to that file. Always call this first.

### 2. Pick a source slide

Use `duplicate_slide`, never `add_slide`. Duplicate carries all custom shapes, decorative elements, master formatting, and theme colors. `add_slide` with `like_slide_index` copies the layout only — all custom shapes are lost.

| Content type | Source slide |
|---|---|
| Cover page | 1 |
| Table of contents | 2 |
| Document best practices / dense bullets | 3 |
| Chapter divider | 4 |
| Background & Objectives | 5 |
| Interview list | 6 |
| Body slide (bullets + quote) | 7 |
| Chart / market sizing | 8 |
| Process flow / value chain | 9 |
| Timeline | 10 |
| Qualitative 4-column comparison | 11 |
| Comparison table (gradient) | 12 |
| 3-panel text / definitions / glossary | 22 |
| Usage rules (continued) | 23 |
| Sourcing & citations | 24 |

### 3. Duplicate and position

```
ppt_duplicate_slide(slide_index=SOURCE)   # copy goes immediately after SOURCE
```

No `ppt_move_slide` needed when you want the copy right after its source. The tool inserts the copy at `SOURCE+1`, not at the end.

**Index tracking when inserting in sequence** — if inserting copies right after each original (first to last), the Nth original is always at position `2N−1` and its copy automatically lands at `2N`. No move required.

### 3b. Delete a shape

```
ppt_delete_shape(slide_index=TARGET, shape_index=N)
```
Use `shape_index` (integer). `shape_name_or_index` is not a valid parameter and throws a validation error.

### 4. List shapes before writing

For any slide with more than a title and simple body:
```
ppt_list_shapes(slide_index=TARGET)
```
Complex slides (process flow, timeline, comparison table) have TextBoxes with the same name — you must use shape index, not name. Identify all text-bearing shapes before writing.

### 5. Write content

#### Headlines state the finding, not the topic
Slide titles should answer "so what" — not just name the subject. Write "Industrial Segment Is Growing 8% Annually" not "Industrial Segment." Draft titles this way by default. Keep titles under ~70 characters for standard layouts; longer titles wrap to a second line and overlap the section label.

#### Bullet spacing
The Newry template has correct bullet spacing built in. Duplicating from the source slide preserves it. Do not manually set paragraph spacing on bullet content — template defaults are correct. If bullet spacing looks wrong after writing, it is a formatting collapse symptom (see Repair Procedures), not a spacing issue.

#### Title / subtitle / simple labels
```
ppt_set_text(shape_name_or_index="Title 1", text="...")
```
Safe for any shape with uniform formatting (single run). Preserves existing style.

#### Body placeholders (Placeholder type shapes)
Prefer `ppt_set_text` by shape name over `ppt_set_placeholder_text`. The placeholder tool strips paragraph-level bullet XML when writing.

If you must use `ppt_set_placeholder_text`, run the **Placeholder Bullet Repair** sequence immediately after (see Repairs).

#### Mixed-format TextBoxes (header + bulleted body in same shape)
`ppt_set_text` collapses all new paragraphs into one run, inheriting the first character's formatting (bold navy). Always run **Mixed-Format TextBox Repair** after writing to any TextBox that originally had a header paragraph followed by body paragraphs.

#### Tables
```
ppt_get_table_data(slide_index, shape_name_or_index)   # inspect first
ppt_set_table_data(slide_index, shape_name_or_index, data=[...])
```
If the new data has more rows than the table: call `ppt_add_table_row` first. Extra rows passed without pre-adding are silently dropped.

After writing table data, call `ppt_set_bullet(bullet_type='none')` on all table cells — tables inherit bullet formatting from the master that doesn't belong.

**Known limitation**: `ppt_set_table_data` strips paragraph-level formatting (bullets, indentation, alignment) from cells that had mixed-format content. All cell text reverts to bold/centered regardless of what you write. There is no fix — do not attempt to restore bullet formatting inside table cells.

For individual cell formatting:
```
ppt_set_table_cell(slide_index, shape, row=1, col=2, text="...", bold=true, color="#1E4C7F")
ppt_merge_table_cells(slide_index, shape, start_row=1, start_col=1, end_row=1, end_col=3)
ppt_set_table_borders(slide_index, shape, border_color="#CCCCCC", border_width=0.5)
ppt_set_table_style(slide_index, shape, style_index=N)
```

#### Formatting multiple shapes at once
```
ppt_batch_apply_formatting(slide_index, shape_indices=[1,2,3], fill_color="#1E4C7F", font_color="#FFFFFF", font_size=14)
```
Preferred over looping individual calls when styling multiple shapes consistently. Supports fill, line, shadow, and text formatting in one call. Use whenever more than one shape needs the same formatting applied.

#### Multi-shape layout consistency (value chain / end market / parallel box layouts)
When writing text into multiple parallel shapes of the same type (e.g., all boxes in a value chain or end market map), all shapes must have the same font size. Never shrink one or two boxes to fit their content while leaving others larger — that inconsistency reads immediately. If a shape's content is too long, **shorten the text** to fit the common size; do not change the font size for that shape alone. After writing, call `ppt_get_text` on all parallel shapes and verify the font size is identical across all of them.

Also check for a key or legend shape: if the slide has color-coded categories (e.g., "customer-facing", "internal"), there is almost certainly a key somewhere on the slide. Find it with `ppt_list_shapes`, update it, and do not leave it blank or remove it. If you cannot find the key and the slide has multiple colors, ask.

### 6. Review (MANDATORY before previewing)

```
ppt_get_text(slide_index=TARGET, shape_name_or_index=N)
```

For every written shape, check:
- **Run count vs paragraph count**: if `paragraph_count > 1` and `runs` has only 1 item → formatting collapsed → run Mixed-Format Repair
- **Per-run bold / color / font_size**: compare against source slide values
  - Title: 28pt, bold or normal (layout-dependent), white or navy
  - Section header (H2): ~16pt bold, #1E4C7F navy
  - Body text: 14–18pt, not bold, #000000 black — **use 16pt (not 20pt) on dense-bullet layouts** (body+quote slide, B&O slide) to avoid overflowing the tombstone/source box at the bottom
  - Caption / footnote: 12pt, not bold, #7F7F7F gray
- **Content overflow**: after previewing, check that no text is clipped by the text box boundary. If the last bullet is cut off, either shorten the content or drop body font size (20pt → 16pt). Do not call the task done if text is visibly cut off.
- **Dashes**: en dash ( – ) with a space on each side for ranges and asides ("$2M – $5M", "strong – but not dominant"). Em dash (—) without spaces only for sentence interruption in pull quotes. Scan what you wrote and fix any straight hyphens used as dashes.

`ppt_get_slide_preview` is for human visual confirmation only. It is NOT a substitute for the programmatic check. Run both.

### 7. Save

```
ppt_save_presentation()
```
Call after every write session. ppt-mcp does not auto-save. If PowerPoint closes mid-session, all changes since the last save are lost.

### QC Pass 1 — Style and consistency sweep

Run after writing all content on a slide or batch.

**En dash sweep — do NOT use `ppt_find_replace_text` for ` - ` → ` – `.** The tool strips leading/trailing whitespace from `find_text`, so it receives just `"-"` and matches every compound-word hyphen in the deck (e.g., "high-quality", "mid-sized") — destructive. Instead:

1. `ppt_get_all_text(slide_index=None)` — scan output for ` - ` patterns with surrounding context
2. Identify true candidates: ranges and asides only (e.g., "$2M - $5M", "strong - but not dominant"), not compound adjectives
3. Fix per-shape: use `ppt_set_text` for a full shape replacement, or `ppt_find_replace_text` with a longer unique phrase that won't match unintended shapes

Mechanical fix that IS safe via `ppt_find_replace_text`:

| Issue | Find | Replace |
|---|---|---|
| Double space | `  ` | ` ` |

Also check:
- Every slide title states a finding, not just a topic label. Fix any that don't.
- Numbers and statistics you generated are flagged explicitly: "I generated this figure — verify before presenting."

### QC Pass 2 — Writing standards sweep

Check all written content against the Writing Standards section:
- En dashes used correctly (not hyphens for ranges/attributions; no em dashes)
- Numbers under 10 written out unless with a unit
- No final punctuation on bullets
- Oxford comma present in lists
- Acronyms spelled out on first use (except FDA, USA, IBM-class common ones)
- Footnote format is `N – source` not `N. source` or `(N) source`
- Unit abbreviations are B/M/k not bn/mm/K

### QC Pass 3 — Claims vs. source of fact

A reasoning pass, not mechanical. For each substantive assertion:
- Is there a traceable source (interview, report, data file) behind it?
- Assertions without a traceable source should be softened or flagged for removal.
- Run before any deck goes to client review. Flag issues in the conversation — do not silently leave unsupported claims.

---

## Additional Tools

### Read all content from a deck before writing

On any real deck (not the blank template), call this before touching anything:
```
ppt_get_all_text(slide_index=None)      # all slides
ppt_get_all_text(slide_index=N)         # single slide
```
Returns all text as pseudo-Markdown with layout and heading analysis. Use this to understand the existing content and structure before making changes.

### Bulk text replacement
```
ppt_find_replace_text(find="Q1 2024", replace="Q2 2025")
```
Replaces text across all slides in one call. Use for updating dates, company names, placeholder labels, or any repeated string. Case-sensitive by default.

### Copy a shape to another slide
```
ppt_copy_shape_to_slide(source_slide=SOURCE, shape_name_or_index=N, target_slide=TARGET)
```
Copies a specific shape (logo, label, decorative element) from one slide to another at the same position. Use instead of duplicating the whole slide when only one element needs to transfer.

### Align and distribute shapes
```
ppt_align_shapes(slide_index, shape_indices=[1,2,3], align="left")
ppt_distribute_shapes(slide_index, shape_indices=[1,2,3], direction="horizontal")
```
Use after adding multiple new shapes. `align` values: `left`, `right`, `top`, `bottom`, `center`, `middle`. `direction`: `horizontal`, `vertical`.

### Shape fill and copied formatting
```
ppt_set_fill(slide_index, shape_name_or_index, fill_type="solid", color="#1E4C7F")
ppt_copy_formatting(source_slide, source_shape, target_slide, target_shape)
```
`ppt_set_fill` sets fill color directly on a shape. `ppt_copy_formatting` copies all formatting (fill, line, font, shadow) from one shape to another — use when a new shape must match an existing one exactly.

### Paragraph spacing
```
ppt_set_paragraph_format(slide_index, shape, paragraph_index=N, space_before=6, space_after=6, line_spacing=1.0)
```
Controls space before/after paragraphs and line spacing. Try this before dropping font size to resolve tight or overflowing layouts.

### Slide management
```
ppt_delete_slide(slide_index=N)
ppt_move_slide(slide_index=N, target_index=M)
```
Indices shift after each deletion — delete from last to first to avoid drift. `ppt_move_slide` renumbers slides accordingly.

### Export a single shape
```
ppt_export_shape(slide_index, shape_name_or_index, output_path="C:/temp/shape.png")
```
Exports a shape as an image. Use when `ppt_get_slide_preview` is too small to read a specific element, or to extract a logo from the deck.

### Export full deck to PDF
```
ppt_export_pdf(output_path="C:/temp/deck.pdf")
```
Exports the active presentation to PDF. Use for final delivery or for sharing without a PowerPoint license.

### Typography audit
```
ppt_check_typography(slide_index=None)
```
Scans the deck for font inconsistencies (wrong typefaces, missing brand fonts, mixed sizes). Run before delivery on any deck that had significant editing.

---

## Repair Procedures

### Mixed-Format TextBox Repair

**When**: `ppt_get_text` returns single run, paragraph_count > 1.

**Steps**:
1. Map paragraphs → identify header paragraphs (ALL-CAPS text) vs body paragraphs
2. Calculate char start positions by summing paragraph text lengths (each `\r` counts as 1 char)
3. For each header paragraph: `ppt_format_text_range(start, length, bold=true, font_size=16, color="#1E4C7F")`
4. For each body group: `ppt_format_text_range(start, length, bold=false, font_size=14, color="#000000")`
5. `ppt_set_bullet(bullet_type='unnumbered')` — all paragraphs
6. `ppt_set_bullet(bullet_type='none', paragraph_index=N)` — for each header and blank paragraph

For a TextBox with two headers (e.g., the right panel on slide 22), you need separate `ppt_format_text_range` calls for each section: body1 range, header2 range, body2 range.

### Critical: `ppt_format_text` scopes to the whole shape, not a paragraph

`ppt_format_text(paragraph_index=N, italic=true)` applies the formatting to the **entire text frame**, overwriting all paragraphs — not just paragraph N. Do not use it when different paragraphs need different italic/bold values.

**Always use `ppt_format_text_range`** for per-paragraph or per-run formatting. It correctly scopes to the character range and supports `italic` as a parameter:

```
ppt_format_text_range(slide_index, shape, start=1, length=19, bold=true, font_size=20, color="#1E4C7F", italic=false)
ppt_format_text_range(slide_index, shape, start=20, length=11, bold=false, font_size=18, color="#000000", italic=true)
```

### Placeholder Bullet Repair

**When**: used `ppt_set_placeholder_text` on a body placeholder.

**Steps**:
1. `ppt_get_text` → find body text start position (after header paragraph, char = header_length + 1)
2. `ppt_format_text_range(start=body_start, length=body_length, bold=false, font_size=18, color="#000000")`
3. `ppt_set_bullet(bullet_type='unnumbered')` — all
4. `ppt_set_bullet(bullet_type='none', paragraph_index=1)` — remove from header

---

## Layout-Specific Notes

### Cover slide (slide 1)

Three editable text shapes in the lower half of the slide:
- **Title** ("Newry Communications"): left=30.48, top=347.44, width=637.09, height=55.1 — 40pt Aptos, not bold, #000000
- **Subtitle**: left=30.48, top=415.93, width=637.09, height=44.33 — 24pt Aptos, not bold, #000000
- **Date**: left=30.48, top=487.7, width=267.02, height=24.23 — 18pt Aptos, not bold, #000000

The navy wave background is part of the slide master — it cannot be added or modified via ppt-mcp.

### TOC slide (slide 2)

- Title is white (#FFFFFF, 28pt Aptos Display) — the dark navy header band comes from the master layout
- Table starts at left=381.77, top=136.47, width=548.23

### Chapter divider (slide 4)

- Single text shape ("Subtitle 1"): left=30, top=350.77, width=900, height=72.75 — 28pt Aptos, not bold, #000000
- No slide number on chapter dividers
- Navy wave background covers the upper ~75% of the slide; lower ~25% is white — both from the master

### Background & Objectives slide (slide 5)

Two-column layout with independent header + body in each column:
- Left header: left=30.69, top=87.18, width=431.57, height=24.14
- Left body: left=30.69, top=117.84, width=431.57, height=383.39
- Right header: left=496.19, top=87.51, width=432, height=23.81
- Right body: left=496.71, top=117.84, width=431.48, height=383.39
- Column gap: ~34pt
- Column headers are H2 style (18–20pt bold ALL-CAPS #1E4C7F); body is 18pt regular #000000

### Body slide layout (slide 7) — exact positions

- Title: left=30, top=6.93, width=898.88, height=66.92
- Bullet area (Text Placeholder 2): left=29.74, top=98.29, width=518.95, height=235.23
- Quote box 1 (Rectangle 7): left=556.14, top=98.29, width=372.74, height=136.29
- Quote box 2 (Rectangle 8): left=556.14, top=251.97, width=372.74, height=136.29
- Tombstone (Rectangle 9): left=27, top=413.1, width=901.88, height=50.35, fill=#BBD4EF
- Source/footnote (Text Placeholder 4): left=29.74, top=493.29, width=861.89, height=36.66

### Team page — updating bios and photos

Only consultant shapes need to change per client. VP shapes stay the same. Inspect first to identify which shapes belong to which person.

**Bio and expertise source**: Airtable Staff table (base `appRawPuacfAvVH2Z`, table `tblAeAug2APoy0Jgf`):
- `Expertise` field (`fldg5gPZRs1xMf4sQ`) — short expertise description; starting point for the bio
- `Stakeholder Profiles` field (`fldSrLZaOtgbSPA3H`) — client-facing profile text; use this if populated
- `Job Title` field (`fldtoROc5cJ5nRIh8`) — current title

The bio in a proposal is tailored to the client engagement. Pull the Airtable text as the base, then adapt it to be relevant to the client's industry and the project scope. Show the adapted bio to the user before writing.

**Photo source**: `Image` field (`fldcS1qHM81M2G0yj`) — attachment object. **Use `thumbnails.full.url`, NOT the top-level `url`.** The top-level attachment URL requires an Airtable auth header and fails with a connection reset error (WinError 10054) when passed to `ppt_add_picture_from_url`. `thumbnails.full.url` is a pre-signed URL that works without auth:
```
ppt_add_picture_from_url(slide_index, url=<record["fields"]["Image"][0]["thumbnails"]["full"]["url"]>, left=X, top=Y, width=W, height=H)
```
Replace the existing photo shape by deleting it first (`ppt_delete_shape`), then placing the new image at the same position. Inspect the original shape position with `ppt_get_shape_info` before deleting.

**Headshot size**: 72 × 72pt, circular crop. When adding a new photo, use width=72, height=72 and match the left/top of the shape being replaced.

### Body Slide 1 (slide 7) — bullets + quote

Two regions: left bullets and right quote block. The quote TextBox and attribution TextBox are separate shapes. Use `ppt_list_shapes` to identify them.

Quote attribution (the line below the pull quote) should be italic and right-aligned:
```
ppt_format_text_range(slide_index, attribution_shape, start=0, length=len(attribution_text), italic=true)
ppt_set_paragraph_format(slide_index, attribution_shape, paragraph_index=0, alignment="right")
```

### Process Flow (slide 9)

Has a "TITLE" sub-header TextBox separate from the slide title (shape index ~5, named "Text Placeholder 3"). Must update by index. Each process stage has its own TextBox — use `ppt_list_shapes` to map all stages before writing.

Sub-header TextBox is narrow (281pt wide) and single-line — keep text to ~20 chars or fewer to avoid overflow. "VALUE CHAIN" fits; "CRITICAL MINERAL VALUE CHAIN" (29 chars) wraps and overlaps the chevrons.

Supporting point TextBoxes (below each stage) are uniform-format body-only content — no Mixed-Format collapse. `ppt_get_text` will show a single run spanning all paragraphs; this is correct when all paragraphs share the same style.

**Sub-bullet dash character**: The template uses dashes (–) for level-2 bullets, but fresh duplicates default to round dots (•). After setting indent_level=2, fix the character with:
```
ppt_set_bullet(slide_index, shape, bullet_type="unnumbered", paragraph_index=N, bullet_char="–")
```
Use `bullet_char=` (not `char=` — that raises a validation error). Apply to every level-2 paragraph in every supporting-point TextBox.

### Timeline (slide 10)

10 time-point TextBoxes (TextBox 7–16), 3 content Rectangles (Rectangle 27, 28, 30), 3 elbow connectors (do not touch), 10 tick connector lines (do not touch), 1 horizontal timeline line (do not touch). Also has a sub-header TextBox at shape index 6 — must update by index.

Line/tick specs (different from standard dividers):
- Horizontal axis (Straight Connector 5): #7F7F7F, **1.5pt solid** — do not change
- Year tick marks (Straight Connector 17–26): #1E4C7F navy, **4.5pt solid** — do not change
- Content boxes (Rectangle 27, 28, 30): #BBD4EF fill, **#7F7F7F 1pt solid border** — intentional, keep
- Content box text: 16pt Aptos, regular, #000000, centered
- YEAR label text: 18pt Aptos, regular, #000000, centered

### Chart slide (slide 8) — think-cell

Think-cell charts render from their own OLE data store, not the native Excel workbook. `ppt_set_chart_data` updates the Excel workbook but the visual does not change. Annotation shapes (year labels, CAGR ovals, segment labels) ARE regular AutoShapes — fully updatable via `ppt_set_text`.

For chart data updates: use the think-cell JSON Data Automation API or the ThinkcellBuilder Python library. Do not attempt chart data updates via ppt-mcp alone.

**Figure title TextBox (shape 3)** — two-paragraph label at top-left of chart area:

| Paragraph | Format |
|---|---|
| 1 — chart title | ALL CAPS, 20pt bold, #1E4C7F navy, italic=false |
| 2 — units | 18pt, bold=false, italic=true, #000000 black |

This shape collapses on write (Mixed-Format). Repair with two `ppt_format_text_range` calls (title range, then units range), passing `italic` explicitly in each call.

The box is narrow (163pt wide). At 20pt bold, any title longer than ~11 chars will overflow the visible area. **Always call `ppt_set_textframe(word_wrap=false)` after writing** — this keeps the title on one line rather than wrapping into the chart area:

```
ppt_set_textframe(slide_index=TARGET, shape_name_or_index=3, word_wrap=false)
```

### Native (non-think-cell) charts
For slides with native PowerPoint charts (no think-cell OLE), full data control is available:
```
ppt_get_chart_data(slide_index, shape_name_or_index)      # inspect series, categories, values
ppt_set_chart_data(slide_index, shape_name_or_index, data={...})
ppt_set_chart_series(slide_index, shape, series_index=N, values=[...])
ppt_change_chart_type(slide_index, shape, chart_type="bar")
ppt_format_chart(slide_index, shape, show_legend=true, show_data_labels=true)
ppt_format_chart_axis(slide_index, shape, axis="value", min=0, max=100, number_format="0%")
```
On non-think-cell decks, use these tools freely. On the Newry template (think-cell), these update the underlying Excel workbook but the visual does not change — use think-cell methods instead (see Think-Cell Integration).

### 3-panel text (slide 22) — same-named TextBoxes

All 3 TextBoxes are named "Text Placeholder 3". Access them by shape index (4, 5, 6 for left-top, left-bottom, right respectively). Always list shapes first to confirm indices.

After writing, run Mixed-Format TextBox Repair on all 3. The right panel (index 6) often has two headers — both need separate repair passes.

### Breakout process pages (NBD proposal)

Used in proposals to detail each phase of the engagement. Standard layout:
- **Chevron row across the top** — one shape per phase; the current module is full-color, all others are greyed out
- **Bullets on the left** — activities or steps for this phase
- **Right panel** — either a text box with deliverable descriptions or an image of deliverable examples

**Chevron shape type**: Use `shape_type="Chevron"` (resolves to type 52 — indented left side, pointed right) when adding process flow arrows with `ppt_add_shape`. Do NOT use `"Pentagon"` — that creates a regular 5-sided polygon (type 12), not a directional arrow.

To grey out inactive chevron shapes:
```
ppt_set_fill(slide_index, shape_name_or_index, fill_type="solid", color="#D9D9D9")
```
Apply to every chevron except the active one. Confirm the active chevron index with `ppt_list_shapes` first — do not grey the wrong one.

Use the cross-slide content propagation workflow (see Workflows) when populating a set of breakout pages from a single summary process slide.

### Brand reference slides (14, 15)

Newry Palette and Newry Logos are style guide artifacts. Do not use as content slide templates. Picture shapes on the Logos slide cannot be swapped without source image files.

---

## Known Limitations

### Think-cell chart data is not updatable via ppt-mcp
`ppt_set_chart_data` and `ppt_set_chart_series` update the underlying Excel workbook, but think-cell renders from its own OLE data store — the visual does not change. To update chart data on think-cell slides, use the think-cell JSON Automation API, the COM API, or ThinkcellBuilder. Non-think-cell slides (native PowerPoint charts) are fully updatable via ppt-mcp.

### Logo and image carryover is a manual step
ppt-mcp cannot swap a logo or replace an image without source image files on disk. If a slide needs a new logo (client deck → Newry branded, or vice versa), that swap must be done manually in PowerPoint. Document this explicitly when handing off a deck.

---

## Think-Cell Integration

Three paths (all deferred until chart automation is prioritized):
1. **JSON Data Automation** — pre-tag think-cell charts with data IDs, POST JSON to `api.think-cell.com`
2. **COM API** — direct COM object access from a Python script
3. **ThinkcellBuilder** — `pip install thinkcellbuilder` (PyPI)

Current approach: consultants update think-cell charts manually; ppt-mcp handles all surrounding text, annotations, and non-chart elements.

---

## Workflows

### Cross-slide content propagation

**When**: user asks to spread content from one summary slide across multiple detail slides (e.g., "fill in slides 7–10 based on slide 6").

1. `ppt_get_all_text(slide_index=SOURCE)` — read the source slide in full
2. Map content to target slides: show a plan before writing anything
   ```
   Slide 7 — Kickoff (bullet 1 from Module 1)
   Slide 8 — Discovery (bullets 2–3 from Module 1)
   Slide 9 — Analysis (Module 2)
   Slide 10 — Recommendations (Module 3)
   ```
3. User approves the mapping. Adjust if wrong.
4. Write each target slide, then `ppt_get_slide_preview` after each batch.
5. On breakout process pages: grey out inactive chevrons (see Breakout process pages in Layout-Specific Notes) and verify the active chevron matches the slide's phase.

Do not invent content beyond what is in the source slide. If the source is sparse, flag it: "Slide 6 only has 2 bullets for Module 2 — I'll need more content for slide 9 or I can leave it as a placeholder."

---

## Shape Defaults (from-scratch builds)

When building a slide from scratch — adding new shapes rather than duplicating template slides — every shape must be checked against these specs before saving. This is the most common source of formatting failures on new slides.

### Canvas
- Slide: 960 × 540 pt
- Left/right margin: 30pt from each edge (safe content width ≈ 900pt)
- Content area top: ~92–98pt (below title)
- Content area bottom: ~493pt (above source box)

### Typography

| Element | Font | Size | Style | Color |
|---|---|---|---|---|
| Slide title | Aptos Display | 28pt | not bold | #000000 (white on dark backgrounds) |
| Cover title | Aptos | 40pt | not bold | #000000 |
| Cover subtitle | Aptos | 24pt | not bold | #000000 |
| Cover date | Aptos | 18pt | not bold | #000000 |
| Section sub-header (H2) | Aptos | 20pt | bold, ALL-CAPS | #1E4C7F |
| Section sub-header (H2) — dense layouts | Aptos | 18pt | bold, ALL-CAPS | #1E4C7F |
| Column / section header (H3) | Aptos | 16pt | bold, Title Case | #000000 |
| Body text | Aptos | 18pt | regular | #000000 |
| Body text range | Aptos | 14–20pt | — | — |
| Table text | Aptos | 16pt | regular | #000000 |
| Table minimum | Aptos | 12pt | — | — |
| Chart units line | Aptos | 18pt | italic | #000000 |
| Source / citation box (footer band) | Aptos | 12pt | regular | #FFFFFF (white — sits on dark navy footer) |
| Source / citation (in content area) | Aptos | 12pt | regular | #7F7F7F |
| Team page — VP name | Aptos | 16pt | bold | #000000 |
| Team page — title / email | Aptos | 16pt | regular | #000000 |
| Line spacing | — | 6–12pt between lines | — | — |

### Shape fills and borders

Two valid fill patterns — use nothing else:
- **Light**: #BBD4EF fill + #000000 black text (preferred for content boxes, tombstones, chevrons)
- **Dark**: #1E4C7F fill + #FFFFFF white text (for headers, active phase chevrons)

Rules that apply to every shape:
- **No borders**: `line: visible=false` — borders are off on all template shapes
- **No shadows**: explicitly prohibited ("Avoid 3D gradients or drop shadows")
- **Square corners only**: no rounded rectangles
- **Quote boxes**: #D9D9D9 fill, no border; quote left-aligned; attribution right-aligned italic
- **Tombstone** (full-width callout bar): #BBD4EF fill, no border, width ≈ 902pt, left = 27–30pt

Exceptions (shapes that legitimately have borders or different fills):
- **CAGR / annotation ovals** on chart slides: white (#FFFFFF) fill, black border 0.75pt solid, 18pt bold #000000 centered — these are annotation shapes, not content shapes
- **Timeline content boxes**: #BBD4EF fill, #7F7F7F border 1pt solid — the border is intentional to define the event box
- **Gradient comparison table legend swatches**: High=#89B4E3, Medium=#BBD4EF, Low=#C6DBF2

### Divider lines
- Color: #7F7F7F
- Weight: 1pt
- Dash style: long segmented dash (dash_style=7 in ppt-mcp)
- **Timeline horizontal axis line is different**: #7F7F7F, **1.5pt solid** (dash_style=1)
- **Timeline tick marks are different**: #1E4C7F navy, **4.5pt solid**

### Value chain chevrons
- First shape: `Pentagon` (flat left edge, pointed right); subsequent: `Chevron`
- Arrow depth adjustment: 0.5
- Default size: 239pt wide × 66.5pt tall; last shape widens to 246.46pt to reach right margin
- Left shift between shapes: 217.84pt → **overlap = ~21.3pt** — do not gap them
- Default fill: #BBD4EF; active/highlighted phase: #1E4C7F; inactive/greyed: #D9D9D9
- No border, no shadow

### Tables

| Element | Spec |
|---|---|
| Font | Aptos, 16pt, #000000 |
| Header row fill | #D9D9D9 (light grey), bold |
| Body row fill | #FFFFFF white, not bold |
| Alignment | Left, top |
| Borders | No colored borders |

### Pre-save checklist for from-scratch slides

Before calling `ppt_save_presentation` on any slide built from scratch:
1. Every shape: `line: visible=false` (no borders) — except CAGR ovals and timeline content boxes
2. Every shape: no shadow set
3. Fill colors are only from the two approved patterns or the special cases above
4. Fonts are Aptos Display (title only) or Aptos (everything else) — not Arial, Calibri, or system defaults
5. Body text is 18pt (not 14pt or 20pt unless dense layout requires it)
6. Source box present at bottom if any data/claims are on the slide
7. Source text in footer band = white (#FFFFFF); source text embedded in content area = #7F7F7F
8. Run `ppt_get_slide_preview` and visually confirm before reporting done

---

## Writing Standards

Apply these rules to all content written to slides. Flag violations found during QC passes.

### Units and numbers

- Abbreviations: **B** = billion, **M** = million, **k** = thousand (e.g., $100B, 200M units, 50k)
- In chart unit lines: spell out — "Thousands of USD", "Millions of USD" (not $k or $M)
- Measurements: `45 kg`, `5 ft³`, `27 ft²` — not "cu ft", "sq ft", "sq m"
- Write out numbers under 10 unless: paired with a unit of measure; a comparable number >10 appears in the same sentence; space is genuinely tight on the slide
- Use tilde (~) for approximations only when the uncertainty is meaningful — not for precise figures

### Punctuation

- **No final punctuation on bullets** — periods only in quotes and tombstones written as full sentences
- Periods and commas go **inside** quote marks; all other punctuation goes outside
- Oxford (serial) comma required: "polymers, fiber, and glass"
- Put commas before and after *e.g.,* and *i.e.,* — they mean "for example" and "that is"
- **Dashes**: use hyphens ( - ) only for word splits (long-term); use **en dashes** ( – ) for ranges, parentheticals, and quote attributions; **no em dashes** ( — )
- Spaces on both sides of en dashes and slashes — except in units (e.g., w/m²)

### Capitalization

- Major words in: axis labels, row/column labels, unit lines, document titles
- Proper nouns: people, places, organizations
- Capitalize job titles of specific people ("Senior Manager Irving Scott") but not generic roles ("he's the regional manager")
- Spell out acronyms on first use — but not common ones (FDA, USA, IBM)

### Footnotes and sources

Footnote format: `N – [source]` — number, space, en dash, space, source text, semicolon before next
```
1 – Frost & Sullivan, North American Biofuels Market, 2007; 2 – Based on interview with Josh Butzbaugh, Energy Star
```
Order sources top-to-bottom then left-to-right on the page. General page sources go under "Source:" after footnotes.

**Citation formats by source type:**

| Type | Format |
|---|---|
| Research report | Issuing Org, *Report Title in Italics*, Date |
| Periodical article | Author, "Title in Quotes," *Periodical in Italics*, Date |
| Book | Author, *Title in Italics*, Publisher, Year |
| Web article | Org or Author, "Title in Quotes," Date, URL |
| Website (data cited) | Company Name Website (specific data point cited) |
| Interview | Based on interview with Name and/or Title, Organization |

Use superscript numbers for footnotes. If the slide has many unit superscripts (ft², m²) that conflict, switch to symbols: *, †, ‡, §, ¶, #

### Subscripts / superscripts

- Chemical formulas: O₂, CO₂, H₂O — subscript the numbers, not superscript
- Exponents in units: ft², m³ — superscript

---

## Brand Reference

| Element | Value |
|---|---|
| Title font | Aptos Display |
| Body font | Aptos |
| Primary navy (hero / headers) | #1E4C7F |
| Dark navy (darkest) | #0F263F |
| Bright blue | #3079CA |
| Second lightest blue (fills) | #BBD4EF |
| Red (highlights only) | #920D29 |
| Gold (highlights only) | #FDBC0D |
| Grey 2 (quotes, table headers) | #D9D9D9 |
| Grey 5 (dividers, source text) | #7F7F7F |
| Body text | #000000 black |
| Caption / source text | #7F7F7F gray |
| Section header font size | 16pt bold |
| Body text font size | 18pt normal (14–20pt range) |
