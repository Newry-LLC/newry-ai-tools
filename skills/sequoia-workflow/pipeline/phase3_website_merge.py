"""Phase 2 correction pass — merge website-confirmed partner findings.

Phase 2's AI partner-check only read cached ADV brochures. Jack's rule says
partners can also come from the firm's *website* — this pass fixes that gap
by merging in a second research round (ZoomInfo + WebFetch per firm) that
specifically re-checked every firm's website for explicit "Partner" titles.

Reads data/phase3_website_partner_findings.json and applies three kinds of
change to data/people/{crd}.json:
  1. partner_upgrades   — an existing person, now confirmed as an explicit
     "Partner" by the website (wasn't caught by the brochure-only pass).
  2. new_partners_to_add — a person not previously in the people list,
     explicitly titled Partner on the website. Added, then the whole list
     is re-ranked and re-capped at 5 (may bump a lower-seniority owner).
  3. unresolved_entity_leads / data_quality_flags — recorded as notes, not
     treated as confirmed facts (no fabrication).

Usage:
  python phase3_website_merge.py
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


def name_key(name):
    return re.sub(r"[^a-z]", "", name.lower())


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
    findings = json.loads((DATA / "phase3_website_partner_findings.json").read_text(encoding="utf-8"))

    report = {"upgrades_applied": [], "new_partners_added": [], "firms_changed": set(),
              "leads_recorded": 0, "flags_recorded": 0}

    # --- 1. partner upgrades on existing people ---
    for u in findings["partner_upgrades"]:
        crd = u["crd"]
        path = PEOPLE / f"{crd}.json"
        d = json.loads(path.read_text(encoding="utf-8"))
        hit = None
        for p in d["people"]:
            if u["name_match"].lower() in name_key(p["name"]):
                hit = p
                break
        if not hit:
            report.setdefault("upgrade_misses", []).append(u)
            continue
        if not hit.get("is_partner_mention"):
            hit["is_partner_mention"] = True
            hit["partner_title_phrase"] = u["title"]
            hit["partner_quote"] = u["quote"]
            hit["partner_source"] = u["source"]
            report["upgrades_applied"].append({"crd": crd, "name": hit["name"], "title": u["title"]})
            report["firms_changed"].add(crd)
        path.write_text(json.dumps(d, indent=2), encoding="utf-8")

    # --- 2. new partners not previously in the list ---
    by_crd = {}
    for np in findings["new_partners_to_add"]:
        by_crd.setdefault(np["crd"], []).append(np)

    for crd, new_people in by_crd.items():
        path = PEOPLE / f"{crd}.json"
        d = json.loads(path.read_text(encoding="utf-8"))
        # people[] holds the capped top-5; recover anyone dropped for cap too,
        # so re-ranking considers the full pool, not just the current 5
        full_pool = list(d["people"])
        # dropped_for_cap only stored names, not full records, in phase2 output —
        # if present we keep them out of scope here since we lack their full
        # data; capping already treated them as lower seniority than the top 5.
        for np in new_people:
            full_pool.append({
                "raw_name": np["name"],
                "name": np["name"],
                "source": np["source"],
                "confidence": np["confidence"],
                "title_or_status": np["title"],
                "is_equity_owner": False,
                "ownership_pct": "",
                "control_person": False,
                "since": "",
                "crd": None,
                "is_partner_mention": True,
                "partner_title_phrase": np["title"],
                "partner_quote": "",
                "partner_source": np["source"],
            })
            report["new_partners_added"].append({"crd": crd, "name": np["name"], "title": np["title"]})
            report["firms_changed"].add(crd)

        for p in full_pool:
            p["seniority_score"] = seniority_score(p)
        full_pool.sort(key=lambda p: -p["seniority_score"])

        capped = full_pool[:5]
        dropped = full_pool[5:]
        d["people"] = capped
        d["capped_from"] = len(full_pool) if len(full_pool) > 5 else d.get("capped_from")
        d["dropped_for_cap"] = [p["name"] for p in dropped]
        path.write_text(json.dumps(d, indent=2), encoding="utf-8")

    # --- 3. unresolved entity leads + data quality flags (notes only) ---
    for lead in findings["unresolved_entity_leads"]:
        if lead["confidence"] == "none":
            continue  # nothing to record — no lead was actually found
        crd = lead["crd"]
        path = PEOPLE / f"{crd}.json"
        d = json.loads(path.read_text(encoding="utf-8"))
        for uo in d.get("unresolved_entity_owners", []):
            if uo["entity_name"].upper() in lead["entity"].upper() or lead["entity"].upper() in uo["entity_name"].upper():
                uo["website_zoominfo_lead"] = {"note": lead["lead"], "confidence": lead["confidence"]}
                report["leads_recorded"] += 1
        path.write_text(json.dumps(d, indent=2), encoding="utf-8")

    for flag in findings["data_quality_flags"]:
        crd = flag["crd"]
        path = PEOPLE / f"{crd}.json"
        d = json.loads(path.read_text(encoding="utf-8"))
        d.setdefault("data_quality_flags", []).append(flag["flag"])
        path.write_text(json.dumps(d, indent=2), encoding="utf-8")
        report["flags_recorded"] += 1

    report["firms_changed"] = sorted(report["firms_changed"])
    (DATA / "phase3_website_merge_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Partner-status upgrades applied: {len(report['upgrades_applied'])}")
    for u in report["upgrades_applied"]:
        print(f"  {u['crd']}: {u['name']} -> {u['title']}")
    print(f"\nBrand-new partners added:        {len(report['new_partners_added'])}")
    for n in report["new_partners_added"]:
        print(f"  {n['crd']}: {n['name']} -> {n['title']}")
    print(f"\nFirms changed:                   {len(report['firms_changed'])}")
    print(f"Unresolved-entity leads recorded: {report['leads_recorded']}")
    print(f"Data quality flags recorded:      {report['flags_recorded']}")
    if report.get("upgrade_misses"):
        print(f"\nWARNING - upgrade name matches failed: {len(report['upgrade_misses'])}")
        for m in report["upgrade_misses"]:
            print(f"  {m}")


if __name__ == "__main__":
    main()
