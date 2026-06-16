---
name: sharepoint-search
description: Search Newry's SharePoint and answer questions about any Newry content. Use this whenever a user asks something that might be answered by a document at Newry — project materials (interview notes, client presentations, deliverables, secondary research), internal resources (Newry Ladder, employee handbook, HR policies, templates, SoW examples), or anything else stored in the company file system. Triggers on questions like "which interviewee mentioned X", "have we presented Y to the client", "what does the Newry Ladder say about PM roles", "find the secondary research on Z", "do we have a template for X", "what's our policy on Y". Don't wait for the user to say "search SharePoint" — if the question sounds like it needs a Newry document, use this skill.
---

# Newry SharePoint Search

Answer questions by searching Newry's SharePoint and synthesizing from the relevant documents. The goal is a direct, cited answer — not a list of files for the user to go read.

## Log usage first

Before any searching, log this run to Airtable. Do this once, at the start.

1. **Check connectivity.** Call `list_records_for_table` (Base `appRawPuacfAvVH2Z`, Table `tblmACtwIClniGn5n`, pageSize 1). If it fails, stop and tell the user: "⚠ **Airtable isn't connected.** This tool requires Airtable for usage logging. Go to Cowork Settings → Connectors, connect Airtable, then start a new session." Do not proceed.
2. **Write the record.** Call `create_records_for_table` (Base `appRawPuacfAvVH2Z`, Table `tblmACtwIClniGn5n`) with fields:
   - `fldRrr3BkrJW8rE3L` (ts) — current UTC, ISO 8601 (e.g. `2026-05-27T14:30:00Z`)
   - `fldNHK285dPCOdNhB` (plugin) — `"newry_knowledge"`
   - `fld4EyuVEhxAhPZEd` (sub_skill) — `"sharepoint_search"`
   - `fldmTXyfFZRpbZEvQ` (user_id) — user's email from session context; else `"unknown"`
   - `fldu8rvXDfvi2O3jF` (project) — project code if known (e.g. `"ALTA01"`); else `""`
   - If the write fails, retry once. If it still fails, silently append one JSON line to `~/.newry/logs/usage-log-<user_id>.jsonl` (create the dir if missing): `{"ts":"<ISO>","plugin":"newry_knowledge","sub_skill":"sharepoint_search","user_id":"<user_id>","project":"<project>"}`. No user-facing error.

## Tools

- `sharepoint_search` — keyword search across the full index. Params: `query`, `folderName` (partial match), `fileType` (extension, e.g. `pptx`), `author` (name/email, partial), `afterDateTime`/`beforeDateTime` (ISO 8601, by last-modified), `limit` (default 10, max 50), `offset` (pagination — pass `nextOffset` from the prior response). All filters AND together. Returns name, `webUrl`, snippet with match highlights, `lastModifiedDateTime`, and `uri`.
- `sharepoint_folder_search` — find folders by name. Use to enumerate client folders for prior-work sweeps.
- `read_resource` — fetch a document's full text by `uri`. Use only when the snippet genuinely can't answer the question.

## The loop

### 1. Classify, then interpret

Sort the question into one type — this is the only branch point, and it sets both your search posture and your answer shape:

| Type | Looks like | Posture |
|---|---|---|
| **Point lookup** | "what did X say about Y", "what does the Ladder say about Z" | **Precision** — find the one right doc |
| **Existence check** | "do we have research on X", "have we presented Y" | **Precision** — confirm yes/no from metadata + snippet |
| **Enumeration** | "which/who/how many/list all mentioned X" | **Recall** — fan out, paginate, don't miss any |
| **Sweep / prior-work** | "what's the project status", "have we worked in domain X" | **Broad** — harvest the spread of files/folders |

State the goal in one plain sentence only if the question is broad, multi-part, or ambiguous (e.g. "You're looking for which people raised CIPP resin in interviews"). Skip narration for short, clear questions. Then proceed — don't wait for the user to confirm. **Default to acting on a reasonable read and reporting back; only pause for the user if a part is genuinely unclear or would surface more than 3–4 docs to read.**

If the question has multiple distinct parts, list them. Any enumerative part ("which/who/how many") must be answered fully from search results before you read documents — don't let a synthesis part quietly absorb an unanswered enumeration. Verify every part is addressed before you finalize.

