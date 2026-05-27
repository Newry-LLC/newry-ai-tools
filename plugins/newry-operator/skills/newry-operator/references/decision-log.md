# Decision Log — Newry AI Program

Running log of design decisions. Each entry captures what was decided, alternatives considered,
and the rationale. Maintained by the program team; updated via the `decision-capture` skill.

---

## 2026-05-21 · decision log in shared logs folder, per-contributor files

**Decided:** The decision log lives at `logs\newry-operator\` in the shared SharePoint Claude Working Folder. Each operator writes to their own `decision-log-<user_id>.md`; a merge step regenerates `decision-log.md` as the canonical snapshot after every write. Supersedes the 2026-05-19 GitHub decision.
**Alternatives considered:** GitHub as source of truth (blocked by proxy in Cowork sandbox); single shared file in logs folder (SharePoint sync conflicts if two operators write simultaneously); Cowork working folder only (not shared across machines).
**Rationale:** Same SharePoint folder both operators sync eliminates the distribution problem. Per-contributor files eliminate sync conflicts. Merge-on-write means the canonical snapshot is always current without any coordination between operators.

---

## 2026-05-21 · per-consultant usage log files, aggregated by log-reader

**Decided:** Each consultant writes to their own `usage-log-<user_id>.jsonl` file (keyed by the anonymous UUID in `~/.user_id`) rather than a single shared `usage-log.jsonl`.
**Alternatives considered:** Single shared log file at the central path (prior implementation).
**Rationale:** A shared file causes SharePoint Sync conflicts when two consultants run skills simultaneously. Per-consultant files eliminate concurrency issues; the log-reader aggregates across all `usage-log-*.jsonl` files in the logs folder to produce firm-wide metrics.

---

## 2026-05-19 · decision log lives in github, updated via skill

**Decided:** ~~`decision-log.md` lives in the `Newry-LLC/newry-ai-tools` GitHub repo.~~ **Superseded 2026-05-21** — GitHub API unreachable from Cowork sandbox. See 2026-05-21 decision above.
**Alternatives considered:** SharePoint (familiar but requires M365 connector); Cowork working folder only (no auto-distribution); bundled static markdown (requires manual repackage).
**Rationale:** Superseded. GitHub approach blocked by proxy.

---

## 2026-05-18 · operator plugin audience is program builders, not matt alone

**Decided:** The operator plugin is designed for anyone building or stewarding the Newry AI program — current or future contributors — not Matt specifically.
**Alternatives considered:** Solo-Matt design (higher hand-holding, more onboarding scaffolding).
**Rationale:** The program needs to be transferable. Calibrating to "program builders" generalizes correctly and doesn't require redesign as the team grows.

---

## 2026-05-06 · tool directory distributed via plugin install

**Decided:** The consultant-facing tool directory is a Cowork artifact delivered via the `newry-knowledge` plugin, not a shared SharePoint link.
**Alternatives considered:** SharePoint page; static HTML shared via email; Cowork artifact without plugin.
**Rationale:** Plugin install ensures everyone on the program has the same version; artifact auto-updates via GitHub auto-update; no SharePoint page to maintain.

---

## 2026-05-04 · cga absorbed into ics mode 2, not standalone sub-skill

**Decided:** Coverage & Gap Analysis is a mode of the Interview Coding & Synthesis skill, not a standalone PRT sub-skill.
**Alternatives considered:** Standalone CGA sub-skill; separate plugin.
**Rationale:** CGA only makes sense post-synthesis with the same corpus; keeping it in ICS avoids context duplication and scope confusion. Four enhancements tracked as ICS Mode 2.

---

## 2026-05-04 · feedback capture recognition-based, not prompted

**Decided:** Feedback is captured when Claude recognizes positive/negative signals in the conversation, not by prompting the user at the end of every run.
**Alternatives considered:** End-of-run prompt ("how did this go?"); thumbs up/down widget.
**Rationale:** Frictionless for the consultant; captures signal from real reactions; keeps conversation focused on work. Triage happens separately from capture.

---

## 2026-05-04 · sharepoint = source of truth; cowork = execution surface

**Decided:** All project files live on SharePoint; Cowork/Claude Code is the execution surface only. File-based markdown manifest (`project.md`) bridges the two.
**Alternatives considered:** Cowork as primary storage; local-only workflow.
**Rationale:** SharePoint is already the firm's source of truth; consultant familiarity; M365 connector enables Claude to read from it without duplication.

---

## 2026-04-28 · rag ruled out; m365 connector handles freshness

**Decided:** Use the M365 SharePoint Search connector rather than building a RAG pipeline over SharePoint.
**Alternatives considered:** Custom RAG (vector DB + chunking + retrieval pipeline over SharePoint).
**Rationale:** M365 connector handles freshness automatically; RAG complexity not worth the maintenance overhead at current program scale; SharePoint Search is sufficient for document retrieval use cases.

---

## 2026-04-28 · coordinator pattern for multi-skill plugins

**Decided:** Use gate-first coordinator routing in all multi-skill plugins (is this Newry-specific? → what type of task?).
**Alternatives considered:** Flat skill list with Claude selecting from descriptions; single monolithic skill.
**Rationale:** Gate-first routing provides cleaner separation of concerns, prevents off-target triggers, and makes routing logic legible to maintainers.
