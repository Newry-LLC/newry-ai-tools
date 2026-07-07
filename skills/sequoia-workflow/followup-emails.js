export const meta = {
  name: 'sequoia-followup-emails',
  description: 'Draft Phase-2 (week 1-2 follow-up) outreach emails for a Sequoia market — one custom paragraph per firm, wrapped in the fixed opening/closing template',
  phases: [
    { title: 'Select firms', detail: 'Read Airtable for all firms in the market (cached up to 24h)' },
    { title: 'Parse examples', detail: 'Extract email-1 text for every firm from the initial-outreach doc(s) (cached up to 24h)' },
    { title: 'Check network connections', detail: 'Cross-reference firms against the Connections table (cached up to 24h)' },
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
    other_notes_field: 'Other firm notes',
    date1_field_id: 'fldReRFJNhcNJ0cHS',
    date2_field_id: 'fldl5L8BgVQTRTJVD',
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
    other_notes_field: 'Other Firm Notes',
    date1_field_id: 'fldaahqFE6VBO06mD',
    date2_field_id: 'fldVf3QKt06IWX6fK',
  },
}

// ─── CONFIG ──────────────────────────────────────────────────────────────────

// `args` arrives as a JSON-stringified string in this environment, not a parsed
// object — confirmed via a minimal diagnostic run. Parse it defensively so this
// works whether the platform ever fixes that or not.
const parsedArgs = typeof args === 'string' ? JSON.parse(args) : (args || {})
log(`args received: ${JSON.stringify(parsedArgs)}`)

const marketName = parsedArgs.market || 'Phoenix'
const market = MARKETS[marketName]
if (!market) throw new Error(`Unknown market: ${marketName}. Valid: ${Object.keys(MARKETS).join(', ')}`)

// Default is TRUE only when the market has a test base — pass { test: false } to
// use production. Markets with no test base (e.g. Walnut Creek) always read
// production directly; that's safe here because this workflow never writes to
// Airtable, only reads it and produces a Word doc. This mirrors the lesson from
// the 7/2 write-back incident: never write to production unless opted in on purpose.
const hasTestBase = !!market.test_base_id
const TEST_MODE = hasTestBase && parsedArgs.test !== false

const BASE_ID = TEST_MODE ? market.test_base_id : market.base_id
const TABLE_ID = TEST_MODE ? market.test_table_id : market.table_id

const limit = parsedArgs.limit || null

// Airtable + doc-parse results are cached to disk and reused for up to this long —
// this is read-heavy research data that changes slowly, and iterating on the Draft
// prompt (register, wording) shouldn't cost a fresh live pull every run. Pass
// { refresh_cache: true } to force a live pull regardless of cache age.
const CACHE_DIR =
  'C:\\Users\\sshank\\OneDrive - Newry Corp\\Desktop\\Newry non-project and backup\\AI Tool Building\\Building Tools for Newry\\skills\\sequoia-workflow\\cache\\'
const CACHE_MAX_AGE_HOURS = 24
const FORCE_REFRESH = !!parsedArgs.refresh_cache
const marketSlug = marketName.replace(/\s+/g, '_')
const FIRMS_CACHE_PATH = `${CACHE_DIR}${marketSlug}-firms.json`
const EMAILS_CACHE_PATH = `${CACHE_DIR}${marketSlug}-email1-parsed.json`
// Connections table is base-wide (spans every market, not just this one), so its cache is NOT
// market-scoped — one shared file reused across Phoenix/Walnut Creek/future markets.
const CONNECTIONS_CACHE_PATH = `${CACHE_DIR}connections-all-markets.json`

const CACHE_CHECK_STEP = (cachePath) => FORCE_REFRESH
  ? 'refresh_cache was requested — ignore any cache, always proceed to the live step below.'
  : `If it prints FRESH, read "${cachePath}" with cat, parse its "firms" array, and skip straight to the return step using that array. If it prints STALE_OR_MISSING, proceed to the live step below.`

const OUTPUT_DOC = parsedArgs.output_path ||
  `${SEQUOIA_FOLDER}${marketName} Second Emails - Draft.docx`

