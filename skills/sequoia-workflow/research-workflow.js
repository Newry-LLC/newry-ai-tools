export const meta = {
  name: 'sequoia-research',
  description: 'Full Sequoia M&A pipeline: ingest FINTRX → research firms → draft emails → write to Airtable',
  phases: [
    { title: 'Ingest', detail: 'Parse FINTRX export, filter by HNW threshold, create Airtable records' },
    { title: 'Research', detail: 'One agent per firm: web research on firm + owners in parallel' },
    { title: 'Draft emails', detail: 'One agent per firm: write custom outreach paragraph' },
    { title: 'Write back', detail: 'Update Airtable records with research + email drafts' },
  ],
}

// ─── CONFIG ──────────────────────────────────────────────────────────────────

// Set to true to run against the test base instead of production
const TEST_MODE = (args && args.test) || false

const BASE_ID = TEST_MODE ? 'appnnsUPTbfAK6kaR' : 'appCQDjrwviHioJeL'

// Market name → Airtable table ID
const MARKET_TABLES = TEST_MODE
  ? { 'Phoenix': 'tbllhUPpeD22MHXoe' }
  : {
      'Denver':       'tblReX4udswCBuuPF',
      'Las Vegas':    'tblrFtuuAk1pkhW2I',
      'Phoenix':      'tblk6rPjUGs5ZVdgn',
      'Walnut Creek': 'tblAPbuJAbVkNG1bz',
    }

// Per-market field IDs for the fields we write to.
// Each table has slightly different IDs for the same logical field.
const FIELD_IDS = {
  // Test base — Phoenix table
  'Phoenix_TEST': {
    name:              'fldylvkQbDajMGkKC',
    website:           'fldrWI99ERvrkQaYT',
    primary_owner:     'fldSLB1kdaUdbgPpA',
    owner_notes:       'fld1ITzddGFpkPFQ3',
    owner2:            'fldm4UvVtydpRbrRS',
    service_model:     'fldiw5gORMPyf2u2E',
    typical_client:    'fldM5JyhlpjOTZiie',
    other_notes:       'fldbIEJrIps1D5YE6',
    research_status:   'fld3u1yPMTSwLm932',
    outreach_strategy: null,
    email_draft:       'fldIjgDI5pWoGDpbx',
  },
  'Denver': {
    name:              'fldO72Bk7MFh8aHzN',
    website:           'fldLVSlheNrzPXVZR',
    primary_owner:     null,               // Denver uses "Owner (age)" — read-only context
    owner_notes:       'fldtOVsoGezZ4Viim',
    owner2:            'fldiGZwvoCAoDXGNy',
    service_model:     'fldTRi3BPkaGnOesh',
    typical_client:    'fldpD66JeD5SUPJE4',
    other_notes:       'fldqdZ1NzgPKn2H53',
    research_status:   'fldEbRpCh7l77Mqj1',
    outreach_strategy: 'fldY6KMH9IwgQm4XE',
    av_notes:          'fldWr0wscfsHFnfwL',  // reuse for email draft
  },
  'Las Vegas': {
    name:              'fldeecGruWEKygin1',
    website:           'fld4baEtlvE701ZQR',
    primary_owner:     null,
    owner_notes:       'fldG14AYN2Fv1vqxa',
    owner2:            null,
    service_model:     'fldiNJZRlKaEYkLTy',
    typical_client:    'fldrvm6G5O34xe60V',
    other_notes:       'fldaN5HWZ9jmUcy1m',
    research_status:   'fldyEmzEC86vHEZiC',
    outreach_strategy: 'flddTCBiordD16zW9',
    av_notes:          null,
  },
  'Phoenix': {
    name:              'fldIKtKYCOGbMrRtO',
    website:           'fldg0DIxGVb9bEOJN',
    primary_owner:     'fldJzYAB3fFNWxhvo',
    owner_notes:       'fldEzuPa2EwuIevMM',
    owner2:            'fldQUGrfzWqhrKyIk',
    service_model:     'fldBSJy4jXZrlLDzV',
    typical_client:    'fldvaoXrz8XhAkLyC',
    other_notes:       'fldXq4geDmlLlTeIl',
    research_status:   'fldX1KJjiKlxWF7NB',
    outreach_strategy: null,
    email_draft:       'fldLea0W50D0fZLJ3',
  },
  'Walnut Creek': {
    name:              'fldDlIfIYazoF4XO5',
    website:           'fldPS42Y4MzVie5sX',
    primary_owner:     'fld7GUtXJClpJ2S8l',
    owner_notes:       'fldx7brbFAlmE42aN',
    owner2:            'fld7e1YIP5VU7e2NM',
    service_model:     'fldOR8sDklhMBlhtQ',
    typical_client:    'fldUqtE7Ll5yt2wL5',
    other_notes:       'fldmsubZm4b5YiinC',
    research_status:   'fldIzg1tBwouftsug',
    outreach_strategy: null,
    email_draft:       'fldQdVhbj5UzXY3iI',
  },
}

