---
name: expert-number-triangulation
description: "Part of the Primary Research Toolkit. Pull every number experts gave across a project's interviews (market sizes, capex, prices, volumes, capacities, timing), put them on one basis, show where experts agree and split, and propose Low / Base / High ranges in an Excel workbook — optionally comparing against, filling a copy of, or building a starter model. Trigger on \"pull the numbers from these interviews,\" \"what numbers did the experts give,\" \"triangulate the expert numbers,\" \"compare the experts' figures,\" \"where do the experts agree on cost,\" \"build assumption ranges from the interviews,\" \"fill our model from the interviews,\" \"check our model against what experts said,\" \"build a starter model from the interviews.\" Do NOT use for qualitative findings — that is Interview Coding & Synthesis."
---

# Expert Number Triangulation

Built by Anna D'Amico; adapted for the Primary Research Toolkit (PRT v1.6.0, 2026-10-30).

Turns a project's expert interviews into an auditable, normalized view of every quantitative claim experts made. The team sees where experts converge, where they split, which assumptions are still thin, and what to ask in the next interview, **before** building the model. If the user provides a model, it can also fill a copy of that model's inputs from the interview evidence. If the user has no model yet, it can build a starter model from the assumption ranges.

Where it sits: Transcript Combine cleans transcripts, Interview Coding & Synthesis handles qualitative findings; this sub-skill handles the numbers.

This skill does not pick the "right" number. It lays out what experts said, proposes ranges with the reasoning shown, and the consultant decides what goes in the model.

**Already done by the coordinator before you start:** project setup (Step 0), continuity read (Step 0.5), usage logging. Don't repeat them.

## Modes

- **Triangulate (default):** produce the triangulation workbook (Steps 1-8).
- **Triangulate + fill model:** the user gives a model (.xlsx) to fill. Do Steps 1-8, then Step 9 (Fill the model). Both files are delivered.
- **Triangulate + compare to model:** the user gives a model only to check against. Add "Model vs. interviews" flags; do not fill or edit anything.
- **Triangulate + build model:** the user has no model and asks to build, start, draft or set up one from the interviews. Do Steps 1-8, then Step 10 (Build a starter model). Both files are delivered.

If the user provides a model and it's unclear whether they want it filled or only compared, ask once. If the user mentions a model but doesn't attach one, ask once whether they have one to share or want a starter model built.

## Output: always Excel

Every deliverable is a Microsoft Excel file (.xlsx), built with the xlsx skill:
- `<Project> - Expert Number Triangulation.xlsx` (always)
- `<original model name> - filled from interviews.xlsx` (fill mode only)
- `<Project> - Starter Model (from interviews).xlsx` (build mode only)

Rules:
- Do **not** deliver results as a Sheets/spreadsheet artifact, a Claude Doc, an HTML page, a Word file, a markdown file, or a table in chat, even if one of those would normally be the default.
- Save every file to `Primary Research/outputs/` (in simple mode, with no project folder structure, save to the root of the mounted folder) and present it in the conversation so the user can open it.
- If LibreOffice recalculation isn't available, still deliver the workbook, say plainly that it was not recalculated or checked for formula errors, and ask the user to open it in Excel and check the Summary tab before relying on it.
- The chat reply is only the short report in Step 8 plus where the files were saved. Never paste workbook contents into chat.
- On re-runs, update the same workbook (same file name, stable Evidence Log IDs) rather than changing the format.

## What counts as a source

**Core (primary research) - this is what the skill is built on:**
- Transcripts in `Primary Research/materials/`: Otter exports, expert-network transcripts (GLG, Tegus, AlphaSights, etc.), translated transcripts, and `Combined Transcript - <Name> - <date>` files from Transcript Combine
- Interview notes and written expert responses (lower weight: paraphrased, not checkable against a recording)

A verbatim transcript export from any tool (Otter, Granola, Zoom, Teams) counts as a transcript. Two files of the **same call** are duplicate recordings (offer Transcript Combine, use one); two files from **different dates** with the same expert are separate calls (log each).

**Interviewer notes** for a call that also has a transcript are a cross-check only: log numbers from the transcript, and use the notes for "Notes vs. transcript" flags. Log numbers from notes only when no transcript exists.

