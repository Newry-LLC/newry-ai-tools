---
name: transcript-combine
description: "Merge one or more recordings of the SAME call into a single cross-checked transcript with named speakers and timestamps, flagging what could not be settled. Runs automatically after Transcript Ingestion when a call has more than one recording, and works on a single recording too. Trigger on \"merge these transcripts,\" \"I have two recordings of the same call,\" \"which version is right,\" \"clean up this transcript,\" \"degarble this,\" \"Otter garbled the names,\" \"make a master transcript,\" \"reconcile these,\" \"fix the speaker labels.\" Do NOT use it to synthesize findings across DIFFERENT interviews — that is Interview Coding & Synthesis, which this feeds."
---

# Transcript Combine

Built by Andrew Gartley as `gartleys-grandiose-degarbler`; adapted for the Primary Research
Toolkit. The reconciliation logic and all six scripts are his.

Two transcription tools listening to the same call fail in different places. Otter mangles a
clinical term but nails the speaker turns; Granola gets the term because it saw the meeting
title, but drops thirty seconds of crosstalk. Neither alone is trustworthy enough to quote a
client from. Where they *disagree*, one is usually right — and project context or a simple vote
usually says which.

Almost all of that work is mechanical, so scripts do it. **Your job is only the spans where the
evidence runs out.**

## What this produces, always

One file per interview: `Combined Transcript - <Name> - <YYYY-MM-DD>.docx` in `materials/`.

**Even from a single recording.** A consultant should never have to choose among three exports
of one call, and Interview Coding & Synthesis should never have to guess which file is real. With
one source there is nothing to cross-check, so the glossary, speaker and filler passes still run
and the header says plainly that no wording is corroborated.

The name is a convention, not a gate. PRT's *Which transcript to code* rules handle transcripts
that never came through here.

## Two rules that make this affordable

**1. Never read the transcripts or `alignment.json` in full.** Every script writes a small
`*.review.json` holding only what needs deciding. On a real 7,900-word interview that was 76 KB
against 164 KB of sources — about a fourfold saving, not the twentyfold an earlier version of
these instructions claimed. Reading the sources to "check the work" defeats the design and costs
several times as much for a worse result, because scripts do not get bored, skip passages, or
quietly improve someone's grammar.

**2. When the inputs don't fit the pipeline, do not repair them by hand.** Every such problem has
a scripted path below. If you find yourself about to pass transcript text to a subagent, paste it
into a heredoc, or rewrite turns manually, stop — that is the signal you have left the pipeline,
and the answer is a script or a question to the user, never manual labour.

Rebuilds are nearly free. If the output looks wrong, fix the decisions and rerun.

## Before the call

The number of independent recordings is the biggest driver of how much work this is: with two,
nothing can be settled automatically, because majority voting needs three witnesses. The
coordinator's *After ingestion* section carries the advice to give a consultant who is still
fielding.

## Output standard: clean verbatim

Every substantive word preserved exactly, with the noise of speech removed.

Remove: filler, stutters, false starts the speaker abandoned, unintentional repetition,
transcription artifacts.

