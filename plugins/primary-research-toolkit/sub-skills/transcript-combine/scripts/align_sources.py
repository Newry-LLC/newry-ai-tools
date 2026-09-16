#!/usr/bin/env python3
"""Align several normalized transcripts of one call and isolate what needs judgment.

Most of a multi-source transcript is not in dispute. This script does the
mechanical work — aligning the sources word by word, keeping what they agree on,
and settling disagreements that have a clear majority behind them — so only the
genuinely ambiguous spans have to be read and decided. On a typical interview
that is a few percent of the words.

Usage:
  python3 align_sources.py \
      --anchor  normalized/otter.jsonl \
      --source  normalized/granola.jsonl \
      --source  normalized/notes.jsonl \
      --out     alignment.json

  # Two files from the same transcription engine are one witness, so they share
  # one vote. Append :GROUP to say so:
  python3 align_sources.py --anchor normalized/otter.jsonl:otter \
      --source normalized/otter_pdf.jsonl:otter \
      --source normalized/granola.jsonl --out alignment.json

Two rules the script enforces so nobody has to remember them:

  * Votes are counted per group, never per file, so a PDF export and a live pull
    from the same engine cannot outvote a genuinely independent source.
  * Absence is not a vote. A source that has nothing where others have speech is
    missing coverage, not arguing for deletion, so it abstains.

Output carries the full transcript, but a caller only needs to read three short
lists from it — needs_judgment, coverage_gaps, filler_candidates — decide those,
and pass the decisions to build_payload.py.
"""

import argparse
import difflib
import json
import os
import re
import sys
from collections import Counter, OrderedDict

# Filler is excluded from alignment so one source saying "um" doesn't read as a
# disagreement. It comes back as filler_candidates, because whether a given
# "you know" is filler or meaningful is a judgment call, not a lookup.
FILLER = {
    "um", "umm", "uh", "uhh", "er", "erm", "ah", "mm", "mhm", "hmm", "huh",
    "like", "sorta", "kinda", "basically", "actually", "literally",
    "so", "well", "anyway", "anyways", "right", "okay", "ok",
}
FILLER_PHRASES = [
    ("you", "know"), ("i", "mean"), ("sort", "of"), ("kind", "of"),
    ("you", "see"), ("i", "guess"), ("or", "whatever"), ("i", "think"),
]

NEGATIONS = {
    "not", "no", "never", "none", "nothing", "nobody", "cannot", "cant",
    "wont", "dont", "doesnt", "didnt", "isnt", "arent", "wasnt", "werent",
    "hasnt", "havent", "hadnt", "shouldnt", "wouldnt", "couldnt", "aint",
    "will", "can", "could", "should", "would", "must", "may", "might",
}
NUMBER_WORDS = {
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty",
    "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred",
    "thousand", "million", "billion", "percent", "half", "quarter", "dozen",
}

WORD_RE = re.compile(r"\S+")
STRIP_RE = re.compile(r"^[^\w$%]+|[^\w$%]+$")

# A stretch this long missing from a source is absent coverage, not a reading.
COVERAGE_GAP_WORDS = 8
# Only genuinely overlapping divergences become one site. Merging neighbours is
# tempting for readability but it destroys voting: two unrelated garbles a word
# apart become one span that no source agrees on, so a disagreement that would
# have resolved 2-1 lands in the review queue instead. Measured on a 9,000-word
# interview, merging across a single word doubled the sites needing judgment.
SITE_MERGE_GAP = 0


def cmp_form(token):
    return STRIP_RE.sub("", token).lower()


def load_jsonl(path):
    turns = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                turns.append(json.loads(line))
    if not turns:
        sys.exit(f"error: {path} has no turns")
    return turns


