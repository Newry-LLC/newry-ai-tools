# Sequoia Follow-Up Email Skill — Build Notes

Running tab of requirements/decisions to fold into the standalone follow-up-email
skill, and later into the broader end-to-end Sequoia skill this will join as one
piece. Add an entry here every time a new requirement is noted in conversation —
don't rely on memory of the conversation itself.

## Requirements noted so far

- **[2026-07-03] Disk cache for Airtable + email-1 doc parsing, refreshed at most
  daily.** This is read-heavy research data that changes slowly; iterating on the
  Draft prompt (register, wording) shouldn't cost a fresh live pull every run.
  Already implemented in `followup-emails.js` (`CACHE_MAX_AGE_HOURS = 24`,
  `refresh_cache: true` arg to force a live pull). Cache files live in
  `skills/sequoia-workflow/cache/`.
- **[2026-07-03] This follow-up-email skill is one piece of a broader skill** covering
  the whole Sequoia outreach process end to end, starting from the raw FINTRX data
  export through to drafted emails. Being scoped in a separate session — this session
  only needs to build the follow-up-email piece.
- **[2026-07-03] Network/warm-connection check, now implemented.** Airtable has a
  base-wide `Connections` table (`tblEX62L13GxXSlhD`, 62 records across all markets) with
  warm-intro research between Sequoia/Eide Bailly/Newry people and target-firm owners —
  a separate research track from the firm/owner fields (see `network-mapping-rubric.md`,
  which is a still-draft tiering rubric awaiting Jack's roster, but the underlying
  Connections data collection has been happening independently of that rubric being
  finalized). `followup-emails.js` now has a "Check network connections" phase
  (cached like Airtable/email1, shared across markets since the table isn't market-scoped)
  that cross-references each firm and, if a match exists, renders a blue "NETWORK
  CONNECTION ON FILE" note at the top of that firm's section in the output doc — with
  contact names, the connection rationale, and status (Awaiting email / In progress /
  Introduction made) — so the follow-up-email process and the warm-intro process don't
  run blind to each other. For the existing Walnut Creek batch, this was retrofitted by
  hand for the 15 firms with a match (found by pulling the Connections table directly).
  **Open question for the broader skill:** should the follow-up email itself ever
  *reference* a warm connection (e.g. naming the shared alma mater), or should that stay
  siloed to the warm-intro conversation and the cold email never mention it? Not yet
  decided — surfaced but not resolved with the user.

- **[2026-07-03] Founder/primary-owner claims are unreliable enough to need a standing
  verification step, not a one-off fix.** After finding one real error by chance (Westend
  Capital Management — "George Bolton founded it in 2002" was wrong; he joined in 2004),
  ran a full spot-check of every explicit founder/primary-owner claim in the Walnut Creek
  batch (~45 firms) against public sources (firm websites, LinkedIn, SEC ADV/IAPD),
  parallelized across 5 research agents. **Result: 7 more real errors found** — Van Strum
  & Towne (founded 1927, not 1976 — off by ~50 years; the named contact is a co-owner who
  joined ~2000, not the founder), Werba Rubin Papier (original firm founded 1990, not
  2006), Financial Avengers (SEC-registered since 2000, not 2013, "founder" title
  unconfirmed), Capital Advantage (founded 1982, not 1998), Occidental Asset Management
  (a different person may be the actual co-founder — unresolved), Creekside Partners
  (firm's own site credits a different/additional co-founder; year off by one), Wealth
  Architects (founded 2005, not 2008; omits a co-founder). That's 7-8 errors out of ~45
  checked — a real, material error rate, not a fluke. **4 of the 7 had already been used
  directly in drafted Version B copy** and required rewriting the paragraph itself, not
  just a footnote. **Recommendation for the broader skill: build this verification as a
  standing pipeline step** (e.g. one web-search-backed check per firm during
  Research/Enrichment), not something that only happens when a human happens to ask for
  it — this batch would have shipped with 8 factual errors in outreach copy otherwise.
  One process note: when delegating this kind of check to sub-agents, some initially
  tried to delegate further to their own child agents instead of doing the search
  directly and had to be explicitly told not to — worth building that constraint into
  the prompt from the start next time.

- **[2026-07-03] Bio documentation completeness — Person/Firm split retrofitted to
  firms 1-20, and both should always pull every available JSON field.** Firms 1-20 were
  drafted before the Person Bio / Firm Bio split existed and only had one combined bio
  block; now match the structure used for firms 21-60. Separately, an audit of the
  last-10 firms found the split structure itself wasn't the only gap — bios were also
  missing real content already sitting in the JSON: named co-principals not addressed in
  the email (e.g. Verita's Christine Connors, Vantage's four other managing partners),
  awards, distinguishing platform/technology, and team size. One firm (Westhill) even had
  no bio at all for the actual email recipient. Applied the same completeness fix to
  firms 1-20 while doing the split (every co-principal now has an entry even when not
  email-addressable, plus platform/technology, employee counts, and awards pulled into
  the Firm Bio). **Recommendation for the broader skill: the Draft/Output step should
  mechanically iterate every populated field on the firm record** rather than relying on
  the agent to remember to surface all of it — the drop-off pattern repeated across two
  separate batches built independently, so it's a systemic gap, not one-off carelessness.

- **[2026-07-03] Bio completeness gap confirmed across the WHOLE batch, not just
  firms 1-20 or 51-60 — now patched everywhere.** After fixing 1-20, went back and
  finished the 51-60 gaps that had been found earlier but not yet applied (10 firms:
  missing co-principals, dropped awards, dropped platform/technology, missing employee
  counts — including Westhill, where Kirk Ludwig, the actual addressee, had zero bio
  content). Then audited firms 21-50 for the same pattern and found it just as bad —
  27 of 29 firms needed additions. **Three more cases of a named email addressee having
  no bio at all**, on top of Westhill: Opes Wealth Management's Mark Duvall (the FIRST-
  named contact — email opens "Mark," — had literally no bio), Fairview Capital's Peter
  Mathieson, and One Wealth Advisors' Jonathan Steele. That's 4 missing-addressee cases
  across 60 firms found via manual audit — strongly suggests this isn't occasional
  carelessness but a systemic blind spot in how the Draft step decides whose bio to
  surface (looks like it defaults to whoever has the richest research, not necessarily
  every named contact). **Recommendation for the broader skill: mechanically verify
  every name in `contact_names` has a corresponding bio entry before finalizing a
  firm's output** — don't rely on the drafting agent to remember. This should be a
  hard validation gate, not a best-effort step.

- **[2026-07-03] Interim default protocol for who gets named in an email (Phase 5),
  pending Jack/AJ sign-off on the open question below.** Criteria, based on patterns
  observed across both Walnut Creek and Phoenix:
  - Default to 1 named recipient. Use 2 only when there are genuinely co-equal owners
    (similar ownership %, both founders/co-founders).
  - Pick by the seniority score already computed in Phase 2 (ownership %, control-person
    flag, senior title keyword) — highest score is the default addressee.
  - Never address someone Phase 4 flagged as ambiguous-ownership, departed, or
    wrong-contact (e.g. Corepath, Exeter, Neumann Capital cases) — route those to a
    human instead of auto-addressing.
  - Non-equity partners are a fallback only (no clear equity owner identified), never
    added alongside an equity owner.
  - No email drafted at all if the firm itself is flagged (acquired/absorbed/no longer
    a viable target).
  This is a default, not a settled decision — see the open question immediately below.

## Open questions / flags for the broader skill

- **[2026-07-03] Owner-count mismatch — interim default set above, root question still
  open.** Jack's stated target is research on 3-6 owners/partners per firm (see
  [[project-sequoia-workflow]] — "people to reach" decision, cap 5, equity owners + all
  partners). But actual Walnut Creek round-1 outreach only named 1-2 people per firm
  (occasionally 3) — see the per-firm target-count table produced this session. Still
  unresolved: is the smaller outreach list a deliberate narrowing (e.g. only the most
  senior/responsive contacts get emailed, even though more are researched), or a gap
  where research isn't making it into outreach? Don't assume either answer — ask
  Jack/AJ when scoping the broader skill.
- **[2026-07-03] Existing Airtable firm/owner data (Walnut Creek production) has no
  source citations or confidence tags** — confirmed by scanning `Walnut_Creek-firms.json`
  (0/106 firms have a URL in free text, 1/106 has any source-citation language, the
  `Research Status` field is empty on every record) and by `Sequoia Workflow
  Automation.docx`'s own description of how it was built: firm research batched ~10
  firms per Claude session ("quality degrades mid-batch" — the team's own note), owner
  research via manual LinkedIn/website search, contact info via ZoomInfo (flagged
  "unreliable" in the same doc). Content read as plausible on spot-check, not
  fabricated, but nothing is independently verified. The broader skill should decide
  whether to backfill source+confidence onto this existing data (matching the v2
  pipeline's verified-or-blank discipline, see [[project-sequoia-workflow]]) or treat
  it as legacy/as-is and only apply that discipline to new markets going forward.
