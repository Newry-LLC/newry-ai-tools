# -*- coding: utf-8 -*-
"""Phase 4B narrow-scope check corrections -- 5 real discrepancies found among the 39 flagged people."""
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


# 1. Alan Edward Rosenfield (116069) -- tenure date discrepancy
d = load("116069")
p = get_person(d, "Alan Edward Rosenfield")
p["bio_note"] = (
    "Founder and Managing Director of Harmony Asset Management. 21+ years of overall financial services "
    "experience; independent sourcing places his tenure at the firm from 2005 (not 2001 as an earlier version of "
    "this bio stated), so '24+ years with the firm' should be read as closer to 20 years. Sits on the firm's "
    "Portfolio Management Team and Investment Committee. Holds Series 63 and 65 registrations, registered to "
    "practice in Arizona and Florida."
)
p["bio_source"] = (
    "AdvisorCheck regulatory profile; Indyfin advisor profile (indyfin.com/financial-advisor/arizona/scottsdale/"
    "alan-rosenfield-1129174); LinkedIn. Phase 4 verification (2026-07-03): Indyfin independently confirms 21+ "
    "years of experience and Series 63/65, but shows a 2005 start date at the firm, not 2001 -- corrected the "
    "tenure figure accordingly."
)
p["bio_confidence"] = "medium"
save("116069", d)

# 2. Matthew Ds Staffieri (152662) -- Artegius Capital title correction
d = load("152662")
p = get_person(d, "Matthew Ds Staffieri")
p["bio_note"] = (
    "Chief Compliance Officer at Rovin Capital as of 2026; has also been an Investment Advisor at the firm since "
    "2013 (12+ years), holds a Series 66. Separately Founder, CEO, and CIO of Artegius Capital, Inc., a "
    "fund-management investment firm (corrected from an earlier 'president' title per his own LinkedIn). Shared "
    "surname with Markell Staffieri suggests a possible family tie, but no independent source confirms a "
    "relationship between them."
)
p["bio_source"] = (
    "Wealthminder and Indyfin profiles, independent of the firm website. Phase 4 verification (2026-07-03): "
    "neither Wealthminder nor Indyfin mentions Artegius Capital at all; his own LinkedIn lists him as 'Founder and "
    "CEO and Chief Investment Officer' at Artegius, not 'president' -- corrected the title."
)
p["bio_confidence"] = "medium"
save("152662", d)

# 3. Colin Patrick Heafy (146054) -- PaineWebber date correction
d = load("146054")
p = get_person(d, "Colin Patrick Heafy")
p["bio_note"] = (
    "Vice President and Principal, co-founded Key Group in 1996 alongside Patrick Murray. Economics degree from "
    "Villanova University; serves on Villanova's College of Professional Studies Dean's Advisory Council. Career "
    "included a stint at PaineWebber in Weehawken, NJ, per FINRA BrokerCheck records covering 1991-1995 (an "
    "earlier version of this bio stated 1990 as the start year); earlier stints at the NYSE, Dean Witter Reynolds, "
    "and Drexel Burnham Lambert are stated on the firm's own site and were not independently corroborated. Holds "
    "FINRA Series 7, 24, 53, and 65."
)
p["bio_source"] = (
    "keygroupwealth.com team bio page; PR Newswire release on Royal Alliance/Key Group (prnewswire.com/"
    "news-releases/royal-alliance-associates-adds-350-million-key-group-management-to-expanding-advisor-network-"
    "300527435.html) -- this release only confirms the 1996 Villanova co-founding detail, not the PaineWebber/"
    "NYSE/Dean Witter/Drexel Burnham specifics. Phase 4 verification (2026-07-03): FINRA BrokerCheck shows "
    "PaineWebber Weehawken NJ registration 1991-1995, not 1990 as previously stated -- corrected; the NYSE/Dean "
    "Witter/Drexel Burnham stints remain firm-sourced only."
)
p["bio_confidence"] = "medium"
save("146054", d)

