# Sequoia Phoenix Pipeline — Status

Single source of truth for where this pipeline stands. Read this before resuming —
don't reconstruct state from chat history. Update it at every phase boundary.

Last verified against disk: 2026-07-03.

## What this is for

Sequoia is doing M&A sourcing into Phoenix-area RIA (wealth management) firms —
finding acquisition targets, identifying the real owners/partners, and reaching
out. This pipeline automates the research + outreach-prep so Jack/AJ can review
accurate, sourced material instead of doing it by hand.

**Non-negotiable design rule** (decision log, 2026-07-02, status LIVE — do not
relitigate without flagging it explicitly): code does everything deterministic;
AI only touches judgment calls and must cite a source; empty is an acceptable
answer; nothing writes to Airtable except one reviewed script at the very end.
This exists because v1 of this pipeline shipped once already, fabricated an
owner name, and an agent overwrote the production Airtable base.

## Pipeline phases — status

| # | Phase | Status | Notes |
|---|---|---|---|
| 0 | Ingest/filter (FINTRX → 52 qualifying firms) | ✅ Done, verified | Prior session |
| 1 | SEC ADV pull (owner names from Schedule A/B) | ✅ Done, verified | This session — see below |
| 2 | Merged people-set (owners + partners, capped at 5) | ✅ Done, verified | This session |
| 3 | Enrichment (bios, firm notes) | ✅ 52/52 firms done, verified | See below. |
| 4 | Verification gate (programmatic + adversarial) | 🔶 In progress | 4A done (all 131 people); 4B spot-check done (13 people, ~10%). See below. |
| 5 | Email drafting | ❌ Not started | |
| 6 | Write-back to Airtable | ❌ Not started | Needs a test-base-scoped PAT from Sylvan |
| 7 | Review report | ❌ Not started | |

## Phase 3 — Enrichment (bios, firm notes)