// ─── FIXED TEMPLATE (from 2026.06.04 Phoenix Second Emails.docx — market-agnostic) ──

const OPENING = (contactName) =>
  `${contactName},\n\nI wanted to follow up on my earlier note. As I mentioned before, Sequoia is looking to expand in your region, and I thought it might be helpful to share a bit more context on how they approach partnership.`

const CLOSING =
  `Sequoia is deliberate about the number of partnerships they pursue, focusing on cultural and service-model alignment above all else. This has supported a ~98% client and advisor retention while generating 18-20% organic growth net of market. Sequoia takes their time pacing integrations, ensuring client service models remain intact, and founders stay meaningfully involved in ways that reinforce what they have built.\n\nIf it would be useful, I'd welcome a brief, low-pressure conversation to share how this works in practice and learn how you're thinking about the firm's next chapter. If now isn't the right time, I completely understand.\n\nBest,`

// ─── PROMPTS ─────────────────────────────────────────────────────────────────

const PY = 'C:/Users/sshank/AppData/Local/Programs/Python/Python314/python.exe'

const PARSE_PROMPT = market.doc_style === 'phoenix' ? `
Step 1 — check the cache. Run this exact Bash command:
  test -f "${EMAILS_CACHE_PATH}" && find "${EMAILS_CACHE_PATH}" -mmin -${CACHE_MAX_AGE_HOURS * 60} | grep -q . && echo FRESH || echo STALE_OR_MISSING
${CACHE_CHECK_STEP(EMAILS_CACHE_PATH)}

Step 2 — live parse (only if you reached this step):
Extract outreach email text from the Word document at:
${market.initial_docs[0]}

Read it with this exact command (fastest reliable path — don't try pandoc first):
${PY} -c "import docx; d = docx.Document(r'${market.initial_docs[0]}'); [print(p.text) for p in d.paragraphs]"

The doc is a series of blocks, each starting
with a firm name as a heading, followed by email body text. Some firms have a single
version. Some firms have a second, labeled "Second version:" or "Second:" — a fuller
A/B alternative to the first paragraph.

Extract EVERY firm block in the doc — not a filtered subset. This cache is shared
across every future run of this skill, including runs for a different set of firms
than today's, so it must cover the whole doc.

RULE: For any firm with a labeled second version, use ONLY that second
version's text as the firm's email_text and discard the first version entirely. For
firms with only one version, use that version.

Build a "firms" array: [ { "firm_name": "...", "contact_names": [], "email_text": "..." } ]
Preserve the email_text verbatim (don't summarize or edit it). Leave contact_names as
[] if the doc doesn't state anyone directly.

Write the cache: run mkdir -p "${CACHE_DIR}" then write a small Python script (don't
hand-write the JSON in a shell heredoc — escaping breaks) that gets the current time via
\`date -u +%Y-%m-%dT%H:%M:%SZ\` and does
json.dump({"fetched_at": "<that timestamp>", "firms": [...]}, open(r"${EMAILS_CACHE_PATH}", "w"))
Then proceed to the return step below with this freshly parsed array.

Return: call the tool with { "firms": [...] } — the array either loaded from cache
(Step 1) or just parsed and cached (Step 2).
` : `
Step 1 — check the cache. Run this exact Bash command:
  test -f "${EMAILS_CACHE_PATH}" && find "${EMAILS_CACHE_PATH}" -mmin -${CACHE_MAX_AGE_HOURS * 60} | grep -q . && echo FRESH || echo STALE_OR_MISSING
${CACHE_CHECK_STEP(EMAILS_CACHE_PATH)}

Step 2 — live parse (only if you reached this step):
Extract outreach paragraphs from these two Word documents (batch 1 and batch 2 of the
same campaign — read both):
${market.initial_docs[0]}
${market.initial_docs[1]}

Read each with this exact command (fastest reliable path — don't try pandoc first):
${PY} -c "import docx; d = docx.Document(r'<PATH>'); [print(p.text) for p in d.paragraphs]"
(substitute each doc's path for <PATH>, run it twice)

Skip the "Standard Opening" / "Standard
Closing" / "Subject Line Format" boilerplate at the top of each doc — only look in the
"Custom Paragraphs by Firm" section. Each firm entry looks like:
  "[Firm Name] - [Contact Name(s)]"
  "Subject: ..."
  <custom paragraph text>

Extract EVERY firm entry in both docs — not a filtered subset. This cache is shared
across every future run of this skill, including runs for a different set of firms
than today's, so it must cover both docs in full.

Build a "firms" array: [ { "firm_name": "...", "contact_names": [], "email_text": "..." } ]
contact_names is an array of every individual person's name listed after the dash,
verbatim, in order — e.g. "Jeff Berry, Matt Bennitt, Kevin Connell, and Nancy Tuck"
becomes ["Jeff Berry", "Matt Bennitt", "Kevin Connell", "Nancy Tuck"]. If the heading
names one person plus "and the [Firm] Team" (no other individuals), return just that one
person. Never invent a name that isn't literally in the heading. Preserve email_text
verbatim.

Write the cache: run mkdir -p "${CACHE_DIR}" then write a small Python script (don't
hand-write the JSON in a shell heredoc — escaping breaks) that gets the current time via
\`date -u +%Y-%m-%dT%H:%M:%SZ\` and does
json.dump({"fetched_at": "<that timestamp>", "firms": [...]}, open(r"${EMAILS_CACHE_PATH}", "w"))
Then proceed to the return step below with this freshly parsed array.

Return: call the tool with { "firms": [...] } — the array either loaded from cache
(Step 1) or just parsed and cached (Step 2).
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
          contact_names: { type: 'array', items: { type: 'string' } },
          email_text: { type: 'string' },
        },
      },
    },
  },
}

// Deterministic — one exact tool call, no exploration. Terminal-status exclusion
// happens afterward in plain JS (see TERMINAL_STATUSES below), not agent reasoning,
// since that's cheap and precise as code but slow and fuzzy as agent judgment.
const SELECT_FIELD_NAMES = [
  'Name', 'Primary Owner', 'Owner Notes', 'Owner 2', 'Owner 2 Info', 'Service Model',
  'Typical Client', market.other_notes_field, 'AUM', 'Employees', 'Fee Structure',
  'Platform / Technology', 'Awards', 'Status', 'Date: 1st Email', 'Date: 2nd Email',
]

// No date-based filter here on purpose: the Date:1st/2nd Email fields are
// under-logged (sends happen without the tracker being updated), so gating
// on them silently drops firms that were genuinely emailed. Fetch everyone
// and let only_firms / TERMINAL_STATUSES (a real reported outcome, not a
// logging artifact) do the filtering instead.
const SELECT_PROMPT = `
Step 1 — check the cache. Run this exact Bash command:
  test -f "${FIRMS_CACHE_PATH}" && find "${FIRMS_CACHE_PATH}" -mmin -${CACHE_MAX_AGE_HOURS * 60} | grep -q . && echo FRESH || echo STALE_OR_MISSING