// ─── PROMPTS ─────────────────────────────────────────────────────────────────

const RESEARCH_PROMPT = (firm) => `
You are researching an independent RIA for Sequoia Financial Group's M&A business development pipeline.
Sequoia ($32B AUM) is looking for acquisition targets: independent RIAs with strong HNW client bases,
good culture fit, and thoughtful ownership.

Firm to research:
- Name: ${firm.name}
- Website: ${firm.website || 'unknown — find it via web search'}
- Known owners/partners: ${firm.known_owners || 'none listed — find from website and SEC ADV'}
- Airtable record ID: ${firm.record_id}

Sources to use (in order of preference):
1. Firm website — About page, team page, investment philosophy
2. SEC IAPD / ADV filing (adviserinfo.sec.gov) — AUM, client counts, ownership, disclosures
3. LinkedIn public profiles — career history, education, board roles
4. Web search — press mentions, awards, community roles

Capture for the FIRM:
- founding_year: when founded
- aum: assets under management (number + source)
- client_count: total accounts
- ownership_structure: solo, partners, family, employee-owned, etc.
- investment_philosophy: their stated approach in 1–2 sentences
- client_focus: who they serve (HNW, UHNW, Silicon Valley execs, retirees, etc.)
- service_model: fee-only, AUM-based, planning + investments, etc.
- typical_client: description of their ideal client
- differentiator: what makes them genuinely distinctive (the specific thing)
- founding_story: notable origin story if one exists
- awards_recognition: any Barron's, Forbes, industry rankings
- red_flags: compliance issues, focus mismatch, or anything disqualifying (blank if none)
- culture_notes: tone from website, community involvement, values signals

Capture for each PRIMARY OWNER / PARTNER (typically 1–3 people):
- name, title
- career_history: prior firms and tenures (be specific — firm names, years)
- education: school, degree, year if findable
- board_roles: nonprofit boards, advisory boards, associations (be specific)
- linkedin_url: if findable
- personal_notes: speaking, writing, community, anything distinctive

Return a single JSON object. Use empty string "" for fields you cannot find — do not omit fields.
`

const EMAIL_DRAFT_PROMPT = (firm, research) => `
You are drafting the custom paragraph for a warm outreach email from AJ Vakharia at Newry
to the owner(s) of ${firm.name}, on behalf of Sequoia Financial Group.

CONTEXT:
- Sequoia ($32B AUM) is expanding nationally and entering new markets with Eide Bailly's support
- The email structure is: standard opening (already written) + YOUR custom paragraph + standard closing (already written)
- You are writing ONLY the custom paragraph — 3–5 sentences

TONE AND STYLE (match these examples exactly):
"What drew us to Clarity Wealth Advisors was its depth of experience and genuine client-first philosophy. Building an independent, fee-only practice and sustaining it for over a decade reflects the kind of intentional culture we take seriously."

"Two things stand out about Avalon: its intellectual rigor and the longevity of its founding partnership. Deep roots in quantitative research — including the firm's proprietary 'Ada' dynamic allocation model — reflect a systematic discipline uncommon in boutique wealth management."

"Sentry stood out for the remarkable concentration and scale of its client relationships. A four-person firm managing over $2.4B, with average client assets near $13M, reflects a highly selective practice built around institutional-quality clients rather than volume."

RULES:
- Lead with the ONE thing that genuinely caught your attention — be specific, not generic
- Explain WHY that thing matters in 1–2 sentences
- End with a synthesis sentence connecting their firm's character to what Sequoia values
- Never mention "acquisition" — use "conversation," "partnership," "platform," "fit"
- Never use superlatives or marketing language ("world-class," "best-in-class")
- Write as if you actually read their ADV and website — because we did
- 3–5 sentences total. No more.

FIRM RESEARCH:
${JSON.stringify(research, null, 2)}

Return only the custom paragraph text. No subject line, no greeting, no JSON wrapper.
`

