# SoF Toolkit — V1 PPTX Feature Design

## What V1 adds

When a user uploads a `.pptx` file (single slide or full deck), the tool:

1. Finds the SoF slide (scan for "SUMMARY OF FINDINGS" or similar labels)
2. Duplicates the SoF slide and inserts the duplicate immediately after the original
3. On the **duplicate slide only**:
   - Rewrites the headline and bullets with the recommended improvements
   - Changed text is rendered in **red**; unchanged text stays black
   - Comment boxes are added to explain the reasoning behind each change
4. Returns the modified `.pptx` file — original slide intact, revised slide directly after it for easy comparison

## Comment box placement

- Comment boxes float **partially off the right edge of the slide** so they don't overlap the slide content
- Each comment box is anchored to the element it's commenting on (headline comment near the title box, bullet comments beside the content area)
- Brief on the slide — a sentence or two per comment. Detailed reasoning can still appear in chat.
- Style: light yellow or light blue fill, small font (~10pt), thin border

## Input modes (both supported)

| Input | Output |
|-------|--------|
| Pasted text or screenshot | Commentary + suggested rewrites in chat only |
| `.pptx` file | Commentary in chat + modified `.pptx` with duplicate annotated slide |

## Implementation notes

- Use the pptx skill workflow: unpack → find SoF slide XML → duplicate via `add_slide.py` → edit duplicate XML → clean → pack
- Red text: set `<a:solidFill><a:srgbClr val="FF0000"/>` on changed `<a:r>` runs
- Comment boxes: add `<p:sp>` text box shapes with explicit position/size — x offset beyond slide width (e.g., slide width + 0.25") so they hang off the right edge
- Finding changed vs. unchanged runs: diff original text against revised text at the run level; only color runs where content changed
- SoF slide detection: scan `markitdown` output for slide containing "SUMMARY OF FINDINGS", "SUMMARY OF FINDING", "KEY FINDINGS", or similar; fall back to asking user if ambiguous

## What's already built (V0 — current state)

- `SKILL.md` — Evaluate, Draft, Consistency modes
- `references/universal-standards.md` — Pyramid Principle standards
- `references/update-type-guidance.md` — 4 update types
- Text/image input path fully functional
- Test cases in `SoF Skill Test Cases.md`
- 2 eval runs in `SoF Skill Eval Run 1.md`

## Pending before V1

- Complete V0 testing: Glass Core evaluate test (known-good reference), Thin Triple draft test
- Iterate skill based on test results
- Build and test PPTX annotation script