${CACHE_CHECK_STEP(FIRMS_CACHE_PATH)}

Step 2 — live fetch (only if you reached this step):
Call the Airtable MCP tool "list_records_for_table" with EXACTLY these arguments —
do not call get_table_schema, list_bases, search_bases, or any write tool first:

{
  "baseId": "${BASE_ID}",
  "tableId": "${TABLE_ID}",
  "fieldIds": ${JSON.stringify(SELECT_FIELD_NAMES)},
  "pageSize": ${limit ? Math.min(limit * 5, 200) : 200}
}

Build a "firms" array from the results in this shape: [ { "record_id": "...", "name": "...",
"primary_owner": "...", "owner_notes": "...", "owner2": "...", "owner2_info": "...",
"service_model": "...", "typical_client": "...", "other_firm_notes": "...",
"aum": "...", "employees": "...", "fee_structure": "...", "platform_technology": "...",
"awards": "...", "status": "..." } ]
Map "${market.other_notes_field}" to other_firm_notes. Use empty string for anything
blank — don't omit fields. Don't filter or interpret anything else yourself.

Write the cache: run mkdir -p "${CACHE_DIR}" then write a small Python script (don't
hand-write the JSON in a shell heredoc — escaping breaks) that gets the current time via
\`date -u +%Y-%m-%dT%H:%M:%SZ\` and does
json.dump({"fetched_at": "<that timestamp>", "firms": [...]}, open(r"${FIRMS_CACHE_PATH}", "w"))
Then proceed to the return step below with this freshly fetched array.

Return: call the tool with { "firms": [...] } — the array either loaded from cache
(Step 1) or just fetched and cached (Step 2).
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
          status: { type: 'string' },
        },
      },
    },
  },
}

// Connections table (tblEX62L13GxXSlhD, base appCQDjrwviHioJeL) holds warm-connection research
// between Sequoia/Eide Bailly/Newry people and target-firm owners — a separate research track
// (see network-mapping-rubric.md) run independently of the firm/owner Airtable fields. It spans
// every market, so this fetch is NOT filtered by market and the cache is shared across markets.
const CONNECTIONS_TABLE_ID = 'tblEX62L13GxXSlhD'

const CONNECTIONS_PROMPT = `
Step 1 — check the cache. Run this exact Bash command:
  test -f "${CONNECTIONS_CACHE_PATH}" && find "${CONNECTIONS_CACHE_PATH}" -mmin -${CACHE_MAX_AGE_HOURS * 60} | grep -q . && echo FRESH || echo STALE_OR_MISSING
