"""Phase 1 — SEC ADV pull (deterministic, no LLM).

For every firm in data/firms.json, fetches from adviserinfo.sec.gov:
  1. Firm IAPD profile JSON            -> data/adv/{crd}/firm.json
  2. Full Form ADV PDF                 -> data/adv/{crd}/adv.pdf
  3. Schedule A parsed from the PDF    -> data/adv/{crd}/schedule_a.json
  4. Part 2 brochure PDFs              -> data/adv/{crd}/brochure_{versionId}.pdf
  5. Individual owner IAPD profiles    -> data/adv/{crd}/owner_{ownerCrd}.json
     (employment history, exams, disclosure flags — for owners listed in
      Schedule A with a CRD number)

Owner names come from Schedule A — a required SEC disclosure — never from
web search. Coverage report written to data/phase1_report.json.

Resumable: existing files are not re-fetched. Usage:
  python phase1_adv.py [--limit N] [--crd 131458] [--force]
"""

import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

from pypdf import PdfReader

DATA = Path(__file__).parent / "data"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"  # files host 404s on non-browser UAs
DELAY = 0.35  # seconds between HTTP requests — be polite to SEC

FIRM_JSON_URL = "https://api.adviserinfo.sec.gov/search/firm/{crd}"
INDIVIDUAL_URL = "https://api.adviserinfo.sec.gov/search/individual/{crd}"
ADV_PDF_URL = "https://reports.adviserinfo.sec.gov/reports/ADV/{crd}/PDF/{crd}.pdf"
BROCHURE_URL = (
    "https://files.adviserinfo.sec.gov/IAPD/Content/Common/"
    "crd_iapd_Brochure.aspx?BRCHR_VRSN_ID={vid}"
)

OWNERSHIP_CODES = {
    "NA": "<5%", "A": "5-10%", "B": "10-25%",
    "C": "25-50%", "D": "50-75%", "E": "75%+",
}


