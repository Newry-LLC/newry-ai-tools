---
name: prt-corpus-query
description: Use this sub-skill to query a primary research corpus and retrieve findings, counts, quotes, or cross-tabulations by person, topic, or segment. Part of the Primary Research Toolkit. Triggers on "who talked about X," "how many people mentioned X," "what did people say about X," "find interviewees who said X," "query the corpus," "search the interviews," "who raised X," "did anyone mention X," "what did [name] say about X," "which [type/geography] interviewees raised X," "summarize what [segment] said about X," "go deeper on [name]," "show me the transcript for [name]," and similar natural-language corpus queries.
---

# Primary Research Toolkit — Corpus Query

A sub-skill for retrieving, counting, and cross-tabulating findings from a coded primary research corpus. Reads from ICS outputs — claims table, summary cards, and preprocessed transcripts — using keyword and topic-tag matching. No semantic search, no web access.

**What this skill does not do:** draw conclusions, make recommendations, resolve contradictions between sources, write new synthesis, update the claims table, or answer questions from outside the corpus.

---

## Output discipline

- **Pre-flight echo at the top of every response.** Before results, emit a compact block reporting what the skill found and is acting on:

  ```
  **Pre-flight**

  - Claims table: [path | not found — see Claims table dependency below]
  - Rows loaded: [N]
  - Route file: [path | not found]
  - Preprocessed transcripts: [N files found at <project-root>/Primary Research/preprocessed/ | not found]
  - Glossary: [N entries at <path> | not found]
  - Pre-flight warnings: [bullet list, or "none"]
  ```

  Pre-flight warnings include: claims table not found, route file not found, glossary not found, preprocessed transcripts not found, query terms not matched in topic_tags or glossary (possible spelling issue), fewer than 3 rows matched (result may be thin), zero rows matched. Pre-flight is informational — it does not gate the query. Report and continue.

- **Zero results.** If the claims table returns 0 rows for the query, surface explicitly: "No results found for [topic] in the claims table. Try broader terms, or say: go deeper on [name] to check their card directly." Do not present an empty result silently.

- **Output ends at source note — one static trailer only.** Do not append next-step menus or offer follow-up options mid-response. After the result, emit one static trailer:

  `Results from claims index ([N] matching rows). To go deeper on any person, say: go deeper on [name(s)].`

  The trailer is a pointer, not a question.

- **Suppress technical noise.** Filter mechanics, regex details, row-iteration steps, and file-load minutiae are working state. Surface only what the consultant needs: result count, matched rows, attribution notes, and any retrieval limitation that affects how to read the result.

---

## Feedback capture

Handled at the coordinator level — see the coordinator's Feedback capture section. Log to `Primary Research/logs/feedback-log.md`. Acknowledge briefly and continue.

---

## Inputs

| File | Role | Required |
|---|---|---|
| `Primary Research/outputs/[Project] Corpus Claims v1.xlsx` | Primary index — one row per finding bullet, with topic_tags, claim text, quote, attribution, and interviewee metadata | Yes |
| `Primary Research/outputs/mode2-route-YYYY-MM-DD.md` | Branch-to-card index — used to route card-fallback queries | For card-fallback queries only |
| `Primary Research/outputs/batch-*-cards.md` | Full card text | For card-fallback queries only |
| `<project-root>/Primary Research/preprocessed/*.preprocessed.md` | Preprocessed transcripts — cleaned, diarized output of `preprocess.py` | For Go Deeper transcript layer only |
| `<project-root>/Primary Research/glossary.md` | Term normalization | Recommended |

Preprocessed transcripts are always at `<project-root>/Primary Research/preprocessed/` — this is the canonical output location of `preprocess.py` across all projects. The skill never reads raw source transcripts from `Primary Research/materials/`.

---

## Claims table dependency

If `Primary Research/outputs/[Project] Corpus Claims v1.xlsx` does not exist:
- Tell the consultant the claims table hasn't been built yet, and offer to run ICS Mode 1 now to produce it. Do not ask the consultant to go do this themselves.
- If batch card files already exist in `Primary Research/outputs/`, offer to build a draft claims table on the spot from those cards instead. State it's a fallback — attribution completeness depends on card quality.