**Never a source for numbers:** AI summaries, Granola summaries, and PRT summary cards. They can misstate figures. Use them only to find which interviews cover which topics, and to raise "AI summary vs. transcript" flags when they disagree with the transcript.

**Optional benchmarks (secondary) - only when the user provides or asks for them:**
- Public filings, disclosures, analyst reports, articles
- Used only as **cross-checks** against what experts said. They get their own "Benchmark" rows and flags, and never set a range on their own. Don't go searching for secondary sources unless the user asks.

## Inputs (ask only for what's missing)

1. **Topic** (e.g. capex for a new specialty-materials plant), plus the **line items the model will need** if known. The project code comes from Step 0. If a model is provided, derive the line items from its input cells. Otherwise derive them from what experts covered and confirm. In build mode, also ask what the model should answer (the headline output(s)) if it isn't clear.
2. **Interviews:** read from `Primary Research/materials/`.
   - Choose files per interviewee using the coordinator's *Which transcript to code* rules: prefer a Combined Transcript; if a call has several recordings and no combined file, offer Transcript Combine first. If the consultant declines, use the most complete recording and lower confidence on garbled numbers. Never block the run because combining didn't happen.
   - If `materials/` is empty or missing interviews, offer the coordinator's **Transcript Ingestion** (Otter / Granola pull) rather than searching Otter yourself. Interview notes on SharePoint can be read with `Microsoft 365:sharepoint_search` + `Microsoft 365:read_resource` and saved into `materials/`.
   - If `Primary Research/glossary.md` exists, use it to read garbled terms and names correctly (see `../../references/glossary.md`).
3. **Model (optional):** an .xlsx to fill or compare against, and which mode. Or, in build mode, no model.
4. **Benchmarks (optional):** any secondary documents the user wants used as cross-checks.

## Step 1: Fetch, save, and classify

- Save every source as plain text in `Primary Research/preprocessed/number-triangulation/` (working files, kept out of `outputs/` so consultants only see deliverables there) (parse persisted JSON outputs when a result is too large); you need the text to verify quotes in Step 7.
- Classify each source, because it sets how much weight it gets:
  - **Recording / transcript** (Otter, combined, expert network): verbatim and timestamped; audio quality varies. A Combined Transcript's flagged passages keep their flag — treat numbers inside them as Medium confidence at best.
  - **Translated transcript**: keep translator notes ([TN]) and treat flagged passages as Medium confidence at best.
  - **Interview notes / written responses**: paraphrased; mark "not verifiable against a recording."
  - **Benchmark** (optional, secondary): record section/table as location; keep original units and currency.
- For each expert, record name/role, network, call date, link, and **what product/scope they actually know**. Flag experts whose experience is adjacent (e.g. commodity grade vs. specialty grade) so their numbers aren't compared like-for-like.

## Step 2: Extract every number

Read each interview fully. **Work one interview at a time:** write that interview's rows to `preprocessed/number-triangulation/evidence-<source key>.csv` before reading the next, and build the workbook from those files, not from memory. Large projects run to hundreds of numbers across a dozen calls; holding them all in context is where numbers get dropped or blended.

For each quantitative claim, log:

- ID, expert, date, category / line item, metric
- Low / high values and **unit** (keep original currency; convert in formulas with a labeled FX cell)
- Basis: scale, geography, greenfield vs. brownfield, design/configuration, what's included or excluded
- **Verbatim quote** ("..." for cuts, [Name] for speaker changes) and the timestamp or page
- Confidence: High / Medium / Low, with a reason

**One metric per Evidence Log row.** Low and High are always the same metric in the same unit. If an expert gives two related figures in one breath (e.g. 96 bushings producing 7,000 t/yr), log two rows. Never put one metric in Low and another in High.