### 2. Search by posture

**Pull 2–4 distinctive terms** — specific nouns, named entities, proper nouns over generic words.

**Precision (point lookup / existence):** tighten up front so the right doc lands in the top results.
- **Quote phrases** for multi-word terms that must stay together: `"CIPP resin"`, `"styrene regulation"`, `"Phase 2 pricing"`. Don't quote broad/common terms.
- **Use the engagement code** if known (`ALTA01`, `COR771`) — the single most reliable discriminator in a cross-project index. Use it as a search term *and* a `folderName` filter.
- **Use `fileType`** only when the user explicitly signals a format — "deck/slides" → `pptx`, "spreadsheet/model" → `xlsx`, "report/memo" → `docx`. Any extension works.
- **Use date filters** only when the user signals a window — "since March" → `afterDateTime`. Note: "latest"/"current" means the *authoritative* version, NOT merely recently-edited — do not impose a date filter for "latest" (see step 3).
- **Use `author`** rarely — only when the user asks about a specific person's output.
- **Narrate any exclusion.** When you filter by type, date, or author, say so in one line: "Looking only at decks since you said 'presented' — tell me to include memos and other docs too." A silent filter that hides the real answer reads as "doesn't exist." (No need to narrate going broad.)

**Recall (enumeration):** one tight query will miss people. Fan out instead.
- Fire **2–4 distinct formulations of the same need** (phrase variant, synonym/variant, code-based, one looser keyword), union the results, dedupe.
- **Paginate** — if a query fills the window (50) with plausible hits, pull the next page via `nextOffset` before concluding. Never let the true set get truncated at 50.

**Broad (sweep / prior-work):** lead with broad keyword searches, no folder filter, `limit: 50`. Harvest which client/project folders appear in result paths — that distribution is the answer, not any single doc. For prior-work: cross-check the harvested folders against the full client list (`sharepoint_folder_search` on `"Clients"`), add domain knowledge for expected-but-missing clients, and flag any you can't classify ("I couldn't confirm whether X, Y are relevant — want me to search them?").

**Narrate as you go:** "Searching Primary Research for styrene regulation..." Users should never wonder if something's happening.

**If the first search comes back empty or useless,** work this sequence before declaring a dead end: relax any type/date/author filter → swap the folder filter (drop it, or move to the parent) → try alternate terms (synonyms, broader/narrower) → use the project code instead of the client name → quote the key phrase → run a broad no-filter search to see which folders the term lives in. After three honest attempts, go to step 4.

### 3. Triage and read

Rank the results by snippet relevance, path (right client/engagement?), and `lastModifiedDateTime`. Read only the top 1–3.

**Pick the authoritative version, not just the newest timestamp.** Someone re-saving an old deck gives a stale file a fresh date. Use `lastModifiedDateTime` *plus* filename/version cues. When two plausible versions disagree, say which you picked and why.

**Snip-then-stop:** if the snippet already answers a point lookup or existence check, answer from it — don't open the doc. Call `read_resource` only for a full quoted section, an ambiguous snippet, or needed surrounding context. (This does NOT apply to enumerations — there you must page to exhaustion, not stop at the first confirming snippet.)

**Large files:** if `read_resource` returns truncated (saved to a path, not inline), do NOT retry the same doc. Pivot — for interview questions, search the individual interview-note files in the same folder (e.g. `*Internal (Anna Notes).docx`), which are small and fully readable; otherwise run a tighter keyword search to surface the section via snippets.

### 4. Answer and cite

Give a direct, specific answer — quote or close-paraphrase, don't vaguely summarize. Shape by type:
- **Point lookup** — quote/paraphrase + one sentence of context.
- **Existence check** — Yes/No + doc name, date, folder.
- **Enumeration** — the full list, one line each.
- **Sweep** — short table (file | date | what it covers) + 2–3 sentence synthesis. Prior-work: client-by-client (client | engagement | relevance), uncertain clients listed separately.

**Two honesty rules:**
- **A top-50 result set does not license a "no" or a confident point answer unless a filter bounded the set.** If you went broad and didn't find the named target, tighten and retry before answering. Absence from the top 50 ≠ absence from SharePoint.
- **Flag incomplete coverage.** If files were too large to fully read, or you stopped paging, say so: "Found two interviewees who mentioned CIPP, but two files were too large to read in full — there may be more."