- **10/52 firms done** (the 9 batch2 firms are re-enrichments of the same 9
  thin batch1 firms, not new ones — not additive). First pass (2026-07-02,
  batch1, 10 firms) used
  ZoomInfo + firm website only and came back thin — 9 of 10 read "confirmed
  as [title], no narrative available." Redesigned per user feedback
  (2026-07-03): ZoomInfo + website + web search run together per person, web
  search treated as the primary lever (not a fallback gated behind the other
  two). Re-ran the 9 thin firms this way (batch2, 2026-07-03) — all 9 now
  have real narrative bios (career histories, credentials, notable
  recognition/press where it exists). Sensible Money (158641, batch1) already
  cleared the bar and was left as-is.
  - **Batch2 firms** (172113 Sierra Legacy Group, 326261 Luminvest, 165214
    Intrinsic Value Partners, 131458 Watts Gwilliam, 335594 Wlth Capital,
    306180 Farnam Financial, 128549 Wealth Engineering, 116933 Sage Financial
    Advisors, 311639 Wise Wealth Partners) — 13 people + 9 firm notes written
    via `phase3_enrichment_merge.py phase3_enrichment_batch2.json`, 0 misses,
    verified by re-reading `data/people/{crd}.json` (all bios 600-1500 chars
    of real narrative vs. batch1's ~100-150 char title-only notes).
  - Notably strong hooks surfaced: Sierra Legacy's Grenert is a former
    MLB-draft-pick-turned-advisor and current MLB Players Trust trustee;
    Wlth Capital's Kenefick-Rogers was featured on Michael Kitces' "Financial
    Advisor Success" podcast; Farnam's Bird was Julian Robertson's caddy
    before Robertson pointed him toward Buffett's letters; Wise Wealth's
    Rellihan is an adjunct finance professor at Grand Canyon University.
- **Batch3 (2026-07-03, 8 new firms)** — switched execution model to cut token
  spend: 2 agents each covering 4 firms (instead of 1 agent per firm), plus a
  tight per-person tool-call budget (1 ZoomInfo check, 1 web search, 1 firm
  website fetch shared across all people at that firm, stop once the bar is
  cleared). Result: 169248 Scottsdale Wealth Planning, 333708 Prosper Private
  Wealth, 173383 Stableford Capital, 337660 Luminescent Wealth Management,
  115994 R.H. Investment Group, 157663 Vigilare Wealth Management, 331395 One
  Wealth Capital Management, 105022 Intrinsic Wealth Counsel — 17 bios + 8
  firm notes written via `phase3_enrichment_merge.py phase3_enrichment_batch3.json`,
  0 misses, verified on disk. ~228k total tokens for 8 firms vs. ~720k for the
  9 firms in batch2 (1-agent-per-firm) — roughly a 3x reduction per firm, at
  the cost of a bit more hands-on QA (one batch agent skipped the required
  per-person web search for 2 people; caught it and ran a small 3-tool-call
  top-up agent to fix before merging).
  - Two people are genuinely thin despite real effort (R.H. Investment
    Group's Haymore, Prosper's Gardner) — no web footprint beyond title/tenure
    found; treated as an honest result, not a research failure.
  - Resolved a Phase 2 data-quality flag: Luminescent's Erin Itkoe is
    confirmed as the same person who left Tarbox Family Office to co-found
    the firm in 2025 (previously flagged as "plausible but unconfirmed").
  - **Known data artifact, not fixed**: two firms (337660, 331395) list the
    same real person twice under different name-key strings (once via a
    trust/Schedule B entry, once via a Schedule A entry with a stray
    "xxx-xx-xxxx" SSN-redaction placeholder baked into the name) — a Phase 2
    parsing quirk. Worked around by writing the identical bio under both keys
    rather than fixing the underlying dedup; worth a real fix if this pattern
    recurs across the remaining 34 firms.
- **Supplemental sourcing pass (2026-07-03)** on the 8 batch3 firms: batch3's
  efficiency rule ("stop once you have one solid source") let the firm's own
  website count as sufficient on its own, so several bios cited only the firm
  site + a vague "web search" with no outlet named — a real gap vs. the
  sourcing protocol (`company-research/SKILL.md`: name the specific page, not
  just the domain). Ran a second, narrower pass (2 agents, same 4-firms-each
  split) that took the existing bios as a base and required one independent
  non-firm source per person, or an explicit "checked X, found nothing"
  statement if none exists. Result: 16 of 17 name-key entries now cite a
  specific outlet (LinkedIn, SEC IAPD/BrokerCheck, U.S. News Advisor Finder,
  AZ Big Media, the Financial Planning Association's own journal archive,
  Wealthminder, SmartAdvisorMatch); the 17th (Mark Rehn) honestly documents a
  lead that couldn't be confirmed rather than citing it anyway.
  - This pass also **caught and corrected a real error**, not just added
    citations: Prosper Private Wealth's Gardner had a "24 years of
    experience" claim that an independent directory's own career timeline
    contradicts (~10-13 years) — flagged and removed rather than repeated.
  - It also **downgraded confidence honestly** where corroboration failed:
    Luminescent's Itkoe kept her AZ Big Media "12 Millennials to Watch"
    citation (now independently verified) but her AICPA award claim is now
    flagged as unverified (medium, was high); Intrinsic Wealth Counsel's
    Gieselle Lacey confirmed to have zero independent footprint anywhere
    (low, unchanged) — the firm's own bio page is genuinely the only source.
  - Cost: 2 agents, ~69k + ~81k tokens = ~150k total for 17 entries, well
    under a full re-run of these 8 firms (~228k) since it reused existing
    findings instead of redoing ZoomInfo/website steps.
- **Batch4 (2026-07-03, 10 new firms)** — first full run using the settled
  standard (independent non-firm source required up front, named specifically
  in bio_source). 4 agents, sized by people-count not firm-count (6-9 people
  each) since two firms in this batch were unusually large (ARQ 147351 and
  L. Roy Papp 105130, both capped down from 6 and 12 people respectively —
  the dropped-for-cap names were explicitly excluded from research). Firms:
  298110 Juncture Wealth Strategies, 147351 ARQ Wealth Advisors, 328450 SL
  Capital, 151365 Biltmore Wealth Management, 332192 Degreen Private Wealth,
  333381 GPS Investments, 153410 Galvin Gaustad & Stein, 127517 Wealth
  Management Solutions, 105130 L. Roy Papp & Associates, 317615 Fortitude
  Family Office. 29 people + 10 firm notes written via
  `phase3_enrichment_merge.py phase3_enrichment_batch4.json`, 0 misses,
  verified on disk. Confidence: 14 high / 9 medium / 4 low / 2 none.
  26 of 29 (90%) cite a specific named independent source (LinkedIn, SEC
  IAPD, U.S. News, PR Newswire, Arizona Historymaker oral histories, Flinn
  Foundation, etc.) — the 3 without are honest "nothing independent found"
  results (2 SL Capital trustees, 1 no confidence), not a sourcing gap.
  - Strong hooks: William Lee (ARQ) — WSJ/Forbes mentions, Five Star Wealth
    Manager 2015-2025; L. Roy Papp & Associates — family-founded by a former
    U.S. ambassador to the Asian Development Bank, now run by his two
    children (independently confirmed via AZ Historymaker bios and the Flinn
    Foundation, not assumed from the shared surname); Kevin Sweeney (Biltmore)
    — Diamondbacks draft pick, Pioneer League MVP, now specializes in
    athlete financial planning; Matt Walker (Fortitude) — Five Star Wealth
    Manager, InvestmentNews Excellence Awardee, Business Intelligence Group
    Executive of the Year.
  - Fortitude's unresolved Holdco ownership question (from Phase 2) got a
    real attempt this round — SEC Form CRS says the holdco is owned
    collectively "by its managers and employees," not confirming Walker
    individually — left flagged as unresolved rather than guessed.
  - Two SL Capital trustees (Marisa Brodt, Victor Sesate) confirmed to have
    zero independently-verifiable footprint despite real search effort;
    same-name matches found could not be confirmed as the same people and
    were correctly not used.
- **Batch5 (2026-07-03, 10 new firms)** — same standard as batch4, 3 agents
  balanced by people-count. Firms: 129597 Brightscape Investment Centers,
  168774 Arbor Wealth Management, 146054 Key Group Management, 116798
  Eaton-Cambridge, 143420 Exeter Financial, 318330 Zenith Wealth Advisors,
  318258 Ridgeline Private Wealth, 299951 Corepath Wealth Partners, 282017
  Taurum Retirement Partners, 113954 Profocus Incorporated. 27 people + 10
  firm notes written via `phase3_enrichment_merge.py phase3_enrichment_batch5.json`,
  0 misses, verified on disk. Confidence: 14 high / 10 medium / 1 low / 2
  none. 24/27 (89%) named-source rate.
  - **Two operationally important findings, not just biographical color**:
    (1) Corepath's Rick Schultenover appears to have left the firm entirely
    to launch a new RIA (Salus Financial Advisors, Colorado Springs) per an
    independent Financial Advisor Magazine article — flagged to verify
    current employment before any outreach touches him. (2) Exeter
    Financial's cached-brochure naming mismatch (flagged in Phase 2) is
    resolved: Exeter operates under the Alkeme Insurance corporate umbrella;
    3 of its 5 "owners" (Barton, Rosandic, Gutin) are Alkeme corporate/PE
    executives with no local Scottsdale presence, while Harrison and Helms
    are the actual local Managing Partners — outreach should target the
    latter two, not the corporate-parent names.
  - Corepath's previously-unresolved Corepath Holdings LLC ownership (Phase 2
    flag) is now resolved via independent Arizona business filings
    (Bizapedia/BizProfile): Mark Bonnett confirmed as the controlling owner.
  - Zenith's two people have shifted primary roles to an affiliated entity
    (Zenith Private Bank & Trust) per independent sources — flagged for
    outreach timing/accuracy even though Zenith Wealth Advisors remains their
    registered RIA.
  - Strong hooks: Eric Weiss (Brightscape) — MBA under Nobel laureate Myron
    Scholes, MA thesis under Robert Mundell, published author; Stephen
    Hofmann (Ridgeline) — rare JD+CPA+CFP combination.
