#!/usr/bin/env python3
"""Build the reconciled-transcript Word document.

Usage:
  python3 build_transcript_docx.py payload.json --out "Transcript.docx"
  python3 build_transcript_docx.py --schema      # print the payload schema

Inline [CONFLICT n] tokens in turn text are highlighted automatically and
cross-referenced to the appendix. Requires python-docx (pip install python-docx
--break-system-packages).
"""

import argparse
import json
import os
import re
import sys

SCHEMA = r"""
payload.json
------------
{
  "title": "Interview Transcript — Dana Whitfield, Acme Materials",

  "meta": {                          // rendered as a provenance table; order preserved
    "Interview":          "Dana Whitfield, VP Operations, Acme Materials",
    "Project":            "Calyxo Growth Strategy (CLXO02)",
    "Date of call":       "2026-07-21",
    "Interviewer(s)":     "Andrew Gartley (Newry)",
    "Participants":       "Dana Whitfield (Acme Materials); Andrew Gartley (Newry)",
    "Sources reconciled": "Otter (58:12, 214 turns); Granola (55:40, 96 turns)",
    "Timing anchor":      "Otter — timestamps correspond to otter-recording.mp3",
    "Verbatim standard":  "Clean verbatim (filler and false starts removed)",
    "Prepared":           "2026-07-28 by Claude, reviewed by Andrew Gartley"
  },

  "notes": [                         // optional caveats shown under the header
    "Speakers 2 and 3 are both from Acme and may be conflated between 22:00-24:30."
  ],

  "turns": [
    {
      "time": "00:00",               // approximate, from the timing anchor
      "speaker": "Andrew Gartley (Newry)",
      "text": "Thanks for making time. Can you walk me through [CONFLICT 1]?"
    }
  ],

  "conflicts": [
    {
      "id": 1,
      "time": "00:14",
      "context": "Andrew asking about the qualification process.",
      "variants": [
        {"source": "Otter",   "text": "the quality cycle"},
        {"source": "Granola", "text": "the qual cycle"}
      ],
      "issue": "Unclear whether the speaker said 'quality' or 'qual'.",
      "best_guess": "the qual cycle",
      "confidence": "medium",        // low | medium | high
      "status": "open"               // open | reviewed-unresolved | resolved
                                     // 'resolved' items should be applied to the
                                     // turn text and dropped from this list
    }
  ]
}

Only "turns" is strictly required. Everything else is optional but recommended —
the meta table is what makes the document defensible six months later.
"""


def die(msg):
    sys.exit(f"error: {msg}")


try:
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor, Inches
except ImportError:  # pragma: no cover
    die("python-docx is not installed. Run:\n"
        "  pip install python-docx --break-system-packages")

CONFLICT_TOKEN = re.compile(r"\[CONFLICT\s+(\d+)\]")

GREY = RGBColor(0x59, 0x59, 0x59)
RED = RGBColor(0xB3, 0x1B, 0x1B)
ACCENT = RGBColor(0x1F, 0x3B, 0x63)

CONF_ORDER = {"low": 0, "medium": 1, "high": 2}


def highlight(run):
    """Yellow highlight, applied via raw XML so it works on any python-docx build."""
    rpr = run._element.get_or_add_rPr()
    shd = OxmlElement("w:highlight")
    shd.set(qn("w:val"), "yellow")
    rpr.append(shd)


def set_cell_shading(cell, hex_fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_fill)
    tc_pr.append(shd)


def add_page_numbers(section):
    """Footer: 'Page N of M'."""
    para = section.footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.add_run("Page ").font.size = Pt(8)

    def field(instr):
        run = para.add_run()
        run.font.size = Pt(8)
        begin = OxmlElement("w:fldChar")
        begin.set(qn("w:fldCharType"), "begin")
        instr_el = OxmlElement("w:instrText")
        instr_el.set(qn("xml:space"), "preserve")
        instr_el.text = instr
        end = OxmlElement("w:fldChar")
        end.set(qn("w:fldCharType"), "end")
        run._element.append(begin)
        run._element.append(instr_el)
        run._element.append(end)

    field("PAGE")
    para.add_run(" of ").font.size = Pt(8)
    field("NUMPAGES")


