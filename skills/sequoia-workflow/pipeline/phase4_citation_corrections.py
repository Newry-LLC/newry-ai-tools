# -*- coding: utf-8 -*-
"""Phase 4 citation corrections -- for people whose bio_source claimed an
aggregator/social site independently corroborated facts that, when directly
checked, weren't actually there. Per updated policy: the firm's own website
is treated as a sufficient standalone source on its own -- no longer needs a
second "independent" site to back it up. This script does NOT change any
bio_note facts (they're presumed accurate, sourced to the firm's site all
along); it only corrects bio_source to say where the facts actually came
from instead of falsely crediting a page that doesn't contain them."""
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
    raise KeyError(f"{name} not found")


def fix_source(crd, name, new_source):
    d = load(crd)
    p = get_person(d, name)
    p["bio_source"] = new_source
    save(crd, d)


PHASE4_TAG = "Phase 4 verification (2026-07-03): the previously-cited independent source does not actually contain this detail when checked directly -- corrected to credit the firm's own website, which under current sourcing policy is treated as sufficient on its own."

FIXES = [
    ("105130", "Jeffrey Nels Edwards",
     "roypapp.com/partners.html (firm's own website states his MBA, Hastings College BA, 1981 NAIA All-American honor, "
     "and Wharton Foundation trustee role). " + PHASE4_TAG + " (smartadvisormatch.com/advisor-network/arizona/"
     "jeffrey-edwards-1105196 confirms only his CFA credential and current role, not these specific biographical facts.)"),

    ("113954", "Michael Maurice Smith",
     "profocus.com/about-us/about-michael-smith (firm's own website states his U.S. Air Force veteran status and "
     "Phoenix Industrial Development Authority Board treasurer role; CFP credential independently confirmed via "
     "SmartAdvisorMatch and Unbiased.com). " + PHASE4_TAG),

    ("128549", "David John Fernandez",
     "wealth-engineering.com/founder and /about (firm's own website states his media-mentions list -- WSJ, Money "
     "Magazine, MSN Money, Business Week, MarketWatch, Arizona Republic, Research Magazine, Kiplinger's, "
     "Investopedia.com -- and his NAPFA/FPA/CAEPC association roles). Phase 4 verification (2026-07-03): no "
     "independent article or archive naming Fernandez in any of these specific outlets was found; this list traces "
     "only to the firm's own self-description, not a verified article-by-article record. Treat as firm-stated, not "
     "independently confirmed."),

    ("129415", "Gina Giachetti Wight",
     "financiallifeplanners.com team page (firm's own website states her prior Vice President, Branch Manager role "
     "at Morgan Stanley). Phase 4 verification (2026-07-03): a ZoomInfo profile for her exists but could not be "
     "directly re-fetched to confirm this specific detail independently; treat as firm-stated."),

    ("131458", "Jeffrey Stephen Watts",
     "wattsgwilliam.com team bio page (firm's own website states his marriage to Kari, five children, and "
     "ultratrail-running/Grand Canyon-hiking hobbies, alongside his BYU education and stock-option specialization). "
     "ZoomInfo and SEC filings independently confirm his title, tenure, and Series 66 license. " + PHASE4_TAG +
     " (the personal/family details are not on SmartAdvisorMatch or any independent source found.)"),

    ("131458", "Daniel Bradford Gwilliam",
     "wattsgwilliam.com team bio page (firm's own website states the father-son relationship with Kimball Gwilliam, "
     "his marriage to Jo, and six children). Kimball Gwilliam's 2022 join date is independently confirmed via "
     "SmartAdvisorMatch (smartadvisormatch.com/advisor-network/arizona/kimball-gwilliam-7816789). " + PHASE4_TAG +
     " (the specific father-son relationship claim is stated only on the firm's site.)"),

    ("131458", "David Bruce Watts",
     "wattsgwilliam.com team bio page (firm's own website states his BYU varsity football background and six years "
     "at Merrill Lynch & Co., five in Los Angeles and one in Phoenix). ZoomInfo and SEC filings independently "
     "confirm his title, 27 years of experience, and Series 66 license. " + PHASE4_TAG +
     " (the football/Merrill Lynch career specifics are not on independent advisor directories found.)"),

    ("131692", "Aimee Lynn Williams-Ramey",
     "Texas Capital Bank leadership bio (texascapitalbank.com/who-we-are/people/leadership/aimee-williams-ramey) "
     "independently confirms her SMU Dedman School of Law JD (summa cum laude), OU undergrad (summa cum laude, "
     "Sumners Scholar), and Best Lawyers in Dallas / Best Women Lawyers in Dallas recognition. Phase 4 verification "
     "(2026-07-03): that page does NOT confirm '2nd in class,' 'Order of the Coif,' the specific 2007-2009 date "
     "range, or 'Texas Rising Star' -- those additional specifics are stated only on Versant's own site "
     "(versantcm.com/team/aimee-williams-ramey) and should be treated as firm-stated rather than independently "
     "confirmed."),

    ("147351", "James Nelson Robinson",
     "arqwealth.com/james-n-robinson (firm's own website states the '#1-ranked wholesaler for a $3B+ independent "
     "broker-dealer' claim and his appearances as a financial contributor on ABC, NBC, CBS, FOX, and CNN). Phase 4 "
     "verification (2026-07-03): no independent record (network archives, wholesaler rankings from the named "
     "broker-dealer, industry press) confirms either specific claim -- both trace only to the firm's own "
     "self-description and its aggregator mirrors (RocketReach, SmartAdvisorMatch), which simply repeat the firm "
     "bio rather than independently verifying it."),

    ("165214", "Carter Allen Pearl",
     "ivpaz.com/team and ivpaz.com/about/us (firm's own website states his investment-committee roles with the "
     "Diocese of Phoenix and the Xavier Foundation, alongside his independently-corroborated career history at "
     "Pearl Capital Management, Peacock Hislop Staley & Given, and First Interstate Trust Investments). Phase 4 "
     "verification (2026-07-03): neither organization's own site, staff roster, or public Form 990 filings name "
     "Pearl as an investment committee member -- treat that specific claim as firm-stated only."),

    ("167657", "Mark Edward Rauguth",
     "immaculatewealth.com (firm's own website states he founded Precision Investments, Inc. in 2000). Indyfin "
     "(indyfin.com/financial-advisor/arizona/mesa/mark-rauguth-1564114) independently confirms his employment dates "
     "at American Express Financial Advisors (1986-1997) and Raymond James (1997-2013), and lists him at Precision "
     "Investments during that period, but does not itself state that he founded it -- that specific detail is "
     "firm-stated only."),

    ("168774", "Jake Clifford Ulrich",
     "arborfirm.com/who-we-are (firm's own website states his Boys and Girls Clubs of Arizona Executive Board of "
     "Directors role). " + PHASE4_TAG + " (smartadvisormatch.com/advisor-network/arizona/jake-ulrich-6126128 "
     "confirms only his professional history, not this volunteer role.)"),

    ("285932", "Kyle Robert Spahn",
     "spahnwealth.com (firm's own website / LinkedIn-sourced bio states his 18-20 years as a financial planner and "
     "Arizona State University degree). " + PHASE4_TAG + " (the cited SmartAdvisorMatch firm-level listing page "
     "contains only his name and location, not these details.)"),

    ("291070", "Cody Lee Ashton",
     "tritonwealthmanagement.com/cody (firm's own website states his marriage to Brooke, three sons, and Lions "
     "Club/youth-sports-coaching involvement, alongside his independently-corroborated Edward Jones/Raymond James "
     "career history). " + PHASE4_TAG + " (smartadvisormatch.com confirms only his professional history, not this "
     "personal detail.)"),

    ("291070", "David Lee Dorsey",
     "tritonwealthmanagement.com/david (firm's own website states his marriage to Kristen, four children, and "
     "hobbies -- gourmet cooking, astronomy, fly fishing -- alongside his independently-corroborated Edward Jones "
     "tenure). " + PHASE4_TAG + " (getwarmer.com/advisors/david-dorsey confirms only professional history, not "
     "this personal detail.)"),

    ("291070", "Michael Clawson Bird",
     "tritonwealthmanagement.com/mike (firm's own website states his marriage to Donna, three adult children, and "
     "his BYU/San Francisco State University education, alongside his independently-corroborated Edward Jones/"
     "Raymond James career history). " + PHASE4_TAG + " (indyfin.com confirms only professional history, not this "
     "personal/educational detail.)"),

    ("298408", "Jeffrey Michael Jones",
     "foothillsadvisors.com/jeff (firm's own website states his marriage to Amber, four children, and hobbies -- "
     "guitar, running, cycling, golf -- alongside his independently-corroborated ASU education and sole ownership/"
     "CCO status via SmartAdvisorMatch). " + PHASE4_TAG + " (the LinkedIn profile cited alongside it could not be "
     "confirmed to contain this personal detail.)"),

    ("326261", "Trent Robert White",
     "luminvest.com/about (firm's own website states the specific figure of managing over $1 billion in assets "
     "across roughly 150 UHNW households during his time at Vanguard). His broader Vanguard tenure and role are "
     "independently corroborated via NAPFA and other advisor-directory sources. Phase 4 verification (2026-07-03): "
     "the specific $1B/150-household figures could not be independently confirmed anywhere (Vanguard does not "
     "publicly disclose individual-advisor book sizes) -- treat that specific figure as firm-stated, not "
     "independently verified."),

    ("328450", "Zachary Stuart Brodt",
     "slcapitalwealth.com (firm's own website states his prior roles at UBS, Raymond James, Gentry Wealth "
     "Management, and Managing Director at First Equity Financial). Phase 4 verification (2026-07-03): U.S. News "
     "and LinkedIn could not be directly re-fetched to independently confirm this specific career history; ZoomInfo "
     "aggregator listings repeat the same information but are themselves compiled from self-reported profile data, "
     "not independent verification. Treat as firm-stated."),

    ("328450", "Marcus John Pimentel",
     "slcapitalwealth.com (firm's own website states his Brophy College Preparatory education and Division II "
     "lacrosse team captaincy at Washington University in St. Louis). SmartAdvisorMatch independently confirms his "
     "Series 65 license and general education timeline (Brophy 2014-2018, Washington University 2018-2022) but "
     "does not mention lacrosse or team captaincy specifically -- treat that detail as firm-stated only."),
]

for crd, name, source in FIXES:
    fix_source(crd, name, source)

print(f"Applied {len(FIXES)} citation corrections.")
