---
name: prt-interview-acquisition
description: Use this sub-skill to source interviewees, draft outreach emails and expert network briefs, research specific targets, and manage the pipeline tracker. Part of the Primary Research Toolkit. Triggers on "help me reach out to experts," "draft outreach for [type]," "add these names to the pipeline," "write an AlphaSights brief," "update the pipeline," "research this person before I interview them."
---

# Interview Acquisition — SKILL.md

**Plugin:** Primary Research Toolkit
**Position in workflow:** Runs in parallel with Interview Guide Design, after Research Plan Design
**Feeds:** Interview Execution

---

## What this sub-skill does

Helps the consultant turn the Research Plan into action across the full acquisition lifecycle: drafting outreach emails and expert network briefs, researching individual targets, populating and managing the pipeline tracker, and tracking status through to confirmed interview.

This is a production assist tool used iteratively throughout fieldwork — not a one-time setup. Consultants return to it as new targets are identified, outreach is sent, and statuses change.

Users can enter at any point — e.g., "research these three names," "draft an AlphaSense brief for expert type X," "update status for these contacts" — without running the full flow.

---

## What you need

**Read from the project folder first:**
- **`Primary Research/outputs/Research Plan v1.md`** — interviewee type map, outreach counts, planning factors, sequencing notes, expert network flags
- **`project.md`** — project name, client context, blinding status, incentive details, Newry contact information
- **`Primary Research/outputs/Interview Pipeline v1.xlsx`** — if it exists, load current tracker state before making any updates

**Ask if not clear from project files:**
- Is this a blinded or unblinded engagement? (affects email templates throughout)
- Is there a monetary incentive being offered? (affects email closing)
- Is the client name available to use in outreach, or must it remain confidential?

**Do not draft outreach emails without knowing the blinding status.** If it is not in `project.md`, ask before proceeding. An unblinded email sent on a blinded engagement is a serious error.

---

## How this sub-skill works

**Full flow (first session):**
1. Present a summary of all interviewee types with the proposed hook for each
2. Ask which types to work on now vs. defer
3. For selected types: draft outreach emails and/or expert network briefs; pause for feedback
4. Set up pipeline tracker
5. Research any identified targets and populate their tracker rows

**Ongoing use (returning sessions):**
- Add new targets: consultant provides names (and optionally LinkedIn URLs, company names); skill researches and populates tracker rows
- Update statuses: consultant updates manually or asks skill to record changes
- Draft follow-up emails or additional outreach as needed

**End of project:**
- Prompt to review and clean up tracker statuses
- Identify any contacts not yet uploaded to Knack/AirTable for the long-term database

**On-demand entry:**
Handle specific requests directly (e.g., "research John Smith at Dow Chemical," "draft a follow-up for our distributor contacts") without requiring the full flow.

---

## What you produce

Saved to the project's `Primary Research/outputs/` folder:

```
Primary Research/outputs/Outreach Templates v1.md       — all email templates and expert network briefs
Primary Research/outputs/Interview Pipeline v1.xlsx     — pipeline tracker (living document; updated across sessions)
```

---

## Steps

### Step 1 — Read the Research Plan and project context

Open `Primary Research/outputs/Research Plan v1.md`. Extract:
- Interviewee types, target N per type, outreach counts, planning factors
- Sequencing note (which types to approach first)
- Expert network flags (which types may need paid sourcing)
- Lead time flags

Then open `project.md` and confirm:
- Blinding status
- Client name (available or confidential)
- Incentive details
- Newry contact name and role for the outreach signature

If the pipeline tracker already exists, load it and note current state (how many contacts per type, status distribution) before proceeding.

---

### Step 2 — Type summary and prioritization

Present a summary table of all interviewee types with a proposed hook for each:

| Type | Value chain position | Proposed hook | Suggested sourcing channel | Sequencing |
|------|---------------------|---------------|---------------------------|------------|
| [Type] | [position] | [hook] | [channel] | Day 1 / Later |

Ask:
- "Do these hooks look right? Which types would you like to work on now, and which do you want to defer?"

Incorporate any hook adjustments. Proceed with the types the consultant selects.

---

### Step 3 — Outreach drafting

For each selected interviewee type:

