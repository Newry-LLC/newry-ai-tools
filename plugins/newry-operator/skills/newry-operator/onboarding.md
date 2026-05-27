# Welcome to the Newry AI Program — Builder Orientation

Your guide as a program builder: what exists, how it's designed, how to use the operator
tools, and where to find things.

**Audience:** Anyone building or stewarding the Newry AI program.

---

## What the program is

A knowledge-activation layer over the firm. Its job: make Newry's methodology, IP, and
institutional knowledge show up at the point of use — inside consultant workflows, without
interruption.

**North star metric:** Active weekly usage rate — % of Newry consultants with ≥1 tool run
in the trailing 7 days (30-day rolling average).
Targets: 25% by Oct 2026 · 50% by Jan 2027 · 80%+ by May 2027

**Ambition level:** L3 — execution transformation and behavioral shift. Horizon: May 2027.

---

## What exists today

| Plugin | Purpose | Status |
|---|---|---|
| newry-knowledge | SharePoint + Airtable search, consultant tool directory | Active |
| Primary Research Toolkit | End-to-end interview research workflow (6 sub-skills) | Active |
| SoF Toolkit | Summary of Findings evaluate / align / draft | Active |
| RMA-OA Builder | Rapid Market Assessment workflow | In progress |
| Project Technical Onboarding | Week-1 technical orientation document | In progress |
| Project Launch Toolkit | Project kickoff workflow | Backlog — highest priority |

For current versions and status: `strategy/program-status.md`.
For all plugins with training links and open items: `strategy/plugin-index.md`.

---

## How to use this plugin

Describe what you're trying to do — the right skill activates automatically.

- **Design question** → `program-advisor` — applies principles + decision history, surfaces trade-offs, recommends
- **Log a decision** → `decision-capture` — structured intake, writes to shared logs folder, merges to canonical snapshot
- **Prioritize backlog** → `build-prioritization` — reads program status + principles, produces ranked recommendation
- **Quality review** → `plugin-reviewer` — runs Plugin Auditor three-pass audit before shipping

---

## How to build and ship

Always in this order:

1. **Build** — write the SKILL.md
2. **Audit** — run `plugin-reviewer` on what changed
3. **Fix** — apply findings
4. **Package** — run Plugin Builder → `outputs/<plugin-name>.plugin`
5. **Update index** — `strategy/plugin-index.md` + xlsx
6. **Reinstall** — uninstall old version in Cowork, install new
7. **Push** — push `.plugin` to `Newry-LLC/newry-ai-tools`; auto-update distributes

---

## Key reference docs (bundled in this plugin)

- `references/principles.md` — 15 design principles; the durable decision-making rules
- `references/north-star.md` — the program horizon and north star metric
- `references/vision.md` — vivid May 2027 end state

## Live docs (read from Cowork working folder at runtime)

- `~\Newry Corp\Clients - Claude Master Working Folder\logs\newry-operator\decision-log.md` — running log of design decisions; **read before designing anything new**
- `strategy/program-status.md` — current state, plugin versions, next priorities
- `strategy/plugin-index.md` — all plugins with versions, logs, training materials

---

## Where things live

| What | Where |
|---|---|
| Plugin source | `Building Tools for Newry/plugins/` |
| Packaged plugins | `Building Tools for Newry/outputs/` |
| Strategy docs | `Building Tools for Newry/strategy/` |
| Decision log | `~\Newry Corp\Clients - Claude Master Working Folder\logs\newry-operator\decision-log.md` |
| Usage logs | `~\Newry Corp\Clients - Claude Master Working Folder\logs\usage-log-<user_id>.jsonl` (one file per consultant) |
| Feedback logs | `~\Newry Corp\Clients - Claude Master Working Folder\logs\feedback-log-<user_id>.md` (one file per consultant) |
| GitHub repo | `Newry-LLC/newry-ai-tools` (private) |
