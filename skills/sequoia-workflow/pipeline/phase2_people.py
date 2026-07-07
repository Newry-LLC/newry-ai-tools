"""Phase 2 — merged people-set (deterministic legal-owner half only).

Per Jack (confirmed via Slack, 2026-07-02): the outreach "people" list per
firm = equity owners + all partners (a partner counts even with no equity;
"partner" is a description found in Part 2B brochure supplements / the
firm's website, not a filed title). Cap: the merged list at 5 people,
ranked by seniority, if it would otherwise run longer.

This script builds the DETERMINISTIC half only — legal owners straight off
Form ADV Schedule A (direct) + Schedule B (indirect, resolved to the entity
they sit behind). It also scans cached brochures for the word "partner" and
writes a worklist of which firms need the AI-bounded partner-extraction step
(phase2_partners_merge.py, run after the Agent fan-out).

Usage:
  python phase2_people.py
"""

import json
import re
from pathlib import Path

from pypdf import PdfReader

DATA = Path(__file__).parent / "data"
ADV = DATA / "adv"
PEOPLE = DATA / "people"


def normalize_name(raw):
    """'LAST, FIRST, MIDDLE' (SEC filing order, any case) -> 'First Middle Last'.

    Kept alongside the raw filed string in every record — never used as the
    only copy of the name — so a normalization slip is visible, not silent.
    """
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if len(parts) >= 2:
        last = parts[0]
        rest = parts[1:]
        ordered = rest + [last]
    else:
        ordered = raw.split()
    return " ".join(w.capitalize() if w.isupper() or w.islower() else w for w in ordered)


def load_schedule(crd, name):
    p = ADV / crd / name
    if not p.exists():
        return {"status": "missing", "owners": []}
    return json.loads(p.read_text(encoding="utf-8"))


def resolve_entity_owner(entity_name, indirect_individuals):
    """Match a Schedule A entity owner to its Schedule B indirect owner(s).

    Schedule B's free-text "entity in which interest is owned" + "status"
    columns are stored combined (no reliable machine split — see
    phase1_adv.parse_schedule_b) under title_or_status, and in practice the
    entity name is always a leading substring of that combined text, e.g.
    "ANDREW BRINKMAN HOLDINGS LLC MANAGING MEMBER". Matching on
    startswith(entity_name) is therefore reliable without over-claiming a
    split we can't actually parse.
    """
    matches = []
    for ind in indirect_individuals:
        if ind["title_or_status"].upper().startswith(entity_name.upper()):
            matches.append(ind)
    return matches


def brochure_text(crd):
    """Concatenate every cached brochure PDF for a firm into one text blob.

    Unlike the ADV filing-history PDFs (see phase1_adv.schedule_section_text),
    brochures are ordinary single documents — page lengths don't grow
    cumulatively — so a plain page join is safe here.
    """
    out = []
    for pdf_path in sorted((ADV / crd).glob("brochure_*.pdf")):
        try:
            reader = PdfReader(str(pdf_path))
            out.append("\n".join((p.extract_text() or "") for p in reader.pages))
        except Exception as e:
            out.append(f"[[unreadable brochure {pdf_path.name}: {e}]]")
    return "\n\n----- next brochure -----\n\n".join(out)