- **Batch6 (2026-07-03, 8 new firms)** — same standard as batch4/5, 2 agents
  balanced by people-count. Firms: 131692 Versant Capital Management, 285932
  Spahn Wealth & Retirement, 175300 Global Strategic Nextgen OCIO, 285243
  Releve Financial Group, 116069 Harmony Asset Management, 167657 Immaculate
  Wealth Management, 298408 Foothills Advisors, 108818 Total Investment
  Management. 19 people + 8 firm notes written via
  `phase3_enrichment_merge.py` (batch6 + a 1-record fix — one agent used the
  clean name "Royce Creighton Ramey" instead of the actual on-file artifact
  name "Royce Creighton xxx-xx-xxxx RAMEY", caught by the merge script's miss
  report and corrected), 0 misses after fix, verified on disk. Confidence: 12
  high / 5 medium / 1 low / 1 none. 17/19 (89%) named-source rate.
  - Versant's unresolved Remington Revocable Trust ownership (Phase 2 flag)
    got a genuine second attempt and stays honestly unresolved — no
    connection found to any of the 5 profiled people or any public filing.
  - Strong finds: Versant's 2023 founder-to-successor ownership transition is
    well-documented via independent press (citybiz.co, AZ Big Media); Royce
    Ramey and Jennifer Kirksey both carry real external recognition (Forbes
    Finance Council, Family Wealth Report award); Total Investment
    Management's founder John Foster is a Vietnam-era Air Force pilot
    awarded the Distinguished Flying Cross, running an aviation-focused RIA
    with his CEO son Todd.
  - One title discrepancy caught and flagged, not silently resolved: Global
    Strategic's Matthew Underwood is listed as CCO in our ownership data but
    independent sources (LinkedIn, U.S. News) show his actual current role
    as Director of Investments.
  - Two people (Brett Pohl at 108818, and a data-quality-flagged pairing at
    175300/Hana Callaghan) came back honestly unconfirmed after real search
    effort — same-name matches found could not be verified as the same
    person and were correctly not used.
