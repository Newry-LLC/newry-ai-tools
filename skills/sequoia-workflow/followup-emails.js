export const meta = {
  name: 'sequoia-followup-emails',
  description: 'Draft Phase-2 (week 1-2 follow-up) outreach emails for a Sequoia market — one custom paragraph per firm, wrapped in the fixed opening/closing template',
  phases: [
    { title: 'Parse examples', detail: 'Extract firm-by-firm text from the initial-outreach doc(s)' },
    { title: 'Select firms', detail: 'Read Airtable for firms that got email 1 but not email 2 yet' },
    { title: 'Draft', detail: 'One agent per firm: write the custom middle paragraph' },
    { title: 'Output', detail: 'Assemble full emails and write a review doc' },
  ],
}

// ─── MARKET CONFIG ───────────────────────────────────────────────────────────

const SEQUOIA_FOLDER =
  'C:\\Users\\sshank\\OneDrive - Newry Corp\\Desktop\\Newry non-project and backup\\AI Tool Building\\Building Tools for Newry\\Newry Projects\\Sequoia\\'

const MARKETS = {
  'Phoenix': {
    base_id: 'appCQDjrwviHioJeL',
    table_id: 'tblk6rPjUGs5ZVdgn',
    test_base_id: 'appnnsUPTbfAK6kaR',
    test_table_id: 'tbllhUPpeD22MHXoe',
    region_label: 'Phoenix',
    initial_docs: [SEQUOIA_FOLDER + '2026.05.07 Phoenix Initial Outreach Emails.docx'],
    doc_style: 'phoenix',
  },
  'Walnut Creek': {
    base_id: 'appCQDjrwviHioJeL',
    table_id: 'tblAPbuJAbVkNG1bz',
    test_base_id: null,
    test_table_id: null,
    region_label: 'Bay Area',
    initial_docs: [
      SEQUOIA_FOLDER + '2026.05.29_Bay_Area_Initial_Outreach_Emails.docx',
      SEQUOIA_FOLDER + '2026_06_19_Bay_Area_Outreach_Emails_Batch2.docx',
    ],
    doc_style: 'bay_area',
  },
}

// ─── CONFIG ──────────────────────────────────────────────────────────────────

log(`args received: ${JSON.stringify(args)}`)

const marketName = (args && args.market) || 'Phoenix'
const market = MARKETS[marketName]
if (!market) throw new Error(`Unknown market: ${marketName}. Valid: ${Object.keys(MARKETS).join(', ')}`)

// Default is TRUE only when the market has a test base — pass { test: false } to
// use production. Markets with no test base (e.g. Walnut Creek) always read
// production directly; that's safe here because this workflow never writes to
// Airtable, only reads it and produces a Word doc. This mirrors the lesson from
// the 7/2 write-back incident: never write to production unless opted in on purpose.
const hasTestBase = !!market.test_base_id
const TEST_MODE = hasTestBase && !(args && args.test === false)

const BASE_ID = TEST_MODE ? market.test_base_id : market.base_id
const TABLE_ID = TEST_MODE ? market.test_table_id : market.table_id

const limit = (args && args.limit) || null

const OUTPUT_DOC = (args && args.output_path) ||
  `${SEQUOIA_FOLDER}${marketName} Second Emails - Draft.docx`

// ─── FIXED TEMPLATE (from 2026.06.04 Phoenix Second Emails.docx — market-agnostic) ──

const OPENING = (contactName) =>
  `${contactName},\n\nI wanted to follow up on my earlier note. As I mentioned before, Sequoia is looking to expand in your region, and I thought it might be helpful to share a bit more context on how they approach partnership.`

const CLOSING =
  `Sequoia is deliberate about the number of partnerships they pursue, focusing on cultural and service-model alignment above all else. This has supported a ~98% client and advisor retention while generating 18-20% organic growth net of market. Sequoia takes their time pacing integrations, ensuring client service models remain intact, and founders stay meaningfully involved in ways that reinforce what they have built.\n\nIf it would be useful, I'd welcome a brief, low-pressure conversation to share how this works in practice and learn how you're thinking about the firm's next chapter. If now isn't the right time, I completely understand.\n\nBest,`

// ─── PROMPTS ─────────────────────────────────────────────────────────────────

