#!/usr/bin/env python3
"""Normalize a transcript from any common format into uniform JSONL turns.

Output: one JSON object per line:
  {"source": "Otter", "start_sec": 42.0, "start": "00:42",
   "speaker": "Dana Whitfield", "text": "..."}

Auto-detects WebVTT, SRT, Teams/Word .docx, PDF exports, Otter-style text
exports, JSON (Otter/Granola API shapes), and plain "Speaker: text" transcripts.

Usage:
  python3 normalize_transcript.py FILE --source-name Otter --out normalized/otter.jsonl
  python3 normalize_transcript.py FILE --source-name Otter --stats
  cat transcript.txt | python3 normalize_transcript.py - --source-name Notes --format speaker_text
"""

import argparse
import json
import os
import re
import sys
import zipfile

# ---------------------------------------------------------------- time helpers

TS_RE = re.compile(
    r"(?:(?P<h>\d{1,2})[:.])?(?P<m>\d{1,2})[:.](?P<s>\d{1,2})(?:[.,](?P<ms>\d{1,3}))?"
)


def parse_ts(text):
    """Parse a timestamp string to seconds. Returns None if unparseable."""
    if text is None:
        return None
    m = TS_RE.search(str(text))
    if not m:
        return None
    h = int(m.group("h") or 0)
    mi = int(m.group("m"))
    s = int(m.group("s"))
    ms = int((m.group("ms") or "0").ljust(3, "0"))
    return h * 3600 + mi * 60 + s + ms / 1000.0


def fmt_ts(sec, force_hours=False):
    if sec is None:
        return ""
    sec = max(0, int(round(sec)))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    if h or force_hours:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


# ------------------------------------------------------------------ text utils

# "Dana Whitfield:", "SPEAKER 1:", "Dr. Ruiz (Acme):", "Andrew G. -"
SPEAKER_LINE = re.compile(
    r"^\s*(?P<speaker>(?:[A-Z][\w.'\-]*(?:\s+[A-Z][\w.'\-]*){0,4})"
    r"|(?:SPEAKER\s*\d+)|(?:Speaker\s*\d+)|(?:[A-Z]{2,}(?:\s+[A-Z]{2,})?))"
    r"\s*(?:\((?P<affil>[^)]{1,40})\))?\s*[:\-–]\s+(?P<text>.*)$"
)

INLINE_TS = re.compile(r"[\[\(]?\b\d{1,2}:\d{2}(?::\d{2})?\b[\]\)]?")

# Teams / Otter document exports put the attribution on its own line, with no
# colon: "Dana Whitfield<tab>0:10" (or "0:10 Dana Whitfield"), text following.
_TS_BARE = r"\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?"
SPEAKER_HEADER_TRAILING = re.compile(
    rf"^\s*(?P<speaker>[A-Z][^\t:]{{0,58}}?)[\t ]+[\[\(]?(?P<ts>{_TS_BARE})[\]\)]?\s*$"
)
SPEAKER_HEADER_LEADING = re.compile(
    rf"^\s*[\[\(]?(?P<ts>{_TS_BARE})[\]\)]?[\t ]+(?P<speaker>[A-Z][^\t:]{{0,58}}?)\s*$"
)


def match_speaker_header(line):
    """Match a bare 'Name  0:10' / '0:10  Name' attribution line.

    Returns (speaker, seconds) or None. Guarded so ordinary sentences that
    happen to end in a time don't get mistaken for attribution lines.
    """
    for pattern in (SPEAKER_HEADER_TRAILING, SPEAKER_HEADER_LEADING):
        m = pattern.match(line)
        if not m:
            continue
        speaker = m.group("speaker").strip(" -–—\t")
        if not speaker or len(speaker.split()) > 5:
            continue
        if speaker[-1] in ".!?,;":
            continue
        return speaker, parse_ts(m.group("ts"))
    return None


def clean(text):
    text = re.sub(r"\s+", " ", text or "")
    return text.strip()


def strip_leading_ts(text):
    """Remove a timestamp sitting at the front of a line; return (ts, rest)."""
    m = re.match(r"^\s*[\[\(]?\s*(\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?)\s*[\]\)]?\s*(.*)$", text)
    if m:
        return parse_ts(m.group(1)), m.group(2)
    return None, text


# -------------------------------------------------------------------- reading