- **Batch7 (2026-07-03, final 6 firms) — PHASE 3 COMPLETE.** Firms: 325721
  Amplify Financial, 170536 Wisdom Wealth Investment Advisors, 282003
  Pinnacle Peak Private Client Group, 291070 Triton Wealth Management, 129415
  Financial Life Planners, 152662 Rovin Capital. 22 people + 6 firm notes
  written via `phase3_enrichment_merge.py phase3_enrichment_batch7.json`, 0
  misses, verified on disk.
  - **Two acquisition findings that matter more than biography — flag for
    Jack/AJ before any outreach planning:**
    1. **Rovin Capital (152662) was acquired by CW Advisors** (a Boston-based
       Osaic Holdings subsidiary) in February 2026, per independent press
       (Pulse2, National Today). Likely no longer independently operating —
       may not be a viable acquisition target.
    2. **Pinnacle Peak Private Client Group (282003) joined Ashton Thomas
       Private Wealth** (Arax Investment Partners / RedBird Capital) in
       March 2026, per an independent GlobeNewswire release with direct
       quotes from two of its three partners. Same caveat — likely not a
       viable target as-is.
    3. **Related finding**: Amplify Financial's (325721) CEO, Aaron Brodt, is
       the same person who founded Ashton Thomas Private Wealth — meaning
       Amplify (a wealth-tech platform, not really a target itself) and
       Pinnacle Peak (now under Ashton Thomas) sit in the same corporate
       family. Worth knowing before treating Amplify as a standalone
       Phoenix-firm target.
  - Amplify's unresolved Phase 2 ownership flag (Amplify Ventures Group LLC)
    got real, if incomplete, progress: Arizona Corporation Commission filings
    confirm the entity's sole member is "Hana Holdings, LLC" — a specific,
    independently-verified fact — but no source ties a human (e.g. Ron
    Shurts) to Hana Holdings. Left flagged, not guessed.
  - Confidence distribution this batch: high 12 / medium 6 / low 1 / none 3.
  - Strong hooks: Jason Rowley (Amplify) — former Phoenix Suns Legacy
    Partners President/CEO who helped drive the franchise to a $4B sale;
    Cynthia Fick (Financial Life Planners) — published author, recurring
    local-media voice on women and money; Markell Staffieri (Rovin) — former
    Philadelphia Eagles free-agent signee.

## Phase 3 final tally (all 52 firms)

- **52/52 firms enriched, 131 people, 0 missing bios** — verified by scanning
  every `data/people/{crd}.json` file directly, not from batch summaries.
- Execution evolved over the course of this work — worth remembering before
  starting Phase 4:
  - Batch1 (10 firms): first pass, ZoomInfo+website only, came back thin.
  - Batch2 (9 of those firms redone): full ZoomInfo+website+web-search
    corroboration, unconditionally per person — the highest-depth standard
    used.
  - Batch3 (8 new firms): switched to fewer/larger agents for token
    efficiency, but the "stop at one good source" rule let firm websites
    count as sufficient alone — sourcing thinned out, caught and patched with
    a supplemental pass.
  - Batch4-7 (26 firms): settled standard — batched agents (people-count
    balanced, not firm-count), independent non-firm source required per
    person from the start. This is the standard that should carry into
    Phase 4 design and any future re-enrichment.
- **Known unresolved items, by design (not bugs)**: 5 unresolved
  entity-owner ownership questions across the pipeline (Corepath — since
  resolved via business filings; Fortitude; Versant/Remington Trust; Amplify
  Ventures Group/Hana Holdings) where a human beneficial owner could not be
  confirmed after genuine effort. A handful of people with `bio_confidence:
  none` where no independent footprint exists anywhere. Two known duplicate
  name-key artifacts from a Phase 2 SSN-redaction parsing bug (337660 Erin
  Itkoe, 331395 Jeremy Dicker, 131692 Royce Ramey) — same real person appears
  under two name strings; both keys carry identical bios, not a data-quality
  problem for downstream use but worth a real fix if the pattern recurs.
