# Sequoia RIA M&A Pipeline — Skill Spec, Phases 0–4

Written 2026-07-03 by pulling the *actual* logic out of the Phoenix-market scripts and
session log, not by re-describing them from memory. This is the spec to build a reusable
Claude Code skill from — every rule below either came from reading a script directly or
from a structured extraction of `STATUS.md` + the `phase4_*.py` files. Where something was
never actually written down as a rule (only done ad hoc), that's flagged explicitly under
**Gaps** rather than papered over.

Phases 5–7 (email drafting, Airtable write-back, review report) are out of scope here —
see `skill-build-notes.md` and `operational-lessons-for-skill-design.md` for that piece,
being scoped separately.

---

## Non-negotiable design rule (decision log, 2026-07-02, status LIVE)

> Code does everything deterministic; AI only touches judgment calls and must cite a
> source; empty is an acceptable answer; nothing writes to Airtable except one reviewed
> script at the very end. This exists because v1 of this pipeline shipped once already,
> fabricated an owner name, and an agent overwrote the production Airtable base.

Six components, applied to every phase below:
1. Code does everything deterministic (ingest, SEC pull, write-back, review report).
2. AI only touches judgment calls (enrichment research, verification, email drafting).
3. AI must cite a source — every field carries source + confidence; no citation, no entry.
4. Empty is an acceptable answer — no required non-empty fields; sparse-but-true beats
   rich-but-invented.
5. Nothing writes to Airtable except one reviewed script at the very end — agents never
   touch Airtable.
6. Do not relitigate this rule without flagging it explicitly — it exists because v1
   failed exactly this way.

Any skill built from this spec must preserve all six, unmodified, for a new market.

---

## Phase 0 — Ingest & Filter

**Purpose:** turn a raw FINTRX market export into a filtered, prioritized firm list.
Fully deterministic, no LLM.

**Input:** one FINTRX `.xlsx` export per market.

**Required columns** (hard error if any is missing — schema drift must be loud, not
silent):

| FINTRX header | Field |
|---|---|
| Firm CRD | `firm_crd` |
| Firm Name | `name` |
| Website Address | `website` |
| Main Office City / State | `city` / `state` |
| Total AUM | `aum` |
| $ High Net Worth Clients | `hnw_aum` |
| # High Net Worth Clients | `hnw_clients` |
| 3 Year AUM Change | `three_yr_aum_change` |
| 3 Year Account Change | `three_yr_account_change` |
| Total Client Count / Total Accounts / Employees | — |
| Fee Structure / Average Client Size / Additional Offices | — |
| Industry Accolades / Retail Custodian / Tamps Used | — |
| Last ADV Filing date / Firm FINTRX Profile Link | — |

**Number parsing:** values may arrive as float, int, `"35%"`, or `"1,234"`. Strip `,` and
`$`, detect a trailing `%` and divide by 100. A bare number > 5 in the "3yr change" columns
is assumed to be percentage points (e.g. `12` → `0.12`), not a fraction already.