**Outreach context:**
- Who we are targeting (title, company type, value chain position)
- The hook — why this person would want to talk to us
- Any access constraints or sensitivities (regulatory, competitive, NDA-adjacent topics)
- Sourcing channel (cold outreach, warm referral, or expert network)

**Cold outreach — draft two emails:**

**Email 1 — Introduction**
Subject line, introduction, purpose, specific ask, flexibility on format/timing, compensation note if applicable.

**Email 2 — Follow-up**
Shorter. References the intro email. Reiterates the ask. Offers a direct alternative contact if they are not the right person.

**Expert network brief (for types flagged for paid sourcing):**
A short brief to send to AlphaSights, Guidepoint, or AlphaSense describing the target profile:
- Title and seniority level
- Company type and value chain position
- Areas of expertise needed
- Topics to be covered in the interview
- Any constraints (e.g., must have direct experience with X, must not be from a competitor)

**Email writing guidance:**
- Keep outreach brief; reference the recipient's specific work or role; lead with what's in it for them
- For blinded engagements: describe the client's industry and situation without naming them; focus the hook on the topic, not the client
- For unblinded: use the client name early if it adds credibility
- Do not promise benefits (incentives, reciprocal information) that have not been confirmed
- Avoid copy-pasting the same email to many recipients in quick succession (Microsoft email volume limits); type individually or batch carefully

**After presenting each type's templates:** Ask:
- "Does this capture the right hook and level of detail for [type]? Anything to adjust?"

Incorporate feedback. Move to the next type.

---

### Step 4 — Target research and tracker population

When a consultant provides a name (or list of names) to add to the pipeline:

1. **Research each target** using web search (LinkedIn, company website, published work, news). Use project context to disambiguate if the name is common or the match is uncertain. If confidence is low, ask before populating.

