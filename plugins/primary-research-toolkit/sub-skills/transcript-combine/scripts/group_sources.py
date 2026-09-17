#!/usr/bin/env python3
"""Group the transcript files in a folder by which call they belong to.

  python3 group_sources.py materials/ --json groups.json
  python3 group_sources.py materials/ --roster "Randall Jenkins" "Bonnie Solitaire"

Combining needs to know which files are recordings of the SAME interview, and
nothing upstream guarantees that. Real folders look like this, all one call:

    GPO Dynamics with Bonnie_otter_ai_transcript.docx
    Bonnie Granola Transcript.docx
    2026-07-28_Urology Medical Device Contracting Dynamics_Bonnie Solitaire.docx

Reading filenames by eye works until it doesn't, and the failure is silent: a
missed file means a witness that never votes, and a wrongly grouped file means
two different calls merged into one transcript.

So this proposes groups and says how confident it is; a person or the calling
skill confirms. It never decides. Exit code is 0 when every file landed in a
confident group, 2 when something needs a human — the same convention
check_sources.py uses.

Signals used, in order of weight:
  * a name from --roster appearing in the filename (strongest, when supplied)
  * a shared date in the filename (2026-07-28, 07202026, 2026.07.28)
  * a shared capitalised personal name, ignoring words common to the folder
  * a recogniser for tool names (Otter, Granola, Teams, Tegus, ...) so those
    words never look like the thing that distinguishes two calls
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

TRANSCRIPT_EXT = {".docx", ".pdf", ".txt", ".vtt", ".srt", ".md", ".json", ".jsonl"}

# Words that say which tool produced a file, not which call it is.
TOOL_WORDS = {
    "otter", "granola", "teams", "zoom", "tegus", "alphasense", "guidepoint",
    "glg", "inexone", "inex", "ai", "transcript", "transcripts", "recording",
    "audio", "export", "raw", "combined", "compiled", "copy", "final", "draft",
    "v1", "v2", "v3", "notes", "note", "summary", "interview", "call", "meeting",
    "discussion", "with", "and", "the", "at", "for", "formerly", "phone",
}

# Things that are output, not input.
NOT_A_SOURCE = re.compile(
    r"combined|compiled|summary card|themed findings|interview summary|_summary|roll-?up",
    re.I)

DATE_PATTERNS = [
    (re.compile(r"(20\d\d)[-._](\d{2})[-._](\d{2})"), lambda m: f"{m[1]}-{m[2]}-{m[3]}"),
    (re.compile(r"\b(\d{2})(\d{2})(20\d\d)\b"), lambda m: f"{m[3]}-{m[1]}-{m[2]}"),
    (re.compile(r"\b(20\d\d)(\d{2})(\d{2})\b"), lambda m: f"{m[1]}-{m[2]}-{m[3]}"),
]


def find_date(name):
    for pattern, fmt in DATE_PATTERNS:
        m = pattern.search(name)
        if m:
            return fmt(m)
    return None


def words(name):
    stem = os.path.splitext(name)[0]
    return [w for w in re.split(r"[^A-Za-z]+", stem) if w]


def candidate_names(name, folder_common):
    """Capitalised words that could be a person, minus tool and folder noise."""
    out = []
    for w in words(name):
        low = w.lower()
        if low in TOOL_WORDS or low in folder_common or len(w) < 3:
            continue
        if w[0].isupper():
            out.append(low)
    return out


def roster_hit(name, roster):
    """Longest roster entry whose surname or forename appears in the filename."""
    low = name.lower()
    best = None
    for person in roster:
        parts = [p.lower() for p in re.split(r"[^A-Za-z]+", person) if len(p) > 2]
        if any(p in low for p in parts):
            if best is None or len(person) > len(best):
                best = person
    return best


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", help="folder of transcript files (e.g. materials/)")
    ap.add_argument("--roster", nargs="*", default=[],
                    help="known interviewee names; supply these when you have them "
                         "— they turn a guess into a match")
    ap.add_argument("--json", help="write the proposed groups here")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.folder):
        sys.exit(f"error: not a folder: {args.folder}")

    files, skipped = [], []
    for f in sorted(os.listdir(args.folder)):
        if os.path.splitext(f)[1].lower() not in TRANSCRIPT_EXT:
            continue
        if NOT_A_SOURCE.search(f):
            skipped.append(f)
            continue
        files.append(f)

    if not files:
        sys.exit(f"error: no transcript files in {args.folder}")

    # Words appearing in most filenames describe the project, not the call.
    counts = Counter()
    for f in files:
        counts.update({w.lower() for w in words(f)})
    folder_common = {w for w, n in counts.items() if n >= max(2, len(files) * 0.6)}

    groups = defaultdict(list)
    how = {}
    for f in files:
        person = roster_hit(f, args.roster) if args.roster else None
        if person:
            key, basis = person, "roster name"
        else:
            names = candidate_names(f, folder_common)
            date = find_date(f)
            if names:
                key, basis = names[0], "name in filename"
            elif date:
                key, basis = f"call on {date}", "date in filename"
            else:
                key, basis = f"ungrouped: {f}", "nothing to group on"
        groups[key].append(f)
        how[key] = basis

    # A group whose files disagree on date is suspect — likely two calls merged.
    report, needs_human = [], False
    for key, members in sorted(groups.items()):
        dates = {d for d in (find_date(m) for m in members) if d}
        basis = how[key]
        concern = None
        if basis == "nothing to group on":
            concern = "could not tell which call this belongs to"
        elif len(dates) > 1:
            concern = f"files disagree on date ({', '.join(sorted(dates))}) — two calls?"
        elif len(members) == 1:
            concern = "only one recording — combining cannot cross-check anything"
        if concern:
            needs_human = True
        report.append({"call": key, "basis": basis, "files": members,
                       "date": sorted(dates)[0] if len(dates) == 1 else None,
                       "concern": concern})

    if not args.quiet:
        print(f"{len(files)} transcript file(s) in {args.folder} "
              f"-> {len(report)} call(s)")
        if skipped:
            print(f"  ignored {len(skipped)} output file(s): "
                  f"{', '.join(skipped[:3])}{' ...' if len(skipped) > 3 else ''}")
        if not args.roster:
            print("  no --roster given, so grouping is inferred from filenames; "
                  "pass the known interviewee names to make it certain")
        print()
        for g in report:
            print(f"  {g['call']}  ({len(g['files'])} file(s), by {g['basis']})")
            for f in g["files"]:
                print(f"      {f}")
            if g["concern"]:
                print(f"      ^ {g['concern']}")
        print()
        multi = [g for g in report if len(g["files"]) > 1]
        print(f"  {len(multi)} call(s) have more than one recording and can be combined")
        if needs_human:
            print("  Confirm the grouping with the consultant before combining.")

    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)) or ".", exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"folder": args.folder, "roster": args.roster,
                       "ignored": skipped, "calls": report}, fh,
                      ensure_ascii=False, indent=1)
        if not args.quiet:
            print(f"  wrote {args.json}")

    sys.exit(2 if needs_human else 0)


if __name__ == "__main__":
    main()
