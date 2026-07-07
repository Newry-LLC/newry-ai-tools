"""Phase 2 (final step) — merge legal owners + AI-found partners, rank, cap.

Combines:
  - data/people/{crd}_legal_owners.json   (phase2_people.py — deterministic,
    Form ADV Schedule A/B)
  - data/phase2_ai_partners.json          (Agent fan-out over cached
    brochures, bounded to explicit "partner" language, source-cited)

per Jack's rule (Slack, 2026-07-02): outreach people = equity owners + all
partners (a partner counts even with zero equity). Cap the merged,
deduped list at 5 per firm, keeping the most senior when it runs longer.

A partner match only counts if it names a person AT the outreach firm
itself (`at_this_firm: true` in phase2_ai_partners.json) — several agent
findings surfaced people called "partner" at a *different* company (a
prior employer, an unrelated holding entity) and are excluded for that
reason, not merged in.

Usage:
  python phase2_merge.py
"""

import json
import re
from pathlib import Path

DATA = Path(__file__).parent / "data"
PEOPLE = DATA / "people"

SENIOR_TITLE_KEYWORDS = [
    "founder", "managing member", "managing partner", "president", "ceo",
    "chief executive", "chairman", "principal", "partner",
]


GENERATIONAL_SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def name_key(name):
    """Loose key for de-duplication across differently-formatted names."""
    return re.sub(r"[^a-z]", "", name.lower())


def name_tokens(name):
    words = re.findall(r"[a-zA-Z]+", name.lower())
    return [w for w in words if w not in GENERATIONAL_SUFFIXES]


def last_first_key(name):
    """(first-initial, last-name-token) — robust to middle-name spelled out
    vs abbreviated ("Robert Ralph Korljan" vs "Robert R. Korljan"), but
    NOT robust to two relatives sharing a first name (father/son "Cornelius
    ... Van Zutphen") — that case needs the title-overlap tiebreak below.
    """
    t = name_tokens(name)
    if not t:
        return None
    return (t[0][0], t[-1])


def title_overlap_score(candidate_title, ai_title_phrase, ai_quote):
    """Score how well a legal-owner's filed title matches an AI partner
    mention's title/quote text — used only to disambiguate when multiple
    legal owners share the same last_first_key (e.g. a parent and child
    with an identical first name)."""
    context = f"{ai_title_phrase} {ai_quote}".lower()
    cand = (candidate_title or "").lower()
    if not cand:
        return 0
    score = 0
    if cand in context:
        score += 10
    # common title abbreviation <-> spelled-out pairs
    expansions = {
        "cio": "chief investment officer", "ceo": "chief executive officer",
        "cco": "chief compliance officer", "cfo": "chief financial officer",
        "coo": "chief operating officer", "vp": "vice president",
    }
    cand_expanded = expansions.get(cand, cand)
    if cand_expanded in context:
        score += 8
    for word in cand.split():
        if len(word) > 2 and word in context:
            score += 1
    return score


def seniority_score(person):
    score = 0
    pct = person.get("ownership_pct") or ""
    if "75" in pct:
        score += 40
    elif "50" in pct:
        score += 30
    elif "25" in pct:
        score += 20
    elif pct:
        score += 10
    if person.get("control_person"):
        score += 15
    if person.get("is_partner_mention"):
        score += 10
    title = (person.get("title_or_status") or "").lower()
    for kw in SENIOR_TITLE_KEYWORDS:
        if kw in title:
            score += 5
            break
    return score