Do not attempt to answer corpus queries without the claims table. Card-fallback queries require the route file; if it is also missing, fall back to direct card reads with a warning that branch routing is unavailable.

---

## Query classification and routing

**Step 1: Parse and classify.** On receiving a query, identify the type from the table below. If ambiguous, default to claims table first.

**Step 2: Normalize terms.** Check query terms against `Primary Research/glossary.md`. Apply confirmed corrections silently (e.g., "altar" → "Alta"). Expand abbreviations where the glossary has an entry. If no glossary exists, proceed and note it in pre-flight.

**Step 3: Execute retrieval per type.**

| Query type | Example | Layer | Method |
|---|---|---|---|
| Topic scan | "who talked about CIPP" | Claims table | Keyword match on claim text + filter topic_tags |
| Count | "how many people mentioned pricing pressure" | Claims table | COUNTIF on topic_tags / claim keyword; deduplicate by interviewee |
| Cross-tab | "which EU interviewees raised data center demand" | Claims table | Filter geography + topic_tags |
| Quote retrieval | "what exact language did people use about tech service" | Claims table | Filter topic_tags, return quote column |
| Person lookup | "what did Lapkowicz say about distributors" | Claims table first, card fallback | Filter name + topic; load card if claims table result is thin |
| Comparison | "who had similar views on distributor strategy" | Claims table | Group by topic_tags, identify overlap across interviewees |
| Branch synthesis | "summarize what commercial staff said about A3" | Cards | Load route file; filter to cards with ✓/~ on specified branch + type filter; read those cards only |
| Open-ended | "what surprised people most about the market" | Claims table first, card fallback | Filter branch = OIT; expand to card reads if OIT claims are sparse |
| Go deeper | "go deeper on Lapkowicz" | Card first, transcript fallback | See Go Deeper section below |

---

## Step 4: Present results

Format depends on query type. Apply consistently.

**Topic scan / Quote retrieval**
- List matching interviewees grouped by type or geography where the distribution is meaningful.
- For each: code `[IS-NN: Name]`, claim or quote, attribution level.
- State whether results are claims-table-only or card-verified.

**Count**
- Lead with the number: "N interviewees raised [topic]."
- List the interviewees with codes.
- Add caveat if relevant: "This counts cards where the topic appeared — passing mentions in transcripts not captured in the claims table are not included."

**Cross-tab**
- State distribution by the requested dimension (type, geography, segment, seniority).
- Inline form when distribution is simple: "4 of 6 EU interviewees raised this; 1 of 5 NA interviewees."
- Table form when distribution is the main message:

  | Segment | Cited | Total |
  |---|---|---|
  | [Type] | N | N |

**Person lookup**
- List the interviewee's relevant claims with codes, quotes where available, branch tags.
- If claims table returns fewer than 3 rows for this person + topic, load their summary card and answer from card text. Note the fallback in pre-flight.

**Comparison**
- Identify the 2–4 interviewees with the most overlap on the topic.
- Characterize what they share: common claim, shared mechanism, or similar framing.
- Note meaningful divergences if present — do not resolve them.

**Branch synthesis**
- Load the route file; identify cards with ✓ or ~ on the specified branch and matching the interviewee type or segment filter.
- Answer from card text directly; do not re-synthesize into new findings — report what the cards say.
- Cite each card: `[IS-NN: Name]`.

**Open-ended**
- Pull OIT-tagged claims from the claims table first; present as a grouped list.
- If OIT claims are sparse (fewer than 5 rows), load the OIT sections of relevant cards and expand.
- State which layer the answer draws from.

**Attribution in all outputs**
- Always include source codes `[IS-NN: Name]` inline.
- Declare attribution level (High / Medium / Low) per source when quoting.
- Note if the result is claims-table-only or card-verified or transcript-verified.

---

## Go Deeper

Triggered by: "go deeper on [name]", "show me the transcript for [name]", "what else did [name] say about [topic]", or any explicit request for more context on a specific person beyond what the claims table returned.

