# -*- coding: utf-8 -*-
"""Fix the 2 'indirectly ok' cases: the originally-cited LinkedIn profile
couldn't be directly re-accessed (blocked), but indirect search corroborated
the same content. Note this explicitly and add the firm's own site as a
standing, sufficient-on-its-own source per current policy, rather than
leaving the citation looking like a clean, verified independent source."""
import json
from pathlib import Path

DATA = Path(__file__).parent / "data" / "people"


def load(crd):
    return json.loads((DATA / f"{crd}.json").read_text(encoding="utf-8"))


def save(crd, d):
    (DATA / f"{crd}.json").write_text(json.dumps(d, indent=2), encoding="utf-8")


def get_person(d, name):
    for p in d["people"]:
        if p["name"] == name:
            return p
    raise KeyError(name)


d = load("143420")
p = get_person(d, "Stephen Leon Harrison")
p["bio_source"] = (
    "exeterfinancial.com/our-firm (firm's own website states his Managing Partner/CCO title and career history at "
    "Friedman Billings Ramsey, Bank of America Private Bank, and Northern Trust). Phase 4 verification "
    "(2026-07-03): his LinkedIn profile (linkedin.com/in/efsteveharrison/) could not be directly re-accessed "
    "(blocked), but indirect search of the same URL's indexed content is consistent with these facts -- treating "
    "as corroborated, with the firm's own site as the primary standing source per current policy."
)
save("143420", d)

d = load("147351")
p = get_person(d, "Richard Alan Siegel")
p["bio_source"] = (
    "arqwealth.com/rich-siegel (firm's own website states his prior role as Senior Financial Planner at The "
    "Vanguard Group and his SUNY Albany 1991 degree). Phase 4 verification (2026-07-03): his LinkedIn profile "
    "(linkedin.com/in/rich-siegel-cfp-87720549) could not be directly re-accessed (blocked), but indirect search "
    "of the same URL's indexed content is consistent with these facts -- treating as corroborated, with the "
    "firm's own site as the primary standing source per current policy."
)
save("147351", d)

print("Applied 2 indirect-case fixes.")
