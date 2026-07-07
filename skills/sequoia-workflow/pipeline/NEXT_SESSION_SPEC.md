# Next Session Spec — Sequoia Phoenix Enrichment (and forward)

Written 2026-07-02 at the end of a session that went sideways on enrichment.
This is a cold-start spec: a fresh session should be able to pick up from here
with no memory of the prior conversation. Read it top to bottom before doing
anything.

## 0. Read these first, in this order

1. `STATUS.md` (same folder) — verified state of the whole pipeline.
2. This spec.
3. `strategy/decision-log.md` → the 2026-07-02 "Sequoia research pipeline v2"
   entry (status LIVE). The design rule below is a compressed version of it;
   the log is authoritative if they ever disagree.

Do **not** reconstruct pipeline state from chat history or memory. The files
are the source of truth.

---

## 1. Goals — start here. Do not skip to the plan.

**Engagement goal.** Sequoia is doing M&A sourcing into Phoenix-area RIA
(wealth-management) firms — identifying acquisition targets, finding the real
owners/partners, and reaching out. This pipeline automates the research and
outreach-prep so Jack/AJ can review accurate, personalized, *sourced* material
instead of doing it by hand.

**What the current phase (Enrichment) is for.** Email drafting (the next phase)
needs something to personalize with. A name and a title is not enough to write
outreach that lands. Enrichment exists to give each owner/partner a genuine
hook — real career background, how they built the firm, notable credentials or
recognition, what the firm stands for — so the eventual email reads like it was
written by someone who did their homework, because it was.

**The bar for "good enrichment" (this is the bar the last session failed).**
For each person, the bio should answer: *who is this person and why would a
thoughtful acquirer find them interesting?* A bio that says "confirmed as CEO;
no narrative background available" does **not** clear the bar. It's a research
failure dressed up as a data point — unless a genuine multi-source search
(including web search, not just ZoomInfo + the firm's own site) actually came
back empty, in which case an honest empty result is acceptable and expected for
some fraction of a niche, small-firm universe.

**Definition of done for Enrichment:**
- Every person in `data/people/{crd}.json` has `bio_note` / `bio_source` /
  `bio_confidence`.
- Every firm has a `firm_note` {text, source, confidence}.
- For any person or firm where the note is empty/thin, the source field
  records *what was actually checked* (e.g. "ZoomInfo: no record; website bio
  page 404; web search: no substantive coverage") — not a bare "none". If you
  can't say what you checked, you're not done with that record.
- All of it written to disk in the per-firm files (see §5), verified by
  re-reading from disk, not from working memory.

---

## 2. Before executing: vet the skill against these goals

We built a **Company Research skill** (`skills/company-research/SKILL.md`).
The last session's mistake was twofold: first ignoring it, then half-applying
it. Do neither. Instead, **explicitly vet it against the goals above before
running anything**, and write down the conclusion.

Read `skills/company-research/SKILL.md` in full, then answer, in the session:

1. **Fit.** The skill is built primarily for *company* profiling — sourcing,
   discovery, screening against a taxonomy, and single-company deep-dives. Our
   task is partly that (the `firm_note`) but is mostly *person-level* bios,
   which the skill treats as secondary. Decide honestly: which parts of the
   skill's method transfer cleanly to person enrichment, and which don't?
2. **Sources.** The skill's tool list and its "reason about the best source per
   field" principle — does it name the right sources for enriching individual
   RIA principals (small private-firm executives, weak ZoomInfo coverage)? What
   should the fallback chain be? (Last session stopped at ZoomInfo + firm
   website and never triggered the skill's mandated web-search fallback — that
   is the specific hole to close.)
3. **Sourcing protocol.** The skill's non-negotiable sourcing rules (field-level
   source, exact quote/URL, "Unknown not No", note what was checked) — adopt
   these wholesale for enrichment. They are exactly what was missing.
4. **Gaps.** Where does the skill *not* cover what this task needs? Name the
   gaps and how you'll adapt (e.g. person bios need a "narrative hook" quality
   bar the skill's binary-classification framing doesn't describe).

Output of this step: a short written verdict — "here's how the skill applies,
here's what I'm adapting, here's the plan" — presented to the user for sign-off
**before** any research runs. The skill itself mandates plan-first; honor that.

---

## 3. The plan (leverage the skill, don't reinvent it)

Follow the skill's sequence: intake (mostly done — see §5) → plan design →
**user confirmation** → execution in batches → output.

Expected shape of the plan (refine after vetting):

- **Mode:** per-entity deep-dive (person + firm), not classification/screening.
- **Sources, in fallback order per person:**
  1. SEC filing data already on hand (title, ownership, tenure) — authoritative,
     no rework.
  2. ZoomInfo contact record (title confirmation; occasionally employment
     history).
  3. Firm website bio/team page (credentials, background, firm positioning).
  4. **Web search — required when 2–3 are thin.** News, press releases, industry
     recognition, conference/speaking mentions, LinkedIn snippets surfaced via
     search. This is the step that makes bios rich; it is not optional just
     because ZoomInfo returned a title.
- **Sourcing protocol:** every bio fact traceable to a specific source (quote or
  URL). Empty is allowed only after the fallback chain is genuinely exhausted,
  and the source field must say what was checked.
- **Batch + check-in:** work in batches (~10 firms), show the user the actual
  bios from the first batch, get a read on quality *before* running the rest.
  Do not run all 52 then declare done.
- **Persist immediately** (see §4).

---

## 4. Guardrails — hard-won, do not relearn them