def parse_spec(spec):
    """'path.jsonl:group' -> source dict. Group defaults to the source name."""
    path, group = spec, None
    # A Windows absolute path carries its own colon ('C:/n/Otter.jsonl'), so look
    # for the group separator only in the part after any drive prefix. Guarding on
    # the whole spec made ':GROUP' unusable on Windows, which silently let two
    # exports of one engine cast two votes.
    drive = re.match(r"^[A-Za-z]:[\\/]", spec)
    tail_part = spec[drive.end():] if drive else spec
    if ":" in tail_part and not os.path.exists(spec):
        head, tail = spec.rsplit(":", 1)
        path, group = head, tail
    if not os.path.exists(path):
        sys.exit(f"error: no such file: {path}")
    turns = load_jsonl(path)
    name = turns[0].get("source") or os.path.splitext(os.path.basename(path))[0]
    return {"path": path, "name": name, "group": group or name, "turns": turns}


def build_streams(source):
    """Flatten turns into an original token stream plus a filler-free
    comparison stream, keeping an index map between them."""
    tokens, owner = [], []
    for t_idx, turn in enumerate(source["turns"]):
        for w_idx, word in enumerate(WORD_RE.findall(turn.get("text") or "")):
            tokens.append(word)
            owner.append((t_idx, w_idx))

    cmp_tokens, cmp_to_orig = [], []
    for idx, token in enumerate(tokens):
        form = cmp_form(token)
        if not form or form in FILLER:
            continue
        cmp_tokens.append(form)
        cmp_to_orig.append(idx)

    keep = [True] * len(cmp_tokens)
    for phrase in FILLER_PHRASES:
        n = len(phrase)
        for i in range(len(cmp_tokens) - n + 1):
            if tuple(cmp_tokens[i:i + n]) == phrase and all(keep[i:i + n]):
                for j in range(i, i + n):
                    keep[j] = False
    if not all(keep):
        cmp_tokens = [t for t, k in zip(cmp_tokens, keep) if k]
        cmp_to_orig = [o for o, k in zip(cmp_to_orig, keep) if k]

    source.update(tokens=tokens, owner=owner,
                  cmp_tokens=cmp_tokens, cmp_to_orig=cmp_to_orig)
    return source


def orig_range(source, c1, c2):
    """Comparison range [c1, c2) -> original token range [start, end)."""
    mapping = source["cmp_to_orig"]
    n = len(source["tokens"])
    if not mapping:
        return (0, 0)
    if c1 >= len(mapping):
        return (n, n)
    start = mapping[c1]
    if c2 <= c1:
        return (start, start)
    return (start, mapping[min(c2, len(mapping)) - 1] + 1)


def text_at(source, c1, c2):
    """The source's own words across a comparison range, filler included."""
    start, end = orig_range(source, c1, c2)
    return " ".join(source["tokens"][start:end])


def analyze(anchor, source):
    """Align one source to the anchor.

    Returns the divergences worth voting on, the long gaps where this source has
    no coverage, and the anchor range this source covers at all — a source that
    stops early must abstain past that point rather than vote for silence.
    """
    matcher = difflib.SequenceMatcher(
        None, anchor["cmp_tokens"], source["cmp_tokens"], autojunk=False)
    blocks = [b for b in matcher.get_matching_blocks() if b.size > 0]

    if blocks:
        covered = (blocks[0].a, blocks[-1].a + blocks[-1].size)
    else:
        covered = (0, 0)

    divergences, gaps = [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        # Outside this source's covered range it has nothing to say.
        if i2 <= covered[0] or i1 >= covered[1]:
            continue
        anchor_words, source_words = i2 - i1, j2 - j1
        if tag == "delete" and anchor_words >= COVERAGE_GAP_WORDS:
            gaps.append({"kind": "missing_from_source", "a1": i1, "a2": i2,
                         "words": anchor_words})
            continue
        if tag == "insert" and source_words >= COVERAGE_GAP_WORDS:
            gaps.append({"kind": "missing_from_anchor", "a1": i1, "a2": i1,
                         "j1": j1, "j2": j2, "words": source_words})
            continue
        divergences.append({"a1": i1, "a2": i2})

    source.update(matcher=matcher, blocks=blocks, covered=covered,
                  divergences=divergences, gaps=gaps)
    return source


def project(source, c1, c2):
    """Map an anchor comparison range onto this source's comparison range.

    Walks the matching blocks so the returned span is what this source has
    *at the same place in the conversation* — which is what makes variants from
    different sources comparable, and what a naive per-opcode span gets wrong.
    """
    blocks = source["blocks"]
    if not blocks:
        return None

    def map_point(a_pos, prefer_end):
        best = None
        for b in blocks:
            if b.a <= a_pos < b.a + b.size:
                return b.b + (a_pos - b.a)
            if b.a + b.size <= a_pos:
                best = b.b + b.size            # last block that ends before us
            elif best is None or not prefer_end:
                # first block starting after us
                return b.b if best is None else best
        return best if best is not None else 0

    j1 = map_point(c1, prefer_end=False)
    j2 = map_point(c2, prefer_end=True)
    if j1 is None or j2 is None:
        return None
    return (min(j1, j2), max(j1, j2))


def covers(source, c1, c2):
    lo, hi = source["covered"]
    return c1 >= lo and c2 <= hi


def merge_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals)
    merged = [list(intervals[0])]
    for start, end in intervals[1:]:
        if start <= merged[-1][1] + SITE_MERGE_GAP:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [tuple(m) for m in merged]