Watch for:
- **Interviewer recaps.** When the interviewer restates the math and the expert says "yes", redo the arithmetic. If the recap is wrong, don't log the recap figure as the expert's number; compute the correct figure in the Comparison tab and raise a flag.
- **Mid-answer corrections.** Log the final answer and note the change.
- **Garbled or translated numbers.** Use context, restatements and the glossary; lower the confidence.
- **Same expert, multiple calls.** Log each separately; changes between calls are a finding.
- **Mismatched pairs.** E.g. an expert quoting a project's cost next to a whole plant's output, or new capacity vs. total capacity. Ask what each number covers.
- **How numbers combine (build mode).** Note any relationship experts describe between quantities (e.g. "cost scales with machine count", "yield loss is on top of downtime"); these become the model's formula logic in Step 10.

## Step 3: Normalize

Put comparable metrics on one basis, using Excel formulas (not hard-coded results):
- Capex per unit of annual capacity; unit prices; productivity ratios
- **Try more than one unit when experts seem to disagree.** A conflict in one unit (e.g. tonnes per machine) can disappear in another (meters per machine), which shows the real driver is a conversion assumption.
- Geography premiums: apply each expert's **own** premium to their **own** number, only to the portion they said it covers
- Keep conversion assumptions (FX, width, weight, uptime) in labeled input cells
- In fill mode, also normalize to the **model's** units, currency, and basis (e.g. $M vs $, per t vs per m, Asia vs US) so values can drop straight in.
- In build mode, normalize to the units and basis agreed for the starter model in Step 10.

## Step 4: Flag