// ─── SCHEMA ──────────────────────────────────────────────────────────────────

const RESEARCH_SCHEMA = {
  type: 'object',
  required: ['firm', 'owners'],
  properties: {
    firm: {
      type: 'object',
      required: ['name', 'airtable_record_id', 'founding_year', 'aum', 'client_count',
                 'ownership_structure', 'investment_philosophy', 'client_focus',
                 'service_model', 'typical_client', 'differentiator', 'founding_story',
                 'awards_recognition', 'red_flags', 'culture_notes'],
      properties: {
        name:                 { type: 'string' },
        airtable_record_id:   { type: 'string' },
        founding_year:        { type: 'string' },
        aum:                  { type: 'string' },
        client_count:         { type: 'string' },
        ownership_structure:  { type: 'string' },
        investment_philosophy:{ type: 'string' },
        client_focus:         { type: 'string' },
        service_model:        { type: 'string' },
        typical_client:       { type: 'string' },
        differentiator:       { type: 'string' },
        founding_story:       { type: 'string' },
        awards_recognition:   { type: 'string' },
        red_flags:            { type: 'string' },
        culture_notes:        { type: 'string' },
      },
    },
    owners: {
      type: 'array',
      items: {
        type: 'object',
        required: ['name', 'title', 'career_history', 'education', 'board_roles', 'linkedin_url', 'personal_notes'],
        properties: {
          name:          { type: 'string' },
          title:         { type: 'string' },
          career_history:{ type: 'string' },
          education:     { type: 'string' },
          board_roles:   { type: 'string' },
          linkedin_url:  { type: 'string' },
          personal_notes:{ type: 'string' },
        },
      },
    },
  },
}

// ─── MAIN ─────────────────────────────────────────────────────────────────────

// args = { market: 'Phoenix', fintrx_path: 'C:/path/to/file.xlsx', test: true }
const market = (args && args.market) || 'Phoenix'
const fintrxPath = args && args.fintrx_path
const limit = (args && args.limit) || null
const tableId = MARKET_TABLES[market]
const fields = FIELD_IDS[TEST_MODE ? `${market}_TEST` : market]

if (!tableId) throw new Error(`Unknown market: ${market}. Valid: ${Object.keys(MARKET_TABLES).join(', ')}`)

// ─── Phase 0: Ingest FINTRX ──────────────────────────────────────────────────
// Only runs when a fintrx_path is provided. If skipped, loads from existing Airtable records.
let firmList = []

if (fintrxPath) {
  phase('Ingest')

  firmList = await agent(
    `Parse the FINTRX Excel export at: ${fintrxPath}

     Steps:
     1. Read the first sheet. Headers are in row 1.
     2. For each firm row, compute: pct_hnw = "$ High Net Worth Clients" / "Total AUM"
        - If Total AUM is 0 or missing, skip the firm.
     3. Apply filters:
        - DISCARD: pct_hnw < 0.60
        - LOW priority: 0.60 <= pct_hnw < 0.70
        - HIGH/MEDIUM priority: pct_hnw >= 0.70 (HIGH if also 3yr AUM Change > 0, else MEDIUM)
     4. For each firm that passes (pct_hnw >= 0.60), return:
        name, website (Website Address), city (Main Office City), state (Main Office State),
        aum (Total AUM), pct_hnw (computed, as decimal e.g. 0.73),
        total_clients (Total Client Count), avg_client_size (Average Client Size),
        employees (Employees), fee_structure (Fee Structure),
        three_yr_aum_change (3 Year AUM Change), accolades (Industry Accolades),
        priority (HIGH / MEDIUM / LOW), firm_crd (Firm CRD)

     Use Python with openpyxl to read the file. Run via Bash.
     Python path: C:/Users/sshank/AppData/Local/Programs/Python/Python314/python.exe
     ${limit ? `Return only the first ${limit} firms that pass the filter.` : ''}
     Return a JSON object with a single key "firms" containing the array.`,
    { schema: { type: 'object', required: ['firms'], properties: { firms: { type: 'array', items: { type: 'object', required: ['name', 'priority'] } } } } }
  ).then(r => r ? r.firms : [])

  // Enforce limit structurally — don't rely on the agent to honor it
  if (limit) firmList = firmList.slice(0, limit)

  log(`FINTRX: ${firmList.length} firms pass the 60% HNW threshold${limit ? ` (limited to ${limit})` : ''}`)

  // Create Airtable records for all firms
  await agent(
    `Create records in Airtable for these firms.

     IMPORTANT: Use ONLY these exact IDs. Do NOT call list_bases, search_bases, or list_tables_for_base.
     Base ID: ${BASE_ID}
     Table ID: ${tableId}

     Field mappings (use get_table_schema on base ${BASE_ID} table ${tableId} to confirm field IDs):
     - Name (${fields.name}): firm.name
     - Website (${fields.website}): firm.website
     - Priority: map HIGH→"High", MEDIUM→"Medium", LOW→"Low" using the Priority field
     - AUM, Total Clients, Employees, Fee Structure, Avg Client Size, 3yr AUM Change:
       write to their respective fields (look them up via get_table_schema on base ${BASE_ID} table ${tableId})

     Firms to create:
     ${JSON.stringify(firmList, null, 2)}

     Use Airtable MCP create_records_for_table. Batch in groups of 10. Return record IDs mapped to firm names.`,
    { schema: { type: 'object' } }
  )

  log(`Airtable records created for ${firmList.length} firms`)

} else {
  // Resume mode: load existing unresearched records from Airtable
  phase('Ingest')

  firmList = await agent(
    `Read all records from Airtable base ${BASE_ID}, table ${tableId} (${market}).
     Filter to records where Research Status (field ${fields.research_status}) is blank or "Not Started".
     For each record return: record_id, name, website, known_owners (Primary Owner field if present).
     Return a JSON object with a single key "firms" containing the array.`,
    { schema: { type: 'object', required: ['firms'], properties: { firms: { type: 'array', items: { type: 'object', required: ['record_id', 'name'] } } } } }
  ).then(r => r ? r.firms : [])

  log(`${market}: ${firmList.length} unresearched firms loaded from Airtable`)
}