def build_legal_owners(crd, name):
    sched_a = load_schedule(crd, "schedule_a.json")
    sched_b = load_schedule(crd, "schedule_b.json")

    direct_individuals = [o for o in sched_a["owners"] if o["entity_type"] == "I"]
    entity_owners = [o for o in sched_a["owners"] if o["entity_type"] in ("DE", "FE")]
    indirect_individuals = [o for o in sched_b["owners"] if o["entity_type"] == "I"]

    people = []
    for o in direct_individuals:
        people.append({
            "raw_name": o["full_legal_name"],
            "name": normalize_name(o["full_legal_name"]),
            "source": "Form ADV Schedule A (direct owner)",
            "confidence": "high",
            "title_or_status": o["title_or_status"],
            "is_equity_owner": True,
            "ownership_pct": o["ownership_pct"],
            "control_person": o["control_person"],
            "since": o["since"],
            "crd": o["crd"],
            "is_partner_mention": False,
        })

    unresolved_entities = []
    matched_indirect_crds = set()
    for e in entity_owners:
        matches = resolve_entity_owner(e["full_legal_name"], indirect_individuals)
        if not matches:
            unresolved_entities.append({
                "entity_name": e["full_legal_name"],
                "ownership_pct": e["ownership_pct"],
                "control_person": e["control_person"],
                "reason": "no_schedule_b_match" if sched_b["owners"] else sched_b["status"],
            })
            continue
        for ind in matches:
            matched_indirect_crds.add(ind["crd"])
            people.append({
                "raw_name": ind["full_legal_name"],
                "name": normalize_name(ind["full_legal_name"]),
                "source": f"Form ADV Schedule B (indirect owner of {e['full_legal_name']})",
                "confidence": "high",
                "title_or_status": ind["title_or_status"],
                "is_equity_owner": True,
                "ownership_pct": e["ownership_pct"],  # the equity stake flows through the entity
                "control_person": ind["control_person"] or e["control_person"],
                "since": ind["since"],
                "crd": ind["crd"],
                "is_partner_mention": False,
            })

    # Indirect individuals not tied to any Schedule A entity we parsed
    # (shouldn't happen given Schedule B always references a Schedule A
    # row, but don't silently drop a filed owner if it does).
    for ind in indirect_individuals:
        if ind["crd"] not in matched_indirect_crds:
            people.append({
                "raw_name": ind["full_legal_name"],
                "name": normalize_name(ind["full_legal_name"]),
                "source": "Form ADV Schedule B (indirect owner, entity unmatched)",
                "confidence": "medium",
                "title_or_status": ind["title_or_status"],
                "is_equity_owner": True,
                "ownership_pct": ind["ownership_pct"],
                "control_person": ind["control_person"],
                "since": ind["since"],
                "crd": ind["crd"],
                "is_partner_mention": False,
            })

    return people, unresolved_entities


def main():
    firms = json.loads((DATA / "firms.json").read_text(encoding="utf-8"))["firms"]
    PEOPLE.mkdir(parents=True, exist_ok=True)

    needs_ai = []
    report = {"firms": []}

    for firm in firms:
        crd, name = firm["firm_crd"], firm["name"]
        people, unresolved = build_legal_owners(crd, name)

        text = brochure_text(crd)
        text_path = ADV / crd / "brochure_text.txt"
        text_path.write_text(text, encoding="utf-8")
        mentions = len(re.findall(r"partner", text, re.I))

        firm_record = {
            "crd": crd,
            "name": name,
            "website": firm.get("website"),
            "legal_owner_count": len(people),
            "unresolved_entity_owners": unresolved,
            "brochure_partner_mentions": mentions,
        }
        report["firms"].append(firm_record)

        (PEOPLE / f"{crd}_legal_owners.json").write_text(
            json.dumps({"crd": crd, "name": name, "legal_owners": people,
                        "unresolved_entity_owners": unresolved}, indent=2),
            encoding="utf-8",
        )

        if mentions:
            needs_ai.append({
                "crd": crd, "name": name, "website": firm.get("website"),
                "brochure_text_path": str(text_path), "mention_count": mentions,
            })

    report["total_firms"] = len(firms)
    report["total_legal_owners"] = sum(f["legal_owner_count"] for f in report["firms"])
    report["firms_with_unresolved_entities"] = sum(
        1 for f in report["firms"] if f["unresolved_entity_owners"]
    )
    report["firms_needing_ai_partner_check"] = len(needs_ai)
    (DATA / "phase2_needs_ai.json").write_text(json.dumps(needs_ai, indent=2), encoding="utf-8")
    (DATA / "phase2_legal_owners_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Firms processed:              {report['total_firms']}")
    print(f"Total legal owners (A+B):     {report['total_legal_owners']}")
    print(f"Firms w/ unresolved entities:  {report['firms_with_unresolved_entities']}")
    print(f"Firms needing AI partner check: {report['firms_needing_ai_partner_check']}")
    for f in report["firms"]:
        if f["unresolved_entity_owners"]:
            print(f"  UNRESOLVED: {f['name']} ({f['crd']}) -> {f['unresolved_entity_owners']}")


if __name__ == "__main__":
    main()
