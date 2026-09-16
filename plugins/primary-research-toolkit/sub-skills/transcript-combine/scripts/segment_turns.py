#!/usr/bin/env python3
"""Repair collapsed diarization: split blob turns back into speaker turns.

When a transcription tool tags a long back-and-forth under one speaker label, the
words are all there but the attribution is wrong — and a quote on the wrong
person's lips looks correct, so nothing downstream catches it.

Splitting is mostly mechanical. Interview dialogue has strong cues: a question
followed by an affirmation, a short acknowledgement, a new question. This script
proposes boundaries from those cues and asks for a decision on each. Crucially it
works in character offsets, so the text is never rewritten — no amount of review
can alter a word, and the cost is a few tokens per boundary rather than the whole
transcript twice.

Propose:
  python3 segment_turns.py --propose normalized/granola.jsonl \
      --out boundaries.json --speakers "Andrew Gartley (Newry)" "Anthony Carpenter (Bayhealth)"

Read boundaries.review.json, write decisions, then:
  python3 segment_turns.py --apply normalized/granola.jsonl boundary_decisions.json \
      --out normalized/granola.split.jsonl

Decisions file:
  {"accept": [1, 2, 5, 9], "reject": [3],
   "speakers": {"1": "Andrew Gartley (Newry)"},
   "default_alternate": true}

  accept            - boundary ids to split at. Unlisted ids are rejected, so a
                      partial pass is safe.
  speakers          - who speaks AFTER that boundary. Omit to use the proposal's
                      guess, or rely on default_alternate.
  default_alternate - alternate between the two --speakers names across accepted
                      boundaries when no explicit speaker is given (default true).
"""

import argparse
import json
import os
import re
import sys

WORD_RE = re.compile(r"\S+")
# Sentence boundary, keeping the offset of what follows.
SENT_BOUNDARY = re.compile(r"(?<=[.!?])\s+")

BLOB_WORDS = 120

AFFIRMATIONS = {
    "yeah", "yep", "yes", "no", "nope", "right", "correct", "sure", "exactly",
    "absolutely", "true", "agreed", "totally", "definitely", "certainly",
}
BACKCHANNEL = (
    "okay", "ok", "got it", "gotcha", "that makes sense", "makes sense",
    "interesting", "understood", "i see", "fair enough", "of course",
    "perfect", "great", "sure", "right", "thank you", "thanks", "wow",
    "very helpful", "that's helpful", "helpful",
)
QUESTION_OPENERS = (
    "do you", "did you", "does it", "does that", "do they", "how do", "how does",
    "how much", "how many", "how are", "what do", "what about", "what's",
    "what is", "what are", "what would", "can you", "could you", "would you",
    "is there", "are there", "was there", "why do", "why is", "why would",
    "when do", "when did", "who is", "who are", "who else", "tell me",
    "walk me", "help me understand", "so how", "so what", "and what", "and how",
    "any sense", "curious", "talk to me",
)


def load(path):
    turns = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                turns.append(json.loads(line))
    if not turns:
        sys.exit(f"error: {path} has no turns")
    return turns


def split_sentences(text):
    """Sentences with their character offsets into text."""
    out, pos = [], 0
    for piece in SENT_BOUNDARY.split(text):
        if not piece:
            continue
        idx = text.find(piece, pos)
        if idx < 0:
            idx = pos
        out.append((idx, piece))
        pos = idx + len(piece)
    return out


def normalized_head(sentence, n=5):
    words = WORD_RE.findall(sentence.lower())
    return re.sub(r"[^\w\s']", "", " ".join(words[:n])).strip()


def score_boundary(prev_sentence, sentence):
    """How strongly does a speaker change start at this sentence?"""
    head = normalized_head(sentence)
    if not head:
        return 0, ""
    first = head.split()[0]
    n_words = len(WORD_RE.findall(sentence))
    prev_is_question = prev_sentence.rstrip().endswith("?")
    is_question = sentence.rstrip().endswith("?")

    if prev_is_question and first in AFFIRMATIONS:
        return 3, "answer to the preceding question"
    if prev_is_question and not is_question:
        return 2, "statement following a question"
    if n_words <= 6 and any(head.startswith(b) for b in BACKCHANNEL):
        return 3, "short acknowledgement, typical of the interviewer"
    if is_question and any(head.startswith(q) for q in QUESTION_OPENERS):
        return 3, "new question"
    if is_question and not prev_is_question:
        return 2, "question following a statement"
    if first in AFFIRMATIONS and n_words <= 12:
        return 2, "short affirmation"
    if any(head.startswith(q) for q in QUESTION_OPENERS):
        return 1, "interrogative phrasing without a question mark"
    return 0, ""