const PARSE_PROMPT = market.doc_style === 'phoenix' ? `
Extract every firm's outreach email text from the Word document at:
${market.initial_docs[0]}

Use python-docx (or pandoc) to read it. The doc is a series of blocks, each starting
with a firm name as a heading, followed by email body text. Some firms have a single
version. Some firms have a second, labeled "Second version:" or "Second:" — a fuller
A/B alternative to the first paragraph.

RULE: For any firm with a labeled second version, use ONLY that second version's text
as the firm's email_text and discard the first version entirely. For firms with only
one version, use that version.

Return a JSON object: { "firms": [ { "firm_name": "...", "contact_name": "", "email_text": "..." } ] }
One entry per firm. Preserve the email_text verbatim (don't summarize or edit it).
Leave contact_name as "" if the doc doesn't state one directly.
` : `
Extract every firm's custom outreach paragraph from these two Word documents (batch 1
and batch 2 of the same campaign — read both, combine into one list):
${market.initial_docs[0]}
${market.initial_docs[1]}

Use python-docx (or pandoc) to read them. Skip the "Standard Opening" / "Standard
Closing" / "Subject Line Format" boilerplate at the top of each doc — only extract the
"Custom Paragraphs by Firm" section. Each firm entry looks like:
  "[Firm Name] - [Contact Name(s)]"
  "Subject: ..."
  <custom paragraph text>

Return a JSON object: { "firms": [ { "firm_name": "...", "contact_name": "...", "email_text": "..." } ] }
One entry per firm across both docs. contact_name is whatever follows the dash after
the firm name (first person's first name if multiple are listed). Preserve email_text
verbatim.
`

const PARSE_SCHEMA = {
  type: 'object',
  required: ['firms'],
  properties: {
    firms: {
      type: 'array',
      items: {
        type: 'object',
        required: ['firm_name', 'email_text'],
        properties: {
          firm_name: { type: 'string' },
          contact_name: { type: 'string' },
          email_text: { type: 'string' },
        },
      },
    },
  },
}

const SELECT_PROMPT = `
READ ONLY. Do not call create_records_for_table, update_records_for_table, or
delete_records_for_table. Do NOT call list_bases or search_bases — use ONLY:
Base ID: ${BASE_ID}
Table ID: ${TABLE_ID}

List records from this table using list_records_for_table (fetch all fields).

${TEST_MODE
  ? `This is the TEST base — it has no email-date tracking fields. Return every record
     as a candidate${limit ? ` (up to ${limit} records)` : ''}.`
  : `Filter to firms where "Date: 1st Email" is populated AND "Date: 2nd Email" is
     blank AND Status is not something terminal like "Declined" or "Not a Fit"
     (if Status is blank or something like "Contacted"/"In Progress", include it).`}

Field names vary slightly by table (e.g. "Other firm notes" vs "Other Firm Notes") —
match by meaning, not exact string. For each selected firm return: record_id, name,
primary_owner, owner_notes, owner2, owner2_info (if present), service_model,
typical_client, other_firm_notes, aum, employees, fee_structure, platform_technology,
awards. Use empty string for anything blank — don't omit fields.

Return a JSON object: { "firms": [ {...} ] }
`

const SELECT_SCHEMA = {
  type: 'object',
  required: ['firms'],
  properties: {
    firms: {
      type: 'array',
      items: {
        type: 'object',
        required: ['record_id', 'name'],
        properties: {
          record_id: { type: 'string' },
          name: { type: 'string' },
          primary_owner: { type: 'string' },
          owner_notes: { type: 'string' },
          owner2: { type: 'string' },
          owner2_info: { type: 'string' },
          service_model: { type: 'string' },
          typical_client: { type: 'string' },
          other_firm_notes: { type: 'string' },
          aum: { type: 'string' },
          employees: { type: 'string' },
          fee_structure: { type: 'string' },
          platform_technology: { type: 'string' },
          awards: { type: 'string' },
        },
      },
    },
  },
}

const DRAFT_PROMPT = (firm, email1Text) => `
You are drafting the custom middle paragraph of a week-2 follow-up email from AJ at
Newry to the owner of ${firm.name}, on behalf of Sequoia Financial Group ($30-32B AUM,
expanding into the ${market.region_label} market with Eide Bailly's support).

The email has a FIXED opening and closing already written — you are writing ONLY the
middle paragraph, 3-5 sentences.

${email1Text
  ? `EMAIL 1 ALREADY SENT TO THIS FIRM (do not repeat this angle or these specific facts):\n${email1Text}\n`
  : `No record of email 1's exact text was found for this firm — pick an angle grounded in the research below.`}

TONE SHIFT vs. email 1: email 1 led with "what caught our attention about you" (flattery
on their story/philosophy). This follow-up should instead surface a specific structural
tension the firm faces — succession, scaling a high-touch model, bandwidth on a small
team, concentration risk, capacity constraints — and explain how Sequoia's approach
addresses that tension WITHOUT disrupting what already works (investment process,
client relationships, culture, founder involvement all stay intact).

MATCH THIS REGISTER (real examples from past follow-ups):
"A hard cap of 70 clients per advisor is a structural commitment to service quality
that most firms never make, and ARQ's consistent AUM growth reflects how well clients
respond to that model. As the practice grows, that capacity discipline creates real
constraints on how many of the right clients you can serve. Sequoia's platform is built
to support exactly this kind of high-touch advisory model, adding infrastructure and
resources that allow the quality of the client relationship to remain as it is, even as
the firm scales."