- First attempt at this phase (2026-07-02, before batch1) gathered data via
  agents but never wrote it anywhere — the fix since then: findings go
  straight into the authoritative file via a re-runnable script, not left in
  chat output.
- Same source discipline as everywhere else: empty is a valid `bio_note`,
  every field carries a source + confidence, no disciplinary/dispute content
  ever surfaces here. No disciplinary/dispute content was surfaced in batch2
  despite several agents finding SEC/regulatory filing data in passing.

## Phase 1 — SEC ADV pull (verified counts)

- 52/52 firms: Schedule A parsed clean, 0 problems.
- 16/52 firms have Schedule B (indirect owners) — 39 indirect-owner records total.
- 138 direct owners + 39 indirect owners pulled from SEC filings.
- **Two real parsing bugs found and fixed this session** (pre-dated this
  session, were silently corrupting some owner names):
  1. The SEC's rendered ADV PDF duplicates content cumulatively page-over-page;
     naive page-joining could grab a stale/truncated copy of Schedule A. Fixed
     by using the last page that still contains the column-header sentinel.
  2. The row-boundary regex had a greedy fallback that, when an owner's
     CRD/SSN column was blank, swallowed the *next* row's name as a fake ID
     (e.g. Stableford Capital lost a row this way). Fixed by anchoring the
     CRD group to digits-only-or-absent.
- Source: `phase1_adv.py`. Report: `data/phase1_report.json`.

## Phase 2 — merged people-set (verified counts)

- 149 legal owners (Schedule A + B) → deduped/ranked/capped → **131 final people
  across all 52 firms**, 0 firms with zero people, 0 duplicate names on audit.
- **3 firms capped at 5** (most senior kept, rest recorded in `dropped_for_cap`):
  - L. Roy Papp & Associates (105130) — 12 → 5
  - Versant Capital Management (131692) — 6 → 5
  - ARQ Wealth Advisors (147351) — 6 → 5 (a newly-found non-equity partner
    didn't outrank the 5 existing equity owners — correct behavior)
- **4 firms have an unresolved entity owner** — a holding company/trust owns
  75%+ but no Schedule B row names the human behind it. Not fabricated, not
  dropped — flagged honestly:
  - Corepath Wealth Partners (299951) — Corepath Holdings LLC
  - Fortitude Family Office (317615) — Fortitude Family Office Holdco, LLC
    (lead: Matthew Walker plausibly controls it — inference, not confirmed)
  - Versant Capital Management (131692) — Remington Revocable Trust
  - Amplify Financial (325721) — Amplify Ventures Group, LLC
    (lead: Ron Shurts/Annexus — low confidence, unconfirmed)
- **Partner-status correction pass** (fixed a real gap — Phase 2's first pass
  only checked cached ADV brochures for "Partner" language; Jack's rule says
  partners can also come from the firm's website, and the brochure-only pass
  was missing real ones):
  - 15 existing people got their Partner status confirmed via the firm's
    website/ZoomInfo (e.g. Sensible Money: 3 of 4 owners are explicit Partners
    that the brochure never mentioned).
  - 5 brand-new partners discovered (named as Partner on the firm's own site,
    not previously on any filing) and added: Jeffrey Shiffra (ARQ), Peter
    Helms (Exeter), Rick Schultenover (Corepath), James Coons (Fortitude),
    Matt Fick (Financial Life Planners).
- **5 data-quality flags recorded, not silently absorbed**:
  - Exeter Financial (143420) — cached brochure text appears to describe a
    differently-named entity (Alkeme Wealth, LLC); website still brands as
    Exeter. Confirm before outreach.
  - Rovin Capital (152662) — website returned HTTP 502 on every attempt; no
    website-based partner check was possible.
  - Vigilare Wealth Management (157663) — website connection refused; same gap.
  - Pinnacle Peak Private Client Group (282003) — website has an expired SSL
    cert; ZoomInfo data still obtained, website check wasn't possible.
  - Luminescent Wealth Management (337660) — Erin Itkoe has zero ZoomInfo
    footprint here; a same-name contact exists at an unrelated firm (Tarbox
    Family Office). Plausible same person, not confirmed.
- Source: `phase2_people.py`, `phase2_merge.py`, `phase3_website_merge.py`.
  Findings: `data/phase3_website_partner_findings.json`. Report:
  `data/phase3_website_merge_report.json`.

## Known open items

- **Enrichment bios/firm notes** — collected during the website/ZoomInfo pass,
  never persisted. Re-run needed if this content is wanted (see Phase 3 above).
- **Background task in flight (started by user in a separate session,
  2026-07-02):** "Add Rick Schultenover to Corepath 299951 people list" — this
  looks redundant, since Schultenover was already added by
  `phase3_website_merge.py` (confirm on completion and reconcile/discard if
  it duplicates or conflicts).
- **4 unresolved entity owners** (above) — worth a human glance before this
  goes further, especially the two with a lead attached.
- **3 unreachable firm websites** (above) — could retry later; not blocking.

## Key files

- `phase0_ingest.py` → `data/firms.json` — the 52 qualifying firms
- `phase1_adv.py` → `data/adv/{crd}/` (firm.json, schedule_a.json,
  schedule_b.json, owner_*.json, brochure_*.pdf, brochure_text.txt) +
  `data/phase1_report.json`
- `phase2_people.py` → `data/people/{crd}_legal_owners.json` (superseded after
  merge) + `data/phase2_needs_ai.json` + `data/phase2_legal_owners_report.json`
- `phase2_merge.py` → `data/people/{crd}.json` (first merge) +
  `data/phase2_report.json`
- `phase3_website_merge.py` → updates `data/people/{crd}.json` in place +
  `data/phase3_website_merge_report.json`
- **`data/people/{crd}.json` is the current, authoritative per-firm people
  file** — 52 of these, one per firm, this is what Phase 3 (verification)
  and Phase 4 (emails) should read from.

## Phase 4 — Verification gate (2026-07-03)

**4A — programmatic checks (`phase4_programmatic_checks.py`, no AI cost):**
ran against all 131 people. 34 raw findings, but manual review showed almost
all are false positives from the checker's crude regex (e.g. "LinkedIn
profile" or "U.S. News" written in prose without a literal `.com` in the
text; two citations sharing a wire-service domain confused the
firm-only-source heuristic). Confirmed the one true-looking hit — a
"disciplinary" keyword match on Sierra Legacy's Grenert — is a false alarm:
the text reads "No disciplinary/regulatory items reviewed or included,"
confirming compliance, not a leak. **One genuine finding stood**: Sensible
Money's 4 bios (158641, the very first firm done, before the sourcing
standard evolved) are noticeably thinner than the rest of the pipeline —
confirmed independently in 4B (see below) to be a real under-research gap,
not just short prose. Report: `data/phase4_programmatic_report.json`. The
checker script itself is crude (naive domain regex) — worth tightening
before relying on it again, or just treat 4A as a cheap first pass and lean
on 4B for anything that matters.

