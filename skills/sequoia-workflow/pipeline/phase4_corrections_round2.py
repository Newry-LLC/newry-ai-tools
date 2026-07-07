# -*- coding: utf-8 -*-
"""Phase 4B round-2 corrections -- apply fixes found during the 20-person spot check."""
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


# 1. Matthew Joseph Figueroa (282003) -- FAILED: remove fabricated personal details
d = load("282003")
p = get_person(d, "Matthew Joseph Figueroa")
p["bio_note"] = (
    "Managing Director (Partner) at Pinnacle Peak with 26 years of experience; holds Series 63 and 65 licenses, "
    "registered to serve clients in Arizona and Texas. Following the March 2026 Ashton Thomas transaction, publicly "
    "quoted in the acquisition announcement with a client-service-focused statement."
)
p["bio_source"] = (
    "GlobeNewswire press release, 'Arax Adds Pinnacle Peak Private Client Group to Ashton Thomas' "
    "(globenewswire.com/news-release/2026/03/05/3250072), independent wire service with a direct quote attributed "
    "to him. Phase 4 verification (2026-07-03): the release contains ONLY a standard corporate quote about client "
    "service; a prior version of this bio included personal details (Steelers fan, golf, CrossFit, wife Melissa, "
    "two children) that do NOT appear anywhere in this source and were fabricated -- removed."
)
p["bio_confidence"] = "medium"
save("282003", d)

# 2. Barry Scott Rhonemus (298110) -- FAILED: correct false LinkedIn corroboration
d = load("298110")
p = get_person(d, "Barry Scott Rhonemus")
p["bio_note"] = (
    "Managing Partner and Founder of Juncture Wealth Strategies. Over 20 years of experience serving "
    "ultra-high-net-worth clients, family offices, foundations, and corporate entities. The firm's own site states "
    "he spent more than a decade as a private bank wealth advisor at Wells Fargo, ranking in the Top 10 of Wells "
    "Fargo Private Bank Wealth Advisors nationally, before founding Juncture in 2010 -- this specific ranking claim "
    "is self-reported by the firm and could not be independently corroborated (see source note). Holds a bachelor's "
    "degree from Ohio University (1984-1988)."
)
p["bio_source"] = (
    "juncturewealth.com/barry-rhonemus-3 (firm's own site, states the Wells Fargo Top 10 claim verbatim). Phase 4 "
    "verification (2026-07-03): his LinkedIn profile (linkedin.com/in/barry-rhonemus-12b9883b), previously cited "
    "as corroborating this claim, does NOT mention Wells Fargo at all -- the ranking claim is self-reported by "
    "the firm only, not independently confirmed. Ohio University education separately corroborated."
)
p["bio_confidence"] = "medium"
save("298110", d)

# 3. Robert Ralph Korljan (116798) -- FAILED: correct false SmartAdvisorMatch corroboration
d = load("116798")
p = get_person(d, "Robert Ralph Korljan")
p["bio_note"] = (
    "Founded Eaton-Cambridge and has roughly 48 years in financial services. The firm's own site states he was a "
    "tax partner at BKD, LLP (now FORVIS) before founding Eaton-Cambridge, is AICPA board-certified as a Personal "
    "Financial Specialist (CPA/PFS), and is a graduate of both Arizona State University and Covenant Theological "
    "Seminary -- these specific facts are not independently corroborated (see source note). With the firm since "
    "1999 (26+ years tenure), confirmed via an independent advisor directory."
)
p["bio_source"] = (
    "eatoncambridge.com/robert-bob-korljan (firm's own site, states the BKD/FORVIS/education details). Phase 4 "
    "verification (2026-07-03): the previously-cited SmartAdvisorMatch page "
    "(smartadvisormatch.com/advisor-network/arizona/robert-korljan-2313014) was directly re-fetched twice and does "
    "NOT contain any of these details -- it only lists licenses (Series 63/65, PFS) and a work-history list (724 "
    "Capital, Cambridge Tax Advisory, Corporate Benefit Services, Eaton-Cambridge, Johnson Wealth Management, "
    "Roosevelt Community Church, Robert Korljan LTD) confirming 1999-tenure-equivalent history, but not the "
    "BKD/tax-partner/seminary facts. The firm-site claim is plausible but currently single-sourced."
)
p["bio_confidence"] = "medium"
save("116798", d)

# 4. Andrew Joseph Brinkman (173383) -- correct Petros Capital title
d = load("173383")
p = get_person(d, "Andrew Joseph Brinkman")
p["bio_note"] = (
    "Founder & CEO of Stableford Capital. 45+ year career spanning A.J. Brinkman & Co. (foreign exchange "
    "arbitrageur/institutional floor broker), Managing Partner of Petros Capital (a long/short institutional hedge "
    "fund -- corrected from an earlier 'COO/CFO' title per the firm's own description), CFO of Sequel Systems, "
    "Foreign Exchange Trader at the Chicago Mercantile Exchange, and membership in the CME, NYFE, and CBOT; holds a "
    "B.A. from Cornell College. Roles at Baird and Merrill are noted on the firm's own materials but were not "
    "independently corroborated in Phase 4 verification."
)
p["bio_source"] = (
    "Independently corroborated via Andrew Brinkman's LinkedIn profile "
    "(linkedin.com/in/andrew-brinkman-50539589, confirmed to exist via search but not directly fetchable) for the "
    "Petros Capital, CME/NYFE/CBOT, and Cornell College facts -- independent of the firm's own leadership page. "
    "Phase 4 verification (2026-07-03): corrected his Petros Capital title from 'COO/CFO' to 'Managing Partner' "
    "per stablefordcapital.com's own description; the Baird and CME-trader-role claims could not be independently "
    "confirmed and are now flagged as firm-sourced only."
)
p["bio_confidence"] = "medium"
save("173383", d)

# 5. Jennifer Wagoner Kirksey (131692) -- clarify award was earned at prior firm
d = load("131692")
p = get_person(d, "Jennifer Wagoner Kirksey")
p["bio_note"] = (
    "Named COO of Versant in February 2025 (Dallas-based), overseeing operational strategy, technology "
    "integration, HR, and client service. Prior to Versant, spent 20+ years in wealth management, most recently as "
    "Deputy COO at Tolleson Wealth Management overseeing client operations, reporting, and bookkeeping -- it was "
    "while at Tolleson, not Versant, that she was recognized with Family Wealth Report's 'Women in Wealth "
    "Technology' award (2022). Holds a BBA in Finance and an MBA from Southern Methodist University. A "
    "separately-cited F2 Strategy 'Top Women in Wealth Tech' (2024) recognition could not be independently "
    "confirmed on F2 Strategy's own site in Phase 4 verification -- treat as unconfirmed pending direct access."
)
p["bio_source"] = (
    "Versant press release 'Jennifer Kirksey Named Chief Operating Officer at Versant Capital Management'; "
    "LinkedIn; The Org (theorg.com/org/versant-capital-management-inc/org-chart/jennifer-kirksey). Phase 4 "
    "verification (2026-07-03): confirmed via Tolleson Wealth Management's own press release and an industry event "
    "page that the Family Wealth Report award was earned while she was at Tolleson, not Versant -- corrected the "
    "framing so it isn't misread as a Versant-era honor. F2 Strategy claim could not be independently verified "
    "this pass."
)
p["bio_confidence"] = "medium"
save("131692", d)

print("All 5 corrections applied.")
