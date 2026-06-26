---
name: value-creation
description: Build the project value creation hypothesis — after the problem statement. Classifies the project, quantifies the value created (range + midpoint), sets Newry's fair share and the upside, writes the six value creation fields to the Airtable project record, and feeds the deck's value-creation page. Collaborative — requires EM judgment, not automation.
---

# Value Creation Sub-Skill

Build a defensible, assumption-explicit value creation hypothesis the EM owns. Runs **after the problem statement** — the value story leans on the SMART objective and scope, so the problem statement must exist first. Writes the six value fields to the Airtable record that launch-intake created, and produces the content for the deck's value-creation page.

Value creation is a judgment call — it can't be filled correctly from the SoW alone. The skill's job is to make the analytical work faster and more rigorous, not to replace the EM's judgment.

## Inputs

**Required:**
- Problem statement (especially the SMART objective and scope) — from the problem-statement sub-skill or provided directly
- SoW / proposal

**Optional (improves output quality):**
- The Airtable project record from launch-intake (fees, dates, type — used for the fee:value ratio and to locate the record to update)
- Client financials or size context (revenue, EBITDA, market cap — anchors the estimate)
- Prior Newry work on this client (past value estimates or benchmarks)

## Flow

**Step 1 — Offer working modes**

Present this in chat:

```
For the value creation hypothesis, how do you want to work?

A) I'll draft based on the SoW + problem statement — you review and we refine together
B) I'll ask you a few questions first, then draft
C) You share your thinking first — I'll structure and pressure-test it

(Or just tell me what you know about the value story and we'll go from there.)
```

Wait for the EM's response before proceeding.

**Step 2 — Execute the chosen mode**

**Mode A — Skill drafts first:**
- Apply the value creation framework (below) to produce a full draft: category classification, quantification logic, $ range + midpoint, confidence rating, fair share, upside, key assumptions with issue-tree linkage
- Show all assumptions explicitly — hurdle rate, EV/EBITDA multiple, SOM estimate, fair share tier, months accelerated (wherever applicable)
- Invite reaction: "Does this match how you're thinking about it? What would you change?"
- Iterate until the EM is satisfied

**Mode B — Questions first:**
- Ask one question at a time. Cover:
  1. What's the primary mechanism of value? (revenue, acceleration, risk reduction, business case, positioning)
  2. What's the relevant size of the opportunity? (annual revenue potential, program budget, cost at risk — whatever fits)
  3. What's Newry's role — pure ideation, ideation + validation, or something heavier?
  4. Any assumptions already in mind (multiples, margins, timeline)?
- Once you have enough to build the model, draft and present for review

**Mode C — EM drafts first:**
- Ask: "Share what you're thinking — even rough numbers or a direction — and I'll build it out."
- Receive the EM's input, structure it into the standard format, fill gaps using the framework, flag any assumptions added
- Review with the EM: "Here's what I built from what you shared. I added [X assumption] — does that hold?"

**In all modes:** share a point of view. If an assumption looks off — fair share % too high for the project scope, SOM estimate implausible, fee:value ratio unusual — say so. The skill is a thinking partner, not a transcriptionist.

**Step 3 — Finalize and write to Airtable**

Once the EM confirms the value creation content, locate the project record (created by launch-intake; find by project code or company), write all six value fields, and output the report.

```
VALUE CREATION COMPLETE — [Client Name] — [Project Code if known]

✅ WRITTEN — VALUE CREATION
  Category: [e.g., Acceleration + Business-Case Development]
  Value Created: $[X]M (range: $[low]–$[high]M)
  Fair Share: $[X]K ([Y]% of midpoint)
  Upside: $[X]M
  Confidence: [High / Medium / Low] — [one-line reason]
  Fee:value ratio: [X:1] — [flag if unusual]
  Key assumptions: [hurdle rate, multiple, SOM, fair share tier, months accelerated]

This feeds the value-creation page of the kickoff deck. Review before the launch meeting.
```

## Value creation fields (Airtable)

| Field | Airtable ID | What to write |
|---|---|---|
| Potential Value Created for Client ($) | `fldWiJCDLtpxJDrb8` | Midpoint of range — round number, never false precision |
| Potential Value Created for Client (Narrative) | `fldRcO57OkiDDhjx2` | Full narrative: mechanism, logic chain, explicit assumptions |
| Newry's Fair Share ($) | `fldHwcVoZqaLG3ri3` | Midpoint of fair share range — round number |
| Newry's Fair Share (Narrative) | `fldhP1uvPmhjvWi8S` | Fair share % with rationale, range, and fee:value commentary |
| Upside | `fldhZgq5zhLRpq129` | High end of the value range |
| Upside Description | `fldiSVoM0TeMdompg` | What would need to be true for the high case to materialize |

