# Operational Lessons — Walnut Creek Follow-Up Email Session (2026-07-03)

Draft spec of concrete, codable rules learned while drafting/QA'ing the 60-firm Walnut
Creek follow-up batch. Written for review before folding into the broader end-to-end
Sequoia skill (FINTRX → drafted emails) being built in a separate session. **Not yet
independently reviewed** — treat every rule below as a proposal, not a settled
decision. See `skill-build-notes.md` for the narrative version of some of these with
full session context.

## 1. Founder/owner claim verification

- Trigger: any field where Airtable says "Founder," "Co-Founder," or "Primary Owner."
- Method: web search `"[Person]" "[Firm]" founder`, `"[Firm]" founded by`, plus the
  firm's own team/about page, LinkedIn, SEC ADV/IAPD. Compare both the *year* and the
  *person* — both types of error occurred (one firm's founding year was off by 49
  years; another firm's credited co-founder was likely the wrong person).
- Output per firm: `CONFIRMED` / `DISCREPANCY` (with source URL + what's wrong) /
  `INCONCLUSIVE`.
- Base rate observed: ~17% (8 of 46 checked) — budget for this as expected, not an
  edge case.
- Action rule: if the wrong fact is inside the drafted paragraph text, rewrite the
  paragraph. If it's only in the background bio, append a correction note and leave
  the paragraph alone.

## 2. Completeness as a mechanical check, not a read-through

- Rule: for every string in `contact_names`, the output must contain a
  `Contact on file — <name>` entry. Missing = hard fail, not a style nit. (This is
  exactly how a firm's *first-named* contact got missed — twice, in two separate
  drafting passes.)
- Rule: for every non-empty field on the firm record (`employees`, `fee_structure`,
  `platform_technology`, `awards`, `owner2_info`), confirm it appears somewhere in the
  bio output. Literal field-by-field checklist, run per firm.
- Rule: every name in `owner2` (comma-split) or mentioned inside `owner2_info` gets its
  own bio entry, even if it can't be named in the email itself.

## 3. Enumerate tables before trusting the one you were pointed at

- Action: call `list_tables_for_base` on the base once per new engagement/market.
  Grep table names for `Connection`, `Network`, `Intro`, `Relationship` before
  assuming the firm table is the whole dataset.
- Match rule: normalize firm names (strip LLC/Inc/Wealth/Capital/etc., strip
  punctuation, lowercase) and substring-match against the candidate table's
  firm-name field.

## 4. Drafting guardrails (literal rules, not vibes)

- Name whitelist = exactly `contact_names` for that firm. Zero exceptions, even for
  people in `owner_notes` with real titles.
- No dollar figures, no headcount numbers, in the *outbound paragraph* (fine in the
  internal bio doc).
- Banned words in outbound copy: "acquisition," "sale." Required substitutes:
  "partnership," "next chapter," "conversation." (Sequoia-specific tone choice —
  treat as a configurable example, not a universal rule, when generalizing.)
- No reuse of email 1's specific descriptive phrase, even paraphrased — must ground in
  a *different* fact than email 1 already used.
- Contact is "you"/"your" only — zero third-person references to them by name.
- Force the draft step through a schema (`{paragraph: string}`), not a "return only X"
  text instruction — the latter leaked reasoning text into ~13/49 outputs in an
  earlier run of this same skill.

## 5. Escalation tiers

| Tier | Condition | Action |
|---|---|---|
| 0 | Fact confirmed | use as-is |
| 1 | Wrong fact, not in drafted copy | append note, no rewrite |
| 2 | Wrong fact live in drafted paragraph | rewrite paragraph + note |
| 3 | Ambiguous who the real contact/owner is | flag ⚠, do NOT auto-rewrite, route to human |
| 4 | Legal/reputational risk on named contacts | no draft at all, hold firm out of the batch entirely |

## 6. Doc-editing mechanics

- Always back up before any script that inserts/moves paragraphs; only delete the
  backup after verifying paragraph/heading counts match expectation.
- Known bug to avoid: anchoring an insertion on "next item in my processing subset"
  instead of "next heading in the actual document." If firms are processed out of
  full document sequence (some skipped for later), those two are NOT the same, and
  content lands under the wrong heading. Fix: either process in full contiguous
  document order, or explicitly map each item to its true document-neighbor before
  inserting.
- Fixed color code: green = bio section labels, blue = network-connection notes,
  amber = FYI/minor discrepancy, red = serious correction or hold-for-review. Don't
  invent new colors per firm.
- Post-edit verification, every time: heading count unchanged, expected block-type
  count == number of firms just touched, zero old-format leftovers.

## 7. Cache mechanics

- TTL: 24h, checked via file modification time.
- Override: a `refresh_cache: true` param, no other special-casing.
- Cache file shape: `{fetched_at: <ISO8601>, <key>: [...]}`.
- Scope rule: market-specific data gets one cache file per market; base-wide data
  (e.g. a cross-market Connections table) gets one shared file, never duplicated per
  market.

## 8. Agent orchestration for QA batches

- Explicit line required in the prompt: "Do not spawn or delegate to other agents —
  perform the searches yourself." Without it, agents sub-delegated and returned
  "still waiting on other agents" instead of actual findings.
- Batch size ~8-10 firms per agent for parallelization.
- Failure detection: if an agent's final message doesn't contain the requested
  structured per-item findings, treat the run as failed — resume with an explicit
  "you didn't deliver X, do it directly now" correction. Don't accept a status update
  as a completed result.
- After resuming an agent, check the actual background-task list for orphaned
  children it may have spawned — a parent reporting "done" doesn't guarantee
  everything under it stopped.

## 9. Decision-state tracking

- The moment a mid-session deviation happens (e.g., swapping reference examples),
  write it to the build-notes file *then* — old value, new value, why — not
  reconstructed later from memory.
- A variant built "for comparison" is a distinct state from "decided." Track it as an
  open item with a named owner until someone actually picks one.

---

*Status: draft, pending independent review (planned for the broader-skill-build
session). Do not treat any rule above as final until reviewed.*