One flag per issue, ranked High / Medium / Low / Agreement / Thin:
- **Expert vs. expert:** spread > ~1.5x on the same normalized metric, with likely reasons
- **Different designs or scopes:** experts describing structurally different setups. These aren't errors; they're scenarios
- **Same expert, different calls**, and **internal math** that doesn't reconcile
- **AI summary vs. transcript**
- **Notes vs. transcript:** where interviewer notes for the same call give a different figure than the recording, log the transcript figure and flag the difference
- **Unit conversion:** apparent conflicts that come from a conversion assumption
- **Agreement:** independent experts who converge, including cross-checks that combine experts (A's unit count x B's unit price lands on C's total)
- **Thin coverage:** single-expert or Low-confidence-only line items
- **Expert vs. benchmark** (only if benchmarks were provided)
- **Model vs. interviews** (when a model is provided): the model's existing value sits outside the expert range, or the model has inputs no expert covered
- **Missing driver** (build mode): a driver the starter model needs that no expert covered

Each flag gets the specific numbers, evidence IDs, and a suggested next step, usually a specific question for a specific expert or expert type.

## Step 5: Propose assumption ranges

For each line item: **Low / Base / High** on the normalized basis, built from expert evidence. Include the supporting evidence IDs, why the base was chosen, what was excluded and why, and an "ask next." Status: **Converging** (2+ independent experts within ~1.5x), **Split**, **Thin** (one expert), **Alt. design** (a valid scenario on a different basis), or **Gap** (a needed line item no expert gave a number for). Note any benchmark that supports or contradicts the range, but don't let a benchmark set the range alone. Add a check row where components should add up to a total.

## Step 6: Build the triangulation workbook

Read and follow the xlsx skill before building (openpyxl; Arial; blue hard-coded inputs, black formulas, green cross-sheet links, yellow fill for assumptions the user should confirm; recalc with LibreOffice; zero formula errors). Low/High in Assumption Ranges link by formula to the Comparison tab, which links by formula to the Evidence Log. Don't start text cells with "=". Freeze header rows and add filters. Tabs, in this order:
1. **Summary** (first tab, opens by default; gridlines off): a one-page read for someone who won't open the other tabs.
   - Header line: number of sources, numbers logged, that quotes were verified, and that Base is a proposed judgment.
   - **Key numbers table:** ~10-20 headline line items grouped by section (e.g. by stage of the value chain, plus Timing), columns Line item | Unit | Low | Base | High | Status | One-line read. Low/Base/High/Status are formulas linking to Assumption Ranges (green), so they update when a Base changes. Color the Status cell. Include US/geography-derived rows and any Alt. design scenario.
   - **Top findings:** 4-6 one-line bullets (structural findings, what converges, the widest gap, the biggest open input).
   - **Ask next:** the priority-1 questions from Open Questions.
   - **Model fill / compare / build** (only in those modes): 1-2 lines on what was filled, flagged, or built (and the starter model's Base output, if built).
   - **Flag count:** COUNTIF of each severity on the Flags tab.
2. **Flags**
3. **Assumption Ranges**
4. **Comparison:** inputs block (FX etc.) at top, then normalized side-by-side tables with spread ratios
5. **Open Questions:** ask-next items, columns Priority (1-3) | Ask (expert / expert type) | Question | Line item(s) | Why it matters | Flags (flag IDs). Interview Prep reads this tab, so keep the columns exact. Also usable for expert-network follow-ups or the next round of sourcing
6. **Evidence Log:** every number, quote, location, link, source type, and confidence; filterable
7. **Sources:** experts (and any benchmarks), type, scope, # of numbers logged (COUNTIF formula), link
8. **Model Map** (fill, compare or build mode only): one row per model input cell - sheet!cell, model label, model unit, matched line item, value written (or existing value), Low/Base/High, status, evidence IDs, note

Name it `<Project> - Expert Number Triangulation.xlsx`.

## Step 7: Verify before delivering

- Programmatically check every quote against its saved source text: split on "..." and [speaker] markers, ignore whitespace differences, and confirm each fragment appears. Fix anything that doesn't match.
- Check that each logged value actually appears in (or is directly computed from) its quote, in the logged unit. A real quote with a misread number or unit still passes the quote check, so this is a separate pass.
- Confirm every Evidence Log row has Low and High in the same unit (one metric per row).
- Recompute every flag's and range's arithmetic and make sure the text matches the workbook values (read the recalculated .xlsx back).
- Recalculate and confirm zero formula errors.
- Confirm the Summary tab is first and its numbers match Assumption Ranges after recalc, and its findings text matches the Flags tab (including any flags downgraded during verification).
- Confirm each .xlsx opens, has the expected tabs, and was saved to `Primary Research/outputs/`.
- Fill mode: also run the Step 9 checks. Build mode: also run the Step 10 checks.

## Step 8: Report

In 3-5 lines: what's converging, what's split, what's thin, any structural finding (e.g. two plant designs), and the most important questions for the next interviews. In fill mode, add one line: how many model inputs were filled, how many left blank, and the biggest model output change if visible. In build mode, add one line: the headline output at Low / Base / High, how many drivers came from interviews, and how many are still gaps. Say where the Excel files were saved and point to the Summary tab. Don't restate the workbook.

## Step 9: Fill the model (fill mode only)

1. **Never touch the original.** Copy it to `<original model name> - filled from interviews.xlsx` and work only on the copy. Keep macros if .xlsm (`keep_vba=True`); preserve external links (check the xlsx skill's guidance before re-saving).
2. **Read the model fully** (formulas and cached values; two loads). Identify input cells using the model's own conventions (blue font, shaded/yellow cells, an Inputs/Assumptions tab, or hard-coded numbers feeding formulas). Note each input's label, unit, currency, and basis, and any Low/Base/High scenario columns.
3. **Map inputs to line items** and show the user the proposed mapping (a short list: model cell -> line item -> value to write) before writing anything. Ask about any ambiguous mapping once.
4. **Write values into input cells only.** Use Base by default; fill Low/High scenario columns if the model has them. Convert to the model's units and currency. Never overwrite a formula, never change formatting or structure, never add rows inside the model's ranges.
5. **Leave a trail in the copy:** add a cell comment on every filled cell (line item, Low/Base/High, status, evidence IDs, confidence). Add a **Source Map** tab to the copy listing every filled cell, its old value, new value, and evidence IDs.
6. **Don't guess gaps.** Inputs no expert covered keep their original value (or stay blank if blank) and get yellow fill plus a comment "Not covered by interviews - see Open Questions." Add them to Open Questions. Thin or Split items are filled with Base but commented with their status.
7. **Check:** recalc the copy, confirm zero new formula errors (compare against the original's errors), confirm no formula cell changed (diff formulas original vs copy), and list key model outputs before vs after in the Model Map tab.

## Step 10: Build a starter model (build mode only)

The goal is a clean, transparent first draft the team can take over and extend, not a finished model. Keep it as simple as the question allows.

1. **Agree the question.** Confirm the headline output(s) (e.g. total capex for a plant of a given capacity, cost per unit, annual revenue at scale), the scope (greenfield/brownfield, geography, scale), units, currency, and whether timing matters. Ask once for anything that isn't clear from the request or the interviews.
2. **Propose the structure before building.** Show the user a short driver tree: each output as a formula of drivers (e.g. Capex = machines x price per machine + building + utilities), and for each driver the matching Assumption Ranges line item and status (Converging / Split / Thin / Alt. design) or "gap - not covered." Use relationships experts described (Step 2) where possible; otherwise use the simplest standard arithmetic and say so. Wait for the user to confirm or adjust.
3. **Build with the xlsx skill** (same formatting rules as Step 6). Tabs, in this order:
   - **Read Me:** what the model answers, scope and basis, that it's a starter model built from interviews on <date>, how to use it, and the color legend.
   - **Inputs:** one row per driver: label, unit, Low, Base, High (blue hard-coded values copied from Assumption Ranges, already converted to the model's units/currency), status, evidence IDs, note. Yellow fill on Split, Thin and gap rows. Conversion assumptions (FX, uptime, etc.) in their own labeled block. No links to the triangulation workbook, so the model stands alone.
   - **Calculations:** formulas only, no hard-coded numbers, laid out step by step with labels and units, in three columns (Low / Base / High) so all scenarios are live at once. Add a simple timeline only if experts gave timing and the user wants it.
   - **Outputs:** headline outputs in Low / Base / High columns, linked to Calculations (green). Note under the table that Low/High are "all-Low inputs" / "all-High inputs" cases, not statistical bounds, and that a low input can push an output up (e.g. a lower price). If any driver feeding an output is a gap, show "Incomplete - see Inputs" with an IF formula rather than a misleading number.
   - **Checks:** component sums vs totals, error checks (ISERROR count), count of gap inputs; each check shows OK / CHECK.
4. **Don't guess gaps.** Drivers no expert covered stay blank with yellow fill and a comment "Not covered by interviews - enter value or see Open Questions." Use an outside or assumed number only if the user supplies or approves it, and label it as such in the Note column.
5. **Keep scope tight.** No financing, tax, depreciation, sensitivity tables or multi-year projections unless the user asks. Mention in the report what an obvious next extension would be.
6. **Record it in the triangulation workbook:** list every starter-model input in the Model Map tab (cell, label, unit, line item, Low/Base/High, status, evidence IDs) and add Missing-driver flags and Open Questions for gaps.
7. **Check:** recalc, zero formula errors, every Calculations and Outputs cell is a formula, every input row has evidence IDs or a gap label, and the Base output matches an independent recomputation in Python.

Name it `<Project> - Starter Model (from interviews).xlsx`.

## Re-running as interviews come in

Append new interviews to the existing workbook's Evidence Log (keep IDs stable), refresh flags, ranges and the Summary tab, and call out what moved since the last run (e.g. "Machine price went from Split to Converging after the latest supplier interview"). In fill mode, refill a fresh copy of the user's current model and note which inputs changed. In build mode, if the user hasn't edited the starter model, update its Inputs tab in place; if they have, treat it as their model and use fill mode on a copy.

## Hand-offs to the rest of the toolkit

- **Open Questions → Interview Prep.** Interview Prep reads the Open Questions tab automatically and puts matching number questions into each interviewee's guide. Keep the tab's columns exactly as specified (Priority | Ask (expert / expert type) | Question | Line item(s) | Why it matters | Flags), and name people, companies or interviewee types in "Ask" the way the pipeline tracker does, so the match works.
- **Numbers vs. qualitative findings.** For figures, the workbook is the more careful source than summary cards; say so if the consultant asks which to trust.

## Guardrails

- Never fill a gap with an outside or assumed number without labeling it as such.
- Never edit the user's original model; only a copy, and only its input cells.
- In compare mode, read the model and flag differences; don't fill anything.
- A built model is always labeled a starter model built from interviews; it is not a reviewed client deliverable.
- Client and expert data stays within Newry's approved tools per the internal AI policy.