**4B — adversarial spot-check (13 people, ~10%, weighted toward highest-stakes
claims — not random sampling):** 2 verifier agents re-checked the specific
sources already cited per person (not new research) and tried to refute each
claim. Result: **10 VERIFIED, 3 PARTIAL, 0 FAILED.**
- Both business-critical acquisition claims (Rovin Capital → CW Advisors;
  Pinnacle Peak → Ashton Thomas) came back solidly VERIFIED via widely
  syndicated independent press (BusinessWire, Yahoo Finance, Osaic.com,
  Morningstar, InvestmentNews, Manila Times, Dealroom, and more) — these can
  be trusted for targeting decisions.
- Corepath's Schultenover departure and Bonnett ownership resolution both
  VERIFIED.
- Versant's Ramey (Forbes Finance Council, 2023 ownership transition) and
  three colorful bios (Kenefick-Rogers/Kitces podcast, Bird/Julian Robertson
  caddy story, Rellihan/GCU professorship) all VERIFIED independently — the
  extraordinary-sounding claims hold up.
- **One real inaccuracy caught and fixed**: Amplify's Aaron Brodt was
  described as sole "Founder" of Amplify (he's co-founder per every
  independent source) and his firm's pre-2023-deal AUM was overstated as
  $11B when it was actually ~$3B at the time (grew to ~$9-10B only *after*
  the 2023 Arax/RedBird deal, years later than implied). Corrected directly
  in `data/people/325721.json`.
- Two PARTIAL verdicts on otherwise-solid people: Grenert's specific
  WealthManagement.com citation couldn't be confirmed to actually name him
  (rest of his bio independently corroborated); Foster's Distinguished
  Flying Cross claim is confirmed on the firm's own site verbatim but has no
  independent military-record corroboration (plausible, not proven — stays
  flagged as single-sourced).
- Confirmed Sensible Money's thinness is a real gap, not just short prose:
  Anspach is actually an Investopedia Top 100 advisor, MarketWatch columnist,
  and published author (Great Courses lecture series, two books) — none of
  which made it into the original bio. Worth a re-enrichment pass on this
  firm's 4 people if it matters for outreach quality.