## Value Creation Framework

### Four categories

Classify the project into one or more. Use the primary category for the headline estimate; note others in the narrative.

| Category | What it means | Trigger phrases in SoW |
|---|---|---|
| **Commercial Traction & Revenue** | Newry's work drives near-term revenue | "grow revenue", "enter market", "identify customers", "launch", "commercial strategy" |
| **Acceleration Toward Launch/Scale/Kill** | Newry accelerates or cleanly ends an innovation program | "reduce time to", "accelerate", "go/no-go decision", "de-risk", "resolve uncertainty" |
| **Business-Case Development** | Newry builds/validates a business case enabling a capital decision | "business case", "investment decision", "Board approval", "financial model", "valuation" |
| **Value Proposition Optimization** | Newry improves pricing, positioning, or market strategy | "pricing strategy", "positioning", "value proposition", "willingness to pay", "differentiation" |

### Quantification by category

**Commercial Traction & Revenue:**
```
Value = SOM ($) × Probability of capture (%) × Gross margin (%) × EV/EBITDA multiple
```
- Gross margin sector norms: specialty materials 40–55%; industrial products 25–40%
- EV/EBITDA: specialty/differentiated materials 11–14x; commodity/basic chemicals 8–10x; broad industrials 9–12x
- Apply time-to-realization discount (see below)

*Qualitative version (when SOM or capture probability is unavailable or too speculative):* "Newry will identify [target segments] and develop a commercial approach to capture a meaningful share of [market description]. Value is realized through [revenue / adoption / market entry ahead of competitors]. A quantitative estimate is not supportable without [missing input — e.g., client revenue data, confirmed SOM]."

**Acceleration Toward Launch/Scale/Kill:**
```
Value = (Annual NPV of program) × (Months accelerated ÷ 12)
      + (Capital at risk) × (Probability of misallocation prevented %)
```
- Months accelerated: typically 3–9 months for a focused Newry engagement
- Annual program NPV: use disclosed client figure or build from R&D budget / revenue signals
- Use 1–2 year discount row or skip discount — value is realized now, not years out

*Qualitative version (when program NPV or capital at risk is unavailable):* "By resolving [key uncertainty], Newry will enable [client] to make a [decision type] [X months] earlier than otherwise possible, reducing the risk of [misallocation / delayed launch / continued investment in a losing program]. The value is real but not quantifiable without [program NPV / capital at risk data]."

**Business-Case Development:**

Quantification is difficult and highly variable — the right approach depends heavily on the nature of the decision being enabled (capital allocation, go/no-go, M&A, regulatory, etc.). In most cases, write qualitative only. Quantify only when the size of the decision or capital at risk is explicitly disclosed and Newry's contribution to decision quality can be credibly bounded.

When quantification is warranted, the relevant inputs will vary by project type and may include: size of the investment decision or capital program at risk; NPV or IRR of the initiative being evaluated; cost of a wrong decision (misallocation, delayed entry, stranded assets); option value of resolving a key uncertainty before committing; probability that Newry's analysis materially changes the outcome. Show all assumptions explicitly — these numbers will be highly uncertain and should be labeled as directional.

*Qualitative version (default):* "Newry will build a business case enabling [client] to make a [investment / allocation / go-no-go] decision with greater confidence. The value is improved decision quality — reducing the risk of a well-funded bad bet or an underfunded good one. The magnitude depends on the size of the decision and how much the analysis shifts the outcome, both of which are too uncertain to quantify at launch."

**Value Proposition Optimization:**
```
Value = (Revenue base) × (Pricing or share improvement %) × Gross margin × EV/EBITDA multiple
     OR (Cost base) × (% reduction) × EV/EBITDA multiple
```

*Qualitative version (when price lift or share gain is too speculative):* "Newry's work will improve [client]'s ability to capture value from [product/segment] through [better pricing / clearer positioning / sharper differentiation]. The magnitude depends on client execution and market response — quantification would require assumptions beyond what's supportable at launch."

### Time-to-realization discount

Apply after the gross value formula. This is a time-value-of-money adjustment, not an execution probability adjustment — probability is already captured in the formula inputs above.

| Time to realization | Discount |
|---|---|
| 1–2 years | 15–20% |
| 3–4 years | 25–35% |
| 5–6 years | 35–45% |
| 7+ years | 45–55% |

*Based on 10–12% WACC — specialty chemicals/materials sector cost of capital (Damodaran, Jan 2026). Covers most of Newry's core client base. Adjust up (12–15%) for early-stage or high-uncertainty programs; down (8–9%) for large-cap commodity producers.*