**Filter logic (Jack's thresholds, confirmed 2026-07-01):**
```
pct_hnw = hnw_aum / aum
Total AUM missing or 0        → skip (report only, not in output)
pct_hnw < 0.60                → discard (report only, not in output)
0.60 ≤ pct_hnw < 0.70         → priority = Low
pct_hnw ≥ 0.70 and 3yr change > 0  → priority = High
pct_hnw ≥ 0.70 and 3yr change ≤ 0 (or missing) → priority = Medium
```
Output sorted descending by `pct_hnw`.

**Output:** `data/firms.json` — `{source_file, market, counts: {input_rows, passed,
skipped_no_aum, discarded_below_60pct, high, medium, low}, firms: [...]}`. Each firm
record carries the mapped fields + `pct_hnw` + `three_yr_aum_change_frac` + `priority`.

**Generalizing to a new market:** the FINTRX column set and Jack's thresholds are the two
things that could change per market/client. Keep both as named constants at the top of the
script (already true) so a new market only requires a config change, not a rewrite.

**Gap:** the script is Phoenix-specific only by virtue of the `--out` default path and the
hardcoded `"market": "Phoenix"` string — genuinely one line to generalize. Low-risk, not
yet done.

---

## Phase 1 — SEC ADV Pull

**Purpose:** pull each firm's Form ADV filing and derive the *legally filed* owner list.
Fully deterministic, no LLM. Owner names come from Schedule A/B — a required SEC
disclosure — **never** from web search, ZoomInfo, or an agent's guess.

**Data sources (adviserinfo.sec.gov, all public, no auth):**
- Firm IAPD profile JSON — `https://api.adviserinfo.sec.gov/search/firm/{crd}`
- Full Form ADV PDF — `https://reports.adviserinfo.sec.gov/reports/ADV/{crd}/PDF/{crd}.pdf`
- Individual owner IAPD profile — `https://api.adviserinfo.sec.gov/search/individual/{crd}`
- Part 2B brochure PDFs — URLs discovered from the firm JSON's `brochures.brochuredetails`

**Must-have request details:** set a browser User-Agent (the file host 404s on non-browser
UAs); rate-limit to ~0.35s between requests (politeness, not a documented SEC requirement
but avoids throttling); script is resumable — skip any file that already exists unless
`--force`.

**Schedule A/B parsing — the two hard-won bugs, do not relearn:**
1. **The rendered ADV PDF duplicates content cumulatively page-over-page** — page N's text
   is a growing superset of page N-1's, for as long as a given "run" continues, then
   *resets* on trailing addenda (Disclosure Reporting Pages, much shorter). Concatenating
   all pages puts stale/incomplete copies of the schedule ahead of the real one, so a naive
   `text.find()` can latch onto a truncated copy and undercount rows. **Fix:** find the
   *last* page (by index) that still contains the column-header sentinel `"FULL LEGAL
   NAME"` — that page alone has the complete, de-duplicated table. Do not assume "first
   page" or "physically last page" — the physically last page may be an unrelated trailing
   section.
2. **The trailing CRD/SSN/EIN column is frequently blank** (entities have no SSN; many
   individuals have no CRD either). The row-boundary regex must match this ID as an
   *optional* run of digits — a greedy "grab whatever comes next" fallback will swallow the
   next row's leading words as a fake ID (observed: a blank-ID row ate the next owner's
   surname and made an entity name vanish entirely).