2. **Populate tracker fields** from research:
   - Light profile (up to a few sentences on background, role, and why they're relevant — more if easily findable)
   - All available contact and demographic fields (see tracker structure below)

3. **For paid expert network candidates:** do not add to tracker until confirmed by the provider. Once confirmed, research using provider bio plus any additional sources.

4. **Flag gaps:** if a field can't be populated from available sources, leave blank and note it.

---

### Step 5 — Pipeline tracker

The tracker is a living Excel file updated across sessions. One tab per interviewee type (or combined if type count is small).

**Column structure** — aligned with Newry's AirTable contact database for easy end-of-project export:

*Contact fields (sync to AirTable at project close):*
- Full Name
- First Name
- Last Name
- Job Title
- Company
- Email
- Phone (Business)
- Phone (Mobile)
- LinkedIn
- Industry
- Market 1 / Industry
- Market 2
- Function / Technical Expertise
- Hourly Rate
- Consulting Staff (Newry contact managing this relationship)

*Project-specific fields (not synced to AirTable):*
- Interviewee type
- Value chain position
- Branch(es) targeted
- Contact method (cold / warm referral / expert network)
- Background research (light profile — a few sentences)
- Status (Targeted / Contacted x1 / Contacted x2 / Contacted x3 / Scheduled / Confirmed / Completed / Declined)
- Outreach date(s)
- Interview date
- Paid? (Y/N)
- Notes

**Pre-fill from Research Plan:** interviewee type, branch coverage, target N per type. Populate contact and research fields as targets are identified. Leave blank what isn't known yet.

**Status updates:** consultant updates manually or asks the skill to record changes. At end of project, skill prompts to review and clean up statuses, and flags any contacts not yet in Knack/AirTable.

**AirTable:** tracker is designed for manual export to AirTable at project close. Native AirTable integration is future scope.

---

### Step 6 — Interview Matrix

Created alongside the pipeline tracker at project setup. A living Excel file that tracks what each interviewee covered — updated by Interview Coding & Synthesis after each transcript is coded.

**File:** `Primary Research/outputs/Interview Matrix v1.xlsx`

**Four tabs:**

*Matrix tab* — the core data layer. One column per interviewee (columns added as interviews are confirmed). Rows seeded at setup from the issue tree (one row per branch) and the interview guide (one row per question). An **Emerging topics** section sits below, where Interview Coding & Synthesis adds rows for themes that appear outside the issue tree and interview guide — any emerging topic that reaches 3 interviewees graduates into the main matrix. Cells contain ✓/~/— coverage coding, color-coded green/yellow/gray.

*Dashboard tab* — summary view. One row per branch and question. Three columns: ✓ count, ~ count, — count. Updated each time the matrix is populated.

*Value chain tab* — matrix collapsed by value chain position. Counts replace individual cells. Drawn from the value chain position field in the pipeline tracker.

*Interviewee type tab* — matrix collapsed by interviewee type (IS / C / E / CI). Same structure as the value chain tab.

**At setup:** create the file with row headers only (no interviewee columns yet). Seed branch rows from the issue tree in `context/`; seed question rows from `Primary Research/outputs/Interview Guide — Master v1.docx` if it exists, or defer question rows until the guide is complete. Add a blank Emerging topics section.

**As interviews are confirmed:** add a column for each confirmed interviewee (name + interviewee code as the header). Interview Coding & Synthesis populates the cells.

**Note:** the interviewee metadata used for the segmentation tabs (value chain position, type, geography, seniority) lives in the pipeline tracker — not duplicated in the matrix file.

---

## Sourcing resources

Reference table for identifying and contacting interviewees. For guidance on which channel to use for a given project, ask: "What sourcing resources should I consider?" — the skill will ask a few orienting questions (budget, target profile, industry) and help think it through.

**Paid channels:**

| Provider | Type | Newry owner | Contact / platform |
|----------|------|-------------|-------------------|
| AlphaSights | Expert network | [TBD] | [TBD] |
| Guidepoint | Expert network | [TBD] | [TBD] |
| AlphaSense / Tegus | Expert network + transcript library | [TBD] | [TBD] |
| ZoomInfo | Contact ID / email lookup | [TBD] | [TBD] |

*This table requires periodic maintenance. If information looks stale, flag it rather than relying on it.*

**Note on paid expert networks:**
- AlphaSights / Guidepoint: ~$1,300 per credit; expert must be listed as "Anonymous" in any client-facing materials — only title and company can be shown
- AlphaSense / Tegus: ~$275–$1,075; interviews are published on the platform — be mindful of what is shared in the conversation

**Unpaid channels:**

| Channel | Notes |
|---------|-------|
| LinkedIn | Primary tool for contact ID and outreach |
| Knack / AirTable | Check prior Newry contacts first — warm outreach has higher hit rate |
| Conference agendas | Identify names from tradeshow/conference programs; use ZoomInfo to find emails |
| Journal / news articles | Contact authors; reference their work in the hook |
| Referrals | Ask each interviewee for recommendations at the close of the interview |

---

## Design principles (inherited from PRT)

- **Blinding status first** — always confirm before drafting. An unblinded email sent on a blinded engagement is a serious error.
- **Living tracker** — the pipeline tracker is updated iteratively across the project, not set up once and forgotten.
- **Research before outreach (unpaid)** — light target research at identification stage enables personalized outreach and pre-populates the tracker.
- **Paid channels: research post-confirmation** — don't add expert network candidates to the tracker until confirmed; provider bio supplies initial research context.
- **Review now or defer** — show all types upfront; consultant chooses which to work on; individual drafts on demand.
- **On-demand entry is valid** — users can enter mid-stream with a specific request; handle directly.
- **Expert network briefs alongside email templates** — draft the provider brief at the same time as outreach emails for flagged types.
- **Anonymity rules** — AlphaSights/Guidepoint experts must be listed as "Anonymous" in client-facing materials; note this at outreach stage.
- **Day 1 bias** — grounding types (academics, consultants, trade associations) flagged for immediate outreach.
- **End-of-project cleanup** — prompt to review statuses and flag contacts not yet in Knack/AirTable.

---

## Relationship to other sub-skills

| Sub-skill | What it receives from Interview Acquisition |
|-----------|---------------------------------------------|
| Interview Prep | Confirmed interviewee list; background research per interviewee; branch focus per type |
| Interview Coding & Synthesis | Pipeline tracker (interviewee metadata for segmentation tabs); Interview Matrix structure (columns added per confirmed interviewee) |

See `SKILL.md` at the plugin root for the full workflow sequence.