**If nothing's found** after reformulation: say which is likeliest — doesn't exist yet, lives under a different name, or predates good indexing — given what you searched. Then give a real next step: the folder to browse, a different angle, or the person at Newry most likely to know. Never leave the user stranded.

**Sources** — end every answer with a Sources section:
- [Document name](document webUrl) — [Open folder](folder URL, derived by stripping the filename from `webUrl`) — *one phrase on why this source (most recent version, the active workplan, etc.)*

## SharePoint map

**Site root:** `newrycorp.sharepoint.com/clients/Shared Documents/`

**`Clients/`** — all project work
- One folder per client (e.g. `ALTA Performance Materials/`, `CORNING/`). `Newry Internal/` = internal initiatives run like engagements.
- Each client → one folder per engagement, named `{CODE}-{Engagement Name}` (e.g. `ALTA01-Growth Strategy`).
- Standard engagement subfolders (some variation): `Primary Research/` → `Internal Interviews/`, `Secondary Research/`, `Newry Presentation/`, `Project Management/` (per-engagement SoWs usually here), `From Client/`, `Data and Analysis/`, `Drafts/`, `Conferences/`, `Claude Working Folder/` (AI-assisted work / Cowork outputs, newer engagements).
- **Corning:** highest project volume of any client, almost entirely retainer — most Corning projects have NO SoW or proposal. Lead with that rather than searching for one that isn't there.

**`Consulting Resources/`** — internal firm resources
- `Document Templates/Newry Templates_Client Facing/` — all PPTX/Excel templates, client-facing *and* internal (quant models, market-sizing); the name is a misnomer. `Document Templates/Newry SME Documents/` — SME contracting (NDA, contractor agreement, W-8).
- `People & Recruiting/ACC Templates and Ladder/` — Newry Ladder (most recent: `202602 Newry Consulting Ladder and Review Process.pptx`), mentor packages. `On Boarding Materials/` — onboarding incl. The Newry Way. `Newry Employee Handbook - 20250227.docx` sits directly in `People & Recruiting/`.
- `TOOLS-TRAINING/` — `Growth Strategy/`, `Interviewing Training/`, `Pyramid Principle/`, `Slide and Document Design/Hero Slides and Documents/` (example deliverables by type: OAs, Market Forecasts, SONAR Deep Dives, RMAs).

**`Marketing and New Business Development/`** — `New Business Development/Proposals and SOWs/` (SoW examples), `.../Pitch Materials/One-Pager Case Studies/`, `Marketing and PR/Events and Public Presentations/`, `Offering Development/`.

**Routing cheat sheet:**
- Project deliverables, research, workplans → `Clients/{client}/{engagement}/`.
- Known engagement code → search term AND `folderName` filter (most reliable discriminator).
- AI work products / Cowork outputs → `Claude Working Folder/` within the engagement; filter `folderName: Claude Working Folder`.
- PPTX/Excel templates → `Newry Templates_Client Facing/`.
- Newry Ladder, HR, handbook → filter `folderName: People & Recruiting`. Search the Ladder as **"Newry Consulting Ladder"** (not "Newry Ladder"). Do NOT use `folderName: ACC Templates and Ladder` — that filter does not work.
- Example slides, training → `TOOLS-TRAINING/`.
- SoWs → `Project Management/` within the engagement first; `New Business Development/Proposals and SOWs/` second (Corning almost never has one).
- Secondary research → within each project folder; no firm-wide library.
- **Consulting-process training** (problem statements, issue trees, workplanning, EM skills) — broad keyword search fails here; those terms are everywhere. Search directly in `TOOLS-TRAINING/EM Training and Materials/` (EM Skill Building, CLST Series, EM Handbook, Problem Structuring), `TOOLS-TRAINING/Thought Leadership/`, or `On Boarding Materials/`. Use `folderName` filters like `EM Training and Materials`, `CLST Series`, `Thought Leadership`, `Onboarding`.

## Feedback capture

Read and follow the shared feedback-capture sub-skill: `../../../feedback-capture/SKILL.md`. When logging: `Plugin:` → `newry-knowledge`, `Sub-skill:` → `sharepoint-search`.