${CACHE_CHECK_STEP(CONNECTIONS_CACHE_PATH)}

Step 2 — live fetch (only if you reached this step):
Call the Airtable MCP tool "list_records_for_table" with EXACTLY these arguments —
do not call get_table_schema, list_bases, search_bases, or any write tool first:

{
  "baseId": "${MARKETS['Phoenix'].base_id}",
  "tableId": "${CONNECTIONS_TABLE_ID}",
  "pageSize": 100
}
This table is small (well under 100 records) — one call should return everything. If the
response indicates more records exist, page through with the cursor until exhausted.

Build a "connections" array from the results in this shape: [ { "target_firm": "...",
"target_contact": "...", "internal_contact": "...", "company": "...", "connection": "...",
"status": "...", "call_to_action": "..." } ]
"company" is the internal person's affiliation (Newry, Sequoia, or Eide Bailly) — map from
the singleSelect field's name. "status" is the singleSelect field's name (e.g. "Awaiting
email", "In progress", "Introduction made", "No connection"). Use empty string for anything
blank — don't omit fields. Don't filter or interpret anything else yourself — return every
record, including ones for other markets (Colorado, Nevada, Arizona); this script filters to
the current market's firms afterward.

Write the cache: run mkdir -p "${CACHE_DIR}" then write a small Python script (don't
hand-write the JSON in a shell heredoc — escaping breaks) that gets the current time via
\`date -u +%Y-%m-%dT%H:%M:%SZ\` and does
json.dump({"fetched_at": "<that timestamp>", "connections": [...]}, open(r"${CONNECTIONS_CACHE_PATH}", "w"))
Then proceed to the return step below with this freshly fetched array.

Return: call the tool with { "connections": [...] } — the array either loaded from cache
(Step 1) or just fetched and cached (Step 2).
`

const CONNECTIONS_SCHEMA = {
  type: 'object',
  required: ['connections'],
  properties: {
    connections: {
      type: 'array',
      items: {
        type: 'object',
        required: ['target_firm'],
        properties: {
          target_firm: { type: 'string' },
          target_contact: { type: 'string' },
          internal_contact: { type: 'string' },
          company: { type: 'string' },
          connection: { type: 'string' },
          status: { type: 'string' },
          call_to_action: { type: 'string' },
        },
      },
    },
  },
}

const TERMINAL_STATUSES = ['declined', 'not a fit', 'not interested', 'closed', 'dead', 'pass']

const DRAFT_PROMPT = (firm, email1Text, contactName, otherNames) => `
You are drafting the custom middle paragraph of a week-2 follow-up email from AJ at
Newry to ${contactName}, an owner of ${firm.name}, on behalf of Sequoia Financial Group
($30-32B AUM, expanding into the ${market.region_label} market with Eide Bailly's
support).

The email is addressed directly to ${contactName} (that's who it opens "${contactName},").
Refer to ${contactName} as "you"/"your" throughout — never refer to them by name in the
third person (e.g. NOT "Bill's leadership," write "your leadership").

NAMES YOU MAY USE: ${contactName}${otherNames && otherNames.length ? `, ${otherNames.join(', ')}` : ''}.
${otherNames && otherNames.length
  ? `${otherNames.join(' and ')} may be mentioned by name, in third person, if it reads naturally — email 1 named them alongside ${contactName}, so they're the only other people you may name.`
  : `Email 1 named no one else at this firm — do NOT name any other individual, even if
one appears in the firm research below (owner2, owner_notes, etc.). If you need to
reference the rest of the firm, say "your team" or "your partners," never a specific
name that wasn't in email 1.`}
The firm research below is for factual grounding only — never a source of names to use.