def read_docx(path):
    """Extract paragraph text from a .docx without external deps."""
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n == "word/document.xml"]
        if not names:
            raise ValueError("not a Word document (no word/document.xml)")
        xml = z.read(names[0]).decode("utf-8", "replace")
    # Split on paragraph boundaries, then strip tags inside each paragraph.
    paras = re.split(r"</w:p>", xml)
    out = []
    for p in paras:
        p = re.sub(r"<w:tab[^>]*/>", "\t", p)
        p = re.sub(r"<w:br[^>]*/>", "\n", p)
        texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, flags=re.S)
        line = "".join(texts)
        line = (line.replace("&amp;", "&").replace("&lt;", "<")
                    .replace("&gt;", ">").replace("&quot;", '"')
                    .replace("&apos;", "'"))
        out.append(line.strip())
    return "\n".join(out)


def _strip_pdf_furniture(text):
    """Drop page-break artifacts and repeated page headers/footers.

    Transcript PDFs put the same header on every page ("Acme Interview -
    Confidential", "Page 3 of 14"). Left in, those lines land mid-sentence and
    look like speech. A line that recurs on most pages and is short is furniture.
    """
    pages = text.split("\f")
    if len(pages) > 2:
        counts = {}
        for page in pages:
            for line in {l.strip() for l in page.split("\n") if l.strip()}:
                counts[line] = counts.get(line, 0) + 1
        threshold = max(2, int(len(pages) * 0.6))
        furniture = {
            line for line, count in counts.items()
            if count >= threshold and len(line) < 90
        }
    else:
        furniture = set()

    kept = []
    for line in text.replace("\f", "\n").split("\n"):
        stripped = line.strip()
        if stripped in furniture:
            continue
        if re.fullmatch(r"(?:page\s*)?\d{1,4}(?:\s*(?:of|/)\s*\d{1,4})?", stripped, re.I):
            continue
        kept.append(line)
    return "\n".join(kept)


def read_pdf(path):
    """Extract text from a PDF, trying the best available tool in turn."""
    errors = []

    # pdftotext (poppler) preserves reading order well and is fastest.
    try:
        import subprocess
        result = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", path, "-"],
            capture_output=True, timeout=180,
        )
        if result.returncode == 0 and result.stdout.strip():
            return _strip_pdf_furniture(result.stdout.decode("utf-8", "replace"))
        errors.append(f"pdftotext: {result.stderr.decode('utf-8', 'replace')[:200]}")
    except FileNotFoundError:
        errors.append("pdftotext: not installed")
    except Exception as exc:
        errors.append(f"pdftotext: {exc}")

    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
        if any(p.strip() for p in pages):
            return _strip_pdf_furniture("\f".join(pages))
        errors.append("pdfplumber: no extractable text")
    except ImportError:
        errors.append("pdfplumber: not installed")
    except Exception as exc:
        errors.append(f"pdfplumber: {exc}")

    try:
        import pypdf
        reader = pypdf.PdfReader(path)
        pages = [(page.extract_text() or "") for page in reader.pages]
        if any(p.strip() for p in pages):
            return _strip_pdf_furniture("\f".join(pages))
        errors.append("pypdf: no extractable text")
    except ImportError:
        errors.append("pypdf: not installed")
    except Exception as exc:
        errors.append(f"pypdf: {exc}")

    raise ValueError(
        "could not extract text from this PDF.\n  " + "\n  ".join(errors) +
        "\nIf the PDF has no text layer it is a scan — it needs OCR first "
        "(see the 'pdf' skill), or read it directly and normalize by hand."
    )


def read_input(path):
    if path == "-":
        return sys.stdin.read(), "-"
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return read_docx(path), ext
    if ext == ".pdf":
        return read_pdf(path), ext
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read(), ext


# -------------------------------------------------------------------- detection

def detect_format(raw, ext):
    head = raw.lstrip()[:2000]
    if ext == ".json" or head[:1] in "[{":
        try:
            json.loads(raw)
            return "json"
        except Exception:
            pass
    if head.startswith("WEBVTT"):
        return "vtt"
    if re.search(r"^\s*\d+\s*\n\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->", head, re.M):
        return "srt"
    if "-->" in head:
        return "vtt"
    return "speaker_text"


# --------------------------------------------------------------------- parsers

