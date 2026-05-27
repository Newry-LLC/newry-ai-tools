# Primary Research Toolkit — Feedback Log

User-reported feedback, issues, and improvement suggestions captured during PRT runs. Append-only log. Triage runs read this and propose script fixes, SKILL.md sharpening, eval cases, or design-backlog additions.

**Schema (one entry per item):**

```
---
Date: [YYYY-MM-DD HH:MM TZ]
Run reference: [project / mode / scope summary | "general — no specific run"]
Reporter: [name if known, else "user"]
Classification: [bug | friction | quality | feature | question]
Severity: [low | medium | high]
User's words: "[verbatim quote]"
Context: [what the skill was doing or what the user was reacting to]
Status: [open | triaged | resolved | wont-fix]
```

**Classification key:**
- *bug*: script error, broken behavior, malformed output.
- *friction*: hard to use, unclear instructions, wasted user effort.
- *quality*: wrong finding, off synthesis, inaccurate attribution.
- *feature*: capability not currently in the skill.
- *question*: user asking how to do something — log so we can sharpen instructions.

**Severity key:**
- *high*: blocks the run; output the user can't use; quality issue that misrepresents an interview.
- *medium*: slows the run; correctable quality issue.
- *low*: feature wish, minor friction, question.

---

---
Date: 2026-05-04 15:30 ET
Run reference: ALTA01 / ICS Mode 1+2 prep / 55-transcript corpus (Pre-processed v4)
Reporter: self-recognized during Sylvan-directed run (not user-reported)
Classification: bug
Severity: high
User's words: (n/a — observed during run)
Context: `preprocess.py` `OTTER_TURN_RE` had catastrophic regex backtracking at file sizes >~10KB. Hung indefinitely on a 51KB Doug Hofer transcript at 99% CPU. The pattern `(?:.+\n?)+?` with the lookahead caused exponential backtracking. The prior 10-transcript run worked because those files happened to fall under the cliff. At 55-transcript scale (some files up to 53KB) it became a hard blocker. Replaced with a line-based parser (O(N), no regex backtracking risk).
Status: resolved (fix applied 2026-05-04)

---
Date: 2026-05-04 15:35 ET
Run reference: ALTA01 / ICS Mode 1+2 prep / 55-transcript corpus
Reporter: self-recognized during run
Classification: bug
Severity: high
User's words: (n/a — observed during run)
Context: `SPEAKER_LINE_RE` excluded digits from the speaker-name character class. "Speaker 1" / "Speaker 2" lines failed to parse as speaker headers, getting absorbed as body text of the prior named-speaker turn. For all-Speaker-N files (Peter Ross, Lora Kilgore, Benito Rodriguez, Mark Cooper, Thomas Skelskey, Bret Thomas) the script parsed 0 turns. Fixed by adding `0-9` to the speaker-name character class.
Status: resolved (fix applied 2026-05-04)

---
Date: 2026-05-04 15:40 ET
Run reference: ALTA01 / ICS Mode 1+2 prep / 55-transcript corpus
Reporter: self-recognized during run
Classification: bug
Severity: high
User's words: (n/a — observed during run)
Context: `match_filename_to_person` used `last in base` substring search, causing cross-contamination on shared last names. Joy Bennett intercepted Shawn Bennett's file (last=Bennett); Bret Thomas intercepted Thomas Skelskey's file (Bret's last=Thomas, matched first name of Thomas Skelskey). Surface symptom: duplicate entries in INDEX.md and incorrect role/date metadata on cards. Fixed by switching to a token-based matcher that requires whole-word overlap and prefers full-token matches.
Status: resolved (fix applied 2026-05-04)

---
Date: 2026-05-04 15:50 ET
Run reference: ALTA01 / ICS Mode 1+2 prep / 55-transcript corpus
Reporter: self-recognized during run
Classification: bug
Severity: medium
User's words: (n/a — observed during run)
Context: When the interviewee's actual name doesn't appear as a speaker label (Otter labels them "Unknown Speaker" or "Speaker N"), `resolve_speakers` could not identify `interviewee_label`, leaving every turn at role "?" — so EU segmentation flagged 0 substantive EUs. Affected 5 files (Brett Kovach, Jamie Haines, Marcello Cazzulo, Michael Sumner, Guy Schneider). Added an aggregate-words fallback: when no name-based match, the speaker with the most aggregate words is treated as the interviewee (medium-low confidence, surfaced in Speaker resolution notes). Also refined the all-Unknown branch: when multiple distinct Speaker N labels exist, use the dominant-speaker signal instead of alternation.
Status: resolved (fix applied 2026-05-04)

---
Date: 2026-05-04 15:55 ET
Run reference: ALTA01 / ICS Mode 1+2 prep / 55-transcript corpus
Reporter: self-recognized during run
Classification: quality
Severity: low
User's words: (n/a — observed during run)
Context: Header field "Attribution reliability: High" is set from input quality (verbatim transcript) without considering speaker resolution confidence. For files where speaker resolution is medium-low (e.g., aggregate-words fallback) or low (alternation), attribution should be downgraded so synthesis paraphrases instead of citing verbatim. Workaround for this run: speaker resolution notes are still in the file body and ICS Mode 1 is instructed to read them; future fix would be to compute a combined attribution = min(input_quality_attribution, speaker_resolution_confidence).
Status: open


---
Date: 2026-05-08 ET
Run reference: ALTA01 / Research Plan Design / Chunk 1 — branch prioritization
Reporter: Sylvan
Classification: quality
Severity: medium
User's words: "these internal interviews should not be treated the same as external in terms of covering the issue tree"
Context: In Chunk 1 branch prioritization, Claude classified A6 (Technical fit / right to win) as Secondary and Foundational as Secondary, citing internal corpus coverage as partial justification. The internal corpus (55 Alta sales/ops interviews) is inside-out — it reflects what Alta's team believes about the market, not external market validation. Treating it as coverage for any branch in an external research plan is incorrect. Every branch starts at zero until external voices address it.
Fix applied: Two edits to `sub-skills/research-plan-design/SKILL.md` — (1) added interviewee-type check to "Also look for" in Step 1; (2) added explicit decision rule: internal-only corpus does not reduce branch priority for external research planning.
Status: resolved
