# Principles — Newry AI Program

**Version:** v0.7 — 2026-07-10
**Audience:** anyone building, scoping, reviewing, or governing a Newry AI tool

## Changelog

- **2026-07-10 (v0.7)** — Six-principle revision (see decision log 2026-07-10). #2 reframed "tools don't make the call" → "tools propose; the human decides" (judgment permitted if transparent + defeasible + stakes-gated). #8 dropped "Cowork plugin" for the platform-neutral "self-contained unit to the open SKILL.md spec." #10 relocated to `vision.md` (a program-purpose/measurement claim, not a design rule). #11 split — ambition to `vision.md`, its four build-discipline habits to `skill-authoring-standard.md` §3A. #12 sharpened and softened (Claude-specific specs OK, flag them). #13 exception widened to "client data or output integrity." Numbers retained (no renumbering) to keep external citations stable; #10/#11 left as relocation stubs. Craft guidance now lives in the new `skill-authoring-standard.md`.
- **2026-05-15 (v0.6)** — Added Principles #13 (Graceful degradation), #14 (Simple mode first), and #15 (Regular architecture review).
- **2026-04-28 (v0.5)** — Terminology updates in Operating Philosophy: "strategy stack" → "Program Foundations"; "Orientation skill" → "Program Concierge." Both renames adopted across the live program docs to reflect more accurate, plain-language naming.
- **2026-04-28 (v0.4)** — Added Principle #12 ("Write to open standards"). Anchors the program's authoring discipline to the open Agent Skills (`SKILL.md`) specification, which became an open standard in December 2025 and now runs across Claude Code, Cowork, Cursor, Gemini CLI, and Codex CLI. The investment is in the skills themselves, not in any one AI platform.
- **2026-04-23 (v0.3)** — Added Principle #11 ("Build the capability, not just the tool") to encode the forward-looking implication of the L4 redefinition: if the future ambition is net-new AI products, the L2/L3 work has to build the muscle to ship AI products, not just automate consulting. Updated the Operating Philosophy "Relationship" paragraph to reference the new principle.
- **2026-04-23 (v0.2)** — Operating Philosophy added.

## Operating Philosophy

The firm already knows a lot. Years of client engagements, frameworks, decisions, deliverables, operating practices, and accumulated judgment. What the firm doesn't have is a way to make that knowledge show up at the point of use. Documents sit in folders. Prior decisions get re-made because no one recalls them. Past deliverables don't surface as precedent. Methodology exists but isn't pulled in mid-engagement. Every consultant starts partly from scratch, every time.

The program's job is to close that activation gap. **Knowledge is made operational by being read by a system at the point of use — not by being filed, found, and re-read by a human.** The AI program is a knowledge-activation layer over the firm. Everything downstream flows from this.

Two operating rules:

- **AI Program Specifications each get their own dedicated reader.** The documents that define how the program works — strategy, principles, methodology, eval spec, tier framework, naming conventions, north star — are small in number and read deliberately. Each earns a specific skill built to consult it: the Program Concierge reads the Program Foundations; the Eval runner reads the eval spec. If a specification has no reader, it will decay — either build the reader or cut the specification.

- **Firm Knowledge is instantly accessible through any tool's prompt interface.** The firm's existing body of work — past deliverables, client frameworks, engagement archives, the Project Launch Toolkit, templates, everything on SharePoint — is large, heterogeneous, and pre-exists the program. It earns search: one index across the whole body, queried piece-by-piece by any tool that needs a fragment. A consultant using the SoF Toolkit pulls a relevant client framework mid-work, without leaving the tool.

**Grounding.** The philosophy only holds if the mechanisms are real. A dedicated reader is a live skill that loads a specific document on demand — not a document with a table of contents. Search over firm knowledge is a working retrieval system with current indexing — not a search bar over a shared drive. Where the mechanisms don't yet exist, the claim is aspirational, not operational — and the next move is to build the mechanism, not rewrite the claim.

**Relationship to the principles below.** The eleven principles are craft rules for how to build well within this frame. *Plugin-as-unit* is about packaging knowledge-activation cleanly. *Less is more* is about not codifying what the model already knows, so the reader can lean on model strength. *Use is the primary signal* is about whether activation is actually happening in practice. *Build the capability, not just the tool* is about what the program leaves behind — not just plugins, but the organizational muscle to build more of them, including the ones clients will eventually buy. Where principle and philosophy conflict, the philosophy governs.

---

## Principles

These are the durable decision-making rules that resolve tradeoffs across the program. Each is meant to be *usable* — the kind of rule that can kill a proposal, settle a design debate, or set the bar in a review. Where principles conflict, the earlier one wins.

## 1. Client confidentiality is inviolable.

Client material never leaves Newry's systems for training, indexing, or any other secondary use. Tools handle client data as if it is always potentially sensitive. This principle overrides every other principle in this document.

## 2. Tools propose; the human decides.

Tools may do judgment work — rank, resolve contradictions, assess fit — **but only transparently and defeasibly**: the judgment is shown with its reasoning, framed as a proposal (never "the answer"), easily overridable, and contestable (alternatives shown, low-confidence calls flagged). The confirm-gate scales with stakes — low-stakes calls can act and report after; anything that shapes what the client is told gets a gate or a prominent flag before it lands. What stays human regardless: what the recommendation *is*, what matters strategically, and what the client should do. A tool that hides its reasoning or presents one option as the answer is miscalibrated and should be redesigned.