def categorize(texts):
    forms = set()
    for text in texts:
        for token in WORD_RE.findall(text or ""):
            forms.add(cmp_form(token))
    if any(re.search(r"\d", f) for f in forms) or (forms & NUMBER_WORDS):
        return "number"
    if forms & NEGATIONS:
        return "negation"
    for text in texts:
        tokens = WORD_RE.findall(text or "")
        if any(re.match(r"^[A-Z][a-z]", t) for t in tokens):
            return "entity"
    return "wording"


def variant_key(text):
    return " ".join(cmp_form(t) for t in WORD_RE.findall(text or "")).strip()


def sound_key(text):
    """Crude phonetic key: enough to tell 'volumes' from 'volume is' apart from
    'compliance' vs 'finance'. Collapses plurals, doubled letters, silent
    endings and the consonant confusions transcribers actually make."""
    s = re.sub(r"[^a-z]", "", (text or "").lower())
    if not s:
        return ""
    s = re.sub(r"(?:ph)", "f", s)
    s = re.sub(r"(?:ck|q|kh)", "k", s)
    s = re.sub(r"(?:z|s)+", "s", s)
    s = re.sub(r"(?:sh|ch|j)", "x", s)
    s = re.sub(r"(?:v|w)", "v", s)
    s = re.sub(r"[hy]", "", s)
    s = re.sub(r"(.)\1+", r"\1", s)
    s = re.sub(r"(?:e|ing|ed)$", "", s)
    return s


def skeleton(word):
    """First letter plus consonants, for comparing garbles of one term.
    'lithotripsy' and 'lithovripsy' differ in one character here."""
    s = sound_key(word)
    return (s[:1] + re.sub(r"[aeiou]", "", s[1:])) if s else ""