Go Deeper runs two layers in order. Start at Layer 1; escalate to Layer 2 if needed.

---

### Layer 1 — Summary card

**What it does:** Surfaces everything ICS captured for this person on the queried topic — all finding bullets, branch coverage, framing, and any card-level context that doesn't appear in the claims table.

**If no topic is available** (no prior query in the session and the "go deeper" request names only a person), ask one question before proceeding: "What topic are you interested in for [name]?" Lock the answer and continue.

**Steps:**
1. Identify the person's card in `Primary Research/outputs/batch-*-cards.md` (match by name or interviewee code).
2. Use the topic from the preceding query, or the topic extracted from the "go deeper" request, to locate the relevant card sections.
3. Surface: all finding bullets tagged to the relevant branch(es), the coverage rating (✓/~/—), any Outside the Issue Tree items related to the topic, and verbatim quotes where present.
4. Cite as `[IS-NN: Name] — card`.

**Escalate to Layer 2 if any of the following:**
- Fewer than 3 relevant bullets found in the card for the queried topic
- Attribution is Low
- The consultant explicitly asks for the transcript ("show me the actual conversation", "what did they say word for word", "transcript for [name]")

If card result is sufficient (3+ bullets, Medium or High attribution): present the card result, then add one static line: `To read the source exchange, say: transcript for [name].`

---

### Layer 2 — Preprocessed transcript

**What it does:** Finds and surfaces the actual exchange from the interview — the consultant sees the conversation in context, not just the distilled findings.

**Preprocessed transcript location:** `<project-root>/Primary Research/preprocessed/[filename].preprocessed.md`

Filename matching: match by interviewee name or code against `Primary Research/preprocessed/INDEX.md` (written by `preprocess.py`; lists every preprocessed file with its interviewee code and name). If `INDEX.md` is missing, fall back to filename matching directly in `Primary Research/preprocessed/`. If the match is ambiguous (multiple files for the same person, or filename doesn't contain the name), list the candidates and ask the consultant to confirm before proceeding.

**Steps:**
1. Load the correct `.preprocessed.md` file.
2. Keyword-search the file for the normalized query terms (after glossary application). A passage matches if any normalized term appears in a speaker turn.
3. For each matched passage: surface the matched exchange plus 5 turns of surrounding context on each side (before and after), preserving speaker labels.
4. If multiple passages match, surface all of them in order — do not select one arbitrarily.
5. Cite as `[IS-NN: Name] — transcript, [approximate position or section label if present]`.

**If preprocessed transcripts not found:**
Tell the consultant: "Preprocessed transcripts aren't available for this project yet — they're needed to pull source exchanges. I can run `preprocess.py` on the transcripts folder now to generate them. Should I go ahead?"

If yes: run `preprocess.py` with `--input <Primary Research/materials/transcripts-folder> --output <project-root>/Primary Research/preprocessed`, then continue to the transcript retrieval step. Do not ask the consultant to run the script themselves.

If no: stay at the card layer and note the limitation in the output.

**Output format for transcript result:**
```
**[IS-NN: Name] — transcript**

[Speaker label]: [turn text]
[Speaker label]: [turn text]
→ [matched passage highlighted or noted]
[Speaker label]: [turn text]
[Speaker label]: [turn text]
```

Present all matched passages. Do not summarize or paraphrase transcript text — surface it verbatim. After all passages: `Source: preprocessed transcript at <path>.`

---

## Step 5: Logging

At the end of every run, append to `Primary Research/logs/corpus-query-log.md` (project-level, alongside `Primary Research/logs/feedback-log.md`):

```
---
Date: [YYYY-MM-DD]
Project: [Project name]
Query: [Verbatim user query]
Query type: [Topic scan / Count / Cross-tab / Quote retrieval / Person lookup / Comparison / Branch synthesis / Open-ended / Go Deeper]
Layer used: [Claims table / Cards / Transcript / Multiple]
Rows matched: [N]
Glossary applied: [Y/N — N fixes]
Notes: [Anything notable — thin results, fallback triggered, term normalization calls, preprocess.py run on demand]
```