def context(text, offset, before=12, after=12):
    left = " ".join(WORD_RE.findall(text[:offset])[-before:])
    right = " ".join(WORD_RE.findall(text[offset:])[:after])
    return left, right


def propose(turns, min_score, speakers):
    candidates = []
    for t_idx, turn in enumerate(turns):
        text = turn.get("text") or ""
        if len(WORD_RE.findall(text)) < BLOB_WORDS:
            continue
        sents = split_sentences(text)
        for i in range(1, len(sents)):
            offset, sentence = sents[i]
            score, why = score_boundary(sents[i - 1][1], sentence)
            if score < min_score:
                continue
            left, right = context(text, offset)
            candidates.append({
                "turn": t_idx,
                "offset": offset,
                "confidence": {3: "high", 2: "medium", 1: "low"}[score],
                "why": why,
                "before": "…" + left,
                "after": right + "…",
                "guess": None,
            })

    # Guess who speaks after each boundary: a question or acknowledgement points
    # at the interviewer, a substantive answer at the interviewee.
    for cand in candidates:
        why = cand["why"]
        if speakers and len(speakers) >= 2:
            if why in ("new question", "short acknowledgement, typical of the "
                                       "interviewer",
                       "question following a statement",
                       "interrogative phrasing without a question mark"):
                cand["guess"] = speakers[0]
            else:
                cand["guess"] = speakers[1]

    # "Okay. That makes sense." is one interviewer turn, not two. Where adjacent
    # sentences would both be handed to the same speaker, the later boundary is
    # noise — dropping it keeps the review list honest about how many real
    # speaker changes there are.
    consolidated = []
    for cand in candidates:
        prev = consolidated[-1] if consolidated else None
        if (prev and prev["turn"] == cand["turn"] and prev["guess"] == cand["guess"]
                and cand["guess"] is not None
                and cand["offset"] - prev["offset"] <= 60):
            continue
        consolidated.append(cand)

    for i, cand in enumerate(consolidated, 1):
        cand["id"] = i
    return consolidated