def cluster_terms(sites, threshold=0.78, min_key=4):
    """Group judgment sites by the term they are mangling.

    One domain word garbled four ways consumes four judgment slots and needs one
    glossary entry, not four resolutions. On a real interview 'lithotripsy'
    appeared as 'lithovripsy', 'lithtripsy', 'lithotropy' and 'lithovy'. Andrew's
    rules already say to prefer the glossary over per-site fixes; this is what
    makes that visible before the decisions are written.
    """
    clusters = []
    for site in sites:
        words = []
        for variant in site.get("variants", []):
            words += [w for w in re.findall(r"[A-Za-z]{5,}", variant.get("text") or "")]
        if not words:
            continue
        term = max(words, key=len)
        key = skeleton(term)
        # A short skeleton matches almost anything, which merged 'laser', 'speed'
        # and 'value' into one cluster on the first attempt.
        if len(key) < min_key:
            continue
        best, best_ratio = None, 0.0
        for cluster in clusters:
            ratio = difflib.SequenceMatcher(None, key, cluster["key"]).ratio()
            if ratio > best_ratio:
                best, best_ratio = cluster, ratio
        if best is not None and best_ratio >= threshold:
            best["sites"].append(site["id"])
            best["spellings"].add(term)
        else:
            clusters.append({"key": key, "sites": [site["id"]],
                             "spellings": {term}})
    # A cluster is only interesting if the term is spelled differently across
    # sites. The same word appearing in several unrelated disputes ('product',
    # 'products') is not one garble and one glossary entry will not settle it.
    def distinct(spellings):
        return {re.sub(r"s$", "", w.lower()) for w in spellings}

    out = [{"term_key": c["key"], "sites": sorted(c["sites"]),
            "count": len(c["sites"]),
            "spellings": sorted(c["spellings"])[:8]}
           for c in clusters
           if len(c["sites"]) > 1 and len(distinct(c["spellings"])) > 1]
    return sorted(out, key=lambda c: -c["count"])


def resolve(site, anchor, sources, groups):
    """Vote on a site, or send it to judgment. Returns (kind, record, text)."""
    c1, c2 = site
    anchor_text = text_at(anchor, c1, c2)

    variants = OrderedDict()
    variants[anchor["name"]] = anchor_text
    abstained = []
    for source in sources:
        if not covers(source, c1, c2):
            abstained.append(source["name"])
            continue
        span = project(source, c1, c2)
        variants[source["name"]] = "" if span is None else text_at(source, *span)

    # One vote per group; within a group, its own majority reading.
    per_group = OrderedDict()
    for name, text in variants.items():
        per_group.setdefault(groups[name], Counter())[variant_key(text)] += 1

    tally, representative = Counter(), {}
    for group, counter in per_group.items():
        key = counter.most_common(1)[0][0]
        tally[key] += 1
        if key not in representative:
            representative[key] = next(
                t for n, t in variants.items()
                if groups[n] == group and variant_key(t) == key)

    orig_start, orig_end = orig_range(anchor, c1, c2)
    turn_idx = anchor["owner"][orig_start][0] if orig_start < len(anchor["owner"]) \
        else (len(anchor["turns"]) - 1)
    record = {
        "time": anchor["turns"][turn_idx].get("start", ""),
        "turn": turn_idx,
        "c1": c1, "c2": c2,
        "anchor_start": orig_start, "anchor_end": orig_end,
        "category": categorize(list(variants.values())),
        "variants": [{"source": n, "text": t} for n, t in variants.items()],
        "tally": {representative.get(k, k) or "(nothing)": v
                  for k, v in tally.items()},
    }
    if abstained:
        record["no_coverage"] = abstained

    speaking = Counter({k: v for k, v in tally.items() if k})
    silent = tally.get("", 0)

    if not speaking:
        return "keep", record, anchor_text

    speaking_texts = [representative.get(k, k) for k in speaking]
    ranked = speaking.most_common()
    top_key, top_votes = ranked[0]
    runner_up = ranked[1][1] if len(ranked) > 1 else 0
    chosen = representative.get(top_key, top_key)

    if len(speaking) == 1:
        if silent:
            record["note"] = (f"{silent} source(s) drop this; the sources that "
                              f"have it agree, so it is kept.")
            return "coverage", record, chosen
        return "keep", record, chosen

    if top_votes > runner_up:
        record["resolution"] = chosen
        record["margin"] = f"{top_votes}-{runner_up}"
        return "vote", record, chosen

    return "judgment", record, chosen