def parse_cue_based(raw, arrow_sep=True):
    """WebVTT / SRT. Returns list of (start_sec, speaker_or_None, text)."""
    blocks = re.split(r"\n\s*\n", raw.replace("\r\n", "\n"))
    turns = []
    for block in blocks:
        lines = [l for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        if lines[0].strip().upper().startswith("WEBVTT"):
            lines = lines[1:]
        if not lines:
            continue
        ts_idx = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if ts_idx is None:
            continue
        start = parse_ts(lines[ts_idx].split("-->")[0])
        body_lines = lines[ts_idx + 1:]
        if not body_lines:
            continue
        speaker = None
        # VTT voice tag: <v Dana Whitfield>text
        vm = re.match(r"\s*<v\s+([^>]+)>(.*)", body_lines[0])
        if vm:
            speaker = clean(vm.group(1))
            body_lines[0] = vm.group(2)
        body = clean(" ".join(body_lines))
        body = re.sub(r"</?[cvbiu][^>]*>", "", body)
        if speaker is None:
            sm = SPEAKER_LINE.match(body)
            if sm:
                speaker = clean(sm.group("speaker"))
                body = clean(sm.group("text"))
        if body:
            turns.append((start, speaker, body))
    return turns


def parse_json(raw):
    data = json.loads(raw)
    # Find the most plausible list of segment dicts anywhere in the structure.
    candidates = []

    def walk(node):
        if isinstance(node, list):
            if node and isinstance(node[0], dict):
                keys = set().union(*(set(d.keys()) for d in node if isinstance(d, dict)))
                score = len(keys & {"text", "transcript", "content", "words",
                                    "speaker", "speaker_name", "speaker_id",
                                    "start", "start_time", "start_ms", "startTime",
                                    "offset", "timestamp"})
                if score >= 2:
                    candidates.append((score, len(node), node))
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)

    walk(data)
    if not candidates:
        raise ValueError("could not find transcript segments in JSON")
    candidates.sort(key=lambda c: (c[0], c[1]), reverse=True)
    segs = candidates[0][2]

    turns = []
    for seg in segs:
        if not isinstance(seg, dict):
            continue
        text = None
        for key in ("text", "transcript", "content", "value", "body"):
            if isinstance(seg.get(key), str) and seg[key].strip():
                text = seg[key]
                break
        if text is None and isinstance(seg.get("words"), list):
            words = [w.get("word") or w.get("text") or "" for w in seg["words"]
                     if isinstance(w, dict)]
            text = " ".join(w for w in words if w)
        if not text or not text.strip():
            continue

        speaker = None
        for key in ("speaker_name", "speaker", "speakerName", "speaker_label",
                    "name", "displayName", "speaker_id"):
            val = seg.get(key)
            if isinstance(val, dict):
                val = val.get("name") or val.get("speaker_name")
            if isinstance(val, (str, int)) and str(val).strip():
                speaker = str(val).strip()
                break

        start = None
        for key in ("start", "start_time", "startTime", "start_sec", "offset",
                    "timestamp", "time"):
            if key in seg and seg[key] is not None:
                val = seg[key]
                if isinstance(val, (int, float)):
                    start = float(val)
                    # Heuristic: very large numbers are ms, not seconds.
                    if start > 100000:
                        start /= 1000.0
                else:
                    start = parse_ts(val)
                break
        if start is None:
            for key in ("start_ms", "startMs", "offset_ms"):
                if isinstance(seg.get(key), (int, float)):
                    start = float(seg[key]) / 1000.0
                    break

        turns.append((start, speaker, clean(text)))
    return turns


def parse_speaker_text(raw):
    """Plain-text transcripts: 'Speaker: text', optional timestamps on their
    own line or leading the speaker line. Also handles no-speaker paragraphs."""
    lines = raw.replace("\r\n", "\n").split("\n")
    turns = []
    pending_ts = None
    cur = None  # [start, speaker, [text parts]]

    def flush():
        nonlocal cur
        if cur and cur[2]:
            body = clean(" ".join(cur[2]))
            if body:
                turns.append((cur[0], cur[1], body))
        cur = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # A line that is only a timestamp applies to whatever follows.
        if re.fullmatch(r"[\[\(]?\s*\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?\s*[\]\)]?", stripped):
            flush()
            pending_ts = parse_ts(stripped)
            continue
        if "-->" in stripped:
            flush()
            pending_ts = parse_ts(stripped.split("-->")[0])
            continue

        # Bare attribution line (Teams / Otter doc exports): starts a new turn
        # whose text lives on the following lines.
        header = match_speaker_header(stripped)
        if header:
            flush()
            speaker, header_ts = header
            pending_ts = None
            cur = [header_ts, speaker, []]
            continue

        lead_ts, rest = strip_leading_ts(stripped)
        m = SPEAKER_LINE.match(rest)
        if m and len(m.group("speaker")) <= 60:
            flush()
            speaker = clean(m.group("speaker"))
            if m.group("affil"):
                speaker = f"{speaker} ({clean(m.group('affil'))})"
            body = m.group("text")
            body_ts, body = strip_leading_ts(body)
            start = lead_ts if lead_ts is not None else (
                body_ts if body_ts is not None else pending_ts)
            pending_ts = None
            cur = [start, speaker, [clean(body)]]
        else:
            if cur is None:
                start = lead_ts if lead_ts is not None else pending_ts
                pending_ts = None
                cur = [start, None, [clean(rest)]]
            else:
                cur[2].append(clean(rest))
    flush()
    return turns