**Row-end regexes:**
- Schedule A (direct owners): `(\d{2}/\d{4})\s+(NA|A|B|C|D|E)\s+(Y|N)\s+(PR|Y|N)(?:\s+([0-9]{4,10}))?`
- Schedule B (indirect owners — extra "entity in which interest is owned" column, no
  NA/A/B codes since those don't reach the 25% indirect-disclosure threshold):
  `(\d{2}/\d{4})\s+(C|D|E|F)\s+(Y|N)\s+(PR|Y|N)(?:\s+([0-9]{4,10}))?`
- Ownership code → percent band: `NA<5%, A 5-10%, B 10-25%, C 25-50%, D 50-75%, E 75%+`
  (Schedule B adds `F = Other (GP/trustee/elected manager)`).
- A firm legitimately having **no Schedule B** (only individual Schedule A owners) is a
  correct "no indirect owners" result, not a parse failure — don't flag it as one.

**Per-firm output:** `data/adv/{crd}/` — `firm.json`, `adv.pdf`, `schedule_a.json`,
`schedule_b.json`, `brochure_{versionId}.pdf` (skip any download under 5KB — that's an
error page, not a real PDF), `owner_{ownerCrd}.json` per individual with a CRD.

**Coverage report:** `data/phase1_report.json` — adv/schedule_a/schedule_b ok-counts,
total direct/indirect owners, total brochures, a `problems` list of any firm where the ADV
PDF or Schedule A parse didn't come back clean.

---

## Phase 2 — Merged People-Set

**Rule (Jack, confirmed via Slack 2026-07-02):** outreach people per firm = all equity
owners + all partners (a partner counts even with zero equity — "partner" is a description
found in the Part 2B brochure or the firm's website, not a filed title). Cap the merged,
deduped list at **5 people per firm**, keeping the most senior when it would run longer.

### 2a — Deterministic legal owners (code, no LLM)

- Direct individual owners: every Schedule A row with `entity_type == "I"`.
- Entity owners (`DE`/`FE`) are resolved to their real people via Schedule B: match by
  `Schedule B title_or_status.startswith(entity_name)` (Schedule B's two free-text columns
  — entity name + status — are stored combined with no reliable machine split, but in
  practice the entity name is always a leading substring of the combined text, e.g.
  `"ANDREW BRINKMAN HOLDINGS LLC MANAGING MEMBER"`). An entity owner with no Schedule B
  match is **not dropped silently** — it's recorded under `unresolved_entity_owners` with a
  reason, and flagged in the console report.
- Any Schedule B individual not tied to a parsed Schedule A entity (shouldn't happen, but
  don't silently drop a filed owner if it does) is still added, at `confidence: "medium"`
  instead of `"high"`.
- Name normalization: SEC files as `"LAST, FIRST, MIDDLE"` (any case) → reorder to
  `"First Middle Last"`, title-case. **Always keep `raw_name` alongside `name`** so a bad
  normalization is visible, not silently baked in.
- Side output: concatenate every cached brochure into one text blob per firm and count
  occurrences of the word "partner" (case-insensitive). Any firm with ≥1 mention goes into
  `phase2_needs_ai.json` — the worklist for step 2b.

### 2b — AI-bounded partner extraction (Agent fan-out — **gap, see below**)

For every firm in `phase2_needs_ai.json`, an agent reads that firm's brochure text and
extracts explicit "partner" mentions, producing (per the schema `phase2_merge.py` actually
consumes) one entry per mention:
```
{ "name": "...", "title_phrase": "...", "quote": "...",
  "confidence": "high|medium|low", "at_this_firm": true|false }
```
- `at_this_firm` must be `true` for a match to be used — several agent findings this
  session named a person called "partner" at a *different* company (a prior employer, an
  unrelated holding entity); those are excluded, not merged in.
- Every mention must carry a source quote (`quote`) — no bare assertion.

**Gap — this step was never saved as a reusable script or prompt template.** Unlike every
other phase, the fan-out that produces `phase2_ai_partners.json` was run ad hoc this
session; only its *output schema* survives (because `phase2_merge.py` depends on it). A
real skill needs this prompt written down and versioned like the others — currently
someone rebuilding this phase for a new market would have to reverse-engineer the prompt
from the consumer script's expectations.

### 2c — Merge, dedupe, rank, cap (code, no LLM)

- Match an AI partner mention to an existing legal-owner record by `(first-initial,
  last-name)` key. If more than one legal owner shares that key (e.g. a parent/child pair
  with the same first name), disambiguate by scoring title-text overlap between the
  candidate's filed title and the AI mention's `title_phrase` + `quote` (exact substring
  match scores highest; common abbreviation ↔ spelled-out pairs like CIO/"chief investment
  officer" score next; individual word overlap scores lowest). If no candidate scores above
  zero, don't force a match.
- An AI partner mention with no legal-owner match at all is a genuine non-equity partner —
  added as a new person record (`is_equity_owner: false`, `crd: null`, sourced to "ADV Part
  2B brochure (explicit \"partner\" language)").
- Defensive dedupe on a loose alpha-only name key (Schedule A/B already dedupe internally,
  but a person can legitimately appear via both a direct and indirect row in rare cases) —
  on collision, keep whichever copy scores higher on seniority (below).
- **Seniority score** (used both for cap-ranking and dedupe tie-breaking):
  ```
  ownership_pct contains "75" → +40 · "50" → +30 · "25" → +20 · any nonzero → +10
  control_person == true      → +15
  is_partner_mention == true  → +10
  title contains any of [founder, managing member, managing partner, president, ceo,
    chief executive, chairman, principal, partner]  → +5 (first match only)
  ```
- Sort descending by seniority score, keep top 5, record the rest under `dropped_for_cap`
  (never silently discarded — always logged).

**Per-firm output:** `data/people/{crd}.json` — `{crd, name, people: [...capped 5...],
capped_from, dropped_for_cap, unresolved_entity_owners, ai_partner_matches,
ai_partner_mentions_excluded}`. Each person object carries: `name`, `raw_name`, `source`,
`confidence`, `title_or_status`, `is_equity_owner`, `ownership_pct`, `control_person`,
`since`, `crd`, `is_partner_mention` (+ `partner_title_phrase`/`partner_quote` when
applicable), `seniority_score`.

**Known data quirk, not a bug — don't "fix" it:** a person can legitimately appear under
two different name-key strings for the same firm (e.g. once via a Schedule B trust entry,
once via Schedule A with an SSN-redaction placeholder baked into the literal name string).
Both keys carry identical bios once enriched; this was left as-is rather than force a
merge that might be wrong.

---

## Phase 3 — Enrichment

**Purpose:** give every person a genuine outreach hook — real career background, how they
built the firm, notable credentials/recognition — not just a name and title. Full detail
and the "what went wrong the first time" narrative lives in `NEXT_SESSION_SPEC.md`; the
operative rules are summarized here.

**Definition of done, per person:**
- `bio_note` / `bio_source` / `bio_confidence` all present (empty string is a valid
  `bio_note`, but the `bio_source` must then say what was actually checked).
- If thin/empty: the source field records the specific checks that came back empty (e.g.
  "ZoomInfo: no record; website bio page 404; web search: no substantive coverage") — a
  bare "none" is not acceptable; you have to be able to say what you checked.
- Firm-level `firm_note` = `{text, source, confidence}`.
- Everything written to disk via a re-runnable merge script (pattern:
  `phase3_enrichment_merge.py`, matches on exact `name`, reports misses), then **verified
  by re-reading the file** — "gathered in agent output" is not "done."

**Source fallback chain, in order, per person:**
1. SEC filing data already on hand (title, ownership, tenure) — authoritative, no rework.
2. ZoomInfo contact record (title confirmation; occasionally employment history).
3. Firm website bio/team page (credentials, background, positioning).
4. **Web search — required whenever 2–3 are thin, not optional just because ZoomInfo
   returned a title.** This is the step that actually makes bios rich (news, press
   releases, industry recognition, conference mentions, LinkedIn snippets via search).

**Execution shape:**
- Batch ~8–10 firms per agent; check the first batch's actual bios with the user for
  quality *before* running the rest. Don't run all 52 then declare done.
- Bar for "good": can this bio answer *who is this person and why would a thoughtful
  acquirer find them interesting?* "Confirmed as CEO, no narrative available" fails the
  bar unless the full fallback chain genuinely came back empty.
- Cost note (empirically observed this session): 1-agent-per-firm ≈ 3x the token cost of
  2 agents covering ~4 firms each with a tight per-person tool-call budget (1 ZoomInfo
  check, 1 web search, 1 shared firm-website fetch, stop once the bar is cleared) — at the
  cost of slightly more hands-on QA (a batched agent can skip a required step for a person
  or two; catch it with a small top-up agent rather than re-running the whole batch).

**Hard guardrail:** never surface disciplinary history, customer disputes, or regulatory
complaints. This is relationship-building outreach prep, not risk screening — exclude it
at every step, in every agent prompt, even though SEC records contain it and it's factual.

---

## Phase 4 — Verification Gate

**Purpose:** the safeguard against v1's fabricated-owner-name failure. Every enrichment
claim gets some form of check before it's trusted for outreach copy. Three methods, used
together, not interchangeably — described in the order they run.

### 4A — Programmatic checks (code, no LLM — cheap first pass, not authoritative)

Scans every person record for four categories. **Treat this as a noisy pre-filter, not a
verdict** — this session's run produced 34 raw findings across 131 people and nearly all
were false positives (e.g. "LinkedIn profile" written in prose without a literal `.com`
triggered the source-vagueness check).

1. **Thin bio vs. stated confidence** — `bio_confidence: "high"` but `bio_note` under 300
   chars, or `"medium"` but under 200 chars → flag.
2. **Vague source** — `bio_source` has no identifiable domain/outlet
   (`[a-z0-9\-]+\.(com|gov|org|net|io|co)`) for a `"high"`/`"medium"` confidence record →
   flag.
3. **Disciplinary/complaint language leakage** — `bio_note`, `bio_source`, and
   `firm_note.text` scanned against a fixed list of ~24 terms (disciplinary, complaint,
   arbitration, sanction, settlement, enforcement action, finra action, sec enforcement,
   lawsuit, litigation, fine of, violation, misconduct, censure, barred, suspended,
   revoked, etc.) — this is a hard content rule (see Phase 3), so any hit gets checked by a
   human even though the regex itself is crude (a false positive this session: "No
   disciplinary items" tripped it).
4. **Confidence/source mismatch** — `bio_confidence: "high"` but every domain found in
   `bio_source` matches the firm's own domain (i.e. no independent corroboration) → flag.

Output: `data/phase4_programmatic_report.json` (counts + line-level findings).

### 4B — Full adversarial re-verification (agent, refute-prompted)

Spot-check method: 2+ verifier agents re-examine the sources already cited for a person,
explicitly instructed to try to **refute** each claim rather than confirm it — re-fetch or
re-search the cited source, look for contradictions, missing detail, or overstatement.

**Sampling — weighted, not random:**
- Round 1: highest-stakes claims first (e.g. the two acquisition findings that determine
  whether a firm is even still a viable target).
- Round 2: distinctive/unusual claims not yet covered by round 1.

**Verdicts:** `VERIFIED` (source genuinely supports the claim as stated) / `PARTIAL`
(some elements confirmed, others missing or under-cited — includes "false corroboration,"
where a fact is true on the firm's own site but the *specific independent source cited*
doesn't actually contain it) / `FAILED` (source doesn't contain the claim, or contradicts
it).

**This session's numbers (illustrative, not a target to hit):** round 1, 13 people → 10
VERIFIED / 3 PARTIAL / 0 FAILED. Round 2, 20 people → 7 VERIFIED / 10 PARTIAL / 3 FAILED.
Aggregate 33 people, 9% FAILED rate — high enough that a new market should assume this is
a real base rate, not a fluke, and budget verification time accordingly.

### 4C — Narrow-scope / risk-signature check (cheaper than 4B)

Instead of re-verifying a whole bio, filter for the *single specific claim* most likely to
be wrong per person, then check only that. Three risk signatures, used as a union (checking
all three roughly doubled the hit rate vs. picking "interesting-looking" claims by eye):

1. Sole "independent" source is an advisor-aggregator site (SmartAdvisorMatch, Indyfin,
   Wealthminder, etc.) — these often just mirror firm-provided data without independently
   verifying it.
2. Bio contains a superlative/award/ranking claim.
3. A personal/family detail (spouse, kids, hobbies) is attributed to a press release or
   news source, rather than the firm's own bio.

Union of all three flagged ~49% of the remaining unchecked pool this session — a
meaningfully higher hit rate than manual triage. Agents check *only* the flagged claim
against its cited source (much cheaper than a full re-verification).

**Consistent finding to expect in any market:** personal/family details cited to an
aggregator will almost always come back absent from that page — aggregators carry
professional/regulatory data only; personal color is always firm-self-reported, even when
listed as a joint source.

### Standing policies (apply from the start of Phase 4 in a new market — don't relearn)

1. **A firm's own website is a sufficient, standalone source.** It does not need a second
   "independent" citation to be trusted. (Set mid-session this time because nearly every
   "unconfirmed-as-cited" fact turned out to be plainly stated on the firm's own site — the
   only problem was crediting an aggregator that didn't actually contain it. Settle this
   policy *before* Phase 4 starts next time, not mid-correction-cycle.)
2. **Never credit an aggregator as a source for a fact it doesn't contain**, even if the
   fact is true and stated elsewhere (typically the firm's own site).
3. **Sparse-but-true beats rich-but-invented** and **empty is an acceptable answer** — both
   inherited from the top-level design rule, restated here because Phase 4 is where they
   get tested against real findings.
4. **Every Phase 4 verdict that isn't a full rewrite still needs a `phase4_note` written to
   the person's JSON record**, not just a line in STATUS.md — a future phase reading the
   JSON directly must be able to see what was checked and what caveats remain.
5. **Citation language must accurately reflect the source** — never say a source
   "corroborates" a fact it doesn't contain; if a source couldn't be re-accessed, say that
   plainly rather than implying a clean verification that didn't happen.

### Correction mechanics

Standalone, single-purpose, re-runnable Python scripts — load the person's JSON by `name`,
modify specific fields, write back. No API calls, no Airtable writes at this stage.

**Fields touched:**
- `bio_note`, `bio_source` — rewritten when a correction is applied.
- `bio_confidence` — downgraded (high → medium) whenever a correction surfaces doubt:
  false corroboration, fabrication, date error, overstatement all trigger a downgrade.
- `phase4_note` — new field for flagged-but-not-corrected partials: what was checked, what
  remains unconfirmed.
- `phase4_status` — one of `not_checked` / `verified` / `verified_with_caveat` /
  `corrected`.
- `phase4_checked_date` — ISO date of the check.
- Firm-level `phase4_firm_summary` (e.g. "4 of 5 people checked") for a quick per-firm scan.

**Script sequence (illustrative order, re-derive per correction batch, not literally fixed
forever):** programmatic scan → round-2 corrections → round-3 corrections → citation-only
corrections (bulk, applying policy #1/#2 above) → indirect/unreachable-source fixes →
attach-flags (writes `phase4_note` to partials) → status backfill (writes `phase4_status`
+ `phase4_checked_date` to every record, computes the firm-level summary).

### Coverage math and "when is Phase 4 done"

No fixed target was set this session (72/131 = 55% is where it stopped, not a designed
threshold). For a new market, decide the coverage target **before** starting Phase 4, as an
explicit go/no-go with the client, rather than letting it trail off. Whatever the target:
count 4B and 4C coverage separately (they check different things — full-bio vs.
single-claim) and report both, not a blended number.

---

## Cross-phase data schema reference

`data/firms.json` (Phase 0) → `data/adv/{crd}/*` (Phase 1) → `data/people/{crd}.json`
(Phase 2, then extended in place by Phases 3–4):

| Field | Added in | Notes |
|---|---|---|
| `name`, `raw_name`, `source`, `confidence` | Phase 2 | `raw_name` = as-filed string, never overwritten |
| `title_or_status`, `is_equity_owner`, `ownership_pct`, `control_person`, `since`, `crd` | Phase 2 | from Schedule A/B |
| `is_partner_mention`, `partner_title_phrase`, `partner_quote` | Phase 2 | from brochure AI fan-out |
| `seniority_score` | Phase 2 | drives cap-at-5 ranking |
| `bio_note`, `bio_source`, `bio_confidence` | Phase 3 | empty string is valid; source must say what was checked |
| `phase4_status`, `phase4_checked_date`, `phase4_note` (if applicable) | Phase 4 | status ∈ {not_checked, verified, verified_with_caveat, corrected} |
| Firm-level `firm_note` {text, source, confidence} | Phase 3 | |
| Firm-level `phase4_firm_summary` | Phase 4 | e.g. "4 of 5 people checked" |

---

## Gaps to close before this is a real, portable skill

1. **Phase 2b's AI partner-extraction prompt was never saved.** Only its output schema
   survives via the consumer script. Write and version it like every other phase.
2. **Phase 0's market name and FINTRX column set are hardcoded**, not config. Low effort to
   parameterize; not yet done.
3. **Phase 4 has no fixed coverage target or stopping rule.** It should be a decision made
   up front per engagement, not something that trails off at whatever % a session happened
   to reach.
4. **The sourcing policy "firm's own website is sufficient" was set mid-Phase-4, reactively.**
   For a new market, state it (and any other sourcing ground rules) before Phase 3 enrichment
   starts, so Phase 4 isn't spent re-litigating sourcing after the fact.
5. **Phase 4A's checks are hand-tuned regex with a high false-positive rate.** Fine as a
   cheap pre-filter, but don't let it gate anything on its own — every flag still needs a
   human or 4B/4C look.
6. **LinkedIn is a structural blind spot, not a fixable prompt issue.** Confirmed three
   separate ways in a 2026-07-06 cross-check against the client's own manually-researched
   Airtable data: (a) direct fetch of a known LinkedIn URL returns HTTP 999 (LinkedIn's
   standard anti-bot block); (b) web search finds that the profile exists (title/name) but
   never indexes the page body, so education/employment detail inside the profile is
   invisible; (c) archive.org is not fetchable in this environment either. Every gap found
   in the cross-check clustered around exactly the kind of detail that lives only on
   LinkedIn (spouse/kids/hobbies, specific past employers, specific degree years) — never
   on a firm website, in press, or in ZoomInfo. A same-session attempt to route around this
   via Clay (clay.com) hit two separate problems: its bulk "Find people" prospecting search
   returned zero results for a small boutique RIA (likely not indexed at that data
   provider), and once a person was found manually, LinkedIn's own privacy setting had
   truncated his displayed name ("Carter P." instead of "Carter Pearl") — a second,
   generalizable failure mode for any *name-based* matching, automated or manual. Net: this
   pipeline should assume it cannot see LinkedIn-only content at all, budget accordingly (a
   human doing a manual LinkedIn pass on the highest-priority contacts is the only path
   confirmed to work), and not treat "not on LinkedIn" as evidence a fact is unconfirmed —
   it just means the tool never got to look.
7. **Firm-level `firm_note` has never been through any Phase 4 check.** 52/52 firms have a
   populated firm-level description (career-summary equivalent, but for the firm), and 0 of
   them have been re-verified — Phase 4 has only ever touched person-level `bio_note`/
   `bio_source`. Decide explicitly for a new market whether firm-level description text is
   in scope for verification, rather than leaving it implicitly out.
8. **Phase 4's "unconfirmed" downgrades can themselves be false negatives** — checking only
   the source(s) already on hand, rather than doing a fresh independent search, risks
   downgrading a true claim just because the *specific* source checked (often
   SmartAdvisorMatch or a blocked LinkedIn re-fetch) didn't happen to contain it. A
   2026-07-06 cross-check against the client's own independently-researched Airtable data
   found two confirmed cases: Dan Thompson's "Regional President" title and a Boys & Girls
   Club board seat (both downgraded to "firm-stated only, unconfirmed" by Phase 4, both
   independently confirmed via the org's own board page and third-party org charts once
   actually searched for) and Brian Rellihan's GoBankingRates press mentions (Phase 4 said
   "no podcast/press/association mentions found despite targeted searches"; two real,
   name-quoting GoBankingRates articles exist). **Lesson: "not found in the source I
   re-checked" is not the same finding as "actively contradicted" — Phase 4 correction
   language should distinguish the two**, and a downgrade based on a single blocked/thin
   source deserves one more independent search attempt before being written as a
   correction, not just a re-check of the original citation.
9. **Phase 4 coverage should be tracked and reported at the firm level, not just the person
   level.** A person-level "55% checked" number can hide highly uneven firm coverage — in
   the Phoenix run, only 20 of 52 firms (38%) were *fully* checked (every person done);
   23 firms were partially done (some people checked, some not) and 9 were fully untouched.
   A firm with 4 of 5 people verified isn't meaningfully "outreach ready" in a way a partner
   or client can act on — report `phase4_firm_summary`-style counts as the primary coverage
   metric, with the person-level % as a secondary detail, not the other way around.