- **Persist to disk immediately, via a re-runnable script.** The first
  enrichment attempt this session gathered good data in agent output and never
  wrote it anywhere — it was lost. Findings go straight into
  `data/people/{crd}.json` via a merge script (pattern:
  `phase3_enrichment_merge.py`), then get verified by re-reading the file.
  "Gathered" ≠ "done." Only "on disk and re-read" is done.
- **Never surface disciplinary history, customer disputes, or regulatory
  complaints.** This is relationship-building outreach prep, not risk
  screening. Even though SEC records contain this and it's factual, it has no
  place here. Exclude it at every step, in every agent prompt.
- **Empty is honest only after real effort.** "No narrative available" after
  checking one source is a failure. After exhausting the fallback chain, it's a
  legitimate result — record what was checked.
- **Don't declare done when thin.** The bar in §1 is the bar. If a batch comes
  back mostly thin, say so plainly and diagnose why (bad source choice? genuinely
  low-profile people?) before continuing — don't paper over it.
- **One phase at a time; check in.** Do not pipeline enrichment → verification →
  emails automatically. Each phase ends with a check-in.
- **Don't improvise past the skill.** If the skill has a method for something,
  use it. If you're inventing an ad-hoc approach, stop and check the skill first.
- **No Airtable writes** until the dedicated write-back phase (needs a
  test-base-scoped PAT from Sylvan). Agents never touch Airtable.

---

## 5. Current state (what a fresh session is inheriting)

**Pipeline (full detail in STATUS.md):**
- Phase 0 (ingest/filter → 52 firms): done, verified.
- Phase 1 (SEC ADV owner pull): done, verified. 52/52 firms, 138 direct + 39
  indirect owners, 0 problems. Two parsing bugs found and fixed.
- Phase 2 (merged people-set): done, verified. 131 people across 52 firms;
  partner status corrected via website check (15 confirmations + 5 new partners
  found). 3 firms capped at 5; 4 firms have an unresolved entity owner (flagged,
  not fabricated); 5 data-quality flags recorded.
- **Phase 3 (Enrichment): this is the job.** 10 of 52 firms have a first-pass
  enrichment already written to disk — but 9 of those 10 are **thin** (only
  Sensible Money, CRD 158641, cleared the bar). The thin ones used ZoomInfo +
  firm website only. **These 9 need re-doing with the full fallback chain**, and
  the remaining 42 firms are not started.
- Phases 4–7 (verification gate → email drafts → Airtable write-back → review
  report): not started.

**The 10 already-attempted firms (redo the 9 thin ones; 158641 is already good):**
172113 Sierra Legacy Group · 326261 Luminvest · 165214 Intrinsic Value Partners ·
131458 Watts Gwilliam · 335594 Wlth Capital · 306180 Farnam Financial ·
128549 Wealth Engineering · **158641 Sensible Money (DONE, good)** ·
116933 Sage Financial Advisors · 311639 Wise Wealth Partners.

**Data schema (already established — match it exactly):**
- Authoritative per-firm file: `data/people/{crd}.json` (52 of them).
- Each person object already carries: `name`, `raw_name`, `source`, `confidence`,
  `title_or_status`, `is_equity_owner`, `ownership_pct`, `control_person`,
  `since`, `crd`, `is_partner_mention` (+ partner_* fields where applicable),
  `seniority_score`.
- Enrichment adds to each person: `bio_note` (string, "" if genuinely empty),
  `bio_source` (string — what was checked), `bio_confidence`
  (high/medium/low/none).
- Enrichment adds to the firm (top level): `firm_note` {text, source,
  confidence}.
- Merge via a script like `phase3_enrichment_merge.py` (already exists — reads a
  batch JSON keyed by CRD, matches on exact `name`, writes in place, reports
  misses). Reuse or adapt it.

**Scripts on disk:** `phase0_ingest.py`, `phase1_adv.py`, `phase2_people.py`,
`phase2_merge.py`, `phase3_website_merge.py`, `phase3_enrichment_merge.py`.
Reports: `data/phase*_report.json`. Batch-1 enrichment input (thin, for
reference): `data/phase3_enrichment_batch1.json`.

**Environment note:** Python is `C:/Users/sshank/AppData/Local/Programs/Python/
Python314/python.exe`. ZoomInfo, WebFetch/web search available. Do NOT use the
Chrome browser tool for this (user instruction; background web fetch/search
only).

---

## 6. After enrichment (so the fresh session sees the whole arc)

Do not start these without finishing enrichment and checking in first.

- **Phase 4 — Verification gate.** Programmatic checks (placeholder text,
  name-echo fabrication, missing citations) + adversarial AI pass that tries to
  *refute* each fact. Verdicts: Verified / Partial–Review / Failed. This is the
  safeguard against v1's fabricated-owner-name failure.
- **Phase 5 — Email drafting.** Verified facts only; personalized from the
  enrichment. "Insufficient basis" flag instead of filler when a person's data
  is thin.
- **Phase 6 — Airtable write-back.** One reviewed Python script, test base only,
  hard-coded base ID, field IDs validated at startup. Needs the scoped PAT from
  Sylvan. Agents never write.
- **Phase 7 — Review report.** Verdict counts + flagged records + owner/source
  table for a ~10-minute human scan.

---

## The one-line version

Start from the goal (rich, sourced, outreach-ready bios). Read and honestly vet
the Company Research skill against that goal. Present a plan and get sign-off.
Then execute in batches with the full source-fallback chain, persist to disk
immediately, and don't call anything done until it's on disk and clears the bar.
