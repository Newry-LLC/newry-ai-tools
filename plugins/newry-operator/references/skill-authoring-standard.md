---
type: reference
version: 0.2
last_updated: 2026-07-10
description: How Newry authors a skill well — the craft layer between the principles (why) and the plugin-auditor (review). Portable-core backbone from Anthropic guidance, sharpened with Newry-specific build discipline. Machine-usable: every rule is tagged mechanical or judgment, with a matching audit checklist.
---

# Skill-Authoring Standard — Newry AI Program

The craft guide for building a Newry skill. It sits between two documents:

- **Above — `strategy/principles.md`** (the 15 principles: what to build, what a tool may do, what "done" means). Cite by number where one governs; do not restate.
- **Below — `plugins/plugin-auditor/SKILL.md`** (the review bar). Its passes derive their checks from this standard's checklist.

Also connects to `strategy/quality-drift.md` — why every shipped skill carries evals.

**Audience:** anyone authoring or auditing a Newry skill. Loaded by Program Advisor at design time; the Plugin Auditor checks against the checklist below.

**Use:** apply Parts 1–3 when building; run the Part 4 checklist before review. Deep source detail (exact limits, the Claude A/B eval loop, surface-specific constraints, primary Anthropic source links) lives in `strategy/skill-authoring-research.md` — point to it, don't reproduce it.

## Rule tags

Every rule carries one:

- **`[M]` mechanical** — deterministic pass/fail. An auditor checks it without judgment. Fail = **blocker**.
- **`[J]` judgment** — heuristic; needs reasoned assessment or a judge pass. Fail = **flag for review**.

## Scope note (Principle #12)

Newry distributes everything inside Claude (Cowork plugins + Code skills). Claude-specific specs are acceptable where useful; the asset is still the skill files. Rule: flag anything Claude-specific so a future non-Claude port is bounded. See Part 2.

## Changelog

- **2026-07-10 (v0.2)** — Rewrote imperative; tagged every rule `[M]`/`[J]`; added inline good/bad examples for judgment rules; converted the checklist to check → verify → severity. Part 2 softened (Claude-specific OK, flag it) per the same-day #12 revision.
- **2026-07-10 (v0.1)** — Initial draft. Portable core from mid-2026 Anthropic guidance; four build-discipline habits relocated from Principle #11; transparent-judgment-step guidance for the #2 revision; three frontier additions (auto-swap self-improvement rejected).

---

## Part 1 — The portable core

Works on Cowork and any Agent Skills surface. The default unless a Part 3 rule sharpens it.

### 1. Write `name` + `description` as the trigger surface

- **`[M]`** `description` ≤1024 chars, third person, no XML tags.
- **`[M]`** `name` ≤64 chars, lowercase/digits/hyphens, no "anthropic"/"claude"; gerund or verb phrase; not `helper`/`utils`/`tools`/`data`.
- **`[J]`** `description` states both *what it does* and *when to use it*, front-loads the primary use, lists concrete trigger phrases a consultant would say, and reads pushy (bias toward firing).
  - ✓ "Codes interview transcripts against a project's analytical frame and synthesizes findings across the corpus. Use when the user says 'code these interviews', 'build summary cards', 'create a roll-up', 'synthesize these transcripts'."
  - ✗ "Helps with research and interviews." (vague, no triggers, not pushy)

### 2. Keep the body lean; push detail down