**Round 2 (2026-07-03, 20 more people, weighted toward distinctive claims not
yet checked)** — 3 agents, ~7 people each. Result: **7 VERIFIED, 10 PARTIAL,
3 FAILED.** This changed the read from round 1 — a larger sample surfaced
real problems that the first 13 (0 failures) didn't catch:
- **Matthew Figueroa (282003, Pinnacle Peak) — genuine fabrication.**
  Personal details (Steelers fan, golf, CrossFit, wife Melissa, two children)
  do not appear anywhere in the press release they were attributed to — the
  release only contains a generic corporate quote. Removed; bio_confidence
  downgraded high→medium.
- **Barry Rhonemus (298110, Juncture) — false corroboration.** His "Top 10
  nationally at Wells Fargo" claim is self-reported by the firm only; the
  bio_source claimed LinkedIn corroborated it, but his LinkedIn profile
  doesn't mention Wells Fargo at all. Corrected framing + source; downgraded
  to medium.
- **Robert Korljan (116798, Eaton-Cambridge) — false corroboration.** Same
  pattern: cited SmartAdvisorMatch page, re-fetched twice, contains none of
  the claimed BKD/FORVIS/Covenant Seminary facts — those trace only to the
  firm's own site. Corrected; downgraded to medium.
- **Andrew Brinkman (173383, Stableford) — title error.** Bio said "COO/CFO
  of Petros Capital"; the firm's own site calls him "Managing Partner"
  there. Corrected; also flagged unconfirmed Baird/CME-trader-role claims.
  Downgraded to medium.
- **Jennifer Kirksey (131692, Versant) — misleading attribution.** Her
  Family Wealth Report award was earned at her *prior* firm (Tolleson
  Wealth Management), not at Versant — bio didn't clarify this, which could
  read as a Versant-era honor. Corrected framing. Downgraded to medium.
- **Two self-sourced superlatives, flagged not removed** (facts are
  consistently stated but trace only to the subject's own marketing copy,
  never independently corroborated): Eric Weiss's (129597) Myron
  Scholes/Robert Mundell academic mentorship claims; Dawn Jurkovich's
  (285243) "nation's first certified Behavioral Financial Advisor" claim
  (also published under a different name, "Dawn Dahlby" — same person,
  confirmed via her hyphenated Forbes profile).
- Everything else in this round (Foster, Thompson, Underwood, Fick, Wray,
  Hofmann fully VERIFIED; Callaghan, Botticelli, Sollis, Rowley, Hatfield,
  Dicker, Shabaker partially verified with only minor, non-load-bearing
  gaps) held up.

All 5 write-worthy corrections applied via `phase4_corrections_round2.py`,
verified on disk (valid JSON, confidence downgraded as noted).