PARSERS = {
    "vtt": lambda raw: parse_cue_based(raw),
    "srt": lambda raw: parse_cue_based(raw),
    "json": parse_json,
    "speaker_text": parse_speaker_text,
}


# ----------------------------------------------------------------- postprocess

# Never merge a turn past this many words. Merging exists to repair cue formats
# that fragment one sentence across several captions, not to build paragraphs.
MERGE_WORD_CAP = 120


def merge_consecutive(turns, gap_limit=None):
    """Merge adjacent turns from the same speaker (cue formats fragment heavily).

    Merging is only safe when the timestamps say the turns are genuinely
    adjacent. An unknown gap is a reason NOT to merge: transcripts without
    timestamps are usually paragraph-per-speaker exports, where merging welds
    separate turns into blobs and — if diarization was already shaky — buries a
    speaker change inside a single turn where nothing downstream can see it.
    """
    merged = []
    for start, speaker, text in turns:
        if merged and speaker is not None and merged[-1][1] == speaker:
            prev_start, prev_speaker, prev_text = merged[-1]
            timing_known = start is not None and prev_start is not None
            close_enough = timing_known and (start - prev_start) <= gap_limit
            within_cap = len((prev_text + " " + text).split()) <= MERGE_WORD_CAP
            if close_enough and within_cap:
                merged[-1] = (prev_start, prev_speaker, clean(prev_text + " " + text))
                continue
        merged.append((start, speaker, text))
    return merged


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="transcript file, or '-' for stdin")
    ap.add_argument("--source-name", required=True,
                    help="label for this source, e.g. Otter, Granola, Teams")
    ap.add_argument("--out", help="output .jsonl path (default: stdout)")
    ap.add_argument("--format", choices=sorted(PARSERS),
                    help="override format auto-detection")
    ap.add_argument("--merge-gap", type=float, default=30.0,
                    help="merge same-speaker turns within this many seconds "
                         "(default 30; use 0 to disable merging)")
    ap.add_argument("--stats", action="store_true",
                    help="print a summary to stderr (duration, turns, speakers)")
    args = ap.parse_args()

    raw, ext = read_input(args.input)
    if not raw.strip():
        sys.exit("error: input is empty")

    fmt = args.format or detect_format(raw, ext)
    try:
        turns = PARSERS[fmt](raw)
    except Exception as exc:
        sys.exit(f"error: failed to parse as {fmt}: {exc}\n"
                 f"Try --format with one of: {', '.join(sorted(PARSERS))}, "
                 f"or normalize this file by hand.")

    if not turns:
        sys.exit(f"error: parsed as {fmt} but found no turns. "
                 f"Try --format, or normalize by hand.")

    if args.merge_gap > 0:
        turns = merge_consecutive(turns, args.merge_gap)

    times = [t for t, _, _ in turns if t is not None]
    force_hours = bool(times) and max(times) >= 3600

    records = []
    for start, speaker, text in turns:
        records.append({
            "source": args.source_name,
            "start_sec": None if start is None else round(start, 2),
            "start": fmt_ts(start, force_hours),
            "speaker": speaker,
            "text": text,
        })

    payload = "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n"
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(payload)
    else:
        sys.stdout.write(payload)

    if args.stats or args.out:
        words = sum(len(r["text"].split()) for r in records)
        speakers = sorted({r["speaker"] for r in records if r["speaker"]})
        unlabeled = sum(1 for r in records if not r["speaker"])
        untimed = sum(1 for r in records if r["start_sec"] is None)
        lines = [
            f"source:        {args.source_name}",
            f"format:        {fmt}" + ("" if args.format else " (auto-detected)"),
            f"turns:         {len(records)}",
            f"words:         {words}",
            f"duration:      {fmt_ts(max(times)) if times else 'unknown'}"
            + (f"  (first turn {fmt_ts(min(times))})" if times else ""),
            f"speakers ({len(speakers)}): {', '.join(speakers) if speakers else 'none labeled'}",
        ]
        if unlabeled:
            lines.append(f"WARNING:       {unlabeled} turn(s) without a speaker label")
        if untimed:
            lines.append(f"WARNING:       {untimed} turn(s) without a timestamp")
        print("\n".join(lines), file=sys.stderr)


if __name__ == "__main__":
    main()
