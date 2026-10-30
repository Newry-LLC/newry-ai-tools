#!/usr/bin/env python3
"""Score an Expert Number Triangulation run against an answer key.

Usage:
  python3 score.py triangulate <workbook.xlsx> [--key answer_key_px01.json]
  python3 score.py fill        <workbook.xlsx> <filled-model.xlsx> [--key ...]
  python3 score.py compare     <workbook.xlsx> [--key ...]
  python3 score.py rerun       <round1.xlsx> <round2.xlsx> [--key ...]

Prints one line per check (PASS / FAIL / WARN) and a JSON summary on the last line.
The workbook must have been recalculated (cached values present) for value checks.
Behaviour that can't be read from files (e.g. "showed the mapping before writing")
is judged by a reviewer — see evals.json.
"""
import argparse, hashlib, json, os, re, sys
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TABS = ["Summary", "Flags", "Assumption Ranges", "Comparison", "Open Questions", "Evidence Log", "Sources"]
OQ_HEADERS = ["Priority", "Ask (expert / expert type)", "Question", "Line item(s)", "Why it matters", "Flags"]
ERRORS = ("#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A", "#NUM!", "#NULL!")

results = []
def rec(check_id, ok, msg, level="FAIL"):
    status = "PASS" if ok else level
    results.append({"id": check_id, "status": status, "msg": msg})
    print(f"{status:4}  {check_id:4}  {msg}")

def num(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    if isinstance(v, str):
        s = v.replace(",", "").replace("$", "").replace("%", "").strip()
        try:
            return float(s)
        except ValueError:
            return None
    return None

def close(a, b, tol):
    if a is None or b is None:
        return False
    if b == 0:
        return abs(a) <= tol
    return abs(a - b) / abs(b) <= tol

def close_pct(a, b, tol, percent):
    return close(a, b, tol) or (percent and a is not None and close(a * 100, b, tol))

def norm(s):
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())

def load(path):
    return openpyxl.load_workbook(path, data_only=True), openpyxl.load_workbook(path, data_only=False)

def find_header(ws, must=("ID", "Expert")):
    for r in range(1, min(ws.max_row, 15) + 1):
        vals = [str(c.value).strip() if c.value is not None else "" for c in ws[r]]
        if all(any(m.lower() == v.lower() for v in vals) for m in must):
            return r, vals
    return None, None

def col(headers, *names):
    for n in names:
        for i, h in enumerate(headers):
            if n.lower() in h.lower():
                return i
    return None

def evidence_rows(wb):
    ws = wb["Evidence Log"]
    hr, headers = find_header(ws)
    if hr is None:
        return [], {}
    idx = {
        "id": col(headers, "ID"), "expert": col(headers, "Expert"), "date": col(headers, "date"),
        "line": col(headers, "Line item"), "metric": col(headers, "Metric"),
        "low": col(headers, "Low"), "high": col(headers, "High"), "unit": col(headers, "Unit"),
        "quote": col(headers, "quote"), "conf": col(headers, "Confidence"),
        "notes": col(headers, "reason", "notes"), "basis": col(headers, "Basis"),
        "source": col(headers, "Source type", "Link"),
    }
    rows = []
    for r in ws.iter_rows(min_row=hr + 1, values_only=True):
        if not r or idx["id"] is None or r[idx["id"]] in (None, ""):
            continue
        g = lambda k: (r[idx[k]] if idx[k] is not None and idx[k] < len(r) else None)
        rows.append({k: g(k) for k in idx})
    return rows, idx

def all_fixture_text(key):
    base = os.path.join(HERE, key["fixtures"])
    chunks = []
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith((".txt", ".md")):
                chunks.append(open(os.path.join(root, f), encoding="utf-8").read())
    return norm("\n".join(chunks))

def match_number(rows, spec, tol):
    hits = []
    for row in rows:
        if spec["expert"].lower() not in str(row["expert"]).lower():
            continue
        text = f'{row["line"]} {row["metric"]}'.lower()
        if not any(k in text for k in spec["keywords"]):
            continue
        lo, hi = num(row["low"]), num(row["high"])
        p = spec.get("percent", False)
        if close_pct(lo, spec["low"], tol, p) and close_pct(hi, spec["high"], tol, p):
            hits.append(row)
    return hits