**Flagged-but-not-corrected partials now attached to the data too**: the 10
"flagged only" partials (Grenert, Foster, Callaghan-Donald, Botticelli,
Rowley, Hatfield, Sollis, Jurkovich, Dicker, Shabaker) initially only had
their caveats recorded here in STATUS.md, not in the actual
`data/people/{crd}.json` files — meaning a future Phase 5 session reading
the JSON directly would never see them. Fixed via
`phase4_attach_flags.py`: each now carries a `phase4_note` field with what
was checked and what remains unconfirmed (verified on disk, 11/11 present
including both of Dicker's duplicate name-key entries). Going forward, any
Phase 4 verdict that isn't a full rewrite should still get a `phase4_note`
on the record, not just a STATUS.md line.

**Running total: 33/131 people spot-checked (25%). 17 VERIFIED, 13 PARTIAL,
3 FAILED overall.** The failure rate (3/33 ≈ 9%) is a real signal, not
noise — worth deciding explicitly whether to keep scaling before treating
the rest of the pipeline as trustworthy.

## Phase 4 — targeted narrow-scope check (2026-07-03, round 3)

Instead of full bio re-verification, built a risk-signature filter and
checked ONLY the flagged claim per person (cheaper than a full re-check).
Signatures, run against all 80 then-unchecked high/medium people: (1a) sole
"independent" source is an advisor-aggregator site (SmartAdvisorMatch,
Indyfin, Wealthminder, etc.) — 32 matches; (1b) bio contains a
superlative/award/ranking claim — 12 matches; (2) personal/family detail
attributed to a press release — 4 matches. Union: 39 people (49% of the
remaining pool) — a much higher hit rate than picking "interesting claims"
by eye.

4 agents, ~10 people each, checking only the flagged fact against its cited
source. **Result: 11 CONFIRMED, 24 unconfirmed-as-cited (source doesn't
contain the claim), 2 unreachable-but-corroborated-elsewhere, 2 with a real
discrepancy (dates), 1 with real overstatement (awards).**

**Key pattern, not fabrication**: nearly every "unconfirmed" case is a
citation-overstatement, not an invented fact — the underlying detail is
almost always still stated on the firm's own site, just not independently
confirmed the way the source list implied. One pattern was 100% consistent:
**every personal/family detail (spouse name, kids, hobbies) checked against
an aggregator citation came back absent from that page** — those sites only
ever carry professional/regulatory data; personal color is always
firm-self-reported, even when cited alongside an aggregator as if both
back it. Worth remembering for any future enrichment: don't list an
aggregator as a joint source for facts it doesn't actually contain.

**5 real corrections applied** via `phase4_corrections_round3.py`, verified
on disk (confidence downgraded to medium on each):
1. Alan Rosenfield (116069) — tenure date wrong (2001 vs. actual 2005).
2. Matthew Ds Staffieri (152662) — Artegius Capital title wrong ("president"
   vs. actual Founder/CEO/CIO).
3. Colin Heafy (146054) — PaineWebber start year wrong (1990 vs. BrokerCheck's
   1991-1995).
4. Daniel Thompson (318330) — "Regional President" title and a Boys & Girls
   Clubs board seat aren't in the cited source; corrected to unconfirmed.
5. Matthew Walker (317615) — 2 of 3 award claims overstated: the actual 2024
   InvestmentNews regional "Advisor of the Year" went to a different person
   (Walker's is a broader "Excellence Awardee" tier); the Business
   Intelligence Group award was won in a narrower customer-service category,
   not BIG's flagship standalone award.

**Update (same day) — these WERE corrected after all, per explicit user
direction.** Initial instinct was to leave the 24 "unconfirmed-as-cited"
people alone since the underlying facts are plausible and likely true. User
correctly pushed back: a citation that credits a source which doesn't
contain the fact is wrong regardless of whether the fact itself is true, and
should be fixed, not left as-is.

**New standing policy, set by the user this session: the firm's own website
is a sufficient, standalone source. It no longer needs a second
"independent" citation to be trusted.** This resolves the original tension
these fixes exposed — nearly every "unconfirmed" fact was, in fact, stated
plainly on the firm's own site; the only problem was crediting an
aggregator/social page that didn't actually say it. Corrected 22 of the 24
via `phase4_citation_corrections.py` + `phase4_indirect_fixes.py`
(bio_source only — bio_note facts were left untouched since they were never
in question, only their sourcing was): removed the false attribution to the
aggregator page, credited the firm's own website instead, and noted what
(if anything) is still independently confirmed. 2 of the 24
("indirectly ok" — Harrison, Siegel) got a lighter fix: their originally-cited
LinkedIn page couldn't be re-accessed to disprove or confirm directly, so
the note now says that plainly and adds the firm's site as the standing
source, rather than implying a clean independent verification that didn't
actually happen. All 22 edits verified on disk (valid JSON, updated
bio_source confirmed).

**Running total, Phase 4 corrections across all rounds: 30 people touched**
(1 AUM/founder overstatement, 3 false-corroboration citations, 1
fabrication, 1 misattributed award, 1 award-tier overstatement, 2 date
errors, 1 title error, 1 unsupported title/board claim, 20 citation-only
corrections crediting the firm's site instead of a false aggregator
citation, 2 indirect-access notes). Every person touched by Phase 2 verified
had *some* real issue in either their facts or their sourcing — a useful
signal that Phase 4 is finding genuine problems, not just confirming clean
work.

**Running total: 72/131 people touched by some form of Phase 4 check (33
full adversarial + 39 narrow-scope), 55% of the pipeline.** 8 real
corrections applied total across all rounds (1 AUM/founder overstatement, 3
false-corroboration citations, 1 fabrication, 1 title error, 1 misattributed
award, 2 date errors, 1 award overstatement — some people had more than one
fix).

## Next step

Phase 4 has now touched 72/131 people (55%) via two different methods (full
adversarial spot-check + targeted narrow-scope check). Options for
continuing, not yet decided:
- Run the narrow-scope risk-signature check against the remaining ~41
  lower-risk people for completeness (expected lower yield based on the
  pattern so far).
- Decide what to do with the 24 unresolved "unconfirmed-as-cited" people
  from this round (leave as-is, soften sourcing language, or re-verify).
- Re-enrich Sensible Money (158641, 4 people) to close the confirmed
  thinness gap from round 1.
- Move on to Phase 5 (email drafting) treating current coverage as
  sufficient.
Do not proceed on any of these without explicit go-ahead — work one phase
at a time.