def apply(turns, decisions, speakers):
    accept = set(decisions.get("accept") or [])
    explicit = {int(k): v for k, v in (decisions.get("speakers") or {}).items()}
    alternate = decisions.get("default_alternate", True)
    proposals = {c["id"]: c for c in decisions.get("_proposals", [])}
    if not proposals:
        sys.exit("error: decisions file must carry the proposal list. Pass the "
                 "boundaries file produced by --propose as 'boundaries', or add "
                 "a '_proposals' key. See --help.")

    by_turn = {}
    for bid in sorted(accept):
        if bid not in proposals:
            sys.exit(f"error: boundary {bid} is not in the proposals")
        cand = proposals[bid]
        by_turn.setdefault(cand["turn"], []).append((cand["offset"], bid, cand))

    out, split_count = [], 0
    for t_idx, turn in enumerate(turns):
        marks = sorted(by_turn.get(t_idx, []))
        if not marks:
            out.append(turn)
            continue
        text = turn.get("text") or ""
        offsets = [0] + [m[0] for m in marks] + [len(text)]
        current = turn.get("speaker")
        for piece_idx in range(len(offsets) - 1):
            chunk = text[offsets[piece_idx]:offsets[piece_idx + 1]].strip()
            if not chunk:
                continue
            if piece_idx == 0:
                speaker = current
            else:
                _, bid, cand = marks[piece_idx - 1]
                if bid in explicit:
                    speaker = explicit[bid]
                elif cand.get("guess"):
                    speaker = cand["guess"]
                elif alternate and speakers and len(speakers) >= 2:
                    speaker = speakers[1] if current == speakers[0] else speakers[0]
                else:
                    speaker = current
                current = speaker
            # A split that puts the same speaker either side wasn't a speaker
            # change; fold it back rather than leaving a spurious turn break.
            if out and out[-1].get("speaker") == speaker and piece_idx:
                out[-1]["text"] = (out[-1]["text"] + " " + chunk).strip()
                continue
            new_turn = dict(turn)
            new_turn["speaker"] = speaker
            new_turn["text"] = chunk
            if piece_idx:
                new_turn["start_sec"] = None
                new_turn["start"] = turn.get("start", "")
                new_turn["split_from_turn"] = t_idx
            out.append(new_turn)
        split_count += len(marks)
    return out, split_count


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--propose", metavar="JSONL",
                    help="normalized .jsonl to find boundaries in")
    ap.add_argument("--apply", nargs=2, metavar=("JSONL", "DECISIONS"),
                    help="normalized .jsonl plus a decisions file")
    ap.add_argument("--boundaries", help="boundaries file from --propose "
                                        "(needed by --apply if the decisions "
                                        "file has no _proposals)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--speakers", nargs="*", default=[],
                    help="interviewer first, then interviewee")
    ap.add_argument("--min-confidence", choices=["low", "medium", "high"],
                    default="medium")
    args = ap.parse_args()

    if not args.propose and not args.apply:
        sys.exit("error: pass --propose or --apply")

    if args.propose:
        turns = load(args.propose)
        min_score = {"low": 1, "medium": 2, "high": 3}[args.min_confidence]
        candidates = propose(turns, min_score, args.speakers)
        blobs = [i for i, t in enumerate(turns)
                 if len(WORD_RE.findall(t.get("text") or "")) >= BLOB_WORDS]

        os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"source": args.propose, "speakers": args.speakers,
                       "blob_turns": blobs, "proposals": candidates}, fh,
                      ensure_ascii=False, indent=1)

        base = args.out[:-5] if args.out.endswith(".json") else args.out
        review_path = base + ".review.json"
        review = {
            "read_me": "Accept or reject each boundary. 'before'/'after' show the "
                       "words either side; no text is rewritten, so a decision "
                       "cannot change a word. Write {\"accept\": [ids], "
                       "\"speakers\": {\"id\": \"Name\"}} and run --apply.",
            "source": args.propose,
            "speakers": args.speakers,
            "blob_turns": len(blobs),
            "boundaries": [{"id": c["id"], "turn": c["turn"],
                            "confidence": c["confidence"], "why": c["why"],
                            "guess": c["guess"], "before": c["before"],
                            "after": c["after"]} for c in candidates],
        }
        with open(review_path, "w", encoding="utf-8") as fh:
            json.dump(review, fh, ensure_ascii=False, indent=1)

        by_conf = {}
        for c in candidates:
            by_conf[c["confidence"]] = by_conf.get(c["confidence"], 0) + 1
        print(f"wrote {args.out}")
        print(f"  blob turns examined:  {len(blobs)}")
        print(f"  boundaries proposed:  {len(candidates)}  "
              f"({', '.join(f'{n} {k}' for k, n in sorted(by_conf.items()))})")
        print(f"  review file:          {review_path} "
              f"({os.path.getsize(review_path) // 1024} KB)")
        if not candidates and blobs:
            print("  NOTE: blobs present but no boundaries found. Try "
                  "--min-confidence low; if still nothing, the blob may really "
                  "be one long answer.")
        return

    jsonl_path, decisions_path = args.apply
    turns = load(jsonl_path)
    with open(decisions_path, "r", encoding="utf-8") as fh:
        decisions = json.load(fh)
    if "_proposals" not in decisions:
        boundaries_path = args.boundaries
        if not boundaries_path:
            guess = decisions_path
            for cand in (args.out, decisions_path):
                pass
            sys.exit("error: pass --boundaries pointing at the file from --propose")
        with open(boundaries_path, "r", encoding="utf-8") as fh:
            decisions["_proposals"] = json.load(fh)["proposals"]

    speakers = args.speakers or decisions.get("speakers") or []
    out_turns, splits = apply(turns, decisions, speakers)

    before_words = sum(len(WORD_RE.findall(t.get("text") or "")) for t in turns)
    after_words = sum(len(WORD_RE.findall(t.get("text") or "")) for t in out_turns)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        for turn in out_turns:
            fh.write(json.dumps(turn, ensure_ascii=False) + "\n")

    print(f"wrote {args.out}")
    print(f"  turns:            {len(turns)} -> {len(out_turns)} "
          f"({splits} split{'s' if splits != 1 else ''} applied)")
    print(f"  words:            {before_words} -> {after_words}")
    if before_words != after_words:
        print(f"  WARNING: word count changed by {after_words - before_words}. "
              f"Splitting must never lose or add words — investigate before "
              f"building anything from this file.")
    else:
        print("  word count unchanged, as it must be")
    longest = max((len(WORD_RE.findall(t.get("text") or "")) for t in out_turns),
                  default=0)
    print(f"  longest turn:     {longest} words"
          + ("  (still blob-sized; consider --min-confidence low)"
             if longest >= BLOB_WORDS else ""))


if __name__ == "__main__":
    main()