*Craft:* `skill-authoring-standard.md` §3B is how to build such a step. The exact stakes-to-gate mapping is being settled by test (decision log, 2026-07-10).

## 3. Newry-grade quality is non-negotiable.

The quality floor a tool produces is set by what Newry would put in front of a client, not by what the model produces generically. Faster-but-worse is not shipping. Speed and scale matter, but they come after quality.

*Related:* `quality-drift.md` explains why holding this principle over time requires continuous evaluation — LLM-based tools silently degrade even with frozen text, so "Newry-grade" is a moving commitment that needs measurement, not a one-time calibration.

## 4. Build for jobs-to-be-done.

Every tool exists because a consultant has a real task. Design from that task — not from a tidy abstraction, not from what the technology makes easy, not from what looks impressive in a demo. Every plugin should name the job it does and the consultant it serves.

## 5. Less is more.

We don't codify what the model already knows. Rules get added only when they encode Newry-specific calibration, firm IP, or a standard the model won't hit on its own. When a skill misses something, the default answer is to trust the model and improve through testing — not to add a rule.

## 6. Test before iterating.

Observations from real material drive changes; hunches don't. Run the tool against fresh input before modifying it. If we haven't tested recently, we're not allowed to "improve" the tool on intuition.

## 7. Use is the primary signal.

Tools evolve based on observations from real use. Feedback from consultants running the tool in real engagements is the primary input to improvement — not designer intuition, not wish lists, not theoretical completeness. If feedback from use isn't flowing back into the program, the improvement loop isn't running.

## 8. Plugin-as-unit.

Every module is structured as a self-contained unit authored to the open SKILL.md spec from day one — clean scoping, native deployment shape, independent evaluation. Shared infrastructure is pulled out deliberately, not left accidentally coupled across plugins.

## 9. Firm knowledge compounds, or the program isn't working.

Each plugin should make the next one faster to build. Methodology, patterns, and IP captured in one place should be reusable in another. If we find ourselves re-solving the same problem in a second plugin, the answer is to extract the shared layer before continuing.

## 10. Freed capacity gets redirected by design.

*Relocated to `vision.md` (2026-07-10) — this is a program-purpose/measurement commitment, not a design decision rule. See vision.md "What this commits us to" (first commitment) and north-star.md (P&L accountability). Number retained to keep citations stable.*

## 11. Build the capability, not just the tool.

*Split (2026-07-10): the strategic ambition (net-new AI products, the L4 option) is program-horizon material — see `vision.md` "Beyond May 2027." The four build-discipline habits it named — real user discovery, eval rigor, versioned release, observable use — are now concrete craft in `skill-authoring-standard.md` §3A. Number retained to keep citations stable.*

## 13. Shared dependencies degrade gracefully.

Shared components — `project-setup`, `feedback-capture`, `preprocess.py`, and any future shared skill or script — are enhancements, not hard requirements. If a shared dependency is missing or fails, the calling skill notes the degradation clearly and continues in a reduced mode rather than blocking the run. The exception is client data integrity: if `project-setup`'s mismatch detection is unavailable, the skill should warn the consultant explicitly rather than silently skipping the check.

The exception is **client data or output integrity**: a check that protects the client's data or the correctness of an output (e.g., `project-setup`'s mismatch detection) should warn the consultant explicitly rather than silently skip.

*What this prevents:* a broken shared component taking down every skill that references it. Plugins fail locally, not systemically.

## 14. Simple mode before full mode.

Every file-writing skill supports two run modes. Full mode enforces the complete folder structure, `project.md`, SharePoint sync, and mismatch detection. Simple mode requires only that any folder is mounted — the consultant defines it, the skill writes there, and structure checks are skipped. Step 0 detects which mode applies automatically: if the expected structure is present, full mode; if not, offer simple mode rather than stopping cold. Skills are designed for simple mode first and full mode as an overlay — not the reverse.

*What this prevents:* onboarding friction that blocks first use. A consultant who hasn't set up their SharePoint folder yet should still be able to run the skill and get value.

## 15. Revisit the architecture regularly.

As plugins multiply and shared components accumulate, coupling risks grow silently. Schedule a periodic architecture review — at minimum once per program phase — to ask: what breaks together, what's too tightly coupled, what shared layer should be extracted, and what should be simplified or removed. If the program is adding plugins without reviewing the architecture, technical debt is accumulating faster than the reviews will catch.

## 12. Write to open standards.

The asset Newry is building is in the skill files themselves — the markdown that encodes how we draft strategy, synthesize research, and what counts as Newry-grade. Author to the open Agent Skills (`SKILL.md`) spec so that asset compounds independently of any one platform. Newry distributes everything inside Claude today (Cowork + Claude Code), so Claude-specific features are acceptable where they earn their place — but **flag every Claude-specific use** so a future port to a non-Claude platform is a bounded, known change rather than a hunt. Keep the portable core (name, description, progressive disclosure, degrees of freedom) genuinely portable; treat Claude-only frontmatter as a deliberate, marked choice. See `skill-authoring-standard.md` Part 2 for specifics.