- **`[M]`** Body ≤500 lines / ~2,000 words.
- **`[M]`** References one level deep from SKILL.md; any reference >100 lines opens with a TOC.
- **`[J]`** Body reads as a table of contents pointing to detail, not the detail itself. Domain-partition references so unrelated contexts never co-load. On a persistent surface every body line is a recurring cost — write standing instructions, not one-time steps. (Principle #5.)

### 3. Match degrees of freedom to fragility

- **`[J]`** Give loose prose where many approaches are valid and output depends on judgment; pin exact steps where a step is fragile, consistency-critical, or a known failure point.
  - ✓ Same skill: "Run `preprocess.py` on the transcript folder" (fragile → pinned) *and* "Lead each finding with the strategic verdict, not the topic" (judgment → prose).
  - ✗ Pseudo-precise ceremony on a judgment task, or vague hand-waving on a fragile one.

### 4. Prefer deterministic scripts over model-generated code

- **`[J]`** Put repeatable/fragile logic in a bundled script, not in prose the model re-implements each run.
- **`[M]`** Invoke scripts explicitly ("Run `X`"), and list dependencies + install command.
- **`[J]`** Scripts: solve-don't-punt (handle errors in-script); no undocumented constants; verbose, specific error messages; plan → validate → execute for destructive/batch work.

### 5. Write imperative; explain why once

- **`[J]`** Verb-first/infinitive, not second person. State rationale once and briefly. Reserve ALL-CAPS for a rule observation shows won't stick.
- **`[M]`** One term per concept, never varied; forward slashes in paths; no time-sensitive phrasing (park legacy in a collapsed block).
- **`[J]`** Offer one default path + an escape hatch, not a menu. Use input→output examples where output quality depends on style/format.

### 6. Build evals before docs

- **`[M]`** Ship ≥3 eval scenarios (`{skills, query, files, expected_behavior}`) + a scoring path.
- **`[M]`** Every skill change ships with a new or updated eval case.
- **`[J]`** Write the *minimum* instructions to close observed gaps — not everything imaginable (Principle #5). Baseline the task without the skill first.

### 7. Compose via coordinator + sub-skills

- **`[J]`** Route from a coordinator to narrower sub-skills; keep sub-skill trigger phrases distinct and non-overlapping.
- **`[J]`** When a coordinator accumulates edge-case routing branches, redesign the gate from first principles rather than adding a branch.

### 8. Reference MCP tools by full name

- **`[M]`** Every MCP tool reference is `ServerName:tool_name`. A bare name is a portability bug.

---

## Part 2 — Claude-specific features: use where useful, flag them

- **`[M]`** Do not put Claude Code-only frontmatter in a Cowork plugin — it is inert there: `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `user-invocable`, `context: fork`, `agent`, `model`, `effort`, `paths`, `hooks`, `when_to_use`, `shell`, `` !`cmd` `` injection, `$ARGUMENTS`/`${CLAUDE_SESSION_ID}` and similar.
- **`[J]`** On a Code skill, use those features where they earn their place — and flag each Claude-specific use in the skill so a future non-Claude port is a bounded change.
- **`[M]`** Write `description` to ≤1024 chars (safe across surfaces). Version the plugin (`plugin.json`), not SKILL.md frontmatter (`version`/`compatibility` are inert on Code).

---

## Part 3 — The Newry craft

### 3A. Build-discipline habits (from Principle #11)

- **`[J]`** Build from an observed consultant task; name the job and the consultant it serves (Principle #4). No observed task = guessing.
- **`[M]`** Ship with evals + a scoring path against Newry-grade (see §6; Principle #3).
- **`[M]`** Release at a stated, numbered version.
- **`[M]`** Usage logging present (real use is the improvement signal, Principle #7).

### 3B. Build a transparent, defeasible judgment step (Principle #2, revised 2026-07-10)

A tool may rank, resolve, or assess **if** the judgment is transparent and the human stays in control. Build in all four:

- **`[J]`** **Transparent** — show the reasoning and inputs, not just the verdict.
- **`[J]`** **Proposal, not conclusion** — label it as a proposed read, never "the answer."
- **`[M]`** **Overridable** — an explicit, frictionless way to change or discard it is present.
- **`[J]`** **Contestable** — show the alternatives it beat; flag low-confidence calls.
  - ✓ "Proposed order, most-cited first: A, C, B. (Alternatives weighed: recency, source diversity. B3 low-confidence — 2 sources.) Reorder freely."
  - ✗ "The top finding is A." (conclusion; no reasoning, alternatives, or override)
- **`[J]`** Scale the confirm-gate to stakes: low-stakes → act, then report the call (ICS "Decisions made"); high-stakes (shapes what the client is told) → gate or prominent flag before it lands. Exact thresholds: settled by test.
- **`[J]`** The tool never states what the recommendation *is* or what the client should do. It proposes and structures; the consultant decides.

### 3C. Frontier additions

Source: the practitioner distillation `skill_building_best_practices.md` — **secondary/practitioner**, not first-party.

- **`[J]`** **Expertise, not steps** — judgment sections read like a practitioner, not documentation. *Not blanket:* keep the fragile/mechanical spine procedural (§3).
- **`[M]`/`[J]`** **Feed failures back in-context** — recurring failure captured in `plugins/newry-knowledge/evals/skill-building-log.md` **`[M]`: an entry exists**; fix promoted into the skill at the point of failure **`[J]`**. Capture in the log, fix in the skill; don't duplicate.
- **`[M]`/`[J]`** **Self-verify before returning** — a **`[M]`** deterministic check first (outputs exist, counts non-zero, every Type-4 claim has Type-1/2 evidence), then an **`[J]`** optional judge pass only where quality can't be checked deterministically.
- **Rejected:** self-improving skills that auto-swap themselves in. Keep failure *detection*; a human decides changes (Principle #6, human-gated releases).

---

## Part 4 — Audit checklist

Run before handing to the Plugin Auditor. **Blocker** = must pass (mechanical). **Review** = flag for reasoned assessment (judgment).

| # | Check | How to verify | Severity |
|---|-------|---------------|----------|
| 1 | `description` ≤1024, third person, no XML | Count chars; read voice | Blocker |
| 2 | `name` ≤64, lowercase/digits/hyphens, no reserved words | Inspect string | Blocker |
| 3 | `description` says what + when, front-loads use, lists real triggers, pushy | Compare to ✓/✗ in §1 | Review |
| 4 | Body ≤500 lines | Count lines | Blocker |
| 5 | References one level deep; >100-line refs have a TOC | Walk the tree | Blocker |
| 6 | Body is a TOC pointing to detail; references domain-partitioned | Read structure | Review |
| 7 | Degrees of freedom match fragility | Judgment loose, fragile pinned (§3) | Review |
| 8 | Repeatable/fragile logic is a script, invoked "Run X", deps listed | Grep for inline logic vs. script calls | Review |
| 9 | Imperative voice; one term per concept; forward slashes; no dated phrasing | Read; grep terms/paths | Blocker |
| 10 | ≥3 eval scenarios + scoring path; this change adds/updates an eval | Check eval file | Blocker |
| 11 | Coordinator triggers distinct and non-overlapping | Compare sub-skill triggers | Review |
| 12 | MCP tools referenced `ServerName:tool_name` | Grep tool refs | Blocker |
| 13 | No Claude-only frontmatter in a Cowork plugin; Code-specific use flagged | Inspect frontmatter | Blocker |
| 14 | Built from a named observed task + consultant | Read the skill's stated job | Review |
| 15 | Numbered version; usage logging present | Inspect `plugin.json` + logging block | Blocker |
| 16 | Judgment step transparent, proposal-framed, overridable, contestable; gate scaled to stakes | Compare to ✓/✗ in §3B | Review |
| 17 | Tool states no recommendation / client action | Scan output spec for verdict language | Review |
| 18 | Recurring failures logged in skill-building-log.md and fixed in-context | Check log + skill | Review |
| 19 | Self-verification before output: deterministic check present (judge optional) | Find the check step | Review |
