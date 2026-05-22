# Principles — Newry AI Program

**Version:** v0.6 — 2026-05-15
**Audience:** anyone building, scoping, reviewing, or governing a Newry AI tool

## Operating Philosophy

The firm already knows a lot. Years of client engagements, frameworks, decisions, deliverables, operating practices, and accumulated judgment. What the firm doesn't have is a way to make that knowledge show up at the point of use. Documents sit in folders. Prior decisions get re-made because no one recalls them. Past deliverables don't surface as precedent. Methodology exists but isn't pulled in mid-engagement. Every consultant starts partly from scratch, every time.

The program's job is to close that activation gap. **Knowledge is made operational by being read by a system at the point of use — not by being filed, found, and re-read by a human.** The AI program is a knowledge-activation layer over the firm. Everything downstream flows from this.

Two operating rules:

- **AI Program Specifications each get their own dedicated reader.** The documents that define how the program works — strategy, principles, methodology, eval spec, tier framework, naming conventions, north star — are small in number and read deliberately. Each earns a specific skill built to consult it: the Program Concierge reads the Program Foundations; the Eval runner reads the eval spec. If a specification has no reader, it will decay — either build the reader or cut the specification.

- **Firm Knowledge is instantly accessible through any tool's prompt interface.** The firm's existing body of work — past deliverables, client frameworks, engagement archives, the Project Launch Toolkit, templates, everything on SharePoint — is large, heterogeneous, and pre-exists the program. It earns search: one index across the whole body, queried piece-by-piece by any tool that needs a fragment. A consultant using the SoF Toolkit pulls a relevant client framework mid-work, without leaving the tool.

---

## Principles

## 1. Client confidentiality is inviolable.
Client material never leaves Newry's systems for training, indexing, or any other secondary use. Tools handle client data as if it is always potentially sensitive. This principle overrides every other principle in this document.

## 2. Tools don't make the call.
Tools draft, structure, scan, synthesize, and flag — but judgments about what matters, what the client should do, and what the recommendation is remain human. A tool that implies it has the answer is miscalibrated and should be redesigned.

## 3. Newry-grade quality is non-negotiable.
The quality floor a tool produces is set by what Newry would put in front of a client, not by what the model produces generically. Faster-but-worse is not shipping.

## 4. Build for jobs-to-be-done.
Every tool exists because a consultant has a real task. Design from that task — not from a tidy abstraction, not from what the technology makes easy, not from what looks impressive in a demo. Every plugin should name the job it does and the consultant it serves.

## 5. Less is more.
We don't codify what the model already knows. Rules get added only when they encode Newry-specific calibration, firm IP, or a standard the model won't hit on its own.

## 6. Test before iterating.
Observations from real material drive changes; hunches don't. Run the tool against fresh input before modifying it.

## 7. Use is the primary signal.
Tools evolve based on observations from real use. Feedback from consultants running the tool in real engagements is the primary input to improvement.

## 8. Plugin-as-unit.
Every module is structured as a Cowork plugin from day one — clean scoping, native deployment shape, independent evaluation. Shared infrastructure is pulled out deliberately, not left accidentally coupled across plugins.

## 9. Firm knowledge compounds, or the program isn't working.
Each plugin should make the next one faster to build. Methodology, patterns, and IP captured in one place should be reusable in another.

## 10. Freed capacity gets redirected by design.
Tools create the conditions for the behavioral shift the vision commits to; leadership makes it real. The program is measured not by how many hours AI saves, but by whether the freed hours land on client thinking, judgment work, and relationship depth.

## 11. Build the capability, not just the tool.
Every plugin is also Newry learning to ship AI products — with real user discovery, eval rigor, versioned release, and observable use.

## 12. Write to open standards.
Author plugins to the open Agent Skills (`SKILL.md`) specification. The asset Newry is building is in the skill files themselves — the platform is replaceable.

## 13. Shared dependencies degrade gracefully.
Shared components are enhancements, not hard requirements. If a shared dependency is missing or fails, the calling skill notes the degradation clearly and continues in a reduced mode.

## 14. Simple mode before full mode.
Every file-writing skill supports two run modes. Full mode enforces complete folder structure and SharePoint sync. Simple mode requires only that any folder is mounted. Skills are designed for simple mode first.

## 15. Revisit the architecture regularly.
As plugins multiply and shared components accumulate, coupling risks grow silently. Schedule a periodic architecture review — at minimum once per program phase.
