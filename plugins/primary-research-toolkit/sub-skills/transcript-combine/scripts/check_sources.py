#!/usr/bin/env python3
"""Preflight: are these files actually degarblable, and how hard will it be?

Run this before anything else. The pipeline assumes each source is a verbatim
transcript of one call with usable speaker turns. When that assumption is wrong —
a paraphrased analyst report standing in for a transcript, diarization that
collapsed both speakers into one label, no timestamps — the assumption fails
silently and the cost of finding out by hand is enormous. This script finds out
for a few hundred tokens instead.

Usage:
  python3 check_sources.py normalized/*.jsonl
  python3 check_sources.py normalized/granola.jsonl normalized/tegus.jsonl --json report.json

Exit status is 0 when the set looks workable and 2 when something needs a human
decision before proceeding, so it can gate a script. The verdict is advisory, not
a veto: show it to the user and let them choose.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

WORD_RE = re.compile(r"\S+")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

# A dialogue turn this long is suspicious; combined with internal dialogue cues
# it means the turn probably contains more than one speaker.
BLOB_WORDS = 120
# Above this share of words sitting in suspect turns, attribution is unreliable
# enough that quoting from the result would be unsafe.
BLOB_SHARE_SERIOUS = 0.15

AFFIRMATIONS = {
    "yeah", "yep", "yes", "no", "right", "correct", "sure", "exactly",
    "absolutely", "okay", "ok", "true", "agreed", "totally", "definitely",
}
BACKCHANNEL = {
    "okay", "got it", "that makes sense", "makes sense", "interesting",
    "understood", "i see", "sure", "right", "fair enough", "of course",
    "gotcha", "perfect", "great", "thank you", "thanks",
}
QUESTION_OPENERS = (
    "do you", "did you", "does it", "how do", "how does", "how much", "how many",
    "what do", "what about", "what's", "what is", "can you", "could you",
    "would you", "is there", "are there", "why do", "why is", "when do",
    "who is", "who are", "tell me", "walk me", "help me understand", "so how",
    "so what", "and what", "and how",
)
# Markers of a paraphrased report rather than a transcript of speech.
PARAPHRASE_MARKERS = (
    "alphasense", "tegus", "expert call", "advisor", "adr",
    "this transcript", "the following", "executive summary", "key topics",
    "topics covered", "biography", "disclaimer", "confidential",
    "for internal use", "do not distribute", "third-party", "expert network",
)


def load(path):
    turns = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    turns.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    return None, f"line {len(turns) + 1} is not valid JSON: {exc}"
    if not turns:
        return None, "file has no turns"
    return turns, None


def sentences(text):
    return [s.strip() for s in SENT_SPLIT.split(text or "") if s.strip()]


def first_words(sentence, n=4):
    return " ".join(WORD_RE.findall(sentence.lower())[:n])


def dialogue_cues(text):
    """Count signs that a single turn contains a back-and-forth exchange."""
    sents = sentences(text)
    cues = 0
    for idx, sent in enumerate(sents):
        head = first_words(sent)
        bare = re.sub(r"[^\w\s]", "", head).strip()
        if idx and sents[idx - 1].rstrip().endswith("?"):
            if bare.split()[:1] and bare.split()[0] in AFFIRMATIONS:
                cues += 1
                continue
        if any(bare.startswith(b) for b in BACKCHANNEL) and len(WORD_RE.findall(sent)) <= 6:
            cues += 1
            continue
        if any(head.startswith(q) for q in QUESTION_OPENERS) and sent.rstrip().endswith("?"):
            cues += 1
    return cues


def looks_paraphrased(turns):
    """Distinguish a report about a call from a transcript of one.

    Speech is dense in first- and second-person pronouns and contractions;
    written summaries are not, and they carry front-matter no speaker would say.
    """
    text = " ".join((t.get("text") or "") for t in turns)
    words = WORD_RE.findall(text.lower())
    if not words:
        return False, []
    total = len(words)
    head = text[:3000].lower()
    markers = sorted({m for m in PARAPHRASE_MARKERS if m in head})

    # Expert-network front matter is decisive on its own and needs no length:
    # nobody says "Biography" or "CONFIDENTIAL — do not distribute" out loud.
    if len(markers) >= 3:
        return True, [f"expert-network front matter in the opening: "
                      f"{', '.join(markers[:5])}"]

    # The statistical signals are noisy on short samples, and wrongly calling a
    # real transcript paraphrased would strip it of its vote.
    if total < 200:
        return False, []

    bare = [re.sub(r"[^\w']", "", w) for w in words]
    pronouns = sum(1 for w in bare if w in
                   {"i", "you", "we", "my", "your", "our", "me", "us", "i'm",
                    "you're", "we're", "i've", "you've", "we've"})
    contractions = sum(1 for w in bare if "'" in w)

    reasons = []
    pronoun_rate = pronouns / total
    if pronoun_rate < 0.030:
        reasons.append(f"first/second-person pronouns are only "
                       f"{pronoun_rate * 100:.1f}% of words (speech is usually 5-9%)")
    if contractions / total < 0.008:
        reasons.append("almost no contractions, which spoken English is full of")
    if markers:
        reasons.append(f"report-style markers in the opening: {', '.join(markers[:4])}")
    # Two independent signals before calling it — one alone has false positives
    # on unusually formal calls.
    return len(reasons) >= 2, reasons


def token_stream(turns):
    text = " ".join((t.get("text") or "") for t in turns).lower()
    return re.sub(r"[^\w\s]", "", text).split()


# Two exports of the SAME engine agree on essentially every token. Two different
# engines transcribing one call also agree on most tokens — that is the whole
# premise of the pipeline — so only near-identity distinguishes them, and it has
# to be measured over the region they share, since one export may be truncated.
DUPLICATE_RATIO = 0.99


def same_engine(a_turns, b_turns):
    """Similarity over the overlapping region, ignoring truncation."""
    import difflib
    a, b = token_stream(a_turns), token_stream(b_turns)
    if len(a) < 40 or len(b) < 40:
        return None
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    blocks = [blk for blk in matcher.get_matching_blocks() if blk.size]
    if not blocks:
        return 0.0
    a_lo, a_hi = blocks[0].a, blocks[-1].a + blocks[-1].size
    b_lo, b_hi = blocks[0].b, blocks[-1].b + blocks[-1].size
    span = max(a_hi - a_lo, b_hi - b_lo)
    if span < 40:
        return None
    matched = sum(blk.size for blk in blocks)
    return round(matched / span, 4)


def inspect(path):
    turns, error = load(path)
    if error:
        return {"path": path, "fatal": error}

    name = turns[0].get("source") or os.path.basename(path)
    texts = [(t.get("text") or "") for t in turns]
    words = sum(len(WORD_RE.findall(t)) for t in texts)
    timed = [t for t in turns if t.get("start_sec") is not None]
    labels = [t.get("speaker") for t in turns if t.get("speaker")]
    label_counts = Counter(labels)

    blobs = []
    for idx, turn in enumerate(turns):
        n_words = len(WORD_RE.findall(turn.get("text") or ""))
        if n_words < BLOB_WORDS:
            continue
        cues = dialogue_cues(turn.get("text") or "")
        if cues >= 2:
            blobs.append({"turn": idx, "words": n_words, "cues": cues,
                          "speaker": turn.get("speaker")})
    blob_words = sum(b["words"] for b in blobs)

    paraphrased, para_reasons = looks_paraphrased(turns)

    problems, notes = [], []
    if not timed:
        notes.append("no timestamps — turn numbers will stand in for clock times, "
                     "and same-speaker merging is disabled (correctly)")
    elif len(timed) < len(turns) * 0.8:
        notes.append(f"only {len(timed)} of {len(turns)} turns carry a timestamp")

    if not labels:
        problems.append("no speaker labels at all")
    elif len(label_counts) == 1:
        problems.append(f"only one speaker label ({next(iter(label_counts))}) for the "
                        f"whole file — diarization failed or this is a monologue")
    elif len(label_counts) > 12:
        notes.append(f"{len(label_counts)} distinct speaker labels, which usually "
                     f"means header lines were parsed as speakers")

    generic = [l for l in label_counts if re.match(
        r"^(speaker\s*\d+|me|them|us|unknown|participant\s*\d*)$", l.strip(), re.I)]
    if generic:
        notes.append(f"generic labels need mapping to real people: "
                     f"{', '.join(sorted(generic)[:6])}")

    if blobs:
        share = blob_words / words if words else 0
        message = (f"{len(blobs)} turn(s) holding {blob_words} words "
                   f"({share * 100:.0f}% of the file) look like several speakers "
                   f"merged into one turn")
        (problems if share >= BLOB_SHARE_SERIOUS else notes).append(message)

    if paraphrased:
        problems.append("this reads as a paraphrased report, not a verbatim "
                        "transcript: " + "; ".join(para_reasons))

    return {
        "path": path, "name": name, "turns": len(turns), "words": words,
        "timestamps": bool(timed),
        "duration": turns[-1].get("start") if timed else None,
        "speaker_labels": dict(label_counts.most_common(8)),
        "generic_labels": generic,
        "blobs": blobs, "blob_words": blob_words,
        "blob_share": round(blob_words / words, 3) if words else 0,
        "looks_paraphrased": paraphrased,
        "paraphrase_reasons": para_reasons,
        "problems": problems, "notes": notes,
        "_turns": turns,
        "longest_turn": max((len(WORD_RE.findall(t)) for t in texts), default=0),
    }


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", help="normalized .jsonl files")
    ap.add_argument("--json", help="also write the report as JSON")
    args = ap.parse_args()

    reports = [inspect(p) for p in args.sources]
    fatal = [r for r in reports if r.get("fatal")]
    ok = [r for r in reports if not r.get("fatal")]

    # Same transcript twice? Then it is one witness and must share a vote group.
    duplicates = []
    parent = {i: i for i in range(len(ok))}

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(ok)):
        for j in range(i + 1, len(ok)):
            ratio = same_engine(ok[i]["_turns"], ok[j]["_turns"])
            if ratio is not None and ratio >= DUPLICATE_RATIO:
                duplicates.append((ok[i]["name"], ok[j]["name"], ratio))
                parent[find(i)] = find(j)

    verbatim = [r for r in ok if not r["looks_paraphrased"]]
    paraphrase = [r for r in ok if r["looks_paraphrased"]]
    verbatim_idx = [i for i, r in enumerate(ok) if not r["looks_paraphrased"]]
    votes = len({find(i) for i in verbatim_idx})

    print("=" * 68)
    print("SOURCE PREFLIGHT")
    print("=" * 68)
    for r in reports:
        print()
        if r.get("fatal"):
            print(f"  {os.path.basename(r['path'])}: UNREADABLE — {r['fatal']}")
            continue
        print(f"  {r['name']}  ({os.path.basename(r['path'])})")
        print(f"    {r['turns']} turns, {r['words']} words, longest turn "
              f"{r['longest_turn']} words"
              + (f", runs to {r['duration']}" if r["duration"] else ""))
        print(f"    speakers: {', '.join(f'{k} ({v})' for k, v in r['speaker_labels'].items()) or 'none'}")
        for p in r["problems"]:
            print(f"    PROBLEM: {p}")
        for n in r["notes"]:
            print(f"    note:    {n}")

    if duplicates:
        print()
        for a, b, overlap in duplicates:
            print(f"  DUPLICATE: {a} and {b} share {overlap * 100:.0f}% of their "
                  f"opening text — same transcript twice. Give them the same "
                  f"':GROUP' so they share one vote.")

    # ---- verdict
    blocking = [(r["name"], p) for r in ok for p in r["problems"]]
    difficulty = "straightforward"
    reasons, path = [], []

    if paraphrase:
        difficulty = "needs a decision"
        for r in paraphrase:
            reasons.append(f"{r['name']} is not a verbatim transcript, so it cannot "
                           f"vote on wording")
        path.append("Use the paraphrased source(s) for glossary and context only — "
                    "do not pass them to align_sources.py.")

    bad_blobs = [r for r in ok if r["blob_share"] >= BLOB_SHARE_SERIOUS]
    if bad_blobs:
        difficulty = "difficult"
        for r in bad_blobs:
            reasons.append(f"{r['name']} has {r['blob_share'] * 100:.0f}% of its words "
                           f"in turns that mix speakers, so attribution is unreliable")
        path.append("Repair attribution first with segment_turns.py --propose, "
                    "which finds candidate turn boundaries for review. Do NOT "
                    "re-segment by hand or hand transcript text to subagents.")

    if votes < 2:
        if difficulty == "straightforward":
            difficulty = "needs a decision"
        reasons.append(f"{max(votes, 0)} independent verbatim source(s), so nothing "
                       f"can be cross-checked")
        path.append("Run the single-source path: align_sources.py with an anchor "
                    "and no --source. Glossary, filler and speaker work still "
                    "apply; corroboration does not.")
    elif votes == 2:
        reasons.append("2 independent sources, so a disagreement can never be "
                       "settled by majority — expect more flags")

    unreadable = [r["path"] for r in fatal]
    if unreadable:
        difficulty = "difficult"
        reasons.append(f"unreadable: {', '.join(unreadable)}")

    print()
    print("-" * 68)
    print(f"VERDICT: {difficulty.upper()}")
    print(f"  independent verbatim sources that can vote: {max(votes, 0)}")
    for r in reasons:
        print(f"  - {r}")
    if path:
        print("  Recommended path:")
        for p in path:
            print(f"    * {p}")
    if difficulty != "straightforward":
        print()
        print("  Show this to the user and ask how to proceed before doing any "
              "full-text work.")
    print("-" * 68)

    if args.json:
        for r in reports:
            r.pop("_turns", None)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"difficulty": difficulty, "votes": max(votes, 0),
                       "reasons": reasons, "recommended_path": path,
                       "sources": reports, "duplicates": duplicates}, fh,
                      ensure_ascii=False, indent=1)
        print(f"  report written to {args.json}")

    sys.exit(0 if difficulty == "straightforward" else 2)


if __name__ == "__main__":
    main()