if (!firmList || firmList.length === 0) {
  log('No firms to process — check FINTRX filter or Airtable records')
  return { market, firms_researched: 0, emails_drafted: 0 }
}

// ─── Phase 2: Research ────────────────────────────────────────────────────────
phase('Research')

const researchResults = await pipeline(
  firmList,
  (firm) => agent(
    RESEARCH_PROMPT(firm),
    {
      label: `research:${firm.name}`,
      phase: 'Research',
      schema: RESEARCH_SCHEMA,
    }
  )
)

const researched = researchResults.filter(Boolean)
log(`Research complete: ${researched.length}/${firmList.length} firms`)

// ─── Phase 3: Draft emails ────────────────────────────────────────────────────
phase('Draft emails')

const withEmails = await pipeline(
  researched,
  (result, originalFirm) => agent(
    EMAIL_DRAFT_PROMPT(firmList[researchResults.indexOf(result)], result),
    {
      label: `email:${result.firm.name}`,
      phase: 'Draft emails',
    }
  ).then(emailDraft => ({ ...result, email_draft: emailDraft }))
)

// ─── Phase 4: Write back to Airtable ─────────────────────────────────────────
phase('Write back')

await pipeline(
  withEmails.filter(Boolean),
  (result) => agent(
    `Update this Airtable record with firm research results.

     IMPORTANT: Use ONLY these exact IDs. Do NOT call list_bases, search_bases, or list_tables_for_base.
     Base ID: ${BASE_ID}
     Table ID: ${tableId}
     Record ID: ${result.firm.airtable_record_id}

     Write these fields using update_records_for_table:
     - Service Model (${fields.service_model}): "${result.firm.service_model}"
     - Typical Client (${fields.typical_client}): "${result.firm.typical_client}"
     - Other Notes (${fields.other_notes}): Summary combining: differentiator, founding story, culture notes, awards, red flags. Keep under 500 chars.
     - Owner Notes (${fields.owner_notes}): For each owner: name, title, career history, education, board roles, LinkedIn. Combine all owners into one text block.
     ${fields.email_draft ? `- Email Draft (${fields.email_draft}): "${result.email_draft}"` : fields.av_notes ? `- AV Notes (${fields.av_notes}): "${result.email_draft}"` : `- append to Other Notes: "EMAIL DRAFT: ${result.email_draft}"`}
     - Research Status (${fields.research_status}): "Complete"

     Use the Airtable MCP update_records_for_table tool. Return "done" when complete.`,
    {
      label: `writeback:${result.firm.name}`,
      phase: 'Write back',
    }
  )
)

return {
  market,
  firms_researched: researched.length,
  emails_drafted: withEmails.filter(Boolean).length,
  results: withEmails.filter(Boolean),
}