The email has a FIXED opening and closing already written — you are writing ONLY the
middle paragraph.

${email1Text
  ? `EMAIL 1 ALREADY SENT TO THIS FIRM (do not repeat this angle or these specific facts):\n${email1Text}\n`
  : `No record of email 1's exact text was found for this firm — pick an angle grounded in the research below.`}

TONE: email 1 led with "what caught our attention about you" (flattery on their story/
philosophy). This follow-up should stay POSITIVE and OPPORTUNITY-framed throughout —
never describe the firm as thin, aging, at-risk, stretched, or lacking. Frame Sequoia's
fit as helping the firm do MORE of what already works (grow, extend, safeguard capacity,
plan ahead) — not as fixing a weakness. Do NOT use phrases like "little room," "thin,"
"aging," "key-person risk," "concentration risk," or anything that reads as pointing out
a vulnerability.

MATCH THIS REGISTER AND LENGTH (real approved examples):
"The concentrated, relationship-driven model you've built is exactly what Sequoia is
designed to support — and to help grow. Their platform adds operating and investment
infrastructure around your existing team, so the people your clients already trust keep
doing what they do, with more room to take on new relationships and plan ahead on your
own terms."

"The founder-level attention you bring to entrepreneur clients is hard to scale — and
that's exactly where Sequoia's platform helps. They take on the operating and
administrative load so you can stay focused on investment strategy and client
relationships as the firm grows, extending what makes the firm distinctive to more
clients without building out a bigger back office."

RULES:
- Do not reuse email 1's specific descriptive words or phrases, even paraphrased close to
  verbatim (e.g. if email 1 called something a "niche" or "proprietary process," don't
  call it that again — describe the same underlying fact in genuinely different words).
- Ground the paragraph in a SPECIFIC, QUALITATIVE fact from the research below (service
  model, niche, client type, structure) — never a specific dollar AUM figure or headcount
  number. Reference scale only in general terms if at all (e.g. "a concentrated team,"
  "a firm of your scale"), never exact figures.
- Never say "acquisition" or "sale" — use "partnership," "next chapter," "conversation"
- No superlatives or marketing language
- ${contactName} is "you"/"your" — never third person about them.
- 2-3 sentences, ~55-70 words total — match the LENGTH of the register examples above.
  Do not pad to 4-5 sentences or run past ~70 words.
- Call the tool with the "paragraph" field set to ONLY the finished paragraph text.
  Do not put reasoning, notes about missing research fields, or any sentence starting
  "Given...", "Since...", or "Working..." into that field — think it through silently,
  then write just the final paragraph.

