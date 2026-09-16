# Reconciliation rules

Read this when deciding the `sites` and `coverage_gaps` in `alignment.review.json`.

The aligner has already done the mechanical work: matched the sources word by word, kept what they agree on, settled disagreements with a clear majority, and refused to let a source that dropped content vote for deleting it. What reaches you is what evidence alone couldn't settle. So this file is only about judgment.

## 1. Resolving a site

Each site shows what every source said across the same span. Work down this list and stop at the first level that resolves it confidently.

**1. Semantic coherence.** Does one version make sense in context and the other not? A reading that is grammatical, responsive to the question just asked, and consistent with what the speaker said earlier is almost certainly the real one. Garbled transcription produces near-misses that are phonetically close but semantically empty. This resolves most sites.

**2. The glossary.** If one source says "naphion" and another "Nafion" and Nafion is in your glossary, that's settled. Same for company names, products, people, acronyms. Put these in `decisions.json`'s `glossary` rather than resolving site by site — it applies everywhere and catches the same error elsewhere in the call.

**3. Phonetic plausibility.** Candidates should sound like the same audio. One that is phonetically distant from the others is more likely that tool's guess than a better hearing. Conversely, when two sources converge on similar-sounding nonsense, the truth is often a real word that sounds like both: "derisk the shuttle chain" + "derisk the supply chain" → supply chain.

**4. Source reliability.** See §2. The weakest level — enough to break a tie, not to overrule coherence or the glossary.

If nothing resolves it, flag it. Don't fall back on "pick the longest" or "pick the anchor" — an arbitrary choice that reads smoothly is worse than an honest flag, because nobody will ever catch it.

Two mechanical notes. A resolution replaces **exactly** the span shown in `said`: if the variants are "Veltrix" and "Veltrex", write "Veltrix", not "Veltrix Polymers", or the next word appears twice. And check `adjacent_to` — neighbouring sites are often one garbled phrase the aligner split in two, and deciding them independently can leave the halves contradicting each other.

## 2. What each tool tends to get wrong

Priors, not rules. Verify against what you see.

**Otter** — Strong turn boundaries and timestamps; usually the best anchor. Weak on jargon and proper nouns, which it renders as similar-sounding common words. Can misattribute short interjections.

**Granola** — Better on proper nouns and company names, having the meeting title and agenda as context. Notes-oriented, so completeness varies and speaker labelling is less consistent. Watch for coverage gaps.

**Teams / Outlook auto-transcript** — Best speaker attribution, knowing who was on which audio channel. Weakest on domain vocabulary, and confidently so. Usually complete, which makes it a good check on whether another source dropped something.

**PDFs** — A wrapper around one of the above; work out which and use its priors. A PDF export and a live pull from the same engine are one witness, which is what `:GROUP` on the command line is for.

**Human or note-taker transcripts** — Accurate on meaning and terminology, but usually paraphrased. Excellent for working out *what was meant*; don't lift its phrasing as verbatim unless another source corroborates the exact wording.

## 3. When to flag

Flag when you couldn't resolve a site with confidence — meaning you'd be uncomfortable if a consultant quoted your choice to the client. Sites left undecided are flagged automatically, which is the safe default.

The categories where you should work the hierarchy properly rather than let a plausible reading substitute for evidence:

- **Numbers.** "$40m" vs "$14m", 40% vs 14%, 2023 vs 2013. These get quoted and put into models. Coherence rarely helps — both readings are usually plausible — and phonetic similarity is exactly why the error happened. If a number reached you, no majority settled it, so flag unless context genuinely decides. Never pick the rounder number or the one that fits your sense of the market.
- **Negations and modals.** "will" vs "won't", "can" vs "can't". Tiny audio difference, inverted meaning. Context often does resolve these: a speaker who has just explained why a timeline is immovable said "won't".
- **Named entities.** Check the glossary, then try a search — tools garble proper nouns constantly and the right spelling is usually public. Flag what survives both.
- **Attribution disputes on substantive claims.** A quotable claim on the wrong person's lips is worse than a garbled word, because it looks correct.
- **Passages where every source is incoherent.** Resolve to `[inaudible MM:SS]` and flag it.

Don't flag punctuation, capitalization, or wording differences that don't change meaning. Over-flagging trains the reviewer to skim the appendix, which defeats the point. Ten or fifteen substantive flags on an hour-long interview is a reasonable order of magnitude.

Each flag needs enough for the reviewer to decide without opening the sources: what each source said, why it's unresolved, your best guess, your confidence. `build_payload.py` writes a serviceable default `issue` from the site's category and coverage; override it when you know something more useful.

## 4. Coverage gaps

A gap is a passage another source has that the anchor lacks. Two possibilities, needing opposite treatment.

**Real speech the anchor dropped.** Include it. A missing passage is worse than a wrong word, because a reader cannot detect it. Set the speaker if the source's label looks wrong.

**A hallucination.** Tools sometimes generate fluent text that was never spoken — in silence, over crosstalk, at recording boundaries. Tests: does it respond to what came before? Does the timing leave room for it? Is it suspiciously polished next to the surrounding speech? If one source has thirty seconds of clean narration where the others have a pause, distrust it.

When you can't tell, include it and flag it. An unresolved passage the reader can see beats a passage silently dropped.

## 5. Speaker attribution

Map the sources' labels to real people in `decisions.json`'s `speakers`, as `Name (Company)` or `Name (Newry)`.

Use the roster from step 1, self-identification in the opening minutes, and role-consistent content — the person answering detailed questions about a manufacturing line is the operations person. Interviewer and interviewee are usually easy to tell apart by function: questions versus answers. Don't consult calendars.

If two people can't be reliably distinguished — same company, similar voices, overlapping talk — say so in the header `notes` rather than guessing turn by turn. A note that two speakers may be conflated in places is honest; silently guessing two hundred times is not.

## 6. Failure modes

**Smoothing.** The strongest pull is toward making the transcript read well. Real speech is full of restarts and half-sentences; if your output reads like written prose, you have edited meaning into it. Preserving bad grammar is the job. The pipeline protects you here — text the sources agreed on passes through untouched — so this risk now lives entirely in the resolutions you write.

**Over-wide resolutions.** Writing a whole phrase where the site covers one word, duplicating text in the output. `build_payload.py` warns; don't ignore it.

**Hallucination laundering.** Accepting a coverage gap because it reads well. See §4.

**Glossary drift.** Spelling a term one way early and another way late. Using `glossary` instead of per-site resolutions prevents this by construction.

**False confidence.** Resolving a site because a version reads better rather than because evidence supports it. The reviewer trusts unflagged text completely — that trust is the product.
