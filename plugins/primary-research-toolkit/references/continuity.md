# Proactive Continuity — Shared Block

*Referenced by the PRT coordinator (`../SKILL.md`) and by ICS, Interview Prep, and Corpus Query — any sub-skill that opens on an in-progress project. One shared definition so a solo maintainer doesn't have to keep behavior in sync across seven files.*

**Relationship to Step 0 (`project-setup/SKILL.md`):** Step 0 answers "which project/client is this, and does the folder structure exist?" — identity and scaffolding. This block answers a different question, one layer in: "given this confirmed project, what does the research corpus actually look like right now?" Run Step 0 first (or confirm it already ran this session); this block never re-verifies identity or re-scaffolds folders.

**State model (locked — see decision-log 2026-07-10):** PRT does not maintain a bespoke state file. "State" is the artifacts already produced — canonical Markdown cards/Roll-up, the pipeline tracker, `materials/` — read fresh each time, because centrally-synced skill files get overwritten on every update and a state file living there would be wiped. Treat state as a **point-in-time inventory**, never a linear progress bar — consultants enter at any stage, do work outside the tool, and add interviews over many rounds; "done" doesn't apply, only "as of right now."

---

## 1. Startup read

On wake in a project's `Primary Research/` folder, before acting:

1. **List `materials/`** — transcripts/notes present, by normalized source filename (lowercase, spaces→hyphens, special chars stripped — the same key ICS uses when naming cards).
2. **List `outputs/`** — canonical cards/Roll-up Markdown and their docx renders, the Interview Matrix, the pipeline tracker (Interview Acquisition's tracker, if present).
3. **Identity-map, don't count.** Match each material to the card(s) that cite it (cards reference their source file). A material is "coded" once at least one card cites it. This names the actual missing work ("Smith and Torres transcripts are uncoded") rather than a bare count delta. Group/repeat interviews aren't 1:1 (one file → several people, or several files → one person) — list ambiguous cases rather than guessing a count.
4. **Detect shape**, and orient differently per shape:
   - *Empty* (no materials, no outputs) — fresh start. If it's unclear where the working folder even is, ask before scaffolding anything (don't assume one exists).
   - *Materials present, no cards* — offer to start Mode 1 coding, or Transcript Ingestion if `materials/` is empty but the consultant mentioned Otter.
   - *Cards exist, no Roll-up* — enough to run Mode 2 Roll-up; say so.
   - *Roll-up exists* — check its `coverage-method:` marker (see ICS SKILL.md §Coverage table). An older-or-unmarked Roll-up is **not comparable** to current ratings — flag "re-run to refresh" rather than treating its flags as current.
   - *An artifact that doesn't look like PRT's own output* (hand-made notes, a differently-structured doc, something from outside the tool) — **flag it explicitly as unrecognized**, never fold it silently into a count or assume it's stale PRT output. Ask what it is if it matters to the current task.
5. **Low confidence → say so, don't recommend confidently.** If the folder is ambiguous (unrecognized artifacts, ragged filenames, a shape that doesn't match any case above), state the uncertainty and ask rather than issuing a confident greeting off a shaky read.

## 2. Prescriptive greeting — lead with the best next move

**If the consultant's opening message already names a task** ("code these three transcripts," "what did people say about pricing"), do that task. Don't front-load a status read — at most one line at the end: "(want a full status read on this project?)".

**On a genuine cold open** (no task named, or first message after a gap), don't just list what's on disk — **open with the single highest-value next move and the reason for it**, then offer one or two alternatives. Pick the recommendation by walking this order (first that applies wins), reading only from what's already in the folder:

1. **Uncoded transcripts sitting in `materials/`** → "code these first" (nothing downstream is trustworthy until they're in).
2. **All coded, no Roll-up yet** → "run the Roll-up" (the synthesis the corpus is ready for).
3. **Roll-up exists, a branch reads Thin/Insufficient on the current method** → "the [X] branch is thin on [directness/diversity] — worth targeting [source type] next," or prep a confirmed interview that can fill it.
4. **Roll-up exists and is stale-method (no/old `coverage-method` marker)** → "re-run the Roll-up to refresh coverage" (see §1).
5. **Confirmed interviews on the pipeline, none prepped** → "prep the calls."
6. Nothing obvious → present the inventory and ask.

Say plainly what the read can't see (calendar, client priorities, what the partner asked for) so the recommendation reads as "best from what I can see," not omniscient — and it's always overridable (L6). Example:

> "You've got 6 of 9 transcripts coded and 3 still uncoded in `materials/`. **Best next move: code those 3** — the Roll-up can't be trusted until the corpus is complete. After that, the distributor branch is the one to watch (it's Emerging — 2 sources, both one region). I can't see your calendar or what's most urgent for the client — want to start with the coding, or something else?"

Lead with one move. Alternatives are a short tail, not a menu.

## 3. Mid-run save

Append each unit to the canonical Markdown as it completes (a card as its transcript finishes; the Roll-up on completion) — so an interruption partway through a batch keeps everything already written. Don't rely on file modification time for freshness (OneDrive/Cowork sync and hand-edits corrupt it) — derive state from reading content.

## 4. End-of-step next move — lead with one, offer alternatives

Close every sub-skill's output the same way: **one recommended next move + the reason, then one or two alternatives.** This is the most-repeated proactivity signal — it should make the tool feel like it's walking the consultant through the workflow, not dumping output and going quiet. Read the recommendation from current inventory + where the just-finished step lands in the workflow. Examples:

> "Card done — 7 of 9 coded now. **Next: code the last 2**, then run the Roll-up on the full set. (Or roll up the 7 now if you need a read before the last two land.)"

> "Roll-up done. **Next: the distributor branch is Emerging — prep [name]'s call to fill it**, since they're the one confirmed source who can. (Or hand the Roll-up to SoF Draft if you're ready to write.)"

Vary the phrasing; don't fire an identical sentence every time. One move leads; alternatives are a short tail, never a numbered menu, never a question the run waits on. Never rank findings as fact or decide for the consultant (L6) — propose, basis shown, overridable. (This replaces ICS's older flat one-line trailer — the trailer's no-menu, no-question discipline still holds; it just now leads with a recommendation instead of a bare pointer.)

## 5. Progress narration

On a long run (ICS coding a batch, then the multi-pass Roll-up), narrate milestones — "coded 6 of 9… rolling up across the corpus… checking coverage per branch." Any count in narration must come from an actual tally of completed units, not generated prose, and should only report units that actually finished (not a projected total).
