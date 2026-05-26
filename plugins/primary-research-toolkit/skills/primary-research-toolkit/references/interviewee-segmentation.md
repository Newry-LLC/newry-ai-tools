# Interviewee Segmentation Framework

Seven dimensions for classifying interview subjects in primary research. Each dimension is independent — any given interviewee can be described across all seven simultaneously. Together they determine how to weight, interpret, and synthesize what was said.

These dimensions are inputs to skill design decisions, not just taxonomy. Where segmentation affects how a synthesis tool should behave, that is noted.

---

## 1. Relationship to the client (subject type)

The most fundamental cut. Determines what kind of knowledge the interviewee holds and how much evidentiary weight to assign their claims.

| Type | Knowledge base | Notes |
|------|---------------|-------|
| **Internal client staff** | How the business actually operates; internal strategy, process, culture | May self-censor; their view of their own company can be systematically biased |
| **Client customers (current)** | Real purchase behavior, unmet needs, switching triggers, value perception | High trust on "what we need"; lower trust on "what the market does" |
| **Client customers (prospective)** | Stated interest and requirements; has not yet been tested by transaction | Discount aspirational claims; watch for social desirability bias |
| **Industry / technical SMEs** | Market structure, competitive dynamics, technical standards, trend signals | Strong on facts about the broader market; weaker on client-specific dynamics |
| **Competitive intelligence sources** (former competitors, distributors, channel) | Competitor capabilities, pricing, positioning, customer relationships | High-value but handle with care; may carry their own agenda |
| **Regulators / standard-setters** | Compliance requirements, approval timelines, policy direction | Narrow but authoritative within scope |

**Tool implication:** Synthesis should never flatten across types. A finding from internal staff about "where we win" and a finding from a competitor-adjacent source about "where Alta loses" are different data, even if they address the same branch of the issue tree.

---

## 2. Attribution and disclosure (blind vs. non-blind)

Whether the interviewee knows who the client is — and whether they know their responses may be attributed.

| Mode | Description | Effect on interpretation |
|------|-------------|-------------------------|
| **Blind** | Respondent does not know who the client is | More candid on sensitive topics (competitor weaknesses, client vulnerabilities, pricing); higher trust for adversarial topics |
| **Semi-blind** | Knows the general topic/industry but not the specific company | Moderate candor; some self-censorship possible |
| **Non-blind** | Knows the client, project purpose, and/or that their employer commissioned the work | Greater context and cooperation on collaborative topics; more diplomatic on sensitive ones |
| **Attributed** | Respondent knows their specific statements may be identified to them | Stronger self-censorship; higher value on opinions they do choose to share |

**Tool implication:** Synthesis should surface disclosure status alongside quotes. A blind expert's critique of Alta's market position is higher-signal than the same claim from a non-blind internal stakeholder.

---

## 3. Type of knowledge being elicited

Orthogonal to who the interviewee is — this is about what they are being asked to provide.

| Type | Description | Synthesis handling |
|------|-------------|-------------------|
| **Factual / market** | Quantitative claims, market structure, competitive facts ("We spend $4M/year on resin, 60/40 between two suppliers") | Aggregate and triangulate; flag inconsistencies across sources |
| **Experiential / operational** | What it is actually like to do a job, navigate a process, face a constraint ("The supplier approval process takes us 18 months") | Sample and quote; patterns matter, but outlier detail also has value |
| **Opinion / strategic** | Views on what should happen, what the right move is, what the future holds | Track explicitly; disagreement across sources is the signal, not the problem |
| **Validation** | Testing a hypothesis already formed ("We're hearing X — does that match your experience?") | Report hit rate; note when the framing may have primed the response |

**Tool implication:** Factual and experiential findings can be aggregated and counted. Opinions require disagreement tracking — the synthesis should show spread, not just consensus. Validation findings need a clear "n confirmed / n challenged / n novel" structure.

---

## 4. Incentive and relationship structure

Affects motivation to participate, candor, and expected response quality.

| Structure | Description | Effect |
|-----------|-------------|--------|
| **Paid / formal expert network** (AlphaSights, GLG, etc.) | Compensated; pre-consented; time-bounded; often sourced for specific expertise | Technically deep; format often consistent (transcript provided); expert may be performing credibility |
| **Warm / relationship-based** | Unpaid but willing; reached through a mutual contact or prior Newry relationship | Often more candid than formal expert calls; format more variable |
| **Obligated internal** | Client employees directed to participate by their employer | Showed up because asked; varying candor and preparation; may give the "official" answer |
| **Cold outreach / no prior relationship** | Respondent had no prior connection to Newry or the client and was approached directly (e.g., LinkedIn, email, conference) | Willingness to engage is itself a signal; once participating, often candid precisely because they have no stake in the relationship |
| **Self-selected / inbound** | Prospects or partners who chose to engage (e.g., customers who responded to outreach) | Motivated; selection bias toward interested / favorable parties |

**Tool implication:** Weight calibration. A single paid expert with 30 years of experience saying something unusual deserves more signal weight than a pattern from five obligated employees repeating the company line.

---

## 5. Interview structure

Affects how the transcript is formed and what can be reliably extracted from it.

| Structure | Description | Synthesis handling |
|-----------|-------------|-------------------|
| **Structured / guided** | Set of predetermined questions; comparable across sessions | Easy to aggregate; missing answers (skipped questions) are meaningful |
| **Semi-structured** | Core questions with exploratory follow-up | Most common in Newry fieldwork; requires tracking which questions were and weren't addressed |
| **Exploratory / unguided** | Follows the interviewee's framing; no fixed question set | High-value emergent content; harder to cross-compare; themes emerge inductively |
| **1:1 interview** | Single respondent | Standard case; individual view is clearly attributed |
| **Group / workshop** | Multiple respondents in the same session | Dynamic data: people build on, contradict, or hedge against each other; requires interaction tracking, not just statement extraction |

**Tool implication:** The synthesis approach must match the structure. Guided transcripts can be compared question-by-question. Exploratory transcripts require inductive theme identification. Group sessions require attribution to specific speakers and tracking of convergence/divergence dynamics.

---

## 6. Note quality and input format

The most practical constraint on what the tool can do.

| Format | Description | Tool handling |
|--------|-------------|--------------|
| **Verbatim transcript** | Full word-for-word record; may include timestamps and speaker labels | Highest fidelity; direct quote extraction reliable |
| **Lightly edited transcript** | Verbatim with filler words removed; structure preserved | Near-verbatim; quote extraction reliable with minor caveats |
| **Synthesized notes** | Consultant-written summary of key points; paraphrase rather than direct quote | Quote extraction not reliable; findings attributed to the note-taker's interpretation |
| **Rough bullets** | Quick capture during or immediately after interview; incomplete and subjective | Lowest fidelity; treat as directional signal, not evidence |

**Tool implication:** The tool must declare input fidelity at the top of every output artifact and adjust quote attribution accordingly. Verbatim transcripts support direct quotation. Synthesized notes support paraphrased attribution only. Outputs from rough-bullet inputs should be flagged as low-confidence.
