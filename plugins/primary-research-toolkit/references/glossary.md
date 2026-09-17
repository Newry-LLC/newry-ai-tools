# The project glossary — shared reference

Read this when building, reading, or applying a project glossary. Two sub-skills use the same
file: **Transcript Combine** (which usually creates it, since it runs first) and **Interview
Coding & Synthesis** (which grows it from the corpus). This is the single source of truth for
where it lives, how it is written, and how it is applied.

## Where it lives

`<project-root>/Primary Research/glossary.md` — one file per project, travelling with the project.

If a glossary exists anywhere else, the toolkit will not find it. Move it here rather than
pointing tools at it.

## The format, exactly as the script parses it

`scripts/term_reconcile.py` reads sectioned Markdown. The canonical spelling goes in bold before
the arrow; every variant it should replace goes after, each in backticks.

```markdown
## Confirmed corrections (auto-apply forever in this project)
- **Nafion** ← `naphion`, `nay-fee-on`
- **Tegus** ← `teigas`, `tgs`

## Best-inference corrections (auto-apply, medium confidence — review periodically)
- **Veltrix** ← `Veltrex`

## Contextual corrections (apply only with anchor keyword in same paragraph)
- **Alta** ← `altar` (anchors: `resin`, `supplier`)

## File-specific corrections
### Randall Jenkins
- **lithotripsy** ← `lithovripsy`, `lithotropy`
```

**The script fails quietly.** An entry it cannot parse is skipped — no error, no correction
applied. A glossary that looks right and reads zero entries is the failure to watch for, so prove
it with `--dry-run` rather than trusting the file (see *Applying it* below).

## Where a term belongs

The section is the decision. Getting it wrong is either a wrong correction applied forever, or a
right one never applied.

| Section | Use when | Why |
|---|---|---|
| **Confirmed** | You have seen this mis-hearing in a transcript | Auto-applies everywhere, forever in this project |
| **Best-inference** | You are predicting a mis-hearing before any transcript exists | It is a guess. Still auto-applies, but flagged for periodic review |
| **Contextual** | The word has a legitimate literal use in this project | Only corrected near an anchor word, so "altar" survives for a church client |
| **File-specific** | One speaker or file mangles a term the others get right | Scoped to that file by name-token match |

A term you cannot classify stays out. A silently wrong correction applied across a corpus is worse
than an uncorrected word a reader can see.

## Building it

Whichever sub-skill runs first creates the file; the other reads and grows it. Never create a
second one.

**From documents** — available immediately, and the only route before any transcript exists. This
is what Transcript Combine uses on the first interview:
- Project and client name
- Interviewee names, from metadata or the Airtable contact record
- Branch labels and key concepts from the analytical frame
- Acronyms and proper nouns from the SoW or issue tree
- The interview guide and the kickoff deck — usually the densest source of acronyms
- Every likely speaker's full name (the speaker roster needs these too)

Predicted mis-hearings from this route go under **Best-inference**, not Confirmed.

**From the corpus** — once transcripts exist, terms are found rather than predicted. Interview
Coding & Synthesis owns this half; its detection categories and impact-confidence matrix are in
its own SKILL.md. Confirmed mis-hearings observed this way move to **Confirmed**.

A term learned by either route belongs in the file, so the next interview inherits it. A glossary
that stops growing is the most likely reason later interviews come out worse than earlier ones.

## Applying it

```bash
python3 scripts/term_reconcile.py --input <pre-processed dir> \
    --glossary "<project-root>/Primary Research/glossary.md" [--dry-run]
```

- `--dry-run` changes nothing and reports entries read plus fixes it would apply. Use it after any
  hand-edit of the glossary
- Applies every Confirmed and Best-inference correction in place across `.preprocessed.md` files,
  handling contextual anchors and file scoping
- Safely re-runnable: prior fix logs are masked, never duplicated. Originals are never touched
- On Windows, `python3` resolves to a Microsoft Store stub that fails — use the full interpreter
  path

**Do not hand-edit transcript text to apply a term.** Deciding a term is judgment; applying it is
repeatable, fragile logic that belongs to the script.

## Two things that look like problems and are not

- **Both sub-skills apply glossary fixes.** Applying a correction twice changes nothing — the
  second pass finds nothing to replace. Do not add logic to suppress it.
- **`decisions.json` has its own `glossary` map.** That is per-run scratch inside a
  transcript-combining run, not the project glossary. Terms settled during review get promoted
  into the project file.
