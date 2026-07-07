"""Phase 3 — merge enrichment (bios, firm notes) into data/people/{crd}.json.

Reads a batch findings file (e.g. data/phase3_enrichment_batch1.json) shaped:
  {"<crd>": {"firm_note": {...}, "people": {"<exact name>": {bio_note, bio_source, bio_confidence}}}}

and writes bio_note/bio_source/bio_confidence onto the matching person record
and firm_note onto the top level of data/people/{crd}.json, in place.

This exists specifically because the first enrichment pass (2026-07-02)
gathered this data via agents but never persisted it — the fix is: findings
go straight into the authoritative per-firm file, immediately, via a script
that's re-runnable and re-verifiable, not left sitting in chat output.

Usage:
  python phase3_enrichment_merge.py <batch_file.json>
"""

import json
import sys
from pathlib import Path

DATA = Path(__file__).parent / "data"
PEOPLE = DATA / "people"


def main():
    batch_file = sys.argv[1] if len(sys.argv) > 1 else "phase3_enrichment_batch1.json"
    batch = json.loads((DATA / batch_file).read_text(encoding="utf-8"))

    applied = []
    misses = []

    for crd, entry in batch.items():
        path = PEOPLE / f"{crd}.json"
        if not path.exists():
            misses.append({"crd": crd, "reason": "no people.json file"})
            continue
        d = json.loads(path.read_text(encoding="utf-8"))
        d["firm_note"] = entry["firm_note"]

        matched_names = set()
        for person in d["people"]:
            if person["name"] in entry["people"]:
                bio = entry["people"][person["name"]]
                person["bio_note"] = bio["bio_note"]
                person["bio_source"] = bio["bio_source"]
                person["bio_confidence"] = bio["bio_confidence"]
                matched_names.add(person["name"])
                applied.append({"crd": crd, "name": person["name"]})

        for name in entry["people"]:
            if name not in matched_names:
                misses.append({"crd": crd, "name": name, "reason": "no matching person in people.json"})

        path.write_text(json.dumps(d, indent=2), encoding="utf-8")

    print(f"Bios applied: {len(applied)}")
    for a in applied:
        print(f"  {a['crd']}: {a['name']}")
    print(f"Firm notes applied: {len(batch)}")
    if misses:
        print(f"\nMISSES ({len(misses)}) — did not apply, needs review:")
        for m in misses:
            print(f"  {m}")


if __name__ == "__main__":
    main()