def main():
    ai_partners = json.loads((DATA / "phase2_ai_partners.json").read_text(encoding="utf-8"))
    legal_owner_files = sorted(PEOPLE.glob("*_legal_owners.json"))

    summary = {"firms": []}

    for f in legal_owner_files:
        d = json.loads(f.read_text(encoding="utf-8"))
        crd, name = d["crd"], d["name"]
        people = list(d["legal_owners"])

        ai_entry = ai_partners.get(crd, {"partners": []})
        matched_ai = []
        unmatched_ai = []
        used_candidate_ids = set()
        for p in ai_entry["partners"]:
            if not p.get("at_this_firm"):
                unmatched_ai.append(p)
                continue
            ai_key = last_first_key(p["name"])
            candidates = [
                person for person in people
                if last_first_key(person["name"]) == ai_key
                and id(person) not in used_candidate_ids
            ]
            hit = None
            if len(candidates) == 1:
                hit = candidates[0]
            elif len(candidates) > 1:
                # ambiguous (e.g. parent/child sharing a first name) —
                # disambiguate by matching the AI's title/quote text
                # against each candidate's filed Schedule A title
                scored = [
                    (title_overlap_score(c["title_or_status"], p["title_phrase"], p["quote"]), c)
                    for c in candidates
                ]
                scored.sort(key=lambda x: -x[0])
                if scored[0][0] > 0:
                    hit = scored[0][1]
            if hit:
                used_candidate_ids.add(id(hit))
                hit["is_partner_mention"] = True
                hit["partner_title_phrase"] = p["title_phrase"]
                hit["partner_quote"] = p["quote"]
                matched_ai.append({"ai_name": p["name"], "matched_to": hit["name"]})
            else:
                # explicitly a partner at this firm but not already in the
                # legal-owner set — a genuine non-equity partner. Add them.
                people.append({
                    "raw_name": p["name"],
                    "name": p["name"],
                    "source": "ADV Part 2B brochure (explicit \"partner\" language)",
                    "confidence": p["confidence"],
                    "title_or_status": p["title_phrase"],
                    "is_equity_owner": False,
                    "ownership_pct": "",
                    "control_person": False,
                    "since": "",
                    "crd": None,
                    "is_partner_mention": True,
                    "partner_title_phrase": p["title_phrase"],
                    "partner_quote": p["quote"],
                })

        # dedupe (defensive — Schedule A/B already dedupe internally, but a
        # person can legitimately appear via both a direct and an indirect
        # row in rare cases)
        deduped = {}
        for person in people:
            k = name_key(person["name"])
            if k in deduped:
                # keep the higher-confidence / more senior of the two
                if seniority_score(person) > seniority_score(deduped[k]):
                    deduped[k] = person
            else:
                deduped[k] = person
        people = list(deduped.values())

        for person in people:
            person["seniority_score"] = seniority_score(person)
        people.sort(key=lambda p: -p["seniority_score"])

        capped = people[:5]
        dropped = people[5:]

        out = {
            "crd": crd,
            "name": name,
            "people": capped,
            "capped_from": len(people) if len(people) > 5 else None,
            "dropped_for_cap": [p["name"] for p in dropped],
            "unresolved_entity_owners": d.get("unresolved_entity_owners", []),
            "ai_partner_matches": matched_ai,
            "ai_partner_mentions_excluded": unmatched_ai,
        }
        (PEOPLE / f"{crd}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
        f.unlink()  # superseded by the merged {crd}.json

        summary["firms"].append({
            "crd": crd, "name": name,
            "final_people_count": len(capped),
            "was_capped": len(people) > 5,
            "non_equity_partners_added": sum(
                1 for p in capped if not p["is_equity_owner"]
            ),
            "unresolved_entity_owners": len(d.get("unresolved_entity_owners", [])),
        })

    summary["total_firms"] = len(summary["firms"])
    summary["firms_capped"] = sum(1 for f in summary["firms"] if f["was_capped"])
    summary["firms_with_zero_people"] = sum(
        1 for f in summary["firms"] if f["final_people_count"] == 0
    )
    summary["total_final_people"] = sum(f["final_people_count"] for f in summary["firms"])
    summary["total_non_equity_partners_added"] = sum(
        f["non_equity_partners_added"] for f in summary["firms"]
    )
    (DATA / "phase2_report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Firms processed:                {summary['total_firms']}")
    print(f"Total people in final sets:     {summary['total_final_people']}")
    print(f"Firms capped at 5:              {summary['firms_capped']}")
    print(f"Firms with zero people:         {summary['firms_with_zero_people']}")
    print(f"Non-equity partners added (AI): {summary['total_non_equity_partners_added']}")
    for fr in summary["firms"]:
        if fr["final_people_count"] == 0:
            print(f"  ZERO PEOPLE: {fr['name']} ({fr['crd']})")
        if fr["unresolved_entity_owners"]:
            print(f"  UNRESOLVED ENTITY: {fr['name']} ({fr['crd']}) x{fr['unresolved_entity_owners']}")


if __name__ == "__main__":
    main()
