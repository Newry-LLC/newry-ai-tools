# Network Mapping — Plausibility Rubric (DRAFT for Jack review)

## Purpose
Filter connection matches between Sequoia targets (firm owners + partners) and the internal roster (Newry, Sequoia, Bailey employees) by strength of connection. Only surface Tier 1 and Tier 2 matches. Discard the rest.

## Internal roster
_[PLACEHOLDER — Jack to provide: names, firm affiliation, LinkedIn URLs]_

## Tiers

### Tier 1 — Worth an intro ask
Strong, specific, verifiable connections. These get surfaced to the client with a recommended ask.

- Served on the same board, committee, or advisory council **at the same time**
- Direct co-worker at the same firm with overlapping tenure
- Co-founder or business partner
- Investor and portfolio company relationship (one invested in the other's firm)
- Shared deal / transaction (both sides of the same M&A, capital raise, etc.)
- Served on the same third-org board/committee at the same time
- Close personal / family connection (where evident from public sources)

### Tier 2 — Flag for human review
Plausible but needs a judgment call. Surface with a note; human decides whether to act.

- Same company, overlapping tenure, but no evidence of direct interaction (e.g., large firm, different offices)
- Mutual board member at a third organization, no evidence of overlap in tenure
- Shared alma mater **and** same graduation year (±2 years)
- Both involved in the same industry association or conference as speakers/organizers
- One worked at a firm that was a known client/vendor of the other's firm

### Tier 3 — Discard
Too weak to be actionable. Do not surface.

- Same state or metro area, no other connection
- Same broad industry vertical (e.g., both in financial services)
- Same university, different graduation years (>2 year gap)
- Both attended the same large conference (no evidence of direct interaction)
- Same general era at a large institution with no role overlap

## Output format per match
```
target_name: <owner/partner name>
target_firm: <RIA firm>
internal_contact: <Newry/Sequoia/Bailey person>
tier: 1 | 2
connection_type: <e.g., "Co-board member, XYZ Nonprofit, 2018–2021">
evidence: <source — LinkedIn, firm website, press release, etc.>
confidence: high | medium | low
recommended_action: <e.g., "Ask [internal contact] to make intro to [target]">
```

## Notes for Jack
- Tiers above are a draft — please push back on anything that doesn't match Sequoia's actual bar
- If there are connection types we're missing (e.g., military service, religious community), add them
- "Same time" for boards: we'll treat overlapping by ≥1 year as qualifying
- Confidence reflects how verifiable the evidence is from public sources, not how strong the connection is