**Default if timeline is unclear: 30% (3–4 year horizon).**

Apply as: Discounted value = Gross value × (1 − discount %)

For Acceleration projects where value is realized immediately (a decision made now, capital preserved now), use the 1–2 year row or skip the discount and note why.

### Range, midpoint, and precision

Always produce a low and high case. Midpoint = headline $. Never a single-point estimate.
- Low: conservative assumptions
- High: favorable but not implausible
- **Round numbers only.** $7M, not $7,359,445.57. The estimate is inherently approximate — false precision undermines credibility.
- Round to nearest $500K for large estimates; $50K for smaller ones.

### Fair share tiers

| Stage | % | When to use |
|---|---|---|
| Pure ideation | 1–2% | Newry surfaces options; client does all commercialization. Early application development, initial opportunity scans. |
| Ideation + validation | 4–5% | Newry narrows the field with early evidence; major downstream work remains. Most application development + growth strategy work. |
| Process / reusable system | ~10% | Newry delivers a durable artifact with lasting operational impact. Workshops, process improvement, templates. |
| Acceleration + risk reduction | 8–12% | Newry measurably accelerates a capital decision or reduces misallocation risk. Performance-based consulting benchmark. |
| Surveillance / ongoing intelligence | N/A | Value is real but non-quantifiable. Write qualitative narrative; leave $ fields blank. |

Fair share $ = Value midpoint × fair share %

**Fair share narrative must include:** the % tier applied, plain-English rationale for what Newry is and isn't doing, a range (not a point), and — if the fee:value ratio is unusual — a note explaining it.

**Fee:value ratio check (Check 1):** compute value midpoint ÷ Newry fees. A ratio of 20:1–30:1 is a strong ROI story worth highlighting. Below 5:1, call it out — either the value is understated or the fees are too high relative to scope.

**Fair share vs. fees check (Check 2):** Fair share $ should be in the same ballpark as actual Newry engagement fees — within 2x in either direction. If fair share comes out at $5M but the engagement is $200K, one of three things is true: (a) the value estimate is inflated, (b) a lower fair share tier should have been used, or (c) the upside story is unusually strong — explain it in the narrative.

### Confidence rating

Assign one of three levels and include a one-line explanation:

- **High** — key inputs (SOM, program NPV, cost base) are grounded in disclosed client data or verified market figures
- **Medium** — key inputs are estimated from analogues, sector norms, or partial client data; logic is sound but numbers are illustrative
- **Low** — primary inputs are unavailable; estimate is directional only; recommend requesting data in Week 1

### When to write qualitative only

Skip the dollar fields when:
- The project is surveillance, competitive intelligence, or ongoing advisory
- The project is purely qualitative with no commercializable output
- Quantification would require fabricating inputs with no grounding

Write a narrative explaining: what value the work creates, why a number isn't appropriate, what the qualitative benefit is. See COR772 (NexGen Waveguide Materials) as the model.

## Common Errors to Avoid

- **False precision** — $7M, not $7,359,445. The model producing a precise number doesn't mean the estimate is precise.
- **Missing logic chain** — narrative must show the math, not just the conclusion.
- **Overclaiming attribution** — Newry accelerates or enables; it rarely executes. Fair share % should reflect scope honestly.
- **Single-point estimate** — always low/high/midpoint.
- **Copy-pasting from a prior project** — narratives must be project-specific. Prior projects inform benchmarks, not templates.
- **Leaving value fields blank when a draft is possible** — a clearly-labeled rough draft with explicit assumptions is better than nothing.
- **Not flagging an unusual fee:value ratio** — if it looks off, it will look off to the client too. Call it out.

## Design Notes

- **Runs after the problem statement.** The value hypothesis leans on the SMART objective and scope — don't run it before the problem statement exists.
- **Writes to the launch-intake record.** Locate the project record (by code or company) and update the six value fields; don't create a new record.
- **Feeds two destinations.** The same hypothesis populates the Airtable value fields and the deck's value-creation page.
- **Collaborative, not automated.** The modes exist because EM judgment is required. Iterate until the EM owns it before writing.
- **Connects forward to the issue tree.** Every key assumption should become an issue the team validates — flag them for the issue-tree step.

## References

- `strategy/airtable-base.md` — canonical table/field reference (`appRawPuacfAvVH2Z`); Projects: `tbl3FaAcnmFWjRwqr`
- Project Initiation Template — the value creation metrics reference (4 categories) and the value-creation hypothesis / Newry fair share page
- Prior project examples (Airtable): HASA01, COR771, INGEV02, DUP38, ALTA01, COR772 — correct narrative structure and fair share tiers
