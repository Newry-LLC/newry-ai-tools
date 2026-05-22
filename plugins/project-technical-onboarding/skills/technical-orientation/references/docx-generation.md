# Docx Generation

Use docx-js to generate the Technical Orientation document. Write the full Node.js generation script from scratch using the helpers and setup below, then run it.

---

## Setup

```bash
npm install -g docx
```

---

## How to generate

Write a Node.js script at `/tmp/generate-tech-orientation.js`. The script has two parts:

1. **Boilerplate** — page setup, colors, helpers, header/footer. Copy this exactly.
2. **Document body** — write this yourself from the interview content, following the structure guidance in `references/artifact-structure.md`.

Run the script, then save the output to the project Claude working folder.

---

## Part 1 — Boilerplate (copy exactly)

```javascript
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, LevelFormat
} = require('docx');
const fs = require('fs');

// ── Page constants ────────────────────────────────────────────────────────────
const PAGE_WIDTH_DXA  = 12240;
const PAGE_HEIGHT_DXA = 15840;
const MARGIN_DXA      = 1440;
const CONTENT_WIDTH_DXA = PAGE_WIDTH_DXA - (MARGIN_DXA * 2); // 9360

// ── Colors ────────────────────────────────────────────────────────────────────
const COLORS = {
  black:      '000000',
  darkGray:   '404040',
  midGray:    '666666',
  lightGray:  'F2F2F2',
  borderGray: 'CCCCCC',
  accent:     '1F497D',
};

// ── Helpers ───────────────────────────────────────────────────────────────────

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 120 },
    children: [new TextRun({ text, bold: true, size: 28, font: 'Arial', color: COLORS.accent })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 80 },
    children: [new TextRun({ text, bold: true, size: 24, font: 'Arial', color: COLORS.darkGray })]
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 60 },
    children: [new TextRun({ text, bold: true, size: 22, font: 'Arial', color: COLORS.darkGray })]
  });
}

function body(text) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    children: [new TextRun({ text, size: 22, font: 'Arial', color: COLORS.black })]
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: 'bullets', level },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, size: 22, font: 'Arial', color: COLORS.black })]
  });
}

function spacer() {
  return new Paragraph({ spacing: { before: 60, after: 60 }, children: [new TextRun('')] });
}

function divider() {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.borderGray, space: 1 } },
    spacing: { before: 160, after: 160 },
    children: [new TextRun('')]
  });
}

// ── Table helpers ─────────────────────────────────────────────────────────────
const cellBorder = { style: BorderStyle.SINGLE, size: 1, color: COLORS.borderGray };
const allBorders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };

function tableCell(text, { width = 2340, bold = false, shade = false } = {}) {
  return new TableCell({
    borders: allBorders,
    width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: COLORS.lightGray, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({
      children: [new TextRun({ text, size: 20, font: 'Arial', bold, color: COLORS.black })]
    })]
  });
}

function buildTable(headers, rows, colWidths) {
  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) => tableCell(h, { width: colWidths[i], bold: true, shade: true }))
  });
  const dataRows = rows.map(row =>
    new TableRow({ children: row.map((cell, i) => tableCell(cell, { width: colWidths[i] })) })
  );
  return new Table({
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, ...dataRows]
  });
}
```

---

## Part 2 — Document body (write from scratch)

Build the document body using the helpers above. Follow the structure and content guidance in `references/artifact-structure.md`. Exercise full judgment on:

- **Sub-section depth** — use `heading2` and `heading3` wherever they help the reader navigate. Don't limit yourself to one heading level per section.
- **Prose vs. bullets** — use `body()` for narrative and analysis; use `bullet()` for enumerable items (specs, competitor attributes, distinct customer segments, open questions). Default to bullets where a list genuinely exists; default to prose where you're explaining or analyzing.
- **Section depth** — add sub-sections where the content warrants it. The artifact-structure spec defines the minimum; exceed it where the content is richer.

The title block, header, footer, and document config are fixed — write these exactly:

```javascript
const CLIENT      = '[Client name from interview]';
const PROJECT_CODE = '[Project code from interview]';
const CONSULTANT  = '[Consultant name]';
const DATE        = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

const doc = new Document({
  numbering: {
    config: [{
      reference: 'bullets',
      levels: [
        { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } } },
      ]
    }]
  },
  styles: {
    default: { document: { run: { font: 'Arial', size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 28, bold: true, font: 'Arial', color: COLORS.accent },
        paragraph: { spacing: { before: 360, after: 120 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 24, bold: true, font: 'Arial', color: COLORS.darkGray },
        paragraph: { spacing: { before: 280, after: 80 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 22, bold: true, font: 'Arial', color: COLORS.darkGray },
        paragraph: { spacing: { before: 200, after: 60 }, outlineLevel: 2 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_WIDTH_DXA, height: PAGE_HEIGHT_DXA },
        margin: { top: MARGIN_DXA, right: MARGIN_DXA, bottom: MARGIN_DXA, left: MARGIN_DXA }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.borderGray, space: 4 } },
          children: [
            new TextRun({ text: `${CLIENT} Technical Orientation`, size: 18, font: 'Arial', color: COLORS.midGray }),
            new TextRun({ text: `  |  ${PROJECT_CODE}`, size: 18, font: 'Arial', color: COLORS.midGray }),
          ]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: COLORS.borderGray, space: 4 } },
          children: [
            new TextRun({ text: `Draft — ${DATE}`, size: 16, font: 'Arial', color: COLORS.midGray }),
            new TextRun({ text: '   Page ', size: 16, font: 'Arial', color: COLORS.midGray }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, font: 'Arial', color: COLORS.midGray }),
          ]
        })]
      })
    },
    children: [
      // Title block — keep this structure
      new Paragraph({ spacing: { before: 0, after: 80 },
        children: [new TextRun({ text: 'Technical Orientation', bold: true, size: 40, font: 'Arial', color: COLORS.accent })] }),
      new Paragraph({ spacing: { before: 0, after: 40 },
        children: [new TextRun({ text: `${CLIENT}  —  ${PROJECT_CODE}`, size: 26, font: 'Arial', color: COLORS.darkGray })] }),
      new Paragraph({ spacing: { before: 0, after: 40 },
        children: [new TextRun({ text: `Prepared by: ${CONSULTANT}`, size: 20, font: 'Arial', color: COLORS.midGray })] }),
      new Paragraph({ spacing: { before: 0, after: 40 },
        children: [new TextRun({ text: `Date: ${DATE}`, size: 20, font: 'Arial', color: COLORS.midGray })] }),
      new Paragraph({ spacing: { before: 0, after: 200 },
        children: [new TextRun({ text: 'Status: Initial Draft (Week 1) — living document', size: 20, font: 'Arial', color: COLORS.midGray, italics: true })] }),
      divider(),

      // ── YOUR CONTENT GOES HERE ─────────────────────────────────────────────
      // Write the five sections using heading1/heading2/heading3/body/bullet/buildTable/spacer/divider
      // Follow artifact-structure.md for section requirements
      // Exercise full judgment on depth, sub-sections, and prose vs. bullets

    ]
  }]
});

// ── Write file ────────────────────────────────────────────────────────────────
const filename = `${CLIENT.replace(/\s+/g, '_')}_Technical_Orientation_${PROJECT_CODE}.docx`;
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(`/tmp/${filename}`, buffer);
  console.log(`Written: /tmp/${filename}`);
}).catch(err => { console.error(err); process.exit(1); });
```

---

## Running the script

```bash
node /tmp/generate-tech-orientation.js
```

Then save to the project Claude working folder:
`~\Newry Corp\[Project SharePoint path]\Claude Working Folder - [Project Code]\`

---

## Validation

Use the `docx` skill to validate the output. Refer to the docx skill for editing guidance if validation fails.

---

## Key rules

- Always set page size explicitly (US Letter: 12240 × 15840 DXA)
- Never use unicode bullets — use `LevelFormat.BULLET` with numbering config
- Always use `WidthType.DXA` on tables — never `WidthType.PERCENTAGE`
- Tables need dual widths: `columnWidths` array AND each cell `width` — both must match and sum to `CONTENT_WIDTH_DXA` (9360)
- Use `ShadingType.CLEAR` for table shading — never `ShadingType.SOLID`
- `PageBreak` must be inside a `Paragraph`
- `heading3` is available and should be used — don't flatten everything to two heading levels