def fetch(url, dest=None, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    time.sleep(DELAY)
    if dest:
        dest.write_bytes(data)
    return data if binary else data.decode("utf-8", errors="replace")


def iapd_content(raw_json):
    """Unwrap the iacontent envelope of an IAPD search response."""
    doc = json.loads(raw_json)
    hits = doc.get("hits", {}).get("hits", [])
    if not hits:
        return None
    return json.loads(hits[0]["_source"]["iacontent"])


# --- Schedule A / B parsing --------------------------------------------------

# BUG FIX (2026-07-02): the SEC's rendered ADV PDF duplicates content
# cumulatively across pages — page N's extracted text is a growing superset
# of page N-1's (confirmed across every cached PDF: page lengths increase
# monotonically page-over-page, and each page is a near-prefix of the next).
# Concatenating all pages (the old approach) put several stale/incomplete
# copies of Schedule A/B ahead of the real one in the string, so `text.find()`
# could latch onto a truncated copy — e.g. Stableford Capital's Schedule A
# was undercounted 1/3 rows this way. The LAST page alone is the complete,
# de-duplicated document text.
# The trailing CRD/SSN/EIN column is frequently BLANK (entities don't have
# personal SSNs, and plenty of individuals have no CRD either). Matching it
# as an optional run of digits — not a greedy "grab whatever token comes
# next" fallback — is what keeps the row boundary from bleeding into the
# next owner's name (a blank-ID row used to swallow the next row's leading
# words as a fake "raw_id", e.g. Stableford's "REHN, MARK" row lost "REHN,"
# to the previous entity-owner row and "OPR HOLDINGS LLC" vanished entirely).
ROW_END = re.compile(
    r"(\d{2}/\d{4})\s+(NA|A|B|C|D|E)\s+(Y|N)\s+(PR|Y|N)(?:\s+([0-9]{4,10}))?"
)
TYPE_SPLIT = re.compile(r"\s+(DE|FE|I)\s+")

# Schedule B rows carry an extra "Entity in Which Interest is Owned" column
# and use ownership codes C/D/E/F (no NA/A/B — those don't reach the 25%
# indirect-ownership threshold that requires disclosure).
ROW_END_B = re.compile(
    r"(\d{2}/\d{4})\s+(C|D|E|F)\s+(Y|N)\s+(PR|Y|N)(?:\s+([0-9]{4,10}))?"
)
OWNERSHIP_CODES_B = {
    "C": "25-50%", "D": "50-75%", "E": "75%+", "F": "Other (GP/trustee/elected manager)",
}


def schedule_section_text(pdf_path):
    """Return the one page whose extracted text holds the complete,
    de-duplicated Schedule A/B tables.

    The SEC's rendered ADV PDF re-emits the running document cumulatively
    page over page (page N's text is a growing superset of page N-1's) for
    as long as a given "run" of the form continues, then RESETS on trailing
    addenda (Disclosure Reporting Pages etc. — much shorter, unrelated
    content). So neither "first page" nor "always the physical last page"
    is safe: the right page is the LAST one (by index) that still contains
    the Schedule A column-header sentinel — later pages may belong to a
    different, shorter trailing section that doesn't restate ownership.
    """
    reader = PdfReader(str(pdf_path))
    texts = [(p.extract_text() or "") for p in reader.pages]
    for t in reversed(texts):
        if "FULL LEGAL NAME" in t:
            return t
    return texts[-1] if texts else ""


def _parse_owner_rows(flat, row_re, code_map, has_entity_col):
    owners = []
    cursor = 0
    for m in row_re.finditer(flat):
        head = flat[cursor:m.start()].strip()
        cursor = m.end()
        split = TYPE_SPLIT.split(head, maxsplit=1)
        if len(split) == 3:
            name, de_fe_i, rest = split[0].strip(), split[1], split[2].strip()
        else:  # couldn't split cleanly — keep raw so nothing is invented
            name, de_fe_i, rest = head, "", ""
        entity_owned, title = "", rest
        if has_entity_col and rest:
            # Schedule B: "<Entity in Which Interest is Owned> <Status>"
            # No reliable delimiter between the two free-text columns, so
            # keep the combined text under title_or_status rather than
            # guess a split point.
            entity_owned, title = "", rest
        ident = (m.group(5) or "").strip()
        owners.append({
            "full_legal_name": name,
            "entity_type": de_fe_i,
            "entity_interest_owned": entity_owned,
            "title_or_status": title,
            "since": m.group(1),
            "ownership_code": m.group(2),
            "ownership_pct": code_map.get(m.group(2), ""),
            "control_person": m.group(3) == "Y",
            "public_reporting": m.group(4) == "PR",
            "crd": ident or None,
            "raw_id": ident or None,
        })
    return owners


def parse_schedule_a(pdf_path):
    """Extract the Schedule A direct-owners table from a Form ADV PDF."""
    text = schedule_section_text(pdf_path)
    start = text.find("FULL LEGAL NAME")
    if start == -1:
        return {"status": "schedule_a_not_found", "owners": []}
    end = text.find("Schedule B", start)
    section = text[start:end if end != -1 else None]
    flat = re.sub(r"\s+", " ", section).strip()
    header = re.search(r"IRS Tax No\.? or Employer ID No\.?", flat)
    if header:
        flat = flat[header.end():].strip()

    owners = _parse_owner_rows(flat, ROW_END, OWNERSHIP_CODES, has_entity_col=False)
    return {"status": "ok" if owners else "no_rows_parsed", "owners": owners}


def parse_schedule_b(pdf_path):
    """Extract the Schedule B indirect-owners table from a Form ADV PDF.

    Schedule B is only present when Schedule A has an entity (DE/FE) owner
    that itself has a 25%+ owner one level up. Firms with only individual
    (I) Schedule A owners legitimately have no Schedule B — that is a
    correct "no indirect owners", not a parse failure.
    """
    text = schedule_section_text(pdf_path)
    start = text.find("Indirect Owners")
    if start == -1:
        return {"status": "no_schedule_b", "owners": []}
    # Section runs from the real column header (not the instructions,
    # which also say "Indirect Owners") to the next schedule / item.
    header = text.find("FULL LEGAL NAME", start)
    if header == -1:
        return {"status": "no_schedule_b", "owners": []}
    end = text.find("Schedule D", header)
    if end == -1:
        end = text.find("Schedule C", header)
    section = text[header:end if end != -1 else None]
    flat = re.sub(r"\s+", " ", section).strip()
    col_header = re.search(r"IRS Tax No\.? or Employer\s*ID No\.?", flat)
    if col_header:
        flat = flat[col_header.end():].strip()

    owners = _parse_owner_rows(flat, ROW_END_B, OWNERSHIP_CODES_B, has_entity_col=True)
    return {"status": "ok" if owners else "no_rows_parsed", "owners": owners}


# --- per-firm pull ----------------------------------------------------------

def pull_firm(firm, force=False, reparse_schedules=False):
    crd = firm["firm_crd"]
    out = DATA / "adv" / crd
    out.mkdir(parents=True, exist_ok=True)
    result = {"crd": crd, "name": firm["name"]}

    # 1. firm profile JSON
    fj = out / "firm.json"
    try:
        if force or not fj.exists():
            raw = fetch(FIRM_JSON_URL.format(crd=crd))
            content = iapd_content(raw)
            if content is None:
                result["firm_json"] = "no_iapd_record"
            else:
                fj.write_text(json.dumps(content, indent=2), encoding="utf-8")
                result["firm_json"] = "ok"
        else:
            result["firm_json"] = "cached"
    except Exception as e:
        result["firm_json"] = f"error: {e}"

    # 2. full ADV PDF
    pdf = out / "adv.pdf"
    try:
        if force or not pdf.exists():
            fetch(ADV_PDF_URL.format(crd=crd), dest=pdf, binary=True)
        result["adv_pdf"] = "ok" if pdf.exists() and pdf.stat().st_size > 10000 else "too_small"
    except Exception as e:
        result["adv_pdf"] = f"error: {e}"

    # 3. Schedule A + B
    sa = out / "schedule_a.json"
    sb = out / "schedule_b.json"
    redo = force or reparse_schedules
    try:
        if (redo or not sa.exists()) and pdf.exists():
            parsed_a = parse_schedule_a(pdf)
            sa.write_text(json.dumps(parsed_a, indent=2), encoding="utf-8")
        parsed_a = json.loads(sa.read_text(encoding="utf-8")) if sa.exists() else {"owners": []}
        result["schedule_a"] = parsed_a.get("status", "missing")
        result["owner_count"] = len(parsed_a.get("owners", []))

        if (redo or not sb.exists()) and pdf.exists():
            parsed_b = parse_schedule_b(pdf)
            sb.write_text(json.dumps(parsed_b, indent=2), encoding="utf-8")
        parsed_b = json.loads(sb.read_text(encoding="utf-8")) if sb.exists() else {"owners": []}
        result["schedule_b"] = parsed_b.get("status", "missing")
        result["indirect_owner_count"] = len(parsed_b.get("owners", []))

        result["individual_owners"] = [
            o for o in parsed_a.get("owners", []) + parsed_b.get("owners", [])
            if o["entity_type"] == "I"
        ]
    except Exception as e:
        result["schedule_a"] = f"error: {e}"
        result["individual_owners"] = []

    # 4. brochures
    result["brochures"] = 0
    try:
        if fj.exists():
            content = json.loads(fj.read_text(encoding="utf-8"))
            details = (content.get("brochures") or {}).get("brochuredetails") or []
            for b in details:
                vid = b.get("brochureVersionID")
                if not vid:
                    continue
                bp = out / f"brochure_{vid}.pdf"
                if force or not bp.exists():
                    data = fetch(BROCHURE_URL.format(vid=vid), dest=bp, binary=True)
                    if len(data) < 5000:  # error page, not a PDF
                        bp.unlink(missing_ok=True)
                        continue
                result["brochures"] += 1
    except Exception as e:
        result["brochures_error"] = str(e)

    # 5. individual owner profiles (career history / exams / disclosures)
    result["owner_profiles"] = 0
    for o in result.get("individual_owners", []):
        if not o.get("crd"):
            continue
        op = out / f"owner_{o['crd']}.json"
        try:
            if force or not op.exists():
                raw = fetch(INDIVIDUAL_URL.format(crd=o["crd"]))
                content = iapd_content(raw)
                if content is None:
                    continue
                op.write_text(json.dumps(content, indent=2), encoding="utf-8")
            result["owner_profiles"] += 1
        except Exception:
            pass

    result.pop("individual_owners", None)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--crd", default=None, help="pull a single firm by CRD")
    ap.add_argument("--force", action="store_true", help="re-fetch cached files")
    ap.add_argument(
        "--reparse-schedules", action="store_true",
        help="re-parse schedule_a/schedule_b from the cached PDF without re-fetching anything over the network",
    )
    args = ap.parse_args()

    firms = json.loads((DATA / "firms.json").read_text(encoding="utf-8"))["firms"]
    if args.crd:
        firms = [f for f in firms if f["firm_crd"] == args.crd]
    if args.limit:
        firms = firms[: args.limit]
    if not firms:
        sys.exit("no firms matched")

    results = []
    for i, firm in enumerate(firms, 1):
        r = pull_firm(firm, force=args.force, reparse_schedules=args.reparse_schedules)
        results.append(r)
        print(
            f"[{i}/{len(firms)}] {r['name'][:45]:45} "
            f"adv={r.get('adv_pdf','-'):4} schedA={r.get('schedule_a','-'):14} "
            f"ownersA={r.get('owner_count',0)} schedB={r.get('schedule_b','-'):14} "
            f"ownersB={r.get('indirect_owner_count',0)} profiles={r.get('owner_profiles',0)} "
            f"brochures={r.get('brochures',0)}"
        )

    report = {
        "firms_pulled": len(results),
        "adv_ok": sum(1 for r in results if r.get("adv_pdf") == "ok"),
        "schedule_a_ok": sum(1 for r in results if r.get("schedule_a") == "ok"),
        "schedule_b_ok": sum(1 for r in results if r.get("schedule_b") == "ok"),
        "total_owners": sum(r.get("owner_count", 0) for r in results),
        "total_indirect_owners": sum(r.get("indirect_owner_count", 0) for r in results),
        "total_owner_profiles": sum(r.get("owner_profiles", 0) for r in results),
        "total_brochures": sum(r.get("brochures", 0) for r in results),
        "problems": [r for r in results if r.get("schedule_a") not in ("ok",)
                     or r.get("adv_pdf") != "ok"],
        "results": results,
    }
    (DATA / "phase1_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print()
    print(f"ADV PDFs ok:        {report['adv_ok']}/{len(results)}")
    print(f"Schedule A parsed:  {report['schedule_a_ok']}/{len(results)}")
    print(f"Direct owners:      {report['total_owners']}")
    print(f"Schedule B parsed:  {report['schedule_b_ok']}/{len(results)}")
    print(f"Indirect owners:    {report['total_indirect_owners']}")
    print(f"Owner profiles:     {report['total_owner_profiles']}")
    print(f"Brochures cached:   {report['total_brochures']}")
    print(f"Problem firms:      {len(report['problems'])}")
    for p in report["problems"]:
        print(f"  - {p['name']} ({p['crd']}): adv={p.get('adv_pdf')} schedA={p.get('schedule_a')}")


if __name__ == "__main__":
    main()
