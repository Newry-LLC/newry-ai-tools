# Post format — canonical template and sourcing

**One standardized format for everyone.** Every person's post uses the exact field labels, order, and structure below — regardless of how they've posted before. The point of the skill is to normalize the channel to a single consistent format. Do not copy a person's prior idiosyncratic labels.

**Scope note (confirmed 2026-07-07):** this template is SoF-style only. Newry's documented Weekly Project Scorecard (budget status, progress vs. workplan, people/firm capability development, 1–5 value-delivery and relationship scores) is deliberately excluded — current #weekly_call_in practice doesn't use it. Not an oversight.

## The canonical template (one block per project)

Slack uses single asterisks for bold. Field labels are bolded exactly as written; values are plain. Fields, in this order, always:

```
*Client and Project Code:* <code + short name>
*Team:* <first names>
*Purpose:* <what we're doing for the client and why — static>
*Findings / Status:*
• <this week's substance — grounded in sources>
• <...>
*Next Update:* <date/time or cadence>
*Final Update:* <date/time, "N/A" for ongoing, or "Done!">
*Editorial needs this week:* <deck/slides needed, or None>
*Issues / Risks / Needs:* <only real, source-backed risks; else None>
```

Multiple projects → multiple blocks in one message. Some people separate blocks with a line of underscores (AJ), most just use a blank line.

## Field-by-field sourcing

Use the canonical labels above in every case. The "Source" column says where the *value* comes from — never where the label/format comes from (that's always the template).

| Field | Source |
|---|---|
| Client and Project Code | **Airtable Project Code** (the canonical code) + Airtable Project Name for the short descriptor. Match internally on client + fuzzy code to find the record, but always emit the Airtable code — normalize any improvised channel variant (IN02→INGEV02, DUP038→DUP38) to it. |
| Team | Airtable Project Roles (all staff on the project), first names. |
| Purpose | Carry forward from last post if it exists (static), but conform the label to *Purpose*. Else synthesize from Airtable Project Description / Client Goals / Firm Goals. |
| Findings / Status | **The week's work** — synthesized from transcripts, SharePoint changes, email, calendar (see `data-sources.md`). The delta since last post, not a repeat. |
| Next Update | Calendar + known cadence. |
| Final Update | Calendar / project end date; "N/A" for ongoing retainer-style work; "Done!" when wrapped. |
| Editorial needs this week | Driven by upcoming client meetings on the calendar (deck needed?). "None" if nothing upcoming. |
| Issues / Risks / Needs | Only risks a source actually surfaced. Default "None." Never invent. |

## Normalize to the standard — don't copy prior styles

Prior posts in the channel use inconsistent labels. **Convert all of these to the canonical labels above**, never reproduce them:
- "Findings/Progress", "Update" → **Findings / Status**
- "Background / Purpose" → **Purpose**
- Missing *Issues / Risks / Needs* (some people omit it) → **always include it**, default "None"
- Underscore dividers between projects → drop; use a blank line between blocks
- Free-form or improvised codes ("ALTA, ALTA01", "IN02", "DUP038") → the canonical Airtable project code + short name

## Worked examples (content shape — labels shown are already normalized)

These illustrate the substance/tone of a good block. The labels here are the canonical ones; older real posts by these people used different labels that the skill would normalize.

### Concise, single project
```
*Client and Project Code:* COR770 Thin Triple Q2 2026
*Team:* Matt, Christian
*Purpose:* Grow Corning's Advanced Windows business through sales of advanced triple-/quad-pane and laminate windows by assisting in development of their value prop and accelerating demand for Corning's Enlighten Glass across the value chain.
*Findings / Status:*
• Corning is interested in whole-home energy modeling for EMEA and Japan similar to what we've completed for US and Canada; we're working to connect with energy modelers in those regions
• We've revised the Canadian dealer-installer survey based on additional feedback from All Weather Group and sent to Emily for review; likely wait until after Q3 OKRs finalized to launch
*Next Update:* 7/8
*Final Update:* N/A; due to ongoing nature of the project, we have biweekly updates scheduled
*Editorial needs this week:* None
*Issues / Risks / Needs:* None
```

### Wrapping-up project (note: original was posted with non-standard "Background / Purpose" + "Findings/Progress" labels — shown here normalized)
```
*Client and Project Code:* DUP38 - Tyvek Pipeline Development
*Team:* Kasey, Erin, Nicole, Christian
*Purpose:* Identify/validate high-potential growth opportunities for HC and C&IC businesses where a Tyvek-adjacent material can address unmet needs and DuPont has a right-to-win.
*Findings / Status:* See attached SoFs
*Next Update:* None
*Final Update:* Done!
*Editorial needs this week:* We might have 1-2 slides to add to the deck before sending the doc of record — will check in with Adam.
*Issues / Risks / Needs:* None
```

### Full template, multi-workstream update
```
*Client and Project Code:* ALTA01 - Alta Growth Strategy
*Team:* David, Anna, Jack, Scott, Krishna, Matt
*Purpose:* Identify and execute on 3–6 high-value growth initiatives (≥$5M EBITDA each) for Alta in North America and Europe by leveraging adjacent applications and strategic portfolio expansion
*Findings / Status:*
• Prioritizing data centers, CIPP, and drones. Working to uncover ALTA's right to win/value prop, market segmentation by key applications, future technology needs
• Conducting ~40 VOC interviews and SME interviews; secondarily focusing on VOC from Composites One
*Next Update:* check-in with key stakeholders 7/1; formal report out to CEO 7/08, then core team 7/9; informal: next Wednesday
*Final Update:* End of Aug
*Editorial needs this week:* 7/8 deck that needs to be high level (visual graphs) & reuse for core team on 7/9; need marketing literature for drone material
*Issues / Risks / Needs:* prove out Newry's value in next steps so client doesn't stop; client taking on "low hanging fruit" identified by Newry may make ROI harder to prove
```

### Multi-OKR technical project, sub-bolded workstreams
```
*Client and Project Code:* COR771 Rare Earth Elements Business Model Q2
*Team:* Lisa, Isabel, Andrew, Matt
*Purpose:* Supporting Corning's Critical & Industrial Materials groups on recovering rare earth elements and critical materials from various feedstocks. Work spans four active OKRs: technoeconomic modeling, US REE supply chain mapping, T-glass qualification, and Ge feedstock identification.
*Findings / Status:*
• *TEM (Critical Materials)* — Model essentially complete our end; integrating Kai's AFR extraction model...
• *US REE Supply Chain* — Done. Supply gap analysis complete across NdPr, Y, Ga, Ge, Sc, and Sm...
• *T-Glass Qualification* — Done. Results shared with Patrick and Jaymin...
• *Ge Production* — Introductions made to several potential suppliers; Peabody Bear Run Seam 7 emerging as a credible candidate...
*Next Update:* Weekly working group sessions on Wednesdays
*Final Update:* N/A
*Editorial needs this week:* Edit the Sherwood 2-pager; may grab time to discuss white paper strategy
*Issues / Risks / Needs:*
• AFR extraction model integration needs resolution — backward-calculation logic creates cost-misestimation potential; near-term priority
• Ge supplier landscape thin on near-term options; stress-test Peabody Bear Run Seam 7 against timing before treating as a solution
```

## Tone

Peer-to-peer internal status. Tight, factual, skimmable bullets. No hype, no filler. It's read live on a Tuesday call — someone should get the state of the project in ~15 seconds.