FIRM RESEARCH:
${JSON.stringify(firm, null, 2)}
`

const DRAFT_SCHEMA = {
  type: 'object',
  required: ['paragraph'],
  properties: { paragraph: { type: 'string' } },
}

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

// Phase 0: Select firms due for follow-up
phase('Select firms')

let firms = await agent(SELECT_PROMPT, { schema: SELECT_SCHEMA }).then(r => r ? r.firms : [])
if (!TEST_MODE) {
  firms = firms.filter(f => !TERMINAL_STATUSES.some(s => (f.status || '').toLowerCase().includes(s)))
}
if (parsedArgs.only_firms && parsedArgs.only_firms.length) {
  const wanted = parsedArgs.only_firms.map(normalizeName)
  firms = firms.filter(f => wanted.includes(normalizeName(f.name)))
  firms.sort((a, b) => wanted.indexOf(normalizeName(a.name)) - wanted.indexOf(normalizeName(b.name)))
  log(`Filtered to only_firms: ${firms.length}/${parsedArgs.only_firms.length} requested names matched`)
}
if (limit) firms = firms.slice(0, limit)
log(`${firms.length} firms selected for follow-up drafting${TEST_MODE ? ' (test base)' : ' (production)'} (cache refreshed at most every ${CACHE_MAX_AGE_HOURS}h)`)

if (!firms.length) {
  log('No firms to draft — nothing due for follow-up')
  return { firms_drafted: 0 }
}

// Phase 1: Parse initial-outreach doc(s) for email-1 text — cached, covers every firm
// in the doc(s) regardless of which ones are selected this run (see PARSE_PROMPT)
phase('Parse examples')

const parsedEmails = await agent(PARSE_PROMPT, { schema: PARSE_SCHEMA }).then(r => r ? r.firms : [])
log(`Parsed ${parsedEmails.length} email-1 blocks from the ${marketName} initial-outreach doc(s) (cache refreshed at most every ${CACHE_MAX_AGE_HOURS}h)`)

// Phase 1.5: Cross-reference firms against the Connections table (warm-intro research —
// a separate track from firm/owner Airtable fields, see network-mapping-rubric.md). A firm
// with an open connection here may already have a warm-intro conversation in flight through
// a different person — worth knowing before finalizing a cold follow-up.
phase('Check network connections')

const allConnections = await agent(CONNECTIONS_PROMPT, { schema: CONNECTIONS_SCHEMA }).then(r => r ? r.connections : [])
log(`Loaded ${allConnections.length} connection records across all markets (cache refreshed at most every ${CACHE_MAX_AGE_HOURS}h)`)

function findConnections(firmName, connections) {
  const norm = normalizeName(firmName)
  return connections.filter(c => {
    const cn = normalizeName(c.target_firm)
    return cn && norm && (cn.includes(norm) || norm.includes(cn))
  })
}

// Phase 2: Draft the custom paragraph per firm
phase('Draft')

const drafted = await pipeline(
  firms,
  (firm) => {
    const match = findEmail1(firm.name, parsedEmails)
    if (!match) log(`No email-1 match found for "${firm.name}" — drafting without contrast`)
    // Filter out collective phrases like "The Ohana Team" — not a person's name,
    // just email 1's way of saying "no individual named, address the firm."
    const realNames = (match && match.contact_names || [])
      .filter(n => n && !/^the\s/i.test(n.trim()) && !/\bteam\b/i.test(n))
    const namesFromEmail1 = realNames.length ? realNames : (firm.primary_owner ? [firm.primary_owner] : [firm.name])
    const firstNames = namesFromEmail1.map(firstName).filter(Boolean)
    const contactName = firstNames[0] || firm.name
    const otherNames = firstNames.slice(1)
    const connections = findConnections(firm.name, allConnections)
    return agent(DRAFT_PROMPT(firm, match ? match.email_text : null, contactName, otherNames), { label: `draft:${firm.name}`, phase: 'Draft', schema: DRAFT_SCHEMA })
      .then(r => ({ firm, match, contactName, connections, paragraph: r ? r.paragraph : '' }))
  }
)

const withParagraphs = drafted.filter(Boolean)
log(`Drafted ${withParagraphs.length}/${firms.length} custom paragraphs`)

// Phase 3: Assemble full emails (deterministic — no agent needed)
const assembled = withParagraphs.map(({ firm, match, contactName, connections, paragraph }) => {
  const fullText = `${OPENING(contactName)}\n\n${paragraph}\n\n${CLOSING}`
  return {
    firm_name: firm.name, contact_name: contactName, email1_matched: !!match, full_text: fullText,
    connections: (connections || []).map(c => ({
      target_contact: c.target_contact || '', internal_contact: c.internal_contact || '',
      company: c.company || '', connection: c.connection || '', status: c.status || '',
      call_to_action: c.call_to_action || '',
    })),
  }
})
const firmsWithConnections = assembled.filter(a => a.connections.length)
if (firmsWithConnections.length) {
  log(`${firmsWithConnections.length} firm(s) have an open network connection on file: ${firmsWithConnections.map(a => a.firm_name).join(', ')}`)
}

// Phase 4: Write review doc — ready-to-run script, no design decisions left to the agent
phase('Output')

const noteText = `DRAFT -- for review before sending. ${assembled.filter(a => !a.email1_matched).length} firm(s) below had no matching email-1 text found; double-check those paragraphs don't repeat email 1's angle.`

const DOC_SCRIPT = `
import docx, json
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Parsed via json.loads, not embedded as a Python literal — JSON's true/false/null
# are not valid Python syntax (True/False/None), which broke this exact script
# on the previous run and cost a full error-Edit-rerun cycle.
data = json.loads(r"""${JSON.stringify({ note: noteText, firms: assembled })}""")

