"""Phase 4A -- programmatic verification checks (no AI, deterministic).

Scans every data/people/{crd}.json record and flags:
  1. Thin bio relative to stated confidence (high/medium confidence but short bio_note)
  2. bio_source that doesn't name a specific outlet/URL (still just "web search"-style)
  3. Disciplinary/complaint/regulatory language that should never appear here
  4. Confidence/source mismatch: high confidence sourced only to the firm's own domain

Writes data/phase4_programmatic_report.json and prints a summary.
"""

import json
import re
from pathlib import Path

DATA = Path(__file__).parent / "data"
PEOPLE = DATA / "people"

THIN_THRESHOLD = {"high": 300, "medium": 200}

DISCIPLINARY_TERMS = [
    "disciplinary", "complaint", "arbitration", "sanction", "settlement",
    "enforcement action", "finra action", "sec enforcement", "lawsuit",
    "litigation", "fine of", "violation", "misconduct", "censure",
    "barred", "suspended", "revoked",
]

SOURCE_DOMAIN_RE = re.compile(r"[a-z0-9\-]+\.(com|gov|org|net|io|co)\b", re.I)


def has_named_source(source_text):
    return bool(SOURCE_DOMAIN_RE.search(source_text or ""))


def is_firm_only_source(source_text, firm_domain_hint):
    if not source_text:
        return False
    domains = SOURCE_DOMAIN_RE.findall(source_text)
    text_lower = source_text.lower()
    # crude heuristic: source mentions "firm website"/"firm's own site" and nothing else with .com
    all_domains = re.findall(r"[a-z0-9\-\.]+\.(?:com|gov|org|net|io|co)", text_lower)
    if not all_domains:
        return False
    if firm_domain_hint and all(firm_domain_hint in d for d in all_domains):
        return True
    return False


def main():
    findings = []
    total_people = 0
    stats = {"thin": 0, "vague_source": 0, "disciplinary_hit": 0, "firm_only_high_conf": 0}

    for path in sorted(PEOPLE.glob("*.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        crd = d.get("crd")
        firm_name = d.get("name", "")
        firm_note = d.get("firm_note", {})

        # check firm note too for disciplinary language
        for field_name, text in [("firm_note.text", firm_note.get("text", ""))]:
            for term in DISCIPLINARY_TERMS:
                if term in (text or "").lower():
                    findings.append({
                        "crd": crd, "firm": firm_name, "person": None,
                        "issue": "disciplinary_language", "field": field_name,
                        "detail": f"term '{term}' found in firm_note"
                    })
                    stats["disciplinary_hit"] += 1

        for p in d.get("people", []):
            total_people += 1
            name = p.get("name")
            bio_note = p.get("bio_note", "") or ""
            bio_source = p.get("bio_source", "") or ""
            conf = p.get("bio_confidence", "")

            # 1. thin bio relative to confidence
            threshold = THIN_THRESHOLD.get(conf)
            if threshold and len(bio_note) < threshold:
                findings.append({
                    "crd": crd, "firm": firm_name, "person": name,
                    "issue": "thin_bio_for_confidence",
                    "detail": f"confidence={conf} but bio_note is {len(bio_note)} chars (threshold {threshold})"
                })
                stats["thin"] += 1

            # 2. vague source (no named outlet at all)
            if conf in ("high", "medium") and not has_named_source(bio_source):
                findings.append({
                    "crd": crd, "firm": firm_name, "person": name,
                    "issue": "no_named_source",
                    "detail": f"confidence={conf} but bio_source has no identifiable outlet/URL: {bio_source[:150]!r}"
                })
                stats["vague_source"] += 1

            # 3. disciplinary language in bio
            for term in DISCIPLINARY_TERMS:
                if term in bio_note.lower() or term in bio_source.lower():
                    findings.append({
                        "crd": crd, "firm": firm_name, "person": name,
                        "issue": "disciplinary_language",
                        "detail": f"term '{term}' found in bio_note/bio_source"
                    })
                    stats["disciplinary_hit"] += 1

            # 4. high confidence but source looks firm-only
            firm_domain_hint = None
            m = re.search(r"([a-z0-9\-]+)\.com", firm_note.get("source", "").lower())
            if m:
                firm_domain_hint = m.group(1)
            if conf == "high" and is_firm_only_source(bio_source, firm_domain_hint):
                findings.append({
                    "crd": crd, "firm": firm_name, "person": name,
                    "issue": "high_confidence_firm_only_source",
                    "detail": f"bio_source appears to cite only the firm's own domain: {bio_source[:150]!r}"
                })
                stats["firm_only_high_conf"] += 1

    report = {
        "total_people_scanned": total_people,
        "total_findings": len(findings),
        "stats": stats,
        "findings": findings,
    }
    (DATA / "phase4_programmatic_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Scanned {total_people} people across {len(list(PEOPLE.glob('*.json')))} firms")
    print(f"Total findings: {len(findings)}")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    if findings:
        print("\nDetail:")
        for f in findings:
            print(f"  [{f['issue']}] {f['crd']} {f['firm']} / {f.get('person')}: {f['detail']}")


if __name__ == "__main__":
    main()