"Strong AUM growth as a solo CFP reflects a relationship-first model that clients are
clearly responding to. For a single-advisor practice managing a growing book, sustaining
that quality of service as the practice expands is a real challenge. Sequoia's
partnership model adds platform support and continuity infrastructure without requiring
you to give up the direct client relationships that made the practice what it is."

RULES:
- Ground the paragraph in a SPECIFIC fact from the research below — not a generic claim
- Never say "acquisition" or "sale" — use "partnership," "next chapter," "conversation"
- No superlatives or marketing language
- 3-5 sentences total, no more
- Return only the paragraph text — no greeting, no signature, no JSON

FIRM RESEARCH:
${JSON.stringify(firm, null, 2)}
`

// ─── HELPERS ─────────────────────────────────────────────────────────────────

function normalizeName(name) {
  return (name || '')
    .toLowerCase()
    .replace(/\b(llc|l\.l\.c\.|inc|incorporated|corp|corporation|co|company|ltd|l\.p\.|lp|group|advisors|advisers|wealth|management|partners|capital|financial)\b/g, '')
    .replace(/[^a-z0-9]/g, '')
    .trim()
}

function findEmail1(firmName, parsedEmails) {
  const norm = normalizeName(firmName)
  let match = parsedEmails.find(e => normalizeName(e.firm_name) === norm)
  if (!match) {
    match = parsedEmails.find(e => {
      const en = normalizeName(e.firm_name)
      return en && norm && (en.includes(norm) || norm.includes(en))
    })
  }
  return match || null
}

function firstName(fullName) {
  if (!fullName) return null
  return fullName.trim().split(/\s+/)[0]
}

// ─── MAIN ─────────────────────────────────────────────────────────────────────

// Phase 0: Parse initial-outreach doc(s) for email-1 text per firm
phase('Parse examples')

const parsedEmails = await agent(PARSE_PROMPT, { schema: PARSE_SCHEMA }).then(r => r ? r.firms : [])
log(`Parsed ${parsedEmails.length} firm email-1 blocks from the ${marketName} initial-outreach doc(s)`)

// Phase 1: Select firms due for follow-up
phase('Select firms')

let firms = await agent(SELECT_PROMPT, { schema: SELECT_SCHEMA }).then(r => r ? r.firms : [])
if (limit) firms = firms.slice(0, limit)
log(`${firms.length} firms selected for follow-up drafting${TEST_MODE ? ' (test base)' : ' (production)'}`)

if (!firms.length) {
  log('No firms to draft — nothing due for follow-up')
  return { firms_drafted: 0 }
}

// Phase 2: Draft the custom paragraph per firm
phase('Draft')

const drafted = await pipeline(
  firms,
  (firm) => {
    const match = findEmail1(firm.name, parsedEmails)
    if (!match) log(`No email-1 match found for "${firm.name}" — drafting without contrast`)
    return agent(DRAFT_PROMPT(firm, match ? match.email_text : null), { label: `draft:${firm.name}`, phase: 'Draft' })
      .then(paragraph => ({ firm, match, paragraph }))
  }
)

const withParagraphs = drafted.filter(Boolean)
log(`Drafted ${withParagraphs.length}/${firms.length} custom paragraphs`)

// Phase 3: Assemble full emails (deterministic — no agent needed)
const assembled = withParagraphs.map(({ firm, match, paragraph }) => {
  const contactName = (match && match.contact_name) || firstName(firm.primary_owner) || firm.name
  const fullText = `${OPENING(contactName)}\n\n${paragraph}\n\n${CLOSING}`
  return { firm_name: firm.name, contact_name: contactName, email1_matched: !!match, full_text: fullText }
})

// Phase 4: Write review doc
phase('Output')

await agent(
  `Create a Word document at:
   ${OUTPUT_DOC}

   Format it like "2026.06.04 Phoenix Second Emails.docx" in the same folder — for
   each firm, a bold heading with the firm name, then the full assembled email text as
   plain paragraphs (blank line between the greeting, opening, custom paragraph, and
   closing).

   Firms and their assembled emails, in order:
   ${JSON.stringify(assembled, null, 2)}

   At the very top of the doc, add a short note: "DRAFT — for review before sending.
   ${assembled.filter(a => !a.email1_matched).length} firm(s) below had no matching
   email-1 text found; double-check those paragraphs don't repeat email 1's angle."

   Use python-docx or the docx skill conventions (US Letter, Calibri or Arial, dark
   blue firm-name headings to match the existing Sequoia outreach docs in that folder).`,
  { label: 'output:doc' }
)

log(`Follow-up drafts written to: ${OUTPUT_DOC}`)

return {
  market: marketName,
  test_mode: TEST_MODE,
  firms_selected: firms.length,
  firms_drafted: withParagraphs.length,
  unmatched_email1: assembled.filter(a => !a.email1_matched).map(a => a.firm_name),
  output_doc: OUTPUT_DOC,
  results: assembled,
}