# 4. Daniel Christopher Thompson (318330) -- title/board seat overstatement
d = load("318330")
p = get_person(d, "Daniel Christopher Thompson")
p["bio_note"] = (
    "President and CEO of Zenith Wealth Advisors (and its affiliated Zenith Private Bank & Trust) in Scottsdale, "
    "with the firm since 2022. A CERTIFIED FINANCIAL PLANNER. Independent sourcing confirms 17 years at First "
    "Western Trust Bank (2004-2021) but does not confirm the specific 'Regional President' title or a board seat "
    "with the Boys & Girls Clubs of Greater Scottsdale -- both are stated only on the firm's own materials and "
    "should be treated as unconfirmed rather than repeated as fact. Studied Finance at the University of Arizona "
    "and earned his CFP through the College for Financial Planning."
)
p["bio_source"] = (
    "SmartAdvisorMatch advisor profile (smartadvisormatch.com/advisor-network/arizona/daniel-thompson-2656870), "
    "corroborated by LinkedIn. Phase 4 verification (2026-07-03): SmartAdvisorMatch confirms 17 years at First "
    "Western Trust Bank (2004-2021, not the previously-stated '14-17 years') but does NOT mention 'Regional "
    "President' or the Boys & Girls Clubs board seat -- both flagged as unconfirmed, firm-sourced claims."
)
p["bio_confidence"] = "medium"
save("318330", d)

# 5. Matthew Gene Walker (317615) -- award claims overstated
d = load("317615")
p = get_person(d, "Matthew Gene Walker")
p["bio_note"] = (
    "Founder & CEO of Fortitude Family Office (CPA, CGMA). Founded the firm in 2021 to provide direct, meaningful "
    "wealth solutions for high- and ultra-high-net-worth families. Holds an M.S. in Taxation and a B.S. in "
    "Accountancy, both from Arizona State University. Received industry recognition, though at a more modest tier "
    "than an earlier version of this bio implied: (1) named to Five Star Professional's 2023 'Five Star Wealth "
    "Manager' list -- a legitimate, broad-based third-party award; (2) an 'InvestmentNews Awards 2024 Excellence "
    "Awardee' recognition, which is a broader finalist/honorable-mention tier, NOT the same as InvestmentNews' "
    "named 2024 Southwest 'Advisor of the Year' (that specific title went to a different advisor); (3) a Business "
    "Intelligence Group 'Executive of the Year' award that, per BIG's own site, was awarded within the narrower "
    "'2024 Excellence in Customer Service Awards' program, not BIG's flagship standalone Executive of the Year "
    "award. UNRESOLVED OWNERSHIP QUESTION (per Phase 2 flag, still open): SEC/ADV filings show Walker as a 75%+ "
    "owner via Fortitude Partner Holdings LLC. A separate entity, Fortitude Family Office Holdco, LLC, also holds "
    "75%+ ownership; the firm's Form CRS describes Holdco as owned collectively 'by its managers and employees' "
    "rather than naming an individual, and no AZ Corporation Commission filing or press coverage names Walker "
    "specifically as the controlling person behind Holdco."
)
p["bio_source"] = (
    "Firm website (fortitudefo.com/team/) and three PR Newswire releases confirming Founder/CEO title and the "
    "three award announcements. Phase 4 verification (2026-07-03): re-checked all three awards against the "
    "awarding organizations' own sites, not just the PR Newswire announcements. Five Star Professional recognition "
    "is consistent with a real award (broad-based, no pay-to-play). The InvestmentNews claim is real but "
    "overstated -- the actual 2024 Southwest 'Advisor of the Year' title went to a different advisor (Stephanie "
    "Tsang); Walker's is a broader 'Excellence Awardee' tier. The Business Intelligence Group award, confirmed on "
    "bintelligence.com itself, was awarded within BIG's 2024 Excellence in Customer Service Awards program "
    "(a 102-winner program) rather than BIG's flagship 7-person standalone Executive of the Year list -- corrected "
    "the characterization accordingly."
)
p["bio_confidence"] = "medium"
save("317615", d)

print("All 5 corrections applied.")
