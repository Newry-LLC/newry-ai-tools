# -*- coding: utf-8 -*-
"""Attach Phase 4B 'flagged only' verification notes directly to the per-person
data files, so the caveat travels with the record instead of living only in
STATUS.md. Adds a `phase4_note` field; does not alter bio_note/bio_source."""
import json
from pathlib import Path

DATA = Path(__file__).parent / "data" / "people"


def load(crd):
    return json.loads((DATA / f"{crd}.json").read_text(encoding="utf-8"))


def save(crd, d):
    (DATA / f"{crd}.json").write_text(json.dumps(d, indent=2), encoding="utf-8")


def apply_note(crd, name, note):
    d = load(crd)
    found = False
    for p in d["people"]:
        if p["name"] == name:
            p["phase4_note"] = note
            found = True
    if not found:
        raise KeyError(f"{name} not found in {crd}")
    save(crd, d)


NOTES = [
    ("172113", "Geoffrey Allen Grenert",
     "Phase 4 verification (2026-07-03): baseball draft history (Astros/White Sox/Angels) and MLB Players Trust "
     "trustee role independently confirmed via Baseball-Reference.com and MLB Players Trust's own announcement. The "
     "specific WealthManagement.com 'Eleven MLB Players Turned Financial Advisors' citation could not be confirmed "
     "to actually name him despite repeated attempts -- treat that one sub-claim as unconfirmed; everything else in "
     "the bio holds up. Verdict: PARTIAL."),
    ("108818", "John Edward Foster",
     "Phase 4 verification (2026-07-03): the Distinguished Flying Cross claim is confirmed verbatim on the firm's "
     "own website (timgt.com/company), but no independent military-record source (DFC Society, veteran databases) "
     "could be found naming him. Plausible for a Vietnam-era Air Force pilot, but currently single-sourced to the "
     "firm. Verdict: PARTIAL."),
    ("175300", "Donald Edward Callaghan",
     "Phase 4 verification (2026-07-03): education and CRD/tenure details independently corroborated via "
     "WealthMinder. However, records show he left Hirtle, Callaghan & Co. in 2012, three years before co-founding "
     "Global Strategic (2015) -- the bio's framing of continuous involvement through founding isn't well supported; "
     "there's an unexplained 3-year gap. Verdict: PARTIAL."),
    ("175300", "Nicholas Guido Botticelli",
     "Phase 4 verification (2026-07-03): the cited source (ic-research.com) was re-fetched directly and does not "
     "contain the claimed Exelon/$43B/Verizon career details -- those facts appear consistent across multiple "
     "search results (likely sourced from gsisus.com, which could not be directly re-fetched) but the specific "
     "citation doesn't support them as given. Verdict: PARTIAL."),
    ("325721", "Jason Charles Rowley",
     "Phase 4 verification (2026-07-03): Suns Legacy Partners tenure and the franchise's 2023 $4B sale are "
     "independently confirmed (NBA.com, ESPN, Wikipedia), but his specific title tenure is closer to 11 years as "
     "President/CEO (~16 years total with the org) than the stated '15+ years,' and the specific 'bottom-third to "
     "#5 in league revenue' statistic could not be independently verified anywhere. Verdict: PARTIAL."),
    ("325721", "David T. Hatfield",
     "Phase 4 verification (2026-07-03): the 'AI-native data lake' claim is confirmed verbatim in the cited Wealth "
     "Advisor article. The Arizona State University MS in Information Management credential is not mentioned in "
     "that article and was not independently corroborated elsewhere this pass. Verdict: PARTIAL."),
    ("282017", "Robert Verlin Sollis",
     "Phase 4 verification (2026-07-03): the cited LinkedIn profile could not be directly accessed (bot-blocked), "
     "but the same career facts (Fidelity President's Circle Award, Allay Financial Services founding/merger) are "
     "independently corroborated via Taurum's own site content matching the claim closely. Low concern. Verdict: "
     "PARTIAL."),
    ("285243", "Dawn Deborah Jurkovich",
     "Phase 4 verification (2026-07-03): the 'nation's first certified Behavioral Financial Advisor' claim and "
     "'WELLthy360' branding trace only to her own self-authored bio copy (repeated across her Forbes profile and "
     "personal site) -- no independent third party (e.g. the BFA certifying body) confirms the 'first' superlative. "
     "Also note: her book 'Live WELLthy' is published under the name 'Dawn Dahlby,' not 'Jurkovich' -- confirmed to "
     "be the same person via her hyphenated Forbes profile (Dahlby-Jurkovich), not a different individual. Verdict: "
     "PARTIAL."),
    ("331395", "Jeremy Paul Dicker",
     "Phase 4 verification (2026-07-03): MassMutual/Guardian Life/Park Avenue Securities employment history "
     "independently confirmed via SEC IAPD/BrokerCheck. However, the 'started one day before his 18th birthday' "
     "detail and Finseca membership date are only on the firm's own site, not the SEC record. Also, IAPD shows his "
     "CEO registration around 4-5/2024, not the bio's stated 11/2023 -- a minor date discrepancy worth a second "
     "look before outreach cites a specific start date. Verdict: PARTIAL."),
    ("331395", "Jeremy Paul xxx-xx-xxxx DICKER",
     "Same individual as Jeremy Paul Dicker (data artifact) -- see that record's phase4_note. Phase 4 verification "
     "(2026-07-03): MassMutual/Guardian Life/Park Avenue Securities employment history independently confirmed via "
     "SEC IAPD/BrokerCheck; 'started one day before his 18th birthday' and Finseca date are firm-site-only; IAPD "
     "shows CEO registration ~4-5/2024 vs. bio's stated 11/2023. Verdict: PARTIAL."),
    ("131692", "Elizabeth Mollie Shabaker",
     "Phase 4 verification (2026-07-03): Women's Choice Award and CFP/CDC credentials independently confirmed via "
     "the award's own site. Her pre-Versant career history (GenSpring Family Offices, KPMG Personal Financial "
     "Planning Practice) is stated only on Versant's own site and was not independently corroborated this pass. "
     "Verdict: PARTIAL."),
]

for crd, name, note in NOTES:
    apply_note(crd, name, note)

print(f"Applied {len(NOTES)} phase4_note entries.")
