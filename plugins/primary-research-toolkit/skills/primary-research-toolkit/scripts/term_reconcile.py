#!/usr/bin/env python3
"""
term_reconcile.py — Glossary-based term reconciliation for PRT.

Implements ICS Step 3: applies project glossary fixes to pre-processed
transcripts. Uses a three-state glossary (confirmed corrections,
best-inference corrections, contextual corrections) and an
impact × confidence matrix.

Glossary format (Markdown sections under <project_root>/glossary.md):
- "## Confirmed corrections (auto-apply forever in this project)"
- "## Best-inference corrections (auto-apply, medium confidence — review periodically)"
- "## Contextual corrections (apply only with anchor keyword in same paragraph)"
- "## File-specific corrections" (optional)

Within each section, entries follow:
    - **<canonical>** ← `variant1`, `variant2`, ...
    - **<canonical>** ← `variant3`     (additional line for the same canonical)

Contextual entries:
    - **<canonical>** ← `variant` (anchors: `kw1`, `kw2`)

File-specific scope (two equivalent forms; can also be combined):
    1. H2 parenthetical (preferred when one file is the scope of the section):
           ## File-specific corrections (Olli Piiroinen — phonetic mishearings)
       The leading identifier ("Olli Piiroinen") becomes the default scope
       for all entries before any H3. Token-based filename match: every
       whitespace-separated token >=3 chars must appear in the normalized
       filename (separators collapsed, case-insensitive).
    2. H3 sub-scope (when one section covers multiple files):
           ## File-specific corrections
           ### Olli Piiroinen
           - **Polynt** ← `Poland`
           ### Some Other File
           - **Acme** ← `acne`
       H3 scope overrides any H2 default for entries underneath.

Re-running is safe: text inside "## Term reconciliation" and
"## Decisions made" H2 sections is masked during substitution so prior
fix logs are never re-rewritten.

Working copies of transcripts are updated in place (write to a sibling
`.reconciled.md` if --no-inplace is set). Originals are never touched.
The glossary file is updated with a fresh project-wide totals block.

Usage:
    python term_reconcile.py --input <pre-processed dir> \\
        --glossary <project_root>/glossary.md \\
        [--no-inplace] [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


# =====================================================================
# Glossary parsing
# =====================================================================

@dataclass
class GlossaryEntry:
    canonical: str
    variants: list[str]
    section: str            # "confirmed" | "best-inference" | "contextual" | "file-specific"
    anchors: list[str] = field(default_factory=list)
    file_scope: str = ""    # for file-specific entries


SECTION_HEADER_RE = re.compile(
    r"^##\s+(?P<title>Confirmed corrections|Best-inference corrections|"
    r"Contextual corrections|File-specific corrections)(?P<trailer>.*)$",
    re.MULTILINE,
)

ENTRY_RE = re.compile(
    r"^\s*-\s+\*\*(?P<canonical>[^*]+?)\*\*\s*←\s*(?P<rhs>.+?)\s*$",
    re.MULTILINE,
)

VARIANT_RE = re.compile(r"`([^`]+)`")
ANCHOR_RE = re.compile(r"\(anchors:\s*(.+?)\)")
H2_PARENTHETICAL_RE = re.compile(r"\(([^)]+)\)")


def _extract_h2_scope(trailer: str) -> str:
    """Extract a default file scope from an H2 header trailer.

    The trailer is the text after the section title (e.g.,
    " (Olli Piiroinen — phonetic mishearings)"). We pull the parenthetical,
    then split on em-dash / dash separator and take the leading identifier
    so descriptive tails don't bleed into filename matching.
    """
    m = H2_PARENTHETICAL_RE.search(trailer)
    if not m:
        return ""
    inside = m.group(1).strip()
    # Split on em-dash, en-dash, or " - " (with surrounding whitespace) and
    # keep the leading identifier portion.
    parts = re.split(r"\s+[—–-]+\s+", inside, maxsplit=1)
    return parts[0].strip()


def parse_glossary(text: str) -> list[GlossaryEntry]:
    entries: list[GlossaryEntry] = []
    headers = list(SECTION_HEADER_RE.finditer(text))
    if not headers:
        return entries

    # Determine section ranges
    sections: list[tuple[str, int, int, str]] = []
    for i, h in enumerate(headers):
        title = h.group("title").lower()
        trailer = h.group("trailer") or ""
        if title.startswith("confirmed"):
            tag = "confirmed"
        elif title.startswith("best-inference"):
            tag = "best-inference"
        elif title.startswith("contextual"):
            tag = "contextual"
        else:
            tag = "file-specific"
        start = h.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        sections.append((tag, start, end, trailer))

    for tag, start, end, trailer in sections:
        section_text = text[start:end]

        # File-specific: pick out optional H3 subsections for file scope.
        # Default scope can also be set on the H2 header line as a parenthetical
        # (e.g., "## File-specific corrections (Olli Piiroinen — phonetic mishearings)"):
        # entries before any H3 inherit that scope instead of being treated
        # as project-wide. Per-H3 scopes still override and are unaffected.
        # Stop at the first H3 that looks like a totals/log subsection
        # ("Auto-applied", "Best-inference applied", "Contextual", "File-specific")
        # since those are not file scopes.
        if tag == "file-specific":
            default_scope = _extract_h2_scope(trailer)
            sub_re = re.compile(r"^###\s+(.+?)$", re.MULTILINE)
            non_scope_h3 = re.compile(
                r"^(Auto-applied|Best-inference applied|Contextual|File-specific|Skipped)",
                re.IGNORECASE,
            )
            subs = [m for m in sub_re.finditer(section_text)
                    if not non_scope_h3.match(m.group(1).strip())]
            cut_idx = None
            # Identify earliest H3 to cut on (whether scope or non-scope)
            all_h3 = list(sub_re.finditer(section_text))
            if all_h3:
                cut_idx = all_h3[0].start()

            # Prologue before any H3: inherits H2-level default scope (may be "")
            prologue_end = cut_idx if cut_idx is not None else len(section_text)
            entries.extend(_parse_entries(section_text[:prologue_end], tag, default_scope))

            # Per-scope entries (only true scope H3s, not totals)
            for j, m in enumerate(subs):
                sub_start = m.end()
                # Scope ends at the next H3 of any kind, or end of section
                next_h3_starts = [h.start() for h in all_h3 if h.start() > m.start()]
                sub_end = min(next_h3_starts) if next_h3_starts else len(section_text)
                file_scope = m.group(1).strip()
                entries.extend(_parse_entries(section_text[sub_start:sub_end], tag, file_scope))
            continue

        entries.extend(_parse_entries(section_text, tag, ""))

    return entries


def _parse_entries(block: str, tag: str, file_scope: str) -> list[GlossaryEntry]:
    out: list[GlossaryEntry] = []
    for m in ENTRY_RE.finditer(block):
        canonical = m.group("canonical").strip()
        rhs = m.group("rhs").strip()
        anchors: list[str] = []
        # For contextual entries, separate the (anchors: ...) clause from variants
        # so anchor terms aren't accidentally treated as variants to replace.
        variant_rhs = rhs
        if tag == "contextual":
            am = ANCHOR_RE.search(rhs)
            if am:
                anchors = [a.strip().strip("`") for a in am.group(1).split(",")]
                # Strip the anchors clause before harvesting variants
                variant_rhs = rhs[:am.start()] + rhs[am.end():]
        variants = VARIANT_RE.findall(variant_rhs)
        if canonical and variants:
            out.append(GlossaryEntry(
                canonical=canonical, variants=variants, section=tag,
                anchors=anchors, file_scope=file_scope,
            ))
    return out


# =====================================================================
# Apply corrections
# =====================================================================

@dataclass
class FixCount:
    canonical: str
    variant: str
    section: str
    count: int


# H2 sections that carry log/metadata content the reconciler must NOT rewrite.
# The script injects "## Term reconciliation" itself; "## Decisions made" is
# written by the preprocessor. Re-running today would corrupt these blocks
# (e.g., the line "Poland→Polynt" would re-match \bPoland\b and become
# "Polynt→Polynt"). We mask these regions before applying substitutions.
LOG_H2_RE = re.compile(
    r"^##\s+(Decisions made|Term reconciliation)\b.*$",
    re.MULTILINE | re.IGNORECASE,
)
ANY_H2_RE = re.compile(r"^##\s+", re.MULTILINE)


def _split_log_regions(text: str) -> list[tuple[bool, str]]:
    """Split text into segments tagged (is_log, segment).

    Each log H2 section runs from its header until the next H2 (any) or EOF.
    Active segments are everything else. Concatenating the segments in order
    reproduces the original text exactly.
    """
    segments: list[tuple[bool, str]] = []
    pos = 0
    while pos < len(text):
        m = LOG_H2_RE.search(text, pos)
        if not m:
            segments.append((False, text[pos:]))
            break
        if m.start() > pos:
            segments.append((False, text[pos:m.start()]))
        next_h2 = ANY_H2_RE.search(text, m.end())
        end = next_h2.start() if next_h2 else len(text)
        segments.append((True, text[m.start():end]))
        pos = end
    return segments


def _file_scope_matches(scope: str, filename: str) -> bool:
    """Token-based scope matching.

    The scope (e.g. "Olli Piiroinen") is split on whitespace; every token of
    length >=3 must appear as a substring of the normalized filename
    (lowercased, with separators collapsed to spaces). This survives common
    filename conventions like "Internal - Olli Piiroinen_otter_ai_transcript".
    Empty scope returns True (entry is project-wide).
    """
    if not scope:
        return True
    fn_norm = re.sub(r"[\s\-_]+", " ", filename.lower())
    tokens = [t for t in scope.lower().split() if len(t) >= 3]
    if not tokens:
        # Fall back to a substring check if scope is all short tokens
        return scope.lower() in fn_norm
    return all(t in fn_norm for t in tokens)


def _apply_to_text(
    text: str, entries: list[GlossaryEntry], filename: str,
    counts: dict[tuple[str, str, str], int],
) -> str:
    """Run all entry replacements on a single text segment, accumulating counts."""
    for entry in entries:
        # Skip file-specific entries that don't match current file
        if entry.section == "file-specific" and entry.file_scope:
            if not _file_scope_matches(entry.file_scope, filename):
                continue

        for variant in entry.variants:
            # Word-boundary regex; case-insensitive search; preserve case where
            # canonical is all-caps (e.g., DERAKANE) or capitalized.
            pattern = re.compile(r"\b" + re.escape(variant) + r"\b", re.IGNORECASE)

            if entry.section == "contextual" and entry.anchors:
                # Apply only when an anchor keyword appears in the same paragraph
                paragraphs = re.split(r"\n\s*\n", text)
                new_paras: list[str] = []
                for para in paragraphs:
                    if any(a.lower() in para.lower() for a in entry.anchors):
                        para_new, n = pattern.subn(entry.canonical, para)
                        if n:
                            counts[(entry.canonical, variant, entry.section)] += n
                        new_paras.append(para_new)
                    else:
                        new_paras.append(para)
                text = "\n\n".join(new_paras)
            else:
                text, n = pattern.subn(entry.canonical, text)
                if n:
                    counts[(entry.canonical, variant, entry.section)] += n
    return text


def apply_corrections(
    text: str, entries: list[GlossaryEntry], filename: str
) -> tuple[str, list[FixCount]]:
    """Apply entries to text. Returns (new_text, list of fix counts).

    Skips text inside log/metadata H2 sections ("## Term reconciliation",
    "## Decisions made") so prior fix logs are never re-rewritten.
    """
    counts: dict[tuple[str, str, str], int] = defaultdict(int)
    out_segments: list[str] = []
    for is_log, seg in _split_log_regions(text):
        if is_log:
            out_segments.append(seg)
        else:
            out_segments.append(_apply_to_text(seg, entries, filename, counts))
    new_text = "".join(out_segments)

    fixes = [
        FixCount(canonical=c, variant=v, section=s, count=n)
        for (c, v, s), n in counts.items()
    ]
    return new_text, fixes


# =====================================================================
# Glossary totals block update
# =====================================================================

def render_totals_block(
    files_processed: int, all_fixes: dict[str, list[FixCount]]
) -> str:
    """Render the 'Project-wide totals (this run)' section."""
    lines = ["## Project-wide totals (this run)", ""]
    lines.append(f"Files processed: {files_processed}")
    lines.append("")

    # Aggregate by section
    by_section: dict[str, list[FixCount]] = defaultdict(list)
    for fixes in all_fixes.values():
        for f in fixes:
            by_section[f.section].append(f)

    for section, label in [
        ("confirmed", "Auto-applied (high-confidence)"),
        ("best-inference", "Best-inference applied (medium confidence)"),
        ("contextual", "Contextual"),
        ("file-specific", "File-specific"),
    ]:
        section_fixes = by_section.get(section, [])
        if not section_fixes:
            continue

        # Aggregate (variant→canonical, count) across files
        agg: dict[tuple[str, str], int] = defaultdict(int)
        for f in section_fixes:
            agg[(f.variant, f.canonical)] += f.count
        total = sum(agg.values())

        lines.append(f"### {label}: {total} fixes")
        for (variant, canonical), n in sorted(agg.items(), key=lambda x: -x[1]):
            lines.append(f"- {variant}→{canonical} ×{n}")
        lines.append("")

    return "\n".join(lines)


def update_glossary_totals(glossary_path: Path, totals_block: str) -> None:
    text = glossary_path.read_text(encoding="utf-8")
    # Replace existing "## Project-wide totals" block, or append
    pat = re.compile(
        r"^##\s+Project-wide totals.*?(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pat.search(text):
        new_text = pat.sub(totals_block + "\n\n", text)
    else:
        # Insert before "## Notes" if present, else append
        notes_pat = re.compile(r"^##\s+Notes\s*$", re.MULTILINE)
        m = notes_pat.search(text)
        if m:
            new_text = text[:m.start()] + totals_block + "\n\n" + text[m.start():]
        else:
            new_text = text.rstrip() + "\n\n" + totals_block + "\n"
    glossary_path.write_text(new_text, encoding="utf-8")


# =====================================================================
# Per-file fix log injection
# =====================================================================

FIX_LOG_HEADER = "## Term reconciliation"

def inject_fix_log(text: str, fixes: list[FixCount]) -> str:
    """Replace the placeholder under '## Term reconciliation' with concrete fix counts."""
    if not fixes:
        block = (
            "No glossary fixes applied to this file.\n"
        )
    else:
        agg: dict[str, int] = defaultdict(int)
        for f in fixes:
            agg[f"{f.variant}→{f.canonical}"] += f.count
        lines = ["Glossary fixes auto-applied to this file:", ""]
        for label, n in sorted(agg.items(), key=lambda x: -x[1]):
            lines.append(f"- {label} ×{n}")
        block = "\n".join(lines) + "\n"

    # Replace existing section body
    pat = re.compile(
        rf"({re.escape(FIX_LOG_HEADER)}\s*\n\s*\n).*?(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pat.search(text):
        return pat.sub(r"\1" + block + "\n", text)
    return text + "\n\n" + FIX_LOG_HEADER + "\n\n" + block


# =====================================================================
# Main
# =====================================================================

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--input", required=True,
                        help="Folder of pre-processed transcripts (.preprocessed.md)")
    parser.add_argument("--glossary", required=True,
                        help="Path to project glossary.md")
    parser.add_argument("--no-inplace", action="store_true",
                        help="Write to .reconciled.md instead of modifying in place")
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute fix counts without writing files")
    args = parser.parse_args(argv)

    in_dir = Path(args.input)
    glossary_path = Path(args.glossary)

    if not in_dir.is_dir():
        print(f"ERROR: input folder not found: {in_dir}", file=sys.stderr)
        return 2
    if not glossary_path.is_file():
        print(f"ERROR: glossary file not found: {glossary_path}", file=sys.stderr)
        return 2

    glossary_text = glossary_path.read_text(encoding="utf-8")
    entries = parse_glossary(glossary_text)
    if not entries:
        print("WARNING: no entries parsed from glossary. Check format.", file=sys.stderr)

    files = sorted(in_dir.glob("*.preprocessed.md"))
    if not files:
        print(f"ERROR: no .preprocessed.md files in {in_dir}", file=sys.stderr)
        return 2

    all_fixes: dict[str, list[FixCount]] = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        new_text, fixes = apply_corrections(text, entries, path.name)
        new_text = inject_fix_log(new_text, fixes)
        all_fixes[path.name] = fixes

        if args.dry_run:
            total = sum(f.count for f in fixes)
            print(f"[dry-run] {path.name}: {total} fixes")
            continue

        out_path = path if not args.no_inplace else path.with_suffix(".reconciled.md")
        out_path.write_text(new_text, encoding="utf-8")
        total = sum(f.count for f in fixes)
        print(f"Reconciled: {path.name} ({total} fixes)")

    if not args.dry_run:
        totals_block = render_totals_block(len(files), all_fixes)
        update_glossary_totals(glossary_path, totals_block)
        print(f"\nUpdated totals in {glossary_path}")

    grand_total = sum(f.count for fixes in all_fixes.values() for f in fixes)
    print(f"\nTotal fixes: {grand_total} across {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