Keep exactly as spoken: word choice, grammar including bad grammar, meaning-bearing hedges ("I
*think* it's about 40%" — the hedge is the finding), profanity, sentences left hanging, numbers as
stated.

The line to hold: any sentence must be quotable in a client deck and defensible. No smoothing, no
tightening, no making someone sound more articulate than they were. When you feel the urge to
improve a sentence, don't — that urge is the failure mode this skill exists to prevent.

## Running the scripts

On Mac, Linux, or inside Cowork's container, `python3` works as written below. **On Windows
`python3` resolves to a Microsoft Store stub that fails**; use the real interpreter path, e.g.
`C:/Users/<you>/AppData/Local/Programs/Python/Python314/python.exe`. Needs `python-docx` and
`pypdf`.

## Which model runs this, and why it is recorded

**Use Opus 5 for the judgment step, and put it in the header** as a `Model` row in
`decisions.json`'s `meta`.

The scripts use no model at all. The only model work is deciding the disagreements the scripts
could not settle, and choosing what to flag — and that is where quality varies run to run. Across
one real project, flagging fell from three per interview to zero over five weeks while the scripts
produced identical mechanical results, and nothing in the output recorded what had changed.

Two things have to be fixed for one run to be comparable to another: the inputs (which recording
is the anchor, which share a vote, which are summaries that must not vote — all named in the
header already) and the model. Pin both, record both. A transcript that looks worse than an
earlier one can then be traced to a cause rather than a hunch.

## Workflow

### 1. Identify the call and get the glossary

Ask which interview and which project.

**One glossary per project, shared with the rest of the toolkit.** It lives at
`<project-root>/Primary Research/glossary.md` and is the same file Interview Coding & Synthesis
seeds and grows and that `scripts/term_reconcile.py` parses. Do not create a second one, and do
not write a different format into it — `term_reconcile.py` silently applies nothing when it
cannot parse an entry.

**Read it first.** A project runs fifteen or thirty interviews sharing almost all their
vocabulary, so if one exists, read it and go to step 2. This is the biggest saving across a
project, and a glossary that stops growing is the most likely reason later interviews come out
worse than earlier ones.

**If there is none, seed it** — this sub-skill runs before Interview Coding & Synthesis, so
it is often first. Use ICS's seeding sources: project and client name, interviewee names from
metadata, branch labels and key concepts from the analytical frame, and acronyms and proper nouns
from the SoW or issue tree. Add the interview guide and kickoff deck, which are usually densest in
acronyms. Search for those yourself rather than making the user hunt for paths.

**Write it in ICS's three-state format**, which is what the shared script expects:
*Confirmed correction* (auto-apply forever in this project), *Confirmed non-correction* (never
flag again), *Pending* (surfaces for review). Note the expected mis-hearings alongside each term
where you know them ("Nafion — expect 'naphion', 'nay-fee-on'"); that is what makes a garble
recognizable on the next interview. Cover client and competitor names, products, technical terms,
acronyms, and every likely speaker's full name.

`decisions.json`'s own `glossary` map is a per-run scratch, not the project glossary. Terms
settled during review get promoted into the project file at step 7.

**Speaker roster.** Named speakers are required in the output; tools label people "Speaker 1" or
"Me"/"Them". Build the roster from the interview guide header, the Airtable contact record, the
labels the sources carry, self-identification in the opening minutes, and the user — ask them,
they were on the call. Do not consult calendars. Record each as **Name (Company or Newry)** and
note the interviewer.

### 2. Fetch and normalize

- **Otter and Granola** — PRT's Transcript Ingestion pulls these into `materials/`.
- **Files** — `.pdf`, `.docx`, `.vtt`, `.srt`, `.txt`, pasted text. A scan with no text layer
  needs OCR first via the `pdf` skill.
- **Expert-network exports (AlphaSense, Tegus, Guidepoint, GLG, InexOne)** — these bundle
  paraphrased and verbatim material in one file, so never judge them by the vendor name or the
  first page. Most contain a **full verbatim transcript somewhere in the document**, usually after
  the summary. Keep that body, drop everything else, save it as its own `.txt` named for the
  vendor, and normalize *that*. `references/reconciliation-rules.md` §2 has the per-vendor shapes
  and what to strip.

  Be careful: one such export ran 53,000 characters with its transcript heading at character
  51,645 — a paraphrased summary with no verbatim body, which would have been wrong to treat as a
  witness. Step 3 confirms whether it earns a vote.

```bash
python3 scripts/normalize_transcript.py sources/otter.vtt --source-name Otter --out normalized/otter.jsonl
```

### 3. Preflight — and stop if it's difficult

```bash
python3 scripts/check_sources.py normalized/*.jsonl --json preflight.json
```

Do this before anything else. It costs a few hundred tokens and answers the questions that are
ruinous to discover late: is each file actually a verbatim transcript, are the speaker labels
usable, how many *independent* sources can really vote, and are two files the same transcript
twice. Exit 0 for a straightforward set, 2 when a human should decide.

**If the verdict is anything but STRAIGHTFORWARD, show the user the verdict and its recommended
path, and ask how to proceed.** Say plainly what will be harder and why. The user may want to
proceed, fix a source, supply another, or skip the interview. It is much cheaper to ask now.

Findings and what they mean:

- **A paraphrased source** — an analyst report, a note-taker's write-up, or the summary section
  of an expert-network export. Not a record of what was said, so it must never anchor or vote.
  Use it for the glossary and for understanding what was meant. (If the user explicitly asks, it
  may settle a conflict the verbatim sources cannot — to confirm which reading was *meant*, never
  to supply wording. Say so in the `notes`.)
- **An expert-network verbatim transcript is a real voting source**, and often a better anchor
  than a live tool: an InexOne transcript carries named speakers and timestamps. In testing, a
  professional transcript was the only source carrying a threshold figure correctly where the ASR
  garbled it — worth more as a second witness than another ASR.
  Two caveats: these exports carry licence terms that may restrict use with AI tools, so confirm
  the user is comfortable; and it still needs the glossary and filler passes.
- **Collapsed diarization** — turns holding both speakers. Go to step 4 before aligning.
- **Fewer than two independent verbatim sources** — nothing can be cross-checked. Run the
  single-source path in step 5 and be explicit about it in the `notes`.
- **Duplicates** — a PDF print and a live pull of the same session. Give them the same `:GROUP`.
  This is the easiest way to get a wrong answer out of the pipeline, and interview folders do
  hold the same export twice.

Then confirm the plan with the user: interview and project, speaker roster, each source's size
and anything odd, glossary terms in play, and **which source is the timing anchor**. Ask whether
they have **audio or video paired with one of the transcripts** — if so that transcript should be
the anchor, so a flagged timestamp points at something they can scrub to. Name the anchor and the
recording in the header. With no timestamps anywhere, flags cite turn numbers instead.

### 4. Repair attribution, if preflight flagged blobs

A tool that tags a long back-and-forth under one speaker leaves the words intact but the
attribution wrong — and a quote on the wrong person's lips looks correct, so nothing downstream
catches it.

```bash
python3 scripts/segment_turns.py --propose normalized/granola.jsonl --out boundaries.json \
    --speakers "Andrew Gartley (Newry)" "Dana Whitfield (Acme Materials)"
```

Read `boundaries.review.json` — each candidate boundary with a dozen words either side, a
confidence, and a guess at who speaks next. Accept the ones that are real speaker changes:

```bash
python3 scripts/segment_turns.py --apply normalized/granola.jsonl decisions_boundaries.json \
    --boundaries boundaries.json --out normalized/granola.split.jsonl \
    --speakers "Andrew Gartley (Newry)" "Dana Whitfield (Acme Materials)"
```

Splitting happens by character offset, so no decision can alter a word; the script verifies the
word count is unchanged. Use the split file downstream. If boundaries look sparse, try
`--min-confidence low`; if a blob really is one long answer, leave it and note it.

`segment_turns` does *not* fix one speaker scattered across several generic labels (`Speaker 2`,
`Speaker 3`, `Speaker 5` all being the interviewee). Resolve that in `decisions.json`'s `speakers`
map, and if one label holds two people you cannot cleanly split, say so in the header `notes`
rather than guessing turn by turn.

Attribution reconstructed this way is good but not certain — say so in the `notes` for the
affected passage. If a high share of words remains in merged-speaker turns, `build_payload.py`
writes that disclosure automatically; do not delete it.

### 5. Align, then decide only what's left

```bash
python3 scripts/align_sources.py \
    --anchor normalized/otter.jsonl:otter \
    --source normalized/otter_pdf.jsonl:otter \
    --source normalized/granola.jsonl \
    --out alignment.json
```

Append `:GROUP` to files from the same engine so they share one vote. The script enforces two
rules so nobody has to remember them: votes count once per group, and **absence is never a vote**
— a source that drops content is not evidence the content is absent.

Strip obvious header/meta turns before aligning (a docx's title line, `Meeting Title`, `Date`,
`SUMMARY KEYWORDS`, `Meeting participants`) — the normalizer keeps them as speech and they inflate
the site count with junk.

**Single verbatim source:** same command with an anchor and no `--source`. No sites appear; the
glossary, filler and speaker work still apply, and garbles get caught by the glossary rather than
by disagreement. Record in `notes` that no wording is corroborated by a second witness.

Now read **`alignment.review.json` only**, and write `decisions.json` (`build_payload.py
--schema` gives the format):

- **`term_clusters`** — read this first. Each cluster is one word garbled several ways across
  different sites; one glossary entry settles all of them. In testing, one clinical term appeared
  garbled four different ways across four separate sites. Clustering is a hint, not a verdict —
  roughly a tenth of judgment sites, and some are wrong, so glance and move on.
- **`sites`** — spans where sources split with no majority. `references/reconciliation-rules.md`
  covers how to resolve them and when to flag. A resolution replaces *exactly* the span shown in
  `said`. Watch `adjacent_to`.
- **`filler`** — decided per group, since sixty "um"s are one decision. Remove unambiguous groups
  wholesale; for `hedge`, `restart`, `false_start`, and words like "right", "well", "actually",
  read the samples and keep the group or spare ids with `filler.keep`.
- **`coverage_gaps`** — passages another source has that the anchor missed. Real speech the anchor
  dropped (include) or a hallucination (don't); see the rules file.

Also set `speakers`, `glossary`, `meta`, and `title`. Include a `Model` row in `meta` naming the model that made these decisions.

### 6. Build the document — the lean pass is the default

```bash
python3 scripts/build_payload.py alignment.json decisions.json --out payload.json
python3 scripts/build_transcript_docx.py payload.json --out "Combined Transcript - <Name> - <YYYY-MM-DD>.docx"
```

The lean pass is what you get by default, because conclusions do not depend on the fine detail
(`--full` flags wording ties too, for a deeper pass). Checked against a
real summary card: every claim on it was supportable from a single recording, and what combining
changed was whether the person could be quoted *verbatim*. So:

- **Wording-only ties take the anchor's reading** and are counted in the header, with their
  timestamps listed so the consultant can see which spans were decided that way. In testing this
  was about a third of the sites needing judgment.
- **Figures, names and negations still flag.** Those are the categories that reach a deck.

Resolve sites yourself only where you have real evidence — the glossary, coherence, a search.
Otherwise leave them and let them flag. Flagging is cheaper than deciding and more honest.

Four checks will stop or change the build. They exist because each one caught a real defect:

- **A resolution no source supports is demoted to a flag.** Glossary values count as support, so
  real corrections pass.
- **Many judgment sites and zero flags refuses the build.** Deciding hundreds of sites and
  flagging none is not a credible outcome. `--no-flags-ok` overrides and records the
  acknowledgement in the document.
- **High merged-speaker share writes a disclosure note,** so unverified attribution does not read
  identically to verified attribution.
- **Every appendix row gets a marker.** A site spanning a turn boundary has no placeholder in the
  text, so its marker attaches to the site's own turn. Any that still cannot be placed are named in
  a warning — resolve those before sending the document.

Take the coverage warning seriously — output much shorter than the longest source means dropped
passages.

### 7. Work through the flags with the user

A real step, not a courtesy. Walk the conflicts in appendix order with timestamp, competing
versions, and your best guess. Batch them — fifteen flags shouldn't mean fifteen round trips. If
the user has audio, the timestamp says where to listen.

The document also carries a second appendix listing the figures, names and negations that were
**settled by majority without anyone reading them**. Nothing there is known to be in doubt; it is
there so those few can be spot-checked against the recording.

Update `decisions.json` and rerun step 6. Resolved items leave the appendix; anything deliberately
left open stays flagged with `"status": "reviewed-unresolved"`, because "nobody looked" and "we
looked and still can't tell" mean different things to the next reader.

When a resolution teaches you a term, add it to `glossary.md` — including the project copy — and
rerun. The glossary applies everywhere, so one correction usually fixes several places.

### 8. Offer the deeper pass

End by telling the consultant what is still open, with the number in front of them:

> *"31 substantive disagreements remain open — figures, names and negations the sources split on.
> A deeper pass would work through them; roughly twenty minutes."*

Offer it when the count is high, when only two sources were available so nothing could be settled
by vote, when speakers are still merged, or when this interview is one they intend to quote in the
deck. A transcript with forty open flags is hard to trust even if nothing gets quoted.

**The deeper pass is a continuation, not a new run.** Add resolutions to the existing
`decisions.json` and rebuild — same filename, resolved items drop out of the appendix. So keep
`normalized/`, `alignment.json` and `decisions.json` until the consultant confirms they are done,
and add a header line saying a deeper pass was applied and when. Two people holding the same
filename otherwise cannot tell whose copy has been worked through.

### 9. Hand off

Present the file and ask where it belongs: `materials/` in the project folder, or SharePoint.
Default local, offer SharePoint.

Then offer derived versions from `references/summary-formats.md` — executive summary, key quotes,
themed findings, and the Newry summary card that hands off into Interview Coding & Synthesis. All
summaries derive from the approved transcript, and quotes must be exact.

## Notes

- Synthesis *across* interviews belongs to Interview Coding & Synthesis. This skill's job ends at
  a trustworthy transcript.
- Never invent content to bridge a gap. If every source is unintelligible, that is
  `[inaudible 12:34]` — an honest gap is useful, a plausible guess is a liability.
- `examples/` holds a synthetic five-format fixture for smoke-testing the scripts. It is excluded
  from distribution, so it exists only in the build repo.
- If the `Write` tool can't reach the working directory, don't fall back on bash heredocs. Write
  small JSON decision files with `python3 -c` reading from a path.