def filler_candidates(anchor):
    """Flag likely filler for adjudication. High recall on purpose — nothing is
    removed here, because whether a hedge carries meaning needs a decision."""
    tokens = anchor["tokens"]
    forms = [cmp_form(t) for t in tokens]
    out = []

    def context(idx, span=1):
        lo, hi = max(0, idx - 7), min(len(tokens), idx + span + 7)
        return " ".join(tokens[lo:hi])

    def add(kind, start, end):
        out.append({"kind": kind, "start": start, "end": end,
                    "text": " ".join(tokens[start:end]),
                    "turn": anchor["owner"][start][0],
                    "time": anchor["turns"][anchor["owner"][start][0]].get("start", ""),
                    "context": context(start, end - start)})

    for idx, form in enumerate(forms):
        if form in FILLER:
            add("filler_word", idx, idx + 1)
    for phrase in FILLER_PHRASES:
        n = len(phrase)
        for idx in range(len(forms) - n + 1):
            if tuple(forms[idx:idx + n]) == phrase:
                add("hedge" if phrase in (("i", "think"), ("i", "guess"))
                    else "filler_phrase", idx, idx + n)
    for idx in range(1, len(forms)):
        if forms[idx] and forms[idx] == forms[idx - 1]:
            add("repeat", idx - 1, idx + 1)
    for idx in range(2, len(forms) - 1):
        if forms[idx:idx + 2] == forms[idx - 2:idx] and all(forms[idx:idx + 2]):
            add("restart", idx - 2, idx + 2)
    for idx, token in enumerate(tokens):
        if len(token) > 1 and re.search(r"[-–—]{1,2}$", token):
            add("false_start", idx, idx + 1)

    out.sort(key=lambda c: (c["start"], c["end"]))
    for i, cand in enumerate(out, 1):
        cand["id"] = i
    return out