def write_turn_text(para, text, conflict_ids):
    """Write turn body, highlighting [CONFLICT n] tokens and [inaudible] markers."""
    pos = 0
    for match in CONFLICT_TOKEN.finditer(text):
        if match.start() > pos:
            para.add_run(text[pos:match.start()])
        cid = int(match.group(1))
        conflict_ids.add(cid)
        run = para.add_run(f"[CONFLICT {cid}]")
        run.bold = True
        run.font.color.rgb = RED
        highlight(run)
        pos = match.end()
    remainder = text[pos:]
    # Highlight [inaudible ...] markers too — they are gaps a reader should notice.
    for piece in re.split(r"(\[inaudible[^\]]*\])", remainder, flags=re.I):
        if not piece:
            continue
        run = para.add_run(piece)
        if piece.lower().startswith("[inaudible"):
            run.italic = True
            run.font.color.rgb = GREY


def build(payload, out_path):
    turns = payload.get("turns")
    if not turns:
        die("payload has no 'turns'")

    doc = Document()

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    style.paragraph_format.space_after = Pt(0)

    section = doc.sections[0]
    section.left_margin = section.right_margin = Inches(1.0)
    add_page_numbers(section)

    # ---- title
    title = payload.get("title") or "Reconciled Interview Transcript"
    heading = doc.add_paragraph()
    run = heading.add_run(title)
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = ACCENT
    heading.paragraph_format.space_after = Pt(10)

    # ---- provenance table
    meta = payload.get("meta") or {}
    if meta:
        table = doc.add_table(rows=0, cols=2)
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.LEFT
        for key, value in meta.items():
            cells = table.add_row().cells
            cells[0].width = Inches(1.6)
            cells[1].width = Inches(4.9)
            krun = cells[0].paragraphs[0].add_run(str(key))
            krun.bold = True
            krun.font.size = Pt(9)
            set_cell_shading(cells[0], "F2F2F2")
            vrun = cells[1].paragraphs[0].add_run(str(value))
            vrun.font.size = Pt(9)
        doc.add_paragraph()

    # ---- notes / caveats
    notes = payload.get("notes") or []
    if notes:
        para = doc.add_paragraph()
        run = para.add_run("Notes on this transcript")
        run.bold = True
        run.font.size = Pt(10)
        for note in notes:
            npara = doc.add_paragraph(style="List Bullet")
            nrun = npara.add_run(str(note))
            nrun.font.size = Pt(9)
            nrun.font.color.rgb = GREY
        doc.add_paragraph()

    conflicts = payload.get("conflicts") or []
    open_conflicts = [c for c in conflicts
                      if str(c.get("status", "open")).lower() != "resolved"]
    if open_conflicts:
        para = doc.add_paragraph()
        run = para.add_run(
            f"{len(open_conflicts)} unresolved passage"
            f"{'s' if len(open_conflicts) != 1 else ''} "
            f"marked [CONFLICT n] below — see the appendix."
        )
        run.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = RED
        doc.add_paragraph()

    # ---- transcript
    thead = doc.add_paragraph()
    trun = thead.add_run("Transcript")
    trun.bold = True
    trun.font.size = Pt(13)
    trun.font.color.rgb = ACCENT
    thead.paragraph_format.space_after = Pt(8)

    referenced = set()
    last_speaker = None
    for turn in turns:
        speaker = (turn.get("speaker") or "Unidentified speaker").strip()
        time = (turn.get("time") or "").strip()
        text = turn.get("text") or ""
        if not text.strip():
            continue

        para = doc.add_paragraph()
        para.paragraph_format.space_before = Pt(8 if speaker != last_speaker else 4)
        para.paragraph_format.space_after = Pt(0)

        if time:
            trun = para.add_run(f"[{time}] ")
            trun.font.size = Pt(9)
            trun.font.color.rgb = GREY
        srun = para.add_run(f"{speaker}: ")
        srun.bold = True
        write_turn_text(para, text, referenced)
        last_speaker = speaker

    # ---- appendix
    if open_conflicts:
        doc.add_page_break()
        ahead = doc.add_paragraph()
        arun = ahead.add_run("Appendix — Unresolved Conflicts")
        arun.bold = True
        arun.font.size = Pt(13)
        arun.font.color.rgb = ACCENT

        intro = doc.add_paragraph()
        irun = intro.add_run(
            "Each row corresponds to a highlighted [CONFLICT n] marker in the "
            "transcript. Sources disagreed and the difference could not be "
            "resolved with confidence from project context. Timestamps refer to "
            "the timing anchor named above."
        )
        irun.font.size = Pt(9)
        irun.font.color.rgb = GREY
        intro.paragraph_format.space_after = Pt(10)

        table = doc.add_table(rows=1, cols=5)
        table.style = "Table Grid"
        widths = [Inches(0.4), Inches(0.6), Inches(1.7), Inches(2.4), Inches(1.4)]
        headers = ["#", "Time", "Context", "What each source said", "Assessment"]
        for idx, text in enumerate(headers):
            cell = table.rows[0].cells[idx]
            cell.width = widths[idx]
            run = cell.paragraphs[0].add_run(text)
            run.bold = True
            run.font.size = Pt(9)
            set_cell_shading(cell, "E8EDF5")

        ordered = sorted(
            open_conflicts,
            key=lambda c: (CONF_ORDER.get(str(c.get("confidence", "low")).lower(), 0),
                           c.get("time") or "",
                           c.get("id") or 0),
        )
        for conflict in ordered:
            cells = table.add_row().cells
            for idx in range(5):
                cells[idx].width = widths[idx]

            cid = conflict.get("id", "?")
            cells[0].paragraphs[0].add_run(str(cid)).font.size = Pt(9)
            cells[1].paragraphs[0].add_run(str(conflict.get("time", ""))).font.size = Pt(9)
            cells[2].paragraphs[0].add_run(str(conflict.get("context", ""))).font.size = Pt(9)

            vcell = cells[3]
            first = True
            for variant in conflict.get("variants") or []:
                para = vcell.paragraphs[0] if first else vcell.add_paragraph()
                first = False
                srun = para.add_run(f"{variant.get('source', '?')}: ")
                srun.bold = True
                srun.font.size = Pt(9)
                trun = para.add_run(f"“{variant.get('text', '')}”")
                trun.font.size = Pt(9)

            acell = cells[4]
            issue = conflict.get("issue")
            para = acell.paragraphs[0]
            if issue:
                run = para.add_run(str(issue))
                run.font.size = Pt(9)
                para = acell.add_paragraph()
            guess = conflict.get("best_guess")
            if guess:
                grun = para.add_run("Best guess: ")
                grun.bold = True
                grun.font.size = Pt(9)
                para.add_run(f"“{guess}”").font.size = Pt(9)
                para = acell.add_paragraph()
            conf = conflict.get("confidence")
            if conf:
                crun = para.add_run(f"Confidence: {conf}")
                crun.font.size = Pt(9)
                crun.font.color.rgb = GREY
            status = str(conflict.get("status", "open")).lower()
            if status == "reviewed-unresolved":
                para = acell.add_paragraph()
                srun = para.add_run("Reviewed and left unresolved.")
                srun.italic = True
                srun.font.size = Pt(9)
                srun.font.color.rgb = GREY

    # ---- second appendix: decisions taken by majority, without a human
    settled = payload.get("settled_by_vote") or []
    if settled:
        doc.add_page_break()
        shead = doc.add_paragraph()
        srun = shead.add_run("Appendix — Figures, Names and Negations Settled by Majority")
        srun.bold = True
        srun.font.size = Pt(13)
        srun.font.color.rgb = ACCENT

        intro = doc.add_paragraph()
        irun = intro.add_run(
            "These spans were decided by a majority of independent sources and "
            "were not flagged, which is the intended rule. They are listed here "
            "because they are the categories worth spot-checking against the "
            "recording: a figure, a name, or a negation that a majority got wrong "
            "would otherwise pass unseen. Nothing here is known to be in doubt."
        )
        irun.font.size = Pt(9)
        irun.font.color.rgb = GREY
        intro.paragraph_format.space_after = Pt(10)

        stable = doc.add_table(rows=1, cols=5)
        stable.style = "Table Grid"
        swidths = [Inches(0.6), Inches(0.8), Inches(1.6), Inches(2.5), Inches(0.6)]
        sheaders = ["Time", "Type", "Used", "What each source said", "Vote"]
        for idx, text in enumerate(sheaders):
            cell = stable.rows[0].cells[idx]
            cell.width = swidths[idx]
            run = cell.paragraphs[0].add_run(text)
            run.bold = True
            run.font.size = Pt(9)
            set_cell_shading(cell, "E8EDF5")

        for item in sorted(settled, key=lambda s: (s.get("time") or "")):
            cells = stable.add_row().cells
            for idx in range(5):
                cells[idx].width = swidths[idx]
            cells[0].paragraphs[0].add_run(str(item.get("time", ""))).font.size = Pt(9)
            cells[1].paragraphs[0].add_run(str(item.get("category", ""))).font.size = Pt(9)
            cells[2].paragraphs[0].add_run(
                f"“{item.get('resolution', '')}”").font.size = Pt(9)
            vcell, first = cells[3], True
            for variant in item.get("variants") or []:
                para = vcell.paragraphs[0] if first else vcell.add_paragraph()
                first = False
                vrun = para.add_run(f"{variant.get('source', '?')}: ")
                vrun.bold = True
                vrun.font.size = Pt(9)
                para.add_run(f"“{variant.get('text', '')}”").font.size = Pt(9)
            cells[4].paragraphs[0].add_run(str(item.get("margin", ""))).font.size = Pt(9)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    doc.save(out_path)

    # ---- consistency warnings: markers and appendix rows must correspond
    declared = {c.get("id") for c in open_conflicts}
    warnings = []
    for cid in sorted(referenced - declared):
        warnings.append(f"[CONFLICT {cid}] appears in the transcript but has no "
                        f"open appendix entry")
    for cid in sorted(declared - referenced):
        warnings.append(f"conflict {cid} is listed in the appendix but no "
                        f"[CONFLICT {cid}] marker appears in the transcript")
    resolved_still_marked = {
        c.get("id") for c in conflicts
        if str(c.get("status", "open")).lower() == "resolved"
    } & referenced
    for cid in sorted(resolved_still_marked):
        warnings.append(f"conflict {cid} is marked resolved but [CONFLICT {cid}] "
                        f"is still in the transcript text")

    words = sum(len((t.get("text") or "").split()) for t in turns)
    speakers = sorted({(t.get("speaker") or "").strip() for t in turns if t.get("speaker")})
    print(f"wrote {out_path}")
    print(f"  turns:            {len(turns)}")
    print(f"  words:            {words}")
    print(f"  speakers ({len(speakers)}):    {', '.join(speakers) or 'none'}")
    print(f"  open conflicts:   {len(open_conflicts)}")
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
        print("  Fix these before sending the document to anyone.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("payload", nargs="?", help="path to payload.json")
    ap.add_argument("--out", help="output .docx path")
    ap.add_argument("--schema", action="store_true", help="print the payload schema and exit")
    args = ap.parse_args()

    if args.schema:
        print(SCHEMA)
        return
    if not args.payload:
        die("payload.json is required (or pass --schema)")
    if not args.out:
        die("--out is required")

    with open(args.payload, "r", encoding="utf-8") as fh:
        try:
            payload = json.load(fh)
        except json.JSONDecodeError as exc:
            die(f"payload.json is not valid JSON: {exc}")

    build(payload, args.out)


if __name__ == "__main__":
    main()