doc = docx.Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.left_margin = section.right_margin = Inches(1)
section.top_margin = section.bottom_margin = Inches(1)

note_p = doc.add_paragraph()
note_run = note_p.add_run(data['note'])
note_run.bold = True
note_run.font.size = Pt(11)
note_run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
note_run.font.name = 'Calibri'
doc.add_paragraph()

for firm in data['firms']:
    heading = doc.add_paragraph()
    hrun = heading.add_run(firm['firm_name'])
    hrun.bold = True
    hrun.font.size = Pt(14)
    hrun.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    hrun.font.name = 'Calibri'
    if firm.get('connections'):
        net_color = RGBColor(0x1F, 0x4E, 0x8C)
        label_p = doc.add_paragraph()
        lrun = label_p.add_run('*** NETWORK CONNECTION ON FILE -- check before finalizing; modify this email if a warm connection comes through ***')
        lrun.bold = True
        lrun.font.size = Pt(11)
        lrun.font.color.rgb = net_color
        lrun.font.name = 'Calibri'
        for c in firm['connections']:
            line = f"{c['target_contact']} <-> {c['internal_contact']} ({c['company']}) -- {c['connection']} Status: {c['status']}."
            cp = doc.add_paragraph(line)
            for r in cp.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(11)
                r.font.color.rgb = net_color
        doc.add_paragraph()
    for block in firm['full_text'].split(chr(10)+chr(10)):
        p = doc.add_paragraph(block)
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.size = Pt(11)
    doc.add_paragraph()

doc.save(r"${OUTPUT_DOC}")
print("saved")
`

await agent(
  `Run this exact Python script via Bash to produce the review doc — write it to a temp
   .py file and execute with: C:/Users/sshank/AppData/Local/Programs/Python/Python314/python.exe
   Do not modify the script or design your own version — just run it as-is and confirm
   it printed "saved". If it errors, fix only the specific error and re-run — don't
   rewrite the approach.

   ${DOC_SCRIPT}`,
  { label: 'output:doc' }
)

log(`Follow-up drafts written to: ${OUTPUT_DOC}`)

return {
  market: marketName,
  test_mode: TEST_MODE,
  firms_selected: firms.length,
  firms_drafted: withParagraphs.length,
  unmatched_email1: assembled.filter(a => !a.email1_matched).map(a => a.firm_name),
  firms_with_network_connections: firmsWithConnections.map(a => a.firm_name),
  output_doc: OUTPUT_DOC,
  results: assembled,
}