# ---------------------------------------------------------------- triangulate
def score_triangulate(wb_path, key):
    tol = key["tolerance"]
    wbv, wbf = load(wb_path)
    names = wbv.sheetnames
    rec("W1", names[0] == "Summary", f"Summary is the first tab (got {names[0]!r})")
    order = [n for n in names if n in TABS]
    rec("W2", order == TABS, f"core tabs present and in order (got {order})")
    if "Open Questions" in names:
        hr, hdr = find_header(wbv["Open Questions"], must=("Priority",))
        got = [h for h in (hdr or []) if h][:6]
        rec("W3", got == OQ_HEADERS, f"Open Questions columns exact (Interview Prep reads them): {got}")
    errs = [f"{ws.title}!{c.coordinate}" for ws in wbv.worksheets for row in ws.iter_rows() for c in row
            if isinstance(c.value, str) and c.value.strip() in ERRORS]
    rec("W4", not errs, f"no formula errors in cached values ({len(errs)} found {errs[:5]})")
    formulas = sum(1 for ws in wbf.worksheets for row in ws.iter_rows() for c in row
                   if isinstance(c.value, str) and c.value.startswith("="))
    rec("W5", formulas >= 20, f"workbook is formula-driven ({formulas} formulas)")

    rows, idx = evidence_rows(wbv)
    rec("E0", len(rows) > 0, f"Evidence Log parsed ({len(rows)} rows)")
    for spec in key["numbers"]:
        hits = match_number(rows, spec, tol)
        ok = len(hits) > 0
        msg = f'{spec["id"]} {spec["expert"]}: {spec["what"]} = {spec["low"]}-{spec["high"]}'
        if ok and spec.get("confidence_not"):
            bad = [h for h in hits if str(h["conf"]).strip() in spec["confidence_not"]]
            if bad:
                ok, msg = False, msg + f" (confidence must not be {spec['confidence_not']})"
        rec(spec["id"], ok, msg)

    # one metric per row
    packed = [r["id"] for r in rows if r["unit"] and re.search(r"\((low|high)\)", str(r["unit"]), re.I)]
    rec("E1", not packed, f"one metric per Evidence row (packed rows: {packed})")

    # quotes appear in sources
    corpus = all_fixture_text(key)
    bad_q = []
    scope = key.get("quote_scope_expert")
    for r in rows:
        q = r["quote"]
        if not q or (scope and scope.lower() not in str(r["expert"]).lower()):
            continue
        frags = [f for f in re.split(r"\.\.\.|…|\[[^\]]*\]", str(q)) if norm(f)]
        if any(norm(f) not in corpus for f in frags):
            bad_q.append(r["id"])
    rec("E2", not bad_q, f"every quote fragment found in the source files (failures: {bad_q[:10]})")

    # traps
    for t in key["traps"]:
        if "value" in t:
            hits = [r for r in rows if t["value"] in (num(r["low"]), num(r["high"]))]
            if t.get("max_rows") is not None:
                ok = len(hits) <= t["max_rows"]
            elif t.get("allowed_if_note_any"):
                ok = all(any(a in f'{r["notes"]} {r["basis"]} {r["metric"]}'.lower() for a in t["allowed_if_note_any"]) for r in hits)
            else:
                ok = not hits
            rec(t["id"], ok, f'{t["what"]} (offending rows: {[r["id"] for r in hits]})')
        else:
            hits = [r for r in rows if any(s.lower() in f'{r["source"]} {r["notes"]}'.lower() for s in t["source_text_any"])]
            rec(t["id"], not hits, f'{t["what"]} (offending rows: {[r["id"] for r in hits]})')

    # flags
    flag_text = " ".join(str(c.value) for row in wbv["Flags"].iter_rows() for c in row if c.value).lower() if "Flags" in names else ""
    for f in key["required_flags"]:
        rec(f["id"], any(a.lower() in flag_text for a in f["any"]), f'flag present: {f["what"]}')

    # normalized checks
    for n in key["normalized_checks"]:
        sheets = [wbv[s] for s in n["sheets"] if s in names]
        if "value" in n:
            found = any(close(num(c.value), n["value"], n["tol"]) for ws in sheets for row in ws.iter_rows() for c in row)
        else:
            found = any(any(l.lower() in str(c.value).lower() for l in n["label_any"]) for ws in sheets for row in ws.iter_rows() for c in row if c.value)
        rec(n["id"], found, n["what"])

    # status checks
    if "Assumption Ranges" in names:
        ar = wbv["Assumption Ranges"]
        for s in key["status_checks"]:
            got = None
            for row in ar.iter_rows(values_only=True):
                text = " ".join(str(v) for v in row if v is not None)
                if all(k in text.lower() for k in s["row_keywords"]):
                    for st in ("Converging", "Split", "Thin", "Alt. design", "Gap"):
                        if st in text:
                            got = st
                    break
            rec(s["id"], got == s["status"], f'{s["what"]} (got {got})', level="WARN")
    return rows