def group_filler(candidates):
    """Collapse candidates into decidable groups.

    An hour of speech throws up hundreds of candidates but only a dozen or so
    distinct ones — sixty "um"s are one decision, not sixty. Grouping keeps the
    judgment with the reader while making it cheap to exercise; a group whose
    instances genuinely differ can be itemised on request.
    """
    groups = OrderedDict()
    for cand in candidates:
        key = "%s:%s" % (cand["kind"], cmp_form(cand["text"]).lower())
        group = groups.setdefault(key, {
            "key": key, "kind": cand["kind"],
            "text": cmp_form(cand["text"]),
            "count": 0, "ids": [], "samples": [],
        })
        group["count"] += 1
        group["ids"].append(cand["id"])
        if len(group["samples"]) < 3:
            group["samples"].append(cand["context"])
    # Context-dependent kinds first: those are where a per-instance look pays off.
    order = {"false_start": 0, "restart": 1, "hedge": 2, "repeat": 3,
             "filler_phrase": 4, "filler_word": 5}
    return sorted(groups.values(),
                  key=lambda g: (order.get(g["kind"], 9), -g["count"]))


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--anchor", required=True,
                    help="normalized .jsonl of the timing anchor, or PATH:GROUP")
    ap.add_argument("--source", action="append", default=[],
                    help="another normalized .jsonl, or PATH:GROUP (repeatable)")
    ap.add_argument("--out", required=True, help="output alignment.json")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    anchor = build_streams(parse_spec(args.anchor))
    sources = [analyze(anchor, build_streams(parse_spec(s))) for s in args.source]
    everything = [anchor] + sources
    groups = {s["name"]: s["group"] for s in everything}
    n_groups = len(set(groups.values()))

    sites = merge_intervals(
        [(d["a1"], d["a2"]) for s in sources for d in s["divergences"]])

    by_vote, judgment, coverage = [], [], []
    edits = []          # (orig_start, orig_end, replacement_text)
    site_id = 0
    for site in sites:
        kind, record, chosen = resolve(site, anchor, sources, groups)
        if kind == "keep":
            continue
        site_id += 1
        record["id"] = site_id
        if kind == "vote":
            by_vote.append(record)
            edits.append((record["anchor_start"], record["anchor_end"], chosen))
        elif kind == "coverage":
            coverage.append(record)
            edits.append((record["anchor_start"], record["anchor_end"], chosen))
        else:
            judgment.append(record)
            # Leave a placeholder rather than a decision. build_payload.py fills
            # it with whatever is decided, or with a [CONFLICT n] marker if the
            # site is left open — so nothing here presumes an outcome.
            edits.append((record["anchor_start"], record["anchor_end"],
                          "{{SITE:%d}}" % site_id))

    # Rebuild the anchor's turns with the settled edits applied, back to front so
    # that earlier offsets stay valid.
    turns_out = [{"turn": i, "time": t.get("start", ""),
                  "speaker": t.get("speaker"), "text": t.get("text", "")}
                 for i, t in enumerate(anchor["turns"])]
    words_by_turn = {i: WORD_RE.findall(t["text"]) for i, t in enumerate(turns_out)}
    skipped = crossed = overlapped = 0
    frontier = None     # lowest token index already rewritten

    for orig_start, orig_end, replacement in sorted(edits, reverse=True):
        if orig_start >= len(anchor["owner"]):
            skipped += 1
            continue
        if frontier is not None and orig_end > frontier:
            # Two sites landed on the same words; rewriting both would corrupt
            # the text, so leave this one as the anchor's reading and say so.
            overlapped += 1
            skipped += 1
            continue
        t_idx, w_start = anchor["owner"][orig_start]
        last = min(orig_end, len(anchor["owner"])) - 1
        if last < orig_start or anchor["owner"][last][0] != t_idx:
            crossed += 1    # spans a turn boundary; leave the anchor's reading
            skipped += 1
            continue
        w_end = anchor["owner"][last][1] + 1
        words_by_turn[t_idx][w_start:w_end] = WORD_RE.findall(replacement)
        frontier = orig_start

    for i, turn in enumerate(turns_out):
        turn["text"] = " ".join(words_by_turn[i])

    # Any site whose placeholder didn't land would silently lose its marker.
    placed = " ".join(t["text"] for t in turns_out)
    unplaced = [s["id"] for s in judgment
                if "{{SITE:%d}}" % s["id"] not in placed]
    for site in judgment:
        if site["id"] in unplaced:
            site["unplaced"] = True

    # Content the anchor missed that another source has.
    gaps = []
    for source in sources:
        for gap in source["gaps"]:
            if gap["kind"] != "missing_from_anchor":
                continue
            orig_pos, _ = orig_range(anchor, gap["a1"], gap["a1"])
            t_idx = anchor["owner"][min(orig_pos, len(anchor["owner"]) - 1)][0] \
                if anchor["owner"] else 0
            s_start, s_end = orig_range(source, gap["j1"], gap["j2"])
            gaps.append({
                "source": source["name"], "after_turn": t_idx,
                "time": anchor["turns"][t_idx].get("start", ""),
                "words": gap["words"],
                "speaker_in_source": source["turns"][
                    source["owner"][s_start][0]].get("speaker"),
                "text": " ".join(source["tokens"][s_start:s_end]),
            })

    term_clusters = cluster_terms(judgment)

    candidates = filler_candidates(anchor)
    groups_out = group_filler(candidates)

    out = {
        "anchor": anchor["name"],
        "sources": [{"name": s["name"], "group": s["group"],
                     "turns": len(s["turns"]), "words": len(s["tokens"])}
                    for s in everything],
        "independent_sources": n_groups,
        "majority_possible": n_groups >= 3,
        "turns": turns_out,
        "needs_judgment": judgment,
        "coverage_gaps": gaps,
        "kept_despite_gaps": coverage,
        "resolved_by_vote": by_vote,
        "term_clusters": term_clusters,
        "filler_candidates": candidates,
        "filler_groups": groups_out,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)

    # A second, small file holding only what has to be decided. alignment.json
    # carries the whole transcript and is meant for build_payload.py, not for
    # reading — reading it would undo the point of the split.
    review = {
        "read_me": "Decide the items below and write decisions.json "
                   "(build_payload.py --schema). Do not read alignment.json; "
                   "everything needing a decision is here. Start with "
                   "term_clusters: each one is a single word garbled several "
                   "ways, so one glossary entry settles every site it lists.",
        "term_clusters": term_clusters,
        "anchor": anchor["name"],
        "independent_sources": n_groups,
        "majority_possible": n_groups >= 3,
        "settled_without_you": {
            "by_majority_vote": len(by_vote),
            "kept_despite_missing_coverage": len(coverage),
            "of_which_consequential": sum(
                1 for v in by_vote
                if v["category"] in ("number", "negation", "entity")),
        },
        "sites": [dict(
            {
                "id": s["id"],
                "time": s["time"],
                "category": s["category"],
                "said": {v["source"]: v["text"] for v in s["variants"] if v["text"]},
                "no_coverage": s.get("no_coverage", []),
            },
            # Neighbouring sites are often one garbled phrase split in two.
            # Decide them together or the halves can disagree with each other.
            **({"adjacent_to": [o["id"] for o in judgment
                                if o["id"] != s["id"]
                                and abs(o["c1"] - s["c1"]) <= 4]}
               if any(o["id"] != s["id"] and abs(o["c1"] - s["c1"]) <= 4
                      for o in judgment) else {})
        ) for s in judgment],
        "coverage_gaps": [{
            "id": i, "time": g["time"], "source": g["source"],
            "words": g["words"], "speaker_in_source": g["speaker_in_source"],
            "text": g["text"],
        } for i, g in enumerate(gaps)],
        "filler_groups": [{
            "key": g["key"], "kind": g["kind"], "text": g["text"],
            "count": g["count"], "samples": g["samples"],
        } for g in groups_out],
    }
    base = args.out[:-5] if args.out.endswith(".json") else args.out
    review_path = base + ".review.json"
    with open(review_path, "w", encoding="utf-8") as fh:
        json.dump(review, fh, ensure_ascii=False, indent=1)

    if not args.quiet:
        total = len(anchor["tokens"])
        to_read = sum(len(WORD_RE.findall(v["text"]))
                      for s in judgment for v in s["variants"])
        to_read += sum(g["words"] for g in gaps)
        print(f"wrote {args.out}")
        print(f"  anchor:               {anchor['name']} "
              f"({len(anchor['turns'])} turns, {total} words)")
        print(f"  independent sources:  {n_groups}"
              + ("" if n_groups >= 3
                 else "   (no majority possible; ties go to judgment)"))
        print(f"  divergence sites:     {site_id}")
        print(f"    settled by vote:    {len(by_vote)}")
        print(f"    kept despite gaps:  {len(coverage)}")
        cats = Counter(s["category"] for s in judgment)
        print(f"    need judgment:      {len(judgment)}"
              + (f"   ({', '.join(f'{n} {c}' for c, n in cats.most_common())})"
                 if judgment else ""))
        if term_clusters:
            covered = sum(c["count"] for c in term_clusters)
            print(f"    of those, {covered} sites are {len(term_clusters)} term(s) "
                  f"garbled repeatedly — one glossary entry each")
        print(f"  coverage gaps:        {len(gaps)}")
        print(f"  filler candidates:    {len(candidates)} "
              f"in {len(groups_out)} groups")
        if crossed:
            print(f"  NOTE: {crossed} site(s) crossed a turn boundary and were "
                  f"left as the anchor's reading")
        if overlapped:
            print(f"  NOTE: {overlapped} overlapping site(s) were left as the "
                  f"anchor's reading")
        if unplaced:
            print(f"  WARNING: sites {unplaced} could not be marked in the text; "
                  f"decide them from {review_path} and place them by hand")
        if total:
            print(f"  words to adjudicate:  ~{to_read} of {total} "
                  f"({to_read * 100.0 / total:.1f}%)")
        print(f"  review file:          {review_path}  "
              f"({os.path.getsize(review_path) // 1024} KB — read this one, "
              f"not {os.path.basename(args.out)})")


if __name__ == "__main__":
    main()
