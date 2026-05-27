# newry-operator

Operator plugin for the Newry AI program. For anyone building or stewarding the program —
not for consultant workflows.

## Skills

- **newry-operator** (coordinator) — routes to the right sub-skill
- **program-advisor** — design and architecture advisor; applies principles + decision history
- **decision-capture** — logs decisions to per-contributor files in the shared logs folder; merges to canonical snapshot; no GitHub API required
- **build-prioritization** — advises on what to build next based on program state + principles
- **plugin-reviewer** — quality review (Plugin Auditor three-pass) before shipping
- **operator-dashboard** — creates/refreshes the persistent Cowork operator dashboard artifact

## Bundled reference docs

- `references/principles.md` — 15 design principles
- `references/north-star.md` — north star statement + metric + milestones
- `references/vision.md` — May 2027 end state
- `references/plugin-index.md` — current plugin registry (name, version, status, audience)

## Live docs (read at runtime)

- `~\Newry Corp\Clients - Claude Master Working Folder\logs\newry-operator\decision-log.md` — merged decision log (canonical snapshot, shared across operators)
- `strategy/program-status.md` — current program state (Cowork working folder)

## Repository

`Newry-LLC/newry-ai-tools`