# ---------------------------------------------------------------- fill
def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def cell(wb, ref):
    sh, c = ref.split("!")
    return wb[sh][c]

def score_fill(wb_path, filled_path, key):
    fm = key["fill_mode"]
    orig = os.path.join(HERE, fm["model"])
    rec("M1", sha(orig) == fm["original_sha256"], "original model file is untouched")
    of = openpyxl.load_workbook(orig)
    ff = openpyxl.load_workbook(filled_path)
    fv = openpyxl.load_workbook(filled_path, data_only=True)
    same = all(of[fm["formula_sheet"]][c.coordinate].value == c.value
               for row in ff[fm["formula_sheet"]].iter_rows() for c in row
               if isinstance(of[fm["formula_sheet"]][c.coordinate].value, str) and of[fm["formula_sheet"]][c.coordinate].value.startswith("="))
    rec("M2", same, "no formula in the model was changed")
    for ref, (lo, hi) in fm["expect_ranges"].items():
        v = num(cell(fv, ref).value)
        ok = v is not None and (lo * 0.97 <= v <= hi * 1.03 or (v > 1 and lo < 1 and lo * 97 <= v <= hi * 103))
        rec("M3", ok, f"{ref} filled within expert range {lo}-{hi} (got {v})")
        c = cell(ff, ref)
        rec("M4", c.comment is not None, f"{ref} has an evidence comment", level="WARN")
    for ref, original in fm["gap_cells"].items():
        c = cell(ff, ref)
        rec("M5", num(cell(fv, ref).value) == original, f"gap {ref} keeps original value {original}")
        txt = c.comment.text if c.comment else ""
        rec("M6", any(g.lower() in txt.lower() for g in fm["gap_comment_any"]), f"gap {ref} commented 'Not covered by interviews'")
    rec("M7", "Source Map" in ff.sheetnames, "filled copy has a Source Map tab")
    wbv = openpyxl.load_workbook(wb_path, data_only=True)
    rec("M8", "Model Map" in wbv.sheetnames, "triangulation workbook has a Model Map tab")

def score_compare(wb_path, key):
    fm = key["fill_mode"]
    rec("C1", sha(os.path.join(HERE, fm["model"])) == fm["original_sha256"], "original model file is untouched")
    wbv = openpyxl.load_workbook(wb_path, data_only=True)
    flags = " ".join(str(c.value) for row in wbv["Flags"].iter_rows() for c in row if c.value).lower()
    rec("C2", "model" in flags and "3.5" in flags, "flags the model's kiln price (3.5) as below the expert range")
    rec("C3", "mainten" in flags or "not covered" in flags, "flags model inputs no expert covered (maintenance)")
    rec("C4", "Model Map" in wbv.sheetnames, "Model Map tab present")
    filled = [f for f in os.listdir(os.path.dirname(wb_path)) if "filled from interviews" in f]
    rec("C5", not filled, "no filled model copy was created in compare mode")

def score_rerun(r1, r2, key):
    a, _ = evidence_rows(openpyxl.load_workbook(r1, data_only=True))
    b, _ = evidence_rows(openpyxl.load_workbook(r2, data_only=True))
    bmap = {r["id"]: r for r in b}
    moved = [r["id"] for r in a if r["id"] not in bmap or num(bmap[r["id"]]["low"]) != num(r["low"]) or num(bmap[r["id"]]["high"]) != num(r["high"])]
    rec("R1", not moved, f"round-1 Evidence IDs stable with same values (changed/missing: {moved[:10]})")
    for spec in key["rerun"]["new_numbers"]:
        rec(spec["id"], bool(match_number(b, spec, key["tolerance"])), f'new interview number logged: {spec["expert"]} {spec["low"]}-{spec["high"]}')
    print("Also check by hand: the report names what moved (e.g. maintenance went from gap to Thin; total capex range widened).")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["triangulate", "fill", "compare", "rerun"])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--key", default=os.path.join(HERE, "answer_key_px01.json"))
    a = ap.parse_args()
    key = json.load(open(a.key, encoding="utf-8"))
    if a.mode == "triangulate":
        score_triangulate(a.files[0], key)
    elif a.mode == "fill":
        score_fill(a.files[0], a.files[1], key)
    elif a.mode == "compare":
        score_compare(a.files[0], key)
    else:
        score_rerun(a.files[0], a.files[1], key)
    fails = [r["id"] for r in results if r["status"] == "FAIL"]
    print(json.dumps({"mode": a.mode, "checks": len(results), "failed": fails,
                      "warned": [r["id"] for r in results if r["status"] == "WARN"], "pass": not fails}))
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
