# Decisions Made — Template

Used at the end of Mode 1 signal cards and Mode 2 Roll-up output. Audit trail of every non-trivial inference the skill made during the run. Scan for anything that looks wrong; correct after the fact.

```
## Decisions made

### Scope
- Branches synthesized: [list]
- Branches excluded: [list with one-line reason each]
- Ambiguous branches included: [list with reasoning]
- Outside the Issue Tree volume: [e.g., "12% of substantive exchanges across the corpus mapped Outside" or "Transcripts IS-7 and IS-12 had >40% of content map Outside"]

### Files
- Files loaded: [count]
- Combined-file splits performed: [count, with boundary points]
- Tracked changes / comments encountered: [list of files; skipped]

### Filename ↔ person matching
- Confirmed mappings: [count]
- Ambiguous mappings, skill's call: [list]

### Term fixes
- Applied (high-confidence): [table grouped by canonical fix with counts — e.g., altar→Alta ×7]
- Best-inference applied (med/low confidence, high-impact): [list with confidence and reasoning — review if needed]
- Skipped (low-impact): [count]
- Glossary entries added this run: [count]

### Input quality
- [Per-transcript classification, especially anything downgraded to Low attribution]

### Frame interpretation
- [If frame was non-issue-tree, what was assumed]
```
